# AI Agriculture System: Crop & Fruit Disease Detection

## Introduction
I developed this AI Agriculture System to solve a critical problem in modern farming and gardening: early and accurate disease detection. Crop diseases can devastate entire harvests if left untreated. My goal was to build a highly accessible, lightning-fast web application where users can simply upload a photo of a leaf or a fruit, and instantly receive a diagnosis along with professional agricultural treatment advice.

---

## The AI Models Used

To ensure maximum accuracy, I engineered a **Dual-Model AI Engine**. Instead of forcing one neural network to learn everything, I split the task into two specialized models:

### 1. The Leaf Disease Model (`plant_disease_model.h5`)
*   **Purpose:** To analyze the specific spot patterns, discoloration, and structural damage on plant leaves.
*   **Classes:** Trained to recognize **38 different classes** of leaf conditions (e.g., Apple Scab, Tomato Early Blight, Healthy Corn).
*   **Training Data:** Built using the massive PlantVillage dataset.

### 2. The Fruit Disease Model (`fruit_disease_model.h5`)
*   **Purpose:** To detect rot, fungal infections, and physical blemishes directly on the skin of the harvested fruit.
*   **Classes:** Trained to recognize **30 different classes** across 15 different crops (including Mangoes, Apples, Oranges, and Tomatoes), differentiating between Healthy and Diseased states.

### The Core Architecture: MobileNetV2
For both of these models, I chose to use the **MobileNetV2** architecture. I selected this specific Convolutional Neural Network (CNN) because it utilizes "depthwise separable convolutions." This significantly reduces the mathematical parameters required, making the model incredibly fast and lightweight without sacrificing accuracy. 

**How I trained it (Transfer Learning):**
I did not train MobileNetV2 from scratch. Instead, I used a technique called **Transfer Learning**. 
1. I loaded the pre-trained MobileNetV2 model (which already knew how to extract basic shapes and textures from millions of images).
2. I "froze" the base layers so they wouldn't lose their knowledge.
3. I attached my own custom `Dense` layer and `Softmax` output layer to the top of the network, matching the exact number of classes I needed (38 for leaves, 30 for fruits).
4. I fed my datasets into the model using an optimized `128x128` image resolution, allowing the model to quickly learn the specific patterns of crop diseases.

---

## Technologies & Tools: What I Used & How I Used It

To build this full-stack AI application from scratch, I integrated several specific tools. Here is exactly how I utilized each one:

### 1. Python 3
*   **How I used it:** Python served as the core programming language for the entire backend. It tied the machine learning models, the web server, and the image processing scripts together into one seamless pipeline.

### 2. TensorFlow & Keras
*   **How I used it:** I used TensorFlow's Keras API to build, compile, and train the neural networks. I utilized `ImageDataGenerator` to load the 16,000+ dataset images from my folders, applied the `MobileNetV2` application module, and used `model.fit()` to train the AI. Finally, I used `load_model()` in the web server to load the `.h5` files into memory for live predictions.

### 3. Flask (Web Framework)
*   **How I used it:** I used Flask to build a RESTful API backend (`app.py`). I created two main endpoints: `/api/analyze` and `/api/analyze_fruit`. When a user uploads a photo, Flask catches the HTTP POST request, passes the image to the TensorFlow model, and returns the prediction and medical advice back to the website in JSON format.

### 4. Pillow (PIL) & NumPy
*   **How I used it:** AI models only understand numbers, not JPEG files. 
    *   I used **Pillow (PIL)** to open the uploaded image bytes, ensure it was in RGB format, and resize it to the strict `128x128` pixel size required by my model.
    *   I used **NumPy** to convert that Pillow image into a mathematical matrix (array). I also used the `np.argmax()` function to look at the array of probabilities the AI spits out, and find the index of the highest confidence prediction.

### 5. HTML5, Vanilla CSS, & JavaScript
*   **How I used it:** I designed the frontend entirely from scratch without relying on heavy frameworks like React.
    *   **HTML:** Structured the drag-and-drop zone and the two-tab layout (Leaf Scanner vs. Fruit Scanner).
    *   **CSS:** I implemented a modern "Glassmorphism" design system (`backdrop-filter: blur()`) with earthy emerald colors to ensure the UI looks premium and organic.
    *   **JavaScript:** I wrote async `fetch()` functions to silently send the uploaded images to the Flask backend without refreshing the page. JS also handles the dynamic loading animations and populates the results card with the medical advice.

### 6. Kaggle API & Web Scraping
*   **How I used it:** To get the thousands of images needed to train the AI, I wrote scripts to programmatically download datasets from Kaggle. For edge-case fruits that weren't on Kaggle (like specific Mango or Blueberry diseases), I wrote supplementary web-scraping scripts to aggregate the remaining data.

---

## Comprehensive Agricultural Knowledge Base
Instead of just outputting the name of a disease (e.g., "Mango_Diseased"), I engineered a massive internal knowledge base dictionary directly into the backend. 
When the AI makes a prediction, the system queries this database and outputs:
*   **Diagnosis & Health Status:** Clear identification of the pathogen.
*   **Visual Symptoms:** What the farmer should look for to manually verify the AI's prediction.
*   **Medicine & Fungicides:** Exact chemical and organic treatments required to kill the disease.
*   **Management Practices:** Pruning techniques, soil drainage advice, and preventative measures to stop the disease from returning.
