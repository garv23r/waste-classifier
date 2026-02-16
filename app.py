import streamlit as st
from views.how_it_works import how_it_works_page
from views.prediction import predict_page
from views.donate_sell import donate_sell_page
from views.rewards import rewards_page
from views.about import about_page
from views.home import home_pages

# --------------------------------------------------
# App Config
# --------------------------------------------------
st.set_page_config(
    page_title="EcoVision AI",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="expanded"
)


if "points" not in st.session_state:
    st.session_state.points = 0

if "badges" not in st.session_state:
    st.session_state.badges = []

# --------------------------------------------------
# Global Glassmorphism Sidebar CSS
# --------------------------------------------------
st.markdown("""
    <style>
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.9); /* Dark Slate to match content */
        backdrop-filter: blur(15px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* Sidebar Navigation Text */
    [data-testid="stSidebarNav"] {
        background-color: transparent !important;
    }

    /* Radio Button Styling */
    div[data-testid="stSidebarUserContent"] .stRadio > label {
        color: #4ade80 !important; /* Green Accent */
        font-weight: bold;
    }
    
    div[data-testid="stSidebarUserContent"] .stRadio div[role="radiogroup"] > label {
        background: rgba(255, 255, 255, 0.05);
        padding: 10px 15px;
        border-radius: 10px;
        margin-bottom: 5px;
        transition: 0.3s;
    }

    div[data-testid="stSidebarUserContent"] .stRadio div[role="radiogroup"] > label:hover {
        background: rgba(74, 222, 128, 0.1);
    }

    /* Pinned Points Card at Bottom */
    .sidebar-footer {
        position: fixed;
        bottom: 20px;
        left: 20px;
        right: 20px;
        background: linear-gradient(135deg, rgba(74, 222, 128, 0.2), rgba(45, 212, 191, 0.2));
        border: 1px solid rgba(74, 222, 128, 0.3);
        padding: 15px;
        border-radius: 15px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Sidebar Navigation
# --------------------------------------------------
with st.sidebar:
    st.markdown("<h1 style='color: white;'>♻️ EcoVision</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94a3b8;'>Smart Waste Intelligence</p>", unsafe_allow_html=True)
    st.write("---")
    
    page = st.radio(
        "NAVIGATION",
        ["Home", "How it Works", "AI Prediction", "Donate / Sell", "Rewards", "About Us"]
    )
    
    # Pinned Points Display
    st.markdown(f"""
        <div class="sidebar-footer">
            <small style="color: #94a3b8;">CURRENT BALANCE</small><br>
            <span style="color: #4ade80; font-size: 1.2rem; font-weight: bold;">⭐ {st.session_state.get('points', 0)} Points</span>
        </div>
    """, unsafe_allow_html=True)

# --------------------------------------------------
# Page Routing
# --------------------------------------------------
if page == "Home":
    home_pages()
elif page == "How it Works":
    how_it_works_page()
elif page == "AI Prediction":
    predict_page()
elif page == "Donate / Sell":
    donate_sell_page()
elif page == "Rewards":
    rewards_page()
elif page == "About Us":
    about_page()