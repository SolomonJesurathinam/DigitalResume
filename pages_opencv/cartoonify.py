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
from reusable.image_functions import resize_func, load_img, download,capture_frame

st.title("Cartoonify Your Image")

def output(img,blur,edge,bFilter):
    img=resize_func(img)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray,blur) #3
    edges = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,edge,edge) #5
    col_img = cv2.bilateralFilter(img,bFilter,255,255) #5
    cartoon = cv2.bitwise_and(col_img,col_img,mask=edges)
    image = cv2.cvtColor(cartoon, cv2.COLOR_BGR2RGB)
    return image

def Catroonify():
    cartoon = output(cv2_img, blur=blur, edge=edge, bFilter=bFilter)
    color_img = cv2.cvtColor(cartoon, cv2.COLOR_BGR2RGB)
    st.image(color_img)
    download(color_img,"cartoonify")    

radio_values = st.radio(label="Prediction",options= ("Upload a picture","Photo from Camera", "Live Feed"))

if radio_values == "Upload a picture":
    input_image = st.file_uploader("Upload a pic",type=['png', 'jpg'])
    cv2_img = load_img(input_image)
    if cv2_img is not None:
        st.image(resize_func(cv2_img))
        st.success("Play around with the parameters to find the right combination")
        blur = st.slider("blur",min_value=1,max_value=21,step=2,value=3)
        edge = st.slider("edge",min_value=3,max_value=21,step=2,value=9)
        bFilter = st.slider("bFilter",min_value=1,max_value=21,step=2,value=5)
        Catroonify()   

if radio_values == "Photo from Camera":
    input_image = st.camera_input("Take a Picture to predict")
    cv2_img = load_img(input_image)
    if cv2_img is not None:
        st.success("Play around with the parameters to find the right combination")
        blur = st.slider("blur",min_value=1,max_value=21,step=2,value=3)
        edge = st.slider("edge",min_value=3,max_value=21,step=2,value=9)
        bFilter = st.slider("bFilter",min_value=1,max_value=21,step=2,value=5)
        Catroonify() 

def cartoonify_image(img, blur, edge, bFilter):
    img = resize_func(img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, blur)
    edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                  cv2.THRESH_BINARY, edge, edge)
    col_img = cv2.bilateralFilter(img, bFilter, 255, 255)
    cartoon = cv2.bitwise_and(col_img, col_img, mask=edges)
    return cartoon

if radio_values == "Live Feed":
    blur = st.slider("Blur", min_value=1, max_value=21, step=2, value=3)
    edge = st.slider("Edge", min_value=3, max_value=21, step=2, value=9)
    bFilter = st.slider("Bilateral Filter", min_value=1, max_value=21, step=2, value=5)

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

    webrtc_ctx = webrtc_streamer(    
    key="cartoonify-stream",
    video_processor_factory=lambda: video_processor,
    media_stream_constraints={"video": True, "audio": False},
    async_processing=True)

    if webrtc_ctx.video_processor:
        webrtc_ctx.video_processor.update_params(blur, edge, bFilter)
        capture_frame(webrtc_ctx)


