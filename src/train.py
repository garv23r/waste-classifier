import tensorflow as tf
import numpy as np
import json
from tensorflow.keras import layers, models
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from sklearn.utils.class_weight import compute_class_weight

DATASET_DIR = "dataset"
MODEL_PATH = "models/waste_classifier.h5"
CLASS_NAMES_PATH = "class_names.json"

IMAGE_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 20
FINE_TUNE_EPOCHS = 15
SEED = 42

# ---------------- LOAD DATA ---------------- #

train_ds = tf.keras.utils.image_dataset_from_directory(
    DATASET_DIR,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    validation_split=0.2,
    subset="training",
    seed=SEED
)

val_ds = tf.keras.utils.image_dataset_from_directory(
    DATASET_DIR,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    validation_split=0.2,
    subset="validation",
    seed=SEED
)

class_names = train_ds.class_names
num_classes = len(class_names)

print(f"📦 Classes ({num_classes}): {class_names}")

# Save class order ONCE
with open(CLASS_NAMES_PATH, "w") as f:
    json.dump(class_names, f)

data_augmentation = tf.keras.Sequential([
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.1),
    layers.RandomZoom(0.1),
    layers.RandomContrast(0.1),
])

# ---------------- PREPROCESS ---------------- #

train_ds = train_ds.map(
    lambda x, y: (preprocess_input(data_augmentation(x)), y),
    num_parallel_calls=tf.data.AUTOTUNE
)

val_ds = val_ds.map(
    lambda x, y: (preprocess_input(x), y),
    num_parallel_calls=tf.data.AUTOTUNE
)

train_ds = train_ds.prefetch(tf.data.AUTOTUNE)
val_ds = val_ds.prefetch(tf.data.AUTOTUNE)

# ---------------- CLASS WEIGHTS ---------------- #

raw_train_ds = tf.keras.utils.image_dataset_from_directory(
    DATASET_DIR,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    validation_split=0.2,
    subset="training",
    seed=SEED
)

y_train = np.concatenate([y.numpy() for _, y in train_ds])


class_weights = compute_class_weight(
    class_weight="balanced",
    classes=np.unique(y_train),
    y=y_train
)

class_weights = dict(enumerate(class_weights))
print("⚖️ Class Weights:", class_weights)

# ---------------- MODEL ---------------- #

base_model = tf.keras.applications.MobileNetV2(
    input_shape=(*IMAGE_SIZE, 3),
    include_top=False,
    weights="imagenet"
)

base_model.trainable = False

model = models.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.BatchNormalization(),
    layers.Dense(256, activation="relu"),
    layers.Dropout(0.4),
    layers.Dense(num_classes, activation="softmax")
])

model.compile(
    optimizer=tf.keras.optimizers.Adam(1e-4),
    loss=tf.keras.losses.SparseCategoricalCrossentropy(),
    metrics=["accuracy"]
)

# ---------------- TRAIN (HEAD) ---------------- #

print("\n🚀 Training classifier head...\n")

history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=EPOCHS,
    class_weight=class_weights
)

# ---------------- FINE-TUNE ---------------- #

print("\n🔧 Fine-tuning backbone...\n")

base_model.trainable = True

# Freeze early layers (generic features)
for layer in base_model.layers[:100]:
    layer.trainable = False

model.compile(
    optimizer=tf.keras.optimizers.Adam(1e-5),
    loss=tf.keras.losses.SparseCategoricalCrossentropy(),
    metrics=["accuracy"]
)

history_fine = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=FINE_TUNE_EPOCHS,
    class_weight=class_weights
)


# ---------------- SAVE ---------------- #

model.save(MODEL_PATH)
print(f"\n✅ Model saved to {MODEL_PATH}")