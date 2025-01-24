import sqlite3


class DatabaseManager:
    """Manages the SQLite database connection and initialization."""
    def __init__(self, db_name="mobile_management.db"):
        self.connection = sqlite3.connect(db_name)
        self.initialize_database()

    def initialize_database(self):
        """Initialize tables for brands, mobiles, customers, and sales."""
        queries = [
            """
            CREATE TABLE IF NOT EXISTS brands (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS mobiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                brand_id INTEGER NOT NULL,
                model TEXT NOT NULL,
                price REAL NOT NULL,
                stock INTEGER NOT NULL,
                FOREIGN KEY (brand_id) REFERENCES brands (id)
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mobile_id INTEGER NOT NULL,
                customer_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                FOREIGN KEY (mobile_id) REFERENCES mobiles (id),
                FOREIGN KEY (customer_id) REFERENCES customers (id)
            );
            """
        ]
        cursor = self.connection.cursor()
        for query in queries:
            cursor.execute(query)
        self.connection.commit()

    def execute_query(self, query, params=()):
        """Executes a query with optional parameters."""
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        self.connection.commit()
        return cursor

    def close(self):
        """Closes the database connection."""
        self.connection.close()


class MobileManagementSystem:
    """Manages brands, mobiles, customers, and sales."""
    def __init__(self):
        self.db_manager = DatabaseManager()

    # Brand Management
    def add_brand(self):
        name = input("Enter brand name: ")
        query = "INSERT INTO brands (name) VALUES (?);"
        self.db_manager.execute_query(query, (name,))
        print(f"Brand '{name}' added successfully!")

    def view_brands(self):
        query = "SELECT * FROM brands;"
        cursor = self.db_manager.execute_query(query)
        print("\nAvailable Brands:")
        for row in cursor.fetchall():
            print(f"ID: {row[0]}, Name: {row[1]}")

    # Mobile Model Management
    def add_mobile(self):
        self.view_brands()
        brand_id = int(input("Enter brand ID: "))
        model = input("Enter model name: ")
        price = float(input("Enter price: "))
        stock = int(input("Enter stock quantity: "))
        query = "INSERT INTO mobiles (brand_id, model, price, stock) VALUES (?, ?, ?, ?);"
        self.db_manager.execute_query(query, (brand_id, model, price, stock))
        print(f"Mobile '{model}' added successfully!")

    def view_mobiles(self):
        query = """
        SELECT m.id, b.name, m.model, m.price, m.stock
        FROM mobiles m
        JOIN brands b ON m.brand_id = b.id;
        """
        cursor = self.db_manager.execute_query(query)
        print("\nAvailable Mobiles:")
        for row in cursor.fetchall():
            print(f"ID: {row[0]}, Brand: {row[1]}, Model: {row[2]}, Price: {row[3]}, Stock: {row[4]}")

    # Customer Management
    def add_customer(self):
        name = input("Enter customer name: ")
        phone = input("Enter phone number: ")
        email = input("Enter email: ")
        query = "INSERT INTO customers (name, phone, email) VALUES (?, ?, ?);"
        self.db_manager.execute_query(query, (name, phone, email))
        print(f"Customer '{name}' added successfully!")

    def view_customers(self):
        query = "SELECT * FROM customers;"
        cursor = self.db_manager.execute_query(query)
        print("\nRegistered Customers:")
        for row in cursor.fetchall():
            print(f"ID: {row[0]}, Name: {row[1]}, Phone: {row[2]}, Email: {row[3]}")

    # Sales Management
    def record_sale(self):
        self.view_mobiles()
        mobile_id = int(input("Enter mobile ID: "))
        self.view_customers()
        customer_id = int(input("Enter customer ID: "))
        quantity = int(input("Enter quantity: "))
        date = input("Enter sale date (YYYY-MM-DD): ")

        # Check stock availability
        stock_query = "SELECT stock FROM mobiles WHERE id = ?;"
        cursor = self.db_manager.execute_query(stock_query, (mobile_id,))
        stock = cursor.fetchone()[0]
        if stock < quantity:
            print("Error: Not enough stock available!")
            return

        # Record sale
        sale_query = "INSERT INTO sales (mobile_id, customer_id, date, quantity) VALUES (?, ?, ?, ?);"
        self.db_manager.execute_query(sale_query, (mobile_id, customer_id, date, quantity))

        # Update stock
        update_stock_query = "UPDATE mobiles SET stock = stock - ? WHERE id = ?;"
        self.db_manager.execute_query(update_stock_query, (quantity, mobile_id))
        print("Sale recorded successfully!")

    # Report Generation
    def generate_report(self):
        query = """
        SELECT b.name AS brand, m.model, SUM(s.quantity) AS total_sales
        FROM sales s
        JOIN mobiles m ON s.mobile_id = m.id
        JOIN brands b ON m.brand_id = b.id
        GROUP BY m.id;
        """
        cursor = self.db_manager.execute_query(query)
        print("\nSales Report:")
        for row in cursor.fetchall():
            print(f"Brand: {row[0]}, Model: {row[1]}, Total Sales: {row[2]}")

    def run(self):
        """Main menu loop."""
        while True:
            print("\n=== Mobile Management System ===")
            print("1. Add Brand")
            print("2. View Brands")
            print("3. Add Mobile")
            print("4. View Mobiles")
            print("5. Add Customer")
            print("6. View Customers")
            print("7. Record Sale")
            print("8. Generate Sales Report")
            print("9. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.add_brand()
            elif choice == "2":
                self.view_brands()
            elif choice == "3":
                self.add_mobile()
            elif choice == "4":
                self.view_mobiles()
            elif choice == "5":
                self.add_customer()
            elif choice == "6":
                self.view_customers()
            elif choice == "7":
                self.record_sale()
            elif choice == "8":
                self.generate_report()
            elif choice == "9":
                self.db_manager.close()
                print("Goodbye!")
                break
            else:
                print("Invalid choice! Please try again.")


if __name__ == "__main__":
    system = MobileManagementSystem()
    system.run()
