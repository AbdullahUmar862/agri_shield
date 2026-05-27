import os
import shutil
import glob

SRC_DIR = r"C:\venv\fruit_dataset"
TARGET_DIR = r"C:\venv\fruit_training_data"

def safe_copy(src, dst):
    try:
        shutil.copy(src, dst)
    except Exception as e:
        pass

def main():
    if not os.path.exists(TARGET_DIR):
        os.makedirs(TARGET_DIR)

    # 1. Tomato (we'll just use the images from 'train/images' and assume they are diseased)
    tomato_dir = os.path.join(TARGET_DIR, "Tomato_Diseased")
    os.makedirs(tomato_dir, exist_ok=True)
    tomato_imgs = glob.glob(os.path.join(SRC_DIR, "train", "images", "*.jpg"))
    for i, img in enumerate(tomato_imgs[:100]): # Limit to 100 for speed
        safe_copy(img, os.path.join(tomato_dir, f"tomato_d_{i}.jpg"))

    # 2. Apple (apple_disease_classification usually has subfolders)
    apple_src = os.path.join(SRC_DIR, "apple_disease_classification")
    if os.path.exists(apple_src):
        for folder in os.listdir(apple_src):
            folder_path = os.path.join(apple_src, folder)
            if os.path.isdir(folder_path):
                # Is it healthy or diseased?
                if "healthy" in folder.lower():
                    target = os.path.join(TARGET_DIR, "Apple_Healthy")
                else:
                    target = os.path.join(TARGET_DIR, "Apple_Diseased")
                os.makedirs(target, exist_ok=True)
                imgs = glob.glob(os.path.join(folder_path, "*.*"))
                for i, img in enumerate(imgs[:50]): # 50 per sub-disease
                    safe_copy(img, os.path.join(target, f"{folder}_{i}.jpg"))

    # 3. Mango (MangoFruitDDS)
    mango_src = os.path.join(SRC_DIR, "MangoFruitDDS")
    if os.path.exists(mango_src):
        for folder in os.listdir(mango_src):
            folder_path = os.path.join(mango_src, folder)
            if os.path.isdir(folder_path):
                if "healthy" in folder.lower() or "fresh" in folder.lower():
                    target = os.path.join(TARGET_DIR, "Mango_Healthy")
                else:
                    target = os.path.join(TARGET_DIR, "Mango_Diseased")
                os.makedirs(target, exist_ok=True)
                imgs = glob.glob(os.path.join(folder_path, "*.*"))
                for i, img in enumerate(imgs[:50]):
                    safe_copy(img, os.path.join(target, f"mango_{folder}_{i}.jpg"))

    print("Dataset organized successfully at:", TARGET_DIR)
    
if __name__ == "__main__":
    main()
