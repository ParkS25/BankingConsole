from bank import Bank

def main():
    #currently bank will be hard coded
    my_bank = Bank("CitiBank","1", "Tampa")
    while True:
        #select account will contain viewing account details, deposit money, withdrawal, and view transaction history
        choice = input("1) Create Account   2) Select Account  3) Exit\n")
        if choice == "1":
            owner = input("Owner's Name: ").strip()
            account_type = input("Account type (Savings/Checking): ").strip().lower()
            my_bank.create_account(owner, account_type)
        elif choice == "2":
            account_number = input("What is your Account number:")
            account = my_bank.find_account
            choice = input("\n1) Get Account Details  2) Make a Deposit   3) Make a Withdrawal   4) Show Transaction History 5) Exit\n")
            if choice == "1":
                acc_num = int(input("Account number: "))
                account = find_account(acc_num)
                if account:
                    try:
                        amount = float(input("Deposit amount: $"))
                        account.deposit(amount)
                        print(f"\n New balance: ${account.get_balance():.2f}")
                    except ValueError as e:
                        print(f"\n {e}")
            elif choice == "2":
                amount = float(input("Deposit amount:"))
            elif choice == "5":
                break
        elif choice == "3":
            break


if __name__ == "__main__":
    main()
