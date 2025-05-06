import cv2
import mysql.connector

# Connect to the MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Bharath@1608",
    database="recognition"
)
cursor = conn.cursor()

face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

def face_extractor(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray, 1.3, 5)
    if faces is ():
        return None
    for (x, y, w, h) in faces:
        return img[y:y+h, x:x+w]

# Ask user to enter student ID (must exist in database)
student_id = input("Enter Student ID: ")

cursor.execute("SELECT * FROM student WHERE StudentID = %s", (student_id,))
student_data = cursor.fetchone()

if not student_data:
    print("Student not found in the database!")
    exit()

cap = cv2.VideoCapture(0)
count = 0

while True:
    ret, frame = cap.read()
    if face_extractor(frame) is not None:
        count += 1
        face = cv2.resize(face_extractor(frame), (200, 200))
        face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)

        file_name_path = f'dataset/user.{student_id}.{count}.jpg'
        cv2.imwrite(file_name_path, face)

        cv2.putText(face, str(count), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
        cv2.imshow('Face Cropper', face)
    else:
        print("Face not found")
        pass

    if cv2.waitKey(1) == 13 or count == 100:  # Enter key or 100 images
        break

cap.release()
cv2.destroyAllWindows()
print("Face capture completed!")
