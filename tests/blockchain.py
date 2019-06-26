import json
from multiprocessing import Value, Lock

import settings
from src.blockchain import Blockchain
from src.database.models.transaction import Transaction
from src.workers.publisher import publish_transaction
from src.workers.watcher import update_transaction_status
from tests.base import BaseTestCase


class BlockchainTests(BaseTestCase):

    def test_publish_transaction(self):
        tx = Transaction(id=1,
                         contract_name='bokky_token', func_name='transfer',
                         data=json.dumps({
                             '_to': '0x09F18D3a25747A9BA6e10c1F24db6a3c080F4a4E',
                             '_amount': 1
                         })
                         )

        w3 = Blockchain.get_web3()
        nonce = Value('i', w3.eth.getTransactionCount(settings.ADDRESS))
        lock = Lock()

        publish_transaction(Blockchain(lock, nonce), tx)
        self.assertIsNotNone(tx.trx_hash)
        print(tx.trx_hash)

    def test_request_transaction(self):
        tx_hash = '0xc889576f0eea6533202aaa15814a255eac205c0ad0a8a9077b77946a42e0a1e8'
        tx = Transaction(id=1,
                         trx_hash=tx_hash,
                         contract_name='bokky_token', func_name='transfer',
                         data=json.dumps({
                             '_to': '0x09F18D3a25747A9BA6e10c1F24db6a3c080F4a4E',
                             '_amount': 1
                         })
                         )
        update_transaction_status(Blockchain.get_web3(), tx)
        self.assertIsNotNone(tx.blocknumber)
