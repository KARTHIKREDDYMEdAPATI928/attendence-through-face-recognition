import tkinter as tk
from tkinter import messagebox
from db_config import get_connection
from gui.admin_dashboard import show_admin_dashboard
from gui.student_dashboard import show_student_dashboard

def login_screen():
    global window, username_entry, password_entry

    window = tk.Tk()
    window.title("Login")
    window.geometry("400x300")  # Adjusted size
    window.configure(bg="#f0f8ff")  # Light Alice Blue background
    window.resizable(False, False)

    # --- Styling ---
    title_font = ("Helvetica", 24, "bold")
    label_font = ("Helvetica", 12)
    entry_font = ("Helvetica", 12)
    button_font = ("Helvetica", 14, "bold")
    accent_color = "#4682b4"  # Steel Blue
    button_bg = "#ffffff"
    button_fg = accent_color
    button_active_bg = "#e0f2f7"  # Light cyan
    frame_bg = "#e0f2f7"  # Light cyan for the frame

    # --- Center Frame ---
    frame = tk.Frame(window, bg=frame_bg, bd=2, relief=tk.GROOVE, padx=30, pady=30)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    # Login Title
    title_label = tk.Label(frame, text="Login", font=title_font, bg=frame_bg, fg=accent_color)
    title_label.pack(pady=(0, 20))

    # Username Label and Entry
    username_label = tk.Label(frame, text="Username", font=label_font, bg=frame_bg, fg="#333")
    username_label.pack(pady=(10, 0), fill="x")
    username_entry = tk.Entry(frame, width=20, font=entry_font)
    username_entry.pack(pady=5, fill="x")

    # Password Label and Entry
    password_label = tk.Label(frame, text="Password", font=label_font, bg=frame_bg, fg="#333")
    password_label.pack(pady=(10, 0), fill="x")
    password_entry = tk.Entry(frame, show="*", width=20, font=entry_font)
    password_entry.pack(pady=5, fill="x")

    # Login Button
    login_button = tk.Button(
        frame,
        text="🔑 Login",
        width=15,
        bg=button_bg,
        fg=button_fg,
        activebackground=button_active_bg,
        font=button_font,
        relief="raised",
        command=authenticate
    )
    login_button.pack(pady=25)

    window.mainloop()

def authenticate():
    username = username_entry.get()
    password = password_entry.get()

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authentication_service WHERE UserName = %s AND Password = %s", (username, password))
        result = cursor.fetchone()

        if result:
            role = result[4]  # 5th column is role
            if role and role.lower() == 'admin':
                messagebox.showinfo("Login Success", f"Welcome {username}!")
                window.destroy()
                show_admin_dashboard(username)
            elif role and role.lower() == 'student':
                messagebox.showinfo("Login Success", f"Welcome {username}!")
                window.destroy()
                show_student_dashboard(username)
            else:
                messagebox.showwarning("Access Denied", "Invalid role.")
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

        cursor.close()
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", f"Error during login: {e}")

# Start the login screen
login_screen()