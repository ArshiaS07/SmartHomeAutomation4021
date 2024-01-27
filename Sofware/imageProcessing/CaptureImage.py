import cv2
import numpy as np
import os

def capture_images(num_images_per_user=50, num_users=2):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)

    faces = []
    labels = []
    image_save_path = "captured_images"

    if not os.path.exists(image_save_path):
        os.makedirs(image_save_path)

    for user_id in range(1, num_users + 1):
        user_faces = []
        username = input(f"Enter the username for user {user_id}: ")

        for img_count in range(1, num_images_per_user + 1):
            ret, frame = cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces_detected = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            for (x, y, w, h) in faces_detected:
                face_roi = cv2.resize(gray[y:y + h, x:x + w], (200, 200))
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Add the face sample and label to the training set
                user_faces.append(face_roi)
                labels.append(username)

                image_filename = f"{username}_{img_count}_{user_id}.jpg"
                image_path = os.path.join(image_save_path, image_filename)

                cv2.imwrite(image_path, face_roi)

            cv2.imshow(f'Capture Faces - User {user_id}', frame)
            cv2.waitKey(1000)  # Delay for 1 second between each capture

        faces.extend(user_faces)

    cap.release()
    cv2.destroyAllWindows()

    return np.array(faces), np.array(labels)

if __name__ == "__main__":
    captured_faces, labels = capture_images(num_images_per_user=5, num_users=2)
    np.save('captured_images/captured_faces.npy', captured_faces)
    np.save('captured_images/labels.npy', labels)
