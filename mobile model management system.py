import sqlite3

class Mobile:
    def __init__(self, mobile_id, name, brand, price, specifications):
        self.mobile_id = mobile_id
        self.name = name
        self.brand = brand
        self.price = price
        self.specifications = specifications

    def __str__(self):
        return f"ID: {self.mobile_id}, Name: {self.name}, Brand: {self.brand}, Price: {self.price}, Specifications: {self.specifications}"

class DatabaseManager:
    DB_NAME = "mobiles.db"

    @staticmethod
    def initialize_database():
        with sqlite3.connect(DatabaseManager.DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Mobiles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    brand TEXT NOT NULL,
                    price REAL NOT NULL,
                    specifications TEXT NOT NULL
                )
            ''')
            conn.commit()

    @staticmethod
    def add_mobile(name, brand, price, specifications):
        with sqlite3.connect(DatabaseManager.DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO Mobiles (name, brand, price, specifications)
                VALUES (?, ?, ?, ?)
            ''', (name, brand, price, specifications))
            conn.commit()
            print("Mobile added successfully.")

    @staticmethod
    def update_mobile(mobile_id, name, brand, price, specifications):
        with sqlite3.connect(DatabaseManager.DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE Mobiles
                SET name = ?, brand = ?, price = ?, specifications = ?
                WHERE id = ?
            ''', (name, brand, price, specifications, mobile_id))
            if cursor.rowcount > 0:
                conn.commit()
                print("Mobile updated successfully.")
            else:
                print("Mobile not found.")

    @staticmethod
    def remove_mobile(mobile_id):
        with sqlite3.connect(DatabaseManager.DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                DELETE FROM Mobiles WHERE id = ?
            ''', (mobile_id,))
            if cursor.rowcount > 0:
                conn.commit()
                print("Mobile removed successfully.")
            else:
                print("Mobile not found.")

    @staticmethod
    def search_mobile_by_name(name):
        with sqlite3.connect(DatabaseManager.DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM Mobiles WHERE name LIKE ?
            ''', (f"%{name}%",))
            results = cursor.fetchall()
            if results:
                for row in results:
                    print(Mobile(*row))
            else:
                print("No mobiles found with the given name.")

    @staticmethod
    def search_mobile_by_brand(brand):
        with sqlite3.connect(DatabaseManager.DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM Mobiles WHERE brand LIKE ?
            ''', (f"%{brand}%",))
            results = cursor.fetchall()
            if results:
                for row in results:
                    print(Mobile(*row))
            else:
                print("No mobiles found with the given brand.")

if __name__ == "__main__":
    DatabaseManager.initialize_database()

    while True:
        print("\nMobile Management System")
        print("1. Add Mobile")
        print("2. Update Mobile")
        print("3. Remove Mobile")
        print("4. Search Mobile by Name")
        print("5. Search Mobile by Brand")
        print("6. Exit")

        choice = input("Enter your choice: ")
        if choice == "1":
            name = input("Enter name: ")
            brand = input("Enter brand: ")
            price = float(input("Enter price: "))
            specifications = input("Enter specifications: ")
            DatabaseManager.add_mobile(name, brand, price, specifications)

        elif choice == "2":
            mobile_id = int(input("Enter mobile ID to update: "))
            name = input("Enter new name: ")
            brand = input("Enter new brand: ")
            price = float(input("Enter new price: "))
            specifications = input("Enter new specifications: ")
            DatabaseManager.update_mobile(mobile_id, name, brand, price, specifications)

        elif choice == "3":
            mobile_id = int(input("Enter mobile ID to remove: "))
            DatabaseManager.remove_mobile(mobile_id)

        elif choice == "4":
            name = input("Enter name to search: ")
            DatabaseManager.search_mobile_by_name(name)

        elif choice == "5":
            brand = input("Enter brand to search: ")
            DatabaseManager.search_mobile_by_brand(brand)

        elif choice == "6":
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")
