import os
import shutil

KAGGLE_DIR = r"C:\Users\User\.cache\kagglehub\datasets\muhammad0subhan\fruit-and-vegetable-disease-healthy-vs-rotten\versions\1\Fruit And Vegetable Diseases Dataset"
TARGET_DIR = r"C:\venv\project_fruit_dataset\train"

def main():
    src_healthy = os.path.join(KAGGLE_DIR, "Mango__Healthy")
    src_rotten = os.path.join(KAGGLE_DIR, "Mango__Rotten")
    
    dst_healthy = os.path.join(TARGET_DIR, "Mango_Healthy")
    dst_rotten = os.path.join(TARGET_DIR, "Mango_Diseased")
    
    print("Copying Mango_Healthy...")
    if os.path.exists(src_healthy):
        shutil.copytree(src_healthy, dst_healthy, dirs_exist_ok=True)
        print(f"Copied {len(os.listdir(src_healthy))} healthy mango images.")
        
    print("Copying Mango_Diseased...")
    if os.path.exists(src_rotten):
        shutil.copytree(src_rotten, dst_rotten, dirs_exist_ok=True)
        print(f"Copied {len(os.listdir(src_rotten))} diseased mango images.")
        
    print("Mango successfully added to the dataset!")

if __name__ == "__main__":
    main()
