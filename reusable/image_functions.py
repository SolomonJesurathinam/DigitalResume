import cv2
from io import BytesIO, BufferedReader
import streamlit as st
import numpy as np

def resize_func(image):
    # Same resize as you have
    original_shape = image.shape
    if original_shape[0] >= 1000:
        scale_percent = 30
    else:
        scale_percent = 90
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    img = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    return img

def load_img(image):
    if image is not None:
        bytes_data = image.getvalue()
        cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
        cv2_img = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
        return cv2_img

def download(img,imgname):
    im_rgb = img[:, :, [2, 1, 0]]  # numpy.ndarray
    ret, img_enco = cv2.imencode(".png", im_rgb)  # numpy.ndarray
    srt_enco = img_enco.tobytes()  # bytes
    img_BytesIO = BytesIO(srt_enco)  # _io.BytesIO
    img_BufferedReader = BufferedReader(img_BytesIO)  # _io.BufferedReader
    st.download_button(label="Download", data=img_BufferedReader, file_name=imgname+".png", mime="image/png")


def capture_frame(webrtc_ctx):
    capture = st.button("📸 Capture Frame")
    if capture:
        with webrtc_ctx.video_processor.frame_lock:
            frame = webrtc_ctx.video_processor.latest_frame
        if frame is not None:
            st.image(frame, channels="BGR", caption="Captured Frame") 
            _, buffer = cv2.imencode(".png", frame)
            img_bytes = buffer.tobytes()
            st.download_button(
            label="Download Captured Frame",
            data=img_bytes,
            file_name="captured_frame.png",
            mime="image/png"
        )    