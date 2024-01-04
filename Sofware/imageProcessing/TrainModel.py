import cv2
import numpy as np
import os

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

if __name__ == "__main__":
    train_model()
