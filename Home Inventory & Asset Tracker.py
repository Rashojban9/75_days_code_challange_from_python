import sqlite3

class Database:
    def __init__(self, db_name="home_inventory.db"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.initialize()

    def initialize(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Items (
                id INTEGER PRIMARY KEY, 
                category TEXT, 
                name TEXT, 
                value REAL
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Warranties (
                id INTEGER PRIMARY KEY, 
                item_id INTEGER, 
                expiration_date TEXT, 
                FOREIGN KEY(item_id) REFERENCES Items(id)
            )
        """)
        self.connection.commit()

    def execute(self, query, params=()):
        self.cursor.execute(query, params)
        self.connection.commit()
        return self.cursor

    def close(self):
        self.connection.close()

class Item:
    def __init__(self, category, name, value):
        self.category = category
        self.name = name
        self.value = value

    def save(self, db):
        db.execute("INSERT INTO Items (category, name, value) VALUES (?, ?, ?)", (self.category, self.name, self.value))

class Warranty:
    @staticmethod
    def set_warranty(db, item_id, expiration_date):
        db.execute("INSERT INTO Warranties (item_id, expiration_date) VALUES (?, ?)", (item_id, expiration_date))

class AssetTracker:
    @staticmethod
    def calculate_total_value(db):
        result = db.execute("SELECT SUM(value) FROM Items").fetchone()
        return result[0] if result[0] else 0.0

if __name__ == "__main__":
    db = Database()
    item = Item("Electronics", "Laptop", 1200.0)
    item.save(db)
    Warranty.set_warranty(db, 1, "2026-08-10")
    total_value = AssetTracker.calculate_total_value(db)
    print(f"Total asset value: ${total_value}")
    db.close()
