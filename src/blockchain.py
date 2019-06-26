import multiprocessing

from web3 import Web3, HTTPProvider
from web3.gas_strategies.time_based import fast_gas_price_strategy

import settings
from src.api.forms import NAME2FORM


class Blockchain:

    def __init__(self, lock: multiprocessing.Lock = None, nonce: multiprocessing.Value = None):
        self.lock = lock
        self.nonce = nonce
        self.w3 = Blockchain.get_web3()

    @staticmethod
    def get_web3() -> Web3:
        w3 = Web3(HTTPProvider(settings.NODE_URL))
        w3.eth.setGasPriceStrategy(fast_gas_price_strategy)
        return w3

    def __generate_tx_params(self, w3: Web3, gas_count: int) -> dict:
        with self.lock:
            params = {
                'gas': gas_count,
                'gasPrice': w3.toWei(settings.GAS_PRICE, 'gwei'),
                'nonce': self.nonce.value,
            }
            self.nonce.value += 1
        return params

    def call_function(self, contract_name: str, func_name: str, data: dict) -> str:
        assert self.lock, "You can't call methods not providing multiprocessing lock"
        assert self.nonce, "You can't call methods not providing multiprocessing nonce"

        contract_info = NAME2FORM[contract_name]
        form_class = contract_info[func_name]
        contract = self.w3.eth.contract(contract_info['address'], abi=contract_info['abi'])
        func_obj = getattr(contract.functions, form_class.func_name, None)
        assert func_obj, "Function %s is not declared in abi"
        trx = func_obj(**data).buildTransaction(self.__generate_tx_params(self.w3, form_class.gas_limit))
        signed_txn = self.w3.eth.account.signTransaction(trx, private_key=settings.PRIVATE_KEY)
        self.w3.eth.sendRawTransaction(signed_txn.rawTransaction)
        return str(signed_txn.hash.hex())
