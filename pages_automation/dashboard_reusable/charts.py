"""
Chart and Visualization Components
"""

import streamlit as st
import plotly.express as px
import pandas as pd

def render_charts(df, config, framework):
    """Render charts section"""
    
    st.subheader("📈 Visual Analytics")
    
    if df.empty:
        st.warning("No data available for charts")
        return
    
    # Get status column
    if framework in ["Cucumber", "Allure"]:
        status_col = "Status"
    else:
        status_col = "Outcome"
    
    # Create tabs for different charts
    tab1, tab2, tab3 = st.tabs(["Status Distribution", "Duration Analysis", "Feature Analysis"])
    
    with tab1:
        render_status_charts(df, status_col)
    
    with tab2:
        if config["show_duration_analysis"]:
            render_duration_charts(df, status_col)
    
    with tab3:
        if framework == "Cucumber":
            render_feature_charts(df)

def render_status_charts(df, status_col):
    """Render status distribution charts"""
    
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

def render_duration_charts(df, status_col):
    """Render duration analysis charts"""
    
    if "Duration (s)" not in df.columns:
        st.info("Duration data not available")
        return
    
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

def render_feature_charts(df):
    """Render feature analysis charts for Cucumber"""
    
    if "Feature" not in df.columns:
        st.info("Feature data not available")
        return
    
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

def render_tag_analysis(df):
    """Render tag analysis for Cucumber"""
    
    st.subheader("🏷️ Tag Analysis")
    
    if "Tags" not in df.columns:
        st.info("Tags data not available")
        return
    
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
    else:
        st.info("No tags found in the data")

def render_failed_analysis(df, framework):
    """Render failed tests analysis"""
    
    status_col = "Status" if framework == "Cucumber" else "Outcome"
    failed_df = df[df[status_col] == "failed"]
    
    if failed_df.empty:
        return
    
    st.subheader("❌ Failed Tests Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if framework == "Cucumber" and "Feature" in failed_df.columns:
            st.write("**Failed Tests by Feature**")
            failed_by_feature = failed_df["Feature"].value_counts()
            st.bar_chart(failed_by_feature)
        else:
            st.info("Feature breakdown not available")
    
    with col2:
        if framework == "Cucumber" and "Failed Step" in failed_df.columns:
            st.write("**Common Failed Steps**")
            failed_steps = failed_df["Failed Step"].value_counts().head(5)
            st.write(failed_steps)
        else:
            st.info("Failed step analysis not available")