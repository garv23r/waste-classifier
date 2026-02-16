import streamlit as st
import numpy as np
from PIL import Image
import tensorflow as tf
import json
import time
from utils.preprocessing import preprocess_image
from utils.bin_rules import CLASS_TO_BIN

# --------------------------------------------------
# CONFIGURATION & CSS
# --------------------------------------------------
MODEL_PATH = "models/waste_classifier.h5"
CLASS_NAMES_PATH = "class_names.json"
CONFIDENCE_THRESHOLD = 0.65

def apply_prediction_styles():
    st.markdown("""
        <style>
        .stApp {
            background-image: url("https://images.unsplash.com/photo-1532996122724-e3c354a0b15b?q=80&w=2070&auto=format&fit=crop");
            background-size: cover;
            background-attachment: fixed;
            filter: brightness(83%);
        }
        .stApp::before {
            content: ""; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0, 0, 0, 0.7); z-index: -1;
        }
        .prediction-card {
            background: rgba(15, 23, 42, 0.8);
            padding: 25px;
            border-radius: 20px;
            border: 1px solid rgba(74, 222, 128, 0.3);
            margin-top: 20px;
        }
        .points-badge {
            background: linear-gradient(135deg, #f59e0b, #d97706);
            color: white;
            padding: 10px 20px;
            border-radius: 50px;
            font-weight: bold;
            display: inline-block;
            box-shadow: 0 4px 15px rgba(245, 158, 11, 0.3);
        }
        .bin-indicator {
            font-size: 1.5rem;
            font-weight: 800;
            color: #4ade80;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        </style>
    """, unsafe_allow_html=True)

# --------------------------------------------------
# MODEL LOADING (CACHED)
# --------------------------------------------------
@st.cache_resource
def load_model():
    return tf.keras.models.load_model(MODEL_PATH)

@st.cache_data
def load_class_names():
    with open(CLASS_NAMES_PATH, "r") as f:
        return json.load(f)

# PREDICT PAGE
# --------------------------------------------------
def predict_page():
    # 1. Initialize Session State
    if 'points' not in st.session_state:
        st.session_state.points = 0
    if 'last_uploaded_file' not in st.session_state:
        st.session_state.last_uploaded_file = None
    if 'prediction_results' not in st.session_state:
        st.session_state.prediction_results = None

    apply_prediction_styles()
    
    # Header Section
    col_title, col_points = st.columns([3, 1])
    with col_title:
        st.title("♻️ EcoVision AI")
        st.caption("Precision Waste Identification & Sorting")
    with col_points:
        st.markdown(f"<div style='text-align:right;'><span class='points-badge'>⭐ {st.session_state.points} pts</span></div>", unsafe_allow_html=True)

    # --------------------------------------------------
    # INPUT AREA
    # --------------------------------------------------
    with st.container():
        st.markdown('<div class="prediction-card">', unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Drop an image of your waste item here...", type=["jpg", "jpeg", "png"])
        
        if not uploaded_file:
            st.info("📸 Awaiting image upload to begin analysis.")
            st.session_state.last_uploaded_file = None
            st.session_state.prediction_results = None
            st.markdown('</div>', unsafe_allow_html=True)
            return

        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption="Current Scan", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # --------------------------------------------------
    # ANALYSIS ENGINE (Fixed: Bar only shows on new upload)
    # --------------------------------------------------
    if uploaded_file.name != st.session_state.last_uploaded_file:
        progress_text = "Analyzing material composition..."
        scanning_bar = st.progress(0, text=progress_text)

        # Load resources and predict
        model = load_model()
        CLASS_NAMES = load_class_names()
        processed = preprocess_image(image)
        preds = model.predict(processed, verbose=0)[0]

        # Simulation for visual effect
        for percent_complete in range(100):
            time.sleep(0.01) 
            scanning_bar.progress(percent_complete + 1, text=progress_text)
        
        scanning_bar.empty()

        # Save results to session state to prevent reload on interaction
        top_indices = np.argsort(preds)[::-1]
        st.session_state.prediction_results = {
            'top1_class': CLASS_NAMES[top_indices[0]],
            'top1_conf': float(preds[top_indices[0]]),
            'top2_class': CLASS_NAMES[top_indices[1]],
            'top2_conf': float(preds[top_indices[1]])
        }
        st.session_state.last_uploaded_file = uploaded_file.name

    # Use stored results
    res = st.session_state.prediction_results
    st.markdown("### 🧠 AI Analysis")
    
    if res['top1_conf'] >= CONFIDENCE_THRESHOLD:
        st.success(f"**Target Identified:** {res['top1_class']} ({res['top1_conf']*100:.1f}%)")
        predicted_class = res['top1_class']
    else:
        st.warning("⚠️ **Ambiguous Item:** The AI is seeing multiple possibilities.")
        choice = st.radio(
            "Which of these looks correct?",
            [f"{res['top1_class']} ({res['top1_conf']*100:.1f}%)", f"{res['top2_class']} ({res['top2_conf']*100:.1f}%)"]
        )
        predicted_class = res['top1_class'] if choice.startswith(res['top1_class']) else res['top2_class']

    # --------------------------------------------------
    # VALIDATION & DYNAMIC BIN LOGIC
    # --------------------------------------------------
    st.markdown("---")
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown("### ✅ Validation")
        feedback = st.radio("Is this result accurate?", ["Perfect", "Incorrect"])
        
        if feedback == "Incorrect":
            # TIERED CATEGORIES
            major_categories = {
                "Plastic/Metal/Glass": ["plastic_bottles", "glass_containers", "paper_products", "cans_all_type"],
                "Organic/Food": ["food_scraps", "egg_shells", "coffee_tea_bags", "yard_trimmings", "kitchen_waste"],
                "General Garbage": ["stroform_product", "diapers", "sanitary_napkin", "ceramic_product", "platics_bags_wrappers"],
                "Hazardous": ["batteries", "e-waste", "paints", "pesticides"]
            }
            
            major_cat = st.selectbox("Select Major Category:", list(major_categories.keys()))
            final_class = st.selectbox(f"Correct {major_cat} type:", major_categories[major_cat])
        else:
            final_class = predicted_class

        # Logic to determine bin based on your dictionary
        suggested_bin = CLASS_TO_BIN.get(final_class, "Manual Check (Consult Local Guidelines)")

        st.markdown(f"""
            <div class="prediction-card" style="text-align: center; border-left: 8px solid #4ade80; padding: 15px;">
                <p style="margin-bottom: 0; color: #94a3b8; font-size: 0.8rem;">Dispose of this item in:</p>
                <div class="bin-indicator" style="font-size: 1.2rem;">{suggested_bin}</div>
            </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("### 🗑️ Action")
        action = st.radio("What will you do?", ["Dispose Correctly", "Donate/Sell"])
        
        if action == "Dispose Correctly":
            st.info("👏 Thank You for Responsible Waste Disposal!")

        if action == "Donate/Sell":
            st.info("💡 **Next Step:** Head over to the **'Donate/Sell'** tab to view local partners!")

        if st.button("Complete Task", use_container_width=True):
            pts = 10 if action == "Donate/Sell" else 5
            st.session_state.points += pts
            st.balloons()
            st.success(f"Excellent! +{pts} points added to your profile.")
            time.sleep(1)
            st.rerun()

    # --------------------------------------------------
    # LOGIC EXPLANATION (IMAGE ADDED)
    # --------------------------------------------------
    st.markdown("---")
    with st.expander("🔍 How the Prediction Engine Works"):
        st.write("""
        EcoVision uses a Convolutional Neural Network (CNN) to break down your image into 
        mathematical patterns (edges, colors, textures).
        """)
        
        st.write("""
        1. **Feature Extraction:** AI looks for labels or material textures.
        2. **Probability Mapping:** The model weighs 18 categories against your image.
        3. **Rule Application:** We map the result to Sarnia's local bin guidelines.
        """)