"""
Main Content Rendering Components
"""

import streamlit as st
import json
from pages_automation.dashboard_reusable.test_parsers import get_parser_by_framework
from pages_automation.dashboard_reusable.metrics import render_summary_metrics, apply_filters, style_dataframe, get_status_column
from pages_automation.dashboard_reusable.charts import render_charts, render_tag_analysis, render_failed_analysis
from pages_automation.dashboard_reusable.downloads import render_download_section
from pages_automation.dashboard_reusable.sidebar import render_sample_formats

def load_and_parse_data(config):
    """Load and parse test data based on configuration"""
    
    framework = config["framework"]
    parser = get_parser_by_framework(framework)
    
    if not parser:
        st.error(f"No parser available for {framework}")
        return None
    
    # Load data based on framework
    if framework == "Allure" and config["files"]:
        with st.spinner("Parsing Allure reports..."):
            return parser(config["files"])
    elif framework != "Allure" and config["file"]:
        with st.spinner(f"Parsing {framework} report..."):
            data = json.load(config["file"])
            return parser(data)
    
    return None

def render_data_table(df, config, framework):
    """Render the detailed data table with search and styling"""
    
    st.subheader("📋 Detailed Test Results")
    
    # Add search functionality
    search_term = st.text_input("🔍 Search tests", 
                               placeholder="Search by scenario name, feature, or error message...")
    
    # Apply search filter
    if search_term:
        if framework == "Cucumber":
            mask = (
                df["Scenario"].str.contains(search_term, case=False, na=False) |
                df["Feature"].str.contains(search_term, case=False, na=False) |
                df["Error Message"].str.contains(search_term, case=False, na=False)
            )
        else:
            mask = df.iloc[:, 0].str.contains(search_term, case=False, na=False)
        
        df_filtered = df[mask]
    else:
        df_filtered = df
    
    # Select appropriate columns for display
    if framework == "Cucumber":
        display_df = df_filtered[["Feature", "Scenario", "Status", "Duration (s)", 
                                "Error Message", "Failed Step", "Tags"]]
    else:
        display_df = df_filtered
    
    # Apply styling
    status_col = get_status_column(framework)
    if status_col in display_df.columns:
        styled_df = style_dataframe(display_df, status_col)
        st.dataframe(styled_df, use_container_width=True)
    else:
        st.dataframe(display_df, use_container_width=True)

def render_main_content(config):
    """Render the main dashboard content"""
    
    # Load and parse data
    df = load_and_parse_data(config)
    
    if df is not None and not df.empty:
        st.success("✅ Report parsed successfully!")
        
        # Apply filters
        df_filtered = apply_filters(df, config, config["framework"])
        
        # Render summary metrics
        metrics = render_summary_metrics(df_filtered, config["framework"])
        
        # Render charts
        render_charts(df_filtered, config, config["framework"])
        
        # Render tag analysis for Cucumber
        if config["framework"] == "Cucumber" and config.get("show_tag_analysis"):
            render_tag_analysis(df_filtered)
        
        # Render failed analysis
        render_failed_analysis(df_filtered, config["framework"])
        
        # Render detailed data table
        render_data_table(df_filtered, config, config["framework"])
        
        # Render download section
        render_download_section(df_filtered, config["framework"])
        
    elif config["files"] or config["file"]:
        st.error("❌ Failed to parse the uploaded file(s). Please check the file format.")
        render_sample_formats(config["framework"])
    else:
        st.info("👆 Please upload a test report file to get started!")
        render_sample_formats(config["framework"])