import cv2
import numpy as np
import os

def train_model(captured_faces_path, captured_labels_path, model_save_path):
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()

    captured_faces = np.load(captured_faces_path, allow_pickle=True)
    labels = np.load(captured_labels_path, allow_pickle=True)


    # Convert labels to integers
    unique_labels, label_mapping = np.unique(labels, return_inverse=True)
    labels = label_mapping

    face_recognizer.train(captured_faces, labels)

    if not os.path.exists(model_save_path):
        os.makedirs(model_save_path)
    # دیگر بخش‌های کد
    model_filename = 'face_recognizer_model.xml'
    model_path = os.path.join(model_save_path, model_filename)
    face_recognizer.save(model_path)
    print(f"Model saved at: {model_path}")

if __name__ == "__main__":
    captured_faces_path = 'captured_images/captured_faces.npy'
    captured_labels_path = 'captured_images/labels.npy'
    model_save_path = 'trained_model'

    train_model(captured_faces_path, captured_labels_path, model_save_path)
