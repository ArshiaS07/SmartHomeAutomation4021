import cv2
import numpy as np
import os

# Initialize the face recognition confidence threshold
confidence_threshold = 50  # Decreased threshold for stricter matching

def train_model():
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()

    captured_faces = np.load('captured_images/captured_faces.npy')
    labels = np.load('captured_images/labels.npy')

    # Convert labels to integers
    unique_labels, label_mapping = np.unique(labels, return_inverse=True)
    labels = label_mapping

    face_recognizer.train(captured_faces, labels)

    model_save_path = "trained_model"
    if not os.path.exists(model_save_path):
        os.makedirs(model_save_path)
    face_recognizer.save(os.path.join(model_save_path, 'face_recognizer_model.xml'))

def face_recognition():
    global confidence_threshold  # Make confidence_threshold a global variable

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()

    model_path = "trained_model/face_recognizer_model.xml"
    face_recognizer.read(model_path)

    cap = cv2.VideoCapture(0)

    while True:
        # Capture frame from webcam
        ret, frame = cap.read()

        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces_detected = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces_detected:
            # Extract the face region
            face_roi = gray[y:y + h, x:x + w]

            # Resize the face image to a fixed size for recognition
            face_roi = cv2.resize(face_roi, (200, 200))

            # Recognize the face only if the model is trained
            if model_trained:
                # Recognize the face
                label, confidence = face_recognizer.predict(face_roi)

                # Check if the confidence is below the threshold for face recognition
                if confidence < confidence_threshold:
                    # Faces match, open the door (you can replace this with your own action)
                    username = get_username(label)
                    print(f"Face recognized as {username} with confidence: {confidence}. Access granted!")

                    # Perform action after recognizing the face (e.g., open the door)
                    # For demonstration purposes, we print a message
                    print("Opening the door!")

                else:
                    # Faces do not match
                    print(f"Face not recognized with confidence: {confidence}. Access denied.")

            # Draw rectangle around the face
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Display the frame
        cv2.imshow('Face Recognition', frame)

        # Break the loop when 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close all windows
    cap.release()
    cv2.destroyAllWindows()

def get_username(label):
    # Assuming label corresponds to the index in unique_labels
    unique_labels = np.load('captured_images/unique_labels.npy')
    return unique_labels[label]

if __name__ == "__main__":
    train_model()  # Train the model first
    model_trained = True  # Set the flag indicating that the model is trained
    face_recognition()  # Start face recognition
