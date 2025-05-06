# attendance-management-system-using-facial-recognition

This project is a Student Management System that incorporates face recognition for attendance tracking and student identification. It provides a graphical user interface (GUI) built with Tkinter for easy interaction.

## Features

* **Student Management:**
    * Add new student records (ID, Name, DOB, Contact, Class, Gender, Email).
    * View a list of all registered students.
    * (Potentially) Edit and delete student records (implementation may vary).
* **Attendance Tracking:**
    * Capture student faces using a webcam.
    * Train a face recognition model based on captured images.
    * View attendance records, showing date, time, student name, and status.
* **User Authentication:**
    * Secure login for administrators and students.
    * Role-based access control (admin and student dashboards).
* **Reporting (Potentially):**
    * Generate and view reports (PDF format).
* **Queries:**
    * Provides a menu to view common SQL queries for student management, attendance tracking, and authentication.

## Prerequisites

Before running the application, ensure you have the following installed:

* **Python 3.x:** Download from [https://www.python.org/downloads/](https://www.python.org/downloads/)
* **Required Python Libraries:** Install them using pip:
    ```bash
    pip install tkinter pillow opencv-python mysql-connector-python
    ```
    * `tkinter`: For the graphical user interface (usually comes with Python).
    * `pillow`: For image manipulation.
    * `opencv-python`: For face detection and image processing.
    * `mysql-connector-python`: For connecting to the MySQL database.
* **MySQL Database:** You need a running MySQL server and a database set up for the application. Update the database connection details in `db_config.py`.

## Setup

1.  **Clone the Repository:**
    ```bash
    git clone [repository URL]
    cd [repository directory]
    ```
2.  **Database Configuration:**
    * Open the `db_config.py` file.
    * Modify the `db_config` dictionary with your MySQL server details (host, user, password, database name).
    ```python
    db_config = {
        'host': 'your_host',
        'user': 'your_user',
        'password': 'your_password',
        'database': 'your_database'
    }
    ```
3.  **Database Schema (Example - You might need to create your own):**
    You'll need to create tables in your MySQL database to store student information, attendance, authentication details, etc. Here's a basic example of the `student` and `authentication_service` tables:

    ```sql
    -- Example student table
    CREATE TABLE student (
        StudentID VARCHAR(20) PRIMARY KEY,
        FirstName VARCHAR(50) NOT NULL,
        LastName VARCHAR(50),
        DOB DATE,
        Email VARCHAR(100),
        ContactNo VARCHAR(20),
        class VARCHAR(10),
        Gender VARCHAR(10)
    );

    -- Example authentication_service table
    CREATE TABLE authentication_service (
        username VARCHAR(50) PRIMARY KEY,
        password VARCHAR(255) NOT NULL,
        StudentID VARCHAR(20),
        role VARCHAR(10) NOT NULL, -- 'admin' or 'student'
        FOREIGN KEY (StudentID) REFERENCES student(StudentID)
    );

    -- Example attendance_date table
    CREATE TABLE attendance_date (
        DateID INT AUTO_INCREMENT PRIMARY KEY,
        Date DATE UNIQUE
    );

    -- Example period table
    CREATE TABLE period (
        PeriodID INT AUTO_INCREMENT PRIMARY KEY,
        StartTime TIME NOT NULL,
        EndTime TIME NOT NULL
    );

    -- Example attendance table
    CREATE TABLE attendance (
        AttendanceID INT AUTO_INCREMENT PRIMARY KEY,
        StudentID VARCHAR(20) NOT NULL,
        DateID INT NOT NULL,
        PeriodID INT NOT NULL,
        Status VARCHAR(20), -- e.g., 'Present', 'Absent', 'Late'
        FOREIGN KEY (StudentID) REFERENCES student(StudentID),
        FOREIGN KEY (DateID) REFERENCES attendance_date(DateID),
        FOREIGN KEY (PeriodID) REFERENCES period(PeriodID),
        UNIQUE KEY unique_attendance (StudentID, DateID, PeriodID)
    );

    -- Example attendance_log table (for tracking time)
    CREATE TABLE attendance_log (
        LogID INT AUTO_INCREMENT PRIMARY KEY,
        StudentID VARCHAR(20) NOT NULL,
        DateID INT NOT NULL,
        PeriodID INT NOT NULL,
        LoginTime DATETIME,
        LogoutTime DATETIME,
        FOREIGN KEY (StudentID) REFERENCES student(StudentID),
        FOREIGN KEY (DateID) REFERENCES attendance_date(DateID),
        FOREIGN KEY (PeriodID) REFERENCES period(PeriodID)
    );
    ```

    Adjust the schema based on your specific requirements.

## Running the Application

1.  Navigate to the project directory in your terminal.
2.  Run the `main.py` file:
    ```bash
    python main.py
    ```
    This will start the login screen of the application.

## Project Structure

## Contributing

Contributions to this project are welcome. Feel free to fork the repository and submit pull requests with improvements or bug fixes. Please follow standard coding practices and provide clear descriptions of your changes.

## License

[Specify your license here, e.g., MIT License]

## Acknowledgements

* Tkinter for the GUI framework.
* OpenCV for face recognition functionalities.
* Pillow for image handling.
* MySQL Connector for database interaction.
* (Mention any other libraries or resources you used)

## Further Development

* Implement editing and deleting of student records.
* Enhance the face recognition accuracy and speed.
* Add more detailed attendance reporting features.
* Implement user role management more comprehensively.
* Improve the overall user interface and user experience.

Markdown

# Student Management System with Face Recognition

This project is a Student Management System that incorporates face recognition for attendance tracking and student identification. It provides a graphical user interface (GUI) built with Tkinter for easy interaction.

## Features

* **Student Management:**
    * Add new student records (ID, Name, DOB, Contact, Class, Gender, Email).
    * View a list of all registered students.
    * (Potentially) Edit and delete student records (implementation may vary).
* **Attendance Tracking:**
    * Capture student faces using a webcam.
    * Train a face recognition model based on captured images.
    * View attendance records, showing date, time, student name, and status.
* **User Authentication:**
    * Secure login for administrators and students.
    * Role-based access control (admin and student dashboards).
* **Reporting (Potentially):**
    * Generate and view reports (PDF format).
* **Queries:**
    * Provides a menu to view common SQL queries for student management, attendance tracking, and authentication.

## Prerequisites

Before running the application, ensure you have the following installed:

* **Python 3.x:** Download from [https://www.python.org/downloads/](https://www.python.org/downloads/)
* **Required Python Libraries:** Install them using pip:
    ```bash
    pip install tkinter pillow opencv-python mysql-connector-python
    ```
    * `tkinter`: For the graphical user interface (usually comes with Python).
    * `pillow`: For image manipulation.
    * `opencv-python`: For face detection and image processing.
    * `mysql-connector-python`: For connecting to the MySQL database.
* **MySQL Database:** You need a running MySQL server and a database set up for the application. Update the database connection details in `db_config.py`.

## Setup

1.  **Clone the Repository:**
    ```bash
    git clone [repository URL]
    cd [repository directory]
    ```
2.  **Database Configuration:**
    * Open the `db_config.py` file.
    * Modify the `db_config` dictionary with your MySQL server details (host, user, password, database name).
    ```python
    db_config = {
        'host': 'your_host',
        'user': 'your_user',
        'password': 'your_password',
        'database': 'your_database'
    }
    ```
3.  **Database Schema (Example - You might need to create your own):**
    You'll need to create tables in your MySQL database to store student information, attendance, authentication details, etc. Here's a basic example of the `student` and `authentication_service` tables:

    ```sql
    -- Example student table
    CREATE TABLE student (
        StudentID VARCHAR(20) PRIMARY KEY,
        FirstName VARCHAR(50) NOT NULL,
        LastName VARCHAR(50),
        DOB DATE,
        Email VARCHAR(100),
        ContactNo VARCHAR(20),
        class VARCHAR(10),
        Gender VARCHAR(10)
    );

    -- Example authentication_service table
    CREATE TABLE authentication_service (
        username VARCHAR(50) PRIMARY KEY,
        password VARCHAR(255) NOT NULL,
        StudentID VARCHAR(20),
        role VARCHAR(10) NOT NULL, -- 'admin' or 'student'
        FOREIGN KEY (StudentID) REFERENCES student(StudentID)
    );

    -- Example attendance_date table
    CREATE TABLE attendance_date (
        DateID INT AUTO_INCREMENT PRIMARY KEY,
        Date DATE UNIQUE
    );

    -- Example period table
    CREATE TABLE period (
        PeriodID INT AUTO_INCREMENT PRIMARY KEY,
        StartTime TIME NOT NULL,
        EndTime TIME NOT NULL
    );

    -- Example attendance table
    CREATE TABLE attendance (
        AttendanceID INT AUTO_INCREMENT PRIMARY KEY,
        StudentID VARCHAR(20) NOT NULL,
        DateID INT NOT NULL,
        PeriodID INT NOT NULL,
        Status VARCHAR(20), -- e.g., 'Present', 'Absent', 'Late'
        FOREIGN KEY (StudentID) REFERENCES student(StudentID),
        FOREIGN KEY (DateID) REFERENCES attendance_date(DateID),
        FOREIGN KEY (PeriodID) REFERENCES period(PeriodID),
        UNIQUE KEY unique_attendance (StudentID, DateID, PeriodID)
    );

    -- Example attendance_log table (for tracking time)
    CREATE TABLE attendance_log (
        LogID INT AUTO_INCREMENT PRIMARY KEY,
        StudentID VARCHAR(20) NOT NULL,
        DateID INT NOT NULL,
        PeriodID INT NOT NULL,
        LoginTime DATETIME,
        LogoutTime DATETIME,
        FOREIGN KEY (StudentID) REFERENCES student(StudentID),
        FOREIGN KEY (DateID) REFERENCES attendance_date(DateID),
        FOREIGN KEY (PeriodID) REFERENCES period(PeriodID)
    );
    ```

    Adjust the schema based on your specific requirements.

## Running the Application

1.  Navigate to the project directory in your terminal.
2.  Run the `main.py` file:
    ```bash
    python main.py
    ```
    This will start the login screen of the application.

## Project Structure

├── gui/
│   ├── admin_dashboard.py     # Admin dashboard interface
│   ├── login.py             # Login screen interface and logic
│   ├── student_dashboard.py   # Student dashboard interface
│   ├── student_register.py    # Interface for adding new students
│   ├── view_attendance.py     # Interface for viewing attendance
│   ├── view_students.py       # Interface for viewing student list
│   └── ... (other GUI files)
├── face_capture.py        # Script for capturing student faces
├── face_trainer.py        # Script for training the face recognition model
├── attendance_checker.py  # (Potentially) Script for real-time attendance checking
├── db_config.py           # Database connection configuration
├── main.py                # Main entry point of the application
├── README.md              # This file
└── ... (other files)
