from models.accounts import SavingsAccount, CheckingAccount
from models.user import User

class Bank:
    def __init__(self, name, branch_number, location, repo):
        self.name = name
        self.branch = branch_number
        self.location = location
        self.repo = repo
        self.next_account_number = 10000

    #________________________________________USER__________________________________________
    #checks if a username is taken
    def is_username_taken(self, username):
        return self.repo.username_exists(username)

    #checks if an email is taken
    def is_email_taken(self, email):
        return self.repo.email_exists(email)

    #User sign up, creates users if username and email are available
    def sign_up(self, username, email, password):
        if self.is_username_taken(username):
            raise ValueError("Username already in use")
        if self.is_email_taken(email):
            raise ValueError("Email already in use")

        self.repo.create_user(username, email, password)
        user = User(username, email, password)
        return user
    
    #User Sign in, returns a user on successful sign in
    def sign_in(self, username, password):
        user_doc = self.repo.get_user(username)
        if user_doc is None or user_doc["password"] != password:
            raise ValueError("Invalid username or password")
        return user_doc

    #_________________________________________ACCOUNTS_________________________________________
    #Creates an account for the user
    def create_account(self, username, account_type, balance=0):
        user = self.repo.get_user(username)
        if user is None:
            raise ValueError("User not found - sign up first")

        account_type = account_type.lower()

        if account_type not in ("savings", "checking"):
            raise ValueError(f"Invalid account type: {account_type}")

        # Enforces exactly 4 states per user: none / savings / checking / both
        if self.repo.account_type_exists(username, account_type):
            raise ValueError(f"User already has a {account_type} account")

        account_number = self.next_account_number

        if account_type == "savings":
            account = SavingsAccount(username, account_number, balance)
        else:  # checking
            account = CheckingAccount(username, account_number, balance)

        # Save to MongoDB
        self.repo.create_account(account_number, username, account_type, balance)
        self.repo.add_account_to_user(username, account_number)
        self.next_account_number += 1
        return account_number


    def has_account_type(self, username, account_type):
        """True if this user already has an account of this type."""
        return self.repo.account_type_exists(username, account_type)


    def find_account(self, account_number):
        account_doc = self.repo.get_account(account_number)
        if account_doc is None:
            return None
        return account_doc
    

    def list_accounts(self):
        accounts = self.repo.get_all_accounts()
        if not accounts:
            print("No accounts yet.")
            return
        for account_doc in accounts:
            print(f"  Account {account_doc['account_number']}: {account_doc['username']} ({account_doc['account_type']}) - Balance: ${account_doc['balance']:.2f}")
   

    def __str__(self):
        return f"{self.name} (ID: {self.bank_id}) - {self.location}"