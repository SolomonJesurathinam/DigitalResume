import streamlit as st
import requests

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="GitHub Repository Viewer | Solomon J",
    page_icon="📂",
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
        max-width: 1400px;
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
        margin-bottom: 1rem;
    }
    
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        font-style: italic;
    }
    
    /* Sidebar styling */
    .stSidebar {
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(10px);
    }
    
    /* Remove all custom box styling */
    
    /* File tree styling */
    .stButton[data-testid="baseButton-secondary"] {
        background: rgba(255, 255, 255, 0.8) !important;
        border: 1px solid rgba(102, 126, 234, 0.2) !important;
        border-radius: 8px !important;
        color: #2c3e50 !important;
        transition: all 0.3s ease !important;
        margin: 0.2rem 0 !important;
        text-align: left !important;
        width: 100% !important;
    }
    
    .stButton[data-testid="baseButton-secondary"]:hover {
        background: linear-gradient(45deg, #667eea, #764ba2) !important;
        color: white !important;
        transform: translateX(5px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: rgba(102, 126, 234, 0.1) !important;
        border-radius: 8px !important;
        color: #2c3e50 !important;
        font-weight: 600 !important;
        border: 1px solid rgba(102, 126, 234, 0.2) !important;
    }
    
    .streamlit-expanderHeader:hover {
        background: rgba(102, 126, 234, 0.2) !important;
    }
    
    .streamlit-expanderContent {
        background: rgba(255, 255, 255, 0.3) !important;
        border-radius: 0 0 8px 8px !important;
        backdrop-filter: blur(4px) !important;
        border: 1px solid rgba(102, 126, 234, 0.1) !important;
        border-top: none !important;
    }
    
    /* Code block styling */
    .stCodeBlock {
        background: rgba(255, 255, 255, 0.9) !important;
        border-radius: 15px !important;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37) !important;
        border: 1px solid rgba(255, 255, 255, 0.18) !important;
        backdrop-filter: blur(8px) !important;
        margin: 1rem 0 !important;
    }
    
    /* Markdown content styling - remove excessive boxes */
    .stMarkdown {
        background: transparent;
        padding: 0;
        border-radius: 0;
        box-shadow: none;
        border: none;
        backdrop-filter: none;
        margin: 0;
    }
    
    /* Info card styling - remove from sidebar */
    
    /* Repository info styling - keep only for main content */
    .repo-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
    }
    
    .repo-header h1, .repo-header h2, .repo-header h3 {
        color: white !important;
        margin: 0.5rem 0;
    }
    
    /* Section headers */
    .section-header {
        color: #2c3e50;
        font-weight: bold;
        font-size: 1.3rem;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #667eea;
    }
    
    /* GitHub link styling - simplified */
    .stSidebar a {
        color: #667eea !important;
        text-decoration: none !important;
        font-weight: 600 !important;
    }
    
    .stSidebar a:hover {
        color: #764ba2 !important;
    }
    
    /* Status badges */
    .status-badge {
        display: inline-block;
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
        margin: 0.2rem;
    }
    
    /* Warning and error styling */
    .stWarning {
        background: rgba(255, 193, 7, 0.1) !important;
        border: 1px solid rgba(255, 193, 7, 0.3) !important;
        border-radius: 10px !important;
        backdrop-filter: blur(8px) !important;
    }
    
    .stError {
        background: rgba(220, 53, 69, 0.1) !important;
        border: 1px solid rgba(220, 53, 69, 0.3) !important;
        border-radius: 10px !important;
        backdrop-filter: blur(8px) !important;
    }
    
    .stInfo {
        background: rgba(13, 202, 240, 0.1) !important;
        border: 1px solid rgba(13, 202, 240, 0.3) !important;
        border-radius: 10px !important;
        backdrop-filter: blur(8px) !important;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2rem;
        }
        
        .repo-header {
            padding: 1rem;
        }
        
        .file-content-area, .file-tree-area {
            padding: 1rem;
        }
        
        .info-card {
            padding: 1rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# --- REPOSITORY CONFIGURATION ---
OWNER = "SolomonJesurathinam"
REPO = "SeleniumFramework_Java"
GITHUB_URL = f"https://github.com/{OWNER}/{REPO}"

HEADERS = {}
if "GITHUB_TOKEN" in st.secrets:
    HEADERS = {"Authorization": f"token {st.secrets['GITHUB_TOKEN']}"}

# --- MAIN TITLE ---
st.markdown('<h1 class="main-title">📂 GitHub Repository Viewer</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Explore and browse repository files with interactive navigation</p>', unsafe_allow_html=True)

# --- REPOSITORY HEADER ---
st.markdown(f"""
<div class="repo-header">
    <h2>🔧 {REPO}</h2>
    <p>by <strong>{OWNER}</strong></p>
    <p>Interactive repository browser with file explorer and content viewer</p>
</div>
""", unsafe_allow_html=True)

# --- CACHING FUNCTIONS ---
@st.cache_data
def get_default_branch():
    url = f"https://api.github.com/repos/{OWNER}/{REPO}"
    res = requests.get(url, headers=HEADERS)
    if res.status_code == 200:
        return res.json().get("default_branch", "master")
    return "master"

@st.cache_data
def fetch_github_tree(branch):
    try:
        # Try direct tree API first
        tree_url = f"https://api.github.com/repos/{OWNER}/{REPO}/git/trees/{branch}?recursive=1"
        res = requests.get(tree_url, headers=HEADERS)
        
        if res.status_code == 200:
            return [item for item in res.json()["tree"] if item["type"] in ("blob", "tree")]
        
        # Fallback to contents API
        contents_url = f"https://api.github.com/repos/{OWNER}/{REPO}/contents?ref={branch}"
        res = requests.get(contents_url, headers=HEADERS)
        
        if res.status_code == 200:
            # Convert contents format to tree format
            items = []
            for item in res.json():
                items.append({
                    "path": item["name"],
                    "type": "tree" if item["type"] == "dir" else "blob"
                })
            return items
            
    except Exception as e:
        st.error(f"❌ Error loading repository: {str(e)}")
        return []
    
    st.error("❌ Failed to load GitHub file tree.")
    return []

@st.cache_data
def fetch_file_content(branch, filepath):
    url = f"https://raw.githubusercontent.com/{OWNER}/{REPO}/{branch}/{filepath}"
    res = requests.get(url)
    if res.status_code == 200:
        return res.text
    return "❌ Failed to load file content."

@st.cache_data
def fetch_readme(branch):
    return fetch_file_content(branch, "README.md")

# --- HELPER FUNCTIONS ---
def build_tree(file_list):
    tree = {}
    for item in file_list:
        path_parts = item["path"].split("/")
        current = tree
        for part in path_parts[:-1]:
            if part not in current or not isinstance(current[part], dict):
                current[part] = {}
            current = current[part]
        current[path_parts[-1]] = item["type"]
    return tree

def get_file_icon(filename):
    if filename.endswith(".java"):
        return "☕"
    elif filename.endswith(".xml"):
        return "📜"
    elif filename.endswith(".md"):
        return "📘"
    elif filename.endswith(".json"):
        return "🛠️"
    elif filename.endswith((".png", ".jpg", ".jpeg")):
        return "🖼️"
    elif filename.endswith(".yml") or filename.endswith(".yaml"):
        return "⚙️"
    elif filename.endswith(".properties"):
        return "🔧"
    else:
        return "📄"

def render_tree(tree, level=0, parent_key="", selected_file=None):
    selected = selected_file
    indent = "\u2003" * level
    for key, value in tree.items():
        if isinstance(value, dict):
            if not key.startswith(".idea"):
                with st.expander(f"{indent}📁 {key}", expanded=(key == "src")):    
                    sel = render_tree(value, level + 1, f"{parent_key}{key}/", selected)
                    if sel:
                        selected = sel
        else:
            file_path = f"{parent_key}{key}"
            icon = get_file_icon(key)

            if not key.startswith(".gitignore"):
                if st.button(f"{indent}{icon} {key}", key=file_path, type="secondary"):    
                    selected = file_path
    return selected 

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.header("🔍 Navigation")
    
    view_option = st.radio(
        "Choose what to display:",
        ["📘 README", "📂 Browse Files"],
        index=0
    )
    
    st.header("📊 Repository Info")
    st.write("**Owner:** SolomonJesurathinam")
    st.write("**Repository:** SeleniumFramework_Java") 
    st.write("**Type:** Java Selenium Framework")
    
    st.header("✨ Features")
    st.write("• Interactive file browser")
    st.write("• Syntax-highlighted code viewer")
    st.write("• Markdown rendering")
    st.write("• Image preview support")
    st.write("• Real-time GitHub integration")
    
    st.header("💡 Navigation Tips")
    st.write("• Click folder icons to expand/collapse")
    st.write("• Click file names to view content")
    st.write("• Use README view for project overview")
    st.write("• Browse Files for detailed exploration")
    
    # Status
    st.success("🔗 Connected to GitHub")
    st.info("📂 Repository Loaded")
    
    # GitHub link
    st.markdown(f"[🔗 Open on GitHub →]({GITHUB_URL})")

# --- MAIN CONTENT ---
branch = get_default_branch()

if view_option == "📘 README":
    st.markdown("### 📘 Project Documentation")
    
    with st.spinner("📖 Loading README..."):
        readme = fetch_readme(branch)
        
    if readme and readme != "❌ Failed to load file content.":
        st.markdown(readme, unsafe_allow_html=True)
    else:
        st.warning("⚠️ README.md not found in this repository.")

elif view_option == "📂 Browse Files":
    st.markdown("### 📂 Repository File Explorer")

    with st.spinner("🔄 Loading repository structure..."):
        file_list = fetch_github_tree(branch)

    if not file_list:
        st.warning("⚠️ No files found or failed to load GitHub tree.")
    else:
        tree = build_tree(file_list)
        col1, col2 = st.columns([1, 2])

        with col1:
            st.markdown("#### 📁 Repository Structure")
            selected_file = render_tree(tree)

        with col2:
            if selected_file:
                icon = get_file_icon(selected_file)
                st.markdown(f"#### {icon} {selected_file}")
                
                with st.spinner(f"📖 Loading {selected_file}..."):
                    content = fetch_file_content(branch, selected_file)
                    
                if content != "❌ Failed to load file content.":
                    if selected_file.endswith((".png", ".jpg", ".jpeg")):
                        st.image(content)
                    elif selected_file.endswith(".md"):
                        st.markdown(content)
                    else:
                        # Determine language for syntax highlighting
                        if selected_file.endswith(".java"):
                            lang = "java"
                        elif selected_file.endswith(".xml"):
                            lang = "xml"
                        elif selected_file.endswith(".json"):
                            lang = "json"
                        elif selected_file.endswith(".yml") or selected_file.endswith(".yaml"):
                            lang = "yaml"
                        elif selected_file.endswith(".properties"):
                            lang = "properties"
                        else:
                            lang = "text"
                            
                        st.code(content, language=lang)
                else:
                    st.error("❌ Failed to load file content.")
            else:
                st.info("👉 Select a file from the repository structure to view its content here.")

# --- FOOTER ---
st.markdown("---")
st.markdown("""
<div style="
    text-align: center; 
    padding: 1.5rem; 
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); 
    color: white; 
    border-radius: 15px; 
    margin-top: 2rem;
    box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
">
    <h3 style="margin: 0;">🚀 Explore Code Like Never Before</h3>
    <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">
        Interactive repository browsing with beautiful code visualization! 📂
    </p>
</div>
""", unsafe_allow_html=True)