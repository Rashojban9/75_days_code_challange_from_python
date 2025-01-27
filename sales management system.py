import sqlite3
from datetime import datetime

# Database Manager
class DatabaseManager:
    def __init__(self, db_name="sales_management.db"):
        self.db_name = db_name
        self.initialize_database()

    def initialize_database(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sales (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    customer_name TEXT NOT NULL,
                    model TEXT NOT NULL,
                    sale_date TEXT NOT NULL,
                    price REAL NOT NULL
                )
            ''')

    def get_connection(self):
        return sqlite3.connect(self.db_name)

# Sale Entity
class Sale:
    def __init__(self, customer_name, model, sale_date, price):
        self.customer_name = customer_name
        self.model = model
        self.sale_date = sale_date
        self.price = price

# Sales Manager
class SalesManager:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def record_sale(self, sale):
        query = "INSERT INTO sales (customer_name, model, sale_date, price) VALUES (?, ?, ?, ?)"
        try:
            with self.db_manager.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (sale.customer_name, sale.model, sale.sale_date, sale.price))
                print("Sale recorded successfully.")
        except sqlite3.Error as e:
            print(f"Error recording sale: {e}")

    def display_sales_history(self, filter_type, filter_value):
        query = {
            "model": "SELECT * FROM sales WHERE model = ?",
            "customer": "SELECT * FROM sales WHERE customer_name = ?",
            "date": "SELECT * FROM sales WHERE sale_date = ?"
        }.get(filter_type.lower())

        if not query:
            print("Invalid filter type.")
            return

        try:
            with self.db_manager.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (filter_value,))
                rows = cursor.fetchall()
                for row in rows:
                    print(f"ID: {row[0]}, Customer: {row[1]}, Model: {row[2]}, Date: {row[3]}, Price: {row[4]}")
        except sqlite3.Error as e:
            print(f"Error fetching sales history: {e}")

    def generate_sales_report(self):
        query = "SELECT COUNT(*) AS total_sales, SUM(price) AS total_revenue FROM sales"
        try:
            with self.db_manager.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query)
                result = cursor.fetchone()
                print(f"Total Sales: {result[0]}")
                print(f"Total Revenue: ${result[1]:.2f}")
        except sqlite3.Error as e:
            print(f"Error generating sales report: {e}")

# Main Application
def main():
    db_manager = DatabaseManager()
    sales_manager = SalesManager(db_manager)

    while True:
        print("\n--- Sales Management System ---")
        print("1. Record a Sale")
        print("2. View Sales History")
        print("3. Generate Sales Report")
        print("4. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            customer_name = input("Enter customer name: ")
            model = input("Enter phone model: ")
            sale_date = input("Enter sale date (YYYY-MM-DD): ")
            price = float(input("Enter price: "))

            sale = Sale(customer_name, model, sale_date, price)
            sales_manager.record_sale(sale)

        elif choice == "2":
            filter_type = input("Filter by (model/customer/date): ")
            filter_value = input(f"Enter value for {filter_type}: ")
            sales_manager.display_sales_history(filter_type, filter_value)

        elif choice == "3":
            sales_manager.generate_sales_report()

        elif choice == "4":
            print("Exiting system. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
