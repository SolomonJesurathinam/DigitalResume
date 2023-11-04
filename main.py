import streamlit as st
from pathlib import Path
from PIL import Image

# --- PATH SETTINGS ---
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
css_file = current_dir / "styles" / "main.css"
resume_file = current_dir / "assets" / "SolomonResume.pdf"
profile_pic = current_dir / "assets" / "profilepic.png"

# --- GENERAL SETTINGS ---
PAGE_TITLE = "Digital CV | Solomon J"
PAGE_ICON = ":wave:"
NAME = "Solomon Jesurathinam"
DESCRIPTION = """
Automation Engineer, Functional Tester, Test Lead, Data Science, Android Development
"""
EMAIL = "solomon258@gmail.com"
SOCIAL_MEDIA={
    "LinkedIn":"https://www.linkedin.com/in/solomon-jesurathinam-a3a80723/",
    "Github":"https://github.com/SolomonJesurathinam",
    "Android":"https://play.google.com/store/apps/developer?id=Solomon+Jesurathinam"
}
PROJECTS={
    "🥇 ML Projects":"https://solomonjesurathinam-mlprojects-homepage-5sdkej.streamlit.app/",
    "📷 OPEN CV":"https://solomonjesurathinam-opencvprojects-homepage-1ujplw.streamlit.app/",
    "📓 Ipynb Converter":"https://ipynbconverter.streamlit.app/",
    "👨‍🦱 Saloon Management":"https://saloonmanagement.streamlit.app/"
}

st.set_page_config(page_title=PAGE_TITLE,page_icon=PAGE_ICON)

# --- LOAD CSS, PDF & PROFILE PIC ---
with open(css_file) as f:
    st.markdown("<style>{}</style>".format(f.read()),unsafe_allow_html=True)
with open(resume_file,"rb") as pdf_file:
    PDFByte = pdf_file.read()
profile_pic = Image.open(profile_pic)

# --- HERO SECTION ---
col1, col2 = st.columns(2,gap="small")
with col1:
    st.image(profile_pic,width=230)
with col2:
    st.title(NAME)
    st.write(DESCRIPTION)
    st.download_button(
        label="⏬ Download Resume",
        data=PDFByte,
        file_name=resume_file.name,
        mime="application/octet-stream"
    )
    st.write("📫",EMAIL)

# --- SOCIAL LINKS ---
st.write("#")
cols = st.columns(len(SOCIAL_MEDIA))
for index, (platform,link) in enumerate(SOCIAL_MEDIA.items()):
    cols[index].write(f"[{platform}]({link})")

# --- EXPERIENCE ---
st.write("#")
st.subheader("Professional Experience & Qualifications")
st.write("""
- 🔅 9.10 years of IT experience with prime focus in Automation testing
- 🔅 Strong knowledge in Test Automation using Tools like Java, Selenium WebDriver, Maven, Tosca
- 🔅 Strong Knowledge in creating hybrid frameworks from scratch using TestNG, Cucumber and Data driven.
- 🔅 Expertise in functional testing the application
- 🔅 Experience in QA Agile testing (Scrum) with extensive knowledge of agile
- 🔅 Specialized in different Testing Methodologies – Smoke, Regression, End to End Flow & Ad-hoc
""")

st.write("#")
st.subheader("Personal Developments & Experiences")
st.write("""
- 🥷 Have completed DataScience course and have intermediate knowledge on Machine learning
- 🥷 Created a couple of Machine learning projects
- 🥷 Have intermediate knowledge on Android development
- 🥷 Created a couple of Android applications and they are available in playstore
- 🥷 Intermediate experience in Streamlit framework for creating web applications
""")

st.write("#")
st.subheader("Hard Skills")
st.write("""
- 💻 Programming: Java, Python, SQL
- ⚙️ Selenium with Java (WebDriver)
- ♻️ ML modelling (Logistic/linear regression, decision trees, tensorflow)
- 📱 Android Development
""")

# --- WORK HISTORY ---
st.write("#")
st.subheader("Work History")
st.write("---")

#--- JOB 1 ---
st.write("***Test Lead | Accenture***")
st.write("07/2017 - Present")
st.write("""
- Implementation of Page Object Model automation framework in Selenium using Java
- Managing and Mentoring Offshore team of 6 by assigning task and taking responsibilities on task
ownership of each sprint
- Engaging in all agile ceremonies.
- Involved in test estimation, test planning for automation project, Defect review meeting, Sign off
release for testing
- Reviewed all test cases and test scripts for quality and identified additional areas to review
- Creating weekly status reports and daily status reports on the test automation progress.
""")

#--- JOB 2 ---
st.write("#")
st.write("***Senior Quality analyst | Anjanasoft Solutions***")
st.write("11/2013 - 07/2017")
st.write("""
- Executed End to End Adhoc testing in Functional and Regression regions.
- Interacting with Onsite Manager for preparing the test result and documentation on daily basis
- Trained freshers for the testing team and helped the team in floor for any clarifications
- Collaborated effectively with the other Development Managers, Product Managers, and Operations
team to deliver end-to-end quality in our products
""")

