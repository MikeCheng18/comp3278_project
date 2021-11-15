import mysql.connector
import cv2
import pickle
import time


def faceIDLoginProcessCode():    
    # 2 Load recognize and read label from model
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("train.yml")
    labels = {"person_name": 1}
    with open("labels.pickle", "rb") as f:
        labels = pickle.load(f)
        labels = {v: k for k, v in labels.items()}
    # Define camera and detect face
    face_cascade = cv2.CascadeClassifier(
        'haarcascade/haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)

    # 3 Open the camera and start face recognition
    start = time.time()
    # only open camera for 3 seconds
    while (time.time() - start < 3):
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(
            gray, scaleFactor=1.5, minNeighbors=3)

        for (x, y, w, h) in faces:
            roi_gray = gray[y:y + h, x:x + w]
            # predict the id and confidence for faces
            id_, conf = recognizer.predict(roi_gray)

            # 4.1 If the face is recognized
            gui_confidence = 0.5
            if conf >= gui_confidence:
                name = labels[id_]

                # Find the customer information in the database.
                myconn = mysql.connector.connect(
                host="localhost", user="root", passwd="!@#$%^&*()qwertyuiopWinter2021", database="iKYC")
                cursor = myconn.cursor()
                sql = "SELECT username FROM Customer WHERE username=%s"
                value = (name, )
                cursor.execute(sql, value)
                result = cursor.fetchall()
                myconn.commit()

                if (result == []):
                    return "404"
                # If the customer's information is found in the database
                else:
                    # Login SUCCESS
                    return name
            # 4.2 If the face is unrecognized
            else:
                print("Face is unrecognized")
    return "404"

print(faceIDLoginProcessCode())