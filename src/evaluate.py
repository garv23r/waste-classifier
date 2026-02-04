import tensorflow as tf
import numpy as np
import json
from sklearn.metrics import classification_report, confusion_matrix
from data_loader import get_datasets

DATASET_DIR = "dataset"
MODEL_PATH = "models/waste_classifier.h5"
BATCH_SIZE = 32

# Load trained model
model = tf.keras.models.load_model(MODEL_PATH)

# Load validation dataset ONLY
_, val_ds, class_names = get_datasets(
    DATASET_DIR,
    batch_size=BATCH_SIZE
)

# Optional safety: load saved class names instead
# with open("class_names.json") as f:
#     class_names = json.load(f)

y_true = []
y_pred = []

for images, labels in val_ds:
    predictions = model.predict(images, verbose=0)
    y_true.extend(labels.numpy())
    y_pred.extend(np.argmax(predictions, axis=1))

print("\n📊 Classification Report\n")
print(classification_report(y_true, y_pred, target_names=class_names))

print("\n🧩 Confusion Matrix\n")
print(confusion_matrix(y_true, y_pred))