from settings_local import API_ENDPOINT
from src.api.errors import ERROR_CONTRACT_NOT_SUPPORTED, ERROR_FUNCTION_NOT_SUPPORTED
from tests.base import ApiTestCase


class ApiTransactionsTests(ApiTestCase):
    ENDPOINT_CONTRACT_CALL = API_ENDPOINT + 'contracts/%s/%s'

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
        self.assertIn('Function call data contains errors', resp.json['message'])

    def test_valid_func_call(self):
        resp = self.client.post(self.ENDPOINT_CONTRACT_CALL % ('mockcontract', 'mockaction'),
                                data={'name': "123", 'testbool': True})
        self.assertEqual(200, resp.status_code)
        self.assertNotIn('error_code', resp.json)
