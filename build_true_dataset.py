import os
import shutil
from bing_image_downloader import downloader

# The Kaggle dataset we downloaded earlier
KAGGLE_DIR = r"C:\Users\User\.cache\kagglehub\datasets\muhammad0subhan\fruit-and-vegetable-disease-healthy-vs-rotten\versions\1\Fruit And Vegetable Diseases Dataset"
TARGET_DIR = r"C:\venv\project_fruit_dataset\train"

# Crops that are IN the project AND IN the Kaggle dataset
MATCHING_CROPS = {
    "Apple": ("Apple__Healthy", "Apple__Rotten"),
    "Grape": ("Grape__Healthy", "Grape__Rotten"),
    "Orange": ("Orange__Healthy", "Orange__Rotten"),
    "Pepper": ("Bellpepper__Healthy", "Bellpepper__Rotten"),
    "Potato": ("Potato__Healthy", "Potato__Rotten"),
    "Strawberry": ("Strawberry__Healthy", "Strawberry__Rotten"),
    "Tomato": ("Tomato__Healthy", "Tomato__Rotten")
}

# Crops that are IN the project but MISSING from Kaggle dataset
MISSING_CROPS = [
    "Blueberry", "Cherry", "Corn", "Peach", "Raspberry", "Soybean", "Squash"
]

def main():
    if not os.path.exists(TARGET_DIR):
        os.makedirs(TARGET_DIR)

    print("--- Step 1: Copying matching crops from Kaggle dataset ---")
    for crop, (healthy_dir, rotten_dir) in MATCHING_CROPS.items():
        print(f"Processing {crop}...")
        
        # Source paths
        src_healthy = os.path.join(KAGGLE_DIR, healthy_dir)
        src_rotten = os.path.join(KAGGLE_DIR, rotten_dir)
        
        # Target paths
        dst_healthy = os.path.join(TARGET_DIR, f"{crop}_Healthy")
        dst_rotten = os.path.join(TARGET_DIR, f"{crop}_Diseased")
        
        if os.path.exists(src_healthy):
            shutil.copytree(src_healthy, dst_healthy, dirs_exist_ok=True)
        if os.path.exists(src_rotten):
            shutil.copytree(src_rotten, dst_rotten, dirs_exist_ok=True)
            
    print("\n--- Step 2: Downloading missing crops from Bing ---")
    for crop in MISSING_CROPS:
        print(f"Downloading {crop}...")
        
        healthy_query = f"{crop} fruit fresh healthy isolated high quality"
        healthy_dir = f"{crop}_Healthy"
        
        rotten_query = f"{crop} fruit rotten disease mold infected spots"
        rotten_dir = f"{crop}_Diseased"
        
        try:
            downloader.download(healthy_query, limit=50, output_dir=TARGET_DIR, adult_filter_off=True, force_replace=False, timeout=10)
            os.rename(os.path.join(TARGET_DIR, healthy_query), os.path.join(TARGET_DIR, healthy_dir))
        except Exception as e:
            print(f"Error downloading {healthy_query}: {e}")
            
        try:
            downloader.download(rotten_query, limit=50, output_dir=TARGET_DIR, adult_filter_off=True, force_replace=False, timeout=10)
            os.rename(os.path.join(TARGET_DIR, rotten_query), os.path.join(TARGET_DIR, rotten_dir))
        except Exception as e:
            print(f"Error downloading {rotten_query}: {e}")

    print("\nDataset generation complete!")

if __name__ == "__main__":
    main()
