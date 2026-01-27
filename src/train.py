import tensorflow as tf
from tensorflow.keras import layers, models
from sklearn.model_selection import train_test_split
from sklearn.utils.class_weight import compute_class_weight
import numpy as np
from data_loader import get_dataset

DATASET_DIR = "dataset"
MODEL_PATH = "models/waste_classifier.h5"
BATCH_SIZE = 16
IMAGE_SIZE = (224, 224)
EPOCHS = 10
FINE_TUNE_EPOCHS = 10

# ---------------- LOAD DATA ---------------- #
full_ds, class_names = get_dataset(DATASET_DIR, batch_size=BATCH_SIZE)
num_classes = len(class_names)

print(f"Classes: {class_names}")

# Split manually (80/20)
ds_size = len(full_ds.file_paths) if hasattr(full_ds, "file_paths") else None

# Instead of splitting manually, use image_dataset_from_directory with validation_split
train_ds = tf.keras.utils.image_dataset_from_directory(
    DATASET_DIR,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    validation_split=0.2,
    subset="training",
    seed=42
)

val_ds = tf.keras.utils.image_dataset_from_directory(
    DATASET_DIR,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    validation_split=0.2,
    subset="validation",
    seed=42
)

# Normalize
train_ds = train_ds.map(lambda x, y: (x / 255.0, y)).prefetch(tf.data.AUTOTUNE)
val_ds = val_ds.map(lambda x, y: (x / 255.0, y)).prefetch(tf.data.AUTOTUNE)

# Get labels from training dataset
y_train = np.concatenate([y.numpy() for _, y in train_ds])

class_weights = compute_class_weight(
    class_weight="balanced",
    classes=np.unique(y_train),
    y=y_train
)

class_weights = dict(enumerate(class_weights))
print("Class Weights:", class_weights)





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
    layers.Dense(128, activation="relu"),
    layers.Dropout(0.4),
    layers.Dense(num_classes, activation="softmax")
])

model.compile(
    optimizer=tf.keras.optimizers.Adam(1e-3),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

# Train
history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=EPOCHS,
    class_weight=class_weights
)


# Fine-tuning
base_model.trainable = True
for layer in base_model.layers[:100]:
    layer.trainable = False

model.compile(
    optimizer=tf.keras.optimizers.Adam(1e-5),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

history_fine = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=EPOCHS + FINE_TUNE_EPOCHS,
    initial_epoch=history.epoch[-1] + 1,
    class_weight=class_weights
)

# Save
model.save(MODEL_PATH)
print(f"Model saved to {MODEL_PATH}")