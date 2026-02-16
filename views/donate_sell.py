import streamlit as st
import pandas as pd
import math
import time
import os

# --------------------------------------------------
# STYLING
# --------------------------------------------------
def apply_donate_styles():
    st.markdown("""
        <style>
        .stApp {
            background-image: url("https://images.unsplash.com/photo-1497215728101-856f4ea42174?q=80&w=2070&auto=format&fit=crop");

            background-size: cover;

            background-attachment: fixed;

            filter: brightness(80%);
        }
        .stApp::before {
            content: ""; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0, 0, 0, 0.75); z-index: -1;
        }
        .location-card {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 15px;
            transition: transform 0.2s ease;
        }
        .location-card:hover {
            border-color: #f59e0b;
            transform: translateX(5px);
        }
        .dist-badge {
            background: rgba(245, 158, 11, 0.2);
            color: #f59e0b;
            padding: 2px 10px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: bold;
            float: right;
        }
        .note-text {
            color: #fbbf24;
            font-size: 0.85rem;
            font-style: italic;
            margin-top: 8px;
            display: block;
        }
        </style>
    """, unsafe_allow_html=True)

# --------------------------------------------------
# THE COMPLETE 18 SARNIA LOCATIONS
# --------------------------------------------------
DONATION_DATA = [
    # Donation Centres
    {"name": "Goodwill Donation Centre", "address": "1121 Wellington St", "lat": 42.9785, "lon": -82.3812, "cat": "Clothing & Household", "accepts": "Clothing, linens, books, and small appliances."},
    {"name": "Value Village Centre", "address": "1379 London Rd", "lat": 42.9812, "lon": -82.3654, "cat": "Clothing & Household", "accepts": "Clothing, shoes, and housewares."},
    {"name": "Goodwill Donation Centre (Michigan)", "address": "1307 Michigan Ave", "lat": 42.9930, "lon": -82.3550, "cat": "Clothing & Household", "accepts": "Gently used household goods."},
    {"name": "Goodwill Community Store", "address": "1307 Michigan Ave", "lat": 42.9931, "lon": -82.3551, "cat": "Clothing & Household", "accepts": "Used apparel and accessories."},
    {"name": "Habitat for Humanity Restore", "address": "1787 London Line", "lat": 42.9934, "lon": -82.3210, "cat": "Home Improvement", "accepts": "Building materials, appliances, and furniture."},
    {"name": "Mission Thrift Store", "address": "595 Murphy Rd", "lat": 42.9750, "lon": -82.3720, "cat": "Clothing & Household", "accepts": "Clothing, furniture, and used goods."},
    {"name": "Talize Sarnia Outlet", "address": "1330 Exmouth St", "lat": 42.9880, "lon": -82.3680, "cat": "Clothing & Household", "accepts": "Fashion and housewares."},
    
    # Bottle Returns
    {"name": "The Beer Store", "address": "1380 London Rd", "lat": 42.9810, "lon": -82.3660, "cat": "Bottle Returns", "accepts": "Beer, wine, and spirit containers.", "note": "⚠️ Must be 19+ to enter or return containers."},
    {"name": "The Beer Store", "address": "1107 Confederation St", "lat": 42.9610, "lon": -82.3880, "cat": "Bottle Returns", "accepts": "Beer, wine, and spirit containers.", "note": "⚠️ Must be 19+ to enter or return containers."},
    {"name": "The Beer Store", "address": "210 Maxwell St", "lat": 42.9780, "lon": -82.4010, "cat": "Bottle Returns", "accepts": "Beer, wine, and spirit containers.", "note": "⚠️ Must be 19+ to enter or return containers."},
    
    # Recycling Depots
    {"name": "Curran Recycling Ltd", "address": "526 McGregor Side Rd", "lat": 42.9320, "lon": -82.4150, "cat": "Recycling Depots", "accepts": "Scrap metal and recyclable containers."},
    {"name": "Transco Waste & Recycling", "address": "387 McGregor Side Rd", "lat": 42.9380, "lon": -82.4140, "cat": "Recycling Depots", "accepts": "Waste management and industrial recycling."},
    {"name": "Premier Recycling Sarnia", "address": "325 Gladwish Dr", "lat": 42.9650, "lon": -82.4180, "cat": "Recycling Depots", "accepts": "Metal recycling and containers."},

    # Churches
    {"name": "Salvation Army Community Church", "address": "970 Confederation St", "lat": 42.9612, "lon": -82.3890, "cat": "Churches", "accepts": "Clothing and household items.", "note": "⛪ Accepts clothing and household items only."},
    {"name": "River City Vineyard", "address": "260 Mitton St N", "lat": 42.9710, "lon": -82.3980, "cat": "Churches", "accepts": "Clothing and household items.", "note": "⛪ Accepts clothing and household items only."},
    {"name": "St. Vincent de Paul", "address": "228 Davis St", "lat": 42.9730, "lon": -82.4030, "cat": "Churches", "accepts": "Clothing and household items.", "note": "⛪ Accepts clothing and household items only."},
    {"name": "St. Luke’s United Church", "address": "350 Indian Rd S", "lat": 42.9650, "lon": -82.3750, "cat": "Churches", "accepts": "Clothing and household items.", "note": "⛪ Accepts clothing and household items only."},

    # Charities
    {"name": "The Inn of the Good Shepherd", "address": "115 John St", "lat": 42.9680, "lon": -82.4040, "cat": "Charities", "accepts": "Food and basic hygiene necessities."},
    {"name": "Good Shepherd’s Lodge", "address": "950 Confederation St", "lat": 42.9610, "lon": -82.3895, "cat": "Charities", "accepts": "Clothing and shelter essentials."}
]

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat, dlon = math.radians(lat2 - lat1), math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    return R * 2 * math.asin(math.sqrt(a))

@st.cache_data
def load_n7s_codes():
    if os.path.exists("N7S_postal_codes.csv"):
        df = pd.read_csv("N7S_postal_codes.csv")
        df.columns = df.columns.str.strip()
        return df
    return pd.DataFrame({"postal_code": ["N7S0A1"], "lat": [42.97], "lon": [-82.40]})

def donate_sell_page():
    if 'points' not in st.session_state: st.session_state.points = 0
    apply_donate_styles()

    st.markdown('<h1 style="color:#f59e0b; text-align:center;">🤝 Sarnia Community Network</h1>', unsafe_allow_html=True)

    # --------------------------------------------------
    # POSTAL CODE SELECTOR (PREFIX + DROPDOWN)
    # --------------------------------------------------
    st.subheader("📍 Location Settings")
    col1, col2 = st.columns(2)
    
    with col1:
        prefix = st.selectbox("Select Postal Prefix", ["N7S", "N7T", "N7V", "N7W", "N7X"])
    
    with col2:
        df_codes = load_n7s_codes()
        if prefix == "N7S":
            # Show specific codes for N7S from CSV
            codes_list = df_codes["postal_code"].unique()
            postal_code = st.selectbox("Select Specific Code", codes_list)
            user_data = df_codes[df_codes["postal_code"] == postal_code].iloc[0]
            u_lat, u_lon = user_data["lat"], user_data["lon"]
        else:
            st.info(f"Using central coordinates for {prefix}")
            u_lat, u_lon = 42.9745, -82.4060 # Default

    # --------------------------------------------------
    # CATEGORY FILTER
    # --------------------------------------------------
    cat_list = ["All Categories", "Clothing & Household", "Bottle Returns", "Churches", "Charities", "Recycling Depots", "Home Improvement"]
    selected_cat = st.selectbox("What are you donating today?", cat_list)

    # --------------------------------------------------
    # TABS
    # --------------------------------------------------
    tab_donate, tab_sell = st.tabs(["🎁 Donation & Returns", "💰 Selling Platforms"])

    with tab_donate:
        df_display = pd.DataFrame(DONATION_DATA)
        
        # Filter by category if selected
        if selected_cat != "All Categories":
            df_display = df_display[df_display["cat"] == selected_cat]

        # Calculate Proximity
        df_display["dist"] = df_display.apply(lambda r: haversine(u_lat, u_lon, r["lat"], r["lon"]), axis=1)
        df_sorted = df_display.sort_values("dist")

        if df_sorted.empty:
            st.warning("No matches found in this category.")
        else:
            for _, row in df_sorted.iterrows():
                st.markdown(f"""
                    <div class="location-card">
                        <span class="dist-badge">📏 {row['dist']:.2f} km</span>
                        <h4 style="margin: 0; color: white;">{row['name']}</h4>
                        <p style="margin: 5px 0; color: #cbd5e1; font-size: 0.9rem;">📍 {row['address']}</p>
                        <p class="accepts-text">📦 <b>Accepts:</b> {row['accepts']}</p>
                        <span class="note-text">{row.get('note', '')}</span>
                    </div>
                """, unsafe_allow_html=True)

    with tab_sell:
        st.markdown("### Online Marketplaces")
        sell_sites = [
            {"name": "Facebook Marketplace", "url": "https://www.facebook.com/marketplace/sarnia/", "desc": "Best for household items and furniture."},
            {"name": "Kijiji Sarnia", "url": "https://www.kijiji.ca/b-city-of-sarnia/l1700251", "desc": "Great for electronics and vehicles."},
            {"name": "Karrot", "url": "https://www.karrotmarket.com/", "desc": "Verified local community marketplace."}
        ]
        for site in sell_sites:
            st.markdown(f"""
                <div class="location-card" style="border-left: 5px solid #10b981;">
                    <h4 style="margin: 0;"><a href="{site['url']}" target="_blank" style="color: #10b981; text-decoration: none;">{site['name']} ↗</a></h4>
                    <p style="margin: 5px 0; color: #cbd5e1; font-size: 0.9rem;">{site['desc']}</p>
                </div>
            """, unsafe_allow_html=True)

    # --------------------------------------------------
    # REWARD SECTION
    # --------------------------------------------------
    st.markdown("---")
    reward_col, btn_col = st.columns([2, 1])
    with reward_col:
        st.markdown(f"""
            <div style="background: rgba(245, 158, 11, 0.1); padding: 15px; border-radius: 12px; border: 1px solid rgba(245, 158, 11, 0.3);">
                <p style="margin: 0; color: #f59e0b; font-weight: bold;">Did you complete a hand-off?</p>
                <p style="margin: 0; color: #cbd5e1; font-size: 0.85rem;">Confirm to add 10 points to your account.</p>
            </div>
        """, unsafe_allow_html=True)
    
    with btn_col:
        st.write("##")
        if st.button("Confirm & Claim Points", use_container_width=True):
            st.session_state.points += 10
            st.balloons()
            st.success("10 Points Awarded! 🏆")
            time.sleep(1)
            st.rerun()