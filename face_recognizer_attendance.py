# face_recognizer_attendance.py
import cv2
import numpy as np
import mysql.connector
from datetime import datetime, timedelta
import pickle
import os
import sys

if len(sys.argv) > 1:
    logged_in_username = sys.argv[1]
    print(f"Logged-in username (received as argument): {logged_in_username}")
else:
    logged_in_username = "unknown_user"
    print("Logged-in username not provided as argument.")

# Load trained face recognizer and labels
recognizer = cv2.face.LBPHFaceRecognizer_create()
try:
    recognizer.read("trainer/trainer.yml")
except Exception as e:
    print(f"Error loading trainer.yml: {e}")
    exit()

# Load face cascade
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
if face_cascade.empty():
    print("Error loading face cascade xml file.")
    exit()

# Load labels
try:
    with open("labels.pickle", "rb") as f:
        labels = pickle.load(f)
        labels = {v: k for k, v in labels.items()}
except Exception as e:
    print(f"Error loading labels.pickle: {e}")
    exit()

# Connect to database
try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Bharath@1608",
        database="recognition"
    )
    cursor = conn.cursor()
except mysql.connector.Error as err:
    print(f"Error connecting to MySQL: {err}")
    exit()

attendance_marked_absent_today = False

# Mark attendance function (marks per period)
def mark_attendance(student_id):
    global attendance_marked_absent_today
    now = datetime.now()
    current_datetime = now.strftime("%Y-%m-%d %H:%M:%S")
    current_time_str = now.strftime("%H:%M:%S")
    current_date = now.date()

    print(f"mark_attendance called for StudentID: {student_id} at {current_datetime}") # DEBUG

    try:
        # Get the DateID
        cursor.execute("SELECT DateID FROM attendance_date WHERE Date = %s", (current_date,))
        date_result = cursor.fetchone()
        if date_result:
            date_id = date_result[0]
            print(f"DateID found: {date_id}") # DEBUG
        else:
            cursor.execute("INSERT INTO attendance_date (Date) VALUES (%s)", (current_date,))
            conn.commit()
            date_id = cursor.lastrowid
            print(f"New DateID inserted: {date_id}") # DEBUG

        # Find the current PeriodID
        cursor.execute("SELECT PeriodID FROM period WHERE StartTime <= %s AND EndTime > %s", (current_time_str, current_time_str))
        period_result = cursor.fetchone()

        if period_result:
            period_id = period_result[0]
            print(f"Active PeriodID found: {period_id}") # DEBUG

            # Check if attendance is already marked for this student, date, and period
            cursor.execute(
                "SELECT AttendanceID FROM attendance WHERE StudentID = %s AND DateID = %s AND PeriodID = %s",
                (student_id, date_id, period_id)
            )
            existing_attendance = cursor.fetchone()

            if not existing_attendance:
                status = 'Present'
                cursor.execute(
                    "INSERT INTO attendance (DateID, StudentID, PeriodID, Status) VALUES (%s, %s, %s, %s)",
                    (date_id, student_id, period_id, status)
                )
                conn.commit()
                print(f"Attendance marked as {status} for StudentID {student_id} on {current_date} at {current_time_str}, PeriodID: {period_id}")
                return True
            else:
                print(f"Attendance already marked for StudentID {student_id} on {current_date} during PeriodID {period_id}.")
                return True
        else:
            print(f"No active period found for the current time: {current_time_str}. Attempting to mark as Absent with NULL PeriodID.")
            if not attendance_marked_absent_today:
                status = 'Absent'
                print(f"Attempting to INSERT: DateID={date_id}, StudentID={student_id}, PeriodID=NULL, Status='{status}'") # DEBUG
                try:
                    cursor.execute(
                        "INSERT INTO attendance (DateID, StudentID, PeriodID, Status) VALUES (%s, %s, NULL, %s)",
                        (date_id, student_id, status)
                    )
                    conn.commit()
                    print(f"Attendance marked as Absent for StudentID {student_id} on {current_date} with PeriodID NULL.")
                    attendance_marked_absent_today = True
                    return False
                except mysql.connector.Error as err:
                    print(f"MySQL Error during Absent marking: {err}")
                    print(f"Error details: {err}") # More detailed error info
                    conn.rollback()
                    return False
            else:
                print(f"Attendance already marked as Absent (outside period) today.")
                return False

    except mysql.connector.Error as err:
        print(f"MySQL Error marking attendance: {err}")
        print(f"Error details (outer): {err}") # More detailed error info
        conn.rollback()
        return False

# Start webcam
cam = cv2.VideoCapture(0)

while True:
    ret, frame = cam.read()
    if not ret:
        print("Error: Could not read frame from webcam.")
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]

        id_, conf = recognizer.predict(roi_gray)
        if conf < 60:
            recognized_student_id = id_
            try:
                # Get the StudentID associated with the logged-in username
                cursor.execute("SELECT StudentID FROM authentication_service WHERE UserName = %s", (logged_in_username,))
                auth_result = cursor.fetchone()

                if auth_result:
                    logged_in_student_id = auth_result[0]

                    # Compare the recognized StudentID with the logged-in StudentID
                    if recognized_student_id == logged_in_student_id:
                        # Get the full name for display
                        cursor.execute("SELECT FirstName, LastName FROM student WHERE StudentID = %s", (recognized_student_id,))
                        student_info = cursor.fetchone()
                        if student_info:
                            first_name, last_name = student_info
                            full_name = f"{first_name} {last_name}"
                            print(f"Face recognized matches logged-in user (StudentID: {logged_in_student_id})")
                            mark_attendance(recognized_student_id)
                            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                            cv2.putText(frame, full_name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
                        else:
                            print("StudentID found in authentication but not in student table.")
                    else:
                        print(f"Face detected (StudentID: {recognized_student_id}) does not match logged-in user (StudentID: {logged_in_student_id})")
                else:
                    print(f"Logged-in username '{logged_in_username}' not found in authentication service.")

            except mysql.connector.Error as err:
                print(f"Error querying database: {err}")
        else:
            # Optionally display the recognized face even if confidence is low
            try:
                cursor.execute("SELECT FirstName, LastName FROM student WHERE StudentID = %s", (id_,))
                student_info = cursor.fetchone()
                if student_info:
                    first_name, last_name = student_info
                    full_name = f"{first_name} {last_name}"
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2) # Different color for non-recognized
                    cv2.putText(frame, f"Unknown", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
            except:
                pass

    cv2.imshow("Face Recognizer", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
if conn.is_connected():
    cursor.close()
    conn.close()