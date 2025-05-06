import tkinter as tk
from tkinter import ttk
import mysql.connector

def show_notifications():
    # Create a new window
    win = tk.Tk()
    win.title("Attendance Notifications")
    win.geometry("700x400")
    win.config(bg="white")

    # Title label
    title = tk.Label(win, text="Notifications", font=("Helvetica", 20, "bold"), bg="white", fg="#333")
    title.pack(pady=10)

    # Treeview widget to display notifications
    tree = ttk.Treeview(win, columns=("ID", "StudentID", "Message", "Timestamp"), show="headings")
    tree.heading("ID", text="Notification ID")
    tree.heading("StudentID", text="Student ID")
    tree.heading("Message", text="Message")
    tree.heading("Timestamp", text="Timestamp")

    # Set column width
    tree.column("ID", width=100)
    tree.column("StudentID", width=100)
    tree.column("Message", width=300)
    tree.column("Timestamp", width=180)

    # Add vertical scrollbar
    scrollbar = ttk.Scrollbar(win, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    tree.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

    # Connect to MySQL and fetch data
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Bharath@1608',
            database='recognition'
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM notifications ORDER BY Timestamp DESC")
        rows = cursor.fetchall()

        for row in rows:
            tree.insert("", tk.END, values=row)

        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        error_label = tk.Label(win, text=f"Database Error: {err}", fg="red", bg="white")
        error_label.pack(pady=10)

    win.mainloop()

# Run the GUI window
show_notifications()
