import streamlit as st
import cv2
from reusable.image_functions import load_img, download
import numpy as np
import os
from pathlib import Path

current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
PROTOTXT = current_dir.parent / "data" / "colorize" /"colorization_deploy_v2.prototxt"
POINTS = current_dir.parent / "data" / "colorize" / "pts_in_hull.npy"
MODEL = current_dir.parent / "data" / "colorize" / "colorization_release_v2.caffemodel"

#Load the models
net = cv2.dnn.readNetFromCaffe(PROTOTXT, MODEL)
pts = np.load(POINTS)

st.title("Colorize Black and White Images")

#load centers for ab channel
class8 = net.getLayerId("class8_ab")
conv8 = net.getLayerId("conv8_313_rh")
pts = pts.transpose().reshape(2, 313, 1, 1)
net.getLayer(class8).blobs = [pts.astype("float32")]
net.getLayer(conv8).blobs = [np.full([1, 313], 2.606, dtype="float32")]

def ImageFunction(image,LightnessValue):
    #Load image
    #image = cv2.imread(image)
    scaled = image.astype("float32") / 255.0
    lab = cv2.cvtColor(scaled,cv2.COLOR_BGR2LAB)
    #resize
    resized = cv2.resize(lab, (224,224))
    #Take L channel
    L = cv2.split(resized)[0]
    L-= LightnessValue #hyperparameter 50
    #Get Results
    net.setInput(cv2.dnn.blobFromImage(L))
    ab = net.forward()[0,:, :, :].transpose((1,2,0))
    #resize to original image
    ab = cv2.resize(ab,(image.shape[1],image.shape[0]))
    L = cv2.split(lab)[0]

    #Colorize
    colorized = np.concatenate((L[:, :, np.newaxis],ab),axis=2)
    colorized = cv2.cvtColor(colorized,cv2.COLOR_LAB2BGR)
    colorized = np.clip(colorized,0,1)
    colorized = (255*colorized).astype("uint8")
    return colorized

image = st.file_uploader("Upload a picture")
cv2_img = load_img(image)
if cv2_img is not None:
    st.image(cv2_img)
    LightnessValue = st.slider("Lightness Value",min_value=28,max_value=80,value=50,help="Tune the value based on your preference")
    colorized = ImageFunction(cv2_img,LightnessValue)
    colorized = cv2.cvtColor(colorized, cv2.COLOR_BGR2RGB)
    st.image(colorized)
    download(colorized,"colorized")