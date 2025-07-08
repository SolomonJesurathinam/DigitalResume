"""
Download Components for Reports
"""

import streamlit as st
from pages_automation.dashboard_reusable.report_generators import (
    generate_csv_report, 
    generate_json_report, 
    generate_html_report, 
    generate_pdf_report,
    get_filename
)

def render_download_section(df, framework):
    """Render download section with all export options"""
    
    st.subheader("📥 Download Reports")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # CSV download
        csv_data = generate_csv_report(df)
        st.download_button(
            label="📊 Download CSV",
            data=csv_data,
            file_name=get_filename(framework, "csv"),
            mime="text/csv"
        )
    
    with col2:
        # JSON download
        json_data = generate_json_report(df)
        st.download_button(
            label="📋 Download JSON",
            data=json_data,
            file_name=get_filename(framework, "json"),
            mime="application/json"
        )
    
    with col3:
        # HTML download
        html_data = generate_html_report(df, framework)
        st.download_button(
            label="🌐 Download HTML",
            data=html_data,
            file_name=get_filename(framework, "html"),
            mime="text/html"
        )
    
    with col4:
        # PDF download
        pdf_data = generate_pdf_report(df, framework)
        if pdf_data:
            st.download_button(
                label="📄 Download PDF",
                data=pdf_data,
                file_name=get_filename(framework, "pdf"),
                mime="application/pdf"
            )
        else:
            st.info("PDF export requires reportlab. Install with: pip install reportlab")