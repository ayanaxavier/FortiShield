import numpy as np
import cv2
import os


def binary_to_image(file_path, output_folder="temp"):

    os.makedirs(output_folder, exist_ok=True)

    with open(file_path, 'rb') as file:
        binary_data = file.read()

    byte_array = np.frombuffer(binary_data, dtype=np.uint8)

    size = int(np.sqrt(len(byte_array)))

    byte_array = byte_array[:size * size]

    image = byte_array.reshape((size, size))

    # 🔥 FIX: Resize large images to manageable size
    image = cv2.resize(image, (256, 256))

    file_name = os.path.basename(file_path)
    name_without_ext = os.path.splitext(file_name)[0]

    output_path = os.path.join(output_folder, name_without_ext + ".png")

    cv2.imwrite(output_path, image)

    print(f"Converted: {file_name}")

    return output_path