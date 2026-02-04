import streamlit as st
import pandas as pd
import math

# --------------------------------------------------
# SESSION STATE (POINTS SAFETY)
# --------------------------------------------------
if "points" not in st.session_state:
    st.session_state.points = 0

POINTS_DONATE = 10

# --------------------------------------------------
# SAMPLE DATASET (PLACEHOLDER)
# We can later replace this with CSV / DB
# --------------------------------------------------
DONATION_DATA = [
    {
        "name": "Goodwill Sarnia",
        "type": "Donation",
        "category": "Clothing / Household",
        "address": "1362 Lambton Mall Rd, Sarnia",
        "lat": 42.9747,
        "lon": -82.4066,
        "url": "https://www.goodwillindustries.ca"
    },
    {
        "name": "Salvation Army Thrift Store",
        "type": "Donation",
        "category": "Clothing / Furniture",
        "address": "800 Exmouth St, Sarnia",
        "lat": 42.9972,
        "lon": -82.4034,
        "url": "https://www.salvationarmy.ca"
    },
    {
        "name": "Value Village",
        "type": "Resale",
        "category": "Clothing / Small Items",
        "address": "1362 Lambton Mall Rd, Sarnia",
        "lat": 42.9749,
        "lon": -82.4068,
        "url": "https://www.valuevillage.com"
    },
    {
        "name": "Facebook Marketplace",
        "type": "Resale (Online)",
        "category": "General Items",
        "address": "Online",
        "lat": None,
        "lon": None,
        "url": "https://www.facebook.com/marketplace"
    },
    {
        "name": "Kijiji",
        "type": "Resale (Online)",
        "category": "General Items",
        "address": "Online",
        "lat": None,
        "lon": None,
        "url": "https://www.kijiji.ca"
    }
]

# --------------------------------------------------
# DISTANCE CALCULATION (OPTIONAL – FUTURE USE)
# --------------------------------------------------

def haversine(lat1, lon1, lat2, lon2):
    """Calculate distance between two lat/lon points (km)."""
    if None in [lat1, lon1, lat2, lon2]:
        return None

    R = 6371  # Earth radius (km)
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    return R * c

# --------------------------------------------------
# PAGE FUNCTION
# --------------------------------------------------

def donate_sell_page():
    st.title("🤝 Donate / Sell Your Item")
    st.caption("Give waste a second life and earn EcoVision points")

    st.info(
        "Donating or reselling items reduces landfill waste, "
        "saves resources, and supports the local community."
    )

    # --------------------------------------------------
    # LOCATION SELECTION
    # --------------------------------------------------
    location = st.selectbox(
        "Select your location",
        ["Sarnia, Ontario"],
        index=0
    )

    st.markdown("---")
    st.subheader("📍 Recommended Donation & Resale Options")

    df = pd.DataFrame(DONATION_DATA)

    # Display top 5 places (static for now)
    for _, row in df.head(5).iterrows():
        with st.container():
            st.markdown(f"### {row['name']}")
            st.markdown(f"**Type:** {row['type']}")
            st.markdown(f"**Accepts:** {row['category']}")
            st.markdown(f"**Address:** {row['address']}")
            st.markdown(f"[🌐 Visit Website]({row['url']})")
            st.divider()

    # --------------------------------------------------
    # CONFIRM DONATION / SALE
    # --------------------------------------------------
    st.subheader("✅ Confirm Your Action")

    if st.button("I donated / sold this item"):
        st.session_state.points += POINTS_DONATE
        st.success(f"🎉 Thank you! You earned {POINTS_DONATE} points.")
        st.info(f"⭐ Total Points: {st.session_state.points}")

    # --------------------------------------------------
    # FUTURE EXPANSION NOTE
    # --------------------------------------------------
    st.markdown("---")
    st.subheader("🚀 Coming Soon")

    st.markdown(
        """
        - Automatic location detection  
        - Distance-based sorting  
        - Item-specific donation matching  
        - Partner verification badges  
        - Impact tracking (CO₂ saved)
        """
    )
