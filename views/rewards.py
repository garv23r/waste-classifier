import streamlit as st

def rewards_page():
    # --- Custom CSS for Gamified Progress ---
    st.markdown("""
        <style>
        .stApp {
            background-image: url("https://images.unsplash.com/photo-1550751827-4bd374c3f58b?q=80&w=2070&auto=format&fit=crop");
            background-size: cover;
            background-attachment: fixed;
            filter: brightness(90%);
        }
        .stApp::before {
            content: ""; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(10, 20, 10, 0.85); z-index: -1;
        }

        /* Profile Header */
        .profile-header {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(15px);
            border: 1px solid rgba(74, 222, 128, 0.2);
            border-radius: 30px;
            padding: 40px;
            text-align: center;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }

        /* Avatar Glow Effect */
        .avatar-glow {
            font-size: 100px;
            text-shadow: 0 0 20px rgba(74, 222, 128, 0.6);
            margin-bottom: 10px;
            display: inline-block;
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }

        /* Badge Grid */
        .badge-card {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 20px;
            text-align: center;
            transition: all 0.3s ease;
        }
        .badge-card.earned {
            border-color: #f59e0b;
            background: rgba(245, 158, 11, 0.05);
        }
        .badge-card.locked {
            opacity: 0.5;
            filter: grayscale(100%);
        }

        /* Level Progress */
        .stProgress > div > div > div > div {
            background-image: linear-gradient(to right, #4ade80 , #2dd4bf);
        }
        </style>
    """, unsafe_allow_html=True)

    # --- Logic ---
    points = st.session_state.get('points', 0)
    
    # Update badges logic
    BADGE_DEFINITIONS = [
        {"name": "First Sort", "points": 10, "emoji": "🥇"},
        {"name": "Recycler", "points": 50, "emoji": "♻️"},
        {"name": "Donation Hero", "points": 100, "emoji": "🤝"},
        {"name": "Zero Waste Champ", "points": 250, "emoji": "🏆"}
    ]
    
    current_badges = st.session_state.get('badges', [])
    for b in BADGE_DEFINITIONS:
        if points >= b["points"] and b["name"] not in current_badges:
            current_badges.append(b["name"])
    st.session_state.badges = current_badges

    # Avatar Stages
    AVATAR_STAGES = [
        {"name": "Eco Seed", "min": 0, "emoji": "🌱", "desc": "Every journey toward sustainability starts with a seed."},
        {"name": "Green Sprout", "min": 50, "emoji": "🌿", "desc": "You're building eco-friendly habits!"},
        {"name": "Earth Guardian", "min": 150, "emoji": "🌍", "desc": "You're actively protecting the planet."},
        {"name": "Eco Visionary", "min": 300, "emoji": "🦋", "desc": "A true sustainability leader inspiring others."}
    ]

    # Get current and next stage
    current_stage = next((s for s in reversed(AVATAR_STAGES) if points >= s["min"]), AVATAR_STAGES[0])
    next_stage = next((s for s in AVATAR_STAGES if s["min"] > points), None)

    # --- Page UI ---
    st.title("🏆 Rewards & Progress")
    
    # Stats row
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Global Impact Points", f"{points} ⭐")
    with c2:
        st.metric("Milestones Unlocked", len(current_badges))
    with c3:
        st.metric("Current Rank", current_stage["name"])

    # Hero Avatar Section
    st.markdown(f"""
        <div class="profile-header">
            <div class="avatar-glow">{current_stage['emoji']}</div>
            <h2 style="color: #4ade80; margin: 0;">{current_stage['name']}</h2>
            <p style="color: #cbd5e1; font-style: italic;">"{current_stage['desc']}"</p>
        </div>
    """, unsafe_allow_html=True)

    # Evolution Progress
    if next_stage:
        needed = next_stage["min"] - points
        progress_val = points / next_stage["min"]
        st.write(f"🧬 **Evolution Progress:** {points} / {next_stage['min']} pts")
        st.progress(min(progress_val, 1.0))
        st.caption(f"✨ Earn **{needed} more points** to evolve into a **{next_stage['name']}**!")
    else:
        st.success("🎉 Final Evolution Reached: You are a legendary Eco Visionary!")

    st.markdown("---")
    st.subheader("🎖️ Achievement Gallery")

    # Achievement Grid
    cols = st.columns(4)
    for i, b in enumerate(BADGE_DEFINITIONS):
        earned = b["name"] in current_badges
        status_class = "earned" if earned else "locked"
        with cols[i]:
            st.markdown(f"""
                <div class="badge-card {status_class}">
                    <div style="font-size: 40px; margin-bottom: 10px;">{b['emoji'] if earned else '🔒'}</div>
                    <div style="font-weight: bold; color: white;">{b['name']}</div>
                    <div style="font-size: 0.8rem; color: #94a3b8;">{b['points']} PTS</div>
                </div>
            """, unsafe_allow_html=True)

    # Future Roadmap
    st.markdown("---")
    with st.container():
        st.markdown("### 🚀 The Roadmap to Zero Waste")
        col_a, col_b = st.columns(2)
        with col_a:
            st.info("🎯 **Seasonal Challenges:** Limited-time events to boost your rank.")
            st.info("🗺️ **Local Leaderboards:** See how your neighborhood in Sarnia is doing.")
        with col_b:
            st.info("🎁 **Real Rewards:** Convert points into discounts at local eco-shops.")
            st.info("📊 **Impact Tracking:** Visualize the total mass of waste you've diverted.")