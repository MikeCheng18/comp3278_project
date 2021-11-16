import cv2
import os


def faceCapture(userName):
    NUM_IMGS = 50  # maximum number of images capture for each login
    count = 1
    video_capture = cv2.VideoCapture(0)
    
    if not os.path.exists('data/{}'.format(userName.upper())):
        # if this is a new user, help him make a new directory
        os.mkdir('data/{}'.format(userName.upper()))
    
    # Open camera
    while count <= NUM_IMGS:
        # Capture frame-by-frame
        ret, frame = video_capture.read()
        cv2.imshow('webcam', frame)
        cv2.imwrite(
            "data/{}/{}{:03d}.jpg".format(userName.upper(), userName.upper(), count), frame)
        count += 1
        cv2.waitKey(10)
    
    video_capture.release()
    cv2.destroyAllWindows()
