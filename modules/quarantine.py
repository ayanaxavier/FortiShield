import os
import shutil

QUARANTINE_FOLDER = "quarantine"


def move_to_quarantine(file_path):

    if not os.path.exists(QUARANTINE_FOLDER):
        os.makedirs(QUARANTINE_FOLDER)

    file_name = os.path.basename(file_path)
    destination = os.path.join(QUARANTINE_FOLDER, file_name)

    try:
        shutil.move(file_path, destination)
        print(f"⚠ File moved to quarantine: {destination}")
    except Exception as e:
        print("Error moving file to quarantine:", e)