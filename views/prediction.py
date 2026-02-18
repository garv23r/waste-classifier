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
    # VALIDATION & INTEGRATED SARNIA BIN LOGIC
    # --------------------------------------------------
    st.markdown("---")
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown("### ✅ Validation")
        feedback = st.radio("Is this result accurate?", ["Perfect", "Incorrect"])
        
        if feedback == "Incorrect":
            # MATERIAL-BASED CATEGORIES (Sarnia Rules)
            material_categories = {
                "Paper": {
                    "items": ["newspaper", "magazines", "office_paper", "shredded_paper", "envelopes", "paper_bags"],
                    "help": "Clean and dry paper only."
                },
                "Cardboard": {
                    "items": ["corrugated_cardboard", "cereal_boxes", "detergent_boxes", "egg_cartons_paper", "shoe_boxes"],
                    "help": "Flatten all boxes."
                },
                "Plastic": {
                    "items": ["plastic_bottles", "margarine_tubs", "yogurt_cups", "shampoo_bottles", "clamshell_packaging"],
                    "help": "Rigid plastics #1-7 only."
                },
                "Metal/Glass": {
                    "items": ["aluminum_cans", "steel_tin_cans", "aluminum_foil", "glass_bottles", "glass_jars"],
                    "help": "Rinse containers thoroughly."
                },
                "Organics": {
                    "items": ["food_scraps", "meat_dairy_bones", "coffee_grounds", "soiled_paper_plates", "pizza_boxes_greasy"],
                    "help": "Items that belong in Sarnia's composting stream."
                },
                "Hazardous": {
                    "items": ["batteries", "light_bulbs", "paint_cans", "electronics", "chemicals"],
                    "help": "DO NOT put in regular bins. Requires special drop-off."
                },
                "Garbage": {
                    "items": ["styrofoam", "diapers", "plastic_wrappers", "pet_waste", "ceramics"],
                    "help": "Non-recyclable household waste."
                }
            }
            
            major_cat = st.selectbox("Select Material Type:", list(material_categories.keys()))
            st.caption(f"🏛️ {material_categories[major_cat]['help']}")
            final_class = st.selectbox(f"Identify the {major_cat} item:", material_categories[major_cat]["items"])
        else:
            final_class = predicted_class

        # --- MANUAL MAPPING LOGIC (Integrated) ---
        # This maps the chosen item to the Sarnia Bin System
        bin_map = {
            # Paper & Cardboard (Stream 1)
            "newspaper": "Blue Bin (Paper)", 
            "magazines": "Blue Bin (Paper)", 
            "office_paper": "Blue Bin (Paper)", 
            "shredded_paper": "Blue Bin (Paper)",
            "envelopes": "Blue Bin (Paper)", 
            "paper_bags": "Blue Bin (Paper)", 
            "paper_products": "Blue Bin (Paper)",
            "corrugated_cardboard": "Blue Bin (Cardboard)", 
            "cereal_boxes": "Blue Bin (Cardboard)", 
            "detergent_boxes": "Blue Bin (Cardboard)",
            "egg_cartons_paper": "Blue Bin (Cardboard)", 
            "shoe_boxes": "Blue Bin (Cardboard)",

            # Containers: Glass/Metal/Plastic (Stream 2)
            "plastic_bottles": "Blue Bin (Containers)", 
            "margarine_tubs": "Blue Bin (Containers)", 
            "yogurt_cups": "Blue Bin (Containers)",
            "shampoo_bottles": "Blue Bin (Containers)", 
            "clamshell_packaging": "Blue Bin (Containers)", 
            "aluminum_cans": "Blue Bin (Containers)",
            "steel_tin_cans": "Blue Bin (Containers)", 
            "aluminum_foil": "Blue Bin (Containers)", 
            "glass_bottles": "Blue Bin (Containers)",
            "glass_jars": "Blue Bin (Containers)", 
            "glass_containers": "Blue Bin (Containers)", 
            "cans_all_type": "Blue Bin (Containers)",

            # Organics
            "food_scraps": "Green Bin (Organics)", 
            "meat_dairy_bones": "Green Bin (Organics)", 
            "coffee_grounds": "Green Bin (Organics)",
            "soiled_paper_plates": "Green Bin (Organics)", 
            "pizza_boxes_greasy": "Green Bin (Organics)", 
            "yard_trimmings": "Green Bin (Organics)",
            "kitchen_waste": "Green Bin (Organics)", 
            "egg_shells": "Green Bin (Organics)", 
            "coffee_tea_bags": "Green Bin (Organics)",

            # Hazardous (Stay as Hazardous for safety)
            "batteries": "HAZARDOUS", "light_bulbs": "HAZARDOUS", "paint_cans": "HAZARDOUS",
            "electronics": "HAZARDOUS", "chemicals": "HAZARDOUS", "e-waste": "HAZARDOUS",
            "paints": "HAZARDOUS", "pesticides": "HAZARDOUS",

            # Garbage
            "styrofoam": "Black Bag (Garbage)", 
            "stroform_product": "Black Bag (Garbage)",
            "diapers": "Black Bag (Garbage)", 
            "sanitary_napkin": "Black Bag (Garbage)",
            "plastic_wrappers": "Black Bag (Garbage)", 
            "platics_bags_wrappers": "Black Bag (Garbage)",
            "pet_waste": "Black Bag (Garbage)", 
            "ceramics": "Black Bag (Garbage)", 
            "ceramic_product": "Black Bag (Garbage)"
        }

        suggested_bin = bin_map.get(final_class, "Check Sarnia Waste Wizard")

        # Dynamic Styling based on Bin Type
        border_color = "#ef4444" if suggested_bin == "HAZARDOUS" else "#4ade80"
        bg_color = "rgba(239, 68, 68, 0.1)" if suggested_bin == "HAZARDOUS" else "rgba(74, 222, 128, 0.1)"

        st.markdown(f"""
            <div style="background: {bg_color}; padding: 20px; border-radius: 15px; border-left: 10px solid {border_color}; margin-top: 15px;">
                <p style="margin: 0; color: #cbd5e1; font-size: 0.9rem;">Recommended Disposal:</p>
                <h2 style="margin: 0; color: white; letter-spacing: 1px;">{suggested_bin}</h2>
            </div>
        """, unsafe_allow_html=True)
        
        if suggested_bin == "HAZARDOUS":
            st.warning("⚠️ **Safety First:** Take this to the Household Special Waste depot at 325 Gladwish Dr.")

    with c2:
        st.markdown("### 🗑️ Action")
        
        # Check if the material is dangerous
        is_hazardous = (suggested_bin == "HAZARDOUS")
        
        if is_hazardous:
            # Hide Donate/Sell for safety and force "Dispose Correctly"
            st.warning("🚨 **Safety Warning:** This material is hazardous. It cannot be donated or sold.")
            action_options = ["Dispose Correctly"]
        else:
            action_options = ["Dispose Correctly", "Donate/Sell"]

        action = st.radio("What will you do?", action_options)
        
        if action == "Dispose Correctly":
            if is_hazardous:
                st.info("📍 **Requirement:** Take this to the Sarnia Household Hazardous Waste Depot at 325 Gladwish Dr.")
                
            else:
                st.info("👏 Thank You for Responsible Waste Disposal!")

        if action == "Donate/Sell":
            st.info("💡 **Next Step:** Head over to the **'Donate/Sell'** tab to view local partners!")

        # Final submission button
        if st.button("Complete Task", use_container_width=True):
            # Higher points for Hazardous disposal because it requires a special trip!
            if is_hazardous:
                pts = 15 
            else:
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