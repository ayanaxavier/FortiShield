import os
from modules.preprocess import binary_to_image

input_folder = "benign_files"
output_folder = "dataset/benign"

os.makedirs(output_folder, exist_ok=True)

files = os.listdir(input_folder)

print("Files found:",  len(files))

for file in files:
    file_path = os.path.join(input_folder, file)

    if os.path.isfile(file_path):
        try:
            binary_to_image(file_path, output_folder)
        except Exception as e:
            print("Skipped:", file, e)

print("Finished converting benign files.")