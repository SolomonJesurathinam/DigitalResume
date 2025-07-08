"""
Main Dashboard Entry Point
Streamlit Test Report Dashboard
"""

import streamlit as st
from pages_automation.dashboard_reusable.page_config import setup_page_config, render_homepage
from pages_automation.dashboard_reusable.sidebar import render_sidebar
from pages_automation.dashboard_reusable.main_content import render_main_content
from pages_automation.dashboard_reusable.footer import render_footer

def main():
    """Main function to run the dashboard"""
    # Setup page configuration
    setup_page_config()
    
    # Render sidebar and get configuration
    config = render_sidebar()
    
    # Check if user has uploaded files
    has_files = (config["files"] and len(config["files"]) > 0) or config["file"] is not None
    
    if has_files:
        # Render main content with uploaded data
        render_main_content(config)
    else:
        # Render homepage/documentation
        render_homepage()
    
    # Render footer
    render_footer()

if __name__ == "__main__":
    main()