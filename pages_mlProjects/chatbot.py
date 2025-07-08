import streamlit as st
from groq import Groq
import re
from pathlib import Path

# --- PAGE CONFIG ---
st.set_page_config(
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ENHANCED STYLING ---
st.markdown("""
<style>
    /* Show header with styling */
    header[data-testid="stHeader"] {
        visibility: visible !important;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%) !important;
        height: 60px;
    }
    
    header[data-testid="stHeader"] * {
        color: white !important;
    }
    
    header[data-testid="stHeader"] button {
        color: white !important;
        border-color: rgba(255, 255, 255, 0.3) !important;
    }
    
    header[data-testid="stHeader"] button:hover {
        background-color: rgba(255, 255, 255, 0.1) !important;
    }
    
    header[data-testid="stHeader"] svg {
        fill: white !important;
        color: white !important;
    }

    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Main app background */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        min-height: 100vh;
    }
    
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Main title styling */
    .main-title {
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 2rem;
    }
    
    /* Sidebar styling */
    .stSidebar {
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(10px);
    }
    
    .stSidebar .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.9);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 10px;
        backdrop-filter: blur(8px);
    }
    
    .stSidebar .stButton > button {
        background: linear-gradient(45deg, #667eea, #764ba2) !important;
        color: white !important;
        border-radius: 25px !important;
        border: none !important;
        padding: 0.5rem 1rem !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
    }
    
    .stSidebar .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    /* Chat message styling */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.9) !important;
        border-radius: 15px !important;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37) !important;
        border: 1px solid rgba(255, 255, 255, 0.18) !important;
        backdrop-filter: blur(8px) !important;
        margin: 1rem 0 !important;
        padding: 1rem !important;
    }
    
    /* User message styling */
    .stChatMessage[data-testid*="user"] {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1)) !important;
        border-left: 4px solid #667eea !important;
    }
    
    /* Assistant message styling */
    .stChatMessage[data-testid*="assistant"] {
        background: linear-gradient(135deg, rgba(40, 167, 69, 0.1), rgba(23, 162, 184, 0.1)) !important;
        border-left: 4px solid #28a745 !important;
    }
    
    /* Chat input styling */
    .stChatInput > div {
        background: rgba(255, 255, 255, 0.9) !important;
        border-radius: 25px !important;
        border: 2px solid rgba(102, 126, 234, 0.3) !important;
        backdrop-filter: blur(8px) !important;
        box-shadow: 0 4px 16px rgba(31, 38, 135, 0.2) !important;
    }
    
    .stChatInput input {
        background: transparent !important;
        border: none !important;
        color: #2c3e50 !important;
    }
    
    .stChatInput input::placeholder {
        color: #7f8c8d !important;
    }
    
    /* Expander styling for thinking */
    .streamlit-expanderHeader {
        background: rgba(102, 126, 234, 0.1) !important;
        border-radius: 10px !important;
        color: #2c3e50 !important;
        font-weight: 500 !important;
    }
    
    .streamlit-expanderContent {
        background: rgba(255, 255, 255, 0.5) !important;
        border-radius: 0 0 10px 10px !important;
        backdrop-filter: blur(4px) !important;
    }
    
    /* Info card styling */
    .info-card {
        background: rgba(255, 255, 255, 0.9) !important;
        padding: 1.5rem !important;
        border-radius: 15px !important;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37) !important;
        border: 1px solid rgba(255, 255, 255, 0.18) !important;
        border-left: 5px solid #667eea !important;
        margin: 1rem 0 !important;
        backdrop-filter: blur(8px) !important;
    }
    
    .info-card h2 {
        color: #2c3e50 !important;
        margin-bottom: 1rem !important;
        font-size: 1.2rem !important;
    }
    
    .info-card p, .info-card li {
        color: #2c3e50 !important;
        line-height: 1.6 !important;
    }
    
    /* Model selection styling */
    .stSelectbox label {
        color: #2c3e50 !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
    }
    
    /* Section headers */
    .stMarkdown h1 {
        color: #2c3e50 !important;
        font-weight: bold !important;
        margin-bottom: 1rem !important;
    }
    
    /* Typing indicator */
    .typing-indicator {
        color: #667eea;
        animation: pulse 1.5s infinite;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    
    /* Status indicators */
    .model-badge {
        display: inline-block;
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
        margin: 0.2rem 0;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2rem;
        }
        
        .info-card {
            padding: 1rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# --- MAIN TITLE ---
st.markdown('<h1 class="main-title">🤖 AI ChatBot</h1>', unsafe_allow_html=True)

# --- API SETUP ---
chat_api_key = st.secrets["groq_api_key"]
client = Groq(api_key=chat_api_key)

# --- SESSION STATE INITIALIZATION ---
if "messages" not in st.session_state:
    st.session_state.messages = []

if "groq_model" not in st.session_state:
    st.session_state["groq_model"] = "llama3-8b-8192"  

if "last_selected_model" not in st.session_state:
    st.session_state["last_selected_model"] = st.session_state["groq_model"]      

# --- SIDEBAR CONFIGURATION ---
with st.sidebar:
    st.markdown("### 🎛️ Model Configuration")
    
    model = st.selectbox(
        "Select AI Model",
        options=["llama3-8b-8192", "llama3-70b-8192", "deepseek-r1-distill-llama-70b", "qwen/qwen3-32b"],
        index=["llama3-8b-8192", "llama3-70b-8192", "deepseek-r1-distill-llama-70b", "qwen/qwen3-32b"].index(st.session_state["groq_model"]),
        help="Choose the AI model for your conversation"
    )
    
    # Display current model info
    st.markdown(f'<div class="model-badge">Current: {model}</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    if st.button("🗑️ Clear Chat", type="primary", help="Reset the entire conversation"):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    
    # Enhanced info section
    st.markdown("""
    <div class="info-card">
        <h2>🤖 ChatBot Features</h2>
        <p><strong>🚀 Powered by Groq API</strong></p>
        <p>• Multiple LLaMA models available</p>
        <p>• Real-time streaming responses</p>
        <p>• Internal thinking process visible</p>
        <p>• Context-aware conversations</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-card">
        <h2>💡 Tips for Best Results</h2>
        <p>• Be clear and specific in your prompts</p>
        <p>• Use the thinking feature for complex queries</p>
        <p>• Switch models for different capabilities</p>
        <p>• Clear chat when changing topics</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Model switch logic
    if model != st.session_state["last_selected_model"]:
        st.session_state.messages = []
        st.session_state["last_selected_model"] = model
        st.success(f"Switched to {model}! Chat history cleared.")

st.session_state["groq_model"] = model

# --- MAIN CHAT INTERFACE ---

# Display chat messages from history
for message in st.session_state.messages:
    if isinstance(message, dict) and "content" in message:
        with st.chat_message(message["role"]):
            if message.get("think"):
                with st.expander("🧠 AI Internal Thoughts (click to expand)", expanded=False):
                    st.markdown(message["think"])
            st.markdown(message["content"])

# React to user input
prompt = st.chat_input("💭 Ask me anything...", key="chat_input")

if prompt:
    # Add user message to session state first
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response
    with st.chat_message("assistant"):
        think_placeholder = st.container()
        message_placeholder = st.empty()
        full_response = ""

        # Context window (last 10 messages)
        context_window = st.session_state.messages[-10:]

        # Stream the response
        try:
            for chunk in client.chat.completions.create(
                model=st.session_state["groq_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in context_window
                ],
                stream=True
            ):
                content = chunk.choices[0].delta.content or ""
                full_response += content
                message_placeholder.markdown(full_response + '<span class="typing-indicator">▌</span>', unsafe_allow_html=True)

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.stop()

        # Fix broken <think> block
        if "<think>" in full_response and "</think>" not in full_response:
            full_response = full_response.replace("<think>", "")

        # Extract thinking content
        think_matches = re.findall(r"<think>(.*?)</think>", full_response, flags=re.DOTALL)
        think_content = "\n\n---\n\n".join(t.strip() for t in think_matches if t.strip())

        # Remove thinking blocks from visible content
        visible_content = re.sub(r"<think>.*?</think>", "", full_response, flags=re.DOTALL).strip()

        # Display thinking content if available
        if think_content:
            with think_placeholder:
                with st.expander("🧠 AI Internal Thoughts (click to expand)", expanded=False):
                    st.markdown(think_content)

        # Display final response
        message_placeholder.markdown(visible_content)

        # Save assistant response to session state
        st.session_state.messages.append({
            "role": "assistant", 
            "content": visible_content, 
            "think": think_content
        })

# Display conversation stats after processing
if len(st.session_state.messages) > 0:
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("💬 Messages", len(st.session_state.messages))
    with col2:
        user_msgs = len([m for m in st.session_state.messages if m.get("role") == "user"])
        st.metric("👤 User", user_msgs)
    with col3:
        ai_msgs = len([m for m in st.session_state.messages if m.get("role") == "assistant"])
        st.metric("🤖 AI", ai_msgs)

# --- FOOTER ---
st.markdown("---")