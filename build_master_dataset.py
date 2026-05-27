import kagglehub
import os
import time

DATA_DIR = r"C:\venv\master_fruit_dataset"

def main():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        
    print("Downloading muhammad0subhan/fruit-and-vegetable-disease-healthy-vs-rotten...")
    print("Note: This is a 5GB dataset, it will take a while.")
    
    max_retries = 10
    for attempt in range(max_retries):
        try:
            path = kagglehub.dataset_download("muhammad0subhan/fruit-and-vegetable-disease-healthy-vs-rotten")
            print(f"Successfully downloaded to {path}")
            
            print("\nDirectory contents:")
            for root, dirs, files in os.walk(path):
                level = root.replace(path, '').count(os.sep)
                indent = ' ' * 4 * (level)
                print(f"{indent}{os.path.basename(root)}/")
                if level == 2:
                    pass
            print("\nDataset ready!")
            break
        except Exception as e:
            print(f"Network error on attempt {attempt + 1}: {e}")
            print("Retrying in 5 seconds...")
            time.sleep(5)
    else:
        print("Failed to download dataset after maximum retries.")

if __name__ == "__main__":
    main()
