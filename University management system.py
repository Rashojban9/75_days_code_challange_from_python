import sqlite3

# Initialize database
def initialize_db():
    conn = sqlite3.connect("university.db")
    cursor = conn.cursor()

    # Create tables
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        dob TEXT,
        email TEXT,
        phone TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Faculty (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT,
        phone TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_name TEXT NOT NULL,
        faculty_id INTEGER,
        FOREIGN KEY(faculty_id) REFERENCES Faculty(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Grades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        course_id INTEGER,
        grade TEXT,
        FOREIGN KEY(student_id) REFERENCES Students(id),
        FOREIGN KEY(course_id) REFERENCES Courses(id)
    )
    """)
    conn.commit()
    conn.close()

# Add a new student
def add_student():
    name = input("Enter Student Name: ")
    dob = input("Enter Date of Birth (YYYY-MM-DD): ")
    email = input("Enter Email: ")
    phone = input("Enter Phone: ")

    conn = sqlite3.connect("university.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Students (name, dob, email, phone) VALUES (?, ?, ?, ?)", (name, dob, email, phone))
    conn.commit()
    conn.close()
    print("Student added successfully!")

# View all students
def view_students():
    conn = sqlite3.connect("university.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Students")
    students = cursor.fetchall()
    conn.close()

    print("\nStudents:")
    for student in students:
        print(f"ID: {student[0]}, Name: {student[1]}, DOB: {student[2]}, Email: {student[3]}, Phone: {student[4]}")

# Add a new course
def add_course():
    course_name = input("Enter Course Name: ")
    faculty_id = input("Enter Faculty ID (or leave blank): ")

    conn = sqlite3.connect("university.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Courses (course_name, faculty_id) VALUES (?, ?)", (course_name, faculty_id or None))
    conn.commit()
    conn.close()
    print("Course added successfully!")

# View all courses
def view_courses():
    conn = sqlite3.connect("university.db")
    cursor = conn.cursor()
    cursor.execute("""
    SELECT Courses.id, Courses.course_name, Faculty.name
    FROM Courses
    LEFT JOIN Faculty ON Courses.faculty_id = Faculty.id
    """)
    courses = cursor.fetchall()
    conn.close()

    print("\nCourses:")
    for course in courses:
        print(f"ID: {course[0]}, Name: {course[1]}, Faculty: {course[2] or 'Not Assigned'}")

# Add a new faculty member
def add_faculty():
    name = input("Enter Faculty Name: ")
    email = input("Enter Email: ")
    phone = input("Enter Phone: ")

    conn = sqlite3.connect("university.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Faculty (name, email, phone) VALUES (?, ?, ?)", (name, email, phone))
    conn.commit()
    conn.close()
    print("Faculty added successfully!")

# View all faculty members
def view_faculty():
    conn = sqlite3.connect("university.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Faculty")
    faculty = cursor.fetchall()
    conn.close()

    print("\nFaculty:")
    for member in faculty:
        print(f"ID: {member[0]}, Name: {member[1]}, Email: {member[2]}, Phone: {member[3]}")

# Assign a grade to a student
def assign_grade():
    student_id = input("Enter Student ID: ")
    course_id = input("Enter Course ID: ")
    grade = input("Enter Grade: ")

    conn = sqlite3.connect("university.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Grades (student_id, course_id, grade) VALUES (?, ?, ?)", (student_id, course_id, grade))
    conn.commit()
    conn.close()
    print("Grade assigned successfully!")

# View grades
def view_grades():
    conn = sqlite3.connect("university.db")
    cursor = conn.cursor()
    cursor.execute("""
    SELECT Students.name, Courses.course_name, Grades.grade
    FROM Grades
    INNER JOIN Students ON Grades.student_id = Students.id
    INNER JOIN Courses ON Grades.course_id = Courses.id
    """)
    grades = cursor.fetchall()
    conn.close()

    print("\nGrades:")
    for grade in grades:
        print(f"Student: {grade[0]}, Course: {grade[1]}, Grade: {grade[2]}")

# Main menu
def main_menu():
    initialize_db()

    while True:
        print("\nUniversity Management System")
        print("1. Add Student")
        print("2. View Students")
        print("3. Add Faculty")
        print("4. View Faculty")
        print("5. Add Course")
        print("6. View Courses")
        print("7. Assign Grade")
        print("8. View Grades")
        print("9. Exit")

        choice = input("Choose an option: ")
        if choice == "1":
            add_student()
        elif choice == "2":
            view_students()
        elif choice == "3":
            add_faculty()
        elif choice == "4":
            view_faculty()
        elif choice == "5":
            add_course()
        elif choice == "6":
            view_courses()
        elif choice == "7":
            assign_grade()
        elif choice == "8":
            view_grades()
        elif choice == "9":
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# Run the program
if __name__ == "__main__":
    main_menu()
