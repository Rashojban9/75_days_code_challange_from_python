import sqlite3


# Database Manager Class
class DatabaseManager:
    def __init__(self, db_name="course_management.db"):
        self.connection = sqlite3.connect(db_name)
        self.initialize_database()

    def initialize_database(self):
        with self.connection:
            self.connection.execute("""
                CREATE TABLE IF NOT EXISTS Courses (
                    course_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    course_name TEXT NOT NULL,
                    instructor_name TEXT NOT NULL
                )
            """)
            self.connection.execute("""
                CREATE TABLE IF NOT EXISTS Students (
                    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_name TEXT NOT NULL
                )
            """)
            self.connection.execute("""
                CREATE TABLE IF NOT EXISTS CourseAssignments (
                    assignment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    course_id INTEGER NOT NULL,
                    student_id INTEGER NOT NULL,
                    FOREIGN KEY (course_id) REFERENCES Courses(course_id),
                    FOREIGN KEY (student_id) REFERENCES Students(student_id)
                )
            """)

    def execute_query(self, query, params=()):
        with self.connection:
            cursor = self.connection.execute(query, params)
        return cursor

    def fetch_all(self, query, params=()):
        cursor = self.execute_query(query, params)
        return cursor.fetchall()

    def fetch_one(self, query, params=()):
        cursor = self.execute_query(query, params)
        return cursor.fetchone()


# Course Class
class Course:
    def __init__(self, db_manager, course_name, instructor_name, course_id=None):
        self.db_manager = db_manager
        self.course_name = course_name
        self.instructor_name = instructor_name
        self.course_id = course_id

    def save(self):
        if self.course_id is None:
            # Insert new course
            self.db_manager.execute_query(
                "INSERT INTO Courses (course_name, instructor_name) VALUES (?, ?)",
                (self.course_name, self.instructor_name)
            )
            print("Course added successfully.")
        else:
            # Update existing course
            self.db_manager.execute_query(
                "UPDATE Courses SET course_name = ?, instructor_name = ? WHERE course_id = ?",
                (self.course_name, self.instructor_name, self.course_id)
            )
            print("Course updated successfully.")

    def delete(self):
        if self.course_id:
            self.db_manager.execute_query(
                "DELETE FROM Courses WHERE course_id = ?",
                (self.course_id,)
            )
            print("Course deleted successfully.")

    @staticmethod
    def list_all(db_manager):
        courses = db_manager.fetch_all("SELECT * FROM Courses")
        for course in courses:
            print(f"Course ID: {course[0]}, Name: {course[1]}, Instructor: {course[2]}")


# Student Class
class Student:
    def __init__(self, db_manager, student_name, student_id=None):
        self.db_manager = db_manager
        self.student_name = student_name
        self.student_id = student_id

    def save(self):
        if self.student_id is None:
            # Insert new student
            self.db_manager.execute_query(
                "INSERT INTO Students (student_name) VALUES (?)",
                (self.student_name,)
            )
            print("Student added successfully.")

    @staticmethod
    def list_all(db_manager):
        students = db_manager.fetch_all("SELECT * FROM Students")
        for student in students:
            print(f"Student ID: {student[0]}, Name: {student[1]}")


# Course Assignment Class
class CourseAssignment:
    def __init__(self, db_manager, course_id, student_id):
        self.db_manager = db_manager
        self.course_id = course_id
        self.student_id = student_id

    def assign(self):
        self.db_manager.execute_query(
            "INSERT INTO CourseAssignments (course_id, student_id) VALUES (?, ?)",
            (self.course_id, self.student_id)
        )
        print("Student assigned to course successfully.")

    @staticmethod
    def list_students_in_course(db_manager, course_id):
        students = db_manager.fetch_all("""
            SELECT s.student_id, s.student_name FROM Students s
            JOIN CourseAssignments ca ON s.student_id = ca.student_id
            WHERE ca.course_id = ?
        """, (course_id,))
        print(f"Students in Course ID {course_id}:")
        for student in students:
            print(f"Student ID: {student[0]}, Name: {student[1]}")


# Main Application Class
class CourseManagementSystem:
    def __init__(self):
        self.db_manager = DatabaseManager()

    def run(self):
        while True:
            print("\nCourse Management System")
            print("1. Add Course")
            print("2. Update Course")
            print("3. Delete Course")
            print("4. List Courses")
            print("5. Add Student")
            print("6. List Students")
            print("7. Assign Student to Course")
            print("8. List Students in Course")
            print("9. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                course_name = input("Enter course name: ")
                instructor_name = input("Enter instructor name: ")
                course = Course(self.db_manager, course_name, instructor_name)
                course.save()
            elif choice == "2":
                course_id = int(input("Enter course ID to update: "))
                course_name = input("Enter new course name: ")
                instructor_name = input("Enter new instructor name: ")
                course = Course(self.db_manager, course_name, instructor_name, course_id)
                course.save()
            elif choice == "3":
                course_id = int(input("Enter course ID to delete: "))
                course = Course(self.db_manager, None, None, course_id)
                course.delete()
            elif choice == "4":
                Course.list_all(self.db_manager)
            elif choice == "5":
                student_name = input("Enter student name: ")
                student = Student(self.db_manager, student_name)
                student.save()
            elif choice == "6":
                Student.list_all(self.db_manager)
            elif choice == "7":
                course_id = int(input("Enter course ID: "))
                student_id = int(input("Enter student ID: "))
                assignment = CourseAssignment(self.db_manager, course_id, student_id)
                assignment.assign()
            elif choice == "8":
                course_id = int(input("Enter course ID to view students: "))
                CourseAssignment.list_students_in_course(self.db_manager, course_id)
            elif choice == "9":
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please try again.")


# Run the Application
if __name__ == "__main__":
    system = CourseManagementSystem()
    system.run()
