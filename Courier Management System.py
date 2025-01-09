import sqlite3

class CourierManagementSystem:

    def __init__(self):
        self.conn = sqlite3.connect('courier_management.db')
        self.create_tables()

    def create_tables(self):
        parcels_table = '''CREATE TABLE IF NOT EXISTS parcels (
                            parcel_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            sender_name TEXT,
                            receiver_name TEXT,
                            pickup_address TEXT,
                            delivery_address TEXT,
                            status TEXT,
                            payment_status TEXT);'''
        cursor = self.conn.cursor()
        cursor.execute(parcels_table)
        self.conn.commit()

    def add_parcel(self, sender_name, receiver_name, pickup_address, delivery_address):
        sql = '''INSERT INTO parcels(sender_name, receiver_name, pickup_address, delivery_address, status, payment_status)
                 VALUES(?, ?, ?, ?, 'Pending Pickup', 'Unpaid');'''
        cursor = self.conn.cursor()
        cursor.execute(sql, (sender_name, receiver_name, pickup_address, delivery_address))
        self.conn.commit()
        print("Parcel added successfully.")

    def update_parcel_status(self, parcel_id, status):
        sql = '''UPDATE parcels SET status = ? WHERE parcel_id = ?;'''
        cursor = self.conn.cursor()
        cursor.execute(sql, (status, parcel_id))
        self.conn.commit()
        print("Parcel status updated successfully.")

    def update_payment_status(self, parcel_id, payment_status):
        sql = '''UPDATE parcels SET payment_status = ? WHERE parcel_id = ?;'''
        cursor = self.conn.cursor()
        cursor.execute(sql, (payment_status, parcel_id))
        self.conn.commit()
        print("Payment status updated successfully.")

    def view_parcels(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM parcels;")
        rows = cursor.fetchall()
        for row in rows:
            print(row)

    def close_connection(self):
        self.conn.close()


def main():
    system = CourierManagementSystem()

    while True:
        print("1. Add Parcel\n2. View Parcels\n3. Update Parcel Status\n4. Update Payment Status\n5. Exit")
        choice = int(input("Choose an option: "))

        if choice == 1:
            sender_name = input("Enter sender name: ")
            receiver_name = input("Enter receiver name: ")
            pickup_address = input("Enter pickup address: ")
            delivery_address = input("Enter delivery address: ")
            system.add_parcel(sender_name, receiver_name, pickup_address, delivery_address)

        elif choice == 2:
            system.view_parcels()

        elif choice == 3:
            parcel_id = int(input("Enter parcel ID: "))
            status = input("Enter new status: ")
            system.update_parcel_status(parcel_id, status)

        elif choice == 4:
            parcel_id = int(input("Enter parcel ID: "))
            payment_status = input("Enter payment status: ")
            system.update_payment_status(parcel_id, payment_status)

        elif choice == 5:
            system.close_connection()
            print("Exiting...")
            break

        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    main()
