class Student:
    def __init__(self, student_id, name, age, grade):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.grade = grade
        self.attendance = False


class StudentManagementSystem:
    def __init__(self):
        self.students = {}

    # Add Student
    def add_student(self):
        student_id = int(input("Enter Student ID: "))
        name = input("Enter Name: ")
        age = int(input("Enter Age: "))
        grade = float(input("Enter Grade: "))

        self.students[student_id] = Student(student_id, name, age, grade)
        print("Student added successfully!\n")

    # Display Students
    def display_students(self):
        if not self.students:
            print("No students to display.\n")
            return

        for student in self.students.values():
            print(f"ID: {student.student_id}, Name: {student.name}, Age: {student.age}, Grade: {student.grade}, Attendance: {'Present' if student.attendance else 'Absent'}")
        print()

    # Mark Attendance
    def mark_attendance(self):
        student_id = int(input("Enter Student ID to mark attendance: "))
        if student_id in self.students:
            self.students[student_id].attendance = True
            print("Attendance marked successfully!\n")
        else:
            print("Student not found.\n")

    # Remove Student
    def remove_student(self):
        student_id = int(input("Enter Student ID to remove: "))
        if student_id in self.students:
            del self.students[student_id]
            print("Student removed successfully!\n")
        else:
            print("Student not found.\n")

    # Menu
    def menu(self):
        while True:
            print("--- Student Management System ---")
            print("1. Add Student")
            print("2. Display Students")
            print("3. Mark Attendance")
            print("4. Remove Student")
            print("5. Exit")
            choice = int(input("Choose an option: "))

            if choice == 1:
                self.add_student()
            elif choice == 2:
                self.display_students()
            elif choice == 3:
                self.mark_attendance()
            elif choice == 4:
                self.remove_student()
            elif choice == 5:
                print("Exiting... Goodbye!")
                break
            else:
                print("Invalid option. Please try again.\n")


# Main
if __name__ == "__main__":
    system = StudentManagementSystem()
    system.menu()
