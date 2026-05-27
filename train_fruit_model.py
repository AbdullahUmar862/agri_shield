import os
import json
import matplotlib.pyplot as plt
from tensorflow import keras
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.callbacks import EarlyStopping

DATA_DIR = r"C:\venv\project_fruit_dataset\train"
MODEL_DIR = "model"
MODEL_PATH = os.path.join(MODEL_DIR, "fruit_disease_model.h5")
LABELS_PATH = os.path.join(MODEL_DIR, "fruit_class_labels.json")

# Hyperparameters
IMG_SIZE = (128, 128)
BATCH_SIZE = 32 # Larger batch size for bigger dataset
EPOCHS = 4

def main():
    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)

    # 1. Data Generators
    print("[INFO] Loading dataset...")
    datagen = ImageDataGenerator(
        rescale=1./255,
        validation_split=0.2, # 20% for validation
        rotation_range=20,
        zoom_range=0.15,
        horizontal_flip=True,
    )

    train_generator = datagen.flow_from_directory(
        DATA_DIR,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='training'
    )

    val_generator = datagen.flow_from_directory(
        DATA_DIR,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='validation'
    )

    # Save class labels
    class_indices = train_generator.class_indices
    labels = {v: k for k, v in class_indices.items()}
    with open(LABELS_PATH, "w") as f:
        json.dump(labels, f)
    print(f"[INFO] Saved {len(labels)} class labels to {LABELS_PATH}")

    # 2. Build Model
    print("[INFO] Building MobileNetV2 model...")
    base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(IMG_SIZE[0], IMG_SIZE[1], 3))
    base_model.trainable = False # Freeze base model initially

    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(128, activation='relu')(x)
    x = Dropout(0.3)(x)
    predictions = Dense(len(labels), activation='softmax')(x)

    model = Model(inputs=base_model.input, outputs=predictions)
    
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    # 3. Train Model
    print("[INFO] Starting training...")
    early_stop = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)

    history = model.fit(
        train_generator,
        validation_data=val_generator,
        epochs=EPOCHS,
        callbacks=[early_stop]
    )

    # 4. Save Model
    print("[INFO] Saving model...")
    model.save(MODEL_PATH)
    print(f"[INFO] Model saved to {MODEL_PATH}")

    # 5. Plot History
    plt.figure(figsize=(10, 4))
    plt.subplot(1, 2, 1)
    plt.plot(history.history['accuracy'], label='Train Acc')
    plt.plot(history.history['val_accuracy'], label='Val Acc')
    plt.legend()
    plt.title('Accuracy')

    plt.subplot(1, 2, 2)
    plt.plot(history.history['loss'], label='Train Loss')
    plt.plot(history.history['val_loss'], label='Val Loss')
    plt.legend()
    plt.title('Loss')
    
    plt.savefig(os.path.join(MODEL_DIR, "fruit_training_history.png"))
    print("[INFO] Training complete!")

if __name__ == "__main__":
    main()
