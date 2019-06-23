import os
from unittest import TestCase

from app import app


class ApiTestCase(TestCase):

    def setUp(self) -> None:
        app.config['TESTING'] = True
        client = app.test_client()

        self.client = client

    def tearDown(self) -> None:
        self.client = None
