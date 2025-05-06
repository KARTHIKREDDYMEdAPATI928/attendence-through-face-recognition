# gui/view_attendance.py

import tkinter as tk
from tkinter import ttk
import mysql.connector
from tkinter import messagebox

def show_attendance_list():
    try:
        # Connect to MySQL
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Bharath@1608",  # Update this if your MySQL has a password
            database="recognition"
        )
        cursor = conn.cursor()

        # Fixed query using CONCAT for full name and joining necessary tables
        query = """
        SELECT a.AttendanceID,
               ad.Date,
               p.StartTime,
               p.EndTime,
               CONCAT(s.FirstName, ' ', s.LastName) AS StudentName,
               a.Status
        FROM attendance a
        LEFT JOIN student s ON a.StudentID = s.StudentID
        LEFT JOIN attendance_date ad ON a.DateID = ad.DateID
        LEFT JOIN period p ON a.PeriodID = p.PeriodID
        ORDER BY ad.Date DESC, p.StartTime
        """
        cursor.execute(query)
        results = cursor.fetchall()

        # Tkinter Window
        window = tk.Toplevel()
        window.title("Attendance Records")
        window.geometry("700x400")

        tk.Label(window, text="Attendance Records", font=("Arial", 16)).pack(pady=10)

        columns = ("AttendanceID", "Date", "StartTime", "EndTime", "StudentName", "Status")
        tree = ttk.Treeview(window, columns=columns, show="headings")

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor=tk.CENTER, width=120 if col not in ("StudentName") else 200)

        for row in results:
            tree.insert("", tk.END, values=(row[0], row[1], row[2], row[3], row[4], row[5]))

        tree.pack(fill=tk.BOTH, expand=True)

        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

if __name__ == '__main__':
    # This block will only run if this script is executed directly
    # It's useful for testing the view attendance window independently
    root = tk.Tk()
    root.title("Test View Attendance")
    test_button = tk.Button(root, text="Show Attendance List", command=show_attendance_list)
    test_button.pack(pady=20)
    root.mainloop()