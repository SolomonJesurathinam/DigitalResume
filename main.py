import streamlit as st

# --- PAGE SETUP --- 
about_page = st.Page(
    page="views/about_me.py",
    title="About Me",
    icon=":material/account_circle:",
    default=True
)

cartoonify_page = st.Page(
    page="views/cartoonify.py",
    title="Cartoonify",
    icon="💭",
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

pencil_page = st.Page(
    page="views/pencil_sketch.py",
    title="Pencil Sketch",
    icon="✏️"
)

colorize_page = st.Page(
    page="views/colorize_bw.py",
    title="Colorize BW",
    icon="🎨"
)

framework_page = st.Page(
    page="views/automation_framework.py",
    title="Frameworks",
    icon="📚")

dashboard_page = st.Page(
    page="views/dashboard.py",
    title="Automation Dashboard",
    icon="💨"
)

# --- NAVIGATION ---
pg = st.navigation(
    {
        "Info":[about_page],
        "ML Projects":[chatbot_page,crop_page,fifa_22,age_gender_page],
        "OpenCV":[cartoonify_page,pencil_page,colorize_page],
        "Automation":[framework_page,dashboard_page]   
    },position="sidebar"
)

layout_mode = "wide" if pg.url_path in ["automation_framework","FIFA_22_Simulator","chatbot"] else "centered"
st.set_page_config(layout=layout_mode)


st.logo("assets/logo.png")
st.sidebar.text("Made with ❤️ by Solomon")

# --- RN NAVIGATION ---
pg.run()