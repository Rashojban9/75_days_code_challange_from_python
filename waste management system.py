import sqlite3
from datetime import datetime

# Database Connection & Initialization
class DatabaseHelper:
    DB_NAME = "waste_management.db"

    @staticmethod
    def connect():
        return sqlite3.connect(DatabaseHelper.DB_NAME)

    @staticmethod
    def initialize_db():
        queries = [
            """CREATE TABLE IF NOT EXISTS Users (id INTEGER PRIMARY KEY, name TEXT, role TEXT, email TEXT, password TEXT);""",
            """CREATE TABLE IF NOT EXISTS WasteBins (id INTEGER PRIMARY KEY, location TEXT, capacity INTEGER, current_level INTEGER, last_collected TEXT);""",
            """CREATE TABLE IF NOT EXISTS WasteCollection (id INTEGER PRIMARY KEY, bin_id INTEGER, collector_id INTEGER, scheduled_date TEXT, status TEXT);""",
            """CREATE TABLE IF NOT EXISTS Recyclables (id INTEGER PRIMARY KEY, type TEXT, quantity INTEGER, bin_id INTEGER);"""
        ]
        conn = DatabaseHelper.connect()
        cursor = conn.cursor()
        for query in queries:
            cursor.execute(query)
        conn.commit()
        conn.close()

# User Authentication
class User:
    def __init__(self, user_id, name, role, email, password):
        self.id = user_id
        self.name = name
        self.role = role
        self.email = email
        self.password = password

class UserService:
    def login(self, email, password):
        conn = DatabaseHelper.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Users WHERE email = ? AND password = ?", (email, password))
        user = cursor.fetchone()
        conn.close()
        return user is not None

# WasteBin Model & Operations
class WasteBin:
    def __init__(self, bin_id, location, capacity, current_level, last_collected):
        self.id = bin_id
        self.location = location
        self.capacity = capacity
        self.current_level = current_level
        self.last_collected = last_collected

class WasteBinDAO:
    def add_bin(self, location, capacity, current_level):
        conn = DatabaseHelper.connect()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO WasteBins (location, capacity, current_level, last_collected) VALUES (?, ?, ?, ?)",
                       (location, capacity, current_level, datetime.now().strftime("%Y-%m-%d")))
        conn.commit()
        conn.close()

    def update_bin_level(self, bin_id, new_level):
        conn = DatabaseHelper.connect()
        cursor = conn.cursor()
        cursor.execute("UPDATE WasteBins SET current_level = ? WHERE id = ?", (new_level, bin_id))
        conn.commit()
        conn.close()
        if new_level >= 80:
            print(f"⚠ Alert: Waste Bin {bin_id} is almost full! Schedule a collection.")

    def delete_bin(self, bin_id):
        conn = DatabaseHelper.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM WasteBins WHERE id = ?", (bin_id,))
        conn.commit()
        conn.close()

    def search_bins(self, keyword):
        conn = DatabaseHelper.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM WasteBins WHERE location LIKE ?", ('%' + keyword + '%',))
        bins = cursor.fetchall()
        conn.close()
        return bins

# Waste Collection Operations
class WasteCollection:
    def __init__(self, collection_id, bin_id, collector_id, scheduled_date, status):
        self.id = collection_id
        self.bin_id = bin_id
        self.collector_id = collector_id
        self.scheduled_date = scheduled_date
        self.status = status

class WasteCollectionDAO:
    def schedule_collection(self, bin_id, collector_id, date):
        conn = DatabaseHelper.connect()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO WasteCollection (bin_id, collector_id, scheduled_date, status) VALUES (?, ?, ?, 'Scheduled')",
                       (bin_id, collector_id, date))
        conn.commit()
        conn.close()

    def generate_report(self):
        conn = DatabaseHelper.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM WasteCollection")
        records = cursor.fetchall()
        conn.close()
        return records

# Recyclable Operations
class Recyclable:
    def __init__(self, recyclable_id, bin_id, quantity, type_):
        self.id = recyclable_id
        self.bin_id = bin_id
        self.quantity = quantity
        self.type = type_

class RecyclableDAO:
    def add_recyclable(self, type_, quantity, bin_id):
        conn = DatabaseHelper.connect()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Recyclables (type, quantity, bin_id) VALUES (?, ?, ?)",
                       (type_, quantity, bin_id))
        conn.commit()
        conn.close()

    def delete_recyclable(self, recyclable_id):
        conn = DatabaseHelper.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Recyclables WHERE id = ?", (recyclable_id,))
        conn.commit()
        conn.close()

# Main Execution
if __name__ == "__main__":
    DatabaseHelper.initialize_db()

    user_service = UserService()
    bin_dao = WasteBinDAO()
    collection_dao = WasteCollectionDAO()
    recyclable_dao = RecyclableDAO()

    if user_service.login("admin@example.com", "password"):
        bin_dao.add_bin("City Center", 100, 90)  # Add a bin
        bin_dao.update_bin_level(1, 85)  # Update bin level (triggers alert if needed)
        collection_dao.schedule_collection(1, 1, "2024-02-05")  # Schedule collection
        recyclable_dao.add_recyclable("Plastic", 30, 1)  # Add recyclable
        bins = bin_dao.search_bins("City")
        
        print("\n🔍 Search Results:")
        for bin in bins:
            print(f"ID: {bin[0]}, Location: {bin[1]}, Capacity: {bin[2]}, Current Level: {bin[3]}")
        
        print("\n📊 Waste Collection Report:")
        for record in collection_dao.generate_report():
            print(f"Bin ID: {record[1]}, Collector ID: {record[2]}, Date: {record[3]}, Status: {record[4]}")
    else:
        print("Login Failed!")
