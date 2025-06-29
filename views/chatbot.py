import streamlit as st
from groq import Groq

st.title("Chat Bot")

chat_api_key = st.secrets["groq_api_key"]

client = Groq(api_key = chat_api_key)

# chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "groq_model" not in st.session_state:
    st.session_state["groq_model"] = "llama3-8b-8192"    


col1, col2 = st.columns([3,1])

with col1:
    model = st.selectbox(
        "Select Model",
        options=["llama3-8b-8192", "llama2-7b", "llama2-13b"],  # add your supported models here
        index=["llama3-8b-8192", "llama2-7b", "llama2-13b"].index(st.session_state["groq_model"])
    )
    st.session_state["groq_model"] = model

with col2:
    if st.button("Clear Chat"):
        st.session_state.messages = []    

#display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

#React to user input
prompt = st.chat_input("what is up")
if prompt:

    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append({"role":"user", "content":prompt})

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        context_window = st.session_state.messages[-10:]

        for chunk in client.chat.completions.create(
            model = st.session_state["groq_model"],
            messages = [
                {"role": m["role"], "content":m["content"]}
                for m in context_window
            ],
            stream = True
        ):
            content = chunk.choices[0].delta.content or ""
            full_response += content
            message_placeholder.markdown(full_response + "▌")

        message_placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})    


