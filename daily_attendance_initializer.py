import mysql.connector
from datetime import datetime

def initialize_daily_attendance():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Bharath@1608',
            database='recognition'
        )
        cursor = conn.cursor()

        now = datetime.now()

        # Get all students
        cursor.execute("SELECT StudentID FROM student")
        students = cursor.fetchall()

        # Period IDs (assuming 1 to 8)
        periods = list(range(1, 9))

        for student in students:
            student_id = student[0]
            for period_id in periods:
                cursor.execute("""
                    INSERT INTO attendance (Time, StudentID, PeriodID, Status)
                    VALUES (%s, %s, %s, %s)
                """, (now, student_id, period_id, 'Absent'))

        conn.commit()
        print("✅ Daily attendance initialized with 'Absent' for all students.")

        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        print("❌ DB Error:", err)

# Call the initializer
initialize_daily_attendance()
