import streamlit as st

def how_it_works_page():
    st.title("🧠 How EcoVision Works")
    st.caption("Transparent, responsible AI for everyday recycling")

    st.markdown("---")

    # --------------------------------------------------
    # Step-by-step Flow
    # --------------------------------------------------
    st.subheader("🔄 The EcoVision Process")

    col1, col2, col3, col4 = st.columns(4)

    col1.markdown("📸 **Upload Image**\n\nTake or upload a photo of a waste item.")
    col2.markdown("🧠 **AI Analysis**\n\nOur model identifies the object.")
    col3.markdown("♻️ **Bin Recommendation**\n\nCorrect bin is suggested.")
    col4.markdown("🤝 **Human Control**\n\nYou confirm if AI is unsure.")

    st.markdown("---")

    # --------------------------------------------------
    # AI Explanation
    # --------------------------------------------------
    st.subheader("🤖 The AI Behind EcoVision")

    st.markdown("""
    EcoVision uses a **deep learning image classification model**
    based on **MobileNetV2**, a lightweight and efficient convolutional
    neural network used in real-world applications.

    The model is trained to recognize **18 different waste objects**
    such as batteries, plastic bottles, food scraps, and more.
    """)

    # --------------------------------------------------
    # Confidence Score
    # --------------------------------------------------
    st.subheader("📊 Confidence & Transparency")

    st.markdown("""
    Unlike black-box systems, EcoVision always shows a **confidence score**.

    - High confidence → automatic bin suggestion  
    - Low confidence → user confirmation required  

    This ensures **accuracy, accountability, and trust**.
    """)

    # --------------------------------------------------
    # Human in the Loop
    # --------------------------------------------------
    st.subheader("🤝 Human-in-the-Loop Design")

    st.markdown("""
    EcoVision is designed to **assist humans, not replace them**.

    When the AI is unsure, users choose between the top predictions.
    This prevents incorrect disposal and encourages learning.
    """)

    # --------------------------------------------------
    # Why Some Items Are Confusing
    # --------------------------------------------------
    st.subheader("❓ Why Some Items Are Harder")

    st.markdown("""
    Some waste items look visually similar:
    - Kitchen waste vs food scraps  
    - Plastic bags vs wrappers  
    - Mixed-material products  

    EcoVision handles this by being transparent about uncertainty
    instead of making unsafe guesses.
    """)

    # --------------------------------------------------
    # Bin Logic
    # --------------------------------------------------
    st.subheader("🗑️ How Bin Rules Are Decided")

    st.markdown("""
    The AI **only identifies the object**.

    The **bin recommendation** is determined using
    clear, rule-based logic aligned with **local recycling guidelines**.

    This keeps the system:
    - Explainable  
    - Adaptable to different cities  
    - Easy to update  
    """)

    # --------------------------------------------------
    # Future Improvements
    # --------------------------------------------------
    st.subheader("🚀 Continuous Improvement")

    st.markdown("""
    EcoVision improves over time through:
    - More training images  
    - User feedback  
    - Expansion to new regions  
    - Smarter reward-based engagement  

    The system is built to grow with the community.
    """)