import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('hospital.db')
c = conn.cursor()

# Create tables
c.execute('''CREATE TABLE IF NOT EXISTS Patients (
                id INTEGER PRIMARY KEY,
                name TEXT,
                age INTEGER,
                disease TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS Appointments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER,
                doctor_name TEXT,
                date TEXT,
                FOREIGN KEY(patient_id) REFERENCES Patients(id))''')

# Add a new patient
def add_patient():
    id = int(input("Enter Patient ID: "))
    name = input("Enter Name: ")
    age = int(input("Enter Age: "))
    disease = input("Enter Disease: ")
    c.execute("INSERT INTO Patients VALUES (?, ?, ?, ?)", (id, name, age, disease))
    conn.commit()
    print("Patient added successfully!")

# View all patients
def view_patients():
    c.execute("SELECT * FROM Patients")
    patients = c.fetchall()
    for patient in patients:
        print(patient)

# Schedule an appointment
def add_appointment():
    patient_id = int(input("Enter Patient ID: "))
    doctor_name = input("Enter Doctor Name: ")
    date = input("Enter Date (YYYY-MM-DD): ")
    c.execute("INSERT INTO Appointments (patient_id, doctor_name, date) VALUES (?, ?, ?)", (patient_id, doctor_name, date))
    conn.commit()
    print("Appointment scheduled successfully!")

# View all appointments
def view_appointments():
    c.execute("SELECT * FROM Appointments")
    appointments = c.fetchall()
    for appointment in appointments:
        print(appointment)

# Main menu
def main():
    while True:
        print("\nHospital Management System")
        print("1. Add Patient")
        print("2. View Patients")
        print("3. Add Appointment")
        print("4. View Appointments")
        print("5. Exit")
        choice = int(input("Choose an option: "))

        if choice == 1:
            add_patient()
        elif choice == 2:
            view_patients()
        elif choice == 3:
            add_appointment()
        elif choice == 4:
            view_appointments()
        elif choice == 5:
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == '__main__':
    main()

conn.close()
