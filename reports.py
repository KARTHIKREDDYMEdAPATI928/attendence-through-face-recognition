import tkinter as tk
import mysql.connector

def show_reports():
    reports_window = tk.Toplevel()
    reports_window.title("Attendance Reports")
    reports_window.geometry("600x600")

    # Heading
    heading_label = tk.Label(reports_window, text="Attendance Reports", font=("Arial", 16))
    heading_label.pack(pady=10)

    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Bharath@1608",  # Add your password if set
            database="recognition"
        )
        cursor = conn.cursor()

        # Total attendance records per student
        cursor.execute("SELECT StudentID, COUNT(*) FROM attendance GROUP BY StudentID")
        total_attendance = dict(cursor.fetchall())

        # Present attendance records per student
        cursor.execute("SELECT StudentID, COUNT(*) FROM attendance WHERE Status = 'Present' GROUP BY StudentID")
        present_attendance = dict(cursor.fetchall())

        results_above = []
        results_below = []

        for student_id in total_attendance:
            total = total_attendance[student_id]
            present = present_attendance.get(student_id, 0)
            percentage = (present / total) * 100

            cursor.execute("SELECT FirstName, LastName FROM student WHERE StudentID = %s", (student_id,))
            name = cursor.fetchone()
            full_name = f"{name[0]} {name[1]}" if name else "Unknown"

            entry = f"{full_name} - {percentage:.2f}% attendance"

            if percentage >= 75:
                results_above.append(entry)
            else:
                results_below.append(entry)

        # Above 75%
        tk.Label(reports_window, text="Students with ≥ 75% Attendance", font=("Arial", 12, "bold"), fg="green").pack(pady=5)
        for student in results_above:
            tk.Label(reports_window, text=student).pack()

        # Below 75%
        tk.Label(reports_window, text="Students with < 75% Attendance", font=("Arial", 12, "bold"), fg="red").pack(pady=10)
        for student in results_below:
            tk.Label(reports_window, text=student).pack()

        conn.close()

    except Exception as e:
        tk.Label(reports_window, text=f"Error: {e}", fg="red").pack()
