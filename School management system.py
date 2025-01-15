import sqlite3

# Database connection
def connect():
    return sqlite3.connect("school.db")

# Create tables
def create_tables():
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                grade TEXT,
                attendance INTEGER DEFAULT 0
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Teachers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                subject TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Classes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                class_name TEXT,
                teacher_id INTEGER,
                FOREIGN KEY(teacher_id) REFERENCES Teachers(id)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Exams (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER,
                subject TEXT,
                grade TEXT,
                FOREIGN KEY(student_id) REFERENCES Students(id)
            )
        """)
        conn.commit()

# Add student
def add_student(name, grade):
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Students (name, grade) VALUES (?, ?)", (name, grade))
        conn.commit()
        print("Student added successfully!")

# Add teacher
def add_teacher(name, subject):
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Teachers (name, subject) VALUES (?, ?)", (name, subject))
        conn.commit()
        print("Teacher added successfully!")

# Assign class
def assign_class(class_name, teacher_id):
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Classes (class_name, teacher_id) VALUES (?, ?)", (class_name, teacher_id))
        conn.commit()
        print("Class assigned successfully!")

# Add exam grade
def add_exam_grade(student_id, subject, grade):
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Exams (student_id, subject, grade) VALUES (?, ?, ?)", (student_id, subject, grade))
        conn.commit()
        print("Exam grade added successfully!")

# Generate report card
def generate_report_card(student_id):
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT subject, grade FROM Exams WHERE student_id = ?", (student_id,))
        rows = cursor.fetchall()
        if rows:
            print("Report Card:")
            for row in rows:
                print(f"Subject: {row[0]}, Grade: {row[1]}")
        else:
            print("No grades found for the student.")

# Main menu
def main_menu():
    create_tables()
    while True:
        print("\nSchool Management System")
        print("1. Add Student")
        print("2. Add Teacher")
        print("3. Assign Class")
        print("4. Add Exam Grade")
        print("5. Generate Report Card")
        print("6. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            name = input("Enter Student Name: ")
            grade = input("Enter Grade: ")
            add_student(name, grade)
        elif choice == "2":
            name = input("Enter Teacher Name: ")
            subject = input("Enter Subject: ")
            add_teacher(name, subject)
        elif choice == "3":
            class_name = input("Enter Class Name: ")
            teacher_id = int(input("Enter Teacher ID: "))
            assign_class(class_name, teacher_id)
        elif choice == "4":
            student_id = int(input("Enter Student ID: "))
            subject = input("Enter Subject: ")
            grade = input("Enter Grade: ")
            add_exam_grade(student_id, subject, grade)
        elif choice == "5":
            student_id = int(input("Enter Student ID: "))
            generate_report_card(student_id)
        elif choice == "6":
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main_menu()
