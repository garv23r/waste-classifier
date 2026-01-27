import tensorflow as tf
from data_loader import get_dataset
from sklearn.metrics import classification_report
import numpy as np

DATASET_DIR = "dataset"
MODEL_PATH = "models/waste_classifier.h5"
BATCH_SIZE = 16

# Load model
model = tf.keras.models.load_model(MODEL_PATH)

# Load test dataset (no shuffle)
test_ds, class_names = get_dataset(DATASET_DIR, batch_size=BATCH_SIZE, shuffle=False)

# Predict
y_true, y_pred = [], []

for imgs, labels in test_ds:
    preds = model.predict(imgs, verbose=0)
    y_true.extend(labels.numpy())
    y_pred.extend(np.argmax(preds, axis=1))

print("\nClassification Report:\n")
print(classification_report(y_true, y_pred, target_names=class_names))