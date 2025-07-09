import json
import pickle
import tensorflow as tf
import numpy as np
from pathlib import Path
import os
import re
import fitz  # PyMuPDF
import joblib
import streamlit as st
from ai_edge_litert.interpreter import Interpreter

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="PDF Document Classifier | Solomon J",
    page_icon="📄",
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
    
    /* File uploader styling */
    .stFileUploader > div {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        border: 2px dashed rgba(102, 126, 234, 0.3);
        backdrop-filter: blur(8px);
        padding: 2rem;
        text-align: center;
        margin: 2rem 0;
    }
    
    .stFileUploader label {
        color: #2c3e50 !important;
        font-weight: 600 !important;
        font-size: 1.2rem !important;
    }
    
    /* Content area styling */
    .content-card {
        background: rgba(255, 255, 255, 0.9);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        border: 1px solid rgba(255, 255, 255, 0.18);
        backdrop-filter: blur(8px);
        margin: 1rem 0;
        max-height: 300px;
        overflow-y: auto;
    }
    
    /* Prediction result styling */
    .prediction-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
    }
    
    .prediction-card h2, .prediction-card h3 {
        color: white !important;
        margin: 0.5rem 0;
    }
    
    /* Category info styling */
    .category-info {
        background: rgba(255, 255, 255, 0.9);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        border: 1px solid rgba(255, 255, 255, 0.18);
        border-left: 5px solid #28a745;
        backdrop-filter: blur(8px);
        margin: 1rem 0;
    }
    
    /* Feature card styling */
    .feature-card {
        background: rgba(255, 255, 255, 0.9);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        border: 1px solid rgba(255, 255, 255, 0.18);
        backdrop-filter: blur(8px);
        margin: 1rem 0;
        text-align: center;
        transition: transform 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
        background: linear-gradient(45deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .feature-title {
        color: #2c3e50;
        font-size: 1.3rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    
    .feature-desc {
        color: #7f8c8d;
        line-height: 1.6;
    }
    
    /* Info card styling */
    .info-card {
        background: rgba(255, 255, 255, 0.9);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        border: 1px solid rgba(255, 255, 255, 0.18);
        border-left: 5px solid #667eea;
        backdrop-filter: blur(8px);
        margin: 1rem 0;
    }
    
    /* Success message styling */
    .stSuccess {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%) !important;
        border: none !important;
        border-radius: 15px !important;
        color: white !important;
        font-weight: 600 !important;
        font-size: 1.2rem !important;
        padding: 1.5rem !important;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37) !important;
    }
    
    /* Error message styling */
    .stError {
        background: linear-gradient(135deg, #dc3545 0%, #c82333 100%) !important;
        border: none !important;
        border-radius: 15px !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 1.5rem !important;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37) !important;
    }
    
    /* Warning message styling */
    .stWarning {
        background: linear-gradient(135deg, #ffc107 0%, #fd7e14 100%) !important;
        border: none !important;
        border-radius: 15px !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 1.5rem !important;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37) !important;
    }
    
    /* Status badges */
    .status-badge {
        display: inline-block;
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
        margin: 0.2rem 0;
    }
    
    /* Section headers */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #2c3e50 !important;
        font-weight: bold !important;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2rem;
        }
        
        .feature-card, .content-card {
            padding: 1rem;
        }
        
        .info-card {
            padding: 1rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# --- LOAD MODELS AND DATA ---
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
model_path = os.path.join(ROOT_DIR, 'data/pdf', "modeltf.tflite")
label_map = os.path.join(ROOT_DIR, 'data/pdf', "label_mapping.json")
preprocess_rules = os.path.join(ROOT_DIR, 'data/pdf', "preprocessing_rules.json")
tfid_vector_data = os.path.join(ROOT_DIR, 'data/pdf', "tfidf_vectorizer.pkl")

@st.cache_resource
def load_models():
    # Load the TensorFlow Lite model
    interpreter = Interpreter(model_path)
    interpreter.allocate_tensors()
    
    # Load supporting files
    with open(tfid_vector_data, "rb") as f:
        tfidf_vectorizer = joblib.load(f)
    
    with open(label_map, "r") as f:
        label_mapping = json.load(f)
    
    with open(preprocess_rules, "r") as f:
        preprocessing_rules = json.load(f)
    
    return interpreter, tfidf_vectorizer, label_mapping, preprocessing_rules

interpreter, tfidf_vectorizer, label_mapping, preprocessing_rules = load_models()

# --- CATEGORY INFORMATION ---
CATEGORY_INFO = {
    "Professional": {
        "icon": "💼",
        "description": "Business and professional documents",
        "examples": ["Resume", "CV", "Project Proposals", "Business Plans", "Professional Reports"]
    },
    "Finance": {
        "icon": "💰", 
        "description": "Financial and accounting documents",
        "examples": ["Invoice", "Budget", "Financial Statements", "Tax Documents", "Purchase Orders"]
    },
    "Communication": {
        "icon": "📧",
        "description": "Correspondence and messaging documents", 
        "examples": ["Letter", "Email", "Memo", "Internal Communications", "Announcements"]
    },
    "Information": {
        "icon": "📰",
        "description": "Informational and promotional content",
        "examples": ["Advertisement", "News Article", "Presentation", "Brochures", "Marketing Materials"]
    },
    "Forms": {
        "icon": "📝",
        "description": "Forms and structured documents",
        "examples": ["Application Form", "Questionnaire", "Survey", "Registration Forms", "Feedback Forms"]
    },
    "Technical": {
        "icon": "🔬",
        "description": "Technical and scientific documentation",
        "examples": ["Scientific Paper", "Technical Report", "Research Documentation", "Specifications", "Manuals"]
    }
}

# --- HELPER FUNCTIONS ---
def preprocess_text_with_json(text, rules):
    if rules.get("lowercase", False):
        text = text.lower()
    for rule in rules.get("regex_replace", []):
        pattern = rule["pattern"]
        replacement = rule["replacement"]
        text = re.sub(pattern, replacement, text)
    return text.strip()

def extract_text_from_pdf(file_bytes, password=None):
    try:
        text = ""
        with fitz.open(stream=file_bytes, filetype="pdf") as doc:
            # Check if PDF is password protected
            if doc.needs_pass:
                if password:
                    # Try to authenticate with provided password
                    auth_result = doc.authenticate(password)
                    if not auth_result:
                        return None, "WRONG_PASSWORD"
                else:
                    return None, "PASSWORD_REQUIRED"
            
            for page in doc:
                page_text = page.get_text()
                if page_text.strip():  # Only add non-empty pages
                    text += page_text + "\n"
        
        if not text.strip():
            return None, "NO_TEXT"
        
        return text, "SUCCESS"
    except Exception as e:
        return None, f"ERROR: {str(e)}"

# --- MAIN TITLE ---
st.markdown('<h1 class="main-title">📄 AI Document Classifier</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Intelligent PDF document classification using machine learning</p>', unsafe_allow_html=True)

# --- FEATURE OVERVIEW ---
st.markdown("### 🚀 Classifier Features")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🤖</div>
        <div class="feature-title">AI-Powered Classification</div>
        <div class="feature-desc">Advanced machine learning model trained on diverse document types</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📊</div>
        <div class="feature-title">6 Document Categories</div>
        <div class="feature-desc">Professional, Finance, Communication, Information, Forms, and Technical</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">⚡</div>
        <div class="feature-title">Instant Results</div>
        <div class="feature-desc">Fast text extraction and classification with detailed analysis</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# --- MAIN INTERFACE ---
st.markdown("### 📤 Upload Your PDF Document")

uploaded_file = st.file_uploader(
    "Choose a PDF file for classification",
    type=["pdf"],
    help="Upload English PDF documents for best classification accuracy"
)

if uploaded_file:
    # Read file bytes once and store them
    file_bytes = uploaded_file.read()
    
    # Initialize session state for password
    if 'pdf_password' not in st.session_state:
        st.session_state.pdf_password = ""
    if 'password_required' not in st.session_state:
        st.session_state.password_required = False
    if 'wrong_password' not in st.session_state:
        st.session_state.wrong_password = False
    
    # First attempt to extract text
    with st.spinner("📖 Extracting text from PDF..."):
        raw_text, status = extract_text_from_pdf(file_bytes)
    
    # Handle password-protected PDFs
    if status == "PASSWORD_REQUIRED":
        st.session_state.password_required = True
        st.warning("🔒 **Password Protected PDF Detected**")
        st.info("This PDF requires a password to access. Please enter the password below:")
        
        password = st.text_input(
            "🔑 Enter PDF Password:",
            type="password",
            help="Enter the password to unlock this PDF document"
        )
        
        if st.button("🔓 Unlock PDF", type="primary"):
            if password:
                with st.spinner("🔓 Unlocking PDF..."):
                    raw_text, status = extract_text_from_pdf(file_bytes, password)
                
                if status == "WRONG_PASSWORD":
                    st.error("❌ **Incorrect Password**\n\nThe password you entered is incorrect. Please try again.")
                elif status == "SUCCESS":
                    st.success("✅ **PDF Unlocked Successfully!**")
                    st.session_state.password_required = False
                    # Continue with processing (code below will handle this)
                else:
                    st.error(f"❌ **Error**: {status}")
            else:
                st.error("Please enter a password to unlock the PDF.")
        
        # Stop here if password is still required
        if status == "PASSWORD_REQUIRED" or status == "WRONG_PASSWORD":
            st.stop()
            
    elif status == "WRONG_PASSWORD":
        st.error("❌ **Incorrect Password**\n\nThe password you entered is incorrect. Please try again.")
        st.stop()
        
    elif status == "NO_TEXT":
        st.warning("⚠️ **No Text Found**\n\nThis PDF appears to contain no extractable text. It might be a scanned document or image-based PDF.")
        st.stop()
        
    elif status.startswith("ERROR"):
        st.error(f"❌ **Processing Error**\n\n{status}")
        st.stop()
    
    # If we reach here, we have successfully extracted text
    if status == "SUCCESS":
        # Success - process the document
        raw_text_truncated = " ".join(raw_text.split()[:1000])  # Limit to first 1000 words
        
        with st.spinner("🧹 Preprocessing text..."):
            preprocessed_text = preprocess_text_with_json(raw_text_truncated, preprocessing_rules)
        
        with st.spinner("🔮 Classifying document..."):
            # Transform text to TF-IDF vector
            tfidf_vector = tfidf_vectorizer.transform([preprocessed_text])
            input_data = np.array(tfidf_vector.todense(), dtype=np.float32)
            
            # Inference
            input_details = interpreter.get_input_details()
            output_details = interpreter.get_output_details()
            interpreter.set_tensor(input_details[0]['index'], input_data)
            interpreter.invoke()
            output_data = interpreter.get_tensor(output_details[0]['index'])
            
            predicted_index = int(np.argmax(output_data))
            confidence = float(np.max(output_data))
            predicted_label = label_mapping.get(str(predicted_index), "Unknown")
        
        # Display Results
        st.markdown("### 🎯 Classification Results")
        
        # Main prediction display
        if predicted_label in CATEGORY_INFO:
            category_info = CATEGORY_INFO[predicted_label]
            
            st.markdown(f"""
            <div class="prediction-card">
                <h2>{category_info['icon']} Document Category: {predicted_label}</h2>
                <h3>Confidence: {confidence:.2%}</h3>
                <p>{category_info['description']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Category details
            st.markdown(f"""
            <div class="category-info">
                <h4>📋 Typical {predicted_label} Documents Include:</h4>
                <p>• {' • '.join(category_info['examples'])}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.success(f"🔮 **Predicted Category:** {predicted_label} (Confidence: {confidence:.2%})")
        
        # Document analysis
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📝 Extracted Text Preview")
            st.markdown(f"""
            <div class="content-card">
                <p><strong>Word Count:</strong> {len(raw_text_truncated.split())} words (truncated)</p>
                <p><strong>Character Count:</strong> {len(raw_text_truncated)} characters</p>
                <hr>
                {raw_text_truncated}
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("### 🧹 Preprocessed Text")
            st.markdown(f"""
            <div class="content-card">
                <p><strong>Processed Length:</strong> {len(preprocessed_text)} characters</p>
                <p><strong>Language:</strong> English (optimized)</p>
                <hr>
                {preprocessed_text}
            </div>
            """, unsafe_allow_html=True)

# --- SIDEBAR INFORMATION ---
with st.sidebar:
    st.header("📄 About PDF Classifier")
    
    st.write("**AI-powered document classification system that automatically categorizes PDF documents into 6 main categories.**")
    
    st.header("📂 Document Categories")
    for category, info in CATEGORY_INFO.items():
        st.write(f"**{info['icon']} {category}**")
        st.write(f"• {info['description']}")
        st.write("")
    
    st.header("🔧 Technical Details")
    st.write("**Model:** TensorFlow Lite")
    st.write("**Features:** TF-IDF Vectorization")
    st.write("**Language:** English (optimized)")
    st.write("**Input:** PDF text content")
    st.write("**Output:** Document category + confidence")
    
    st.header("💡 Usage Tips")
    st.write("• Works best with English documents")
    st.write("• Supports password-protected PDFs")
    st.write("• Handles various PDF formats")
    st.write("• Scanned documents may have limited accuracy")
    st.write("• Text-based PDFs work best")
    st.write("• Enter password when prompted for locked PDFs")
    
    st.header("📱 Mobile App")
    st.write("This classifier is also available in a mobile app:")
    st.markdown("[📱 PDF Genie Lite](https://play.google.com/store/apps/details?id=com.solomonj.androidreaderlite&hl=en_IN)")
    
    # Status
    st.success("🤖 AI Model Loaded")
    st.info("📄 Ready for Classification")

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
    <h3 style="margin: 0;">🚀 Intelligent Document Organization</h3>
    <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">
        Streamline your document workflow with AI-powered classification! 📄
    </p>
</div>
""", unsafe_allow_html=True)