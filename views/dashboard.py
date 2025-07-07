import streamlit as st
import pandas as pd
import json
from io import StringIO, BytesIO
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime
import base64

# Page configuration
st.set_page_config(
    page_title="Test Report Dashboard", 
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="📊"
)

# Custom CSS for better styling
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
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-header">📊 Test Automation Report Dashboard</h1>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("🔧 Configuration")
    
    # Framework selection
    framework = st.selectbox(
        "Select Test Framework",
        ["Cucumber", "Allure", "Pytest"],
        help="Choose your testing framework"
    )
    
    # File upload
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

# Enhanced parser functions
def parse_cucumber_json(data):
    """Enhanced Cucumber JSON parser with better error handling"""
    results = []
    
    try:
        for feature in data:
            feature_name = feature.get("name", "Unknown Feature")
            feature_uri = feature.get("uri", "")
            
            elements = feature.get("elements", [])
            
            for element in elements:
                element_type = element.get("type", "scenario")
                element_name = element.get("name", "Unknown Element")
                
                # Skip backgrounds
                if element_type == "background":
                    continue
                
                # Handle tags
                tags = element.get("tags", [])
                tag_names = [tag.get("name", "") for tag in tags]
                
                # Process steps
                steps = element.get("steps", [])
                total_duration = 0
                element_status = "passed"
                error_message = ""
                failed_step = ""
                step_count = len(steps)
                
                for step in steps:
                    step_name = step.get("name", "")
                    step_keyword = step.get("keyword", "")
                    
                    result = step.get("result", {})
                    status = result.get("status", "undefined")
                    
                    # Handle duration
                    duration = result.get("duration", 0)
                    if duration and duration > 1000000:  # Likely nanoseconds
                        duration = duration / 1e9
                    total_duration += duration if duration else 0
                    
                    # Determine overall status
                    if status in ["failed", "error"] and element_status == "passed":
                        element_status = status
                        failed_step = f"{step_keyword}{step_name}".strip()
                        error_message = result.get("error_message", "")
                    elif status == "skipped" and element_status == "passed":
                        element_status = "skipped"
                    elif status == "pending" and element_status == "passed":
                        element_status = "pending"
                    elif status == "undefined" and element_status == "passed":
                        element_status = "undefined"
                
                # Handle scenario outlines
                if element_type == "scenario_outline":
                    examples = element.get("examples", [])
                    if examples:
                        for example_table in examples:
                            rows = example_table.get("rows", [])
                            if len(rows) > 1:
                                header = [cell.get("value", "") for cell in rows[0].get("cells", [])]
                                for row_idx, row in enumerate(rows[1:], 1):
                                    values = [cell.get("value", "") for cell in row.get("cells", [])]
                                    example_name = f"{element_name} - Example {row_idx}"
                                    
                                    results.append({
                                        "Feature": feature_name,
                                        "Scenario": example_name,
                                        "Status": element_status,
                                        "Duration (s)": round(total_duration, 3),
                                        "Error Message": error_message.strip(),
                                        "Failed Step": failed_step,
                                        "Tags": ", ".join(tag_names),
                                        "Step Count": step_count,
                                        "Feature URI": feature_uri
                                    })
                    else:
                        results.append({
                            "Feature": feature_name,
                            "Scenario": element_name,
                            "Status": element_status,
                            "Duration (s)": round(total_duration, 3),
                            "Error Message": error_message.strip(),
                            "Failed Step": failed_step,
                            "Tags": ", ".join(tag_names),
                            "Step Count": step_count,
                            "Feature URI": feature_uri
                        })
                else:
                    results.append({
                        "Feature": feature_name,
                        "Scenario": element_name,
                        "Status": element_status,
                        "Duration (s)": round(total_duration, 3),
                        "Error Message": error_message.strip(),
                        "Failed Step": failed_step,
                        "Tags": ", ".join(tag_names),
                        "Step Count": step_count,
                        "Feature URI": feature_uri
                    })
        
        return pd.DataFrame(results)
    
    except Exception as e:
        st.error(f"Error parsing Cucumber JSON: {str(e)}")
        return pd.DataFrame()

def parse_allure_json(files):
    """Enhanced Allure JSON parser"""
    results = []
    try:
        for file in files:
            data = json.load(file)
            if "status" in data:
                duration = (data.get("stop", 0) - data.get("start", 0)) / 1000
                results.append({
                    "Name": data.get("name", ""),
                    "Status": data["status"],
                    "Duration (s)": duration,
                    "Suite": data.get("fullName", "").split(".")[-2] if "." in data.get("fullName", "") else "Unknown"
                })
        return pd.DataFrame(results)
    except Exception as e:
        st.error(f"Error parsing Allure JSON: {str(e)}")
        return pd.DataFrame()

def parse_pytest_json(data):
    """Enhanced Pytest JSON parser"""
    results = []
    try:
        for test in data.get("tests", []):
            call = test.get("call", {})
            results.append({
                "Test": test.get("nodeid", ""),
                "Outcome": test.get("outcome", ""),
                "Duration (s)": call.get("duration", 0),
                "File": test.get("nodeid", "").split("::")[0] if "::" in test.get("nodeid", "") else "Unknown"
            })
        return pd.DataFrame(results)
    except Exception as e:
        st.error(f"Error parsing Pytest JSON: {str(e)}")
        return pd.DataFrame()

# Load and parse data
df = pd.DataFrame()
if framework == "Cucumber" and file:
    with st.spinner("Parsing Cucumber report..."):
        df = parse_cucumber_json(json.load(file))
elif framework == "Allure" and files:
    with st.spinner("Parsing Allure reports..."):
        df = parse_allure_json(files)
elif framework == "Pytest" and file:
    with st.spinner("Parsing Pytest report..."):
        df = parse_pytest_json(json.load(file))

# Display results
if not df.empty:
    st.success("✅ Report parsed successfully!")
    
    # Apply filters
    if show_failed_only:
        if framework == "Cucumber":
            df = df[df["Status"] == "failed"]
        elif framework == "Allure":
            df = df[df["Status"] == "failed"]
        else:
            df = df[df["Outcome"] == "failed"]
    
    # Summary metrics - Fixed status column logic
    st.subheader("📊 Summary Metrics")
    
    if framework == "Cucumber":
        status_col = "Status"
    elif framework == "Allure":
        status_col = "Status"
    else:  # Pytest
        status_col = "Outcome"
    
    total_tests = len(df)
    passed_tests = len(df[df[status_col] == "passed"])
    failed_tests = len(df[df[status_col] == "failed"])
    skipped_tests = len(df[df[status_col] == "skipped"])
    pending_tests = len(df[df[status_col] == "pending"]) if "pending" in df[status_col].values else 0
    pass_rate = (passed_tests/total_tests*100) if total_tests > 0 else 0
    
    # Display metrics
    if pending_tests > 0:
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        with col6:
            st.metric("Pending", pending_tests, delta=f"{(pending_tests/total_tests*100):.1f}%")
    else:
        col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Total Tests", total_tests)
    with col2:
        st.metric("Passed", passed_tests, delta=f"{(passed_tests/total_tests*100):.1f}%")
    with col3:
        st.metric("Failed", failed_tests, delta=f"{(failed_tests/total_tests*100):.1f}%")
    with col4:
        st.metric("Skipped", skipped_tests, delta=f"{(skipped_tests/total_tests*100):.1f}%")
    with col5:
        st.metric("Pass Rate", f"{pass_rate:.1f}%")
    
    # Charts section
    st.subheader("📈 Visual Analytics")
    
    # Create tabs for different charts
    tab1, tab2, tab3 = st.tabs(["Status Distribution", "Duration Analysis", "Feature Analysis"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            # Status distribution pie chart
            status_counts = df[status_col].value_counts()
            fig_pie = px.pie(
                values=status_counts.values,
                names=status_counts.index,
                title="Test Status Distribution",
                color_discrete_map={
                    'passed': '#28a745',
                    'failed': '#dc3545',
                    'skipped': '#ffc107',
                    'pending': '#17a2b8'
                }
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            # Status distribution bar chart
            fig_bar = px.bar(
                x=status_counts.index,
                y=status_counts.values,
                title="Test Status Count",
                labels={'x': 'Status', 'y': 'Count'},
                color=status_counts.index,
                color_discrete_map={
                    'passed': '#28a745',
                    'failed': '#dc3545',
                    'skipped': '#ffc107',
                    'pending': '#17a2b8'
                }
            )
            st.plotly_chart(fig_bar, use_container_width=True)
    
    with tab2:
        if show_duration_analysis and "Duration (s)" in df.columns:
            col1, col2 = st.columns(2)
            
            with col1:
                # Duration histogram
                fig_hist = px.histogram(
                    df, 
                    x="Duration (s)", 
                    nbins=20,
                    title="Test Duration Distribution",
                    labels={'count': 'Number of Tests'}
                )
                st.plotly_chart(fig_hist, use_container_width=True)
            
            with col2:
                # Duration by status
                fig_box = px.box(
                    df, 
                    x=status_col, 
                    y="Duration (s)",
                    title="Duration by Status",
                    color=status_col
                )
                st.plotly_chart(fig_box, use_container_width=True)
    
    with tab3:
        if framework == "Cucumber":
            # Feature analysis
            feature_status = df.groupby(['Feature', 'Status']).size().reset_index(name='Count')
            fig_feature = px.bar(
                feature_status,
                x='Feature',
                y='Count',
                color='Status',
                title="Test Results by Feature",
                barmode='stack'
            )
            fig_feature.update_xaxes(tickangle=45)
            st.plotly_chart(fig_feature, use_container_width=True)
    
    # Tag analysis for Cucumber
    if framework == "Cucumber" and show_tag_analysis and "Tags" in df.columns:
        st.subheader("🏷️ Tag Analysis")
        
        # Extract and count tags
        all_tags = []
        for tags_str in df["Tags"].fillna(""):
            if tags_str:
                all_tags.extend([tag.strip() for tag in tags_str.split(",")])
        
        if all_tags:
            tag_counts = pd.Series(all_tags).value_counts().head(10)
            fig_tags = px.bar(
                x=tag_counts.values,
                y=tag_counts.index,
                orientation='h',
                title="Top 10 Most Used Tags",
                labels={'x': 'Count', 'y': 'Tags'}
            )
            st.plotly_chart(fig_tags, use_container_width=True)
    
    # Failed tests analysis
    if framework == "Cucumber":
        failed_df = df[df["Status"] == "failed"]
        if not failed_df.empty:
            st.subheader("❌ Failed Tests Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Failed Tests by Feature**")
                failed_by_feature = failed_df["Feature"].value_counts()
                st.bar_chart(failed_by_feature)
            
            with col2:
                st.write("**Common Failed Steps**")
                failed_steps = failed_df["Failed Step"].value_counts().head(5)
                st.write(failed_steps)
    
    # Detailed data table
    st.subheader("📋 Detailed Test Results")
    
    # Add search functionality
    search_term = st.text_input("🔍 Search tests", placeholder="Search by scenario name, feature, or error message...")
    
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
    
    # Display dataframe with styling
    if framework == "Cucumber":
        display_df = df_filtered[["Feature", "Scenario", "Status", "Duration (s)", "Error Message", "Failed Step", "Tags"]]
    else:
        display_df = df_filtered
    
    # Style the dataframe
    def highlight_status(val):
        if val == "passed":
            return "background-color: #d4edda; color: #155724"
        elif val == "failed":
            return "background-color: #f8d7da; color: #721c24"
        elif val == "skipped":
            return "background-color: #fff3cd; color: #856404"
        else:
            return ""
    
    styled_df = display_df.style.applymap(highlight_status, subset=[status_col])
    st.dataframe(styled_df, use_container_width=True)
    
    # Download section - Only CSV, JSON, HTML, PDF
    st.subheader("📥 Download Reports")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # CSV download
        csv = df.to_csv(index=False)
        st.download_button(
            label="📊 Download CSV",
            data=csv.encode('utf-8'),
            file_name=f"{framework.lower()}_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    
    with col2:
        # JSON download
        json_str = df.to_json(orient='records', indent=2)
        st.download_button(
            label="📋 Download JSON",
            data=json_str.encode('utf-8'),
            file_name=f"{framework.lower()}_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
    
    with col3:
        # HTML download with charts and collapsible errors
        def generate_html_report_with_charts(df, framework):
            # Calculate metrics properly
            if framework == "Cucumber":
                status_col = "Status"
            elif framework == "Allure":
                status_col = "Status"
            else:  # Pytest
                status_col = "Outcome"
            
            total_tests = len(df)
            passed_tests = len(df[df[status_col] == "passed"])
            failed_tests = len(df[df[status_col] == "failed"])
            skipped_tests = len(df[df[status_col] == "skipped"])
            pending_tests = len(df[df[status_col] == "pending"]) if "pending" in df[status_col].values else 0
            pass_rate = (passed_tests/total_tests*100) if total_tests > 0 else 0
            
            # Generate chart data
            status_counts = df[status_col].value_counts()
            chart_labels = list(status_counts.index)
            chart_values = list(status_counts.values)
            
            # Color mapping
            color_map = {
                'passed': '#28a745',
                'failed': '#dc3545', 
                'skipped': '#ffc107',
                'pending': '#17a2b8'
            }
            chart_colors = [color_map.get(label, '#6c757d') for label in chart_labels]
            
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>{framework} Test Report</title>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
                <style>
                    body {{
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                        margin: 0;
                        padding: 20px;
                        background-color: #f8f9fa;
                        line-height: 1.6;
                    }}
                    .container {{
                        max-width: 1200px;
                        margin: 0 auto;
                    }}
                    .header {{
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        color: white;
                        padding: 30px;
                        border-radius: 15px;
                        text-align: center;
                        margin-bottom: 30px;
                        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                    }}
                    .header h1 {{
                        margin: 0;
                        font-size: 2.5em;
                        font-weight: 300;
                    }}
                    .header p {{
                        margin: 10px 0 0 0;
                        opacity: 0.9;
                    }}
                    .summary {{
                        background: white;
                        padding: 30px;
                        border-radius: 15px;
                        margin-bottom: 30px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                    }}
                    .metrics {{
                        display: grid;
                        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                        gap: 20px;
                        margin-bottom: 30px;
                    }}
                    .metric {{
                        text-align: center;
                        padding: 20px;
                        background: linear-gradient(145deg, #f8f9fa, #e9ecef);
                        border-radius: 12px;
                        border: 1px solid #dee2e6;
                        transition: transform 0.2s;
                    }}
                    .metric:hover {{
                        transform: translateY(-2px);
                    }}
                    .metric-value {{
                        font-size: 2.5em;
                        font-weight: bold;
                        margin-bottom: 5px;
                    }}
                    .metric-label {{
                        color: #6c757d;
                        font-size: 0.9em;
                        text-transform: uppercase;
                        letter-spacing: 1px;
                    }}
                    .status-passed {{ color: #28a745; }}
                    .status-failed {{ color: #dc3545; }}
                    .status-skipped {{ color: #ffc107; }}
                    .status-pending {{ color: #17a2b8; }}
                    
                    .charts-section {{
                        background: white;
                        padding: 30px;
                        border-radius: 15px;
                        margin-bottom: 30px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                    }}
                    .chart-container {{
                        display: grid;
                        grid-template-columns: 1fr 1fr;
                        gap: 30px;
                        margin-top: 20px;
                    }}
                    .chart-box {{
                        position: relative;
                        height: 300px;
                    }}
                    
                    .table-section {{
                        background: white;
                        padding: 30px;
                        border-radius: 15px;
                        margin-bottom: 30px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                    }}
                    table {{
                        width: 100%;
                        border-collapse: collapse;
                        margin-top: 20px;
                    }}
                    th, td {{
                        padding: 12px;
                        text-align: left;
                        border-bottom: 1px solid #dee2e6;
                    }}
                    th {{
                        background: linear-gradient(145deg, #3498db, #2980b9);
                        color: white;
                        font-weight: 600;
                        position: sticky;
                        top: 0;
                    }}
                    tr:nth-child(even) {{
                        background-color: #f8f9fa;
                    }}
                    tr:hover {{
                        background-color: #e3f2fd;
                    }}
                    
                    .collapsible {{
                        background-color: #f1f1f1;
                        color: #444;
                        cursor: pointer;
                        padding: 8px;
                        width: 100%;
                        border: none;
                        text-align: left;
                        outline: none;
                        font-size: 12px;
                        border-radius: 4px;
                        margin: 2px 0;
                    }}
                    .collapsible:hover {{
                        background-color: #ddd;
                    }}
                    .collapsible.active {{
                        background-color: #ccc;
                    }}
                    .content {{
                        padding: 0 8px;
                        max-height: 0;
                        overflow: hidden;
                        transition: max-height 0.2s ease-out;
                        background-color: #f9f9f9;
                        font-size: 11px;
                        border-radius: 0 0 4px 4px;
                    }}
                    .content.show {{
                        max-height: 200px;
                        padding: 8px;
                        overflow-y: auto;
                    }}
                    
                    .footer {{
                        text-align: center;
                        margin-top: 40px;
                        padding: 20px;
                        color: #6c757d;
                        background: white;
                        border-radius: 15px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                    }}
                    
                    @media (max-width: 768px) {{
                        .chart-container {{
                            grid-template-columns: 1fr;
                        }}
                        .metrics {{
                            grid-template-columns: repeat(2, 1fr);
                        }}
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>📊 {framework} Test Report</h1>
                        <p>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                    </div>
                    
                    <div class="summary">
                        <h2>📈 Summary Metrics</h2>
                        <div class="metrics">
                            <div class="metric">
                                <div class="metric-value">{total_tests}</div>
                                <div class="metric-label">Total Tests</div>
                            </div>
                            <div class="metric">
                                <div class="metric-value status-passed">{passed_tests}</div>
                                <div class="metric-label">Passed</div>
                            </div>
                            <div class="metric">
                                <div class="metric-value status-failed">{failed_tests}</div>
                                <div class="metric-label">Failed</div>
                            </div>
                            <div class="metric">
                                <div class="metric-value status-skipped">{skipped_tests}</div>
                                <div class="metric-label">Skipped</div>
                            </div>"""
            
            if pending_tests > 0:
                html_content += f"""
                            <div class="metric">
                                <div class="metric-value status-pending">{pending_tests}</div>
                                <div class="metric-label">Pending</div>
                            </div>"""
            
            html_content += f"""
                            <div class="metric">
                                <div class="metric-value">{pass_rate:.1f}%</div>
                                <div class="metric-label">Pass Rate</div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="charts-section">
                        <h2>📊 Visual Analytics</h2>
                        <div class="chart-container">
                            <div class="chart-box">
                                <canvas id="pieChart"></canvas>
                            </div>
                            <div class="chart-box">
                                <canvas id="barChart"></canvas>
                            </div>
                        </div>
                    </div>
                    
                    <div class="table-section">
                        <h2>📋 Detailed Test Results</h2>
                        <table>
                            <thead>
                                <tr>"""
            
            # Add table headers based on framework
            if framework == "Cucumber":
                html_content += """
                                    <th>Feature</th>
                                    <th>Scenario</th>
                                    <th>Status</th>
                                    <th>Duration (s)</th>
                                    <th>Error Message</th>
                                    <th>Failed Step</th>
                                    <th>Tags</th>"""
            elif framework == "Allure":
                html_content += """
                                    <th>Name</th>
                                    <th>Status</th>
                                    <th>Duration (s)</th>
                                    <th>Suite</th>"""
            else:  # Pytest
                html_content += """
                                    <th>Test</th>
                                    <th>Outcome</th>
                                    <th>Duration (s)</th>
                                    <th>File</th>"""
            
            html_content += """
                                </tr>
                            </thead>
                            <tbody>"""
            
            # Add table rows with collapsible error messages
            for index, row in df.iterrows():
                html_content += "<tr>"
                
                if framework == "Cucumber":
                    error_msg = str(row.get('Error Message', '')).strip()
                    error_cell = ""
                    if error_msg and error_msg != 'nan' and len(error_msg) > 0:
                        if len(error_msg) > 100:
                            error_id = f"error_{index}"
                            error_cell = f'''
                                <button class="collapsible" onclick="toggleError('{error_id}')">
                                    Click to view error ({len(error_msg)} chars)
                                </button>
                                <div id="{error_id}" class="content">
                                    {error_msg}
                                </div>
                            '''
                        else:
                            error_cell = error_msg
                    
                    html_content += f"""
                        <td>{row.get('Feature', '')}</td>
                        <td>{row.get('Scenario', '')}</td>
                        <td><span class="status-{row.get('Status', '').lower()}">{row.get('Status', '')}</span></td>
                        <td>{row.get('Duration (s)', 0)}</td>
                        <td>{error_cell}</td>
                        <td>{row.get('Failed Step', '')}</td>
                        <td>{row.get('Tags', '')}</td>
                    """
                elif framework == "Allure":
                    html_content += f"""
                        <td>{row.get('Name', '')}</td>
                        <td><span class="status-{row.get('Status', '').lower()}">{row.get('Status', '')}</span></td>
                        <td>{row.get('Duration (s)', 0)}</td>
                        <td>{row.get('Suite', '')}</td>
                    """
                else:  # Pytest
                    html_content += f"""
                        <td>{row.get('Test', '')}</td>
                        <td><span class="status-{row.get('Outcome', '').lower()}">{row.get('Outcome', '')}</span></td>
                        <td>{row.get('Duration (s)', 0)}</td>
                        <td>{row.get('File', '')}</td>
                    """
                
                html_content += "</tr>"
            
            html_content += f"""
                            </tbody>
                        </table>
                    </div>
                    
                    <div class="footer">
                        <p><strong>Test Automation Dashboard</strong> | Generated with ❤️</p>
                        <p>Report contains {total_tests} test results | Pass Rate: {pass_rate:.1f}%</p>
                    </div>
                </div>
                
                <script>
                    // Pie Chart
                    const pieCtx = document.getElementById('pieChart').getContext('2d');
                    new Chart(pieCtx, {{
                        type: 'pie',
                        data: {{
                            labels: {chart_labels},
                            datasets: [{{
                                data: {chart_values},
                                backgroundColor: {chart_colors},
                                borderWidth: 2,
                                borderColor: '#ffffff'
                            }}]
                        }},
                        options: {{
                            responsive: true,
                            maintainAspectRatio: false,
                            plugins: {{
                                title: {{
                                    display: true,
                                    text: 'Test Status Distribution',
                                    font: {{ size: 16, weight: 'bold' }}
                                }},
                                legend: {{
                                    position: 'bottom'
                                }}
                            }}
                        }}
                    }});
                    
                    // Bar Chart
                    const barCtx = document.getElementById('barChart').getContext('2d');
                    new Chart(barCtx, {{
                        type: 'bar',
                        data: {{
                            labels: {chart_labels},
                            datasets: [{{
                                label: 'Test Count',
                                data: {chart_values},
                                backgroundColor: {chart_colors},
                                borderColor: {chart_colors},
                                borderWidth: 1
                            }}]
                        }},
                        options: {{
                            responsive: true,
                            maintainAspectRatio: false,
                            plugins: {{
                                title: {{
                                    display: true,
                                    text: 'Test Status Count',
                                    font: {{ size: 16, weight: 'bold' }}
                                }},
                                legend: {{
                                    display: false
                                }}
                            }},
                            scales: {{
                                y: {{
                                    beginAtZero: true,
                                    ticks: {{
                                        stepSize: 1
                                    }}
                                }}
                            }}
                        }}
                    }});
                    
                    // Collapsible error messages
                    function toggleError(errorId) {{
                        const content = document.getElementById(errorId);
                        const button = content.previousElementSibling;
                        
                        if (content.classList.contains('show')) {{
                            content.classList.remove('show');
                            button.classList.remove('active');
                        }} else {{
                            content.classList.add('show');
                            button.classList.add('active');
                        }}
                    }}
                </script>
            </body>
            </html>
            """
            
            return html_content
        
        html_report = generate_html_report_with_charts(df, framework)
        st.download_button(
            label="🌐 Download HTML",
            data=html_report.encode('utf-8'),
            file_name=f"{framework.lower()}_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
            mime="text/html"
        )
    
    with col4:
        # PDF download
        def generate_pdf_report(df, framework):
            try:
                from reportlab.lib.pagesizes import A4
                from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
                from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
                from reportlab.lib.units import inch
                from reportlab.lib import colors
                from reportlab.graphics.shapes import Drawing
                from reportlab.graphics.charts.piecharts import Pie
                from reportlab.lib.enums import TA_CENTER
                from io import BytesIO
                
                buffer = BytesIO()
                doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
                
                elements = []
                styles = getSampleStyleSheet()
                
                title_style = ParagraphStyle(
                    'CustomTitle',
                    parent=styles['Heading1'],
                    fontSize=24,
                    spaceAfter=30,
                    alignment=TA_CENTER,
                    textColor=colors.HexColor('#2c3e50')
                )
                
                heading_style = ParagraphStyle(
                    'CustomHeading',
                    parent=styles['Heading2'],
                    fontSize=16,
                    spaceAfter=12,
                    textColor=colors.HexColor('#34495e')
                )
                
                # Title
                title = Paragraph(f"{framework} Test Report", title_style)
                elements.append(title)
                elements.append(Spacer(1, 12))
                
                # Date
                date_para = Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal'])
                elements.append(date_para)
                elements.append(Spacer(1, 20))
                
                # Summary metrics
                summary_heading = Paragraph("Summary Metrics", heading_style)
                elements.append(summary_heading)
                
                # Calculate metrics - Fixed the status column logic
                if framework == "Cucumber":
                    status_col = "Status"
                elif framework == "Allure":
                    status_col = "Status"
                else:
                    status_col = "Outcome"
                
                total_tests = len(df)
                passed_tests = len(df[df[status_col] == "passed"])
                failed_tests = len(df[df[status_col] == "failed"])
                skipped_tests = len(df[df[status_col] == "skipped"])
                pending_tests = len(df[df[status_col] == "pending"]) if "pending" in df[status_col].values else 0
                pass_rate = (passed_tests/total_tests*100) if total_tests > 0 else 0
                
                # Summary table
                summary_data = [
                    ['Metric', 'Count', 'Percentage'],
                    ['Total Tests', str(total_tests), '100%'],
                    ['Passed', str(passed_tests), f'{(passed_tests/total_tests*100):.1f}%'],
                    ['Failed', str(failed_tests), f'{(failed_tests/total_tests*100):.1f}%'],
                    ['Skipped', str(skipped_tests), f'{(skipped_tests/total_tests*100):.1f}%']
                ]
                
                if pending_tests > 0:
                    summary_data.append(['Pending', str(pending_tests), f'{(pending_tests/total_tests*100):.1f}%'])
                
                summary_data.append(['Pass Rate', f'{pass_rate:.1f}%', ''])
                
                summary_table = Table(summary_data, colWidths=[2*inch, 1*inch, 1*inch])
                summary_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                
                elements.append(summary_table)
                elements.append(Spacer(1, 30))
                
                # Add pie chart
                try:
                    drawing = Drawing(400, 200)
                    pie = Pie()
                    pie.x = 50
                    pie.y = 50
                    pie.width = 100
                    pie.height = 100
                    
                    status_counts = df[status_col].value_counts()
                    pie.data = list(status_counts.values)
                    pie.labels = list(status_counts.index)
                    pie.slices.strokeWidth = 0.5
                    
                    # Color mapping for pie chart
                    color_map = {'passed': colors.green, 'failed': colors.red, 'skipped': colors.orange, 'pending': colors.blue}
                    for i, status in enumerate(status_counts.index):
                        pie.slices[i].fillColor = color_map.get(status, colors.grey)
                    
                    drawing.add(pie)
                    elements.append(drawing)
                    elements.append(Spacer(1, 20))
                except:
                    pass  # Skip chart if there's an error
                
                # Detailed results
                results_heading = Paragraph("Detailed Test Results", heading_style)
                elements.append(results_heading)
                
                # Prepare table data
                if framework == "Cucumber":
                    headers = ['Feature', 'Scenario', 'Status', 'Duration (s)']
                    table_data = [headers]
                    for _, row in df.iterrows():
                        table_data.append([
                            str(row.get('Feature', ''))[:30] + '...' if len(str(row.get('Feature', ''))) > 30 else str(row.get('Feature', '')),
                            str(row.get('Scenario', ''))[:40] + '...' if len(str(row.get('Scenario', ''))) > 40 else str(row.get('Scenario', '')),
                            str(row.get('Status', '')),
                            str(row.get('Duration (s)', 0))
                        ])
                elif framework == "Allure":
                    headers = ['Name', 'Status', 'Duration (s)', 'Suite']
                    table_data = [headers]
                    for _, row in df.iterrows():
                        table_data.append([
                            str(row.get('Name', ''))[:50] + '...' if len(str(row.get('Name', ''))) > 50 else str(row.get('Name', '')),
                            str(row.get('Status', '')),
                            str(row.get('Duration (s)', 0)),
                            str(row.get('Suite', ''))[:20] + '...' if len(str(row.get('Suite', ''))) > 20 else str(row.get('Suite', ''))
                        ])
                else:  # Pytest
                    headers = ['Test', 'Outcome', 'Duration (s)']
                    table_data = [headers]
                    for _, row in df.iterrows():
                        table_data.append([
                            str(row.get('Test', ''))[:60] + '...' if len(str(row.get('Test', ''))) > 60 else str(row.get('Test', '')),
                            str(row.get('Outcome', '')),
                            str(row.get('Duration (s)', 0))
                        ])
                
                # Create table with appropriate column widths
                if framework == "Cucumber":
                    col_widths = [1.5*inch, 2.5*inch, 0.8*inch, 0.8*inch]
                elif framework == "Allure":
                    col_widths = [2.5*inch, 0.8*inch, 0.8*inch, 1.5*inch]
                else:
                    col_widths = [3.5*inch, 0.8*inch, 0.8*inch]
                
                results_table = Table(table_data, colWidths=col_widths, repeatRows=1)
                results_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('FONTSIZE', (0, 1), (-1, -1), 8),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
                ]))
                
                elements.append(results_table)
                
                # Add failed tests section if any
                failed_df = df[df[status_col] == "failed"]
                if not failed_df.empty and framework == "Cucumber":
                    elements.append(PageBreak())
                    failed_heading = Paragraph("Failed Tests Details", heading_style)
                    elements.append(failed_heading)
                    
                    failed_headers = ['Feature', 'Scenario', 'Failed Step', 'Error Message']
                    failed_table_data = [failed_headers]
                    
                    for _, row in failed_df.iterrows():
                        error_msg = str(row.get('Error Message', ''))[:100] + '...' if len(str(row.get('Error Message', ''))) > 100 else str(row.get('Error Message', ''))
                        failed_table_data.append([
                            str(row.get('Feature', ''))[:25] + '...' if len(str(row.get('Feature', ''))) > 25 else str(row.get('Feature', '')),
                            str(row.get('Scenario', ''))[:30] + '...' if len(str(row.get('Scenario', ''))) > 30 else str(row.get('Scenario', '')),
                            str(row.get('Failed Step', ''))[:30] + '...' if len(str(row.get('Failed Step', ''))) > 30 else str(row.get('Failed Step', '')),
                            error_msg
                        ])
                    
                    failed_table = Table(failed_table_data, colWidths=[1.2*inch, 1.8*inch, 1.5*inch, 2*inch], repeatRows=1)
                    failed_table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#dc3545')),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, 0), 9),
                        ('FONTSIZE', (0, 1), (-1, -1), 7),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black),
                        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
                        ('VALIGN', (0, 0), (-1, -1), 'TOP')
                    ]))
                    
                    elements.append(failed_table)
                
                # Build PDF
                doc.build(elements)
                pdf_data = buffer.getvalue()
                buffer.close()
                
                return pdf_data
                
            except ImportError:
                return None
        
        pdf_data = generate_pdf_report(df, framework)
        if pdf_data:
            st.download_button(
                label="📄 Download PDF",
                data=pdf_data,
                file_name=f"{framework.lower()}_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf"
            )
        else:
            st.info("PDF export requires reportlab. Install with: pip install reportlab")

else:
    st.info("👆 Please upload a test report file to get started!")
    
    # Show sample data format
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

# Footer
st.markdown("---")
st.markdown("**Test Report Dashboard** | Built with Streamlit | 🚀 Enhanced Version")