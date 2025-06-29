import streamlit as st
from groq import Groq
import re

st.title("Chat Bot")

chat_api_key = st.secrets["groq_api_key"]

client = Groq(api_key = chat_api_key)

# chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "groq_model" not in st.session_state:
    st.session_state["groq_model"] = "llama3-8b-8192"  

if "last_selected_model" not in st.session_state:
    st.session_state["last_selected_model"] = st.session_state["groq_model"]      


col1, col2 = st.columns([3,1])

with col1:
    model = st.selectbox(
        "Select Model",
        options=["llama3-8b-8192", "llama3-70b-8192", "deepseek-r1-distill-llama-70b","qwen/qwen3-32b","meta-llama/llama-prompt-guard-2-86m"],  # add your supported models here
        index=["llama3-8b-8192", "llama3-70b-8192", "deepseek-r1-distill-llama-70b","qwen/qwen3-32b","meta-llama/llama-prompt-guard-2-86m"].index(st.session_state["groq_model"])
    )

# If the selected model changed, clear chat
if model != st.session_state["last_selected_model"]:
    st.session_state.messages = []
    st.session_state["last_selected_model"] = model

st.session_state["groq_model"] = model

with col2:
    if st.button("Clear Chat"):
        st.session_state.messages = []    

#display chat messages from history
for message in st.session_state.messages:
    if isinstance(message, dict) and "content" in message:
        with st.chat_message(message["role"]):
            if message.get("think"):
                with st.expander("🤖 Internal Thoughts (click to expand)", expanded=False):
                    st.markdown(message["think"])
            st.markdown(message["content"])

#React to user input
prompt = st.chat_input("what is up")
if prompt:

    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append({"role":"user", "content":prompt})

    with st.chat_message("assistant"):
        think_placeholder = st.container()
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

        # message_placeholder.markdown(full_response)

        # Fix broken <think> block: if <think> appears but </think> doesn't
        if "<think>" in full_response and "</think>" not in full_response:
            full_response = full_response.replace("<think>", "")

        # Match ALL <think>...</think> blocks, even if there's more than one
        think_matches = re.findall(r"<think>(.*?)</think>", full_response, flags=re.DOTALL)
        think_content = "\n\n---\n\n".join(t.strip() for t in think_matches if t.strip())
        # think_content = "\n\n---\n\n".join(t.strip() for t in think_matches) if think_matches else ""

        # Remove ALL <think>...</think> blocks from visible content
        visible_content = re.sub(r"<think>.*?</think>", "", full_response, flags=re.DOTALL).strip()

        if think_content:
            with think_placeholder:
                with st.expander("🤖 Internal Thoughts (click to expand)", expanded=False):
                    st.markdown(think_content)

        message_placeholder.markdown(visible_content)

        print("RAW:", repr(full_response))
        print("THINK:", repr(think_content))
        print("VISIBLE:", repr(visible_content))


    st.session_state.messages.append({"role": "assistant", "content": visible_content, "think": think_content})    


