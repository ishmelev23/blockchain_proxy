import json
import os
import signal
import sys
from functools import partial
from logging import getLogger
from multiprocessing import Value, Lock, Pool, Condition, Manager
from threading import Condition as TCondition, Lock as TLock

from math import ceil
from sqlalchemy.orm import Session
from web3 import Web3

import settings
import src.database

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


def publish_transaction(blockchain: Blockchain, transaction: Transaction):
    data = json.loads(transaction.data)
    trx_hash = blockchain.call_function(transaction.contract_name, transaction.func_name, data)
    transaction.trx_hash = trx_hash


def publish_transactions_task(lock: Lock, nonce: Value, ids: list):
    blockchain = Blockchain(lock, nonce)
    logger.debug("Processing transactions %s" % ids)
    with session_context(new_engine=True) as session:
        trxs = session.query(Transaction).filter(Transaction.id.in_(ids))

        for tx in trxs:
            try:
                publish_transaction(blockchain, tx)
            except:
                logger.exception("Can't publish transaction with id %d" % tx.id)


@session_scope_func
def get_transactions_ids(session: Session) -> list:
    return [id for id, in session.query(Transaction.id).filter(Transaction.trx_hash == None).all()]


def update(p: Pool, lock: Lock, nonce: Value):
    txs = get_transactions_ids()
    package_size = ceil(len(txs) / settings.PUBLISHER_PROCESS_COUNT)
    logger.info("Package size %d" % package_size)
    if package_size == 0:
        return

    p.map(partial(publish_transactions_task, lock, nonce),
          [(txs[i * package_size:i * package_size + package_size])
           for i in range(settings.WATCHER_PROCESS_COUNT)])


def start_worker(state: State, process_blocker: TCondition):
    logger.info("Starting publisher with %d workers" % settings.WATCHER_PROCESS_COUNT)

    w3 = Blockchain.get_web3()

    process_blocker.acquire()

    with Pool(settings.PUBLISHER_PROCESS_COUNT) as pool, Manager() as manager:
        lock = manager.Lock()
        nonce = manager.Value('i', w3.eth.getTransactionCount(settings.ADDRESS))
        try:
            while state.active:
                logger.info("Start new process cycle")
                update(pool, lock, nonce)
                logger.info("Process cycle ended")
                if state.active:
                    process_blocker.wait(settings.PUBLISHER_SLEEP_TIME)
        except:
            logger.exception("Failed during iteration of publisher")
        finally:
            logger.info("Ending publishing")
            process_blocker.release()
            logger.info("Ended publishing")


def startup():
    blocker = TCondition(TLock())
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
