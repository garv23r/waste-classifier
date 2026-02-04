import streamlit as st

# --------------------------------------------------
# ABOUT PAGE
# --------------------------------------------------

def about_page():
    st.title("🌍 About EcoVision")
    st.caption("Turning everyday waste decisions into positive environmental impact")

    # --------------------------------------------------
    # WHO WE ARE
    # --------------------------------------------------
    st.markdown("---")
    st.subheader("👥 Who We Are")

    st.markdown(
        """
        **EcoVision – Smart Waste Intelligence System** is an AI-powered platform designed to help people
        correctly identify household waste and dispose of it responsibly.

        Waste sorting rules can be confusing, inconsistent, and overwhelming. EcoVision bridges this gap
        by combining **artificial intelligence, clear local disposal rules, and human verification** —
        making sustainable choices easier for everyone.
        """
    )

    # --------------------------------------------------
    # OUR VISION
    # --------------------------------------------------
    st.markdown("---")
    st.subheader("🌱 Our Vision")

    st.markdown(
        """
        This initiative starts small — but aims big.

        As EcoVision grows, we envision collaboration with:
        - ♻️ **Recycling organizations**  
        - 🏫 **Schools and educational programs**  
        - 🏙️ **Local communities and municipalities**  
        - 🌿 **Eco-friendly product companies**  
        - 🤝 **Agencies that accept donations or buy reusable waste items in bulk**

        Our long-term goal is to create a **connected ecosystem** where:
        - Doing the right thing for the environment is **simple**
        - Sustainable behavior is **rewarded**
        - Environmental awareness is **accessible to everyone**
        """
    )

    st.success(
        "We don’t need more rules — we need better tools.  \
        EcoVision turns confusion into clarity, and small actions into lasting impact."
    )

    # --------------------------------------------------
    # WHAT'S NEXT
    # --------------------------------------------------
    st.markdown("---")
    st.subheader("🚀 What We’re Working Toward")

    st.markdown(
        """
        - City-specific waste rules and expansion beyond Sarnia  
        - Verified donation & resale partner networks  
        - AI model improvement through user feedback  
        - Environmental impact tracking (CO₂ savings, landfill diversion)  
        - Community challenges and leaderboards
        """
    )

    # --------------------------------------------------
    # CONTACT & SOCIAL
    # --------------------------------------------------
    st.markdown("---")
    st.subheader("📬 Contact Us")

    st.markdown(
        """
        We welcome feedback, collaboration ideas, and partnership opportunities.

        📧 **Email:** ecovision.ai@gmail.com  
        🌐 **Website:** Coming Soon  
        💼 **LinkedIn:** Coming Soon  
        🐦 **Twitter / X:** Coming Soon
        """
    )

    st.info(
        "Interested in collaborating or supporting EcoVision?  \
        Let’s work together to build smarter, more sustainable communities."
    )
