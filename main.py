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

# --- NAVIGATION ---
pg = st.navigation(
    {
        "Info":[about_page],
        "Projects":[ml_project_page,chatbot_page]
    }
)

st.logo("assets/logo.png")
st.sidebar.text("Made with ❤️ by Solomon")

# --- RN NAVIGATION ---
pg.run()