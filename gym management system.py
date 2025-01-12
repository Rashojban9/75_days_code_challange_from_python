import sqlite3
from datetime import datetime

# Database connection and table creation
def connect():
    conn = sqlite3.connect("gym.db")
    return conn

def create_tables():
    conn = connect()
    cursor = conn.cursor()

    # Create Members table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            contact TEXT,
            subscription_type TEXT,
            subscription_end_date TEXT
        )
    """)

    # Create Attendance table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            member_id INTEGER,
            date TEXT,
            FOREIGN KEY(member_id) REFERENCES Members(id)
        )
    """)

    # Create Trainers table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Trainers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            expertise TEXT,
            schedule TEXT
        )
    """)

    # Create Payments table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            member_id INTEGER,
            amount REAL,
            payment_date TEXT,
            FOREIGN KEY(member_id) REFERENCES Members(id)
        )
    """)

    conn.commit()
    conn.close()
    print("Tables created successfully!")

# Add a new member
def add_member():
    name = input("Enter Member Name: ")
    age = int(input("Enter Member Age: "))
    contact = input("Enter Member Contact: ")
    subscription_type = input("Enter Subscription Type: ")
    subscription_end_date = input("Enter Subscription End Date (YYYY-MM-DD): ")

    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Members (name, age, contact, subscription_type, subscription_end_date)
        VALUES (?, ?, ?, ?, ?)
    """, (name, age, contact, subscription_type, subscription_end_date))
    conn.commit()
    conn.close()
    print("Member added successfully!")

# Mark attendance
def mark_attendance():
    member_id = int(input("Enter Member ID: "))
    date = input("Enter Date (YYYY-MM-DD): ")

    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Attendance (member_id, date)
        VALUES (?, ?)
    """, (member_id, date))
    conn.commit()
    conn.close()
    print("Attendance marked successfully!")

# Add a trainer
def add_trainer():
    name = input("Enter Trainer Name: ")
    expertise = input("Enter Trainer Expertise: ")
    schedule = input("Enter Trainer Schedule: ")

    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Trainers (name, expertise, schedule)
        VALUES (?, ?, ?)
    """, (name, expertise, schedule))
    conn.commit()
    conn.close()
    print("Trainer added successfully!")

# Record payment
def record_payment():
    member_id = int(input("Enter Member ID: "))
    amount = float(input("Enter Payment Amount: "))
    payment_date = input("Enter Payment Date (YYYY-MM-DD): ")

    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Payments (member_id, amount, payment_date)
        VALUES (?, ?, ?)
    """, (member_id, amount, payment_date))
    conn.commit()
    conn.close()
    print("Payment recorded successfully!")

# Main menu
def main_menu():
    create_tables()
    while True:
        print("\nGym Management System")
        print("1. Add Member")
        print("2. Mark Attendance")
        print("3. Add Trainer")
        print("4. Record Payment")
        print("5. Exit")

        choice = input("Choose an option: ")
        if choice == '1':
            add_member()
        elif choice == '2':
            mark_attendance()
        elif choice == '3':
            add_trainer()
        elif choice == '4':
            record_payment()
        elif choice == '5':
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice! Please try again.")

# Entry point
if __name__ == "__main__":
    main_menu()
