import sqlite3


class DatabaseManager:
    """Manages the SQLite database connection and initialization."""
    def __init__(self, db_name="grading_system.db"):
        self.connection = sqlite3.connect(db_name)
        self.initialize_database()

    def initialize_database(self):
        """Initialize tables for students and grades."""
        create_students_table = """
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        );
        """
        create_grades_table = """
        CREATE TABLE IF NOT EXISTS grades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            course TEXT NOT NULL,
            grade TEXT NOT NULL,
            FOREIGN KEY (student_id) REFERENCES students (id)
        );
        """
        cursor = self.connection.cursor()
        cursor.execute(create_students_table)
        cursor.execute(create_grades_table)
        self.connection.commit()

    def execute_query(self, query, params=()):
        """Executes a query with optional parameters."""
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        self.connection.commit()
        return cursor

    def close(self):
        """Closes the database connection."""
        self.connection.close()


class Student:
    """Represents a student entity."""
    def __init__(self, name):
        self.name = name


class Grade:
    """Represents a grade entity."""
    def __init__(self, student_id, course, grade):
        self.student_id = student_id
        self.course = course
        self.grade = grade


class GradingSystem:
    """Main system for managing students, grades, and reports."""
    def __init__(self):
        self.db_manager = DatabaseManager()

    def add_student(self):
        """Add a new student to the system."""
        name = input("Enter student name: ")
        query = "INSERT INTO students (name) VALUES (?);"
        self.db_manager.execute_query(query, (name,))
        print(f"Student '{name}' added successfully!")

    def assign_grade(self):
        """Assign or update a grade for a student."""
        student_id = int(input("Enter student ID: "))
        course = input("Enter course: ")
        grade = input("Enter grade: ")
        check_query = "SELECT * FROM grades WHERE student_id = ? AND course = ?;"
        cursor = self.db_manager.execute_query(check_query, (student_id, course))

        if cursor.fetchone():
            # Update existing grade
            update_query = "UPDATE grades SET grade = ? WHERE student_id = ? AND course = ?;"
            self.db_manager.execute_query(update_query, (grade, student_id, course))
            print(f"Grade updated to '{grade}' for student ID {student_id} in course '{course}'.")
        else:
            # Insert new grade
            insert_query = "INSERT INTO grades (student_id, course, grade) VALUES (?, ?, ?);"
            self.db_manager.execute_query(insert_query, (student_id, course, grade))
            print(f"Grade '{grade}' assigned to student ID {student_id} for course '{course}'.")

    def display_report(self):
        """Display the report for a specific student."""
        student_id = int(input("Enter student ID: "))
        query = """
        SELECT s.name, g.course, g.grade
        FROM students s
        JOIN grades g ON s.id = g.student_id
        WHERE s.id = ?;
        """
        cursor = self.db_manager.execute_query(query, (student_id,))
        results = cursor.fetchall()

        if results:
            print(f"\nReport for Student ID {student_id}:")
            for row in results:
                print(f"Name: {row[0]}, Course: {row[1]}, Grade: {row[2]}")
        else:
            print(f"No records found for Student ID {student_id}.")

    def run(self):
        """Main menu loop."""
        while True:
            print("\n=== Grading System ===")
            print("1. Add Student")
            print("2. Assign/Update Grade")
            print("3. Display Report")
            print("4. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.add_student()
            elif choice == "2":
                self.assign_grade()
            elif choice == "3":
                self.display_report()
            elif choice == "4":
                self.db_manager.close()
                print("Goodbye!")
                break
            else:
                print("Invalid choice! Please try again.")


if __name__ == "__main__":
    system = GradingSystem()
    system.run()
