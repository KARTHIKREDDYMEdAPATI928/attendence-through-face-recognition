import tkinter as tk
from tkinter import messagebox
import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Bharath@1608",
        database="recognition"
    )

def show_student_register_form():
    window = tk.Toplevel()
    window.title("Student Registration")
    window.geometry("500x500")
    window.configure(bg="#E8F0FE")  # Light blue background

    canvas = tk.Canvas(window, bg="#E8F0FE", highlightthickness=0)
    scrollbar = tk.Scrollbar(window, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#E8F0FE")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    title_label = tk.Label(
        scrollable_frame, text="Student Registration Form",
        font=("Verdana", 18, "bold"), bg="#E8F0FE", fg="#333"
    )
    title_label.pack(pady=20)

    def create_labeled_entry(parent, label_text, show=None):
        frame = tk.Frame(parent, bg="#E8F0FE")
        label = tk.Label(frame, text=label_text, font=("Segoe UI", 11, "bold"), bg="#E8F0FE", fg="#333")
        label.pack(anchor="w", padx=5)
        entry = tk.Entry(frame, font=("Segoe UI", 11), bd=2, relief="groove", highlightthickness=1)
        if show:
            entry.config(show=show)
        entry.pack(ipady=5, fill="x", padx=5)
        frame.pack(padx=30, pady=8, fill="x")
        return entry

    entry_id = create_labeled_entry(scrollable_frame, "StudentID")
    entry_fname = create_labeled_entry(scrollable_frame, "First Name")
    entry_lname = create_labeled_entry(scrollable_frame, "Last Name")
    entry_dob = create_labeled_entry(scrollable_frame, "DOB (YYYY-MM-DD)")
    entry_email = create_labeled_entry(scrollable_frame, "Email")
    entry_contact = create_labeled_entry(scrollable_frame, "Contact No")
    entry_class = create_labeled_entry(scrollable_frame, "Class")

    # Gender Dropdown
    gender_frame = tk.Frame(scrollable_frame, bg="#E8F0FE")
    tk.Label(gender_frame, text="Gender", font=("Segoe UI", 11, "bold"), bg="#E8F0FE", fg="#333").pack(anchor="w", padx=5)
    gender_var = tk.StringVar(value="Male")
    gender_dropdown = tk.OptionMenu(gender_frame, gender_var, "Male", "Female", "Other")
    gender_dropdown.config(font=("Segoe UI", 11), width=30, bg="white")
    gender_dropdown.pack(ipady=5, padx=5, fill="x")
    gender_frame.pack(padx=30, pady=8, fill="x")

    entry_username = create_labeled_entry(scrollable_frame, "Set Username")
    entry_password = create_labeled_entry(scrollable_frame, "Set Password", show="*")

    # Register Function
    def register_student():
        try:
            db = connect_db()
            cursor = db.cursor()

            sid = entry_id.get()
            fname = entry_fname.get()
            lname = entry_lname.get()
            dob = entry_dob.get()
            email = entry_email.get()
            contact = entry_contact.get()
            sclass = entry_class.get()
            gender = gender_var.get()
            username = entry_username.get()
            password = entry_password.get()

            query = "INSERT INTO student (StudentID, FirstName, LastName, DOB, Email, ContactNo, class, Gender) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            values = (sid, fname, lname, dob, email, contact, sclass, gender)
            cursor.execute(query, values)

            if username and password:
                auth_query = "INSERT INTO authentication_service (username, password, StudentID) VALUES (%s, %s, %s)"
                cursor.execute(auth_query, (username, password, sid))

            db.commit()
            messagebox.showinfo("Success", "Student Registered Successfully!")

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))
        finally:
            if db.is_connected():
                cursor.close()
                db.close()

    # Fancy Register Button
    def on_enter(e):
        register_btn.config(bg="#2E8B57", fg="white")

    def on_leave(e):
        register_btn.config(bg="#4CAF50", fg="white")

    register_btn = tk.Button(
        scrollable_frame, text="Register", command=register_student,
        font=("Segoe UI", 12, "bold"), bg="#4CAF50", fg="white", padx=10, pady=10,
        relief="raised", bd=2
    )
    register_btn.pack(pady=20)
    register_btn.bind("<Enter>", on_enter)
    register_btn.bind("<Leave>", on_leave)

    window.mainloop()
