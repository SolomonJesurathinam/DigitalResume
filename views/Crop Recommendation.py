import streamlit as st
import pandas as pd
import os
import pickle
#st.sidebar.write("Details about Project")

#read excel
ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
model_path = os.path.join(ROOT_DIR,'data',"gaussian_model.pkl")

st.set_page_config(initial_sidebar_state="auto",page_title="Crop Recommendation",page_icon="🌱")
st.header("Crop Recommendation🌱")

st.subheader("Find out the suitable crop for your farm 👨‍🌾")

N = st.number_input("Nitrogen",min_value=1,max_value=10000,step=1)
P = st.number_input("Phosporus",min_value=1,max_value=10000,step=1)
K = st.number_input("Potassium",min_value=1,max_value=10000,step=1)
temperature = st.number_input("Temperature",min_value=0.00,max_value=100000.00)
humidity = st.number_input("Humidity in %",min_value=0.00,max_value=100000.00)
ph = st.number_input("Ph",min_value=0.00,max_value=100000.00)
rainfall = st.number_input("Rainfall in mm",min_value=0.00,max_value=100000.00)

xvalue = [[N,P,K,temperature,humidity,ph,rainfall]]
with open(model_path, "rb") as f:
    loaded_model = pickle.load(f)

if st.button("Predict",type="primary"):
    y_predict = loaded_model.predict(xvalue)
    st.success("{} are recommended by A.I".format(y_predict[0].capitalize()))
st.warning("Note: This A.I application is just for educational/demo purposes only and cannot be relied upon.")


with st.sidebar.expander("Information", expanded=True):
    st.write('''Crop recommendation is a key aspect of precision agriculture.
                Many small farms grow the same crops for generations, often missing more optimal choices.
                This project builds a crop recommender system using a Gaussian Naive Bayes model to suggest the best crop based on soil minerals and climate conditions.''')

st.sidebar.subheader("How this will work ❓")
st.sidebar.write("Complete all the parameters and the ML model will predict the most suitable crops to grow based on various parameters")

