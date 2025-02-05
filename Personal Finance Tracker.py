import sqlite3
from datetime import datetime

class Database:
    DB_NAME = "finance.db"

    @staticmethod
    def connect():
        return sqlite3.connect(Database.DB_NAME)

    @staticmethod
    def initialize():
        with Database.connect() as conn:
            cursor = conn.cursor()
            cursor.executescript('''
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    type TEXT,
                    category TEXT,
                    amount REAL,
                    date TEXT
                );
                CREATE TABLE IF NOT EXISTS budgets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category TEXT UNIQUE,
                    limit_amount REAL
                );
            ''')
            conn.commit()

class Transaction:
    def __init__(self, type, category, amount, date=None):
        self.type = type
        self.category = category
        self.amount = amount
        self.date = date or datetime.now().strftime('%Y-%m-%d')

    def save(self):
        with Database.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO transactions (type, category, amount, date) 
                VALUES (?, ?, ?, ?)''', (self.type, self.category, self.amount, self.date))
            conn.commit()

class Budget:
    @staticmethod
    def set_budget(category, limit_amount):
        with Database.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO budgets (category, limit_amount) 
                VALUES (?, ?) 
                ON CONFLICT(category) DO UPDATE SET limit_amount=?''', 
                (category, limit_amount, limit_amount))
            conn.commit()

class Report:
    @staticmethod
    def generate_monthly_report():
        with Database.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT category, SUM(amount) as total 
                FROM transactions 
                WHERE strftime('%Y-%m', date) = strftime('%Y-%m', 'now') 
                GROUP BY category''')
            print("Monthly Financial Report:")
            for row in cursor.fetchall():
                print(f"{row[0]}: {row[1]}")

if __name__ == "__main__":
    Database.initialize()
    t1 = Transaction("Expense", "Food", 50.0)
    t1.save()
    Budget.set_budget("Food", 500)
    Report.generate_monthly_report()
