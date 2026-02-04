import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

IMAGE_SIZE = (224, 224)
DATASET_DIR = "dataset"
MODEL_PATH = "models/waste_classifier.h5"
CLASS_NAMES_PATH = "class_names.json"

IMAGE_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 20
FINE_TUNE_EPOCHS = 15
SEED = 42

def get_datasets(
    dataset_dir,
    batch_size=32,
    val_split=0.2,
    seed=42
):

    train_ds = tf.keras.utils.image_dataset_from_directory(
        DATASET_DIR,
        image_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        validation_split=0.2,
        subset="training",
        seed=SEED,
        label_mode="int"
    )

    val_ds = tf.keras.utils.image_dataset_from_directory(
        DATASET_DIR,
        image_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        validation_split=0.2,
        subset="validation",
        seed=SEED,
        label_mode="int"
    )


    class_names = train_ds.class_names

    # MobileNetV2 preprocessing
    train_ds = train_ds.map(
        lambda x, y: (preprocess_input(x), y),
        num_parallel_calls=tf.data.AUTOTUNE
    )

    val_ds = val_ds.map(
        lambda x, y: (preprocess_input(x), y),
        num_parallel_calls=tf.data.AUTOTUNE
    )

    # Performance optimizations
    train_ds = train_ds.shuffle(1024).prefetch(tf.data.AUTOTUNE)
    val_ds = val_ds.prefetch(tf.data.AUTOTUNE)

    return train_ds, val_ds, class_names