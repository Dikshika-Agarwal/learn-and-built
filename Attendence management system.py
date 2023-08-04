Attendence management system

USER_FILE = "users.txt"
STUDENTS_FILE = "students.txt"
ATTENDANCE_FILE = "attendance.txt"


user={'Dikshika':'Admin123'}
students={}
attendece_record={}

#Login and authentications

def load_users():
    try:
        with open(USER_FILE, "r") as file:
            for line in file:
                username, password = line.strip().split(":")
                user[username]= password
    except FileNotFoundError:
        # File not found, continue with empty data
        pass

def save_users():
    with open(USER_FILE, "w") as file:
        for username, password in user.items():
            file.write(f"{username}:{password}\n")

def register_user(username,password):
    if username not in user:
        user[username]=password
        return True
    return False

def login_user(username,password):
    if username  in user and user[username]==password:
        return True
    return False


# Manage the students

def load_students():
    try:
        with open(STUDENTS_FILE, "r") as file:
            for line in file:
                student_id, name = line.strip().split(":")
                students[student_id] = name
    except FileNotFoundError:
        # File not found, continue with empty data
        pass

def save_students():
    with open(STUDENTS_FILE, "w") as file:
        for student_id, name in students.items():
            file.write(f"{student_id}:{name}\n")

def add_student(student_id,name):
    if student_id not in students:
        students[student_id]=name
        return True
    return False

def view_student():
    print("Student ID \t Name")
    for student_id, name in students.items():
        print(f"{student_id} \t\t {name}")

def update_student(student_id):
    if student_id in students:
        students[student_id]=name
        return True
    return False

def delete_student(student_id):
    if student_id in students:
        del students[student_id]
        # Also remove associated attendance records
        for date, attendance_list in attendece_record.items():
            attendece_record[date] = [record for record in attendance_list if record['student_id'] != student_id]
        return True
    return False



# mark attendence

def load_attendance():
    try:
        with open(ATTENDANCE_FILE, "r") as file:
            for line in file:
                date, student_id, status = line.strip().split(":")
                if date not in attendece_record:
                    attendece_record[date] = []
                attendece_record[date].append({'student_id': student_id, 'status': status})
    except FileNotFoundError:
        # File not found, continue with empty data
        pass

def save_attendance():
    with open(ATTENDANCE_FILE, "w") as file:
        for date, attendance_list in attendece_record.items():
            for record in attendance_list:
                student_id = record['student_id']
                status = record['status']
                file.write(f"{date}:{student_id}:{status}\n")

def mark_attendance(date, student_ids):
    if date not in attendece_record:
        attendece_record[date] = []

    for student_id in student_ids:
        if student_id in students:
            attendece_record[date].append({'student_id': student_id, 'status': 'Present'})
        else:
            print(f"Student with ID {student_id} does not exist.")

def view_attendance(date):
    if date in attendece_record:
        print(f"Attendance for {date}:")
        for record in attendece_record[date]:
            student_id = record['student_id']
            status = record['status']
            name = students.get(student_id, "Unknown")
            print(f"Student ID: {student_id} \t Name: {name} \t Status: {status}")
    else:
        print("No attendance records for this date.")

def view_student_attendance(student_id):
    print(f"Attendance records for Student ID: {student_id}")
    for date, attendance_list in attendece_record.items():
        for record in attendance_list:
            if record['student_id'] == student_id:
                status = record['status']
                print(f"Date: {date} \t Status: {status}")
                break
        else:
            print(f"No attendance record found for Student ID: {student_id}")

#  Generating Reports
def generate_report():
    print("Attendance Report:")
    print("Date \t\t Present Count")
    for date, attendance_list in attendece_record.items():
        present_count = sum(1 for record in attendance_list if record['status'] == 'Present')
        print(f"{date} \t {present_count}")

# main function
def main():
    load_users()
    load_students()
    load_attendance()

    is_logged_in = False
    while True:
        print("\nAttendance Management System")
        if not is_logged_in:
            print("1. Login")
            
        else:
            print("2. Register User")
            print("3. Add Student")
            print("4. Update Student")
            print("5. Delete Student")
            print("6. Mark Attendance")
            print("7. View Student Attendance")
            print("8. Generate Monthly Report")
            print("9. Generate Weekly Report")
            print("10. Generate Daily Report")
            print("11. Logout")
        
        print("12. Exit")

        choice = int(input("Enter your choice: "))

        if not is_logged_in:
            if choice == 1:
                username = input("Enter username: ")
                password = input("Enter password: ")
                if login_user(username, password):
                    is_logged_in = True  # Set is_logged_in to True on successful login
                    print("Login successful.")
                else:
                    print("Invalid username or password.")
            elif choice == 2:
                username = input("Enter new username: ")
                password = input("Enter password: ")
                if register_user(username, password):
                    print("User registration successful.")
                else:
                    print("Username already exists.")
        else:
            if choice == 3:
                student_id = input("Enter student ID: ")
                name = input("Enter student name: ")
                if add_student(student_id, name):
                    print("Student added successfully.")
                else:
                    print("Student with specified ID already exists.")
            elif choice == 4:
                student_id = input("Enter student ID to update: ")
                name = input("Enter new name: ")
                if update_student(student_id, name):
                    print("Student information updated successfully.")
                else:
                    print("Student with specified ID not found.")
            elif choice == 5:
                student_id = input("Enter student ID to delete: ")
                if delete_student(student_id):
                    print("Student deleted successfully.")
                else:
                    print("Student with specified ID not found.")
            elif choice == 6:
                date = input("Enter date (YYYY-MM-DD): ")
                student_ids = input("Enter comma-separated student IDs: ").split(',')
                mark_attendance(date, student_ids)
            elif choice == 7:
                student_id = input("Enter student ID to view attendance: ")
                view_student_attendance(student_id)
            elif choice == 8:
                generate_report('monthly')
            elif choice == 9:
                generate_report('weekly')
            elif choice == 10:
                generate_report('daily')
            elif choice == 11:
                is_logged_in = False
                print("Logged out successfully.")
            elif choice == 12:
                save_users()
                save_students()
                save_attendance()
                print("Exiting the Attendance Management System.")
                break
            else:
                print("Invalid choice. Please try again.")
    main()