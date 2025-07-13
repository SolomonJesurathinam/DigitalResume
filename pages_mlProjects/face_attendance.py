# Simplified Face Recognition App - 3 Sections Only
# Dashboard, Users, Recognition - Clean and Fast

import streamlit as st
import os
import cv2
import numpy as np
from deepface import DeepFace
from scipy.spatial.distance import cosine
import tensorflow as tf
from PIL import Image
import pickle
import json
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, RTCConfiguration
import tempfile
import shutil
from pathlib import Path
import hashlib
import time
import threading
import av
from datetime import datetime

current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
model_path = os.path.join(ROOT_DIR, 'data/face', "liveness.model")

# Configure Streamlit
st.set_page_config(
    page_title="🔮 Face Recognition",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Minimal CSS - Purple Theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    .main { font-family: 'Poppins', sans-serif; background: #f8f7ff; }
    
    .header {
        background: linear-gradient(135deg, #8B7CF6 0%, #6D5ACF 100%);
        padding: 1.5rem; border-radius: 15px; color: white; text-align: center;
        margin-bottom: 1.5rem; box-shadow: 0 5px 15px rgba(139, 124, 246, 0.2);
    }
    
    .tile {
        background: white; padding: 1.5rem; border-radius: 12px;
        box-shadow: 0 2px 8px rgba(139, 124, 246, 0.1);
        margin: 0.5rem; border-left: 4px solid #8B7CF6;
        transition: all 0.2s ease; min-height: 120px;
    }
    
    .tile:hover { transform: translateY(-2px); box-shadow: 0 4px 15px rgba(139, 124, 246, 0.2); }
    
    .metric { background: linear-gradient(135deg, #8B7CF6 0%, #A78BFA 100%);
        padding: 1rem; border-radius: 10px; text-align: center; color: white; margin: 0.5rem; }
    
    .success { background: linear-gradient(135deg, #8B7CF6 0%, #6D5ACF 100%);
        color: white; padding: 1rem; border-radius: 10px; margin: 0.5rem 0; }
    
    .warning { background: linear-gradient(135deg, #FBBF24 0%, #F59E0B 100%);
        color: white; padding: 1rem; border-radius: 10px; margin: 0.5rem 0; }
    
    .stButton > button {
        background: linear-gradient(135deg, #8B7CF6 0%, #6D5ACF 100%);
        border: none; border-radius: 8px; color: white; font-weight: 600;
        padding: 0.5rem 1rem; transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px); box-shadow: 0 4px 12px rgba(139, 124, 246, 0.3);
    }
    
    .sidebar .stSelectbox label { color: #4C1D95 !important; font-weight: 600 !important; }
    
    video { border-radius: 10px; box-shadow: 0 4px 15px rgba(139, 124, 246, 0.2); }
</style>
""", unsafe_allow_html=True)

# WebRTC Configuration
RTC_CONFIGURATION = RTCConfiguration({
    "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
})

# Global variables
MODEL_NAME = "Facenet"
DB_PATH = "./Database"
EMBEDDINGS_FILE = "db_embeddings.pkl"

# Initialize session state
if 'db_embeddings' not in st.session_state:
    st.session_state.db_embeddings = []
if 'liveness_model' not in st.session_state:
    st.session_state.liveness_model = None
if 'captured_images' not in st.session_state:
    st.session_state.captured_images = []

@st.cache_resource
def load_liveness_model():
    """Load liveness detection model"""
    try:
        model = tf.keras.models.load_model(model_path)
        return model
    except Exception:
        return None

def save_embeddings(embeddings):
    """Save embeddings to file"""
    try:
        with open(EMBEDDINGS_FILE, 'wb') as f:
            pickle.dump(embeddings, f)
        return True
    except Exception:
        return False

def load_database_embeddings():
    """Load all embeddings from database folder"""
    db_embeddings = []
    if not os.path.exists(DB_PATH):
        os.makedirs(DB_PATH)
        return db_embeddings

    persons = [p for p in os.listdir(DB_PATH) if os.path.isdir(os.path.join(DB_PATH, p))]
    
    for person in persons:
        person_folder = os.path.join(DB_PATH, person)
        for image_name in os.listdir(person_folder):
            img_path = os.path.join(person_folder, image_name)
            try:
                embedding_obj = DeepFace.represent(
                    img_path=img_path,
                    model_name=MODEL_NAME,
                    enforce_detection=False
                )[0]
                embedding_obj["identity"] = person
                embedding_obj["image_path"] = img_path
                embedding_obj["image_name"] = image_name
                embedding_obj["created_at"] = datetime.fromtimestamp(os.path.getctime(img_path)).isoformat()
                db_embeddings.append(embedding_obj)
            except Exception:
                continue
    
    return db_embeddings

def register_new_user(name, images, source="upload"):
    """Register new user with multiple images"""
    user_folder = os.path.join(DB_PATH, name)
    os.makedirs(user_folder, exist_ok=True)
    
    embeddings_added = []
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    for i, image in enumerate(images):
        try:
            if hasattr(image, 'mode'):
                if image.mode == 'RGBA':
                    rgb_image = Image.new('RGB', image.size, (255, 255, 255))
                    rgb_image.paste(image, mask=image.split()[-1])
                    image = rgb_image
                elif image.mode != 'RGB':
                    image = image.convert('RGB')
            
            image_name = f"{name}_{source}_{timestamp}_{i+1}.jpg"
            image_path = os.path.join(user_folder, image_name)
            image.save(image_path, 'JPEG', quality=95)
            
            try:
                embedding_obj = DeepFace.represent(
                    img_path=image_path,
                    model_name=MODEL_NAME,
                    enforce_detection=False
                )[0]
                embedding_obj["identity"] = name
                embedding_obj["image_path"] = image_path
                embedding_obj["image_name"] = image_name
                embedding_obj["created_at"] = datetime.now().isoformat()
                embedding_obj["source"] = source
                embeddings_added.append(embedding_obj)
            except Exception:
                if os.path.exists(image_path):
                    os.remove(image_path)
        except Exception:
            continue
    
    if embeddings_added:
        st.session_state.db_embeddings.extend(embeddings_added)
        save_embeddings(st.session_state.db_embeddings)
        return len(embeddings_added)
    return 0

def delete_user_image(user_name, image_path):
    """Delete a specific image for a user"""
    try:
        st.session_state.db_embeddings = [
            emb for emb in st.session_state.db_embeddings
            if emb.get("image_path") != image_path
        ]
        if os.path.exists(image_path):
            os.remove(image_path)
        save_embeddings(st.session_state.db_embeddings)
        return True
    except Exception:
        return False

def get_face_hash(coords):
    """Generate a unique hash for face coordinates"""
    x, y, w, h = coords["x"], coords["y"], coords["w"], coords["h"]
    return hashlib.md5(f"{int(x/5)*5}_{int(y/5)*5}_{int(w/5)*5}_{int(h/5)*5}".encode()).hexdigest()[:8]

def calculate_face_overlap(face1_coords, face2_coords):
    """Calculate overlap between two face bounding boxes"""
    x1, y1, w1, h1 = face1_coords["x"], face1_coords["y"], face1_coords["w"], face1_coords["h"]
    x2, y2, w2, h2 = face2_coords["x"], face2_coords["y"], face2_coords["w"], face2_coords["h"]
    
    x_overlap = max(0, min(x1 + w1, x2 + w2) - max(x1, x2))
    y_overlap = max(0, min(y1 + h1, y2 + h2) - max(y1, y2))
    intersection = x_overlap * y_overlap
    
    area1 = w1 * h1
    area2 = w2 * h2
    union = area1 + area2 - intersection
    
    return intersection / union if union > 0 else 0

# Fast Video Processor with improved face tracking
class FaceRecognitionProcessor(VideoProcessorBase):
    def __init__(self, db_embeddings, liveness_model=None):
        self.frame_count = 0
        self.recognition_every_n_frames = 15
        self.liveness_every_n_frames = 30
        
        self.frame_lock = threading.Lock()
        self.recognition_results = []
        self.liveness_results = {}
        self.face_tracking = {}  # Track faces by position
        
        self.db_embeddings = db_embeddings
        self.liveness_model = liveness_model
        
        self.last_recognition_time = time.time()
        self.last_liveness_time = time.time()

    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        img = frame.to_ndarray(format="bgr24")
        self.frame_count += 1
        current_time = time.time()
        
        try:
            faces = DeepFace.extract_faces(
                img_path=img,
                detector_backend='opencv',
                enforce_detection=False,
                align=False
            )
            
            if (self.frame_count % self.recognition_every_n_frames == 0 and 
                current_time - self.last_recognition_time > 0.5):
                self.process_recognition(img, faces)
                self.last_recognition_time = current_time
            
            if (self.frame_count % self.liveness_every_n_frames == 0 and 
                self.liveness_model and 
                current_time - self.last_liveness_time > 1.0):
                self.process_liveness(img, faces)
                self.last_liveness_time = current_time
            
            processed_img = self.draw_results(img, faces)
            
        except Exception:
            processed_img = img
        
        return av.VideoFrame.from_ndarray(processed_img, format="bgr24")

    def process_recognition(self, img, faces):
        try:
            new_results = []
            
            # Sort faces by x-coordinate for consistent ordering
            sorted_faces = sorted(faces, key=lambda f: f["facial_area"]["x"])
            
            for i, face_obj in enumerate(sorted_faces[:2]):  # Max 2 faces
                coords = face_obj["facial_area"]
                result = self.recognize_face(face_obj)
                result['face_id'] = i  # Assign stable ID
                new_results.append(result)
            
            with self.frame_lock:
                self.recognition_results = new_results
        except Exception:
            pass

    def recognize_face(self, face_obj):
        coords = face_obj["facial_area"]
        
        try:
            if not self.db_embeddings:
                return {'coords': coords, 'name': "No Database", 'confidence': 0, 'distance': 1.0}
            
            face_img = face_obj["face"]
            if face_img.max() <= 1:
                face_img = (face_img * 255).astype(np.uint8)
            
            if len(face_img.shape) == 3:
                face_rgb = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)
            else:
                face_rgb = face_img
            
            embedding_result = DeepFace.represent(
                img_path=face_rgb,
                model_name=MODEL_NAME,
                enforce_detection=False
            )
            
            if not embedding_result:
                return {'coords': coords, 'name': "No Embedding", 'confidence': 0, 'distance': 1.0}
            
            embedding = embedding_result[0]["embedding"]
            
            best_match = None
            best_score = 1.0
            
            for db_entry in self.db_embeddings:
                db_embedding = db_entry["embedding"]
                dist = cosine(embedding, db_embedding)
                
                if dist < 0.5 and dist < best_score:
                    best_score = dist
                    best_match = db_entry["identity"]
            
            if best_match:
                return {'coords': coords, 'name': best_match, 'confidence': 1 - best_score, 'distance': best_score}
            else:
                return {'coords': coords, 'name': "Unknown", 'confidence': 0, 'distance': best_score}
                
        except Exception:
            return {'coords': coords, 'name': "Error", 'confidence': 0, 'distance': 1.0}
            
      

    def process_liveness(self, img, faces):
        if not self.liveness_model:
            return
            
        try:
            current_time = time.time()
            
            # Sort faces by x-coordinate for consistent ordering
            sorted_faces = sorted(faces, key=lambda f: f["facial_area"]["x"])
            
            for i, face_obj in enumerate(sorted_faces[:2]):  # Max 2 faces
                coords = face_obj["facial_area"]
                face_id = f"face_{i}"  # Stable face ID based on position
                
                try:
                    x, y, w, h = coords["x"], coords["y"], coords["w"], coords["h"]
                    xmin, ymin = max(0, int(x)), max(0, int(y))
                    xmax, ymax = min(img.shape[1], int(x + w)), min(img.shape[0], int(y + h))
                    
                    if xmax > xmin and ymax > ymin:
                        face_region = img[ymin:ymax, xmin:xmax]
                        
                        # Ensure face region is large enough
                        if face_region.shape[0] < 10 or face_region.shape[1] < 10:
                            continue
                            
                        face_region = cv2.resize(face_region, (32, 32))
                        face_region = face_region.astype('float32') / 255.0
                        face_region = np.expand_dims(face_region, axis=0)
                        
                        liveness_pred = self.liveness_model.predict(face_region, verbose=0)
                        liveness_class = liveness_pred[0].argmax()
                        confidence = float(liveness_pred[0].max())
                        
                        with self.frame_lock:
                            self.liveness_results[face_id] = {
                                'class': liveness_class,
                                'confidence': confidence,
                                'timestamp': current_time,
                                'coords': coords,
                                'face_id': i
                            }
                except Exception:
                    pass
        except Exception:
            pass

    def draw_results(self, img, faces):
        try:
            current_time = time.time()
            
            with self.frame_lock:
                # Clean old liveness results
                self.liveness_results = {
                    k: v for k, v in self.liveness_results.items() 
                    if current_time - v['timestamp'] < 5
                }
                recognition_results = self.recognition_results.copy()
                liveness_results = self.liveness_results.copy()
            
            # Sort faces by x-coordinate for consistent display
            sorted_faces = sorted(faces, key=lambda f: f["facial_area"]["x"])
            
            for i, face_obj in enumerate(sorted_faces):
                coords = face_obj["facial_area"]
                x, y, w, h = coords["x"], coords["y"], coords["w"], coords["h"]
                
                # Get recognition result by index
                if i < len(recognition_results):
                    result = recognition_results[i]
                    name = result['name']
                    confidence = result['confidence']
                else:
                    name = "Processing..."
                    confidence = 0
                
                # Color coding
                if "Error" in name:
                    color = (255, 0, 255)
                elif name == "Processing...":
                    color = (0, 255, 255)
                elif name == "Unknown":
                    color = (0, 0, 255)
                else:
                    color = (0, 255, 0)
                
                # Draw face box
                cv2.rectangle(img, (int(x), int(y)), (int(x+w), int(y+h)), color, 2)
                
                # Draw name
                cv2.putText(img, name[:15], (int(x), int(y) - 10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
                
                # Draw confidence
                if confidence > 0:
                    cv2.putText(img, f"{confidence:.1%}", (int(x), int(y) - 35),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
                
                # Get liveness result by face ID
                face_id = f"face_{i}"
                liveness_text = "Checking..."
                liveness_color = (128, 128, 128)
                
                if face_id in liveness_results:
                    liveness_data = liveness_results[face_id]
                    liveness_class = liveness_data['class']
                    liveness_conf = liveness_data['confidence']
                    
                    if liveness_class == 1:
                        liveness_text = f"REAL ({liveness_conf:.1%})"
                        liveness_color = (0, 255, 0)
                    else:
                        liveness_text = f"FAKE ({liveness_conf:.1%})"
                        liveness_color = (0, 0, 255)
                
                cv2.putText(img, liveness_text, (int(x), int(y + h) + 20),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, liveness_color, 2)
            
            # Simple status
            cv2.putText(img, f"Frame: {self.frame_count}", (10, 25),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
            
        except Exception:
            pass
        
        return img

    def process_liveness(self, img, faces):
        if not self.liveness_model:
            return
            
        try:
            current_time = time.time()
            
            for face_obj in faces:
                coords = face_obj["facial_area"]
                face_hash = get_face_hash(coords)
                
                try:
                    x, y, w, h = coords["x"], coords["y"], coords["w"], coords["h"]
                    xmin, ymin = max(0, int(x)), max(0, int(y))
                    xmax, ymax = min(img.shape[1], int(x + w)), min(img.shape[0], int(y + h))
                    
                    if xmax > xmin and ymax > ymin:
                        face_region = img[ymin:ymax, xmin:xmax]
                        face_region = cv2.resize(face_region, (32, 32))
                        face_region = face_region.astype('float32') / 255.0
                        face_region = np.expand_dims(face_region, axis=0)
                        
                        liveness_pred = self.liveness_model.predict(face_region, verbose=0)
                        liveness_class = liveness_pred[0].argmax()
                        confidence = float(liveness_pred[0].max())
                        
                        with self.frame_lock:
                            self.liveness_results[face_hash] = {
                                'class': liveness_class,
                                'confidence': confidence,
                                'timestamp': current_time,
                                'coords': coords
                            }
                except Exception:
                    pass
        except Exception:
            pass

    def draw_results(self, img, faces):
        try:
            current_time = time.time()
            
            with self.frame_lock:
                self.liveness_results = {
                    k: v for k, v in self.liveness_results.items() 
                    if current_time - v['timestamp'] < 5
                }
                recognition_results = self.recognition_results.copy()
                liveness_results = self.liveness_results.copy()
            
            for i, face_obj in enumerate(faces):
                coords = face_obj["facial_area"]
                x, y, w, h = coords["x"], coords["y"], coords["w"], coords["h"]
                
                # Recognition result
                if i < len(recognition_results):
                    result = recognition_results[i]
                    name = result['name']
                    confidence = result['confidence']
                else:
                    name = "Processing..."
                    confidence = 0
                
                # Color coding
                if "Error" in name:
                    color = (255, 0, 255)
                elif name == "Processing...":
                    color = (0, 255, 255)
                elif name == "Unknown":
                    color = (0, 0, 255)
                else:
                    color = (0, 255, 0)
                
                # Draw face box
                cv2.rectangle(img, (int(x), int(y)), (int(x+w), int(y+h)), color, 2)
                
                # Draw name
                cv2.putText(img, name[:15], (int(x), int(y) - 10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
                
                # Draw confidence
                if confidence > 0:
                    cv2.putText(img, f"{confidence:.1%}", (int(x), int(y) - 35),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
                
                # Liveness result
                face_hash = get_face_hash(coords)
                liveness_text = "Checking..."
                liveness_color = (128, 128, 128)
                
                for liveness_hash, liveness_data in liveness_results.items():
                    if 'coords' in liveness_data:
                        overlap = calculate_face_overlap(coords, liveness_data['coords'])
                        if overlap > 0.3:
                            liveness_class = liveness_data['class']
                            liveness_conf = liveness_data['confidence']
                            
                            if liveness_class == 1:
                                liveness_text = f"REAL ({liveness_conf:.1%})"
                                liveness_color = (0, 255, 0)
                            else:
                                liveness_text = f"FAKE ({liveness_conf:.1%})"
                                liveness_color = (0, 0, 255)
                            break
                
                cv2.putText(img, liveness_text, (int(x), int(y + h) + 20),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, liveness_color, 2)
            
            # Simple status
            cv2.putText(img, f"Frame: {self.frame_count}", (10, 25),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
            
        except Exception:
            pass
        
        return img

def main():
    # Simple header
    st.markdown("""
    <div class="header">
        <h2>🔮 Face Recognition System</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Load models
    if st.session_state.liveness_model is None:
        st.session_state.liveness_model = load_liveness_model()
    
    # Auto-initialize database
    if not st.session_state.db_embeddings and os.path.exists(DB_PATH):
        st.session_state.db_embeddings = load_database_embeddings()
    
    # Simple navigation
    with st.sidebar:
        st.markdown("### 🎛️ Navigation")
        page = st.selectbox("", ["🏠 Dashboard", "👥 Users", "🔍 Recognition"])
        
        # Simple stats
        if st.session_state.db_embeddings:
            users = len(set([emb["identity"] for emb in st.session_state.db_embeddings]))
            st.markdown(f"**👥 Users:** {users}")
            st.markdown(f"**📸 Photos:** {len(st.session_state.db_embeddings)}")
    
    # Route to pages
    if page == "🏠 Dashboard":
        dashboard_page()
    elif page == "👥 Users":
        users_page()
    elif page == "🔍 Recognition":
        recognition_page()

def dashboard_page():
    """Simple dashboard with feature tiles"""
    
    # Quick stats
    col1, col2, col3, col4 = st.columns(4)
    users = len(set([emb["identity"] for emb in st.session_state.db_embeddings])) if st.session_state.db_embeddings else 0
    
    with col1:
        st.markdown(f'<div class="metric"><h3>{users}</h3><p>Users</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric"><h3>{len(st.session_state.db_embeddings)}</h3><p>Photos</p></div>', unsafe_allow_html=True)
    with col3:
        status = "Active" if st.session_state.liveness_model else "Inactive"
        st.markdown(f'<div class="metric"><h3>{status}</h3><p>Liveness</p></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="metric"><h3>0.50</h3><p>Threshold</p></div>', unsafe_allow_html=True)
    
    st.markdown("### Features")
    
    # Feature tiles
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="tile">
            <h4>🎯 Real-time Recognition</h4>
            <p>Advanced AI-powered face detection and recognition with multiple face support</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="tile">
            <h4>📷 Flexible Registration</h4>
            <p>Register users by uploading 3-5 photos or taking pictures with live camera</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="tile">
            <h4>🔍 Liveness Detection</h4>
            <p>Advanced anti-spoofing technology to detect real vs fake faces</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="tile">
            <h4>👥 User Management</h4>
            <p>Complete user management with individual photo control and batch operations</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Installation instructions only on dashboard
    st.markdown("### Setup Instructions")
    st.code("""
SIMPLIFIED FACE RECOGNITION SYSTEM - 3 SECTIONS

INSTALL:
pip install streamlit streamlit-webrtc opencv-python deepface scipy tensorflow pillow

RUN:
streamlit run app.py

FEATURES:
✅ 3 Simple Sections: Dashboard, Users, Recognition
✅ Auto-initialize database on startup  
✅ Small, clean tiles
✅ Fast performance with optimized processing
✅ Multiple face support
✅ Always-on liveness detection
✅ Register: Upload or live camera (3-5 pics)
✅ Delete: Full user or individual photos
✅ Recognition: Image upload/camera + Live WebRTC
✅ Minimal design, maximum functionality

SECTIONS:
🏠 Dashboard: Feature overview + quick stats
👥 Users: Register new (upload/camera) + Delete users (full/partial)  
🔍 Recognition: Image recognition + Live recognition with liveness

Clean, fast, and focused on core functionality!
""", language="text")

def users_page():
    """Users section - Register new or Delete existing"""
    
    tab1, tab2 = st.tabs(["➕ Register New User", "🗑️ Delete User"])
    
    with tab1:
        st.markdown("### Register New User")
        
        # User name
        user_name = st.text_input("👤 Full Name:", placeholder="John Doe")
        
        if user_name:
            # Check if exists
            existing_users = [emb["identity"] for emb in st.session_state.db_embeddings]
            if user_name in existing_users:
                st.markdown('<div class="warning">⚠️ User already exists!</div>', unsafe_allow_html=True)
                if st.checkbox("Replace existing user"):
                    user_folder = os.path.join(DB_PATH, user_name)
                    if os.path.exists(user_folder):
                        shutil.rmtree(user_folder)
                    st.session_state.db_embeddings = [
                        emb for emb in st.session_state.db_embeddings
                        if emb["identity"] != user_name
                    ]
                    st.markdown('<div class="success">✅ Existing user removed</div>', unsafe_allow_html=True)
                else:
                    return
            
            # Registration methods
            method_tab1, method_tab2 = st.tabs(["📁 Upload Photos", "📸 Live Photos"])
            
            with method_tab1:
                uploaded_files = st.file_uploader("Upload 3-5 photos", type=['jpg', 'jpeg', 'png'], accept_multiple_files=True)
                
                if uploaded_files and len(uploaded_files) >= 3:
                    cols = st.columns(min(len(uploaded_files), 5))
                    images = []
                    
                    for i, file in enumerate(uploaded_files[:5]):
                        try:
                            image = Image.open(file)
                            images.append(image)
                            with cols[i]:
                                st.image(image, caption=f"Photo {i+1}", use_container_width=True)
                        except Exception:
                            continue
                    
                    if st.button("✅ Register User", type="primary"):
                        with st.spinner("Registering..."):
                            count = register_new_user(user_name, images, "upload")
                            if count > 0:
                                st.markdown(f'<div class="success">🎉 {user_name} registered with {count} photos!</div>', unsafe_allow_html=True)
                                st.balloons()
                            else:
                                st.error("Registration failed")
            
            with method_tab2:
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    camera_photo = st.camera_input("📸 Take photo")
                    
                    if camera_photo:
                        image = Image.open(camera_photo)
                        
                        col_a, col_b = st.columns(2)
                        with col_a:
                            if st.button("➕ Add Photo"):
                                st.session_state.captured_images.append(image)
                                st.success(f"Photo {len(st.session_state.captured_images)} added!")
                                st.rerun()
                        
                        with col_b:
                            if st.button("🗑️ Clear All"):
                                st.session_state.captured_images = []
                                st.success("Cleared!")
                                st.rerun()
                
                with col2:
                    count = len(st.session_state.captured_images)
                    st.metric("📸 Captured", f"{count}/5")
                    st.progress(min(count / 5, 1.0))
                
                # Show captured images
                if st.session_state.captured_images:
                    st.markdown("**Captured Photos:**")
                    cols = st.columns(5)
                    
                    for i, img in enumerate(st.session_state.captured_images):
                        with cols[i % 5]:
                            st.image(img, caption=f"{i+1}", use_container_width=True)
                            if st.button("🗑️", key=f"del_{i}"):
                                st.session_state.captured_images.pop(i)
                                st.rerun()
                    
                    if len(st.session_state.captured_images) >= 3:
                        if st.button("✅ Register with Camera Photos", type="primary"):
                            with st.spinner("Registering..."):
                                count = register_new_user(user_name, st.session_state.captured_images, "camera")
                                if count > 0:
                                    st.markdown(f'<div class="success">🎉 {user_name} registered with {count} photos!</div>', unsafe_allow_html=True)
                                    st.session_state.captured_images = []
                                    st.balloons()
                                else:
                                    st.error("Registration failed")
    
    with tab2:
        st.markdown("### Delete User")
        
        if not st.session_state.db_embeddings:
            st.info("No users to delete")
            return
        
        # Get users
        users = {}
        for emb in st.session_state.db_embeddings:
            user_name = emb["identity"]
            if user_name not in users:
                users[user_name] = []
            users[user_name].append(emb)
        
        selected_user = st.selectbox("Select user to delete:", [""] + list(users.keys()))
        
        if selected_user:
            user_embeddings = users[selected_user]
            
            st.markdown(f"**User:** {selected_user} ({len(user_embeddings)} photos)")
            
            # Show user photos
            cols = st.columns(5)
            for i, emb in enumerate(user_embeddings):
                img_path = emb.get("image_path")
                if img_path and os.path.exists(img_path):
                    try:
                        with cols[i % 5]:
                            img = Image.open(img_path)
                            st.image(img, caption=f"Photo {i+1}", use_container_width=True)
                            if st.button(f"🗑️ Delete", key=f"del_img_{i}"):
                                if delete_user_image(selected_user, img_path):
                                    st.success("Photo deleted!")
                                    st.rerun()
                    except Exception:
                        continue
            
            st.markdown("---")
            
            # Upload more photos
            st.markdown("**Add More Photos:**")
            new_photos = st.file_uploader("Upload additional photos", type=['jpg', 'jpeg', 'png'], accept_multiple_files=True)
            
            if new_photos:
                new_images = []
                for photo in new_photos:
                    try:
                        img = Image.open(photo)
                        new_images.append(img)
                    except Exception:
                        continue
                
                if new_images and st.button("➕ Add Photos"):
                    with st.spinner("Adding photos..."):
                        count = register_new_user(selected_user, new_images, "additional")
                        if count > 0:
                            st.success(f"Added {count} photos!")
                            st.rerun()
            
            # Delete options
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("🗑️ Delete All Photos", type="secondary"):
                    # Remove user completely
                    st.session_state.db_embeddings = [
                        emb for emb in st.session_state.db_embeddings
                        if emb["identity"] != selected_user
                    ]
                    user_folder = os.path.join(DB_PATH, selected_user)
                    if os.path.exists(user_folder):
                        shutil.rmtree(user_folder)
                    save_embeddings(st.session_state.db_embeddings)
                    st.success(f"{selected_user} deleted!")
                    st.rerun()

def recognition_page():
    """Recognition section - Live or Image recognition"""
    
    if not st.session_state.db_embeddings:
        st.warning("No users registered. Go to Users section to register.")
        return
    
    tab1, tab2 = st.tabs(["📸 Image Recognition", "🎥 Live Recognition"])
    
    with tab1:
        st.markdown("### Image Recognition")
        
        # Take photo or upload
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Take Photo:**")
            camera_photo = st.camera_input("📸 Take photo for recognition")
            
            if camera_photo:
                image = Image.open(camera_photo)
                
                # Show original image
                st.image(image, caption="Original", width=300)
                
                if st.button("🔍 Recognize", type="primary"):
                    with st.spinner("Recognizing..."):
                        result = recognize_image(image)
                        if result:
                            # Show annotated image
                            annotated_img = Image.fromarray(result['annotated_image'])
                            st.image(annotated_img, caption="Recognition Result", width=300)
                            
                            # Show results
                            st.markdown(f"**Found {result['face_count']} face(s):**")
                            for i, face_result in enumerate(result['results']):
                                if face_result['name'] != "Unknown":
                                    st.markdown(f'<div class="success">✅ Face {i+1}: {face_result["name"]} (Confidence: {face_result["confidence"]:.1%})</div>', unsafe_allow_html=True)
                                else:
                                    st.markdown(f'<div class="warning">❓ Face {i+1}: Unknown person</div>', unsafe_allow_html=True)
                        else:
                            st.error("No faces detected or recognition failed")
        
        with col2:
            st.markdown("**Upload Image:**")
            uploaded_image = st.file_uploader("Upload image", type=['jpg', 'jpeg', 'png'])
            
            if uploaded_image:
                image = Image.open(uploaded_image)
                
                # Show original image
                st.image(image, caption="Original", width=300)
                
                if st.button("🔍 Recognize Uploaded", type="primary"):
                    with st.spinner("Recognizing..."):
                        result = recognize_image(image)
                        if result:
                            # Show annotated image
                            annotated_img = Image.fromarray(result['annotated_image'])
                            st.image(annotated_img, caption="Recognition Result", width=300)
                            
                            # Show results
                            st.markdown(f"**Found {result['face_count']} face(s):**")
                            for i, face_result in enumerate(result['results']):
                                if face_result['name'] != "Unknown":
                                    st.markdown(f'<div class="success">✅ Face {i+1}: {face_result["name"]} (Confidence: {face_result["confidence"]:.1%})</div>', unsafe_allow_html=True)
                                else:
                                    st.markdown(f'<div class="warning">❓ Face {i+1}: Unknown person</div>', unsafe_allow_html=True)
                        else:
                            st.error("No faces detected or recognition failed")
    
    with tab2:
        st.markdown("### Live Recognition")
        
        # Quick stats
        users = len(set([emb["identity"] for emb in st.session_state.db_embeddings]))
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("👥 Users", users)
        with col2:
            st.metric("🔍 Liveness", "Active" if st.session_state.liveness_model else "Inactive")
        with col3:
            st.metric("🎯 Threshold", "0.50")
        
        # Live feed
        video_processor = FaceRecognitionProcessor(
            db_embeddings=st.session_state.db_embeddings,
            liveness_model=st.session_state.liveness_model
        )
        
        webrtc_ctx = webrtc_streamer(
            key="face-recognition-live",
            video_processor_factory=lambda: video_processor,
            rtc_configuration=RTC_CONFIGURATION,
            media_stream_constraints={"video": True, "audio": False},
            async_processing=True,
        )
        
        if webrtc_ctx.state.playing:
            st.markdown('<div class="success">🎥 Live recognition active!</div>', unsafe_allow_html=True)
        
        # Legend
        st.markdown("""
        **Legend:** 🟢 Recognized | 🔴 Unknown | 🟡 Processing | REAL/FAKE Liveness
        """)

def recognize_image(image):
    """Recognize face in single image and return result with annotated image"""
    try:
        # Convert to numpy array
        img_array = np.array(image)
        
        # Create a copy for annotation
        annotated_img = img_array.copy()
        
        # Extract faces
        faces = DeepFace.extract_faces(
            img_path=img_array,
            detector_backend='opencv',
            enforce_detection=False,
            align=False
        )
        
        if not faces:
            return None
        
        results = []
        
        for face_obj in faces:
            coords = face_obj["facial_area"]
            face_img = face_obj["face"]
            
            # Convert face image
            if face_img.max() <= 1:
                face_img = (face_img * 255).astype(np.uint8)
            
            if len(face_img.shape) == 3:
                face_rgb = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)
            else:
                face_rgb = face_img
            
            # Extract embedding
            embedding_result = DeepFace.represent(
                img_path=face_rgb,
                model_name=MODEL_NAME,
                enforce_detection=False
            )
            
            if not embedding_result:
                continue
            
            embedding = embedding_result[0]["embedding"]
            
            # Compare with database
            best_match = None
            best_score = 1.0
            
            for db_entry in st.session_state.db_embeddings:
                db_embedding = db_entry["embedding"]
                dist = cosine(embedding, db_embedding)
                
                if dist < 0.5 and dist < best_score:
                    best_score = dist
                    best_match = db_entry["identity"]
            
            # Draw bounding box and label on annotated image
            x, y, w, h = coords["x"], coords["y"], coords["w"], coords["h"]
            
            if best_match:
                name = best_match
                confidence = 1 - best_score
                color = (0, 255, 0)  # Green for recognized
                label = f"{name} ({confidence:.1%})"
            else:
                name = "Unknown"
                confidence = 0
                color = (0, 0, 255)  # Red for unknown
                label = "Unknown"
            
            # Draw rectangle and text
            cv2.rectangle(annotated_img, (int(x), int(y)), (int(x+w), int(y+h)), color, 2)
            cv2.putText(annotated_img, label, (int(x), int(y) - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
            
            results.append({
                'name': name,
                'confidence': confidence,
                'distance': best_score if best_match else 1.0,
                'coords': coords
            })
        
        return {
            'results': results,
            'annotated_image': annotated_img,
            'face_count': len(faces)
        }
            
    except Exception as e:
        return None

if __name__ == "__main__":
    main()

