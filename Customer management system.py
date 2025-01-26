import sqlite3


class Customer:
    """Represents a Customer object."""

    def __init__(self, customer_id, name, phone, email):
        self.customer_id = customer_id
        self.name = name
        self.phone = phone
        self.email = email

    def __str__(self):
        return f"ID: {self.customer_id} | Name: {self.name} | Phone: {self.phone} | Email: {self.email}"


class CustomerDAO:
    """Handles database operations."""

    def __init__(self, db_name="customer_management.db"):
        self.db_name = db_name
        self._initialize_database()

    def _initialize_database(self):
        """Creates the customers table if it doesn't exist."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS customers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    phone TEXT NOT NULL,
                    email TEXT NOT NULL
                )
            """)
            conn.commit()

    def add_customer(self, name, phone, email):
        """Adds a new customer to the database."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO customers (name, phone, email) VALUES (?, ?, ?)", (name, phone, email))
            conn.commit()
        print("Customer added successfully!")

    def update_customer(self, customer_id, name, phone, email):
        """Updates an existing customer."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE customers
                SET name = ?, phone = ?, email = ?
                WHERE id = ?
            """, (name, phone, email, customer_id))
            if cursor.rowcount > 0:
                print("Customer updated successfully!")
            else:
                print("Customer not found.")
            conn.commit()

    def remove_customer(self, customer_id):
        """Removes a customer from the database."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM customers WHERE id = ?", (customer_id,))
            if cursor.rowcount > 0:
                print("Customer removed successfully!")
            else:
                print("Customer not found.")
            conn.commit()

    def list_customers(self):
        """Lists all customers."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM customers")
            rows = cursor.fetchall()
            if rows:
                print("\nRegistered Customers:")
                for row in rows:
                    customer = Customer(row[0], row[1], row[2], row[3])
                    print(customer)
            else:
                print("\nNo customers found.")


class CustomerManagementApp:
    """Main Application class."""

    @staticmethod
    def run():
        dao = CustomerDAO()
        while True:
            print("\n1. Add Customer | 2. Update Customer | 3. Remove Customer | 4. View Customers | 5. Exit")
            choice = input("Choose an option: ").strip()

            if choice == "1":
                name = input("Enter name: ").strip()
                phone = input("Enter phone: ").strip()
                email = input("Enter email: ").strip()
                dao.add_customer(name, phone, email)

            elif choice == "2":
                customer_id = int(input("Enter customer ID to update: ").strip())
                name = input("Enter new name: ").strip()
                phone = input("Enter new phone: ").strip()
                email = input("Enter new email: ").strip()
                dao.update_customer(customer_id, name, phone, email)

            elif choice == "3":
                customer_id = int(input("Enter customer ID to remove: ").strip())
                dao.remove_customer(customer_id)

            elif choice == "4":
                dao.list_customers()

            elif choice == "5":
                print("Goodbye!")
                break

            else:
                print("Invalid choice, please try again.")


# Run the application
if __name__ == "__main__":
    CustomerManagementApp.run()
