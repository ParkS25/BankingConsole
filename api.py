from flask import Flask, jsonify, render_template_string
from models.bank import Bank
from repository import MySQLRepository
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


repo = MySQLRepository(
    host = 'localhost',
    user = 'root',
    password = os.getenv("MySQLPW"),
    database = 'banking_application',
)

repo.connect()


my_bank = Bank("CitiBank", "1", "Tampa")
my_bank.create_account("Seung", "savings")
my_bank.create_account("Philip", "checking")



@app.get("/")
def get_accounts():
    """Returns a JSON list of all accounts in the bank."""
    accounts_data = []
    for account in my_bank.accounts.values():
        accounts_data.append({
            "account_number": account.account_number,
            "owner": account.owner,
            "account_type": account.account_type(),
            "balance": account.get_balance()
        })
    return jsonify(accounts_data)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)


