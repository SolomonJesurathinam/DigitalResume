import streamlit as st
import requests

OWNER = "SolomonJesurathinam"
REPO = "SeleniumFramework_Java"

GITHUB_URL = f"https://github.com/{OWNER}/{REPO}"

HEADERS = {}
if "GITHUB_TOKEN" in st.secrets:
    HEADERS = {"Authorization": f"token {st.secrets['GITHUB_TOKEN']}"}


@st.cache_data
def get_default_branch():
    url = f"https://api.github.com/repos/{OWNER}/{REPO}"
    res = requests.get(url, headers=HEADERS)
    if res.status_code == 200:
        return res.json().get("default_branch", "master")
    return "master"


@st.cache_data
def fetch_github_tree(branch):
    branch_url = f"https://api.github.com/repos/{OWNER}/{REPO}/branches/{branch}"
    res = requests.get(branch_url, headers=HEADERS)
    if res.status_code != 200:
        st.error("❌ Failed to get branch info.")
        return []

    sha = res.json()["commit"]["commit"]["tree"]["sha"]
    tree_url = f"https://api.github.com/repos/{OWNER}/{REPO}/git/trees/{sha}?recursive=1"
    res = requests.get(tree_url, headers=HEADERS)
    if res.status_code != 200:
        st.error("❌ Failed to load GitHub file tree.")
        return []

    return [item for item in res.json()["tree"] if item["type"] in ("blob", "tree")]


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
            if key.endswith(".java"):
                icon = ":notebook:"
            elif key.endswith(".xml"):
                icon = "📜"
            elif key.endswith(".md"):
                icon = "📘"
            elif key.endswith(".json"):
                icon = "🛠️"
            else:
                icon = "💻"

            if not key.startswith(".gitignore"):
                if st.button(f"{indent}{icon} {key}", key=file_path, type="tertiary"):    
                    selected = file_path
    return selected 


# Sidebar navigation
st.sidebar.title("🔍 View")
view_option = st.sidebar.radio(
    "Choose what to display:",
    ["README", "View Files in Streamlit"],
    index=0
)

branch = get_default_branch()

# Main view logic
if view_option == "README":
    # st.title(f" Selenium Framework")
    readme = fetch_readme(branch)
    if readme:
        st.markdown(readme, unsafe_allow_html=True)
    else:
        st.warning("⚠️ README.md not found.")

elif view_option == "View Files in Streamlit":
    st.title("📂 File Explorer")

    file_list = fetch_github_tree(branch)

    if not file_list:
        st.warning("⚠️ No files found or failed to load GitHub tree.")
    else:
        tree = build_tree(file_list)
        col1, col2 = st.columns([2, 4])  # Widen left column

        with col1:
            st.markdown("### 📁 Repository")
            selected_file = render_tree(tree)

        with col2:
            if selected_file:

                if selected_file.endswith(".java"):
                    icon = ":notebook:"
                elif selected_file.endswith(".xml"):
                    icon = "📜"
                elif selected_file.endswith(".md"):
                    icon = "📘"
                elif selected_file.endswith(".json"):
                    icon = "🛠️"
                else:
                    icon = "💻"
                
                st.markdown(f"### {icon} {selected_file}")
                content = fetch_file_content(branch, selected_file)
                if selected_file.endswith((".png", ".jpg", ".jpeg")):
                    st.image(content)
                elif selected_file.endswith(".md"):
                    st.markdown(content)
                else:
                    lang = "java" if selected_file.endswith(".java") else "text"
                    st.code(content, language=lang)
            else:
                st.info("👉 Select a file to view its content.")

# st.sidebar.title("🔗 Github")    
st.sidebar.markdown(f"[Open on GitHub →]({GITHUB_URL})", unsafe_allow_html=True)
