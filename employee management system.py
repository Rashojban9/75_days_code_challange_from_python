class Employee:
    def __init__(self, emp_id, name, department, salary):
        self.emp_id = emp_id
        self.name = name
        self.department = department
        self.salary = salary
        self.attendance = False

class EmployeeManagementSystem:
    def __init__(self):
        self.employees = {}

    # Add Employee
    def add_employee(self):
        emp_id = int(input("Enter Employee ID: "))
        name = input("Enter Name: ")
        department = input("Enter Department: ")
        salary = float(input("Enter Salary: "))
        
        self.employees[emp_id] = Employee(emp_id, name, department, salary)
        print("Employee added successfully!\n")

    # Display Employees
    def display_employees(self):
        if not self.employees:
            print("No employees to display.\n")
            return

        for emp in self.employees.values():
            print(f"ID: {emp.emp_id}, Name: {emp.name}, Department: {emp.department}, Salary: {emp.salary}, Attendance: {'Present' if emp.attendance else 'Absent'}")
        print()

    # Mark Attendance
    def mark_attendance(self):
        emp_id = int(input("Enter Employee ID to mark attendance: "))
        if emp_id in self.employees:
            self.employees[emp_id].attendance = True
            print("Attendance marked successfully!\n")
        else:
            print("Employee not found.\n")

    # Remove Employee
    def remove_employee(self):
        emp_id = int(input("Enter Employee ID to remove: "))
        if emp_id in self.employees:
            del self.employees[emp_id]
            print("Employee removed successfully!\n")
        else:
            print("Employee not found.\n")

    # Menu
    def menu(self):
        while True:
            print("--- Employee Management System ---")
            print("1. Add Employee")
            print("2. Display Employees")
            print("3. Mark Attendance")
            print("4. Remove Employee")
            print("5. Exit")
            choice = int(input("Choose an option: "))

            if choice == 1:
                self.add_employee()
            elif choice == 2:
                self.display_employees()
            elif choice == 3:
                self.mark_attendance()
            elif choice == 4:
                self.remove_employee()
            elif choice == 5:
                print("Exiting... Goodbye!")
                break
            else:
                print("Invalid option. Please try again.\n")

# Main
if __name__ == "__main__":
    system = EmployeeManagementSystem()
    system.menu()
