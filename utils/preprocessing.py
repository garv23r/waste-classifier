import streamlit as st
import tensorflow as tf
import numpy as np
import json
from PIL import Image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from math import radians, cos, sin, asin, sqrt

# --------------------------------------------------
# Image Preprocessing
# --------------------------------------------------
def preprocess_image(image: Image.Image):
    image = image.convert("RGB")
    image = image.resize((224, 224))
    img = np.array(image)
    img = preprocess_input(img)
    return np.expand_dims(img, axis=0)