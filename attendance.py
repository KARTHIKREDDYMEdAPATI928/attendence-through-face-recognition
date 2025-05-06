import tkinter as tk
from db_config import get_connection
from datetime import datetime

def attendance_screen():
    def mark_attendance():
        conn = get_connection()
        cursor = conn.cursor()
        query = "INSERT INTO attendance (AttendanceID, Time) VALUES (%s, %s)"
        attendance_id = entry_attendance_id.get()
        time_now = datetime.now()
        cursor.execute(query, (attendance_id, time_now))
        conn.commit()
        cursor.close()
        conn.close()
        messagebox.showinfo("Success", "Attendance marked successfully.")

    window = tk.Toplevel()
    window.title("Attendance")
    tk.Label(window, text="Attendance ID").pack()
    entry_attendance_id = tk.Entry(window)
    entry_attendance_id.pack()
    tk.Button(window, text="Mark Attendance", command=mark_attendance).pack()
    window.mainloop()
