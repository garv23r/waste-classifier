import streamlit as st

def home_pages():
    # --- Custom CSS for Fixed Background & Premium Glassmorphism ---
    st.markdown("""
        <style>
        /* Fixed Background Image */
        .stApp {
            background-image: url("https://images.unsplash.com/photo-1532996122724-e3c354a0b15b?q=80&w=2070&auto=format&fit=crop");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }

        /* Overlay to darken background for readability */
        .stApp::before {
            content: "";
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.8); /* Adjust darkness here */
            z-index: -1;
        }

        /* Main Container Spacing */
        .main-container {
            padding: 20px;
        }

        /* Hero Section with Glass effect */
        .hero {
            background: rgba(255, 255, 255, 0.08);
            backdrop-filter: blur(15px);
            -webkit-backdrop-filter: blur(15px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 80px 40px;
            border-radius: 30px;
            text-align: center;
            margin-bottom: 50px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.4);
        }
        
        .hero h1 {
            font-size: 4rem;
            background: linear-gradient(to right, #4ade80, #2dd4bf);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
            margin-bottom: 20px;
        }

        .hero p {
            font-size: 1.3rem;
            color: #e5e7eb;
            max-width: 700px;
            margin: 0 auto 30px auto;
            line-height: 1.6;
        }

        /* Call to Action */
        .cta-btn {
            background: linear-gradient(90deg, #10b981 0%, #059669 100%);
            color: white !important;
            padding: 15px 35px;
            border-radius: 12px;
            text-decoration: none;
            font-weight: 700;
            font-size: 1.1rem;
            transition: all 0.3s ease;
            display: inline-block;
            border: none;
        }
        .cta-btn:hover {
            transform: scale(1.05);
            box-shadow: 0 0 20px rgba(16, 185, 129, 0.5);
        }

        /* Premium Cards */
        .card {
            background: rgba(15, 23, 42, 0.9);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 30px;
            height: 100%;
        }
        
        .card h2 {
            color: #4ade80;
            font-size: 1.6rem;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        /* Grid Items */
        .grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 12px;
            margin-top: 20px;
        }
        .grid-item {
            background: rgba(255, 255, 255, 0.1);
            padding: 12px;
            border-radius: 12px;
            text-align: center;
            font-size: 0.9rem;
            color: #f3f4f6;
            border: 1px solid rgba(255, 255, 255, 0.05);
        }

        /* Custom Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
        }
        ::-webkit-scrollbar-track {
            background: rgba(0,0,0,0.1);
        }
        ::-webkit-scrollbar-thumb {
            background: #10b981;
            border-radius: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

    # --- Hero Section ---
    st.markdown("""
    <div class="hero">
        <h1>♻️ EcoVision</h1>
        <p>
            Bridging the gap between waste and sustainability.
            Using cutting-edge AI to transform how we recycle,
            one image at a time.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # --- Content Layout ---
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown("""
            <div class="card">
                <h2>🚨 The Challenge</h2>
                <p>
                Sorting waste shouldn't feel like a puzzle. In many cities, the difference 
                between <b>blue, black, and green</b> bins is unclear, leading to contamination 
                in our recycling streams.
                </p>
                <p style="color: #94a3b8; font-style: italic;">
                "We don’t harm the environment intentionally - we do it because we lack the right tools."
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
            <div class="card">
                <h2>💡 The Insight</h2>
                <p>Simplicity drives action. Our philosophy is built on four pillars:</p>
                <div class="grid">
                    <div class="grid-item">✨ Effortless</div>
                    <div class="grid-item">📸 Visual-First</div>
                    <div class="grid-item">⚡ Real-time</div>
                    <div class="grid-item">🏆 Gamified</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div class="card">
                <h2>🛠️ The Solution</h2>
                <p>
                EcoVision utilizes high-accuracy <b>Neural Networks</b> to analyze your waste. 
                Simply point, shoot, and get instant instructions on where your item belongs.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
            <div class="card">
                <h2>🎁 The Ecosystem</h2>
                <p>We've created a rewarding experience that goes beyond sorting:</p>
                <div class="grid">
                    <div class="grid-item">⭐ Earn Points</div>
                    <div class="grid-item">💰 Sell Recyclables</div>
                    <div class="grid-item">🎖️ Unlock Badges</div>
                    <div class="grid-item">🎨 Custom Avatars</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # --- Full Width Bottom Section ---
    st.markdown("""
        <div class="card" style="text-align: center; background: linear-gradient(135deg, rgba(16, 185, 129, 0.7), rgba(6, 78, 59, 0.9));">
            <h2>🌍 Join the Movement</h2>
            <p style="max-width: 800px; margin: 0 auto;">
                EcoVision is more than an app - it's a community-driven platform designed to educate 
                families and immigrants, ensuring that everyone has the power to protect our planet.
            </p>
        </div>
        """, unsafe_allow_html=True)