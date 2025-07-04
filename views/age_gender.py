import streamlit as st
import tensorflow as tf
from pathlib import Path
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import load_model
import cv2
import numpy as np
import os

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
        cv2.putText(image, str(gender," - ",age), (x, y - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
    return image

def radio_functiom(input_image):
    if input_image is not None:
        bytes_data = input_image.getvalue()
        cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
        cv2_img = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
        output = predict(cv2_img)
        st.image(output)

radio_values = st.radio(label="Prediction",options= ("Upload a picture","Photo from Camera"))
if radio_values == "Upload a picture":
    input_image = st.file_uploader("Upload a pic",type=['png', 'jpg'])
    radio_functiom(input_image)

if radio_values == "Photo from Camera":
    input_image = st.camera_input("Take a Picture to predict")
    radio_functiom(input_image) 