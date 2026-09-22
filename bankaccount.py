class BankAccount:
    def __init__(self, bal=0, nm=''):
        self.balance = bal
        self.name = nm

    def _validate(self, amount): # extracted during Refactor
        if amount < 0:
            raise ValueError("Amount must not be negative")
        
    def deposit(self, amount):
        self._validate(amount)
        self.balance += amount

    def withdraw(self, amount):
        self._validate(amount)
        if amount > self.balance:
            raise ValueError("Insufficient balance")
        self.balance -= amount
