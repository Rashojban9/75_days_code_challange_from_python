import sqlite3

class RealEstateManagementSystem:

    def __init__(self):
        self.conn = sqlite3.connect('real_estate.db')
        self.create_tables()

    def create_tables(self):
        properties_table = '''CREATE TABLE IF NOT EXISTS properties (
                                property_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                property_name TEXT,
                                location TEXT,
                                price REAL,
                                status TEXT);'''

        agents_table = '''CREATE TABLE IF NOT EXISTS agents (
                                agent_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT,
                                contact TEXT);'''

        clients_table = '''CREATE TABLE IF NOT EXISTS clients (
                                client_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT,
                                contact TEXT);'''

        bookings_table = '''CREATE TABLE IF NOT EXISTS bookings (
                                booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                property_id INTEGER,
                                client_id INTEGER,
                                agent_id INTEGER,
                                booking_date TEXT,
                                status TEXT,
                                FOREIGN KEY (property_id) REFERENCES properties(property_id),
                                FOREIGN KEY (client_id) REFERENCES clients(client_id),
                                FOREIGN KEY (agent_id) REFERENCES agents(agent_id));'''

        cursor = self.conn.cursor()
        cursor.execute(properties_table)
        cursor.execute(agents_table)
        cursor.execute(clients_table)
        cursor.execute(bookings_table)
        self.conn.commit()

    def add_property(self, name, location, price):
        sql = '''INSERT INTO properties(property_name, location, price, status)
                 VALUES(?, ?, ?, 'Available');'''
        cursor = self.conn.cursor()
        cursor.execute(sql, (name, location, price))
        self.conn.commit()
        print("Property added successfully.")

    def add_agent(self, name, contact):
        sql = '''INSERT INTO agents(name, contact) VALUES(?, ?);'''
        cursor = self.conn.cursor()
        cursor.execute(sql, (name, contact))
        self.conn.commit()
        print("Agent added successfully.")

    def add_client(self, name, contact):
        sql = '''INSERT INTO clients(name, contact) VALUES(?, ?);'''
        cursor = self.conn.cursor()
        cursor.execute(sql, (name, contact))
        self.conn.commit()
        print("Client added successfully.")

    def book_property(self, property_id, client_id, agent_id, booking_date):
        sql = '''INSERT INTO bookings(property_id, client_id, agent_id, booking_date, status)
                 VALUES(?, ?, ?, ?, 'Booked');'''
        cursor = self.conn.cursor()
        cursor.execute(sql, (property_id, client_id, agent_id, booking_date))
        cursor.execute("UPDATE properties SET status = 'Booked' WHERE property_id = ?;", (property_id,))
        self.conn.commit()
        print("Property booked successfully.")

    def view_properties(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM properties;")
        rows = cursor.fetchall()
        for row in rows:
            print(row)

    def close_connection(self):
        self.conn.close()


def main():
    system = RealEstateManagementSystem()

    while True:
        print("1. Add Property\n2. View Properties\n3. Add Agent\n4. Add Client\n5. Book Property\n6. Exit")
        choice = int(input("Choose an option: "))

        if choice == 1:
            name = input("Enter property name: ")
            location = input("Enter location: ")
            price = float(input("Enter price: "))
            system.add_property(name, location, price)

        elif choice == 2:
            system.view_properties()

        elif choice == 3:
            name = input("Enter agent name: ")
            contact = input("Enter contact: ")
            system.add_agent(name, contact)

        elif choice == 4:
            name = input("Enter client name: ")
            contact = input("Enter contact: ")
            system.add_client(name, contact)

        elif choice == 5:
            property_id = int(input("Enter property ID: "))
            client_id = int(input("Enter client ID: "))
            agent_id = int(input("Enter agent ID: "))
            booking_date = input("Enter booking date: ")
            system.book_property(property_id, client_id, agent_id, booking_date)

        elif choice == 6:
            system.close_connection()
            print("Exiting...")
            break

        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    main()
