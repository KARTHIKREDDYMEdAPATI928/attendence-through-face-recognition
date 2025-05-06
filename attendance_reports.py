import tkinter as tk
from gui.view_students import show_student_list
from gui.student_register import show_student_register_form
from gui.view_attendance import show_attendance_list
from gui.reports import show_reports

def show_admin_dashboard(role=None):
    window = tk.Tk()
    window.title("Admin Dashboard")
    window.geometry("400x400")

    tk.Label(window, text="Welcome, Admin!", font=("Arial", 16)).pack(pady=20)

    # Add Student Button
    tk.Button(window, text="Add Student", width=25, command=show_student_register_form).pack(pady=10)

    # View Students Button
    tk.Button(window, text="View Students", width=25, command=show_student_list).pack(pady=10)

    # View Attendance Button
    tk.Button(window, text="View Attendance", width=25, command=show_attendance_list).pack(pady=10)

    # Reports Button
    tk.Button(window, text="Reports", width=25, command=show_reports).pack(pady=10)

    # Logout Button
    def logout():
        window.destroy()
        import gui.login  # Local import to avoid circular import
        gui.login.login_screen()

    tk.Button(window, text="Logout", width=25, command=logout).pack(pady=20)

    window.mainloop()
