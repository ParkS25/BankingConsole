#Version1: Programming funcdamentals (Bank Console App)
class BankAccount:
    def __init__(self, owner, balance = 0):
        self.owner = owner
        self.balance = balance
        self.transactions = []
    

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit must be positive")
        self.balance += amount

    def withdrawal(self, amount):
        