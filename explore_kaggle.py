import kagglehub
import os

def main():
    try:
        print("Downloading sriramr/fruits-fresh-and-rotten-for-classification...")
        path = kagglehub.dataset_download("sriramr/fruits-fresh-and-rotten-for-classification")
        print(f"Downloaded to {path}")
        
        print("\nDirectory structure:")
        for root, dirs, files in os.walk(path):
            level = root.replace(path, '').count(os.sep)
            indent = ' ' * 4 * (level)
            print(f"{indent}{os.path.basename(root)}/")
            subindent = ' ' * 4 * (level + 1)
            # Only print first few dirs
            if level == 2:
                print(f"{subindent}Files: {len(files)}")
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
