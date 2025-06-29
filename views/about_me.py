import streamlit as st
from pathlib import Path
from PIL import Image
from forms.contact import contact_form

# --- PATH SETTINGS ---
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
css_file = current_dir.parent / "styles" / "main.css"
resume_file = current_dir.parent / "assets" / "SolomonResume.pdf"
profile_pic = current_dir.parent / "assets" / "profilepic.png"

# --- GENERAL SETTINGS ---
PAGE_TITLE = "Digital CV | Solomon J"
PAGE_ICON = ":wave:"
NAME = "Solomon Jesurathinam"
DESCRIPTION = """
Lead SDET, Functional Tester, Machine Learning, Android Development
"""
SOCIAL_MEDIA={
    "LinkedIn":"https://www.linkedin.com/in/solomon-jesurathinam-a3a80723/",
    "Github":"https://github.com/SolomonJesurathinam",
    "Android":"https://play.google.com/store/apps/developer?id=Solomon+J&hl=en_IN"
}
PROJECTS={
    "🥇 Machine Learninig Projects":"https://solomonjesurathinam-mlprojects-homepage-5sdkej.streamlit.app/",
    "📷 OPEN CV Projects":"https://solomonjesurathinam-opencvprojects-homepage-1ujplw.streamlit.app/",
    "📓 Ipynb Converter - Converts Juyter ipynb format to pdf":"https://ipynbconverter.streamlit.app/",
    "👨‍🦱 Saloon Management - POS":"https://saloonmanagement.streamlit.app/"
}

st.set_page_config(page_title=PAGE_TITLE,page_icon=PAGE_ICON)

# --- LOAD CSS, PDF & PROFILE PIC ---
with open(css_file) as f:
    st.markdown("<style>{}</style>".format(f.read()),unsafe_allow_html=True)
with open(resume_file,"rb") as pdf_file:
    PDFByte = pdf_file.read()
profile_pic = Image.open(profile_pic)

@st.dialog("Contact Me")
def show_contact_form():
    contact_form()

# --- HERO SECTION ---
col1, col2 = st.columns(2,gap="small", vertical_alignment="center")
with col1:
    st.image(profile_pic,width=230)
with col2:
    st.title(NAME,anchor=False)
    st.write(DESCRIPTION)
    st.download_button(
        label="⏬ Download Resume",
        data=PDFByte,
        file_name=resume_file.name,
        mime="application/octet-stream"
    )
    if st.button("✉️ Contact Me"):
        show_contact_form()

# --- SOCIAL LINKS ---
st.write("#")
cols = st.columns(len(SOCIAL_MEDIA))
for index, (platform,link) in enumerate(SOCIAL_MEDIA.items()):
    cols[index].write(f"[{platform}]({link})")

# --- EXPERIENCE ---
st.write("#")
st.subheader("Professional Experience & Qualifications")
st.write("""
- 🔅 11+ years of IT experience with a primary focus on Automation Testing and QA leadership
- 🔅 Expertise in Selenium WebDriver with Java, Python (Pytest), TestNG, BDD (Cucumber), and Tosca
- 🔅 Strong experience in designing and implementing custom automation frameworks from scratch (POM, Hybrid)
- 🔅 Skilled in Functional, Smoke, Regression, End-to-End Flow, and Ad-hoc Testing
- 🔅 Excellent understanding of Agile/Scrum methodologies with real-time QA Agile Testing involvement
- 🔅 Proven track record of leading automation teams, conducting trainings, and driving testing best practices
""")

st.write("#")
st.subheader("Personal Developments & Experiences")
st.write("""
- 🥷 Completed a Data Science course with intermediate knowledge of Machine Learning
- 🥷 Built several ML projects using Python (regression, classification, decision trees, etc.)
- 🥷 Developed and published Android applications (available on Google Play Store)
- 🥷 Intermediate proficiency in using Streamlit for building data-driven web apps
""")

st.write("#")
st.subheader("Hard Skills")
st.write("""
- 💻 Programming: Java, Python, SQL
- ⚙️ Tools & Frameworks: Selenium (Java), Pytest, TestNG, Cucumber (BDD), Tosca, Rest Assured
- 🔧 DevOps & Utilities: Git, GitLab, Jira, HP ALM, Azure DevOps
- ♻️ ML Modeling: Logistic/Linear Regression, Decision Trees, TensorFlow
- 📱 Android App Development (Java/XML)
""")

# --- WORK HISTORY ---
st.write("#")
st.subheader("Work History")
st.write("---")

# JOB 1
st.write("💼", "**Principal Software Engineer | Automation Test Engineer** – Maveric Systems Limited")
st.write("📅 Dec 2023 – Present | 📍 Chennai, TN")
st.write("""
- Designed and implemented Selenium with Java BDD framework for Natwest Group client
- Developed Python-based Pytest automation framework for internal projects
- Built TestNG framework for internal applications
- Mentored and led a team of 8 automation engineers; conducted regular trainings
- Created custom automation utilities that improved delivery speed and quality
- Reviewed automation code and ensured adherence to industry best practices
""")

# JOB 2
st.write("💼", "**Test Lead** – Accenture")
st.write("📅 Jul 2017 – Dec 2023 | 📍 Chennai, TN")
st.write("""
- Created Selenium with Java TestNG POM framework for Bank of America projects
- Involved in automation planning, scripting, execution, and reporting for sprint releases
- Managed a 6-member team of automation engineers and provided technical mentorship
- Delivered internal utilities to accelerate automation processes
- Conducted trainings for new joiners in automation tools and frameworks
""")

# JOB 3
st.write("💼", "**Senior Quality Analyst** – Anjana Software Solutions")
st.write("📅 Nov 2013 – Jul 2017 | 📍 Chennai, TN")
st.write("""
- Performed manual and automation testing for Farmers client applications
- Led SIT and regression testing initiatives to ensure high-quality releases
- Automated regression test cases to streamline repeatable test scenarios
- Collaborated with product managers and development teams for requirements and feedback
- Trained junior QA engineers on testing processes and domain knowledge
""")

# --- INTERESTS ---
st.write("#")
st.subheader("Interests")
st.write("🎮 PC Gaming | 🏏 Cricket | ⚽ Football | 🏸 Badminton | 🤖 Machine Learning | 📱 Android Development")