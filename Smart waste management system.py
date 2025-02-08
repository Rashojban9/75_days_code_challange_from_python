import sqlite3

class DatabaseManager:
    def __init__(self, db_name="waste_management.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS WasteBin (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                location TEXT,
                                fillLevel INTEGER,
                                category TEXT)''')
        self.conn.commit()

    def insert_bin(self, location, fill_level, category):
        self.cursor.execute("INSERT INTO WasteBin (location, fillLevel, category) VALUES (?, ?, ?)",
                            (location, fill_level, category))
        self.conn.commit()

    def get_full_bins(self):
        self.cursor.execute("SELECT * FROM WasteBin WHERE fillLevel >= 100")
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()

class WasteBin:
    def __init__(self, bin_id, location, fill_level, category):
        self.id = bin_id
        self.location = location
        self.fill_level = fill_level
        self.category = category

class WasteCollector:
    @staticmethod
    def notify_collectors():
        db = DatabaseManager()
        full_bins = db.get_full_bins()
        for bin in full_bins:
            print(f"Collector Alert: Bin at {bin[1]} is full ({bin[3]})")
        db.close()

if __name__ == "__main__":
    db = DatabaseManager()
    db.insert_bin("Central Park", 100, "Recyclable")
    db.insert_bin("Downtown", 80, "Organic")
    db.insert_bin("Industrial Zone", 120, "Hazardous")
    db.close()
    
    WasteCollector.notify_collectors()
