import streamlit as st

def about_page():
    # --- Custom CSS for About Page ---
    st.markdown("""
        <style>
        .stApp {
            background-image: url("https://images.unsplash.com/photo-1441974231531-c6227db76b6e?q=80&w=2071&auto=format&fit=crop");
            background-size: cover;
            background-attachment: fixed;
            filter: brightness(93%);
        }
        .stApp::before {
            content: ""; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(15, 25, 15, 0.82); z-index: -1;
        }

        /* Glass Cards */
        .about-card {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            margin-bottom: 25px;
        }
        
        .vision-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }

        .contact-pill {
            display: inline-block;
            background: rgba(74, 222, 128, 0.1);
            border: 1px solid rgba(74, 222, 128, 0.3);
            color: #4ade80;
            padding: 8px 18px;
            border-radius: 50px;
            margin: 5px;
            font-size: 0.9rem;
            text-decoration: none;
            transition: 0.3s;
        }
        .contact-pill:hover {
            background: rgba(74, 222, 128, 0.2);
            transform: translateY(-2px);
        }
        </style>
    """, unsafe_allow_html=True)

    # --- Header ---
    st.markdown("""
        <div style="text-align: center; padding: 40px 0;">
            <h1 style="font-size: 3.5rem; color: #4ade80;">🌍 About EcoVision</h1>
            <p style="color: #cbd5e1; font-size: 1.2rem; max-width: 800px; margin: 0 auto;">
                Turning everyday waste decisions into positive environmental impact through 
                Smart Waste Intelligence.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # --- Section 1: Who We Are ---
    st.markdown("""
        <div class="about-card">
            <h2 style="color: #4ade80;">👥 Who We Are</h2>
            <p style="font-size: 1.1rem; line-height: 1.7; color: #e2e8f0;">
                EcoVision is an AI-powered platform designed to help people correctly identify 
                household waste and dispose of it responsibly. Waste sorting rules can be 
                confusing and inconsistent. We bridge this gap by combining <b>Neural Networks</b>, 
                <b>Local Disposal Logic</b>, and <b>Human Verification</b>.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # --- Section 2: The Vision ---
    st.markdown("<h2 style='color: white; margin-left: 10px;'>🌱 Our Vision</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
            <div class="about-card">
                <h3 style="color: #2dd4bf;">🏢 Collaborations</h3>
                <ul style="color: #cbd5e1; line-height: 2;">
                    <li>♻️ Recycling Municipalities</li>
                    <li>🏫 Educational Programs</li>
                    <li>🏙️ Local Communities</li>
                    <li>🌿 Eco-friendly Brands</li>
                    <li>🤝 Donation Agencies</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="about-card">
                <h3 style="color: #2dd4bf;">🎯 Long-term Impact</h3>
                <p style="color: #cbd5e1;">We are building an ecosystem where:</p>
                <ul style="color: #cbd5e1; line-height: 2;">
                    <li>Sustainability is <b>simple</b></li>
                    <li>Good behavior is <b>rewarded</b></li>
                    <li>Awareness is <b>accessible</b> to all</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

    # --- Section 3: Circular Economy Diagram Placeholder ---
    st.markdown("---")
    st.subheader("🔄 The Circular Economy Model")
    st.info("EcoVision follows the circular economy principle: Reduce, Reuse, and then Recycle correctly.")
    

    # --- Section 4: Contact Footer ---
    st.markdown("""
        <div class="about-card" style="text-align: center; border-top: 4px solid #4ade80;">
            <h2 style="color: white;">📬 Get In Touch</h2>
            <p style="color: #94a3b8; margin-bottom: 25px;">Interested in collaborating or supporting EcoVision? Let’s talk.</p>
            <a href="mailto:ecovision.ai@gmail.com" class="contact-pill">📧 ecovision.ai@gmail.com</a>
            <a href="#" class="contact-pill">💼 LinkedIn</a>
            <a href="#" class="contact-pill">🐦 Twitter / X</a>
            <a href="#" class="contact-pill">🌐 Website</a>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<p style='text-align: center; color: #4b5563; font-size: 0.8rem;'>© 2026 EcoVision AI. Built for Sarnia, ON.</p>", unsafe_allow_html=True)