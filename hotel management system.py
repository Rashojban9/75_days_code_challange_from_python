import sqlite3
from datetime import datetime


# Connect to SQLite database
def connect():
    return sqlite3.connect("hotel.db")


# Create necessary tables
def create_tables():
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Rooms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                room_number TEXT UNIQUE,
                room_type TEXT,
                price_per_night REAL,
                availability TEXT DEFAULT 'Available'
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Guests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                contact TEXT,
                room_id INTEGER,
                check_in_date TEXT,
                check_out_date TEXT,
                total_bill REAL,
                FOREIGN KEY (room_id) REFERENCES Rooms (id)
            )
        """)
        conn.commit()


# Add a new room
def add_room(room_number, room_type, price_per_night):
    with connect() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO Rooms (room_number, room_type, price_per_night)
                VALUES (?, ?, ?)
            """, (room_number, room_type, price_per_night))
            conn.commit()
            print("Room added successfully!")
        except sqlite3.IntegrityError:
            print("Room number already exists!")


# Book a room
def book_room(name, contact, room_id, check_in_date, check_out_date):
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT availability, price_per_night FROM Rooms WHERE id = ?", (room_id,))
        room = cursor.fetchone()
        if room and room[0] == "Available":
            price_per_night = room[1]

            # Calculate total bill based on stay duration
            days_stayed = (datetime.strptime(check_out_date, "%Y-%m-%d") - datetime.strptime(check_in_date, "%Y-%m-%d")).days
            total_bill = days_stayed * price_per_night

            # Update room status and add guest details
            cursor.execute("UPDATE Rooms SET availability = 'Occupied' WHERE id = ?", (room_id,))
            cursor.execute("""
                INSERT INTO Guests (name, contact, room_id, check_in_date, check_out_date, total_bill)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (name, contact, room_id, check_in_date, check_out_date, total_bill))
            conn.commit()
            print(f"Room booked successfully! Total Bill: ${total_bill:.2f}")
        else:
            print("Room is not available!")


# List available rooms
def list_available_rooms():
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Rooms WHERE availability = 'Available'")
        rooms = cursor.fetchall()
        if rooms:
            print("\nAvailable Rooms:")
            print(f"{'ID':<5} {'Room Number':<15} {'Room Type':<15} {'Price/Night':<10}")
            for room in rooms:
                print(f"{room[0]:<5} {room[1]:<15} {room[2]:<15} ${room[3]:<10.2f}")
        else:
            print("No available rooms!")


# Main menu
def main():
    create_tables()
    while True:
        print("\nHotel Management System")
        print("1. Add Room")
        print("2. Book Room")
        print("3. List Available Rooms")
        print("4. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            room_number = input("Enter Room Number: ")
            room_type = input("Enter Room Type: ")
            price_per_night = float(input("Enter Price per Night: "))
            add_room(room_number, room_type, price_per_night)
        elif choice == "2":
            name = input("Enter Guest Name: ")
            contact = input("Enter Guest Contact: ")
            room_id = int(input("Enter Room ID to Book: "))
            check_in_date = input("Enter Check-In Date (YYYY-MM-DD): ")
            check_out_date = input("Enter Check-Out Date (YYYY-MM-DD): ")
            book_room(name, contact, room_id, check_in_date, check_out_date)
        elif choice == "3":
            list_available_rooms()
        elif choice == "4":
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
