import os
from PIL import Image

DATA_DIR = r"C:\venv\project_fruit_dataset\train"

def clean_images(directory):
    removed = 0
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                img = Image.open(file_path)
                img.verify() # Verify that it is, in fact, an image
            except (IOError, SyntaxError) as e:
                print(f"Removing corrupt image: {file_path}")
                os.remove(file_path)
                removed += 1
            except Exception as e:
                print(f"Removing unreadable file: {file_path}")
                os.remove(file_path)
                removed += 1
    print(f"Removed {removed} invalid files.")

if __name__ == "__main__":
    clean_images(DATA_DIR)
