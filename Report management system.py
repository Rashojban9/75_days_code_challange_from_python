import sqlite3

# DatabaseManager: Handles database connection and queries
class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path

    def connect(self):
        return sqlite3.connect(self.db_path)

    def execute_query(self, query, params=()):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()

    def execute_update(self, query, params=()):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()

# CarModel: Represents a car model
class CarModel:
    def __init__(self, model, brand, inventory, price):
        self.model = model
        self.brand = brand
        self.inventory = inventory
        self.price = price

# ReportGenerator: Generates reports
class ReportGenerator:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def generate_total_sales_by_model(self):
        query = "SELECT model, SUM(quantity) AS total_sales FROM sales GROUP BY model;"
        results = self.db_manager.execute_query(query)
        print("Total Sales by Model:")
        for model, total_sales in results:
            print(f"Model: {model}, Total Sales: {total_sales}")

    def generate_revenue_report(self):
        query = "SELECT model, SUM(quantity * price) AS revenue FROM sales GROUP BY model;"
        results = self.db_manager.execute_query(query)
        print("Revenue Report:")
        for model, revenue in results:
            print(f"Model: {model}, Revenue: {revenue:.2f}")

    def generate_inventory_report(self):
        query = "SELECT * FROM inventory;"
        results = self.db_manager.execute_query(query)
        print("Inventory Report:")
        for model, brand, inventory, price in results:
            print(f"Model: {model}, Brand: {brand}, Inventory: {inventory}, Price: {price:.2f}")

# Main application class
class ReportApplication:
    @staticmethod
    def initialize_database(db_manager):
        create_inventory_table = """
        CREATE TABLE IF NOT EXISTS inventory (
            model TEXT PRIMARY KEY,
            brand TEXT,
            inventory INTEGER,
            price REAL
        );
        """
        create_sales_table = """
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model TEXT,
            quantity INTEGER,
            price REAL,
            FOREIGN KEY (model) REFERENCES inventory (model)
        );
        """
        db_manager.execute_update(create_inventory_table)
        db_manager.execute_update(create_sales_table)

        # Insert sample data
        insert_inventory = """
        INSERT OR IGNORE INTO inventory (model, brand, inventory, price) VALUES
        ('Model X', 'Tesla', 50, 79999.99),
        ('Model S', 'Tesla', 30, 89999.99),
        ('Mustang', 'Ford', 20, 55999.99);
        """
        insert_sales = """
        INSERT INTO sales (model, quantity, price) VALUES
        ('Model X', 10, 79999.99),
        ('Model S', 5, 89999.99),
        ('Mustang', 2, 55999.99);
        """
        db_manager.execute_update(insert_inventory)
        db_manager.execute_update(insert_sales)

    @staticmethod
    def main():
        db_path = "car_dealership.db"
        db_manager = DatabaseManager(db_path)

        # Initialize database
        ReportApplication.initialize_database(db_manager)

        # Generate reports
        report_generator = ReportGenerator(db_manager)
        report_generator.generate_total_sales_by_model()
        report_generator.generate_revenue_report()
        report_generator.generate_inventory_report()

if __name__ == "__main__":
    ReportApplication.main()
