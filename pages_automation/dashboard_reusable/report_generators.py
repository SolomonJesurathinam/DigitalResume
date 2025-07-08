"""
Report Export Generators
"""

import json
import pandas as pd
from datetime import datetime
from io import BytesIO

def generate_csv_report(df):
    """Generate CSV report"""
    return df.to_csv(index=False).encode('utf-8')

def generate_json_report(df):
    """Generate JSON report"""
    return df.to_json(orient='records', indent=2).encode('utf-8')

def generate_html_report(df, framework):
    """Generate comprehensive HTML report with charts"""
    
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
    
    # Generate chart data - Fix the numpy/pandas conversion issue
    status_counts = df[status_col].value_counts()
    chart_labels = [str(label) for label in status_counts.index.tolist()]
    chart_values = [int(value) for value in status_counts.values.tolist()]
    
    # Color mapping
    color_map = {
        'passed': '#28a745',
        'failed': '#dc3545', 
        'skipped': '#ffc107',
        'pending': '#17a2b8'
    }
    chart_colors = [color_map.get(str(label), '#6c757d') for label in chart_labels]
    
    # Convert to JSON strings for JavaScript
    chart_labels_json = json.dumps(chart_labels)
    chart_values_json = json.dumps(chart_values)
    chart_colors_json = json.dumps(chart_colors)
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{framework} Test Report</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script src="https://cdn.jsdelivr.net/npm/chart.js@3.9.1/dist/chart.min.js"></script>
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
            // Global variables to track chart instances
            let pieChartInstance = null;
            let barChartInstance = null;
            let chartsInitialized = false;
            
            function createCharts() {{
                // Prevent multiple initialization
                if (chartsInitialized) {{
                    console.log('Charts already initialized, skipping...');
                    return;
                }}
                
                console.log('Creating charts...');
                console.log('Chart labels:', {chart_labels_json});
                console.log('Chart values:', {chart_values_json});
                console.log('Chart colors:', {chart_colors_json});
                
                // Check if Chart.js is loaded
                if (typeof Chart === 'undefined') {{
                    console.error('Chart.js not loaded');
                    document.getElementById('pieChart').innerHTML = '<p>Chart.js failed to load</p>';
                    document.getElementById('barChart').innerHTML = '<p>Chart.js failed to load</p>';
                    return;
                }}
                
                try {{
                    // Destroy existing charts if they exist
                    if (pieChartInstance) {{
                        pieChartInstance.destroy();
                        pieChartInstance = null;
                    }}
                    if (barChartInstance) {{
                        barChartInstance.destroy();
                        barChartInstance = null;
                    }}
                    
                    // Pie Chart
                    const pieCtx = document.getElementById('pieChart');
                    if (pieCtx) {{
                        pieChartInstance = new Chart(pieCtx, {{
                            type: 'pie',
                            data: {{
                                labels: {chart_labels_json},
                                datasets: [{{
                                    data: {chart_values_json},
                                    backgroundColor: {chart_colors_json},
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
                        console.log('Pie chart created successfully');
                    }}
                    
                    // Bar Chart
                    const barCtx = document.getElementById('barChart');
                    if (barCtx) {{
                        barChartInstance = new Chart(barCtx, {{
                            type: 'bar',
                            data: {{
                                labels: {chart_labels_json},
                                datasets: [{{
                                    label: 'Test Count',
                                    data: {chart_values_json},
                                    backgroundColor: {chart_colors_json},
                                    borderColor: {chart_colors_json},
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
                        console.log('Bar chart created successfully');
                    }}
                    
                    chartsInitialized = true;
                    console.log('All charts initialized successfully');
                    
                }} catch (error) {{
                    console.error('Error creating charts:', error);
                }}
            }}
            
            // Wait for DOM to load
            document.addEventListener('DOMContentLoaded', function() {{
                console.log('DOM loaded, initializing charts...');
                createCharts();
            }});
            
            // Fallback: Try to create charts after a delay (only if not already created)
            setTimeout(function() {{
                if (!chartsInitialized && typeof Chart !== 'undefined') {{
                    console.log('Chart.js loaded via timeout, creating charts...');
                    createCharts();
                }} else if (!chartsInitialized) {{
                    console.error('Chart.js still not loaded after timeout');
                    // Show fallback content with proper data
                    const statusSummary = {{}};
                    const labels = {chart_labels_json};
                    const values = {chart_values_json};
                    for (let i = 0; i < labels.length; i++) {{
                        statusSummary[labels[i]] = values[i];
                    }}
                    
                    document.querySelector('.charts-section').innerHTML = '<h2>📊 Visual Analytics</h2><div style="text-align: center; padding: 40px; background: #f8f9fa; border-radius: 10px;"><p><strong>Charts could not be loaded.</strong></p><p>Status Summary: ' + JSON.stringify(statusSummary) + '</p></div>';
                }}
            }}, 2000);
            
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
    
    return html_content.encode('utf-8')

def generate_pdf_report(df, framework):
    """Generate PDF report"""
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

def get_filename(framework, extension):
    """Generate timestamped filename"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    return f"{framework.lower()}_report_{timestamp}.{extension}"