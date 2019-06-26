import sys
import signal

from threading import Lock, Condition
from multiprocessing.dummy import Pool
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
        txs = session.query(Transaction).filter(Transaction.id.in_(ids))
        for tx in txs:
            update_transaction_status(w3, tx)


@session_scope_func
def get_transactions_ids(session: Session) -> list:
    return [id for id, in session.query(Transaction.id).filter(Transaction.blocknumber == None).all()]


def update(p: Pool):
    txs = get_transactions_ids()
    package_size = ceil(len(txs) / settings.WATCHER_PROCESS_COUNT)
    if package_size == 0:
        return
    logger.debug("Package size %d" % package_size)
    p.map(update_transactions_statuses_task,
          [txs[i * package_size:i * package_size + package_size] for i in range(settings.WATCHER_PROCESS_COUNT)])


def start_worker(state: State, process_blocker: Condition):
    logger.debug("Starting watcher with %d workers" % settings.WATCHER_PROCESS_COUNT)
    with Pool(settings.WATCHER_PROCESS_COUNT) as p:
        process_blocker.acquire()
        try:
            while state.active:
                update(p)
                if state.active:
                    process_blocker.wait(settings.WATCHER_SLEEP_TIME)
        finally:
            logger.debug("End watching")
            process_blocker.release()


def startup():
    blocker = Condition(Lock())
    state = State(active=True)

    def signal_handler(sig, frame):
        state.active = False
        try:
            blocker.acquire()
            blocker.notify()
        finally:
            blocker.release()
        logger.debug("Ended")
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    start_worker(state, blocker)
