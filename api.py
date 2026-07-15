from flask import Flask, jsonify
from models.bank import Bank
from repository import MongoDBRepository
import os
from dotenv import load_dotenv
from datetime import datetime
load_dotenv()

app = Flask(__name__)

# Initialize MongoDB repository
mongo_uri = os.getenv("MONGO_URI")
if not mongo_uri:
    raise ValueError("MONGO_URI environment variable not set")

repo = MongoDBRepository(mongo_uri)
repo.connect()

# Initialize bank with repository
my_bank = Bank("CitiBank", "1", "Tampa", repo)

# Create sample users and accounts if they don't exist
try:
    if not repo.username_exists("Seung"):
        my_bank.sign_up("Seung", "seung@example.com", "password123")
        my_bank.create_account("Seung", "savings", 500)
    
    if not repo.username_exists("Philip"):
        my_bank.sign_up("Philip", "philip@example.com", "password456")
        my_bank.create_account("Philip", "checking", 800)
except ValueError:
    # Users/accounts may already exist
    pass


@app.get("/")
def home():
    return jsonify({
        "message": "Bank API is running",
        "endpoints": {
            "GET /accounts": "Get all accounts",
            "POST /accounts": "Create an account",
            "GET /accounts/<account_number>": "Get specific account",
        }
    })


@app.get("/accounts")
def get_accounts():
    """Returns a JSON list of all accounts in the bank."""
    accounts_data = repo.get_all_accounts()
    return jsonify(accounts_data)


@app.get("/accounts/<int:account_number>")
def get_account(account_number):
    """Get a specific account by number"""
    account = repo.get_account(account_number)
    if account is None:
        return jsonify({"error": "Account not found"}), 404
    return jsonify(account)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)


