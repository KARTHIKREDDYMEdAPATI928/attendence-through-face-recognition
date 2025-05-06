import tkinter as tk
from tkinter import simpledialog, messagebox, Toplevel, Text, Scrollbar
import subprocess
import os
from gui.view_students import show_student_list
from gui.student_register import show_student_register_form
from gui.view_attendance import show_attendance_list

def show_admin_dashboard(role=None):
    window = tk.Tk()
    window.title("Admin Dashboard")
    window.geometry("500x600")
    window.resizable(False, False)

    # Try to load background image
    try:
        bg_image = tk.PhotoImage(file="admin_bc.png")
        bg_label = tk.Label(window, image=bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        bg_label.lower()
    except tk.TclError:
        # Fallback: soft vertical gradient using canvas
        canvas = tk.Canvas(window, width=500, height=600)
        canvas.pack(fill="both", expand=True)
        for i in range(0, 600):
            r = int(230 - i / 6)
            g = int(240 - i / 8)
            b = int(250 - i / 10)
            color = f"#{r:02x}{g:02x}{b:02x}"
            canvas.create_line(0, i, 500, i, fill=color)

    # Header Banner
    header = tk.Label(window, text="ADMIN CONTROL PANEL", font=("Arial Rounded MT Bold", 18, "bold"), fg="white", bg="#2c3e50", pady=10)
    header.place(relx=0.5, y=20, anchor="n")

    # Stylish card-like main frame
    frame = tk.Frame(window, bg="white", bd=2, relief=tk.GROOVE, highlightbackground="#95a5a6", highlightthickness=2)
    frame.place(relx=0.5, rely=0.52, anchor="center", width=400, height=500)

    tk.Label(frame, text="Welcome, Admin!", font=("Arial", 16, "bold"), bg="white", fg="#34495e").pack(pady=(30, 20))

    def create_button(parent, text, command, bg_color, hover_color):
        def on_enter(e):
            button['bg'] = hover_color
        def on_leave(e):
            button['bg'] = bg_color
        button = tk.Button(parent, text=text, command=command,
                           font=("Arial", 12, "bold"), fg="white", bg=bg_color,
                           activebackground=hover_color, relief=tk.FLAT, bd=0,
                           width=25, height=2)
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
        button.pack(pady=8)
        return button

    create_button(frame, "Add Student", show_student_register_form, "#2980b9", "#3498db")
    create_button(frame, "View Students", show_student_list, "#2980b9", "#3498db")
    create_button(frame, "View Attendance", show_attendance_list, "#2980b9", "#3498db")

    def capture_face():
        student_id = simpledialog.askstring("Enter ID", "Please enter the Student ID:")
        if student_id:
            subprocess.run(["python", "face_capture.py", student_id])

    create_button(frame, "Capture Face", capture_face, "#16a085", "#1abc9c")
    create_button(frame, "Train Face Model", lambda: subprocess.run(["python", "face_trainer.py"]), "#8e44ad", "#9b59b6")

    def logout(current_window):
        current_window.destroy()
        import gui.login
        gui.login.login_screen()

    create_button(frame, "Logout", lambda: logout(window), "#c0392b", "#e74c3c")

    tk.Label(frame, text="© 2025 Admin Panel", font=("Arial", 10), bg="white", fg="#7f8c8d").pack(side="bottom", pady=10)

    # --- Menu Bar ---
    menubar = tk.Menu(window)

    # File Menu
    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label="Logout", command=lambda: logout(window))
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=window.quit)
    menubar.add_cascade(label="File", menu=file_menu)

    # Queries Menu
    queries_menu = tk.Menu(menubar, tearoff=0)

    student_queries = [
        "INSERT INTO student (...) VALUES (...)",
        "INSERT INTO authentication_service (...) VALUES (...)",
        "SELECT * FROM student",
        "DELETE FROM student WHERE StudentID = %s",
    ]

    attendance_queries = [
        "SELECT Date, Time, Status FROM attendance",
        "SELECT * FROM period",
    ]

    authentication_queries = [
        "SELECT * FROM authentication_service WHERE UserName = %s AND Password = %s",
        "SELECT Role FROM authentication_service WHERE UserName = %s"
    ]

    def display_queries(title, queries):
        query_window = Toplevel(window)
        query_window.title(title)
        text_area = Text(query_window, wrap=tk.WORD, height=10, width=60)
        scrollbar = Scrollbar(query_window, command=text_area.yview)
        text_area.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        text_area.insert(tk.END, "\n".join(queries))
        text_area.config(state=tk.DISABLED)

    queries_menu.add_command(label="Student Management Queries", command=lambda: display_queries("Student Queries", student_queries))
    queries_menu.add_command(label="Attendance Queries", command=lambda: display_queries("Attendance Queries", attendance_queries))
    queries_menu.add_command(label="Authentication Queries", command=lambda: display_queries("Authentication Queries", authentication_queries))
    menubar.add_cascade(label="Queries", menu=queries_menu)

    # Reports Menu
    reports_menu = tk.Menu(menubar, tearoff=0)
    reports_path = "C:\\music"

    def open_report(pdf_path):
        if os.path.exists(pdf_path):
            try:
                if os.name == 'nt':
                    os.startfile(pdf_path)
                else:
                    subprocess.run(['open', pdf_path])
            except Exception as e:
                messagebox.showerror("Error Opening Report", f"Could not open the report.\nError: {e}")
        else:
            messagebox.showerror("Report Not Found", f"The report file '{os.path.basename(pdf_path)}' was not found.")

    if os.path.exists(reports_path) and os.path.isdir(reports_path):
        pdf_files = [f for f in os.listdir(reports_path) if f.lower().endswith(".pdf")]
        for pdf_file in pdf_files:
            file_path = os.path.join(reports_path, pdf_file)
            report_name = os.path.splitext(pdf_file)[0].replace("_", " ").title()
            reports_menu.add_command(label=report_name, command=lambda path=file_path: open_report(path))
    else:
        reports_menu.add_command(label="No Reports Found", state=tk.DISABLED)

    menubar.add_cascade(label="Reports", menu=reports_menu)
    window.config(menu=menubar)

    window.mainloop()
