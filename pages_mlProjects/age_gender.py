import streamlit as st
import tensorflow as tf
from pathlib import Path
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import load_model
import cv2
import numpy as np
import os
import av
from streamlit_webrtc import (
    WebRtcMode,
    webrtc_streamer,
    __version__ as st_webrtc_version,
)

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Age & Gender AI | Solomon J",
    page_icon="👁️‍🗨️",
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
        margin-bottom: 2rem;
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
    
    /* Radio button styling */
    .stRadio > div {
        background: rgba(255, 255, 255, 0.9);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        border: 1px solid rgba(255, 255, 255, 0.18);
        backdrop-filter: blur(8px);
        margin: 1rem 0;
    }
    
    .stRadio label {
        color: #2c3e50 !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
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
        margin: 1rem 0;
    }
    
    .stFileUploader label {
        color: #2c3e50 !important;
        font-weight: 600 !important;
    }
    
    /* Camera input styling */
    .stCameraInput > div {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        border: 1px solid rgba(255, 255, 255, 0.18);
        backdrop-filter: blur(8px);
        padding: 1rem;
        margin: 1rem 0;
    }
    
    /* Image display styling */
    .stImage {
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        overflow: hidden;
        margin: 1rem 0;
    }
    
    /* WebRTC styling */
    .stVideo {
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        overflow: hidden;
        margin: 1rem 0;
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
    
    .info-card a {
        color: #667eea !important;
        text-decoration: none !important;
    }
    
    .info-card a:hover {
        color: #764ba2 !important;
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
    
    /* Prediction result styling */
    .prediction-result {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        backdrop-filter: blur(8px);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: rgba(102, 126, 234, 0.1) !important;
        border-radius: 10px !important;
        color: #2c3e50 !important;
        font-weight: 500 !important;
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
    
    /* Status indicators */
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
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2rem;
        }
        
        .feature-card {
            padding: 1rem;
        }
        
        .info-card {
            padding: 1rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# --- LOAD MODELS AND PATHS ---
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
gender_path = current_dir.parent / "assets" / "models" / "gender_model_final.keras"
age_path = current_dir.parent / "assets" / "models" / "age_model_final.keras"
img_path = current_dir.parent / "views" / "img1.png"
classifier = current_dir.parent / "assets" / "models" / "haarcascade_frontalface_alt.xml"

# Load models
@st.cache_resource
def load_models():
    gender_model = load_model(gender_path)
    age_model = load_model(age_path)
    return gender_model, age_model

gender_model, age_model = load_models()

# --- MAIN TITLE ---
st.markdown('<h1 class="main-title">👁️‍🗨️ Age & Gender AI Predictor</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Advanced AI-powered facial analysis using deep learning models</p>', unsafe_allow_html=True)

# --- FEATURE OVERVIEW ---
st.markdown("### 🚀 Features")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📸</div>
        <div class="feature-title">Upload Images</div>
        <div class="feature-desc">Upload photos for instant age and gender prediction</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📷</div>
        <div class="feature-title">Camera Capture</div>
        <div class="feature-desc">Take live photos using your device camera</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🎥</div>
        <div class="feature-title">Live Stream</div>
        <div class="feature-desc">Real-time analysis with live video feed</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# --- PREDICTION FUNCTIONS ---
def load_and_preprocess_image(image_path):
    img = cv2.resize(image_path, (48, 48))
    img = img.astype('float32') / 255.0
    img = img.reshape(1, 48, 48, 1)
    return img

def predict_image(img):
    image = load_and_preprocess_image(img)
    gender_pred = gender_model.predict(image)
    age_pred = age_model.predict(image)
    pred_gender = "Female" if gender_pred[0][0] > 0.5 else "Male"
    pred_age = int(np.round(age_pred.flatten()[0] * 116))
    return pred_gender, pred_age

def predict(image):
    face_cascade = cv2.CascadeClassifier(classifier)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 255, 0), 2)
        gray_face_img = gray[y:y + h, x:x + w].copy()
        
        # Gender and Age Prediction
        gender, age = predict_image(gray_face_img)
        cv2.putText(image, f"{gender} - {age}", (x, y - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
    
    return image

def process_uploaded_image(input_image):
    if input_image is not None:
        bytes_data = input_image.getvalue()
        cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
        cv2_img = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
        
        # Keep original image separate
        original_img = cv2_img.copy()
        
        # Get prediction on a copy
        predicted_img = predict(cv2_img.copy())
        
        # Display results
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 📷 Original Image")
            st.image(original_img, use_container_width=True)
        with col2:
            st.markdown("#### 🎯 Prediction Results")
            st.image(predicted_img, use_container_width=True)
            
            # Add download button for predicted image
            predicted_img_bgr = cv2.cvtColor(predicted_img, cv2.COLOR_RGB2BGR)
            _, buffer = cv2.imencode('.png', predicted_img_bgr)
            
            st.download_button(
                label="📥 Download Prediction",
                data=buffer.tobytes(),
                file_name="age_gender_prediction.png",
                mime="image/png",
                type="primary",
                use_container_width=True
            )

# --- MAIN INTERFACE ---
st.markdown("### 🎛️ Choose Prediction Method")

radio_values = st.radio(
    label="Select how you'd like to predict age and gender:",
    options=("📸 Upload a Picture", "📷 Photo from Camera", "🎥 Live Feed"),
    help="Choose your preferred method for age and gender prediction"
)

if radio_values == "📸 Upload a Picture":
    st.markdown("#### 📤 Upload Your Image")
    input_image = st.file_uploader(
        "Choose an image file", 
        type=['png', 'jpg', 'jpeg'],
        help="Upload a clear photo with visible faces for best results"
    )
    if input_image:
        with st.spinner("🔍 Analyzing image..."):
            process_uploaded_image(input_image)

elif radio_values == "📷 Photo from Camera":
    st.markdown("#### 📷 Camera Capture")
    input_image = st.camera_input(
        "Take a photo for prediction",
        help="Make sure your face is clearly visible and well-lit"
    )
    if input_image:
        with st.spinner("🔍 Analyzing photo..."):
            bytes_data = input_image.getvalue()
            cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
            cv2_img = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
            
            # Keep original image separate
            original_img = cv2_img.copy()
            
            # Get prediction on a copy
            predicted_img = predict(cv2_img.copy())
            
            # Display results
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#### 📷 Original Photo")
                st.image(original_img, use_container_width=True)
            with col2:
                st.markdown("#### 🎯 Prediction Results")
                st.image(predicted_img, use_container_width=True)
                
                # Add download button for predicted image
                predicted_img_bgr = cv2.cvtColor(predicted_img, cv2.COLOR_RGB2BGR)
                _, buffer = cv2.imencode('.png', predicted_img_bgr)
                
                st.download_button(
                    label="📥 Download Prediction",
                    data=buffer.tobytes(),
                    file_name="camera_age_gender_prediction.png",
                    mime="image/png",
                    type="primary",
                    use_container_width=True
                )

elif radio_values == "🎥 Live Feed":
    st.markdown("#### 🎥 Live Video Analysis")
    
    # Global face cascade (from your original code)
    face_cascade = cv2.CascadeClassifier(classifier)
    
    def video_frame_callback(frame: av.VideoFrame) -> av.VideoFrame:
        image = frame.to_ndarray(format="bgr24")
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 5)

        for (x, y, w, h) in faces:
            face_gray = gray[y:y+h, x:x+w]
            face_input = load_and_preprocess_image(face_gray)

            gender_pred = gender_model.predict(face_input)
            age_pred = age_model.predict(face_input)

            gender = "Female" if gender_pred[0][0] > 0.5 else "Male"
            age = int(np.round(age_pred.flatten()[0] * 116))

            label = f"{gender}, {age}"
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 255), 2)
            cv2.putText(image, label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        return av.VideoFrame.from_ndarray(image, format="bgr24")
    
    st.info("🎥 Click 'START' to begin live video analysis. Make sure to allow camera access.")
    
    webrtc_streamer(
        key="age-gender-stream",
        mode=WebRtcMode.SENDRECV,
        video_frame_callback=video_frame_callback,
        media_stream_constraints={"video": True, "audio": False},
        async_processing=True,
    )

# --- SIDEBAR INFORMATION ---
with st.sidebar:
    st.markdown("### 📊 Model Information")
    
    st.markdown("""
    <div class="info-card">
        <h3>🔍 Overview</h3>
        <p>This AI application predicts <strong>Gender</strong> and <strong>Age</strong> from human faces using deep learning models trained on the <strong>UTKFace Dataset</strong>.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Gender Model Section
    st.markdown("""
    <div class="info-card">
        <h3>🚹🚺 Gender Prediction Model</h3>
        <p>• Input: 48×48 grayscale face image</p>
        <p>• Output: Binary classification (0=Male, 1=Female)</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Age Model Section  
    st.markdown("""
    <div class="info-card">
        <h3>🎂 Age Prediction Model</h3>
        <p>• Input: 48×48 grayscale face image</p>
        <p>• Output: Normalized float [0,1]</p>
        <p>• Final Age = Prediction × 116</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-card">
        <h3>📓 Resources</h3>
        <p><strong>Training Notebook:</strong><br>
        <a href="https://github.com/SolomonJesurathinam/JuypterProjects/blob/master/2025/ageGender/AgeGender-final.ipynb" target="_blank">🔗 View on GitHub</a></p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-card">
        <h3>🏆 Technical Credits</h3>
        <p>• <strong>Face Detection:</strong> OpenCV Haar Cascade<br>
        • <strong>ML Framework:</strong> TensorFlow/Keras<br>
        • <strong>Dataset:</strong> UTKFace<br>
        • <strong>Interface:</strong> Streamlit<br>
        • <strong>Video Processing:</strong> streamlit-webrtc</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Model status
    st.markdown('<div class="status-badge">✅ Models Loaded</div>', unsafe_allow_html=True)
    st.markdown('<div class="status-badge">🚀 Ready for Prediction</div>', unsafe_allow_html=True)

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
    <h3 style="margin: 0;">🎯 Accurate AI-Powered Predictions</h3>
    <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">
        Experience the power of computer vision and deep learning! 🚀
    </p>
</div>
""", unsafe_allow_html=True)