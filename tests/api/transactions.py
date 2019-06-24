from settings_local import API_ENDPOINT
from src.api.errors import ERROR_CONTRACT_NOT_SUPPORTED, ERROR_FUNCTION_NOT_SUPPORTED, ERROR_FUNCTION_INVALID_FIELDS, \
    ERROR_TRANSACTION_NOT_EXISTS
from src.database.session import session_scope_method
from src.database.models.transaction import Transaction
from tests.base import ApiTestCase


class ApiTransactionsTests(ApiTestCase):
    ENDPOINT_CONTRACT_CALL = API_ENDPOINT + 'contracts/%s/%s'
    ENDPOINT_TRANSACTION_GET = API_ENDPOINT + 'transactions/%s'

    @classmethod
    @session_scope_method
    def setUpClass(cls, session) -> None:
        ApiTestCase.setUpClass()
        session.query(Transaction).delete()

    def test_invalid_contract_name(self):
        resp = self.client.post(self.ENDPOINT_CONTRACT_CALL % ('qwerty', 'qwerty'))
        self.assertEqual(400, resp.status_code)
        self.assertEqual(ERROR_CONTRACT_NOT_SUPPORTED, resp.json['error_code'])

    def test_invalid_func_name(self):
        resp = self.client.post(self.ENDPOINT_CONTRACT_CALL % ('mockcontract', 'qwerty'))
        self.assertEqual(400, resp.status_code)
        self.assertEqual(ERROR_FUNCTION_NOT_SUPPORTED, resp.json['error_code'])

    def test_invalid_arguments(self):
        resp = self.client.post(self.ENDPOINT_CONTRACT_CALL % ('mockcontract', 'mockaction'))
        self.assertEqual(400, resp.status_code)
        self.assertEqual(ERROR_FUNCTION_INVALID_FIELDS, resp.json['error_code'])

    def test_valid_func_call(self):
        resp = self.client.post(self.ENDPOINT_CONTRACT_CALL % ('mockcontract', 'mockaction'),
                                data={'name': "123", 'testbool': True})
        self.assertEqual(200, resp.status_code)
        self.assertNotIn('error_code', resp.json)

    def test_valid_transaction_request(self):
        resp = self.client.post(self.ENDPOINT_CONTRACT_CALL % ('mockcontract', 'mockaction'),
                                data={'name': "123", 'testbool': True})
        trx_hash = resp.json['trx_hash']
        resp = self.client.get(self.ENDPOINT_TRANSACTION_GET % trx_hash)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json['trx_hash'], trx_hash)

    def test_transaction_not_exists(self):
        resp = self.client.get(self.ENDPOINT_TRANSACTION_GET % '123')
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(ERROR_TRANSACTION_NOT_EXISTS, resp.json['error_code'])
