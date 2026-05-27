"""
AgriShield AI - Fast Model Training Script
Uses a subset of PlantVillage data + smaller model for fast CPU training.
"""

import os
import json
import shutil
import random
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
IMG_SIZE = 128
BATCH_SIZE = 32
EPOCHS = 10
LEARNING_RATE = 0.001
IMAGES_PER_CLASS = 500  # Use 500 images per class for better accuracy
MODEL_DIR = os.path.join(os.path.dirname(__file__), "model")
MODEL_PATH = os.path.join(MODEL_DIR, "plant_disease_model.h5")
LABELS_PATH = os.path.join(MODEL_DIR, "class_labels.json")
PLOT_PATH = os.path.join(MODEL_DIR, "training_history.png")
SUBSET_DIR = "C:\\venv\\dataset_subset"

# Full dataset location (cached by kagglehub)
KAGGLE_CACHE = os.path.join(
    os.path.expanduser("~"), ".cache", "kagglehub", "datasets",
    "abdallahalidev", "plantvillage-dataset", "versions", "3",
    "plantvillage dataset", "color"
)


def find_dataset():
    """Find the downloaded PlantVillage dataset."""
    print("=" * 60)
    print("STEP 1: Locating Dataset")
    print("=" * 60)

    if os.path.exists(KAGGLE_CACHE):
        print(f"Found dataset at: {KAGGLE_CACHE}")
        return KAGGLE_CACHE

    # Search common locations
    for root_path in [os.path.expanduser("~/.cache/kagglehub")]:
        for root, dirs, files in os.walk(root_path):
            if "color" in dirs:
                path = os.path.join(root, "color")
                print(f"Found dataset at: {path}")
                return path

    raise RuntimeError("Dataset not found! Please re-run the download.")


def create_subset(source_dir):
    """Create a smaller subset of the dataset for fast training."""
    print("\n" + "=" * 60)
    print(f"STEP 2: Creating Subset ({IMAGES_PER_CLASS} images/class)")
    print("=" * 60)

    if os.path.exists(SUBSET_DIR):
        # Check if subset already has data
        existing_classes = [d for d in os.listdir(SUBSET_DIR) 
                          if os.path.isdir(os.path.join(SUBSET_DIR, d))]
        if len(existing_classes) > 30:
            print(f"Subset already exists with {len(existing_classes)} classes")
            return SUBSET_DIR
        shutil.rmtree(SUBSET_DIR)

    os.makedirs(SUBSET_DIR, exist_ok=True)

    classes = sorted([d for d in os.listdir(source_dir) 
                     if os.path.isdir(os.path.join(source_dir, d))])
    
    total_copied = 0
    for cls_name in classes:
        src_cls = os.path.join(source_dir, cls_name)
        dst_cls = os.path.join(SUBSET_DIR, cls_name)
        os.makedirs(dst_cls, exist_ok=True)

        images = [f for f in os.listdir(src_cls) 
                 if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
        
        # Take a random subset
        selected = random.sample(images, min(IMAGES_PER_CLASS, len(images)))
        
        for img_name in selected:
            shutil.copy2(os.path.join(src_cls, img_name), 
                        os.path.join(dst_cls, img_name))
        
        total_copied += len(selected)
        print(f"  {cls_name}: {len(selected)} images")

    print(f"\nTotal: {total_copied} images across {len(classes)} classes")
    return SUBSET_DIR


def create_data_generators(data_dir):
    """Create training and validation data generators."""
    print("\n" + "=" * 60)
    print("STEP 3: Preparing Data Generators")
    print("=" * 60)

    train_datagen = ImageDataGenerator(
        rescale=1.0 / 255,
        rotation_range=20,
        width_shift_range=0.15,
        height_shift_range=0.15,
        zoom_range=0.15,
        horizontal_flip=True,
        validation_split=0.2,
    )

    val_datagen = ImageDataGenerator(
        rescale=1.0 / 255,
        validation_split=0.2,
    )

    train_gen = train_datagen.flow_from_directory(
        data_dir,
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode="categorical",
        subset="training",
        shuffle=True,
    )

    val_gen = val_datagen.flow_from_directory(
        data_dir,
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode="categorical",
        subset="validation",
        shuffle=False,
    )

    num_classes = len(train_gen.class_indices)
    print(f"Training images: {train_gen.samples}")
    print(f"Validation images: {val_gen.samples}")
    print(f"Classes: {num_classes}")

    return train_gen, val_gen, num_classes


def build_model(num_classes):
    """Build MobileNetV2 transfer learning model."""
    print("\n" + "=" * 60)
    print("STEP 4: Building MobileNetV2 Model")
    print("=" * 60)

    base_model = MobileNetV2(
        weights="imagenet",
        include_top=False,
        input_shape=(IMG_SIZE, IMG_SIZE, 3),
    )

    base_model.trainable = False

    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dropout(0.3)(x)
    x = Dense(128, activation="relu")(x)
    x = Dropout(0.2)(x)
    predictions = Dense(num_classes, activation="softmax")(x)

    model = Model(inputs=base_model.input, outputs=predictions)

    model.compile(
        optimizer=Adam(learning_rate=LEARNING_RATE),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )

    trainable = sum(tf.keras.backend.count_params(w) for w in model.trainable_weights)
    print(f"Total parameters: {model.count_params():,}")
    print(f"Trainable parameters: {trainable:,}")

    return model


def train_model(model, train_gen, val_gen):
    """Train the model."""
    print("\n" + "=" * 60)
    print("STEP 5: Training Model")
    print("=" * 60)

    callbacks = [
        EarlyStopping(
            monitor="val_loss",
            patience=2,
            restore_best_weights=True,
            verbose=1,
        ),
    ]

    history = model.fit(
        train_gen,
        epochs=EPOCHS,
        validation_data=val_gen,
        callbacks=callbacks,
        verbose=1,
    )

    return history


def save_model_and_labels(model, class_indices):
    """Save trained model and class label mapping."""
    print("\n" + "=" * 60)
    print("STEP 6: Saving Model and Labels")
    print("=" * 60)

    os.makedirs(MODEL_DIR, exist_ok=True)

    model.save(MODEL_PATH)
    print(f"Model saved to: {MODEL_PATH}")

    labels = {str(v): k for k, v in class_indices.items()}
    with open(LABELS_PATH, "w") as f:
        json.dump(labels, f, indent=2)
    print(f"Class labels saved to: {LABELS_PATH}")


def plot_history(history):
    """Save training plots."""
    print("\n" + "=" * 60)
    print("STEP 7: Saving Training Plots")
    print("=" * 60)

    os.makedirs(MODEL_DIR, exist_ok=True)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

    ax1.plot(history.history["accuracy"], label="Train", linewidth=2)
    ax1.plot(history.history["val_accuracy"], label="Val", linewidth=2)
    ax1.set_title("Accuracy")
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    ax2.plot(history.history["loss"], label="Train", linewidth=2)
    ax2.plot(history.history["val_loss"], label="Val", linewidth=2)
    ax2.set_title("Loss")
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(PLOT_PATH, dpi=150)
    print(f"Plot saved to: {PLOT_PATH}")
    plt.close()


def main():
    print("=" * 60)
    print("  AgriShield AI - Fast Model Training")
    print("  MobileNetV2 + PlantVillage Subset")
    print("=" * 60)
    print()

    random.seed(42)

    # Step 1: Find dataset
    source_dir = find_dataset()

    # Step 2: Create subset
    data_dir = create_subset(source_dir)

    # Step 3: Data generators
    train_gen, val_gen, num_classes = create_data_generators(data_dir)

    # Step 4: Build model
    model = build_model(num_classes)

    # Step 5: Train
    history = train_model(model, train_gen, val_gen)

    # Step 6: Save
    save_model_and_labels(model, train_gen.class_indices)

    # Step 7: Plot
    plot_history(history)

    # Summary
    train_acc = history.history["accuracy"][-1]
    val_acc = history.history["val_accuracy"][-1]

    print("\n" + "=" * 60)
    print("TRAINING COMPLETE!")
    print("=" * 60)
    print(f"Training Accuracy:   {train_acc*100:.1f}%")
    print(f"Validation Accuracy: {val_acc*100:.1f}%")
    print(f"Model: {MODEL_PATH}")
    print(f"Labels: {LABELS_PATH}")
    print("\nRun 'python app.py' to start the web application.")


if __name__ == "__main__":
    main()
