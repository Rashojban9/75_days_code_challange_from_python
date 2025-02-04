import sqlite3

class Database:
    def __init__(self, db_name="events.db"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute(""
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY,
                name TEXT,
                seats INTEGER
            )
        ""
        )
        self.cursor.execute(""
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY,
                event_id INTEGER,
                name TEXT,
                seat_no INTEGER
            )
        ""
        )
        self.connection.commit()

    def execute(self, query, params=()):
        self.cursor.execute(query, params)
        self.connection.commit()
        return self.cursor

    def fetch_all(self, query, params=()):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def fetch_one(self, query, params=()):
        self.cursor.execute(query, params)
        return self.cursor.fetchone()

    def close(self):
        self.connection.close()


class Event:
    def __init__(self, db):
        self.db = db

    def list_events(self):
        events = self.db.fetch_all("SELECT * FROM events")
        for event in events:
            print(f"{event[0]}. {event[1]} (Seats: {event[2]})")

    def add_event(self, name, seats):
        self.db.execute("INSERT INTO events (name, seats) VALUES (?, ?)", (name, seats))


class Booking:
    def __init__(self, db):
        self.db = db

    def book_ticket(self, event_id, name):
        event = self.db.fetch_one("SELECT seats FROM events WHERE id=?", (event_id,))
        if event and event[0] > 0:
            seat_no = event[0]
            self.db.execute("INSERT INTO bookings (event_id, name, seat_no) VALUES (?, ?, ?)", (event_id, name, seat_no))
            self.db.execute("UPDATE events SET seats = seats - 1 WHERE id = ?", (event_id,))
            print(f"Ticket booked successfully! Seat: {seat_no}")
        else:
            print("No seats available for this event.")

    def cancel_booking(self, booking_id):
        booking = self.db.fetch_one("SELECT event_id, seat_no FROM bookings WHERE id=?", (booking_id,))
        if booking:
            self.db.execute("DELETE FROM bookings WHERE id=?", (booking_id,))
            self.db.execute("UPDATE events SET seats = seats + 1 WHERE id = ?", (booking[0],))
            print(f"Booking canceled. Seat {booking[1]} is now available.")
        else:
            print("Booking ID not found.")


def main():
    db = Database()
    event_manager = Event(db)
    booking_manager = Booking(db)

    while True:
        print("\n1. List Events\n2. Add Event\n3. Book Ticket\n4. Cancel Booking\n5. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            event_manager.list_events()
        elif choice == "2":
            name = input("Enter event name: ")
            seats = int(input("Enter number of seats: "))
            event_manager.add_event(name, seats)
        elif choice == "3":
            event_id = int(input("Enter Event ID: "))
            name = input("Enter Your Name: ")
            booking_manager.book_ticket(event_id, name)
        elif choice == "4":
            booking_id = int(input("Enter Booking ID to cancel: "))
            booking_manager.cancel_booking(booking_id)
        elif choice == "5":
            print("Exiting...")
            db.close()
            break
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()
