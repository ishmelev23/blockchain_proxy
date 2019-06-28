import os
import signal

from threading import Lock, Condition
from multiprocessing.pool import Pool
from logging import getLogger

from math import ceil
from sqlalchemy.orm import Session
from web3 import Web3

import settings

from src.blockchain import Blockchain
from src.database.models.transaction import Transaction
from src.database.session import session_scope_func, session_context

logger = getLogger(__name__)


class State:
    _active = False

    def __init__(self, active: bool = False):
        self.active = active

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, value):
        self._active = value


def update_transaction_status(w3: Web3, transaction: Transaction):
    data = w3.eth.getTransactionReceipt(transaction.trx_hash)
    if not data:
        return
    transaction.blocknumber = data['blockNumber']
    transaction.blockhash = data['blockHash'].hex()


def update_transactions_statuses_task(ids: list):
    with session_context(new_engine=True) as session:
        w3 = Blockchain.get_web3()
        logger.debug("Processing transactions %s" % ids)
        txs = session.query(Transaction).filter(Transaction.id.in_(ids))
        for tx in txs:
            try:
                update_transaction_status(w3, tx)
            except:
                logger.exception("Can't update transaction status for tx with id %d" % tx.id)


@session_scope_func
def get_transactions_ids(session: Session) -> list:
    return [id for id, in session.query(Transaction.id)
        .filter(Transaction.blocknumber == None, Transaction.trx_hash != None).all()]


def update(p: Pool):
    txs = get_transactions_ids()
    package_size = ceil(len(txs) / settings.WATCHER_PROCESS_COUNT)
    logger.info("Package size %d" % package_size)
    if package_size == 0:
        return
    p.map(update_transactions_statuses_task,
          [txs[i * package_size:i * package_size + package_size] for i in range(settings.WATCHER_PROCESS_COUNT)])


def start_worker(state: State, process_blocker: Condition):
    logger.info("Starting watcher with %d workers" % settings.WATCHER_PROCESS_COUNT)
    process_blocker.acquire()
    with Pool(settings.WATCHER_PROCESS_COUNT) as pool:
        try:
            while state.active:
                logger.info("Start new process cycle")
                update(pool)
                logger.info("Process cycle ended")
                if state.active:
                    process_blocker.wait(settings.WATCHER_SLEEP_TIME)
        except:
            logger.exception("Failed during iteration of watcher")
        finally:
            logger.info("Ending watching")
            process_blocker.release()
            logger.info("Ended watching")


def startup():
    blocker = Condition(Lock())
    state = State(active=True)
    mainpid = os.getpid()

    def signal_handler(sig, frame):
        if mainpid != os.getpid():
            return

        state.active = False
        try:
            blocker.acquire()
            blocker.notify()
        finally:
            blocker.release()
        logger.info("Switched off")

    signal.signal(signal.SIGINT, signal_handler)
    start_worker(state, blocker)
