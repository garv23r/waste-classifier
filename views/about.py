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
            background: rgba(15, 25, 15, 0.85); z-index: -1;
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
                
        .source-link {
            color: #4ade80;
            text-decoration: none;
            font-weight: bold;
        }
        .source-link:hover {
            text-decoration: underline;
        }
        
        .tech-link-card {
            background: rgba(255, 255, 255, 0.05); 
            padding: 20px; 
            border-radius: 15px; 
            border: 1px solid rgba(255, 255, 255, 0.1); 
            text-align: center;
            transition: 0.3s;
        }
        .tech-link-card:hover {
            background: rgba(255, 255, 255, 0.1);
            transform: translateY(-3px);
        }
        </style>
    """, unsafe_allow_html=True)

    # --- Header ---
    st.markdown("""
        <div style="text-align: center; padding: 40px 0;">
            <h1 style="font-size: 3.5rem; color: #4ade80; margin-bottom: 10px;">🌍 About EcoVision</h1>
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
            <p style="color: #e2e8f0; line-height: 1.6;">
                EcoVision is an AI-powered platform designed to bridge the gap between complex 
                AI technology and local community needs. By combining <b>Neural Networks</b> 
                trained on global data with <b>Sarnia-Specific Disposal Logic</b>, we make 
                sustainability simple for every household.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # THE TEAM
    st.markdown("""
        <div class="about-card">
            <h2 style="color: #4ade80;">🤝 The Team</h2>
            <div style="margin-bottom: 25px;">
                <h4 style="color: white; margin-bottom: 5px;">Student Researcher</h4>
                <p style="color: #4ade80; font-size: 0.9rem; font-weight: bold;">Lead Researcher & Concept Architect (Lansdowne Public School)</p>
                <p style="color: #cbd5e1; font-size: 0.95rem; line-height: 1.6;">
                    This student is the driving force behind the project's vision. She conducted 
                    comprehensive research into Sarnia's dual-stream waste systems and defined 
                    the conceptual framework that ensures the AI serves local environmental goals.
                </p>
                <p style="color: #f59e0b; font-size: 0.85rem; font-style: italic; margin-top: 10px; padding: 8px; background: rgba(245, 158, 11, 0.1); border-radius: 8px; display: inline-block;">
                    🔒 The name of this student researcher will be revealed once we collect sufficient user feedback. Stay tuned!
                </p>
            </div>
            <div style="border-top: 1px solid rgba(255,255,255,0.1); padding-top: 20px;">
                <h4 style="color: white; margin-bottom: 5px;">Garv Rastogi</h4>
                <p style="color: #f59e0b; font-size: 0.9rem; font-weight: bold;">Technical Lead & Developer</p>
                <p style="color: #cbd5e1; font-size: 0.95rem;">
                    Garv is a 4th-year <b>Computer Science student at McMaster University</b>. 
                    He translated environmental research into a functional AI application, focusing on deep learning integration and 
                    scalable UI design to help society.
                </p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # CREDIBILITY LINKS
    st.markdown("""
        <div class="about-card">
            <h2 style="color: #4ade80;">📖 Data Sources & Research</h2>
            <p style="color: #cbd5e1; font-size: 0.95rem; line-height: 1.6;">
                To ensure accuracy and reliability, EcoVision relies on the following official 
                Sarnia data and open-source technical datasets:
            </p>
            <ul style="color: #e2e8f0; font-size: 0.95rem; line-height: 2;">
                <li>🏛️ <b>Official Waste Rules:</b> <a href="https://www.sarnia.ca/living-here/waste/" class="source-link">City of Sarnia Waste Portal ↗</a></li>
                <li>📍 <b>Region Mapping:</b> <a href="https://docs.google.com/spreadsheets/d/1ysHm94LgfThO4ClFL0AtEJpz3sujwOuYj9zLYxpnAtU/edit?gid=1709202715#gid=1709202715" class="source-link">N7S Postal Code Database ↗</a></li>
                <li>📂 <b>AI Training Data:</b> <a href="https://www.kaggle.com/datasets/phenomsg/waste-classification/data" class="source-link">Kaggle Waste Dataset ↗</a></li>
                <li>🐙 <b>Source Code:</b> <a href="https://github.com/garv23r/waste-classifier" class="source-link">GitHub Repository ↗</a></li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    
    st.info("💡 **Tip:** Click the Kaggle or GitHub links above to explore the data and code behind this project.")

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

    # --- Section 3: Circular Economy Model ---
    st.markdown("---")
    st.subheader("🔄 The Circular Economy Model")

    st.info("EcoVision follows the circular economy principle: Reduce, Reuse, and then Recycle correctly.")

    # --- Section 4: Embedded Feedback Form ---
    st.markdown("---")
    st.markdown("<h2 style='color: #4ade80; text-align: center;'>⭐ Share Your Feedback</h2>", unsafe_allow_html=True)
    
    # The Google Forms Embed Link
    # Note: I've added /viewform?embedded=true to your URL
    form_url = "https://docs.google.com/forms/d/e/1FAIpQLSdSJ2P85gewLgld7LaQuRzsJaVkHN-mQASSpae0PjFOUooQcA/viewform"
    
    html_code = f"""
        <div style="display: flex; justify-content: center;">
            <iframe src="{form_url}" 
                width="100%" 
                height="800" 
                frameborder="0" 
                marginheight="0" 
                marginwidth="0"
                style="background: rgba(255,255,255,0.05); border-radius: 15px; border: 1px solid rgba(74, 222, 128, 0.3);">
                Loading…
            </iframe>
        </div>
    """
    
    # Render the IFrame
    st.components.v1.html(html_code, height=850, scrolling=True)

    # --- Section 5: Contact Footer ---
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