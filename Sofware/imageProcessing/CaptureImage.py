import cv2
import numpy as np
import os

def capture_images():
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)

    faces = []
    labels = []
    username_labels_dict = {}
    image_save_path = "captured_images"

    if not os.path.exists(image_save_path):
        os.makedirs(image_save_path)

    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces_detected = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces_detected:
            face_roi = cv2.resize(gray[y:y + h, x:x + w], (200, 200))
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            username = input("Enter the username for this face: ")

            # Add the face sample, label, and username to the training set
            faces.append(face_roi)
            labels.append(username)
            username_labels_dict[username] = labels.count(username)

            image_filename = f"{username}_{username_labels_dict[username]}.jpg"
            image_path = os.path.join(image_save_path, image_filename)

            cv2.imwrite(image_path, face_roi)
            
        

        cv2.imshow('Capture Faces', frame)
        key = cv2.waitKey(1)

        if key == ord('q') or len(faces) >= 50:
            break

    cap.release()
    cv2.destroyAllWindows()

    return np.array(faces), np.array(labels)

if __name__ == "__main__":
    captured_faces, labels = capture_images()
    np.save('captured_images/captured_faces.npy', captured_faces)
    np.save('captured_images/labels.npy', labels)
