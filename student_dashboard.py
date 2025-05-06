# student_dashboard.py
import tkinter as tk
from tkinter import messagebox
import subprocess
import sys

def show_student_dashboard(username):
    window = tk.Tk()
    window.title("Student Dashboard")
    window.geometry("400x300")  # Slightly adjusted size
    window.configure(bg="#f0f8ff")  # Light Alice Blue background
    # window.resizable(False, False)  <--- REMOVE OR COMMENT OUT THIS LINE

    # --- Styling ---
    title_font = ("Helvetica", 24, "bold")
    button_font = ("Helvetica", 14)
    accent_color = "#4682b4"  # Steel Blue
    button_bg = "#ffffff"
    button_fg = accent_color
    button_active_bg = "#e0f2f7"  # Light cyan
    logout_bg = "#ff6347"  # Tomato
    logout_active_bg = "#ff8a65"

    # --- Widgets ---
    # Welcome Label with more padding and centered
    welcome_label = tk.Label(
        window,
        text=f"Welcome, {username}!",
        font=title_font,
        bg="#f0f8ff",
        fg=accent_color,
        pady=20
    )
    welcome_label.pack(fill="x")

    # Frame to center buttons
    button_frame = tk.Frame(window, bg="#f0f8ff")
    button_frame.pack(pady=20, padx=20)

    # Recognize & Mark Attendance Button
    def recognize_and_mark():
        try:
            subprocess.run([sys.executable, "face_recognizer_attendance.py", username], check=True)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to run face recognition script:\n{e}")

    recognize_button = tk.Button(
        button_frame,
        text="✨ Recognize & Mark Attendance",
        font=button_font,
        bg=button_bg,
        fg=button_fg,
        activebackground=button_active_bg,
        width=25,
        height=2,
        relief="raised",  # Added a raised effect
        command=recognize_and_mark
    )
    recognize_button.pack(pady=10, fill="x")

    # Logout Button
    def logout():
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            window.destroy()
            subprocess.Popen([sys.executable, "gui/login.py"])

    logout_button = tk.Button(
        button_frame,
        text="🚪 Logout",
        font=button_font,
        bg=logout_bg,
        fg="white",
        activebackground=logout_active_bg,
        width=20,
        height=1,
        relief="raised",  # Added a raised effect
        command=logout
    )
    logout_button.pack(pady=10, fill="x")

    window.mainloop()