import streamlit as st

# --------------------------------------------------
# SESSION STATE INITIALIZATION
# --------------------------------------------------
if "points" not in st.session_state:
    st.session_state.points = 0

if "badges" not in st.session_state:
    st.session_state.badges = []

# --------------------------------------------------
# AVATAR EVOLUTION LOGIC (PLACEHOLDER)
# --------------------------------------------------
AVATAR_STAGES = [
    {
        "name": "Eco Seed",
        "min_points": 0,
        "emoji": "🌱",
        "description": "Every journey toward sustainability starts with a seed."
    },
    {
        "name": "Green Sprout",
        "min_points": 50,
        "emoji": "🌿",
        "description": "You're building eco-friendly habits!"
    },
    {
        "name": "Earth Guardian",
        "min_points": 150,
        "emoji": "🌍",
        "description": "You're actively protecting the planet."
    },
    {
        "name": "Eco Visionary",
        "min_points": 300,
        "emoji": "🦋",
        "description": "A true sustainability leader inspiring others."
    }
]

BADGE_DEFINITIONS = [
    {"name": "First Sort", "points": 10, "emoji": "🥇"},
    {"name": "Recycler", "points": 50, "emoji": "♻️"},
    {"name": "Donation Hero", "points": 100, "emoji": "🤝"},
    {"name": "Zero Waste Champ", "points": 250, "emoji": "🏆"}
]

# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------

def get_current_avatar(points):
    """Return the highest avatar stage unlocked."""
    current = AVATAR_STAGES[0]
    for stage in AVATAR_STAGES:
        if points >= stage["min_points"]:
            current = stage
    return current


def update_badges(points):
    for badge in BADGE_DEFINITIONS:
        if points >= badge["points"] and badge["name"] not in st.session_state.badges:
            st.session_state.badges.append(badge["name"])

# --------------------------------------------------
# PAGE FUNCTION
# --------------------------------------------------

def rewards_page():
    st.title("🏆 EcoVision Rewards & Progress")
    st.caption("Build sustainable habits. Level up your eco avatar.")

    points = st.session_state.points

    update_badges(points)
    avatar = get_current_avatar(points)

    # --------------------------------------------------
    # USER STATS
    # --------------------------------------------------
    st.markdown("---")
    st.subheader("⭐ Your Eco Stats")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Points", points)
    col2.metric("Badges Earned", len(st.session_state.badges))
    col3.metric("Eco Rank", avatar["name"])

    # --------------------------------------------------
    # AVATAR DISPLAY
    # --------------------------------------------------
    st.markdown("---")
    st.subheader("🧬 Your Eco Avatar")

    st.markdown(
        f"""
        <div style='text-align:center; font-size:100px;'>
            {avatar['emoji']}
        </div>
        <h3 style='text-align:center;'>{avatar['name']}</h3>
        <p style='text-align:center;'>{avatar['description']}</p>
        """,
        unsafe_allow_html=True
    )

    # Progress to next avatar
    next_stage = None
    for stage in AVATAR_STAGES:
        if stage["min_points"] > points:
            next_stage = stage
            break

    if next_stage:
        progress = points / next_stage["min_points"]
        st.progress(min(progress, 1.0))
        st.caption(
            f"{next_stage['min_points'] - points} points to reach **{next_stage['name']}**"
        )
    else:
        st.success("🎉 Maximum evolution reached!")

    # --------------------------------------------------
    # BADGES SECTION
    # --------------------------------------------------
    st.markdown("---")
    st.subheader("🎖️ Badges")

    badge_cols = st.columns(4)

    for i, badge in enumerate(BADGE_DEFINITIONS):
        earned = badge["name"] in st.session_state.badges
        with badge_cols[i % 4]:
            st.markdown(
                f"""
                <div style='text-align:center; font-size:40px;'>
                    {badge['emoji'] if earned else '🔒'}
                </div>
                <p style='text-align:center;'>
                    {badge['name']}<br>
                    <small>{badge['points']} pts</small>
                </p>
                """,
                unsafe_allow_html=True
            )

    # --------------------------------------------------
    # FUTURE EXPANSION
    # --------------------------------------------------
    st.markdown("---")
    st.subheader("🚀 Coming Soon")

    st.markdown(
        """
        - Animated avatars (Khan Academy–style evolution)  
        - Seasonal challenges  
        - Community leaderboards  
        - Real-world rewards & partnerships  
        - CO₂ & landfill impact tracking
        """
    )
