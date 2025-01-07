import sqlite3

class VehicleRentalSystem:

    def __init__(self):
        self.conn = sqlite3.connect('vehicle_rental.db')
        self.create_tables()

    def create_tables(self):
        vehicles_table = '''CREATE TABLE IF NOT EXISTS vehicles (
                                vehicle_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                vehicle_name TEXT,
                                type TEXT,
                                rental_price REAL,
                                status TEXT);'''

        bookings_table = '''CREATE TABLE IF NOT EXISTS bookings (
                                booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                vehicle_id INTEGER,
                                customer_name TEXT,
                                contact_number TEXT,
                                booking_date TEXT,
                                return_date TEXT,
                                total_cost REAL,
                                status TEXT,
                                FOREIGN KEY (vehicle_id) REFERENCES vehicles(vehicle_id));'''

        cursor = self.conn.cursor()
        cursor.execute(vehicles_table)
        cursor.execute(bookings_table)
        self.conn.commit()

    def add_vehicle(self, name, vehicle_type, price):
        sql = '''INSERT INTO vehicles(vehicle_name, type, rental_price, status)
                 VALUES(?, ?, ?, 'Available');'''
        cursor = self.conn.cursor()
        cursor.execute(sql, (name, vehicle_type, price))
        self.conn.commit()
        print("Vehicle added successfully.")

    def book_vehicle(self, vehicle_id, customer_name, contact, booking_date, return_date, cost):
        sql = '''INSERT INTO bookings(vehicle_id, customer_name, contact_number, booking_date, return_date, total_cost, status)
                 VALUES(?, ?, ?, ?, ?, ?, 'Booked');'''
        cursor = self.conn.cursor()
        cursor.execute(sql, (vehicle_id, customer_name, contact, booking_date, return_date, cost))
        cursor.execute("UPDATE vehicles SET status = 'Booked' WHERE vehicle_id = ?;", (vehicle_id,))
        self.conn.commit()
        print("Vehicle booked successfully.")

    def return_vehicle(self, booking_id):
        cursor = self.conn.cursor()
        cursor.execute("UPDATE bookings SET status = 'Returned' WHERE booking_id = ?;", (booking_id,))
        cursor.execute("SELECT vehicle_id FROM bookings WHERE booking_id = ?;", (booking_id,))
        vehicle_id = cursor.fetchone()[0]
        cursor.execute("UPDATE vehicles SET status = 'Available' WHERE vehicle_id = ?;", (vehicle_id,))
        self.conn.commit()
        print("Vehicle returned successfully.")

    def view_vehicles(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM vehicles;")
        rows = cursor.fetchall()
        for row in rows:
            print(row)

    def close_connection(self):
        self.conn.close()


def main():
    system = VehicleRentalSystem()

    while True:
        print("1. Add Vehicle\n2. View Vehicles\n3. Book Vehicle\n4. Return Vehicle\n5. Exit")
        choice = int(input("Choose an option: "))

        if choice == 1:
            name = input("Enter vehicle name: ")
            vehicle_type = input("Enter type: ")
            price = float(input("Enter rental price: "))
            system.add_vehicle(name, vehicle_type, price)

        elif choice == 2:
            system.view_vehicles()

        elif choice == 3:
            vehicle_id = int(input("Enter vehicle ID: "))
            customer_name = input("Enter customer name: ")
            contact = input("Enter contact number: ")
            booking_date = input("Enter booking date: ")
            return_date = input("Enter return date: ")
            cost = float(input("Enter total cost: "))
            system.book_vehicle(vehicle_id, customer_name, contact, booking_date, return_date, cost)

        elif choice == 4:
            booking_id = int(input("Enter booking ID: "))
            system.return_vehicle(booking_id)

        elif choice == 5:
            system.close_connection()
            print("Exiting...")
            break

        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    main()
