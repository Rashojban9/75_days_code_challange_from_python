import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('bank.db')
c = conn.cursor()

# Create tables
c.execute('''CREATE TABLE IF NOT EXISTS Accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                balance REAL
            )''')

c.execute('''CREATE TABLE IF NOT EXISTS Loans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_id INTEGER,
                amount REAL,
                interest_rate REAL,
                FOREIGN KEY(account_id) REFERENCES Accounts(id)
            )''')

conn.commit()

# Add account
def add_account(name, balance):
    c.execute("INSERT INTO Accounts (name, balance) VALUES (?, ?)", (name, balance))
    conn.commit()
    print("Account created successfully!")

# Deposit
def deposit(account_id, amount):
    c.execute("UPDATE Accounts SET balance = balance + ? WHERE id = ?", (amount, account_id))
    conn.commit()
    print("Deposit successful!")

# Withdraw
def withdraw(account_id, amount):
    c.execute("SELECT balance FROM Accounts WHERE id = ?", (account_id,))
    balance = c.fetchone()[0]
    if balance >= amount:
        c.execute("UPDATE Accounts SET balance = balance - ? WHERE id = ?", (amount, account_id))
        conn.commit()
        print("Withdrawal successful!")
    else:
        print("Insufficient balance!")

# View account statement
def view_statement(account_id):
    c.execute("SELECT * FROM Accounts WHERE id = ?", (account_id,))
    account = c.fetchone()
    if account:
        print(f"ID: {account[0]}, Name: {account[1]}, Balance: ${account[2]:.2f}")
    else:
        print("Account not found!")

# Main menu
def main():
    while True:
        print("\nBanking Management System")
        print("1. Add Account")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. View Statement")
        print("5. Exit")
        choice = int(input("Choose an option: "))

        if choice == 1:
            name = input("Enter Name: ")
            balance = float(input("Enter Initial Balance: "))
            add_account(name, balance)
        elif choice == 2:
            account_id = int(input("Enter Account ID: "))
            amount = float(input("Enter Amount to Deposit: "))
            deposit(account_id, amount)
        elif choice == 3:
            account_id = int(input("Enter Account ID: "))
            amount = float(input("Enter Amount to Withdraw: "))
            withdraw(account_id, amount)
        elif choice == 4:
            account_id = int(input("Enter Account ID: "))
            view_statement(account_id)
        elif choice == 5:
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

    conn.close()

if __name__ == "__main__":
    main()
