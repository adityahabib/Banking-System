import json
class BankAccount:

    # -------------------------------
    # Class variables
    # -------------------------------

    transaction_code = 1000
    account_counter = 1000

    # -------------------------------
    # Constructor
    # -------------------------------

    def __init__(self, name, balance, pin):

        if balance < 0:
            raise ValueError(
                "Balance cannot be negative"
            )

        BankAccount.account_counter += 1

        self.name = name
        self.__balance = balance
        self.__pin = pin
        self.__transaction = []

        self.account_number = (
            f"gpt{BankAccount.account_counter}"
        )

    # -------------------------------
    # Internal helper methods
    # -------------------------------

    def _get_balance(self):
        return self.__balance

    def _update_balance(self, amount):
        self.__balance += amount

    def _add_transaction(self, text):
        self.__transaction.append(text)

    # -------------------------------
    # Data base 
    # -------------------------------

    def to_dict(self):
        return {
            "name" : self.name,
            "balance" : self._get_balance(),
            "pin" : self._BankAccount__pin,
            "account_number" : self.account_number,
            "account_type" : self.__class__.__name__ ,
            "transaction" : self._BankAccount__transaction
        }
    
    # -------------------------------
    # Verify PIN
    # -------------------------------

    def verify_pin(self, pin):
        return pin == self.__pin

    # -------------------------------
    # Generate transaction code
    # -------------------------------

    def generate_code(self, prefix):

        BankAccount.transaction_code += 1

        return (
            f"{prefix}"
            f"{BankAccount.transaction_code}"
        )

    # -------------------------------
    # Deposit
    # -------------------------------

    def deposit(self, amount):

        if amount <= 0:
            print("Invalid amount")
            return

        self.__balance += amount

        code = self.generate_code("CRA")

        self.__transaction.append(
            f"{code} - Deposited amount: ₹{amount}"
        )

        print(f"\nDeposited: ₹{amount}")

    # -------------------------------
    # Withdraw
    # -------------------------------

    def withdraw(self, amount):

        if amount <= 0:
            print("Invalid amount")
            return

        if amount > self.__balance:
            print("Insufficient balance")
            return

        self.__balance -= amount

        code = self.generate_code("DRA")

        self.__transaction.append(
            f"{code} - Withdrawn amount: ₹{amount}"
        )

        print(f"\nWithdrawn: ₹{amount}")

    # -------------------------------
    # Transfer
    # -------------------------------

    def transfer(
        self,
        amount,
        other_user,
        pin=None
    ):

        if not isinstance(
            other_user,
            BankAccount
        ):
            print("Invalid receiver account")
            return

        if pin is None:
            print("PIN not entered")
            return

        if pin != self.__pin:
            print(
                "Transaction failed: wrong PIN"
            )
            return

        if amount <= 0:
            print("Invalid amount")
            return

        if amount > self.__balance:
            print("Insufficient balance")
            return
        
        # sender side
        self.__balance -= amount

        code = self.generate_code("TDRA")

        self.__transaction.append(
            f"{code} - ₹{amount} "
            f"transferred to "
            f"{other_user.name}"
        )

        # receiver side
        other_user._update_balance(amount)

        code = self.generate_code("TCRA")

        other_user._add_transaction(
            f"{code} - ₹{amount} "
            f"received from {self.name}"
        )

        print(
            f"\n₹{amount} transferred "
            f"to {other_user.name}"
        )

    # -------------------------------
    # Show balance
    # -------------------------------

    def get_balance(self):

        attempt = 4

        while True:

            pin = int(
                input("Enter your PIN: ")
            )

            if pin == self.__pin:

                print(
                    f"\nTotal balance:"
                    f" ₹{self.__balance}"
                )

                break

            else:

                attempt -= 1

                print("\nIncorrect PIN")

                if attempt <= 0:

                    print(
                        "Too many attempts"
                    )

                    break

                print(
                    f"{attempt} attempts left"
                )

    # -------------------------------
    # Transaction history
    # -------------------------------

    def get_transaction(self):

        if len(self.__transaction) <= 0:
            print("No transaction")
            return

        print("\n--------------------------------")

        print("Transaction History:\n")

        print(
            f"Account.no : "
            f"{self.account_number}"
        )

        print(
            f"Account Name: {self.name}"
        )

        for transaction in self.__transaction:
            print(transaction)

        print("--------------------------------")


# =========================================
# Savings Account
# =========================================

class SavingsAccount(BankAccount):

    # -------------------------------
    # Interest rate
    # -------------------------------

    def interest_rate(self):

        balance = self._get_balance()

        if balance >= 250000:
            return 0.15

        elif balance >= 100000:
            return 0.10

        else:
            return 0.05

    # -------------------------------
    # Add interest
    # -------------------------------

    def add_interest(self):

        interest_rate = (
            self.interest_rate()
        )

        interest = round(
            self._get_balance()
            * interest_rate
        )

        self._update_balance(interest)

        code = self.generate_code("ICRA")

        self._add_transaction(
            f"{code} - Interest added:"
            f" ₹{interest}"
        )

        print(
            f"Interest added: ₹{interest}"
        )

    # -------------------------------
    # Withdrawal limit override
    # -------------------------------

    def withdraw(self, amount):

        limit = 20000

        if amount > limit:

            print(
                "Amount exceeds "
                "withdrawal limit"
            )

            return

        super().withdraw(amount)


# =========================================
# Current Account
# =========================================

class CurrentAccount(BankAccount):

    overdraft_limit = 50000
    minimum_balance = 200000 

    # -------------------------------
    # Constructor
    # -------------------------------

    def __init__(
        self,
        name,
        balance,
        pin
    ):

        if (balance < CurrentAccount.minimum_balance):

            raise ValueError(
                "Minimum balance required "
                f"₹{CurrentAccount.minimum_balance}"
            )

        super().__init__(
            name,
            balance,
            pin
        )

    # -------------------------------
    # Overdraft withdraw
    # -------------------------------

    def withdraw(self, amount):

        if amount <= 0:

            print("Invalid amount")

            return

        available_amount = (
            self._get_balance()
            + CurrentAccount.overdraft_limit
        )

        if amount > available_amount:

            print(
                "Overdraft limit exceeded"
            )

            return

        self._update_balance(-amount)

        code = self.generate_code("ODRA")

        self._add_transaction(
            f"{code} - Overdraft "
            f"withdrawal: ₹{amount}"
        )

        print(
            f"\nWithdrawn with overdraft:"
            f" ₹{amount}"
        )

        
# ======================================
# USER_DASHBOARD
# ======================================

def user_dashboard(user, accounts):

    while True:
        
        print("\n===== USER DASHBOARD =====")

        print("1. Deposit")
        print("2. Withdraw")
        print("3. Transfer")
        print("4. Check Balance")
        print("5. Change PIN")
        print("6. Transaction History")
        print("7. Add Interest")
        print("8. Logout")

        choice = input("Enter choice: ")
        
        if choice == "1":
            try:
               amount = int(input("Enter Deposit Account:"))
               user.deposit(amount)

               save_account(accounts)

            except ValueError:
                print("\nInvalid input")
                
        elif choice == "2":
            try:
                amount = int(input("Enter Withdrawal Amount:"))
                user.withdraw(amount)

                save_account(accounts)

            except ValueError:
                print("\nWrong input")
                
        elif choice == "3":
            try:
                other_Acc = input("enter the receiver Account:")

                if other_Acc not in accounts :
                    print("Not find receiver account")
                
                elif user == accounts[other_Acc]:
                    print("Not able to send same account!")

                    continue
                
                receiver_acc = accounts[other_Acc]
                
                amount = int(input("Enter amount to send:"))
                
                pin = int(input("enter your PIN:"))
                
                user.transfer(
                    amount,
                    receiver_acc,
                    pin
                )
                
                save_account(accounts)

            except ValueError:

                print("\nInvalid input")
                
        elif choice == "4":
            try:
                user.get_balance()
                
            except ValueError:
                print("Invalid input")

        elif choice == "5":
            try:
                attempts = 2
                pin = int(input("enter your old PIN :"))

                if not user.verify_pin(pin):

                    print(f"\nwrong PIN 3 attempts left\n")

                    for i in range(attempts, -1, -1):

                        pin = int(input("enter your old PIN :"))
                        
                        if not user.verify_pin(pin):

                            print(f"\nwrong PIN {i} attempts left\n")

                        else:

                            user._BankAccount__pin = int(input("enter new PIN :"))
                            save_account(accounts)
                            print("\npin changed\n")
                            break

                    if attempts <= 0:
                        print("Too many attempts")
                else:
                    user._BankAccount__pin = int(input("enter new PIN :"))
                    save_account(accounts)
                    print("\npin changed\n")


            except ValueError:

                print("wrong input")
                
        elif choice == "6":
            try:
                user.get_transaction()
                
            except ValueError:
                print("\nInvalid input")
                
        elif choice == "7":
            try:
                if isinstance(user, SavingsAccount):
                    user.add_interest()
                else:
                    print("\nInterest is available only for Saveing Account.")

                save_account(accounts)
                
            except ValueError:
                print("\nInvalid input")
                
        elif choice == "8":
            print("\nLOG-OUT Successful\n")
            break

# =========================================
# database
# =========================================

def save_account(accounts):
    print("saveing account")
    data = {}
        
    for acc_no, user in accounts.items():

      data[acc_no] = user.to_dict()


    with open("account.json", "w", encoding = "utf-8") as file :
        json.dump(data, file, indent=4, ensure_ascii = False)
    
    print("File saved successfully")

# =========================================
# load accounts
# =========================================
def load_accounts():
    accounts = {}
    try:
        with open("account.json", "r", encoding = "utf-8") as file:

            data = json.load(file)
            
            for acc_no, info in data.items():

                if info["account_type"] == "SavingsAccount":

                    user = SavingsAccount(info["name"],
                                          info["balance"],
                                          info["pin"])
                else:
                    user = CurrentAccount(info["name"],
                                          info["balance"],
                                          info["pin"])
                    
                user.account_number = acc_no

                user._BankAccount__transaction = info.get("transaction", [])
                
                accounts[acc_no] = user

    except (FileNotFoundError, json.JSONDecodeError):
        
        return {}
    
    return accounts

# =================================
# ADMIN PANEL
# =================================

def Adminpanel(data, pin, accounts):
    try:

        if pin == int(input("enter the admin pin :")):
                        while True:
                            print("\n1. View All Accounts")
                            print("2. Search Account")
                            print("3. Total Money in Bank")
                            print("4. Total Accounts")
                            print("5. Delete Account")
                            print("6. Logout\n")

                            option = input("Enter your choice :")

                            if option == "1":
                                for acc_no, info in data.items():
                                    print("\n-------------------------")
                                    print("NAME : ",info["name"])
                                    print("ACCOUNT_NUMBER :",info["account_number"])
                                    print("BALANCE : ",info["balance"])
                                    print("ACCOUNT_TYPE : ",info["account_type"])
                                    print("-------------------------\n")

                            elif option == "2":
                                search = input("enter the account number :")
                                
                                if search in data:
                                    print("\n-------------------------")
                                    print("Name : ",data[search]["name"])
                                    print("Balance : ",data[search]["balance"])
                                    print("Account Number : ",data[search]["account_number"])
                                    print("Account Type : ",data[search]["account_type"])
                                    print("Transactions : ",len(data[search]["transaction"]))
                                    print("-------------------------\n")

                                else:
                                    print("\nAccount not exist\n")

                            elif option == "3":
                                money = 0

                                for acc_no, info in data.items():
                                    money += info["balance"]

                                print("\ntotal money in bank", money)

                            elif option == "4":

                                print("\nTotal Account in bank : ",len(data))

                            elif option == "5":

                                acc_no = input("enter your Account number:")

                                if acc_no not in data:

                                    print("Account not exist")

                                    continue

                                user = accounts[acc_no]

                                if not user.verify_pin(int(input("enter your pin:"))):
                                    print("Wrong PIN")
                                    continue

                                print(f"\nAccount Number : {acc_no}")
                                print(f"name : {user.name}")
                                print(f"Balance : {user._get_balance()}\n")


                                choice = input("Are you sure ( yes or no ):")

                                if choice.lower() == "yes":
                                    
                                    accounts.pop(acc_no)

                                    save_account(accounts)

                                    print("account Delete.")
                                    print(f"retured Balance : {user._get_balance()}")

                                else:
                                    print("Account not delete")


                            elif option == "6":

                                print("\nAdmin Logout")
                                break
    except ValueError:
        print("Wrong input")

# =========================================
# MAIN FUNCTION
# =========================================

def main():

    print("Banking system start:\n")

    # mini database
    accounts = load_accounts()

    while True:

        print("===== BANK MENU =====")

        print("1. Create ACCOUNT")
        print("2. Login")
        print("3. Delete ACCOUNT")
        print("4. Admin Login")
        print("5. Exit")

        choice = input(
            "Enter choice: "
        )

        # =================================
        # CREATE ACCOUNT
        # =================================

        if choice == "1":

            try:

                name = input(
                    "Enter your name: "
                ).capitalize()

                balance = int(
                    input(
                        "Enter opening balance: "
                    )
                )

                pin = int(
                    input("Create PIN: ")
                )

                print(
                    "\n1. Savings Account"
                )

                print(
                    "2. Current Account"
                )

                acc_type = input(
                    "Choose account type: "
                )

                if acc_type == "1":

                    user = SavingsAccount(
                        name,
                        balance,
                        pin
                    )

                elif acc_type == "2":

                    user = CurrentAccount(
                        name,
                        balance,
                        pin
                    )

                else:

                    print(
                        "Invalid account type"
                    )

                    continue

                accounts[
                    user.account_number
                ] = user

                save_account(accounts)

                print(
                    "\nAccount created "
                    "successfully"
                )

                print(
                    f"Your Account Number:"
                    f" {user.account_number}"
                )

            except ValueError as e:

                print(e)

        # =================================
        # LOGIN
        # =================================

        elif choice == "2":

            try:

                user_no = input(
                    "Enter your "
                    "Account_number: "
                )

                if user_no not in accounts:

                    print(
                        "Account not exist"
                    )

                    continue

                user = accounts[user_no]

                pin = int(
                    input(
                        "Enter your PIN:"
                    )
                )

                if user.verify_pin(pin):

                    print(
                        "\n========Login successful========"
                    )

                    print(
                        f"Welcome "
                        f"{user.name}")
                    user_dashboard(user, accounts)
                        
                    

                else:

                    print("Wrong PIN")

            except ValueError:

                print(
                    "Wrong input"
                )

        # =================================
        # DELETE ACCOUNT
        # =================================


        elif choice == "3":
            try:
                acc_no = input("enter your Account number:")

                if acc_no not in accounts:

                    print("Account not exist")

                    continue

                user = accounts[acc_no]

                if not user.verify_pin(int(input("enter your pin:"))):

                    continue

                print(f"\nAccount Number : {acc_no}")
                print(f"name : {user.name}")
                print(f"Balance : {user._get_balance()}\n")


                choice = input("Are you sure ( yes or no ):")

                if choice.lower() == "yes":
                    
                    accounts.pop(acc_no)

                    save_account(accounts)

                    print("\naccount Delete.")
                    print(f"retured Balance : {user._get_balance()}\n")

                else:
                    print("\nAccount not delete\n")

            except ValueError:

                print("wrong input")

        # =================================
        # ADMIN LOGIN
        # =================================

        elif choice == "4":

            pin = 1234

            with open("account.json", "r", encoding="utf-8") as file:

                data = json.load(file)


            Adminpanel(data, pin, accounts)

        # =================================
        # EXIT
        # =================================

        elif choice == "5":

            print(
                "Thank you for "
                "using banking system"
            )

            break

        else:

            print("Invalid choice")


main()
