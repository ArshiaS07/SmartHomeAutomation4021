import cv2
import numpy as np
import os
import time

def capture_images_from_camera(output_path, num_images_per_user=50):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    faces = []
    labels = []

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    num_users = int(input("Enter the number of users: "))  #   

    cap = cv2.VideoCapture(0)  # 
    for user_id in range(1, num_users + 1):
        username = input(f"Enter the username for user {user_id}: ")  # 

        frame_count = 0
        while frame_count < num_images_per_user:
            ret, frame = cap.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces_detected = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            for (x, y, w, h) in faces_detected:
                face_roi = cv2.resize(gray[y:y + h, x:x + w], (200, 200))
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Add the face sample and label to the training set
                faces.append(face_roi)
                labels.append(f"{username}_{frame_count}")

                image_filename = f"captured_image_{username}_{frame_count}.jpg"
                image_path = os.path.join(output_path, image_filename)

                cv2.imwrite(image_path, face_roi)

                print(f"Image {frame_count} for user {username} saved at {image_path}")

                frame_count += 1

            cv2.imshow('Capture Faces', frame)
            cv2.waitKey(100)  # Delay for 100 milliseconds between each capture
            #time.sleep(1)  # 
        print(f"User {username} completed recording.")

    cap.release()
    cv2.destroyAllWindows()

    return np.array(faces), np.array(labels)

if __name__ == "__main__":
    output_path = os.path.abspath("captured_images_from_camera")

    captured_faces, labels = capture_images_from_camera(output_path, num_images_per_user=50)
    np.save('captured_images_from_camera/captured_faces.npy', captured_faces)
    np.save('captured_images_from_camera/labels.npy', labels)
