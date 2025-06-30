import streamlit as st
from groq import Groq
import re
from pathlib import Path

current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
css_file = current_dir.parent / "styles" / "main.css"

with open(css_file) as f:
    st.markdown("<style>{}</style>".format(f.read()),unsafe_allow_html=True)

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


model = st.sidebar.selectbox(
    "Select Model",
    options=["llama3-8b-8192", "llama3-70b-8192", "deepseek-r1-distill-llama-70b","qwen/qwen3-32b"],  # add your supported models here
    index=["llama3-8b-8192", "llama3-70b-8192", "deepseek-r1-distill-llama-70b","qwen/qwen3-32b"].index(st.session_state["groq_model"])
)

if model != st.session_state["last_selected_model"]:
    st.session_state.messages = []
    st.session_state["last_selected_model"] = model

st.session_state["groq_model"] = model

if st.sidebar.button("Clear Chat",type="primary"):
    st.session_state.messages = []    

with st.sidebar:
    st.header("🤖 ChatBot Info")
    st.markdown("""
    **Welcome to the ChatBot!**

    - Powered by **Groq API** using `llama3-8b-8192` and other LLaMA models.
    - Choose different models from the dropdown above.
    - Click **Clear Chat** to reset the conversation.

    ---
    **Tip**: Keep your prompts clear for best results!
    """)


#display chat messages from history
for message in st.session_state.messages:
    if isinstance(message, dict) and "content" in message:
        with st.chat_message(message["role"]):
            if message.get("think"):
                with st.expander("🤖 Internal Thoughts (click to expand)", expanded=False):
                    st.markdown(message["think"])
            st.markdown(message["content"])

#React to user input
prompt = st.chat_input("What's up")
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

    st.session_state.messages.append({"role": "assistant", "content": visible_content, "think": think_content})    


