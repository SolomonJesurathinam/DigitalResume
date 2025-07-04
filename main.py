import streamlit as st

# --- PAGE SETUP --- 
about_page = st.Page(
    page="views/about_me.py",
    title="About Me",
    icon=":material/account_circle:",
    default=True
)

ml_project_page = st.Page(
    page="views/ml_projects.py",
    title="Ml Projects",
    icon=":material/bar_chart:",
)

chatbot_page = st.Page(
    page="views/chatbot.py",
    title="Chat bot",
    icon="🖥️"
)

age_gender_page = st.Page(
    page="views/age_gender.py",
    title="Age Gender Prediction",
    icon="🧒"
)

crop_page = st.Page(
    page="views/Crop Recommendation.py",
    title="Crop Recommendation",
    icon="🌱"
)

fifa_22 = st.Page(
    page="views/FIFA_22_Simulator.py",
    title="FIFA 22 SIMULATOR",
    icon="⚽"
)

# --- NAVIGATION ---
pg = st.navigation(
    {
        "Info":[about_page],
        "Projects":[ml_project_page,chatbot_page,crop_page,fifa_22,age_gender_page]
    },position="sidebar"
)

st.logo("assets/logo.png")
st.sidebar.text("Made with ❤️ by Solomon")

# --- RN NAVIGATION ---
pg.run()