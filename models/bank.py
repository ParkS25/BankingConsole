from accounts import SavingsAccount, CheckingAccount
from user import User

class Bank:
    def __init__(self, name, branch_number, location):
        self.name = name
        self.branch = branch_number
        self.location = location
        self.accounts = {}     #assume that accounts are stored in the branch they're created at       
        self.next_account_number = 10000     #currently account numbers are handled like this, but can be handled based on branch location and account type
        self.users = {}

    #________________________________________USER__________________________________________
    #checks if a username is taken
    def is_username_taken(self, username):
        return username in self.users

    #checks if an email is taken
    def is_email_taken(self, email):
        return any(user.email == email for user in self.users.values())

    #User sign up, creates users if username and email are available
    def sign_up(self, username, email, password):
        if self.is_username_taken(username):
            raise ValueError("Username already in use")
        if self.is_email_taken(email):
            raise ValueError("Email already in use")

        user = User(username, email, password)
        self.users[username] = user
        print("User created")
        return user
    
    #User Sign in, returns a user on successful sign in
    def sign_in(self, username, password):
        user = self.users.get(username)
        if user is None or user.password != password:
            raise ValueError("Invalid username or password")
        return user

    #_________________________________________ACCOUNTS_________________________________________
    #Creates an account for the user
    def create_account(self, username, account_type, balance=0):
        user = self.users.get(username)
        if user is None:
            raise ValueError("User not found - sign up first")

        account_type = account_type.lower()

        if account_type not in ("savings", "checking"):
            raise ValueError(f"Invalid account type: {account_type}")

        # Enforces exactly 4 states per user: none / savings / checking / both
        if self.has_account_type(username, account_type):
            raise ValueError(f"User already has a {account_type} account")

        account_number = self.next_account_number

        if account_type == "savings":
            account = SavingsAccount(username, account_number, balance)
        else:  # checking
            account = CheckingAccount(username, account_number, balance)

        self.accounts[account_number] = account
        user.add_account(account_number)
        self.next_account_number += 1
        return account_number


    def has_account_type(self, username, account_type):
        """True if this user already has an account of this type."""
        user = self.users.get(username)
        if user is None:
            return False
        return any(
            self.accounts[num].account_type().lower() == account_type.lower()
            for num in user.account_numbers
        )


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
   
   
    def __str__(self):
        return f"{self.name} (ID: {self.bank_id}) - {self.location}"