import streamlit as st
import pandas as pd
import os
import pickle
from pathlib import Path

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Crop Recommendation AI | Solomon J",
    page_icon="🌱",
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
        max-width: 1200px;
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
    
    /* Sidebar styling */
    .stSidebar {
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(10px);
    }
    
    /* Number input styling */
    .stNumberInput > div > div > input {
        background: rgba(255, 255, 255, 0.9) !important;
        border: 2px solid rgba(102, 126, 234, 0.3) !important;
        border-radius: 10px !important;
        color: #2c3e50 !important;
        padding: 0.75rem !important;
        font-size: 1rem !important;
    }
    
    .stNumberInput > div > div > input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    }
    
    .stNumberInput label {
        color: #2c3e50 !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(45deg, #667eea, #764ba2) !important;
        color: white !important;
        border-radius: 25px !important;
        border: none !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
        margin-top: 1rem !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
    }
    
    /* Success message styling */
    .stSuccess {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%) !important;
        border: none !important;
        border-radius: 15px !important;
        color: white !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        padding: 1rem !important;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37) !important;
    }
    
    /* Warning message styling */
    .stWarning {
        background: linear-gradient(135deg, #ffc107 0%, #fd7e14 100%) !important;
        border: none !important;
        border-radius: 15px !important;
        color: white !important;
        font-weight: 500 !important;
        padding: 1rem !important;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37) !important;
    }
    
    /* Info card styling */
    .info-card {
        background: rgba(255, 255, 255, 0.9) !important;
        padding: 1.5rem !important;
        border-radius: 15px !important;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37) !important;
        border: 1px solid rgba(255, 255, 255, 0.18) !important;
        border-left: 5px solid #667eea !important;
        margin: 1rem 0 !important;
        backdrop-filter: blur(8px) !important;
    }
    
    .info-card h2, .info-card h3 {
        color: #2c3e50 !important;
        margin-bottom: 1rem !important;
        font-size: 1.1rem !important;
    }
    
    .info-card p, .info-card li {
        color: #2c3e50 !important;
        line-height: 1.6 !important;
        margin: 0.5rem 0 !important;
    }
    
    /* Parameter card styling */
    .parameter-card {
        background: rgba(255, 255, 255, 0.9);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        border: 1px solid rgba(255, 255, 255, 0.18);
        backdrop-filter: blur(8px);
        margin: 1rem 0;
    }
    
    .parameter-title {
        color: #2c3e50;
        font-size: 1.3rem;
        font-weight: bold;
        margin-bottom: 1.5rem;
        text-align: center;
        background: linear-gradient(45deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Feature highlight cards */
    .feature-highlight {
        background: rgba(255, 255, 255, 0.9);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        border: 1px solid rgba(255, 255, 255, 0.18);
        backdrop-filter: blur(8px);
        margin: 1rem 0;
        text-align: center;
        transition: transform 0.3s ease;
    }
    
    .feature-highlight:hover {
        transform: translateY(-5px);
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        background: linear-gradient(45deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .feature-text {
        color: #2c3e50;
        font-weight: 600;
        font-size: 1rem;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: rgba(102, 126, 234, 0.1) !important;
        border-radius: 10px !important;
        color: #2c3e50 !important;
        font-weight: 600 !important;
    }
    
    .streamlit-expanderContent {
        background: rgba(255, 255, 255, 0.5) !important;
        border-radius: 0 0 10px 10px !important;
        backdrop-filter: blur(4px) !important;
    }
    
    /* Section headers */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #2c3e50 !important;
        font-weight: bold !important;
    }
    
    /* Status badge */
    .status-badge {
        display: inline-block;
        background: linear-gradient(45deg, #28a745, #20c997);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
        margin: 0.2rem 0;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2rem;
        }
        
        .parameter-card {
            padding: 1rem;
        }
        
        .info-card {
            padding: 1rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# --- LOAD MODEL ---
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
model_path = os.path.join(ROOT_DIR, 'data/crop', "gaussian_model.pkl")

@st.cache_resource
def load_crop_model():
    with open(model_path, "rb") as f:
        return pickle.load(f)

loaded_model = load_crop_model()

# --- MAIN TITLE ---
st.markdown('<h1 class="main-title">🌱 Smart Crop Recommendation AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">AI-powered precision agriculture for optimal crop selection</p>', unsafe_allow_html=True)

# --- FEATURE HIGHLIGHTS ---
st.markdown("### 🚀 Why Use AI for Crop Recommendation?")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="feature-highlight">
        <div class="feature-icon">🎯</div>
        <div class="feature-text">Precision Agriculture</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-highlight">
        <div class="feature-icon">📊</div>
        <div class="feature-text">Data-Driven Decisions</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-highlight">
        <div class="feature-icon">💰</div>
        <div class="feature-text">Maximize Yield</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="feature-highlight">
        <div class="feature-icon">🌍</div>
        <div class="feature-text">Sustainable Farming</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# --- MAIN INTERFACE ---
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    <div class="parameter-card">
        <div class="parameter-title">🧪 Soil & Environmental Parameters</div>
    """, unsafe_allow_html=True)
    
    # Soil Nutrients Section
    st.markdown("#### 🧪 Soil Nutrients (NPK)")
    
    col_n, col_p, col_k = st.columns(3)
    with col_n:
        N = st.number_input(
            "Nitrogen (N)",
            min_value=1,
            max_value=10000,
            step=1,
            value=90,
            help="Nitrogen content in soil (mg/kg)"
        )
    
    with col_p:
        P = st.number_input(
            "Phosphorus (P)",
            min_value=1,
            max_value=10000,
            step=1,
            value=42,
            help="Phosphorus content in soil (mg/kg)"
        )
    
    with col_k:
        K = st.number_input(
            "Potassium (K)",
            min_value=1,
            max_value=10000,
            step=1,
            value=43,
            help="Potassium content in soil (mg/kg)"
        )
    
    st.markdown("#### 🌡️ Climate Conditions")
    
    col_temp, col_hum = st.columns(2)
    with col_temp:
        temperature = st.number_input(
            "Temperature (°C)",
            min_value=0.00,
            max_value=100.00,
            value=25.0,
            step=0.1,
            help="Average temperature in Celsius"
        )
    
    with col_hum:
        humidity = st.number_input(
            "Humidity (%)",
            min_value=0.00,
            max_value=100.00,
            value=80.0,
            step=0.1,
            help="Relative humidity percentage"
        )
    
    col_ph, col_rain = st.columns(2)
    with col_ph:
        ph = st.number_input(
            "Soil pH",
            min_value=0.00,
            max_value=14.00,
            value=6.5,
            step=0.1,
            help="Soil pH level (0-14 scale)"
        )
    
    with col_rain:
        rainfall = st.number_input(
            "Rainfall (mm)",
            min_value=0.00,
            max_value=1000.00,
            value=200.0,
            step=1.0,
            help="Annual rainfall in millimeters"
        )
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Prediction Button and Results
    if st.button("🔮 Get AI Recommendation", type="primary"):
        xvalue = [[N, P, K, temperature, humidity, ph, rainfall]]
        y_predict = loaded_model.predict(xvalue)
        
        st.success(f"🌾 **{y_predict[0].capitalize()}** is recommended by AI for your farm conditions!")
        
        # Additional information based on prediction
        crop_info = {
            "rice": "🍚 Rice thrives in warm, humid conditions with consistent water supply.",
            "wheat": "🌾 Wheat grows best in moderate climates with well-drained soil.",
            "corn": "🌽 Corn requires warm temperatures and adequate rainfall for optimal growth.",
            "cotton": "☁️ Cotton needs hot weather and moderate rainfall for best yields.",
            "sugarcane": "🎋 Sugarcane grows well in tropical climates with high humidity.",
        }
        
        crop_name = y_predict[0].lower()
        if crop_name in crop_info:
            st.info(crop_info[crop_name])
        
        st.warning("⚠️ **Disclaimer:** This AI application is for educational and demonstration purposes only. Please consult with agricultural experts before making farming decisions.")

with col2:
    st.markdown("### 📊 Input Summary")
    
    # Display current inputs in a nice format
    st.markdown(f"""
    <div class="info-card">
        <h3>🧪 Soil Analysis</h3>
        <p><strong>Nitrogen:</strong> {N} mg/kg</p>
        <p><strong>Phosphorus:</strong> {P} mg/kg</p>
        <p><strong>Potassium:</strong> {K} mg/kg</p>
        <p><strong>pH Level:</strong> {ph}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="info-card">
        <h3>🌡️ Climate Data</h3>
        <p><strong>Temperature:</strong> {temperature}°C</p>
        <p><strong>Humidity:</strong> {humidity}%</p>
        <p><strong>Rainfall:</strong> {rainfall} mm</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Model status
    st.markdown('<div class="status-badge">✅ AI Model Ready</div>', unsafe_allow_html=True)

# --- SIDEBAR INFORMATION ---
with st.sidebar:
    st.markdown("### 📘 About This Application")
    
    st.markdown("""
    <div class="info-card">
        <h3>🌱 Crop Recommendation System</h3>
        <p>This AI-powered system helps farmers make informed decisions about crop selection based on soil composition and environmental factors.</p>
        <br>
        <p><strong>Key Benefits:</strong></p>
        <p>• Optimize crop yield and quality</p>
        <p>• Reduce farming risks</p>
        <p>• Improve resource utilization</p>
        <p>• Support sustainable agriculture</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-card">
        <h3>🤖 AI Model Information</h3>
        <p><strong>Algorithm:</strong> Gaussian Naive Bayes</p>
        <p><strong>Input Features:</strong> 7 parameters</p>
        <p><strong>Output:</strong> Recommended crop type</p>
        <p><strong>Training:</strong> Agricultural dataset with soil and climate data</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-card">
        <h3>❓ How It Works</h3>
        <p>1. <strong>Input Parameters:</strong> Enter your soil and climate data</p>
        <p>2. <strong>AI Analysis:</strong> Machine learning model processes the data</p>
        <p>3. <strong>Recommendation:</strong> Get the most suitable crop for your conditions</p>
        <p>4. <strong>Decision Making:</strong> Use the recommendation to plan your farming strategy</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-card">
        <h3>💡 Tips for Best Results</h3>
        <p>• Ensure accurate soil testing data</p>
        <p>• Use recent weather data</p>
        <p>• Consider local agricultural conditions</p>
        <p>• Consult with local farming experts</p>
        <p>• Test recommendations on small plots first</p>
    </div>
    """, unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("---")
st.markdown("""
<div style="
    text-align: center; 
    padding: 1.5rem; 
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); 
    color: white; 
    border-radius: 15px; 
    margin-top: 2rem;
    box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
">
    <h3 style="margin: 0;">🌾 Smart Agriculture with AI</h3>
    <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">
        Empowering farmers with intelligent crop recommendations! 🚀
    </p>
</div>
""", unsafe_allow_html=True)