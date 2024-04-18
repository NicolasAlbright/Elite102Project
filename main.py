import mysql.connector


db = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'elite102bank',
    database = 'bank_schema'
)  

cursor = db.cursor(buffered=True)
db.autocommit = True

#account creation
def make_account():
    first_name = input("What is your first name?: ")
    last_name = input("What is your last name?: ")
    birth_date = input("What is your birthday? YYYY-MM-DD: ")
    password = input("Create password: ")
    starting_balance = float(input("How much do you want to deposit?: "))
    cursor.execute("INSERT INTO bankdata (firstname, lastname, birthday, password, balance) VALUES (%s,%s,%s,%s,%s)", (first_name, last_name, birth_date, password, starting_balance))
    print("Account successfully made!")

#login script
def login():
    correct_password = 'N'
    while correct_password != 'Y':
        inputPassword = input("Enter your password: ")
        cursor.execute("SELECT id, firstname, lastname FROM bankdata WHERE password = %s", (inputPassword,))
        account = cursor.fetchone()
        if account:
            id_raw, firstname, lastname = account
            name_final = f'{firstname} {lastname}'
            print(f'Welcome {name_final}!')
            operation(id_raw)
            correct_password = 'Y'
        else:
            print("An account with that password does not exist. Try again: ")

#deposit money
def get_deposit(account_id):
    cursor.execute("SELECT balance FROM bankdata WHERE id = %s", (account_id,))
    balance_raw = cursor.fetchone()
    balance_final = balance_raw[0]  # Extract balance from the fetched tuple
    deposit_amount = float(input("How much would you like to deposit? "))
    new_balance = balance_final + deposit_amount
    cursor.execute("UPDATE bankdata SET balance = %s WHERE id = %s", (new_balance, account_id))
    print(f'Deposit successfully made!\nYour new balance is ${new_balance}')

#take out money
def get_withdrawal(account_id):
    cursor.execute("SELECT balance FROM bankdata WHERE id = %s", (account_id,))
    balance_raw = cursor.fetchone()
    balance_final = balance_raw[0]  # Extract balance from the fetched tuple
    withdraw_amount = float(input("How much would you like to withdraw? "))
    new_balance = balance_final - withdraw_amount
    cursor.execute("UPDATE bankdata SET balance = %s WHERE id = %s", (new_balance, account_id))
    print(f'Withdrawal successfully made!\nYour new balance is ${new_balance}')

#account operation settings
def operation(account_id):
    exit1 = 'N'
    while exit1 != 'Y':
        operation_decision = input("What would you like to do with your account? (Deposit, Withdraw, Check Balance, Settings, Exit): ")
        if operation_decision == 'Check Balance':
            cursor.execute("SELECT balance FROM bankdata WHERE id = %s", (account_id,))
            balance_raw = cursor.fetchone()
            balance_final = balance_raw[0]  # Extract balance from the fetched tuple
            print(f'Your balance is ${balance_final}')
        elif operation_decision == "Deposit":
            get_deposit(account_id)
        elif operation_decision == "Withdraw":
            get_withdrawal(account_id)
        elif operation_decision == "Settings":
            settings(account_id)
        else:
            exit_prompt = input("Would you like to exit? (Y or N)")
            if exit_prompt == 'Y':
                exit1 = 'Y'


#account settings
def settings(account_id):
    exit = 'N'
    while exit != 'Y':
        what_setting = input("Settings: Change Name, Delete Account, Check Everything, Exit: ")
        if what_setting == "Change Name":
            first_name = input('What is your first name? ')
            last_name = input("What is your last name? ")
            cursor.execute("UPDATE bankdata SET firstname = %s, lastname = %s WHERE id = %s", (first_name, last_name, account_id))
            print("Name updated!")
        elif what_setting == "Delete Account":
            cursor.execute("DELETE FROM bankdata WHERE id = %s", (account_id,))
            print("Account has been deleted!")
            exit = 'Y'
        elif what_setting == "Check Everything":
            cursor.execute("SELECT * FROM bankdata WHERE id = %s", (account_id,))
            print("\n|ID|First name|Last name |      birthday     | Password | Balance |")
            print(cursor.fetchone())
        else:
            exit_prompt = input("Would you like to exit? (Y or N)")
            if exit_prompt == 'Y':
                exit = 'Y'


#run main script
exit = 'N'
while exit != 'Y':
    print("=================================================================================================")
    print("")
    print("=================================================================================================")
    print("Welcome to Nicolas Albright Banks!")
    has_account = input("Do you have an account? (Y or N)")
    if has_account == 'Y':
        login()
    else:
        like_to_make_acc = input("Would you like to make an account? (Y or N)")
        if like_to_make_acc == 'Y':
            make_account()
    print("Welcome to Nicolas Albright Banks!")
    exit_prompt = input("Would you like to exit?(Y or N)")
    if exit_prompt == 'Y':
        exit = 'Y'
        break

print("Come back Soon!")
