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

current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
css_file = current_dir.parent / "styles" / "main.css"

with open(css_file) as f:
    st.markdown("<style>{}</style>".format(f.read()),unsafe_allow_html=True)

current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
gender_path = current_dir.parent / "assets" / "models" /"gender_model_final.keras"
age_path = current_dir.parent / "assets" / "models" /"age_model_final.keras"
img_path = current_dir.parent / "views" / "img1.png"
classifier = current_dir.parent/"assets"/"models"/"haarcascade_frontalface_alt.xml"

gender_model = load_model(gender_path)
age_model = load_model(age_path)

def load_and_preprocess_image(image_path):
    # img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  # Read in grayscale
    img = cv2.resize(image_path, (48, 48))                     # Resize to 48x48
    img = img.astype('float32') / 255.0                 # Normalize
    img = img.reshape(1, 48, 48, 1)                      # Add batch and channel dims
    return img

def predict_image(img):
    image = load_and_preprocess_image(img)
    gender_pred = gender_model.predict(image)
    age_pred = age_model.predict(image)
    pred_gender = "Female" if gender_pred[0][0] > 0.5 else "Male"
    pred_age = int(np.round(age_pred.flatten()[0] * 116)) 
    return pred_gender, pred_age

st.title("Age Gender Prediction")


# image = load_and_preprocess_image(img_path)

def predict(image):
    face_cascade = cv2.CascadeClassifier(classifier)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 255, 0), 2)
        gray_face_img = gray[y:y + h, x:x + w].copy()
        color_face_img = image[y:y + h, x:x + w].copy()

        # Gender and Emotion Prediction
        gender,age = predict_image(gray_face_img)
        cv2.putText(image, str(gender)+" - "+str(age), (x, y - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
    return image

def radio_functiom(input_image):
    if input_image is not None:
        bytes_data = input_image.getvalue()
        cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
        cv2_img = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
        output = predict(cv2_img)
        st.image(output)

radio_values = st.radio(label="Prediction",options= ("Upload a picture","Photo from Camera", "Live Feed"))
if radio_values == "Upload a picture":
    input_image = st.file_uploader("Upload a pic",type=['png', 'jpg'])
    radio_functiom(input_image)

if radio_values == "Photo from Camera":
    input_image = st.camera_input("Take a Picture to predict")
    radio_functiom(input_image) 

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
        cv2.putText(image, label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

    return av.VideoFrame.from_ndarray(image, format="bgr24")

if radio_values == "Live Feed":
    face_cascade = cv2.CascadeClassifier(classifier)
    webrtc_streamer(
    key="age-gender-stream",
    mode=WebRtcMode.SENDRECV,
    video_frame_callback=video_frame_callback,
    media_stream_constraints={"video": True, "audio": False},
    async_processing=True,
)   

with st.sidebar.expander("🔍 Overview", expanded=True):
    st.write("""
    This app predicts **Gender** and **Age** from a human face using two deep learning models trained on the **UTKFace Dataset**.
    """)
    # ---

with st.sidebar.expander("📘 🧠 Models Used", expanded=True):
    st.write("""
    - **Gender Prediction Model**  
    - Input: 48x48 grayscale face image  
    - Output: Binary (0 = Male, 1 = Female)

    - **Age Prediction Model**  
    - Input: 48x48 grayscale face image  
    - Output: Normalized float (scaled to [0, 1])  
    - Final Age = Predicted output × 116 """)


with st.sidebar.expander("📓 Notebook", expanded=False):
    st.write("""
    - Training Code (Gender & Age Models):  
    [🔗 View on GitHub](hhttps://github.com/SolomonJesurathinam/JuypterProjects/blob/master/2025/ageGender/AgeGender-final.ipynb) """)

with st.sidebar.expander("🧾 Credits", expanded=False):
    st.write("""
    - Face Detection: OpenCV Haar Cascade  
    - Models: TensorFlow / Keras  
    - Dataset: UTKFace  
    - UI: Streamlit
    """)