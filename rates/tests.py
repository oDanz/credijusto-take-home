import unittest

from django.test import Client

from . import services


class TestRetrieveMethods(unittest.TestCase):
    def test_dof(self):
        response = services.retrieve_dof()
        self.assertIsInstance(response, dict)

    def test_banxico(self):
        response = services.retrieve_banxico()
        self.assertIsInstance(response, dict)

    def test_fixer(self):
        pass
        # response = services.retrieve_fixer()
        # self.assertIsInstance(response, dict)


class TestTokenRequest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_token_retrieve(self):
        response = self.client.post('/api/token/', {'username': 'test', 'password': '123456'})
        self.assertIn('token', response.json())

class TestRatesListVew(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.token = 'e18dd4c87747f68b3ddcf0561c289bcc9a68480a'

    def test_unauthenticated_user(self):
        response = self.client.get('/api/')
        self.assertEqual(response.status_code, 401)

    def test_authenticated_user(self):
        response = self.client.get('/api/', HTTP_AUTHORIZATION=f'Token {self.token}')
        self.assertEqual(response.status_code, 200)
