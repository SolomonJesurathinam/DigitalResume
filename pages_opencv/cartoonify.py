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
from reusable.image_functions import resize_func, load_img, download, capture_frame

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Cartoonify Image AI | Solomon J",
    page_icon="🎨",
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
    
    /* Success message styling */
    .stSuccess {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%) !important;
        border: none !important;
        border-radius: 15px !important;
        color: white !important;
        font-weight: 600 !important;
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
    
    /* Parameter control styling */
    .parameter-panel {
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
        
        .feature-card, .parameter-panel {
            padding: 1rem;
        }
        
        .info-card {
            padding: 1rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# --- MAIN TITLE ---
st.markdown('<h1 class="main-title">🎨 Cartoonify Your Images</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Transform your photos into amazing cartoon-style artwork with AI</p>', unsafe_allow_html=True)

# --- FEATURE OVERVIEW ---
st.markdown("### ✨ Creative Features")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📸</div>
        <div class="feature-title">Upload & Transform</div>
        <div class="feature-desc">Upload any image and convert it to cartoon style with customizable parameters</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📷</div>
        <div class="feature-title">Live Camera</div>
        <div class="feature-desc">Capture photos directly and instantly cartoonify them with real-time preview</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🎥</div>
        <div class="feature-title">Real-time Video</div>
        <div class="feature-desc">Live video cartoonification with adjustable parameters for instant results</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# --- CARTOONIFY FUNCTIONS ---
def output(img, blur, edge, bFilter):
    img = resize_func(img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, blur)
    edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, edge, edge)
    col_img = cv2.bilateralFilter(img, bFilter, 255, 255)
    cartoon = cv2.bitwise_and(col_img, col_img, mask=edges)
    image = cv2.cvtColor(cartoon, cv2.COLOR_BGR2RGB)
    return image

def Cartoonify():
    # Use the same cartoonify_image function as live feed for consistency
    cartoon = cartoonify_image(cv2_img, blur, edge, bFilter)
    # Convert from BGR to RGB for proper display
    # cartoon_rgb = cv2.cvtColor(cartoon, cv2.COLOR_BGR2RGB)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📷 Original Image")
        # Display original image as-is (already processed by load_img)
        st.image(resize_func(cv2_img), use_container_width=True)
    
    with col2:
        st.markdown("#### 🎨 Cartoonified Result")
        st.image(cartoon, use_container_width=True)
        download(cartoon, "cartoonify")

def cartoonify_image(img, blur, edge, bFilter):
    img = resize_func(img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, blur)
    edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                  cv2.THRESH_BINARY, edge, edge)
    col_img = cv2.bilateralFilter(img, bFilter, 255, 255)
    cartoon = cv2.bitwise_and(col_img, col_img, mask=edges)
    return cartoon

# --- MAIN INTERFACE ---
st.markdown("### 🎛️ Choose Your Method")

radio_values = st.radio(
    label="Select how you'd like to cartoonify your images:",
    options=("📸 Upload a Picture", "📷 Photo from Camera", "🎥 Live Video Feed"),
    help="Choose your preferred method for image cartoonification"
)

if radio_values == "📸 Upload a Picture":
    st.markdown("#### 📤 Upload Your Image")
    input_image = st.file_uploader(
        "Choose an image file", 
        type=['png', 'jpg', 'jpeg'],
        help="Upload a clear image for best cartoon results"
    )
    cv2_img = load_img(input_image)
    
    if cv2_img is not None:
        st.success("🎨 Great! Now adjust the parameters below to create your perfect cartoon style")
        
        st.markdown("""
        <div class="parameter-panel">
            <div class="parameter-title">🎛️ Cartoon Style Controls</div>
        </div>
        """, unsafe_allow_html=True)
        
        col_param1, col_param2, col_param3 = st.columns(3)
        
        with col_param1:
            blur = st.slider(
                "🌫️ Blur Level", 
                min_value=1, 
                max_value=21, 
                step=2, 
                value=3,
                help="Controls image smoothing - higher values create more blur"
            )
        
        with col_param2:
            edge = st.slider(
                "📐 Edge Detection", 
                min_value=3, 
                max_value=21, 
                step=2, 
                value=9,
                help="Adjusts edge line thickness - higher values create thicker lines"
            )
        
        with col_param3:
            bFilter = st.slider(
                "🎨 Color Filter", 
                min_value=1, 
                max_value=21, 
                step=2, 
                value=5,
                help="Controls color smoothing - higher values reduce color noise"
            )
        
        Cartoonify()

elif radio_values == "📷 Photo from Camera":
    st.markdown("#### 📷 Camera Capture")
    input_image = st.camera_input(
        "Take a photo to cartoonify",
        help="Make sure you have good lighting for best results"
    )
    cv2_img = load_img(input_image)
    
    if cv2_img is not None:
        st.success("📸 Perfect shot! Now customize your cartoon parameters")
        
        st.markdown("""
        <div class="parameter-panel">
            <div class="parameter-title">🎛️ Cartoon Style Controls</div>
        </div>
        """, unsafe_allow_html=True)
        
        col_param1, col_param2, col_param3 = st.columns(3)
        
        with col_param1:
            blur = st.slider(
                "🌫️ Blur Level", 
                min_value=1, 
                max_value=21, 
                step=2, 
                value=3,
                help="Controls image smoothing"
            )
        
        with col_param2:
            edge = st.slider(
                "📐 Edge Detection", 
                min_value=3, 
                max_value=21, 
                step=2, 
                value=9,
                help="Adjusts edge line thickness"
            )
        
        with col_param3:
            bFilter = st.slider(
                "🎨 Color Filter", 
                min_value=1, 
                max_value=21, 
                step=2, 
                value=5,
                help="Controls color smoothing"
            )
        
        Cartoonify()

elif radio_values == "🎥 Live Video Feed":
    st.markdown("#### 🎥 Real-time Video Cartoonification")
    
    st.markdown("""
    <div class="parameter-panel">
        <div class="parameter-title">🎛️ Live Video Controls</div>
    </div>
    """, unsafe_allow_html=True)
    
    col_live1, col_live2, col_live3 = st.columns(3)
    
    with col_live1:
        blur = st.slider(
            "🌫️ Blur Level", 
            min_value=1, 
            max_value=21, 
            step=2, 
            value=3,
            help="Real-time blur adjustment"
        )
    
    with col_live2:
        edge = st.slider(
            "📐 Edge Detection", 
            min_value=3, 
            max_value=21, 
            step=2, 
            value=9,
            help="Real-time edge adjustment"
        )
    
    with col_live3:
        bFilter = st.slider(
            "🎨 Bilateral Filter", 
            min_value=1, 
            max_value=21, 
            step=2, 
            value=5,
            help="Real-time color filter adjustment"
        )

    class VideoProcessor(VideoTransformerBase):
        def __init__(self):
            self.blur = blur
            self.edge = edge
            self.bFilter = bFilter
            self.latest_frame = None
            self.frame_lock = threading.Lock()
            
        def update_params(self, blur, edge, bFilter):
            self.blur = blur
            self.edge = edge
            self.bFilter = bFilter

        def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
            img = frame.to_ndarray(format="bgr24")
            cartoon = cartoonify_image(img, self.blur, self.edge, self.bFilter)
            with self.frame_lock:
                self.latest_frame = cartoon.copy()
            return av.VideoFrame.from_ndarray(cartoon, format="bgr24")

    # Create an instance of VideoProcessor
    video_processor = VideoProcessor()
    
    st.info("🎥 Click 'START' to begin live video cartoonification. Adjust parameters in real-time!")

    webrtc_ctx = webrtc_streamer(    
        key="cartoonify-stream",
        video_processor_factory=lambda: video_processor,
        media_stream_constraints={"video": True, "audio": False},
        async_processing=True
    )

    if webrtc_ctx.video_processor:
        webrtc_ctx.video_processor.update_params(blur, edge, bFilter)
        capture_frame(webrtc_ctx)

# --- SIDEBAR INFORMATION ---
with st.sidebar:
    st.markdown("### 🎨 About Cartoonify")
    
    st.markdown("""
    <div class="info-card">
        <h3>✨ How It Works</h3>
        <p>This application uses computer vision techniques to transform regular photos into cartoon-style images through a multi-step process:</p>
        <p>• <strong>Edge Detection:</strong> Identifies object boundaries</p>
        <p>• <strong>Color Smoothing:</strong> Reduces color complexity</p>
        <p>• <strong>Image Blending:</strong> Combines edges with smooth colors</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-card">
        <h3>🎛️ Parameter Guide</h3>
        <p><strong>🌫️ Blur Level:</strong> Controls how smooth the image becomes. Higher values create more artistic blur effects.</p>
        <p><strong>📐 Edge Detection:</strong> Adjusts the thickness of cartoon lines. Higher values make bolder outlines.</p>
        <p><strong>🎨 Color Filter:</strong> Smooths color transitions. Higher values reduce noise and create cleaner colors.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-card">
        <h3>💡 Tips for Best Results</h3>
        <p>• Use well-lit images with clear subjects</p>
        <p>• Experiment with different parameter combinations</p>
        <p>• Lower blur values preserve more detail</p>
        <p>• Higher edge values create stronger cartoon effects</p>
        <p>• Balanced parameters often give the best results</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-card">
        <h3>🔧 Technical Details</h3>
        <p><strong>Processing:</strong> OpenCV image processing</p>
        <p><strong>Algorithms:</strong> Adaptive thresholding, bilateral filtering</p>
        <p><strong>Real-time:</strong> WebRTC for live video processing</p>
        <p><strong>Output:</strong> High-quality cartoon-style images</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Status indicators
    st.markdown('<div class="status-badge">🎨 Ready to Cartoonify</div>', unsafe_allow_html=True)
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
    <h3 style="margin: 0;">🎨 Unleash Your Creative Vision</h3>
    <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">
        Transform ordinary photos into extraordinary cartoon art! ✨
    </p>
</div>
""", unsafe_allow_html=True)