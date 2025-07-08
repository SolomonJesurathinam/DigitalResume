"""
Test Report Parsers for different frameworks
"""

import pandas as pd
import json
import streamlit as st

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

def get_parser_by_framework(framework):
    """Get appropriate parser function based on framework"""
    parsers = {
        "Cucumber": parse_cucumber_json,
        "Allure": parse_allure_json,
        "Pytest": parse_pytest_json
    }
    return parsers.get(framework)