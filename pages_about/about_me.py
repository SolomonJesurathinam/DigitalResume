import streamlit as st
from pathlib import Path
from PIL import Image
from forms.contact import contact_form

# --- PAGE CONFIG ---
st.set_page_config(
    layout="wide",
)

# --- PATH SETTINGS ---
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
resume_file = current_dir.parent / "assets" / "SolomonResume.pdf"
profile_pic = current_dir.parent / "assets" / "profilepic.png"

# --- ENHANCED GENERAL SETTINGS ---
PAGE_TITLE = "Digital CV | Solomon J"
PAGE_ICON = "👨‍💻"
NAME = "Solomon Jesurathinam"
DESCRIPTION = """
🚀 Lead SDET | 🧪 Automation Architect | 🤖 ML Engineer | 📱 Android Developer
"""
EMAIL = "solomon.jesurathinam@gmail.com"
LOCATION = "Chennai, Tamil Nadu, India"
EXPERIENCE_YEARS = "11+"

SOCIAL_MEDIA = {
    "LinkedIn": "https://www.linkedin.com/in/solomon-jesurathinam-a3a80723/",
    "GitHub": "https://github.com/SolomonJesurathinam",
}

ANDROID_APPS = {
    "📱 Android Apps": "https://play.google.com/store/apps/developer?id=Solomon+J&hl=en_IN"
}

# --- LOAD ASSETS ---
try:
    with open(resume_file, "rb") as pdf_file:
        PDFByte = pdf_file.read()
except FileNotFoundError:
    st.error("Resume file not found.")
    PDFByte = None

try:
    profile_pic = Image.open(profile_pic)
except FileNotFoundError:
    st.warning("Profile picture not found.")
    profile_pic = None

# --- ENHANCED STYLING ---
st.markdown("""
<style>
    /* Show header but style it properly */
    header[data-testid="stHeader"] {
        visibility: visible !important;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%) !important;
        height: 60px;
    }
    
    /* Style header text and elements */
    header[data-testid="stHeader"] * {
        color: white !important;
    }
    
    /* Header toolbar styling */
    .stToolbar {
        color: white !important;
    }
    
    /* Header buttons styling */
    header[data-testid="stHeader"] button {
        color: white !important;
        border-color: rgba(255, 255, 255, 0.3) !important;
    }
    
    header[data-testid="stHeader"] button:hover {
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
    }
    
    /* Header icons */
    header[data-testid="stHeader"] svg {
        fill: white !important;
        color: white !important;
    }
    
    /* Hide only specific elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Custom gradient overlay for main background */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        z-index: -1;
        pointer-events: none;
    }
    
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
        background: transparent;
    }
    
    /* Header styling with gradient */
    .main-header {
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 0;
    }
    
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        font-style: italic;
    }
    
    /* Card styling with semi-transparent backgrounds */
    .info-card {
        background: rgba(255, 255, 255, 0.9);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        border: 1px solid rgba(255, 255, 255, 0.18);
        border-left: 5px solid #667eea;
        margin: 1rem 0;
        backdrop-filter: blur(8px);
    }
    
    .profile-stats {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        backdrop-filter: blur(8px);
    }
    
    .profile-stats h2, .profile-stats h3, .profile-stats p {
        color: white !important;
    }
    
    /* Location section styling */
    .location-section {
        background: rgba(255, 255, 255, 0.9) !important;
        padding: 1.5rem !important;
        border-radius: 15px !important;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37) !important;
        border-left: 5px solid #667eea !important;
        margin: 1rem 0 !important;
        backdrop-filter: blur(8px) !important;
    }
    
    .location-section h4 {
        color: #2c3e50 !important;
        margin-bottom: 0.5rem !important;
        margin-top: 1rem !important;
    }
    
    .location-section h4:first-of-type {
        margin-top: 0 !important;
    }
    
    .location-section p,
    .location-section div[data-testid="stMarkdownContainer"] p {
        color: #2c3e50 !important;
        margin: 0.3rem 0 !important;
    }
    
    /* Social links styling */
    .social-link {
        display: flex !important;
        align-items: center;
        padding: 0.8rem 1.2rem;
        background: rgba(255, 255, 255, 0.8);
        border-radius: 10px;
        text-decoration: none !important;
        color: #333 !important;
        transition: all 0.3s ease;
        border: 2px solid transparent;
        margin: 0.5rem 0;
        box-shadow: 0 4px 16px rgba(31, 38, 135, 0.2);
        backdrop-filter: blur(4px);
    }
    
    .social-link:hover {
        background: linear-gradient(45deg, #667eea, #764ba2) !important;
        color: white !important;
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
        text-decoration: none !important;
    }
    
    .social-link strong {
        color: inherit !important;
    }
    
    .android-apps-link {
        display: flex !important;
        align-items: center;
        padding: 0.8rem 1.2rem;
        background: rgba(232, 245, 232, 0.8);
        border-radius: 10px;
        text-decoration: none !important;
        color: #2d5a2d !important;
        transition: all 0.3s ease;
        border: 2px solid #28a745;
        margin: 0.5rem 0;
        box-shadow: 0 4px 16px rgba(31, 38, 135, 0.2);
        backdrop-filter: blur(4px);
    }
    
    .android-apps-link:hover {
        background: #28a745 !important;
        color: white !important;
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
        text-decoration: none !important;
    }
    
    .android-apps-link strong {
        color: inherit !important;
    }
    
    /* Timeline styling */
    .timeline-item {
        border-left: 3px solid #667eea;
        padding-left: 2rem;
        margin: 2rem 0;
        position: relative;
        background: rgba(255, 255, 255, 0.9);
        padding: 1.5rem 2rem;
        border-radius: 10px;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        border: 1px solid rgba(255, 255, 255, 0.18);
        backdrop-filter: blur(8px);
    }
    
    .timeline-item::before {
        content: '';
        position: absolute;
        left: -8px;
        top: 1.5rem;
        width: 13px;
        height: 13px;
        border-radius: 50%;
        background: #667eea;
        box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.9);
    }
    
    /* Skill tags */
    .skill-tag {
        display: inline-block;
        background: linear-gradient(45deg, #667eea, #764ba2) !important;
        color: white !important;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        margin: 0.2rem;
        font-size: 0.9rem;
        font-weight: 500;
        box-shadow: 0 4px 16px rgba(31, 38, 135, 0.2);
    }
    
    /* Interest icons */
    .interest-icon {
        font-size: 2rem;
        margin: 0.5rem;
        transition: transform 0.3s ease;
    }
    
    .interest-icon:hover {
        transform: scale(1.2);
    }
    
    .interest-text {
        margin: 0;
        font-weight: 500;
    }
    
    /* Footer with glassmorphism */
    .footer-card {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border-radius: 15px;
        margin-top: 2rem;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        backdrop-filter: blur(8px);
    }
    
    .footer-card h3, .footer-card p {
        color: white !important;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2rem;
        }
        
        .subtitle {
            font-size: 1rem;
        }
        
        .info-card, .location-info {
            padding: 1rem;
        }
        
        .timeline-item {
            padding: 1rem 1.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

@st.dialog("Contact Me")
def show_contact_form():
    contact_form()

# --- ENHANCED HERO SECTION ---
st.markdown('<h1 class="main-header">Solomon Jesurathinam</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">🚀 Lead SDET | 🧪 Automation Architect | 🤖 ML Engineer | 📱 Android Developer</p>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([2, 3, 2])

with col1:
    if profile_pic:
        st.image(profile_pic, width=280, use_container_width=True)
    else:
        st.markdown("""
        <div style="
            width: 280px; 
            height: 280px; 
            background: linear-gradient(135deg, #667eea, #764ba2);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 4rem;
            color: white;
            margin: 0 auto;
        ">
            👨‍💻
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="profile-stats">
        <h3 style="margin: 0;">Quick Stats</h3>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 1rem;">
            <div>
                <h2 style="margin: 0; font-size: 2rem;">11+</h2>
                <p style="margin: 0; opacity: 0.9;">Years Experience</p>
            </div>
            <div>
                <h2 style="margin: 0; font-size: 2rem;">50+</h2>
                <p style="margin: 0; opacity: 0.9;">Projects Delivered</p>
            </div>
            <div>
                <h2 style="margin: 0; font-size: 2rem;">8</h2>
                <p style="margin: 0; opacity: 0.9;">Team Members Led</p>
            </div>
            <div>
                <h2 style="margin: 0; font-size: 2rem;">10+</h2>
                <p style="margin: 0; opacity: 0.9;">Technologies Mastered</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Action buttons
    col_a, col_b = st.columns(2)
    
    with col_a:
        if PDFByte:
            st.download_button(
                label="📄 Download Resume",
                data=PDFByte,
                file_name=resume_file.name,
                mime="application/octet-stream",
                use_container_width=True,
                type="primary"
            )
    
    with col_b:
        if st.button("✉️ Contact Me", use_container_width=True, type="secondary"):
            show_contact_form()

with col3:
    # Create the location card using columns to avoid HTML issues
    st.markdown("""
    <style>
    .location-card {
        background: rgba(255, 255, 255, 0.9);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        border-left: 5px solid #667eea;
        margin: 1rem 0;
        backdrop-filter: blur(8px);
    }
    .location-card h4 {
        color: #2c3e50 !important;
        margin-bottom: 0.5rem !important;
    }
    .location-card p {
        color: #2c3e50 !important;
        margin: 0.3rem 0 !important;
    }
    </style>
    
    <div class="location-card">
    📍 <strong>Location</strong><br>
    Chennai, Tamil Nadu<br>
    India<br><br>
    
    🎯 <strong>Specialization</strong><br>
    • Test Automation<br>
    • Machine Learning<br>
    • Mobile Development<br>
    • Team Leadership
    </div>
    """, unsafe_allow_html=True)

# --- ENHANCED SOCIAL LINKS ---
st.markdown("### 🌐 Connect With Me")
social_col1, social_col2, social_col3 = st.columns(3)

social_icons = {"LinkedIn": "💼", "GitHub": "🐱"}

with social_col1:
    for platform, link in SOCIAL_MEDIA.items():
        icon = social_icons.get(platform, "🔗")
        st.markdown(f"""
        <a href="{link}" target="_blank" class="social-link">
            <span style="margin-right: 0.5rem; font-size: 1.2rem;">{icon}</span>
            <strong>{platform}</strong>
        </a>
        """, unsafe_allow_html=True)
        break  # Only show LinkedIn in first column

with social_col2:
    # Show GitHub
    github_link = SOCIAL_MEDIA["GitHub"]
    st.markdown(f"""
    <a href="{github_link}" target="_blank" class="social-link">
        <span style="margin-right: 0.5rem; font-size: 1.2rem;">🐱</span>
        <strong>GitHub</strong>
    </a>
    """, unsafe_allow_html=True)

with social_col3:
    for platform, link in ANDROID_APPS.items():
        st.markdown(f"""
        <a href="{link}" target="_blank" class="android-apps-link">
            <span style="margin-right: 0.5rem; font-size: 1.2rem;">📱</span>
            <strong>Android Apps</strong>
        </a>
        """, unsafe_allow_html=True)

# --- ENHANCED SKILLS SECTION ---
st.markdown("---")
st.markdown("### 💻 Technical Skills")

skill_categories = {
    "Programming Languages": ["Java", "Python", "SQL", "JavaScript"],
    "Automation Tools": ["Selenium", "Pytest", "TestNG", "Cucumber", "Tosca"],
    "DevOps & Tools": ["Git", "GitLab", "Jira", "Azure DevOps", "HP ALM"],
    "ML & Data Science": ["TensorFlow", "Scikit-learn", "Pandas", "NumPy"],
    "Mobile Development": ["Android Studio", "Java/XML", "Firebase"],
    "Web Technologies": ["Streamlit", "HTML/CSS", "REST APIs"]
}

for category, skills in skill_categories.items():
    st.markdown(f"**{category}:**")
    skills_html = "".join([f'<span class="skill-tag">{skill}</span>' for skill in skills])
    st.markdown(skills_html, unsafe_allow_html=True)
    st.write("")

# --- ENHANCED EXPERIENCE SECTION ---
st.markdown("---")
st.markdown("### 🏆 Professional Highlights")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="info-card">
        <h4>🎯 Core Expertise</h4>
        <ul style="list-style-type: none; padding: 0;">
            <li>🔸 11+ years in Test Automation & QA Leadership</li>
            <li>🔸 Expert in Selenium WebDriver with Java & Python</li>
            <li>🔸 Custom automation framework architect</li>
            <li>🔸 Agile/Scrum methodology specialist</li>
            <li>🔸 Team leadership & mentoring experience</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="info-card">
        <h4>🚀 Innovation & Growth</h4>
        <ul style="list-style-type: none; padding: 0;">
            <li>🔸 Data Science & Machine Learning projects</li>
            <li>🔸 Published Android applications</li>
            <li>🔸 Streamlit web application development</li>
            <li>🔸 Open source contributions</li>
            <li>🔸 Continuous learning & skill development</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# --- ENHANCED WORK HISTORY ---
st.markdown("---")
st.markdown("### 💼 Professional Journey")

# Job 1
st.markdown("""
<div class="timeline-item">
    <div class="job-title">🏢 Principal Software Engineer | Automation Test Engineer</div>
    <div class="job-details">
        <strong>Maveric Systems Limited</strong> | 📅 Dec 2023 – Present | 📍 Chennai, TN
    </div>
    <ul style="margin-top: 1rem;">
        <li>🎯 Architected Selenium + Java BDD framework for Natwest Group</li>
        <li>🐍 Developed Python Pytest automation framework</li>
        <li>👥 Led and mentored team of 8 automation engineers</li>
        <li>🚀 Created custom utilities improving delivery speed by 40%</li>
        <li>📚 Conducted regular training sessions on best practices</li>
        <li>✅ Ensured code quality through comprehensive reviews</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# Job 2
st.markdown("""
<div class="timeline-item">
    <div class="job-title">🏢 Test Lead</div>
    <div class="job-details">
        <strong>Accenture</strong> | 📅 Jul 2017 – Dec 2023 | 📍 Chennai, TN
    </div>
    <ul style="margin-top: 1rem;">
        <li>🏦 Built Selenium TestNG framework for Bank of America</li>
        <li>📊 Managed automation planning, execution & reporting</li>
        <li>👥 Led 6-member automation engineering team</li>
        <li>⚡ Delivered internal utilities for process acceleration</li>
        <li>🎓 Trained new joiners on automation tools & frameworks</li>
        <li>🔄 Streamlined CI/CD integration for automated testing</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# Job 3
st.markdown("""
<div class="timeline-item">
    <div class="job-title">🏢 Senior Quality Analyst</div>
    <div class="job-details">
        <strong>Anjana Software Solutions</strong> | 📅 Nov 2013 – Jul 2017 | 📍 Chennai, TN
    </div>
    <ul style="margin-top: 1rem;">
        <li>🌾 Performed manual & automation testing for agricultural applications</li>
        <li>🧪 Led SIT and regression testing initiatives</li>
        <li>🤖 Automated critical regression test scenarios</li>
        <li>🤝 Collaborated with product managers & development teams</li>
        <li>📈 Improved testing efficiency by 60% through automation</li>
        <li>👨‍🏫 Mentored junior QA engineers on domain knowledge</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# --- ENHANCED INTERESTS ---
st.markdown("---")
st.markdown("### 🎯 Interests & Hobbies")

interests = {
    "🎮": "PC Gaming",
    "🏏": "Cricket", 
    "⚽": "Football",
    "🏸": "Badminton",
    "🤖": "Machine Learning",
    "📱": "Mobile Development",
    "📚": "Continuous Learning",
    "🎵": "Music"
}

interest_cols = st.columns(4)
for i, (icon, interest) in enumerate(interests.items()):
    with interest_cols[i % 4]:
        st.markdown(f"""
        <div style="text-align: center; padding: 1rem; margin: 0.5rem 0;">
            <div class="interest-icon">{icon}</div>
            <p class="interest-text">{interest}</p>
        </div>
        """, unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("---")
st.markdown("""
<div class="footer-card" style="text-align: center; padding: 2rem;">
    <h3 style="margin: 0;">Ready to Collaborate?</h3>
    <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">
        Let's build something amazing together! 🚀
    </p>
</div>
""", unsafe_allow_html=True)