from bank import Bank

def main():
    #currently bank will be hard coded
    my_bank = Bank("CitiBank","1", "Tampa")


    while True:
        #select account will contain viewing account details, deposit money, withdraw, and view transaction history
        choice = input("1) Create Account   2) Select Account  3) Exit\n")

        #allows user to create an account of either savings or checkings using their name
        if choice == "1":
            owner = input("Owner's Name: ").strip()
            while True:
                account_type = input("Account type (Savings/Checking): ").strip().lower()
                if account_type in ("savings", "checking"):
                    break
                print("Invalid account type. Please enter 'Savings' or 'Checking'.")
            my_bank.create_account(owner, account_type)

        #allows users to find their account
        elif choice == "2":

            account_number = int(input("What is your Account number:"))
            account = my_bank.find_account(account_number)
            if account is None:
                continue
            while True:   # <- sub-menu loop, stays here until user picks "5"
               
                sub_choice = input("\n1) Get Account Details  2) Make a Deposit   3) Make a Withdraw   4) Show Transaction History    5) Exit\n")
               
                #prints users account details
                if sub_choice == "1":
                    print(account)

                #allows users to make a deposit
                elif sub_choice == "2":
                    try:
                        amount = float(input("Deposit amount: $"))
                        account.deposit(amount)
                        print("\nDeposit Successful")
                        print(f"\nNew balance: ${account.get_balance():.2f}")
                    except ValueError as e:
                            print(f"\n{e}")

                #allows users to make a withdrawal
                elif sub_choice == "3":
                    try:
                        amount = float(input("Withdraw amount: $"))
                        account.withdraw(amount)
                        print("\nWithdraw Successful")
                        print(f"\nNew balance: ${account.get_balance():.2f}")
                    except ValueError as e:
                        print(f"\n{e}")

                #prints users transaction history
                elif sub_choice == "4":
                    print(f"\nTransaction history for {account.owner}:")
                    for entry in account.get_transaction_history():
                        print(f"  {entry}")
                    print(f"Balance:    {account.get_balance()}")

                #exits the loop
                elif sub_choice == "5":
                    break
        elif choice == "3":
            break
        exit


if __name__ == "__main__":
    main()
