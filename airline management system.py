import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('airline.db')
c = conn.cursor()

# Create tables
c.execute('''CREATE TABLE IF NOT EXISTS Flights (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                flight_number TEXT,
                origin TEXT,
                destination TEXT,
                departure_time TEXT,
                arrival_time TEXT,
                seats_available INTEGER
            )''')

c.execute('''CREATE TABLE IF NOT EXISTS Customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                contact TEXT
            )''')

c.execute('''CREATE TABLE IF NOT EXISTS Reservations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER,
                flight_id INTEGER,
                seat_number TEXT,
                status TEXT,
                FOREIGN KEY(customer_id) REFERENCES Customers(id),
                FOREIGN KEY(flight_id) REFERENCES Flights(id)
            )''')

conn.commit()

# Add flight
def add_flight(flight_number, origin, destination, departure_time, arrival_time, seats_available):
    c.execute("INSERT INTO Flights (flight_number, origin, destination, departure_time, arrival_time, seats_available) VALUES (?, ?, ?, ?, ?, ?)",
              (flight_number, origin, destination, departure_time, arrival_time, seats_available))
    conn.commit()
    print("Flight added successfully!")

# Book ticket
def book_ticket(customer_name, contact, flight_id, seat_number):
    # Add customer
    c.execute("INSERT INTO Customers (name, contact) VALUES (?, ?)", (customer_name, contact))
    customer_id = c.lastrowid

    # Check seat availability
    c.execute("SELECT seats_available FROM Flights WHERE id = ?", (flight_id,))
    seats_available = c.fetchone()[0]

    if seats_available > 0:
        # Book reservation
        c.execute("INSERT INTO Reservations (customer_id, flight_id, seat_number, status) VALUES (?, ?, ?, 'Booked')",
                  (customer_id, flight_id, seat_number))
        c.execute("UPDATE Flights SET seats_available = seats_available - 1 WHERE id = ?", (flight_id,))
        conn.commit()
        print("Ticket booked successfully!")
    else:
        print("No seats available!")

# Cancel reservation
def cancel_reservation(reservation_id):
    c.execute("SELECT flight_id FROM Reservations WHERE id = ?", (reservation_id,))
    flight_id = c.fetchone()[0]

    c.execute("DELETE FROM Reservations WHERE id = ?", (reservation_id,))
    c.execute("UPDATE Flights SET seats_available = seats_available + 1 WHERE id = ?", (flight_id,))
    conn.commit()
    print("Reservation canceled successfully!")

# Generate boarding pass
def generate_boarding_pass(reservation_id):
    c.execute('''SELECT r.id, c.name, f.flight_number, f.origin, f.destination, f.departure_time, f.arrival_time, r.seat_number 
                 FROM Reservations r
                 JOIN Customers c ON r.customer_id = c.id
                 JOIN Flights f ON r.flight_id = f.id
                 WHERE r.id = ?''', (reservation_id,))
    reservation = c.fetchone()

    if reservation:
        print("\nBOARDING PASS")
        print(f"Reservation ID: {reservation[0]}")
        print(f"Passenger: {reservation[1]}")
        print(f"Flight: {reservation[2]}")
        print(f"From: {reservation[3]} To: {reservation[4]}")
        print(f"Departure: {reservation[5]} Arrival: {reservation[6]}")
        print(f"Seat: {reservation[7]}")
    else:
        print("Reservation not found!")

# Main menu
def main():
    while True:
        print("\nAirline Reservation System")
        print("1. Add Flight")
        print("2. Book Ticket")
        print("3. Cancel Reservation")
        print("4. Generate Boarding Pass")
        print("5. Exit")
        choice = int(input("Choose an option: "))

        if choice == 1:
            flight_number = input("Enter Flight Number: ")
            origin = input("Enter Origin: ")
            destination = input("Enter Destination: ")
            departure_time = input("Enter Departure Time: ")
            arrival_time = input("Enter Arrival Time: ")
            seats_available = int(input("Enter Seats Available: "))
            add_flight(flight_number, origin, destination, departure_time, arrival_time, seats_available)
        elif choice == 2:
            customer_name = input("Enter Customer Name: ")
            contact = input("Enter Contact: ")
            flight_id = int(input("Enter Flight ID: "))
            seat_number = input("Enter Seat Number: ")
            book_ticket(customer_name, contact, flight_id, seat_number)
        elif choice == 3:
            reservation_id = int(input("Enter Reservation ID: "))
            cancel_reservation(reservation_id)
        elif choice == 4:
            reservation_id = int(input("Enter Reservation ID: "))
            generate_boarding_pass(reservation_id)
        elif choice == 5:
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

    conn.close()

if __name__ == "__main__":
    main()
