"""
Metrics and Summary Display Components
"""

import streamlit as st

def get_status_column(framework):
    """Get the appropriate status column name for the framework"""
    if framework in ["Cucumber", "Allure"]:
        return "Status"
    else:  # Pytest
        return "Outcome"

def calculate_metrics(df, framework):
    """Calculate test metrics"""
    if df.empty:
        return {}
    
    status_col = get_status_column(framework)
    
    total_tests = len(df)
    passed_tests = len(df[df[status_col] == "passed"])
    failed_tests = len(df[df[status_col] == "failed"])
    skipped_tests = len(df[df[status_col] == "skipped"])
    pending_tests = len(df[df[status_col] == "pending"]) if "pending" in df[status_col].values else 0
    pass_rate = (passed_tests/total_tests*100) if total_tests > 0 else 0
    
    return {
        "total_tests": total_tests,
        "passed_tests": passed_tests,
        "failed_tests": failed_tests,
        "skipped_tests": skipped_tests,
        "pending_tests": pending_tests,
        "pass_rate": pass_rate,
        "status_col": status_col
    }

def render_summary_metrics(df, framework):
    """Render summary metrics section"""
    
    st.subheader("📊 Summary Metrics")
    
    metrics = calculate_metrics(df, framework)
    
    if not metrics:
        st.warning("No metrics to display")
        return metrics
    
    # Display metrics in columns
    if metrics["pending_tests"] > 0:
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        with col6:
            st.metric("Pending", metrics["pending_tests"], 
                     delta=f"{(metrics['pending_tests']/metrics['total_tests']*100):.1f}%")
    else:
        col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Total Tests", metrics["total_tests"])
    with col2:
        st.metric("Passed", metrics["passed_tests"], 
                 delta=f"{(metrics['passed_tests']/metrics['total_tests']*100):.1f}%")
    with col3:
        st.metric("Failed", metrics["failed_tests"], 
                 delta=f"{(metrics['failed_tests']/metrics['total_tests']*100):.1f}%")
    with col4:
        st.metric("Skipped", metrics["skipped_tests"], 
                 delta=f"{(metrics['skipped_tests']/metrics['total_tests']*100):.1f}%")
    with col5:
        st.metric("Pass Rate", f"{metrics['pass_rate']:.1f}%")
    
    return metrics

def apply_filters(df, config, framework):
    """Apply filters to the dataframe"""
    if df.empty:
        return df
    
    if config["show_failed_only"]:
        status_col = get_status_column(framework)
        df = df[df[status_col] == "failed"]
    
    return df

def style_dataframe(df, status_col):
    """Apply styling to dataframe"""
    def highlight_status(val):
        if val == "passed":
            return "background-color: #d4edda; color: #155724"
        elif val == "failed":
            return "background-color: #f8d7da; color: #721c24"
        elif val == "skipped":
            return "background-color: #fff3cd; color: #856404"
        else:
            return ""
    
    return df.style.map(highlight_status, subset=[status_col])