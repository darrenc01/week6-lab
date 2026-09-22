import unittest
from bankaccount import BankAccount

class TestBankAccount(unittest.TestCase):
    def setUp(self):
        self.account =BankAccount(100, "Alice")

    def test_deposit(self):
        self.account.deposit(50)
        self.assertEqual(self.account.balance, 150)

    def test_withdraw(self):
        self.account.withdraw(40)
        self.assertEqual(self.account.balance, 60)

    def test_negative_amount_rejected(self):
        with self.assertRaises(ValueError):
            self.account.deposit(-10)

    def test_overdraw_rejected(self):
        with self.assertRaises(ValueError):
            self.account.withdraw(101)

if __name__ == "__main__":
    unittest.main()