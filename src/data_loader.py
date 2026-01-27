import tensorflow as tf
import os

IMAGE_SIZE = (224, 224)

def load_and_preprocess_image(path, label):
    img = tf.io.read_file(path)
    img = tf.image.decode_png(img, channels=3)
    img = tf.image.resize(img, IMAGE_SIZE)
    img = img / 255.0
    return img, label

def get_dataset(dataset_dir, batch_size=16, shuffle=True, seed=42):
    """
    Loads dataset from folder structure:
    dataset/
        Plastic/
        Metal/
        Glass/
        Paper_Cardboard/
        Organic/
        Textile/
        Other/
    """

    ds = tf.keras.utils.image_dataset_from_directory(
        dataset_dir,
        image_size=IMAGE_SIZE,
        batch_size=batch_size,
        shuffle=shuffle,
        seed=seed
    )
    class_names = ds.class_names

    # Optional: normalize
    ds = ds.map(lambda x, y: (x / 255.0, y), num_parallel_calls=tf.data.AUTOTUNE)
    ds = ds.prefetch(tf.data.AUTOTUNE)

    return ds, class_names