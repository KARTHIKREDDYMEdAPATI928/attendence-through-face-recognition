from datetime import datetime, time
from database_config import get_connection

def mark_present(student_id):
    conn = get_connection()
    cursor = conn.cursor()

    now = datetime.now().time()
    current_datetime = datetime.now()

    # Get the current period
    cursor.execute("SELECT PeriodID, StartTime FROM period WHERE StartTime <= %s AND EndTime > %s", (now, now))
    result = cursor.fetchone()

    if not result:
        print("⏱ Not within any valid period.")
        return

    period_id, start_time = result

    # Only allow marking present in the first 5 minutes
    allowed_marking_time = (datetime.combine(datetime.today(), start_time).replace(minute=start_time.minute + 5).time())
    if now > allowed_marking_time:
        print("❌ Scan too late. Already marked absent.")
        return

    # Get today's AttendanceID
    cursor.execute("SELECT AttendanceID FROM attendance ORDER BY AttendanceID DESC LIMIT 1")
    attendance_id = cursor.fetchone()[0]

    # Update attendance status
    cursor.execute("""
        UPDATE attendance_details
        SET Status = 'Present'
        WHERE StudentID = %s AND PeriodID = %s AND AttendanceID = %s
    """, (student_id, period_id, attendance_id))
    conn.commit()
    conn.close()
    print(f"[✓] Marked student {student_id} as Present for Period {period_id}")
