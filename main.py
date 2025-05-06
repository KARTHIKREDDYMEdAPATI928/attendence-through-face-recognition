# main.py
import tkinter as tk
from tkinter import messagebox
from gui.login import login_screen
import subprocess
import sys

def run_face_recognition(logged_in_username):
    try:
        subprocess.run([sys.executable, "face_recognizer_attendance.py", logged_in_username], check=True)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Error running face recognition script: {e}")
    except FileNotFoundError:
        messagebox.showerror("Error", "face_recognizer_attendance.py not found.")

def main():
    try:
        window = tk.Tk()
        window.withdraw()  # Hide the main window initially
        logged_in_username = login_screen()
        window.deiconify() # Show the main window if needed later

        if logged_in_username:
            run_face_recognition(logged_in_username)
        else:
            messagebox.showinfo("Info", "Login cancelled or failed.")
        if window.winfo_exists():
            window.destroy()
    except Exception as e:
        messagebox.showerror("Error", f"Application failed to start: {e}")

if __name__ == "__main__":
    main()