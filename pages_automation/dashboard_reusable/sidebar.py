"""
Sidebar UI Components
"""

import streamlit as st

def render_sidebar():
    """Render sidebar and return configuration"""
    
    with st.sidebar:
        st.header("🔧 Configuration")
        
        # Framework selection
        framework = st.selectbox(
            "Select Test Framework",
            ["Cucumber", "Allure", "Pytest"],
            help="Choose your testing framework"
        )
        
        # File upload
        files = None
        file = None
        
        if framework == "Allure":
            files = st.file_uploader(
                "Upload Allure result files (.json)", 
                accept_multiple_files=True, 
                type="json",
                help="Upload multiple Allure JSON result files"
            )
        else:
            file = st.file_uploader(
                f"Upload {framework} JSON Report", 
                type="json",
                help=f"Upload your {framework} JSON report file"
            )
        
        # Analysis options
        st.subheader("🔍 Analysis Options")
        show_failed_only = st.checkbox("Show only failed tests", value=False)
        show_duration_analysis = st.checkbox("Show duration analysis", value=True)
        show_tag_analysis = st.checkbox("Show tag analysis", value=True) if framework == "Cucumber" else False
        
        # Return configuration dictionary
        return {
            "framework": framework,
            "files": files,
            "file": file,
            "show_failed_only": show_failed_only,
            "show_duration_analysis": show_duration_analysis,
            "show_tag_analysis": show_tag_analysis
        }

def render_sample_formats(framework):
    """Render sample format information"""
    
    st.subheader("📖 Supported Formats")
    
    if framework == "Cucumber":
        st.code("""
        Sample Cucumber JSON structure:
        [
          {
            "name": "Feature Name",
            "elements": [
              {
                "type": "scenario",
                "name": "Scenario Name",
                "steps": [
                  {
                    "name": "Step Name",
                    "result": {
                      "status": "passed",
                      "duration": 1000000
                    }
                  }
                ]
              }
            ]
          }
        ]
        """)
    
    elif framework == "Allure":
        st.code("""
        Sample Allure JSON structure:
        {
          "name": "Test Name",
          "status": "passed",
          "start": 1234567890,
          "stop": 1234567891
        }
        """)
    
    else:  # Pytest
        st.code("""
        Sample Pytest JSON structure:
        {
          "tests": [
            {
              "nodeid": "test_file.py::test_function",
              "outcome": "passed",
              "call": {
                "duration": 0.001
              }
            }
          ]
        }
        """)