import streamlit as st
from pathlib import Path

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Android Apps Portfolio | Solomon J",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ENHANCED STYLING ---
st.markdown("""
<style>
    /* Show header with styling */
    header[data-testid="stHeader"] {
        visibility: visible !important;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%) !important;
        height: 60px;
    }
    
    header[data-testid="stHeader"] * {
        color: white !important;
    }
    
    header[data-testid="stHeader"] button {
        color: white !important;
        border-color: rgba(255, 255, 255, 0.3) !important;
    }
    
    header[data-testid="stHeader"] button:hover {
        background-color: rgba(255, 255, 255, 0.1) !important;
    }
    
    header[data-testid="stHeader"] svg {
        fill: white !important;
        color: white !important;
    }

    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Main app background */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        min-height: 100vh;
    }
    
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    
    /* Main title styling */
    .main-title {
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        font-style: italic;
    }
    
    /* App card styling */
    .app-card {
        background: rgba(255, 255, 255, 0.9);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(31, 38, 135, 0.37);
        border: 1px solid rgba(255, 255, 255, 0.18);
        backdrop-filter: blur(10px);
        margin: 2rem 0;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .app-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 20px 60px rgba(31, 38, 135, 0.5);
    }
    
    .app-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 5px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    /* App header styling */
    .app-header {
        display: flex;
        align-items: center;
        margin-bottom: 1rem;
        flex-wrap: wrap;
        gap: 1rem;
    }
    
    .app-icon {
        font-size: 3rem;
        margin-right: 1rem;
        background: linear-gradient(45deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .app-title {
        color: #2c3e50;
        font-size: 1.8rem;
        font-weight: bold;
        margin: 0;
        flex: 1;
    }
    
    .app-category {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 500;
    }
    
    /* App metrics styling */
    .app-metrics {
        display: flex;
        gap: 1rem;
        margin: 1rem 0;
        flex-wrap: wrap;
    }
    
    .metric-item {
        background: rgba(102, 126, 234, 0.1);
        padding: 0.5rem 1rem;
        border-radius: 15px;
        border: 1px solid rgba(102, 126, 234, 0.2);
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 0.9rem;
        color: #2c3e50;
        font-weight: 500;
    }
    
    .rating-stars {
        color: #ffd700;
    }
    
    .download-count {
        color: #28a745;
    }
    
    /* Feature list styling */
    .feature-list {
        background: rgba(102, 126, 234, 0.05);
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    
    .feature-list h4 {
        color: #2c3e50;
        margin-bottom: 1rem;
        font-size: 1.2rem;
    }
    
    .feature-item {
        color: #555;
        margin: 0.5rem 0;
        padding-left: 1rem;
        position: relative;
    }
    
    .feature-item::before {
        content: '✓';
        position: absolute;
        left: 0;
        color: #28a745;
        font-weight: bold;
    }
    
    /* Download button styling */
    .download-btn {
        display: inline-block;
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        padding: 0.8rem 2rem;
        border-radius: 25px;
        text-decoration: none;
        font-weight: 600;
        transition: all 0.3s ease;
        margin-top: 1rem;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .download-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
        text-decoration: none;
        color: white;
    }
    
    /* Stats section */
    .stats-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 3rem 2rem;
        border-radius: 20px;
        text-align: center;
        margin: 3rem 0;
        box-shadow: 0 10px 40px rgba(31, 38, 135, 0.37);
    }
    
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 2rem;
        margin-top: 2rem;
    }
    
    .stat-item {
        text-align: center;
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    
    .stat-label {
        font-size: 1rem;
        opacity: 0.9;
    }
    
    /* Section headers */
    .section-header {
        color: #2c3e50;
        font-weight: bold;
        font-size: 2rem;
        margin: 3rem 0 2rem 0;
        text-align: center;
        position: relative;
    }
    
    .section-header::after {
        content: '';
        position: absolute;
        bottom: -10px;
        left: 50%;
        transform: translateX(-50%);
        width: 100px;
        height: 3px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 2px;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2rem;
        }
        
        .app-card {
            padding: 1.5rem;
            margin: 1rem 0;
        }
        
        .app-header {
            flex-direction: column;
            text-align: center;
        }
        
        .stats-grid {
            grid-template-columns: 1fr;
            gap: 1rem;
        }
        
        .app-metrics {
            justify-content: center;
        }
    }
</style>
""", unsafe_allow_html=True)

# --- APP DATA WITH REAL INFORMATION ---
APPS_DATA = {
    "ipynb_viewer": {
        "title": "Ipynb Viewer",
        "icon": "📓",
        "category": "Development Tools",
        "description": "Simple and efficient Jupyter Notebook viewer for Android. View .ipynb files with clean interface and full compatibility. This application allows you to open ipynb files and view them on mobile or tablet with locally cached HTML rendering.",
        "features": [
            "View ipynb files with clean, crisp interface",
            "Save notebooks as PDF with customization options",
            "Multiple HTML rendering options supported",
            "Zoom functions for better readability",
            "Open notebooks from Google Drive and Google Colab",
            "Original Jupyter NbConversion as experimental feature",
            "100% offline processing for privacy",
            "Recent files saved to local storage for quick access"
        ],
        "url": "https://play.google.com/store/apps/details?id=com.solomonj.ipynbviewer",
        "rating": "4.4",
        "downloads": "146K+",
        "reviews": "162 reviews"
    },
    "ipynb_viewer_pro": {
        "title": "Ipynb Viewer Pro",
        "icon": "📔",
        "category": "Development Tools",
        "description": "Professional Jupyter Notebook viewer and converter with advanced features. Navigate, transform, and share notebooks with unprecedented ease. The quintessential Android tool for data scientists and enthusiasts.",
        "features": [
            "Smart file scanning and automatic organization",
            "PDF conversion with versatile export options",
            "Core & Lite rendering modes for flexibility",
            "Direct file opening from file manager",
            "Local and cloud storage access support",
            "Integrated search functionality for files",
            "Cloud conversion beta for enhanced mobility",
            "Privacy-focused with on-device processing"
        ],
        "url": "https://play.google.com/store/apps/details?id=com.solomonj.ipynbviewerpro",
        "rating": "4.5",
        "downloads": "1K+",
        "reviews": "19 reviews"
    },
    "pdf_genie": {
        "title": "PDF Genie Lite",
        "icon": "📄",
        "category": "Productivity",
        "description": "Your ultimate offline PDF companion, combining powerful tools and smart organization in one sleek app. Whether you're a student, professional, or everyday user, PDF Genie Lite gives you everything you need to manage PDF documents with ease.",
        "features": [
            "Fast and smooth PDF viewer with dark/light modes",
            "Merge, split, and compress PDFs efficiently",
            "Password protection and unlocking capabilities",
            "Scan to PDF using camera functionality",
            "Images to PDF converter for easy document creation",
            "Web to PDF for offline reading",
            "AI-powered automatic categorization (100% offline)",
            "Custom categories for personalized organization"
        ],
        "url": "https://play.google.com/store/apps/details?id=com.solomonj.androidreaderlite",
        "rating": "New",
        "downloads": "100+",
        "reviews": "New app"
    },
    "emi_buddy": {
        "title": "EMI Buddy",
        "icon": "💰",
        "category": "Finance",
        "description": "Take control of your loans and EMIs! Are you tired of juggling multiple loans and struggling to keep track of your EMI payments? EMI Buddy simplifies loan management, providing you with a clear and organized overview of your finances.",
        "features": [
            "Home dashboard with instant EMI overview",
            "Current and next month's EMI obligations at a glance",
            "Powerful EMI calculator with comprehensive loan overview",
            "Detailed amortization tables and insightful pie charts",
            "Mark EMIs as 'Paid' for accurate tracking",
            "Export EMI schedules to PDF and Excel",
            "Loan history management for active and closed loans",
            "Visual insights with detailed pie chart breakdowns"
        ],
        "url": "https://play.google.com/store/apps/details?id=com.solomonj.emitracker",
        "rating": "New",
        "downloads": "91+",
        "reviews": "New app"
    },
    "tamil_quiz": {
        "title": "Tamil Quiz",
        "icon": "🎯",
        "category": "Education",
        "description": "Fun and educational Tamil language quiz app designed for anyone who wants to test their general knowledge in Tamil language. With a user-friendly interface, the app offers variety of multiple-choice questions in various categories.",
        "features": [
            "Multiple-choice questions in Tamil language",
            "44 difficulty levels from beginner to expert",
            "Various general knowledge categories",
            "Progressive difficulty system for skill building",
            "User-friendly Tamil interface design",
            "Educational and entertaining content",
            "No data collection for privacy protection",
            "Encrypted data transmission for security"
        ],
        "url": "https://play.google.com/store/apps/details?id=com.solomonj.tamilquiz",
        "rating": "Not enough",
        "downloads": "273+",
        "reviews": "Growing"
    },
    "bible_quiz": {
        "title": "Bible OT Quiz",
        "icon": "📖",
        "category": "Education",
        "description": "Dive into the rich history and teachings of the Old Testament with our engaging quiz app. Designed to challenge and expand your knowledge, this app offers a variety of quizzes on different levels, ensuring a comprehensive learning experience.",
        "features": [
            "Challenging Old Testament quizzes",
            "Multiple difficulty levels for comprehensive learning",
            "Extra games for relaxation and fun",
            "Progress tracking to monitor your learning",
            "Customizable app experience with adjustable settings",
            "In-app feedback system for continuous improvement",
            "Interactive learning approach",
            "Biblical knowledge enhancement"
        ],
        "url": "https://play.google.com/store/apps/details?id=com.solomonj.biblequiz",
        "rating": "5.0",
        "downloads": "47+",
        "reviews": "6 reviews"
    }
}

# --- MAIN TITLE ---
st.markdown('<h1 class="main-title">📱 Android Apps Portfolio</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Innovative mobile applications designed and developed by Solomon Jesurathinam</p>', unsafe_allow_html=True)

# --- PORTFOLIO STATS ---
total_downloads = "147K+"
avg_rating = "4.6"
st.markdown(f"""
<div class="stats-section">
    <h2 style="margin: 0; color: white;">📊 Portfolio Overview</h2>
    <div class="stats-grid">
        <div class="stat-item">
            <div class="stat-number">6</div>
            <div class="stat-label">Published Apps</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">{total_downloads}</div>
            <div class="stat-label">Total Downloads</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">{avg_rating}⭐</div>
            <div class="stat-label">Average Rating</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">100%</div>
            <div class="stat-label">Privacy Focused</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Function to create app card
def create_app_card(app_key):
    app = APPS_DATA[app_key]
    features_html = "".join([f'<div class="feature-item">{feature}</div>' for feature in app['features']])
    
    return f"""
    <div class="app-card">
        <div class="app-header">
            <div class="app-icon">{app['icon']}</div>
            <div>
                <h3 class="app-title">{app['title']}</h3>
                <div class="app-category">{app['category']}</div>
            </div>
        </div>
        <div class="app-metrics">
            <div class="metric-item">
                <span class="rating-stars">⭐</span>
                <span>{app['rating']} ({app['reviews']})</span>
            </div>
            <div class="metric-item">
                <span class="download-count">📥</span>
                <span>{app['downloads']} downloads</span>
            </div>
        </div>
        <p style="color: #666; line-height: 1.6; margin-bottom: 1.5rem;">{app['description']}</p>
        <div class="feature-list">
            <h4>🌟 Key Features:</h4>
            {features_html}
        </div>
        <a href="{app['url']}" target="_blank" class="download-btn">
            📱 View on Google Play
        </a>
    </div>
    """

# --- DEVELOPMENT TOOLS SECTION ---
st.markdown('<div class="section-header">🛠️ Development Tools</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown(create_app_card("ipynb_viewer"), unsafe_allow_html=True)

with col2:
    st.markdown(create_app_card("ipynb_viewer_pro"), unsafe_allow_html=True)

# --- PRODUCTIVITY & FINANCE SECTION ---
st.markdown('<div class="section-header">💼 Productivity & Finance</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown(create_app_card("pdf_genie"), unsafe_allow_html=True)

with col2:
    st.markdown(create_app_card("emi_buddy"), unsafe_allow_html=True)

# --- EDUCATION SECTION ---
st.markdown('<div class="section-header">📚 Educational Apps</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown(create_app_card("tamil_quiz"), unsafe_allow_html=True)

with col2:
    st.markdown(create_app_card("bible_quiz"), unsafe_allow_html=True)

# --- DEVELOPER HIGHLIGHTS SECTION ---
st.markdown('<div class="section-header">🏆 Developer Achievements</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style="
        background: rgba(255, 255, 255, 0.9);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 5px 20px rgba(31, 38, 135, 0.2);
        border-left: 4px solid #28a745;
    ">
        <h3 style="color: #28a745; margin: 0;">🎯 Specialized Focus</h3>
        <p style="color: #666; margin: 1rem 0;">Data Science & Productivity tools for mobile platforms</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="
        background: rgba(255, 255, 255, 0.9);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 5px 20px rgba(31, 38, 135, 0.2);
        border-left: 4px solid #17a2b8;
    ">
        <h3 style="color: #17a2b8; margin: 0;">🔒 Privacy First</h3>
        <p style="color: #666; margin: 1rem 0;">All apps prioritize user privacy with offline processing</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="
        background: rgba(255, 255, 255, 0.9);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 5px 20px rgba(31, 38, 135, 0.2);
        border-left: 4px solid #ffc107;
    ">
        <h3 style="color: #e0a800; margin: 0;">🚀 Innovation</h3>
        <p style="color: #666; margin: 1rem 0;">AI-powered features and cutting-edge mobile solutions</p>
    </div>
    """, unsafe_allow_html=True)

# --- USER TESTIMONIALS SECTION ---
st.markdown('<div class="section-header">💬 User Testimonials</div>', unsafe_allow_html=True)

testimonials = [
    {
        "text": "I've been using Ipynb Viewer for two months, and it's been a good experience overall. The app is simple to use, which is its best feature.",
        "author": "Mohammad Al Faied",
        "app": "Ipynb Viewer",
        "rating": "⭐⭐⭐⭐"
    },
    {
        "text": "This is a really really helpful app, works really well, thanks to the creators. The functionality is exactly what I needed.",
        "author": "Alaa Ashraf",
        "app": "Ipynb Viewer",
        "rating": "⭐⭐⭐⭐⭐"
    },
    {
        "text": "Simple no fuss ipynb viewer! Would be great if you could add the collapse section/subsection feature!",
        "author": "Bharath Kumar",
        "app": "Ipynb Viewer",
        "rating": "⭐⭐⭐⭐"
    }
]

cols = st.columns(len(testimonials))
for i, testimonial in enumerate(testimonials):
    with cols[i]:
        st.markdown(f"""
        <div style="
            background: rgba(255, 255, 255, 0.9);
            padding: 1.5rem;
            border-radius: 15px;
            box-shadow: 0 5px 20px rgba(31, 38, 135, 0.2);
            border-top: 4px solid #667eea;
            margin: 1rem 0;
        ">
            <p style="color: #555; font-style: italic; margin-bottom: 1rem;">"{testimonial['text']}"</p>
            <div style="text-align: right;">
                <strong style="color: #2c3e50;">{testimonial['author']}</strong><br>
                <small style="color: #666;">{testimonial['app']}</small><br>
                <span>{testimonial['rating']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# --- SIDEBAR INFORMATION ---
with st.sidebar:
    st.header("📱 App Categories & Stats")
    
    st.markdown("""
    **🛠️ Development Tools**
    • Ipynb Viewer (146K+ downloads, 4.4⭐)
    • Ipynb Viewer Pro (1K+ downloads, 4.5⭐)
    
    **💼 Productivity**
    • PDF Genie Lite (100+ downloads, New)
    
    **💰 Finance**
    • EMI Buddy (91+ downloads, New)
    
    **📚 Education**
    • Tamil Quiz (273+ downloads, Not enough ratings)
    • Bible OT Quiz (47+ downloads, 5.0⭐)
    """)
    
    st.header("🔧 Technologies & Skills")
    st.write("• **Android Studio** - Primary IDE")
    st.write("• **Java/Kotlin** - Core languages")
    st.write("• **TensorFlow Lite** - On-device AI")
    st.write("• **Jupyter NbConvert** - Notebook processing")
    st.write("• **PDF Libraries** - Document manipulation")
    st.write("• **Material Design** - Modern UI/UX")
    st.write("• **Firebase** - Backend integration")
    st.write("• **Privacy Engineering** - Data protection")
    
    st.header("🌟 Development Philosophy")
    st.write("• **User-Centric Design** - Based on real feedback")
    st.write("• **Privacy by Design** - Offline-first approach")
    st.write("• **Cross-Cultural** - English and Tamil support")
    st.write("• **Quality Focus** - Production-ready solutions")
    st.write("• **Continuous Innovation** - Regular updates")
    
    st.header("📊 Portfolio Impact")
    st.success("147K+ Total Downloads")
    st.info("4.6⭐ Average Rating")
    st.success("6 Active Applications")
    st.info("100% Privacy Focused")
    
    st.header("🔗 Developer Links")
    st.markdown("""
    [📱 Google Play Profile](https://play.google.com/store/apps/developer?id=Solomon+J&hl=en_IN)
    
    **Location:** Chennai, Tamil Nadu, India
    """)

# --- TECHNICAL SPECIFICATIONS SECTION ---
st.markdown('<div class="section-header">⚙️ Technical Specifications</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div style="
        background: rgba(255, 255, 255, 0.9);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 5px 20px rgba(31, 38, 135, 0.2);
    ">
        <h3 style="color: #2c3e50;">🔒 Privacy & Security</h3>
        <ul style="color: #666;">
            <li><strong>Offline Processing:</strong> AI features work without internet</li>
            <li><strong>Local Storage:</strong> Data stays on your device</li>
            <li><strong>Minimal Permissions:</strong> Only necessary access requested</li>
            <li><strong>No Data Collection:</strong> Privacy-first approach</li>
            <li><strong>Encrypted Transit:</strong> Secure data transmission</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="
        background: rgba(255, 255, 255, 0.9);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 5px 20px rgba(31, 38, 135, 0.2);
    ">
        <h3 style="color: #2c3e50;">📱 Compatibility</h3>
        <ul style="color: #666;">
            <li><strong>Android 9+:</strong> Modern Android support</li>
            <li><strong>Tablet Optimized:</strong> Responsive design</li>
            <li><strong>Cloud Integration:</strong> Google Drive, Colab support</li>
            <li><strong>File Manager:</strong> Direct file opening</li>
            <li><strong>Export Options:</strong> PDF, Excel compatibility</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("---")
st.markdown("""
<div style="
    text-align: center; 
    padding: 2rem; 
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); 
    color: white; 
    border-radius: 20px; 
    margin-top: 3rem;
    box-shadow: 0 10px 40px rgba(31, 38, 135, 0.37);
">
    <h2 style="margin: 0;">🚀 Building Mobile Solutions That Matter</h2>
    <p style="margin: 1rem 0; opacity: 0.9; font-size: 1.1rem;">
        From Jupyter notebooks to financial tools - creating mobile experiences that solve real problems with 147K+ downloads! 📱
    </p>
    <div style="margin-top: 1.5rem;">
        <strong>Solomon Jesurathinam</strong> | Chennai, Tamil Nadu, India<br>
        <em>Android Developer & Mobile Solutions Architect</em>
    </div>
</div>
""", unsafe_allow_html=True)