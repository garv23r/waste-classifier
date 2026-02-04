import streamlit as st
import numpy as np
from PIL import Image
import tensorflow as tf
import json

from utils.preprocessing import preprocess_image
from utils.bin_rules import CLASS_TO_BIN

# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------
MODEL_PATH = "models/waste_classifier.h5"
CLASS_NAMES_PATH = "class_names.json"

CONFIDENCE_THRESHOLD = 0.65
POINTS_THROW = 5
POINTS_DONATE = 10
POINTS_CORRECT_PRED = 5

# --------------------------------------------------
# INITIAL SESSION STATE
# --------------------------------------------------
if "points" not in st.session_state:
    st.session_state.points = 0

if "last_prediction" not in st.session_state:
    st.session_state.last_prediction = None

# --------------------------------------------------
# LOAD MODEL & METADATA (CACHED)
# --------------------------------------------------
@st.cache_resource

def load_model():
    return tf.keras.models.load_model(MODEL_PATH)

@st.cache_data

def load_class_names():
    with open(CLASS_NAMES_PATH, "r") as f:
        return json.load(f)

model = load_model()
CLASS_NAMES = load_class_names()

# --------------------------------------------------
# PAGE FUNCTION
# --------------------------------------------------

def predict_page():
    st.title("♻️ EcoVision – Smart Waste Prediction")
    st.caption("AI-powered waste classification with human verification")

    # Disclaimer
    st.warning(
        "⚠️ **Disclaimer:** This AI model is not 100% accurate. "
        "Predictions may be incorrect due to limited training data. "
        "Always verify before disposal."
    )

    # --------------------------------------------------
    # IMAGE UPLOAD
    # --------------------------------------------------
    uploaded_file = st.file_uploader(
        "Upload a waste image (JPG / PNG)",
        type=["jpg", "jpeg", "png"]
    )

    if not uploaded_file:
        st.info("👆 Upload a waste image to begin.")
        return

    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_container_width=True)

    # --------------------------------------------------
    # MODEL PREDICTION
    # --------------------------------------------------
    processed = preprocess_image(image)
    preds = model.predict(processed, verbose=0)[0]

    top_indices = np.argsort(preds)[::-1]
    top1_idx, top2_idx = top_indices[:2]

    top1_class = CLASS_NAMES[top1_idx]
    top2_class = CLASS_NAMES[top2_idx]

    top1_conf = float(preds[top1_idx])
    top2_conf = float(preds[top2_idx])

    st.markdown("---")
    st.subheader("🧠 AI Analysis")

    # --------------------------------------------------
    # CONFIDENCE HANDLING
    # --------------------------------------------------
    if top1_conf >= CONFIDENCE_THRESHOLD:
        predicted_class = top1_class
        st.success("✅ High confidence prediction")
        st.progress(top1_conf)
    else:
        st.warning("⚠️ Low confidence – please help confirm")

        choice = st.radio(
            "Which option best matches the image?",
            [
                f"{top1_class} ({top1_conf*100:.1f}%)",
                f"{top2_class} ({top2_conf*100:.1f}%)"
            ]
        )
        predicted_class = top1_class if choice.startswith(top1_class) else top2_class

    suggested_bin = CLASS_TO_BIN.get(predicted_class, "Manual Disposal Required")

    st.markdown(f"""
    **Detected Category:** `{predicted_class}`  
    **Confidence:** `{top1_conf*100:.2f}%`  
    **Recommended Bin (Sarnia, ON):** `{suggested_bin}`
    """)

    st.session_state.last_prediction = predicted_class

    # --------------------------------------------------
    # USER FEEDBACK LOOP
    # --------------------------------------------------
    st.markdown("---")
    st.subheader("✅ Was this prediction correct?")

    feedback = st.radio(
        "Confirm prediction",
        ["Yes, this is correct", "No, this is incorrect"]
    )

    final_class = predicted_class

    if feedback == "No, this is incorrect":
        final_class = st.selectbox(
            "Select the correct waste category",
            CLASS_NAMES
        )

        corrected_bin = CLASS_TO_BIN.get(final_class, "Manual Disposal Required")

        st.info(f"""
        **Correct Category:** `{final_class}`  
        **Correct Bin:** `{corrected_bin}`
        """)

    else:
        st.session_state.points += POINTS_CORRECT_PRED

    # --------------------------------------------------
    # ACTION SELECTION
    # --------------------------------------------------
    st.markdown("---")
    st.subheader("🗑️ What would you like to do with this item?")

    action = st.radio(
        "Choose an action",
        ["Throw it correctly", "Donate / Sell"]
    )

    if st.button("Confirm Action"):
        if action == "Throw it correctly":
            st.session_state.points += POINTS_THROW
            st.success(f"♻️ You earned {POINTS_THROW} points for proper disposal!")
        else:
            st.session_state.points += POINTS_DONATE
            st.success(f"🤝 You earned {POINTS_DONATE} points for donating / selling!")
            st.query_params(page="Donate / Sell")

        st.info(f"⭐ Total Points Earned: {st.session_state.points}")

    # --------------------------------------------------
    # EDUCATIONAL SECTION
    # --------------------------------------------------
    st.markdown("---")
    st.subheader("🔍 How EcoVision Makes Decisions")

    st.markdown(
        """
        - The AI predicts **material-based waste categories**  
        - High confidence → automatic recommendation  
        - Low confidence → **human-in-the-loop validation**  
        - Disposal rules are **explicit & local**, not guessed  

        This approach ensures **responsible, transparent waste sorting**.
        """
    )
