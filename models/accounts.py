from abc import ABC, abstractmethod
import datetime

class BankAccount(ABC):
    

    def __init__(self, owner, account_number, balance = 0):
        self.owner = owner
        self.account_number = account_number
        self._balance = balance     #encapsulation, can only be changed by methods
        self._transaction_history = []
    

    #deposit method
    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposits must be positive")
        self._balance += amount
        self._transaction_history.append(f"+ ${amount:.2f}")


    #withdraw method
    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdraws must be positive")
        if amount > self._balance:
            raise ValueError("Insufficient Funds")
        self._balance -= amount
        self._transaction_history.append(f"- ${amount:.2f}")


    def get_balance(self):
        return self._balance
    

    def get_transaction_history(self):
        return(self._transaction_history)


    @abstractmethod
    def account_type(self):
        pass

    def __str__(self):
        return (f"Account #{self.account_number} [{self.account_type()}] "
                f"{self.owner} - Balance: ${self._balance:.2f}")

#inheritance Savings account is a subtype of bank account, inherits methods from the bank account class
class SavingsAccount(BankAccount):

    
    def __init__(self, owner, balance = 0, interest_rate = 0.02):
        super().__init__(owner, balance)
        self._interest_rate = interest_rate
    

    def accrue_interest(self):
        interest = self._interest_rate*self._balance
        self._balance += interest


    #Polymorphism: overriding
    def account_type(self):
        return "Savings"

#Checking is also a subclass of bank account
class CheckingAccount(BankAccount):


    def __init__(self, owner, balance = 0, overdraft_limit = 100):
        super().__init__(owner,balance)
        self._overdraft_limit = overdraft_limit
    

    #overrides the withdraw method of the bank accounts parent class, allows for checking accounts to withdraw up to their overdraft limit
    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdraws must be positive")
        if amount > self._balance + self._overdraft_limit:
            raise ValueError("Exceeds overdraft limit")
        self._balance -= amount
        if self._balance < 0:
            print("Account is overdrawn. Make a deposit to avoid overdraft fees.")
        self._transaction_history.append(f"- ${amount:2f}")


    #Polymorphism: overriding
    def account_type(self):
        return "Checking"

