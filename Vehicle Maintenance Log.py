import sqlite3

class Database:
    def __init__(self, db_name="vehicles.db"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.initialize()

    def initialize(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Vehicles (
                id INTEGER PRIMARY KEY, 
                brand TEXT, 
                model TEXT, 
                year INTEGER
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS FuelLog (
                id INTEGER PRIMARY KEY, 
                vehicle_id INTEGER, 
                mileage INTEGER, 
                fuel REAL, 
                FOREIGN KEY(vehicle_id) REFERENCES Vehicles(id)
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Reminders (
                id INTEGER PRIMARY KEY, 
                vehicle_id INTEGER, 
                type TEXT, 
                date TEXT, 
                FOREIGN KEY(vehicle_id) REFERENCES Vehicles(id)
            )
        """)
        self.connection.commit()

    def execute(self, query, params=()):
        self.cursor.execute(query, params)
        self.connection.commit()
        return self.cursor

    def close(self):
        self.connection.close()

class Vehicle:
    def __init__(self, brand, model, year):
        self.brand = brand
        self.model = model
        self.year = year

    def save(self, db):
        db.execute("INSERT INTO Vehicles (brand, model, year) VALUES (?, ?, ?)", (self.brand, self.model, self.year))

class FuelLog:
    @staticmethod
    def log_fuel(db, vehicle_id, mileage, fuel):
        db.execute("INSERT INTO FuelLog (vehicle_id, mileage, fuel) VALUES (?, ?, ?)", (vehicle_id, mileage, fuel))

class Reminder:
    @staticmethod
    def set_reminder(db, vehicle_id, reminder_type, date):
        db.execute("INSERT INTO Reminders (vehicle_id, type, date) VALUES (?, ?, ?)", (vehicle_id, reminder_type, date))

if __name__ == "__main__":
    db = Database()
    car = Vehicle("Toyota", "Camry", 2020)
    car.save(db)
    FuelLog.log_fuel(db, 1, 12000, 40.0)
    Reminder.set_reminder(db, 1, "Service", "2025-06-15")
    print("Vehicle registered and logs updated.")
    db.close()
