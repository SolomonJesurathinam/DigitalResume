"""
Page Configuration, Styling, and Homepage Content
"""

import streamlit as st

def setup_page_config():
    """Setup Streamlit page configuration and custom CSS"""
    
    # Page configuration
    st.set_page_config(
        page_title="Test Report Dashboard", 
        layout="wide",
        initial_sidebar_state="expanded",
        page_icon="📊"
    )
    
    # Custom CSS styling
    st.markdown("""
    <style>
        .main-header {
            font-size: 2.5rem;
            color: #1f77b4;
            text-align: center;
            margin-bottom: 2rem;
        }
        .metric-card {
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            padding: 1rem;
            border-radius: 10px;
            color: white;
            text-align: center;
            margin: 0.5rem;
        }
        .status-passed { color: #28a745; font-weight: bold; }
        .status-failed { color: #dc3545; font-weight: bold; }
        .status-skipped { color: #ffc107; font-weight: bold; }
        .status-pending { color: #17a2b8; font-weight: bold; }
        .sidebar .sidebar-content {
            background: #f8f9fa;
        }
        .feature-card {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin: 10px 0;
            border-left: 4px solid #667eea;
        }
        .code-block {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #28a745;
            font-family: 'Courier New', monospace;
            margin: 10px 0;
        }
        .info-box {
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
        }
        .step-number {
            background: #667eea;
            color: white;
            width: 30px;
            height: 30px;
            border-radius: 50%;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            margin-right: 10px;
        }
    </style>
    """, unsafe_allow_html=True)

def render_homepage():
    """Render the homepage with comprehensive documentation"""
    
    # Main title
    st.markdown('<h1 class="main-header">📊 Test Automation Report Dashboard</h1>', unsafe_allow_html=True)
    
    # Hero section
    st.markdown("""
    <div class="info-box">
        <h2>🚀 Welcome to the Ultimate Test Report Analytics Platform</h2>
        <p>A comprehensive, modular Streamlit dashboard for visualizing and analyzing test automation reports from multiple frameworks with interactive charts, detailed analytics, and professional export options.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick start
    st.subheader("⚡ Quick Start")
    
    st.markdown("**Follow these simple steps to get started:**")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **1️⃣ Select Framework**
        
        Choose from Cucumber, Allure, or Pytest in the sidebar
        """)
    
    with col2:
        st.markdown("""
        **2️⃣ Upload Reports**
        
        Upload your JSON test report files
        """)
    
    with col3:
        st.markdown("""
        **3️⃣ Analyze & Export**
        
        View analytics and export in multiple formats
        """)
    
    # Features section
    st.subheader("🎯 Key Features")
    
    tab1, tab2, tab3 = st.tabs(["📊 Analytics", "🌐 Export Options", "⚙️ Supported Frameworks"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **📈 Interactive Analytics**
            - Summary metrics with pass rates
            - Visual charts (pie, bar, histogram, box plots)  
            - Tag analysis and usage patterns
            - Failed test analysis and error tracking
            - Real-time search and filtering
            - Duration and performance analysis
            """)
        
        with col2:
            st.markdown("""
            **🔍 Advanced Features**
            - Collapsible error messages in HTML
            - Responsive design for all devices
            - Status color coding throughout
            - Feature-wise test breakdown
            - Step-level failure analysis
            - Comprehensive test metrics
            """)
    
    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **📄 Export Formats**
            - **CSV** - Raw data for spreadsheet analysis
            - **JSON** - Structured data for API integration
            - **HTML** - Interactive report with charts
            - **PDF** - Professional report with charts
            """)
        
        with col2:
            st.markdown("""
            **🌐 HTML Report Features**
            - Interactive Chart.js visualizations
            - Collapsible error messages (>100 chars)
            - Responsive mobile-friendly design
            - Professional styling and branding
            - Status-based color coding
            """)
    
    with tab3:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            **🥒 Cucumber**
            - Scenario and scenario outline support
            - Background step handling
            - Tag analysis and filtering
            - Step-level failure tracking
            - Feature organization
            - Duration analysis per scenario
            """)
        
        with col2:
            st.markdown("""
            **🎯 Allure**
            - Test result parsing
            - Suite organization
            - Timing analysis
            - Status tracking
            - Multi-file support
            - Performance metrics
            """)
        
        with col3:
            st.markdown("""
            **🧪 Pytest**
            - Test outcome analysis
            - File-based organization
            - Duration tracking
            - Node ID parsing
            - Call result analysis
            - Coverage integration
            """)
    
    # Sample formats section
    st.subheader("📋 Supported File Formats")
    
    st.markdown("**Upload JSON files in these formats:**")
    
    format_col1, format_col2, format_col3 = st.columns(3)
    
    with format_col1:
        st.markdown("**🥒 Cucumber JSON**")
        st.code('''[
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
]''', language='json')
    
    with format_col2:
        st.markdown("**🎯 Allure JSON**")
        st.code('''{
  "name": "Test Name",
  "status": "passed",
  "start": 1234567890,
  "stop": 1234567891
}''', language='json')
    
    with format_col3:
        st.markdown("**🧪 Pytest JSON**")
        st.code('''{
  "tests": [
    {
      "nodeid": "test_file.py::test_function",
      "outcome": "passed",
      "call": {
        "duration": 0.001
      }
    }
  ]
}''', language='json')
    
    
    # Tips section
    st.subheader("💡 Pro Tips")
    
    tip_col1, tip_col2, tip_col3 = st.columns(3)
    
    with tip_col1:
        st.markdown("""
        **🔍 Search Tips**
        - Use the search box to filter tests
        - Search works across scenarios, features, and error messages
        - Case-insensitive search supported
        """)
    
    with tip_col2:
        st.markdown("""
        **📊 Chart Interaction**
        - Hover over charts for detailed info
        - Click legend items to toggle data
        - Charts are responsive and mobile-friendly
        """)
    
    with tip_col3:
        st.markdown("""
        **📥 Export Best Practices**
        - Use CSV for data analysis in Excel
        - Use HTML for sharing with stakeholders  
        - Use PDF for formal reporting
        - Use JSON for API integration
        """)
    
    # Footer section
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <h3>🚀 Ready to Get Started?</h3>
        <p>Upload your test report using the sidebar to begin analyzing your test results!</p>
        <p><strong>Built with ❤️ using Streamlit</strong> | Enhanced Modular Architecture</p>
    </div>
    """, unsafe_allow_html=True)