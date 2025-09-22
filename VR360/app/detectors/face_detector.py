import cv2

def detect_faces(frame):
    # Use OpenCV's default pre-trained DNN or Haar
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    # Returns list of (x, y, w, h)
    result = []
    for (x, y, w, h) in faces:
        result.append([x, y, x + w, y + h])
    return result
