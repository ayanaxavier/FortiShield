import numpy as np
import tensorflow as tf
import cv2
import os
import sys

from modules.preprocess import binary_to_image
from modules.quarantine import move_to_quarantine
from modules.logger import log_event
from modules.notifier import show_alert

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS   # PyInstaller temp folder
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Load trained AI model
model = tf.keras.models.load_model(resource_path("ai_model/malware_model.keras"))


def scan_file(file_path):

    print("\nScanning with AI model...")
    print(f"File: {file_path}")

    try:
        # Convert file to image
        image_path = binary_to_image(file_path, "temp")

        # Load and preprocess image
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img, (64, 64))
        img = img.reshape(1, 64, 64, 1)

        # Predict
        prediction = model.predict(img)[0][0]
        confidence = round(prediction * 100, 2)

        print(f"Prediction score: {prediction:.4f}")
        print(f"Confidence: {confidence}%")

        if prediction > 0.80:
            print("🚨 Malware detected! (High Confidence)")
            move_to_quarantine(file_path)

            log_event(file_path, "Malware", f"Quarantined ({confidence}%)")

            show_alert(
                "CyberGuardian Alert 🚨",
                f"Malicious file detected!\n{os.path.basename(file_path)}"
            )

            return {
                "prediction": "Malware",
                "confidence": confidence
            }

        elif prediction > 0.60:
            print("⚠ Suspicious file detected! (Medium Risk)")

            log_event(file_path, "Suspicious", f"No action ({confidence}%)")

            return {
                "prediction": "Suspicious",
                "confidence": confidence
            }

        else:
            print("✅ File is safe.")

            log_event(file_path, "Safe", f"No action ({confidence}%)")

            return {
                "prediction": "Safe",
                "confidence": confidence
            }

    except Exception as e:
        print("Error scanning file:", e)
        return {
            "prediction": "Error",
            "confidence": 0
        }