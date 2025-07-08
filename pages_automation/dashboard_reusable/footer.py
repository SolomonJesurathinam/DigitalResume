"""
Footer Component
"""

import streamlit as st

def render_footer():
    """Render footer section"""
    
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; color: #6c757d; padding: 20px;">
            <p><strong>Test Report Dashboard</strong> | Built with Streamlit | 🚀 Enhanced Modular Version</p>
            <p>Supports Cucumber, Allure, and Pytest reports with interactive charts and multiple export formats</p>
        </div>
        """, 
        unsafe_allow_html=True
    )