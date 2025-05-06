# gui/view_students.py
import tkinter as tk
from tkinter import ttk, messagebox
from db_config import get_connection

def delete_student_record(win, tree, student_id):
    """Deletes a student record and all related data."""
    if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete student with ID: {student_id}?", parent=win):
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()

            # First, delete related records from time_tracking_system
            cursor.execute("DELETE FROM time_tracking_system WHERE AttendanceID IN (SELECT AttendanceID FROM attendance WHERE StudentID = %s)", (student_id,))
            conn.commit()

            # Then, delete related attendance records
            cursor.execute("DELETE FROM attendance WHERE StudentID = %s", (student_id,))
            conn.commit()

            # Next, delete related records from attendance_log
            cursor.execute("DELETE FROM attendance_log WHERE StudentID = %s", (student_id,))
            conn.commit()

            # Finally, delete the student record
            cursor.execute("DELETE FROM student WHERE StudentID = %s", (student_id,))
            conn.commit()

            messagebox.showinfo("Success", f"Student with ID {student_id} and all related data deleted successfully!", parent=win)
            # Remove the selected item from the Treeview
            for item in tree.get_children():
                if tree.item(item, 'values')[0] == student_id:
                    tree.delete(item)
                    break

        except Exception as e:
            messagebox.showerror("Database Error", f"Error deleting student and related data: {e}", parent=win)
            if conn:
                conn.rollback()
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

def show_student_list():
    win = tk.Toplevel()
    win.title("Student List")
    win.geometry("1000x600")
    win.configure(bg="#e0f7fa")

    style = ttk.Style()
    style.theme_use('clam')

    style.configure("Treeview.Heading", background="#00bcd4", foreground="white", font=("Roboto", 10, "bold"), relief="solid")
    style.map("Treeview.Heading", background=[('active', '#0097a7')])
    style.configure("Treeview", background="#ffffff", foreground="#424242", font=("Roboto", 9), borderwidth=1, relief="flat")
    style.map("Treeview", background=[('selected', '#80deea')])
    style.configure("Delete.TLabel", foreground="#d32f2f", font=("Roboto", 9, "bold"), background="#ffffff")
    style.map("Delete.TLabel", foreground=[('active', '#f44336')])

    tk.Label(win, text="Student Directory", font=("Roboto", 24, "bold"), bg="#e0f7fa", fg="#1976d2", pady=25).pack()

    # Create Treeview with scrollbars
    tree_frame = tk.Frame(win, bg="#e0f7fa")
    tree_frame.pack(fill=tk.BOTH, expand=True, padx=25, pady=25)

    tree_scroll_y = tk.Scrollbar(tree_frame, orient="vertical")
    tree_scroll_x = tk.Scrollbar(tree_frame, orient="horizontal")

    tree = ttk.Treeview(tree_frame, columns=("ID", "First Name", "Last Name", "DOB", "Email", "Contact", "Class", "Gender", "Action"),
                        show='headings', style="Treeview", yscrollcommand=tree_scroll_y.set, xscrollcommand=tree_scroll_x.set)

    tree_scroll_y.config(command=tree.yview)
    tree_scroll_x.config(command=tree.xview)

    tree.column("#0", width=0, stretch=tk.NO)
    tree.column("ID", anchor=tk.CENTER, width=60)
    tree.column("First Name", anchor=tk.W, width=150)
    tree.column("Last Name", anchor=tk.W, width=150)
    tree.column("DOB", anchor=tk.CENTER, width=110)
    tree.column("Email", anchor=tk.W, width=220)
    tree.column("Contact", anchor=tk.CENTER, width=130)
    tree.column("Class", anchor=tk.CENTER, width=100)
    tree.column("Gender", anchor=tk.CENTER, width=100)
    tree.column("Action", anchor=tk.CENTER, width=80)

    tree.heading("ID", text="ID")
    tree.heading("First Name", text="First Name")
    tree.heading("Last Name", text="Last Name")
    tree.heading("DOB", text="DOB")
    tree.heading("Email", text="Email")
    tree.heading("Contact", text="Contact")
    tree.heading("Class", text="Class")
    tree.heading("Gender", text="Gender")
    tree.heading("Action", text="Action")

    tree_scroll_y.pack(side="right", fill="y")
    tree_scroll_x.pack(side="bottom", fill="x")
    tree.pack(fill=tk.BOTH, expand=True)

    def alternate_row_colors(tree, tag1="oddrow", tag2="evenrow"):
        for i, item in enumerate(tree.get_children()):
            tag = tag1 if i % 2 == 0 else tag2
            tree.item(item, tags=(tag,))
        tree.tag_configure(tag1, background="#f5f5f5")
        tree.tag_configure(tag2, background="#e0f2f7")

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT StudentID, FirstName, LastName, DOB, Email, ContactNo, class, Gender FROM student")
        rows = cursor.fetchall()

        for i, row in enumerate(rows):
            student_id = row[0]
            tree.insert('', tk.END, values=row + ("Delete",), tags=('oddrow' if i % 2 == 0 else 'evenrow',))
        alternate_row_colors(tree)

        def on_treeview_click(event):
            item = tree.identify_row(event.y)
            column = tree.identify_column(event.x)

            if item and column == '#9':  # '#9' is the column identifier for 'Action'
                values = tree.item(item, 'values')
                student_id = values[0]
                delete_student_record(win, tree, student_id)

        tree.bind('<ButtonRelease-1>', on_treeview_click)

        cursor.close()
        conn.close()

    except Exception as e:
        tk.Label(win, text=f"Error loading student data: {e}", fg="red", bg="#e0f7fa").pack(pady=10)