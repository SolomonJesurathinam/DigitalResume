import streamlit as st
import cv2
from reusable.image_functions import load_img, download
import numpy as np
import os
from pathlib import Path

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="AI Image Colorizer | Solomon J",
    page_icon="🌈",
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
    
    /* Slider styling */
    .stSlider > div > div > div {
        background: linear-gradient(45deg, #667eea, #764ba2) !important;
    }
    
    .stSlider label {
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
        margin: 2rem 0;
    }
    
    .stFileUploader label {
        color: #2c3e50 !important;
        font-weight: 600 !important;
        font-size: 1.2rem !important;
    }
    
    /* Image display styling */
    .stImage {
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
    
    /* Control panel styling */
    .control-panel {
        background: rgba(255, 255, 255, 0.9);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        border: 1px solid rgba(255, 255, 255, 0.18);
        backdrop-filter: blur(8px);
        margin: 2rem 0;
    }
    
    .control-title {
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
    
    /* Download button styling */
    .stDownloadButton > button {
        background: linear-gradient(45deg, #667eea, #764ba2) !important;
        color: white !important;
        border-radius: 25px !important;
        border: none !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
        margin-top: 1rem !important;
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
    }
    
    /* Processing indicator */
    .processing-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
    }
    
    /* Section headers */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #2c3e50 !important;
        font-weight: bold !important;
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
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2rem;
        }
        
        .feature-card, .control-panel {
            padding: 1rem;
        }
        
        .info-card {
            padding: 1rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# --- LOAD MODELS ---
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
PROTOTXT = current_dir.parent / "data" / "colorize" / "colorization_deploy_v2.prototxt"
POINTS = current_dir.parent / "data" / "colorize" / "pts_in_hull.npy"
MODEL = current_dir.parent / "data" / "colorize" / "colorization_release_v2.caffemodel"

@st.cache_resource
def load_colorization_model():
    # Load the models
    net = cv2.dnn.readNetFromCaffe(str(PROTOTXT), str(MODEL))
    pts = np.load(str(POINTS))
    
    # Load centers for ab channel
    class8 = net.getLayerId("class8_ab")
    conv8 = net.getLayerId("conv8_313_rh")
    pts = pts.transpose().reshape(2, 313, 1, 1)
    net.getLayer(class8).blobs = [pts.astype("float32")]
    net.getLayer(conv8).blobs = [np.full([1, 313], 2.606, dtype="float32")]
    
    return net

net = load_colorization_model()

# --- MAIN TITLE ---
st.markdown('<h1 class="main-title">🌈 AI Image Colorizer</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Bring black and white photos to life with intelligent AI colorization</p>', unsafe_allow_html=True)

# --- FEATURE OVERVIEW ---
st.markdown("### ✨ AI Colorization Features")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🧠</div>
        <div class="feature-title">Deep Learning AI</div>
        <div class="feature-desc">Advanced neural network trained on millions of images for realistic colorization</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🎨</div>
        <div class="feature-title">Smart Color Prediction</div>
        <div class="feature-desc">Intelligently predicts natural colors based on image content and context</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">⚡</div>
        <div class="feature-title">Instant Results</div>
        <div class="feature-desc">Fast processing with adjustable lightness controls for perfect results</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# --- COLORIZATION FUNCTION ---
def ImageFunction(image, LightnessValue):
    # Process image
    scaled = image.astype("float32") / 255.0
    lab = cv2.cvtColor(scaled, cv2.COLOR_BGR2LAB)
    
    # Resize for model input
    resized = cv2.resize(lab, (224, 224))
    
    # Extract L channel
    L = cv2.split(resized)[0]
    L -= LightnessValue
    
    # Get AI predictions
    net.setInput(cv2.dnn.blobFromImage(L))
    ab = net.forward()[0, :, :, :].transpose((1, 2, 0))
    
    # Resize to original image dimensions
    ab = cv2.resize(ab, (image.shape[1], image.shape[0]))
    L = cv2.split(lab)[0]
    
    # Combine L and ab channels
    colorized = np.concatenate((L[:, :, np.newaxis], ab), axis=2)
    colorized = cv2.cvtColor(colorized, cv2.COLOR_LAB2BGR)
    colorized = np.clip(colorized, 0, 1)
    colorized = (255 * colorized).astype("uint8")
    
    return colorized

# --- MAIN INTERFACE ---
st.markdown("### 📤 Upload Your Black & White Image")

image = st.file_uploader(
    "Choose a black and white image to colorize",
    type=['png', 'jpg', 'jpeg'],
    help="Upload clear black and white photos for best colorization results"
)

cv2_img = load_img(image)

if cv2_img is not None:
    # Display processing status
    st.markdown("""
    <div class="processing-card">
        <h3 style="margin: 0;">🎨 Image Loaded Successfully!</h3>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">
            Adjust the lightness parameter below to fine-tune your colorization
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Control panel
    st.markdown("""
    <div class="control-panel">
        <div class="control-title">🎛️ Colorization Controls</div>
    </div>
    """, unsafe_allow_html=True)
    
    LightnessValue = st.slider(
        "🌟 Lightness Adjustment",
        min_value=28,
        max_value=80,
        value=50,
        help="Fine-tune the brightness and color intensity. Lower values = darker/more vibrant, Higher values = lighter/softer colors"
    )
    
    # Process and display results
    with st.spinner("🎨 AI is colorizing your image..."):
        colorized = ImageFunction(cv2_img, LightnessValue)
        colorized_rgb = cv2.cvtColor(colorized, cv2.COLOR_BGR2RGB)
    
    # Display comparison
    st.markdown("### 🔄 Before & After Comparison")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### ⚫ Original (B&W)")
        original_rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
        st.image(original_rgb, use_container_width=True)
    
    with col2:
        st.markdown("#### 🌈 AI Colorized")
        st.image(colorized_rgb, use_container_width=True)
        
        # Download button
        download(colorized_rgb, "colorized")
    
    # Results summary
    st.success("✨ Colorization completed! Your black and white image has been brought to life with AI-predicted colors.")

# --- SIDEBAR INFORMATION ---
with st.sidebar:
    st.markdown("### 🌈 About AI Colorization")
    
    st.markdown("""
    <div class="info-card">
        <h3>🧠 How AI Colorization Works</h3>
        <p>This application uses a deep convolutional neural network that has been trained on millions of color images to learn the relationship between image content and realistic colors.</p>
        <p><strong>Process:</strong></p>
        <p>• Converts image to LAB color space</p>
        <p>• Analyzes luminance (L) channel</p>
        <p>• Predicts color channels (A & B)</p>
        <p>• Reconstructs full-color image</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-card">
        <h3>🎛️ Lightness Parameter Guide</h3>
        <p><strong>Lower Values (28-40):</strong> Darker, more vibrant colors with higher contrast</p>
        <p><strong>Medium Values (40-60):</strong> Balanced colorization with natural tones</p>
        <p><strong>Higher Values (60-80):</strong> Lighter, softer colors with reduced intensity</p>
        <p><strong>Default (50):</strong> Optimal starting point for most images</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-card">
        <h3>💡 Tips for Best Results</h3>
        <p>• Use high-quality black and white images</p>
        <p>• Images with clear subjects work better</p>
        <p>• Experiment with lightness values</p>
        <p>• Historical photos often need lower lightness</p>
        <p>• Portraits typically work well with default settings</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-card">
        <h3>🔬 Technical Specifications</h3>
        <p><strong>Model:</strong> Deep Convolutional Neural Network</p>
        <p><strong>Framework:</strong> OpenCV DNN</p>
        <p><strong>Color Space:</strong> LAB (Lightness, A, B)</p>
        <p><strong>Input Size:</strong> 224×224 (automatically resized)</p>
        <p><strong>Output:</strong> Full-resolution colorized image</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Model status
    st.markdown('<div class="status-badge">🤖 AI Model Loaded</div>', unsafe_allow_html=True)
    st.markdown('<div class="status-badge">🌈 Ready to Colorize</div>', unsafe_allow_html=True)

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
    <h3 style="margin: 0;">🎨 Revive Your Memories in Living Color</h3>
    <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">
        Transform history into vibrant reality with AI-powered colorization! 🌈
    </p>
</div>
""", unsafe_allow_html=True)