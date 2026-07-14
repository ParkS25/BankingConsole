from accounts import SavingsAccount, CheckingAccount
class Bank:
    def __init__(self, name, branch_number, location):
        self.name = name
        self.branch = branch_number
        self.location = location
        self.accounts = {}     #assume that accounts are stored in the branch they're created at       
        self.next_account_number = 10000     #currently account numbers are handled like this, but can be handled based on branch location and a 

    def create_account(self, owner, account_type, balance=0):
        if account_type == "savings":
            account = SavingsAccount(owner, balance)
        elif account_type == "checking":
            account = CheckingAccount(owner, balance)
        else:
            raise ValueError("Invalid account type")

        account_number = self.next_account_number
        self.accounts[account_number] = account
        self.next_account_number += 1
        print(f"Account created. Account number: {account_number}")
        return None

    def find_account(self, account_number):
        account = self.accounts.get(account_number)
        if account is None:
            print("Account not found.")
        return account