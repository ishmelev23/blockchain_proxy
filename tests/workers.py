from multiprocessing.pool import Pool

import settings
from src.database.models.transaction import Transaction
from src.database.session import session_scope_method, session_context
from src.workers import watcher
from tests.base import BaseTestCase


class WorkersTests(BaseTestCase):
    WATCHING_TRXS = [
        "0xc15dfd76acb77b19e11589ed5e9a0362de7a29572ed13ce77ac3bc97311613de",
        "0x10e1d4972e2e34ff2b7770e4c21989a0310b74c1a5bb7cac739f612155947203",
        "0x4abfb29353f8c3ebb1472d594d4aca23142813a1165f40dd9504d271c6325f48",
        "0x09d2233eced4ad3eecf64750aa76288d323b68652ae275b62d9d6f2edaf335f6",
        "0x4501c53862b1be9fce25e424339c1c1837cbe909fef57b9d6f82f8f38baa3e1b",
        "0x55a09e11fc2fac314720007a105f6c73cea979c9c2a4611987be09efb193c080",
        "0xfda4b1ce22fdb11beb45405c2be3e290c86ec1818dbdc6a643d77cde45e9404e",
        "0xc889576f0eea6533202aaa15814a255eac205c0ad0a8a9077b77946a42e0a1e8",
        "0x925066284c6d2fe0a4151a558a3aaa25200822456a5777c1389c5f364a98275e",
        "0x0b1b51a059c7699d1f0bbebdde843451aa7d7d8ebfe863fb224110091699e5a6",
        "0x9c220eed83b0be3c027d984c2c5140c884a743def3922bae85e9967c4cc0fcde",
        "0x52dc705f2f10ad378d2c9eb0f02dfae3e8145317b525b6d5e04209cff81102ab"
    ]

    def _watcher_test(self, count: int):
        with session_context() as session:
            session.query(Transaction).delete()

            for tx_hash in self.WATCHING_TRXS[:count]:
                tx = Transaction(trx_hash=tx_hash, contract_name="bokky_token", func_name="transfer")
                session.add(tx)

        with Pool(settings.WATCHER_PROCESS_COUNT) as p:
            watcher.update(p)

        with session_context() as session:
            self.assertGreater(session.query(Transaction).filter(Transaction.blockhash != None).count(), 0)
            self.assertEqual(0, session.query(Transaction).filter(Transaction.blockhash == None).count())

    def test_watcher_12(self):
        self._watcher_test(len(self.WATCHING_TRXS))

    def test_watcher_11(self):
        self._watcher_test(11)

    def test_watcher_4(self):
        self._watcher_test(4)

    def test_watcher_3(self):
        self._watcher_test(3)

    def test_watcher_1(self):
        self._watcher_test(3)
