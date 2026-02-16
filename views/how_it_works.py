import streamlit as st

def how_it_works_page():
    # --- Custom CSS (Updated for 2x2 Grid) ---
    st.markdown("""
        <style>
        .stApp {
            background-image: url("https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=2072&auto=format&fit=crop");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            filter: brightness(94%);
        }
        .stApp::before {
            content: "";
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0, 0, 0, 0.75);
            z-index: -1;
        }

        /* 2x2 Grid for Steps */
        .step-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 25px;
            margin: 40px 0;
        }

        .step-card {
            background: rgba(255, 255, 255, 0.07);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 30px;
            position: relative;
            transition: all 0.3s ease;
        }

        .step-card:hover {
            transform: scale(1.02);
            background: rgba(255, 255, 255, 0.12);
            border-color: #4ade80;
        }

        /* Step Number Positioning */
        .step-number {
            position: absolute;
            top: -15px;
            left: 20px;
            background: linear-gradient(135deg, #4ade80, #2dd4bf);
            color: #064e3b;
            width: 40px;
            height: 40px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 800;
            box-shadow: 0 4px 15px rgba(74, 222, 128, 0.4);
        }

        .step-card h4 {
            margin-top: 10px;
            color: #4ade80;
            font-size: 1.4rem;
        }

        .step-card p {
            color: #d1d5db;
            font-size: 1rem;
            line-height: 1.5;
        }
        
        /* Mobile adjustment */
        @media (max-width: 768px) {
            .step-grid {
                grid-template-columns: 1fr;
            }
        }
        </style>
    """, unsafe_allow_html=True)

    # --- Header ---
    st.markdown("""
        <div style="text-align: center; padding: 40px 0;">
            <h1 style="font-size: 2.5rem; color: white;">🧠 The EcoVision Flow</h1>
            <p style="color: #94a3b8; font-size: 1.2rem;">Our four-step intelligence process</p>
        </div>
    """, unsafe_allow_html=True)

    # --- The 2x2 Step Grid ---
    st.markdown("""
        <div class="step-grid">
            <div class="step-card">
                <div class="step-number">01</div>
                <h4>📸 Vision Input</h4>
                <p>Upload a clear photo of your waste. Our system accepts various formats and optimizes the image for neural processing.</p>
            </div>
            <div class="step-card">
                <div class="step-number">02</div>
                <h4>🧠 Neural Analysis</h4>
                <p>The MobileNetV2 architecture scans for shapes, textures, and features to identify the object with high precision.</p>
            </div>
            <div class="step-card">
                <div class="step-number">03</div>
                <h4>♻️ Logic Routing</h4>
                <p>Once identified, our rules engine cross-references the item with local recycling laws to find the perfect bin.</p>
            </div>
            <div class="step-card">
                <div class="step-number">04</div>
                <h4>🤝 Human Validation</h4>
                <p>Transparency is key. You see the confidence score and make the final call, helping the AI learn and grow.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # --- AI & Confidence Section ---
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown("""
            <div class="feature-card">
                <span class="badge">ARCHITECTURE</span>
                <h3>🤖 The AI Brain</h3>
                <p>EcoVision is powered by <b>MobileNetV2</b>, a state-of-the-art Deep Learning model. It's optimized for speed and efficiency, allowing for instant recognition without heavy server lag.</p>
                <p style="font-size: 0.9rem; color: #94a3b8;">Trained on 18+ categories of household waste including complex items like hazardous batteries and organic scraps.</p>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div class="feature-card" style="border-left-color: #4ade80;">
                <span class="badge" style="background: rgba(74, 222, 128, 0.2); color: #4ade80;">TRANSPARENCY</span>
                <h3>📊 Confidence Scores</h3>
                <p>We don't hide our math. Every prediction comes with a <b>Confidence Percentage</b>.</p>
                <ul style="font-size: 0.9rem; color: #cbd5e1;">
                    <li><b>High Score:</b> Automatic sorting suggestion.</li>
                    <li><b>Low Score:</b> System asks for human help.</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # --- Logic & Human-in-the-loop ---
    st.subheader("🛠️ Behind the Scenes Logic")
    
    # Diagrammatic representation using standard markdown
    st.info("💡 **Did you know?** The AI only identifies *what* the object is. A separate 'Rule Engine' decides the bin based on your local city guidelines. This makes EcoVision adaptable to any country!")

    col_a, col_b = st.columns([1, 1])

    with col_a:
        st.markdown("""
            <div class="feature-card">
                <h3>🤝 Human-in-the-Loop</h3>
                <p>AI can be tricked by lighting or angles. We designed EcoVision to <b>assist, not replace</b>.</p>
                <p>By involving the user in "uncertain" cases, we prevent contamination of recycling streams and educate the user simultaneously.</p>
            </div>
        """, unsafe_allow_html=True)

    with col_b:
        st.markdown("""
            <div class="feature-card" style="border-left-color: #f59e0b;">
                <h3>❓ Handling Ambiguity</h3>
                <p>Some items are notoriously difficult:</p>
                <ul style="font-size: 0.9rem; color: #cbd5e1;">
                    <li>Plastic-coated paper (Coffee cups)</li>
                    <li>Mixed material packaging</li>
                    <li>Visually similar food vs. non-food scraps</li>
                </ul>
                <p>Our model flags these as "Complex" to ensure you make the right choice.</p>
            </div>
        """, unsafe_allow_html=True)

    # --- Footer/Future ---
    st.markdown("""
        <div style="background: linear-gradient(90deg, rgba(96, 165, 250, 0.1), rgba(74, 222, 128, 0.1)); padding: 30px; border-radius: 20px; text-align: center; margin-top: 40px; border: 1px solid rgba(255,255,255,0.1);">
            <h3 style="margin-top: 0;">🚀 Continuous Evolution</h3>
            <p style="max-width: 800px; margin: 0 auto; color: #cbd5e1;">
                EcoVision isn't static. Every scan helps improve our global dataset. 
                We are currently working on expanding to 50+ categories and integrating 
                real-time GPS bin locators.
            </p>
        </div>
    """, unsafe_allow_html=True)