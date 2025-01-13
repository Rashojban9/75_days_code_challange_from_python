import sqlite3
from datetime import datetime

# Database connection and initialization
def connect():
    return sqlite3.connect("pharmacy.db")

def create_tables():
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Medicines (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                batch_no TEXT,
                expiry_date TEXT,
                quantity INTEGER,
                price REAL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                medicine_id INTEGER,
                quantity INTEGER,
                total_price REAL,
                order_date TEXT,
                FOREIGN KEY(medicine_id) REFERENCES Medicines(id)
            )
        """)
        conn.commit()

# Add new medicine
def add_medicine():
    name = input("Enter Medicine Name: ")
    batch_no = input("Enter Batch Number: ")
    expiry_date = input("Enter Expiry Date (YYYY-MM-DD): ")
    quantity = int(input("Enter Quantity: "))
    price = float(input("Enter Price per Unit: "))

    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Medicines (name, batch_no, expiry_date, quantity, price)
            VALUES (?, ?, ?, ?, ?)
        """, (name, batch_no, expiry_date, quantity, price))
        conn.commit()
        print("Medicine added successfully!")

# Generate bill and place order
def generate_bill():
    medicine_id = int(input("Enter Medicine ID: "))
    quantity = int(input("Enter Quantity: "))

    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name, price, quantity FROM Medicines WHERE id = ?", (medicine_id,))
        result = cursor.fetchone()

        if result:
            name, price_per_unit, available_quantity = result
            if quantity > available_quantity:
                print("Insufficient stock!")
                return

            total_price = price_per_unit * quantity
            cursor.execute("""
                INSERT INTO Orders (medicine_id, quantity, total_price, order_date)
                VALUES (?, ?, ?, ?)
            """, (medicine_id, quantity, total_price, datetime.now().strftime("%Y-%m-%d")))
            cursor.execute("UPDATE Medicines SET quantity = quantity - ? WHERE id = ?", (quantity, medicine_id))
            conn.commit()
            print(f"Order placed for {name}! Total Bill: ${total_price:.2f}")
        else:
            print("Medicine not found!")

# Notify for restocking
def notify_restocking():
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, quantity FROM Medicines WHERE quantity < 10")
        medicines = cursor.fetchall()

        if medicines:
            print("Medicines to Restock:")
            for med in medicines:
                print(f"ID: {med[0]}, Name: {med[1]}, Quantity: {med[2]}")
        else:
            print("No medicines need restocking.")

# List all medicines
def list_medicines():
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, batch_no, expiry_date, quantity, price FROM Medicines")
        medicines = cursor.fetchall()

        print("\nAvailable Medicines:")
        print(f"{'ID':<5}{'Name':<20}{'Batch No':<15}{'Expiry Date':<15}{'Quantity':<10}{'Price':<10}")
        for med in medicines:
            print(f"{med[0]:<5}{med[1]:<20}{med[2]:<15}{med[3]:<15}{med[4]:<10}{med[5]:<10.2f}")

# Main menu
def main():
    create_tables()

    while True:
        print("\nPharmacy Management System")
        print("1. Add Medicine")
        print("2. Generate Bill")
        print("3. Notify Restocking")
        print("4. List Medicines")
        print("5. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            add_medicine()
        elif choice == "2":
            generate_bill()
        elif choice == "3":
            notify_restocking()
        elif choice == "4":
            list_medicines()
        elif choice == "5":
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
