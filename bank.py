from accounts import SavingsAccount, CheckingAccount
class Bank:
    def __init__(self, name, branch_number, location):
        self.name = name
        self.branch = branch_number
        self.location = location
        self.accounts = {}     #assume that accounts are stored in the branch they're created at       
        self.next_account_number = 10000     #currently account numbers are handled like this, but can be handled based on branch location and account type

    def create_account(self, owner, account_type, balance=0):
        account_number = self.next_account_number   # Bank generates the number

        if account_type == "savings":
            account = SavingsAccount(owner, account_number, balance)
        elif account_type == "checking":
            account = CheckingAccount(owner, account_number, balance)
        else:
            raise ValueError(f"Invalid account type: {account_type}")

        self.accounts[account_number] = account      
        self.next_account_number += 1
        print(f"Account created successfully. Account number: {account_number}")
        return account_number

        

    def find_account(self, account_number):
        account = self.accounts.get(account_number)
        if account is None:
            print("Account not found.")
        return account
    
    def list_accounts(self):
        if not self.accounts:
            print("No accounts yet.")
            return
        for account in self.accounts.values():
            print(f"  {account}")
   