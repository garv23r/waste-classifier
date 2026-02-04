import streamlit as st

from pages.how_it_works import how_it_works_page
from pages.prediction import predict_page
from pages.donate_sell import donate_sell_page
from pages.rewards import rewards_page
from pages.about import about_page
from pages.home import home_pages

# --------------------------------------------------
# App Config
# --------------------------------------------------
st.set_page_config(
    page_title="EcoVision",
    page_icon="♻️",
    layout="wide"
)

# --------------------------------------------------
# Sidebar Navigation
# --------------------------------------------------
st.sidebar.title("♻️ EcoVision")
page = st.sidebar.radio(
    "Navigate",
    [
        "Home",
        "How Our Model Works",
        "Predict Waste Bin",
        "Donate / Sell",
        "Rewards",
        "About Us"
    ]
)

# --------------------------------------------------
# Session State (shared data)
# --------------------------------------------------
if "points" not in st.session_state:
    st.session_state.points = 0

# --------------------------------------------------
# Page Routing
# --------------------------------------------------
if page == "Home":
    home_pages()

elif page == "How Our Model Works":
    how_it_works_page()

elif page == "Predict Waste Bin":
    predict_page()

elif page == "Donate / Sell":
    donate_sell_page()

elif page == "Rewards":
    rewards_page()

elif page == "About Us":
    about_page()