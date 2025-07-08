import streamlit as st
import cv2
import av
from streamlit_webrtc import (
    WebRtcMode,
    webrtc_streamer,
    __version__ as st_webrtc_version,
)
from streamlit_webrtc import VideoTransformerBase
import threading
from reusable.image_functions import resize_func, download, load_img, capture_frame

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Pencil Sketch AI | Solomon J",
    page_icon="✏️",
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
    
    /* Slider styling */
    .stSlider > div > div > div {
        background: linear-gradient(45deg, #667eea, #764ba2) !important;
    }
    
    .stSlider label {
        color: #2c3e50 !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
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
        margin: 1rem 0;
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
    
    /* Video styling */
    .stVideo {
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        overflow: hidden;
        margin: 1rem 0;
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

# --- MAIN TITLE ---
st.markdown('<h1 class="main-title">✏️ Pencil Sketch Artist</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Transform your photos into beautiful hand-drawn pencil sketches</p>', unsafe_allow_html=True)

# --- FEATURE OVERVIEW ---
st.markdown("### 🎨 Artistic Features")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📸</div>
        <div class="feature-title">Upload & Sketch</div>
        <div class="feature-desc">Upload any photo and convert it to a realistic pencil sketch with adjustable blur effects</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📷</div>
        <div class="feature-title">Live Camera</div>
        <div class="feature-desc">Capture photos directly and instantly transform them into artistic pencil drawings</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🎥</div>
        <div class="feature-title">Real-time Video</div>
        <div class="feature-desc">Live video sketching with real-time parameter adjustment for instant artistic effects</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# --- PENCIL SKETCH FUNCTION ---
def PencilnBlack(img, blurValue):
    img = resize_func(img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    neg = 255 - gray
    blur = cv2.GaussianBlur(neg, ksize=(blurValue, blurValue), sigmaX=0, sigmaY=0)
    pencil = cv2.divide(gray, 255 - blur, scale=256)
    return pencil

def process_sketch(cv2_img, blur_value):
    """Process image and return both original and sketch for comparison"""
    pencil = PencilnBlack(cv2_img, blurValue=blur_value)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📷 Original Image")
        original_rgb = cv2_img #cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
        st.image(resize_func(original_rgb), use_container_width=True)
    
    with col2:
        st.markdown("#### ✏️ Pencil Sketch")
        # Convert grayscale to RGB for proper display
        pencil_rgb = cv2.cvtColor(pencil, cv2.COLOR_GRAY2RGB)
        st.image(pencil_rgb, use_container_width=True)
        download(pencil_rgb, "pencilSketch")

# --- MAIN INTERFACE ---
st.markdown("### 🎛️ Choose Your Method")

radio_values = st.radio(
    label="Select how you'd like to create pencil sketches:",
    options=("📸 Upload a Picture", "📷 Photo from Camera", "🎥 Live Video Feed"),
    help="Choose your preferred method for pencil sketch creation"
)

if radio_values == "📸 Upload a Picture":
    st.markdown("#### 📤 Upload Your Image")
    input_image = st.file_uploader(
        "Choose an image file", 
        type=['png', 'jpg', 'jpeg'],
        help="Upload a clear image for best sketch results"
    )
    cv2_img = load_img(input_image)
    
    if cv2_img is not None:
        st.markdown("""
        <div class="control-panel">
            <div class="control-title">✏️ Sketch Controls</div>
        </div>
        """, unsafe_allow_html=True)
        
        blur = st.slider(
            "🌫️ Blur Intensity", 
            min_value=3, 
            max_value=301, 
            step=2, 
            value=21,
            help="Controls sketch detail level - lower values create more detailed sketches, higher values create softer artistic effects"
        )
        
        with st.spinner("✏️ Creating your pencil sketch..."):
            process_sketch(cv2_img, blur)

elif radio_values == "📷 Photo from Camera":
    st.markdown("#### 📷 Camera Capture")
    input_image = st.camera_input(
        "Take a photo to sketch",
        help="Ensure good lighting for best sketch results"
    )
    cv2_img = load_img(input_image)
    
    if cv2_img is not None:
        st.markdown("""
        <div class="control-panel">
            <div class="control-title">✏️ Sketch Controls</div>
        </div>
        """, unsafe_allow_html=True)
        
        blur = st.slider(
            "🌫️ Blur Intensity", 
            min_value=3, 
            max_value=301, 
            step=2, 
            value=21,
            help="Adjust the artistic style of your sketch"
        )
        
        with st.spinner("✏️ Creating your pencil sketch..."):
            process_sketch(cv2_img, blur)

elif radio_values == "🎥 Live Video Feed":
    st.markdown("#### 🎥 Real-time Pencil Sketching")
    
    st.markdown("""
    <div class="control-panel">
        <div class="control-title">✏️ Live Sketch Controls</div>
    </div>
    """, unsafe_allow_html=True)
    
    blur = st.slider(
        "🌫️ Blur Intensity", 
        min_value=3, 
        max_value=301, 
        step=2, 
        value=21,
        help="Real-time blur adjustment for live sketching"
    )

    class VideoProcessor(VideoTransformerBase):
        def __init__(self):
            self.blur = blur
            self.latest_frame = None
            self.frame_lock = threading.Lock()
            
        def update_params(self, blur):
            self.blur = blur

        def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
            img = frame.to_ndarray(format="bgr24")
            pencil = PencilnBlack(img, blurValue=self.blur)
            # Convert grayscale to 3-channel for video stream
            pencil_3ch = cv2.cvtColor(pencil, cv2.COLOR_GRAY2BGR)
            
            with self.frame_lock:
                self.latest_frame = pencil_3ch.copy()
                
            return av.VideoFrame.from_ndarray(pencil_3ch, format="bgr24")

    # Create an instance of VideoProcessor
    video_processor = VideoProcessor()
    
    st.info("🎥 Click 'START' to begin live pencil sketching. Adjust blur in real-time!")

    webrtc_ctx = webrtc_streamer(
        key="pencil-stream",
        video_processor_factory=lambda: video_processor,
        media_stream_constraints={"video": True, "audio": False},
        async_processing=True
    )

    if webrtc_ctx.video_processor:
        webrtc_ctx.video_processor.update_params(blur)
        capture_frame(webrtc_ctx)

# --- SIDEBAR INFORMATION ---
with st.sidebar:
    st.markdown("### ✏️ About Pencil Sketching")
    
    st.markdown("""
    <div class="info-card">
        <h3>🎨 How It Works</h3>
        <p>This application transforms photos into pencil sketches using computer vision techniques:</p>
        <p>• <strong>Grayscale Conversion:</strong> Converts image to black and white</p>
        <p>• <strong>Negative Inversion:</strong> Creates inverted image for blending</p>
        <p>• <strong>Gaussian Blur:</strong> Applies controlled blur effect</p>
        <p>• <strong>Dodge Blend:</strong> Combines original with blurred negative</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-card">
        <h3>🌫️ Blur Intensity Guide</h3>
        <p><strong>Low Values (3-21):</strong> Detailed sketches with fine lines and sharp edges</p>
        <p><strong>Medium Values (21-101):</strong> Balanced artistic effect with good detail retention</p>
        <p><strong>High Values (101-301):</strong> Soft, dreamy sketches with artistic blur</p>
        <p><strong>Default (21):</strong> Optimal starting point for most images</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-card">
        <h3>💡 Tips for Best Results</h3>
        <p>• Use high-contrast images for dramatic sketches</p>
        <p>• Portraits work exceptionally well</p>
        <p>• Experiment with different blur values</p>
        <p>• Good lighting improves sketch quality</p>
        <p>• Lower blur values preserve more detail</p>
        <p>• Higher blur creates artistic effects</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-card">
        <h3>🔧 Technical Details</h3>
        <p><strong>Algorithm:</strong> Dodge Blending Technique</p>
        <p><strong>Processing:</strong> OpenCV Computer Vision</p>
        <p><strong>Color Space:</strong> Grayscale conversion</p>
        <p><strong>Blur Method:</strong> Gaussian Blur with variable kernel</p>
        <p><strong>Real-time:</strong> WebRTC for live video processing</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Status indicators
    st.markdown('<div class="status-badge">✏️ Ready to Sketch</div>', unsafe_allow_html=True)
    st.markdown('<div class="status-badge">📷 Camera Available</div>', unsafe_allow_html=True)

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
    <h3 style="margin: 0;">✏️ Unleash Your Inner Artist</h3>
    <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">
        Transform photos into timeless pencil sketch masterpieces! 🎨
    </p>
</div>
""", unsafe_allow_html=True)