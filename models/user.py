from datetime import datetime
class User:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
        self.account_numbers = []
        self.created_at = datetime.now()

    def add_accounts(self, account_number):
        self.accounts

    def __str__(self):
        return f"User({self.username}, {self.email}, accounts={self.account_numbers})"
"""user functionality:
create users
add accounts
"""