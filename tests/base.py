from unittest import TestCase

import settings
from app import app


class ApiTestCase(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        assert settings.TESTING, "Trying to start tests in non testing mode. You should setup TESTING env variable"

    def setUp(self) -> None:
        app.config['TESTING'] = True
        client = app.test_client()

        self.client = client

    def tearDown(self) -> None:
        self.client = None
