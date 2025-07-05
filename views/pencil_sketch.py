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
from reusable.image_functions import resize_func,download, load_img,capture_frame


st.title("Pencil Sketch Your Image")

def PencilnBlack(img,blurValue):
    img = resize_func(img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    neg = 255-gray
    blur = cv2.GaussianBlur(neg,ksize=(blurValue,blurValue),sigmaX=0,sigmaY=0) #21
    pencil = cv2.divide(gray,255-blur,scale=256)
    return pencil 

radio_values = st.radio(label="Prediction",options= ("Upload a picture","Photo from Camera", "Live Feed"))

if radio_values == "Upload a picture":
    input_image = st.file_uploader("Upload a pic",type=['png', 'jpg'])
    cv2_img = load_img(input_image)
    if cv2_img is not None:
        st.image(resize_func(cv2_img))
        blur = st.slider("blurValue",min_value=3,max_value=301,step=2,value=21)
        pencil= PencilnBlack(cv2_img,blurValue=blur)
        color_img = cv2.cvtColor(pencil, cv2.COLOR_BGR2RGB)
        st.image(color_img)
        download(color_img,"pencilSketch")  

if radio_values == "Photo from Camera":
    input_image = st.camera_input("Take a Picture to predict")
    cv2_img = load_img(input_image)
    if cv2_img is not None:
        blur = st.slider("blurValue",min_value=3,max_value=301,step=2,value=21)
        pencil= PencilnBlack(cv2_img,blurValue=blur)
        color_img = cv2.cvtColor(pencil, cv2.COLOR_BGR2RGB)
        st.image(color_img)
        download(color_img,"pencilSketch")  

if radio_values == "Live Feed":
    blur = st.slider("blurValue",min_value=3,max_value=301,step=2,value=21)

    class VideoProcessor(VideoTransformerBase):
        def __init__(self):
            self.blur = blur
            self.latest_frame = None
            self.frame_lock = threading.Lock()
            
        def update_params(self, blur):
            self.blur = blur

        def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
            img = frame.to_ndarray(format="bgr24")
            pencil= PencilnBlack(img,blurValue=self.blur)
            color_img = cv2.cvtColor(pencil, cv2.COLOR_BGR2RGB)
            with self.frame_lock:
                self.latest_frame = color_img.copy()
            return av.VideoFrame.from_ndarray(color_img, format="bgr24")

    # Create an instance of VideoProcessor
    video_processor = VideoProcessor()

    webrtc_ctx = webrtc_streamer(    
    key="pencil-stream",
    video_processor_factory=lambda: video_processor,
    media_stream_constraints={"video": True, "audio": False},
    async_processing=True)

    if webrtc_ctx.video_processor:
        webrtc_ctx.video_processor.update_params(blur)
        capture_frame(webrtc_ctx)


