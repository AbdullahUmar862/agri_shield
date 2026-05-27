import os
import requests
from duckduckgo_search import DDGS
from concurrent.futures import ThreadPoolExecutor
import time

TARGET_DIR = r"C:\venv\fruit_dataset\train"

# We want healthy and diseased classes for all fruits in our project
FRUITS = [
    "Apple", "Cherry", "Grape", "Peach", "Pepper", "Potato", "Strawberry", "Tomato"
]

CONDITIONS = {
    "Healthy": "healthy freshly picked",
    "Diseased": "rotten diseased infected"
}

IMAGES_PER_CLASS = 40  # Small but enough to train a basic model (total 40 * 16 = 640 images)

def download_image(url, filepath):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            with open(filepath, 'wb') as f:
                f.write(response.content)
            return True
    except Exception as e:
        pass
    return False

def build_dataset():
    if not os.path.exists(TARGET_DIR):
        os.makedirs(TARGET_DIR)
        
    ddgs = DDGS()
    
    for fruit in FRUITS:
        for condition_name, condition_query in CONDITIONS.items():
            class_name = f"{fruit}_{condition_name}"
            class_dir = os.path.join(TARGET_DIR, class_name)
            
            if not os.path.exists(class_dir):
                os.makedirs(class_dir)
                
            print(f"Downloading images for {class_name}...")
            
            # The search query
            query = f"{fruit} fruit {condition_query}"
            
            try:
                results = list(ddgs.images(query, max_results=IMAGES_PER_CLASS * 2))
            except Exception as e:
                print(f"Failed to search {query}: {e}")
                time.sleep(2)
                continue
                
            downloaded = 0
            
            # Use threading to speed up downloads
            def process_img(idx, r):
                url = r.get('image')
                if not url: return False
                ext = url.split('.')[-1][:3].lower()
                if ext not in ['jpg', 'jpe', 'png']:
                    ext = 'jpg'
                filepath = os.path.join(class_dir, f"img_{idx}.{ext}")
                return download_image(url, filepath)

            with ThreadPoolExecutor(max_workers=5) as executor:
                futures = []
                for i, r in enumerate(results):
                    futures.append(executor.submit(process_img, i, r))
                
                for future in futures:
                    if future.result():
                        downloaded += 1
                        if downloaded >= IMAGES_PER_CLASS:
                            break
            
            print(f"Finished {class_name}: downloaded {downloaded} images.")
            time.sleep(1) # Be nice to the API

if __name__ == "__main__":
    print("Starting dataset builder...")
    build_dataset()
    print("Done!")
