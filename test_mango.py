import os
import json
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array

MODEL_PATH = r"C:\Users\User\OneDrive\semester four computer science\Ai theory\aiagri\model\fruit_disease_model.h5"
LABELS_PATH = r"C:\Users\User\OneDrive\semester four computer science\Ai theory\aiagri\model\fruit_class_labels.json"
MANGO_IMG = r"C:\venv\project_fruit_dataset\train\Mango_Diseased\1.jpg"
ORANGE_IMG = r"C:\venv\project_fruit_dataset\train\Orange_Healthy\freshOrange (1).jpg"

def main():
    model = load_model(MODEL_PATH)
    with open(LABELS_PATH, "r") as f:
        labels = json.load(f)

    def predict(img_path):
        image = Image.open(img_path)
        if image.mode != "RGB":
            image = image.convert("RGB")
        image = image.resize((128, 128))
        img_array = img_to_array(image)
        img_array = np.expand_dims(img_array, axis=0)
        img_array /= 255.0
        
        preds = model.predict(img_array)
        idx = np.argmax(preds[0])
        print(f"File: {os.path.basename(img_path)}")
        print(f"Prediction: {labels[str(idx)]} (Confidence: {preds[0][idx]:.2f})")
        print("-" * 30)

    predict(MANGO_IMG)
    predict(ORANGE_IMG)

if __name__ == "__main__":
    main()
