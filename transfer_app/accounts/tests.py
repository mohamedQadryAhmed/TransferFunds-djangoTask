from django.test import TestCase
from .models import Account

class AccountModelTests(TestCase):

    def setUp(self):
        self.account1 = Account.objects.create(name="Account1", balance=100)
        self.account2 = Account.objects.create(name="Account2", balance=50)

    def test_transfer_success(self):
        self.account1.transfer(50, self.account2)
        self.assertEqual(self.account1.balance, 50)
        self.assertEqual(self.account2.balance, 100)

    def test_transfer_insufficient_funds(self):
        with self.assertRaises(ValueError):
            self.account1.transfer(150, self.account2)

class AccountViewTests(TestCase):

    def test_list_accounts(self):
        response = self.client.get('/accounts/')
        self.assertEqual(response.status_code, 200)

    def test_import_accounts(self):
        with open('accounts.csv', 'rb') as f:
            response = self.client.post('/accounts/import/', {'file': f})
        self.assertEqual(response.status_code, 200)
