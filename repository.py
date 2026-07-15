from pymongo import MongoClient
from pymongo.errors import PyMongoError


class MongoDBRepository:
    def __init__(self, connection_string):
        """
        Initialize MongoDB repository
        
        Args:
            connection_string: MongoDB Atlas connection string
            Example: mongodb+srv://username:password@cluster.mongodb.net/database
        """
        self.connection_string = connection_string
        self.client = None
        self.db = None
        self.users_collection = None
        self.accounts_collection = None
    
    def connect(self):
        """Connect to MongoDB Atlas"""
        try:
            self.client = MongoClient(self.connection_string)
            # Verify connection
            self.client.admin.command('ping')
            
            # Get database
            self.db = self.client.banking_app
            
            # Get collections
            self.users_collection = self.db.users
            self.accounts_collection = self.db.accounts
            
            print("Connected to MongoDB Atlas successfully")
        except PyMongoError as e:
            print(f"Error connecting to MongoDB: {e}")
            raise
    
    def disconnect(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
    
    # ==================== USER OPERATIONS ====================
    
    def username_exists(self, username):
        """Check if username already exists"""
        return self.users_collection.find_one({"username": username}) is not None
    
    def email_exists(self, email):
        """Check if email already exists"""
        return self.users_collection.find_one({"email": email}) is not None
    
    def create_user(self, username, email, password):
        """Create a new user"""
        try:
            user_doc = {
                "username": username,
                "email": email,
                "password": password,
                "account_numbers": []
            }
            result = self.users_collection.insert_one(user_doc)
            return result.inserted_id
        except PyMongoError as e:
            print(f"Error creating user: {e}")
            raise
    
    def get_user(self, username):
        """Get user by username"""
        return self.users_collection.find_one({"username": username})
    
    def add_account_to_user(self, username, account_number):
        """Add account number to user's account list"""
        try:
            self.users_collection.update_one(
                {"username": username},
                {"$push": {"account_numbers": account_number}}
            )
        except PyMongoError as e:
            print(f"Error adding account to user: {e}")
            raise
    
    # ==================== ACCOUNT OPERATIONS ====================
    
    def create_account(self, account_number, username, account_type, balance):
        """Create a new account"""
        try:
            account_doc = {
                "account_number": account_number,
                "username": username,
                "account_type": account_type,
                "balance": balance,
                "transaction_history": []
            }
            result = self.accounts_collection.insert_one(account_doc)
            return result.inserted_id
        except PyMongoError as e:
            print(f"Error creating account: {e}")
            raise
    
    def get_account(self, account_number):
        """Get account by account number"""
        return self.accounts_collection.find_one({"account_number": account_number})
    
    def get_accounts_by_user(self, username):
        """Get all accounts for a user"""
        return list(self.accounts_collection.find({"username": username}))
    
    def account_type_exists(self, username, account_type):
        """Check if user already has this account type"""
        return self.accounts_collection.find_one({
            "username": username,
            "account_type": account_type.lower()
        }) is not None
    
    def update_balance(self, account_number, new_balance):
        """Update account balance"""
        try:
            self.accounts_collection.update_one(
                {"account_number": account_number},
                {"$set": {"balance": new_balance}}
            )
        except PyMongoError as e:
            print(f"Error updating balance: {e}")
            raise
    
    def add_transaction(self, account_number, transaction_record):
        """Add transaction to account history"""
        try:
            self.accounts_collection.update_one(
                {"account_number": account_number},
                {"$push": {"transaction_history": transaction_record}}
            )
        except PyMongoError as e:
            print(f"Error adding transaction: {e}")
            raise
    
    def get_all_accounts(self):
        """Get all accounts in the bank"""
        return list(self.accounts_collection.find())
