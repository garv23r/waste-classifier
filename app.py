import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from math import radians, cos, sin, asin, sqrt

# --------------------------------------------------
# Streamlit App Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Smart Waste Classification System",
    page_icon="♻️",
    layout="centered"
)

st.title("♻️ Smart Waste Classification System")
st.write(
    "Upload an image of household waste to identify its category, "
    "get correct disposal guidance, and earn rewards for sustainable actions."
)

# --------------------------------------------------
# Load Trained Model
# --------------------------------------------------
@st.cache_resource
def load_model():
    return tf.keras.models.load_model("models/waste_classifier.h5")

model = load_model()

# --------------------------------------------------
# Class Names
# --------------------------------------------------
CLASS_NAMES = [
    "Plastic",
    "Paper_Cardboard",
    "Glass",
    "Metal",
    "Organic",
    "Textile",
    "Other"
]

# --------------------------------------------------
# Disposal Rules
# --------------------------------------------------
DISPOSAL_RULES = {
    "Plastic": {"bin": "Blue Bin (Recycling)"},
    "Paper_Cardboard": {"bin": "Blue Bin (Recycling)"},
    "Glass": {"bin": "Blue Bin (Recycling)"},
    "Metal": {"bin": "Blue Bin (Recycling)"},
    "Organic": {"bin": "Green Bin (Compost)"},
    "Textile": {"bin": "Donate / Black Bin"},
    "Other": {"bin": "Black Bin (Garbage)"}
}

# --------------------------------------------------
# Donation Points (Only if DONATED)
# --------------------------------------------------
DONATION_POINTS = {
    "Textile": 20,
    "Plastic": 10,
    "Paper_Cardboard": 10,
    "Glass": 5,
    "Metal": 5,
    "Organic": 3,
    "Other": 2
}

# --------------------------------------------------
# Badge System
# --------------------------------------------------
BADGES = {
    50: "🌱 Green Starter",
    100: "♻️ Eco Warrior",
    200: "🏆 Sustainability Champion"
}

# --------------------------------------------------
# Hypothetical Postal Codes (Sarnia)
# --------------------------------------------------
POSTAL_CODES = {
    "N7T 7H5": (42.9746, -82.4066),
    "N7S 5A1": (42.9981, -82.3700),
    "N7V 1B2": (42.9563, -82.3849),
    "N7M 6K8": (42.9801, -82.3582)
}

# --------------------------------------------------
# Hypothetical Disposal Locations
# --------------------------------------------------
DISPOSAL_LOCATIONS = [
    {"name": "Sarnia Recycling Depot", "lat": 42.9850, "lon": -82.4050},
    {"name": "North Compost Facility", "lat": 43.0102, "lon": -82.3754},
    {"name": "Textile Donation Hub", "lat": 42.9701, "lon": -82.3902},
    {"name": "Waste Transfer Station", "lat": 42.9555, "lon": -82.4201},
    {"name": "Community Eco Center", "lat": 42.9903, "lon": -82.3609},
]

# --------------------------------------------------
# Session State
# --------------------------------------------------
if "points" not in st.session_state:
    st.session_state.points = 0

if "earned_badges" not in st.session_state:
    st.session_state.earned_badges = []

# --------------------------------------------------
# Helper Functions
# --------------------------------------------------
def preprocess_image(image: Image.Image):
    image = image.convert("RGB")
    image = image.resize((224, 224))
    img_array = np.array(image)
    img_array = preprocess_input(img_array)
    return np.expand_dims(img_array, axis=0)

def calculate_distance(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    return 6371 * 2 * asin(sqrt(a))

# --------------------------------------------------
# File Upload
# --------------------------------------------------
uploaded_file = st.file_uploader(
    "Upload an image (JPG, JPEG, PNG)",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    processed_image = preprocess_image(image)
    predictions = model.predict(processed_image)

    predicted_index = np.argmax(predictions[0])
    predicted_class = CLASS_NAMES[predicted_index]
    confidence = float(predictions[0][predicted_index])

    rule = DISPOSAL_RULES[predicted_class]

    # --------------------------------------------------
    # Prediction Result
    # --------------------------------------------------
    st.markdown("---")
    st.subheader("🧠 Prediction Result")

    st.markdown(
        f"""
        **Predicted Category:** `{predicted_class}`  
        **Confidence:** `{confidence * 100:.2f}%`  
        **Suggested Disposal:** `{rule['bin']}`
        """
    )
    st.progress(confidence)

    # --------------------------------------------------
    # Donate or Throw Decision
    # --------------------------------------------------
    st.markdown("---")
    st.subheader("🤝 What would you like to do?")

    user_action = st.radio(
        "Choose one option:",
        ["Donate / Reuse", "Throw Away"]
    )

    if user_action == "Donate / Reuse":
        earned = DONATION_POINTS[predicted_class]
        st.session_state.points += earned

        st.success(f"🎉 You earned **{earned} points** for donating!")

        # Badge Check
        for threshold, badge in BADGES.items():
            if (
                st.session_state.points >= threshold
                and badge not in st.session_state.earned_badges
            ):
                st.session_state.earned_badges.append(badge)
                st.balloons()
                st.success(f"🏅 New Badge Unlocked: **{badge}**")

    else:
        st.info("Thanks for disposing responsibly 👍 No points awarded.")

    # --------------------------------------------------
    # Postal Code Selection
    # --------------------------------------------------
    st.markdown("---")
    st.subheader("📍 Select Your Postal Code")

    selected_postal = st.selectbox(
        "Choose your Sarnia postal code:",
        list(POSTAL_CODES.keys())
    )

    user_lat, user_lon = POSTAL_CODES[selected_postal]

    # --------------------------------------------------
    # Nearest Locations
    # --------------------------------------------------
    for loc in DISPOSAL_LOCATIONS:
        loc["distance"] = calculate_distance(
            user_lat, user_lon, loc["lat"], loc["lon"]
        )

    nearest = sorted(DISPOSAL_LOCATIONS, key=lambda x: x["distance"])[:5]

    st.markdown("---")
    st.subheader("📍 Nearest Disposal / Donation Locations")

    for loc in nearest:
        st.markdown(f"**{loc['name']}** — {loc['distance']:.2f} km away")

    # --------------------------------------------------
    # User Progress
    # --------------------------------------------------
    st.markdown("---")
    st.subheader("⭐ Your Sustainability Progress")

    st.metric("Total Points", st.session_state.points)

    if st.session_state.earned_badges:
        st.markdown("**🏅 Badges Earned:**")
        for badge in st.session_state.earned_badges:
            st.markdown(f"- {badge}")
    else:
        st.info("No badges yet — keep donating! 🌱")

    # --------------------------------------------------
    # Future Vision
    # --------------------------------------------------
    st.markdown("---")
    st.subheader("🚀 Future Possibilities")

    st.markdown("""
    - 🎁 Redeem points for garbage or compost bags  
    - 📦 TerraCycle-style donation partnerships  
    - 📱 Mobile app with QR-based donations  
    - 🌍 City-wide sustainability leaderboard  
    """)

else:
    st.info("👆 Upload a waste image to start classification.")
