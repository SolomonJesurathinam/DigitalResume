import streamlit as st

# Info Section
about_page = st.Page(
    page="pages_about/about_me.py",
    title="Solomon's Digital Portfolio",
    icon="🚀",
    default=True
)

# ML Projects Section (Enhanced Icons & Titles)
chatbot_page = st.Page(
    page="pages_mlProjects/chatbot.py",
    title="AI Chat Bot",                    # Better title
    icon="🤖"                               # Robot icon (better than computer)
)

crop_page = st.Page(
    page="pages_mlProjects/Crop Recommendation.py",
    title="Smart Crop Recommendation",      # More descriptive title
    icon="🌾"                               # Wheat icon (better than plant)
)

fifa_22 = st.Page(
    page="pages_mlProjects/FIFA_22_Simulator.py",
    title="FIFA 22 Match Simulator",       # More descriptive title
    icon="⚽"                               # Perfect as is
)

age_gender_page = st.Page(
    page="pages_mlProjects/age_gender.py",
    title="Age & Gender Recognition",      # Better title
    icon="👤"                               # Person icon (better than child)
)

pdf_classify = st.Page(
    page="pages_mlProjects/pdf_classification.py",
    title="PDF Document Classifier",     
    icon="📄"                              
)

face_attendance_page = st.Page(
    page="pages_mlProjects/face_attendance.py",
    title="Face Attendance System",         # More descriptive title
    icon="🕵️‍♂️"                             # Detective (better than face
    )

# OpenCV Section (Enhanced Icons)
cartoonify_page = st.Page(
    page="pages_opencv/cartoonify.py",
    title="Photo Cartoonify",              # More descriptive
    icon="🎨"                               # Art palette (better than thought bubble)
)

pencil_page = st.Page(
    page="pages_opencv/pencil_sketch.py",
    title="Pencil Sketch Generator",       # More descriptive
    icon="✏️"                               # Perfect as is
)

colorize_page = st.Page(
    page="pages_opencv/colorize_bw.py",
    title="B&W Photo Colorizer",           # Better title
    icon="🌈"                               # Rainbow (better for colorizing)
)

# Automation Section (Enhanced Icons & Titles)
framework_page = st.Page(
    page="pages_automation/automation_framework.py",
    title="Test Frameworks",               # Cleaner title
    icon="🧪"                               # Test tube (better than books)
)

dashboard_page = st.Page(
    page="pages_automation/dashboard.py",
    title="Analytics Dashboard",           # More descriptive
    icon="📊"                               # Chart icon (better than wind)
)

#Android section
android_page = st.Page(
    page="pages_android/android_apps.py",
    title="Android Apps",
    icon="📱"  
)                            

# --- NAVIGATION WITH BEAUTIFUL SECTION ICONS ---
pg = st.navigation(
    {
        "ℹ️ About": [about_page],
        "🧠 ML Projects": [chatbot_page, crop_page, fifa_22, age_gender_page, pdf_classify, face_attendance_page],
        "👁️ Computer Vision": [cartoonify_page, pencil_page, colorize_page],
        "⚡ Automation": [framework_page, dashboard_page],
        "📱 Android": [android_page]
    },
    position="top"
)

# layout_mode = "wide" if pg.url_path in [
#     "automation_framework", "FIFA_22_Simulator", "chatbot", "dashboard", "age_gender","about_me"
# ] else "centered"

st.set_page_config(
    # page_title="Solomon's Digital Portfolio",
    # page_icon="🚀",
    # layout=layout_mode,
    initial_sidebar_state="expanded"
)

# Enhanced sidebar
st.sidebar.markdown("""
<div style="text-align: center; margin-top: 20px;">
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
    ">
        <h3 style="margin: 0; font-size: 1.2rem;">👨‍💻 Solomon J</h3>
        <p style="margin: 5px 0 0 0; font-size: 0.9rem; opacity: 0.9;">
            AI Engineer & Automation Expert
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

st.sidebar.text("Made with ❤️ by Solomon")

pg.run()