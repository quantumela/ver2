# ====================================================================
# COPY THIS ENTIRE SECTION TO THE TOP OF EACH WRAPPER FILE
# ====================================================================

import streamlit as st

def apply_professional_mvs_theme():
    """Apply professional enterprise tool styling to MVS"""
    st.markdown("""
    <style>
        /* Hide Streamlit elements for clean tool appearance */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stDeployButton {visibility: hidden;}
        
        /* Professional app background */
        .stApp {
            background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%);
            font-family: 'Segoe UI', 'Arial', sans-serif;
        }
        
        /* Clean content workspace */
        .main .block-container {
            background: #ffffff;
            border-radius: 8px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.15);
            margin: 15px;
            padding: 30px;
            max-width: 100%;
        }
        
        /* Professional sidebar */
        .css-1d391kg {
            background: #1f2937;
            padding-top: 20px;
        }
        
        .css-1d391kg .css-1v0mbdj {
            background: #1f2937;
            color: #f9fafb;
        }
        
        /* Sidebar title styling */
        .css-1d391kg h1 {
            color: #ffffff !important;
            font-size: 18px !important;
            font-weight: 600 !important;
            border-bottom: 2px solid #4b5563 !important;
            padding-bottom: 10px !important;
            margin-bottom: 20px !important;
            border-radius: 0 !important;
        }
        
        /* Sidebar text */
        .css-1d391kg .css-1v0mbdj p {
            color: #d1d5db;
            font-size: 14px;
        }
        
        /* Professional navigation buttons */
        .css-1d391kg .stRadio > div {
            background: transparent;
        }
        
        .css-1d391kg .stRadio label {
            color: #e5e7eb !important;
            font-weight: 500 !important;
            padding: 12px 16px !important;
            border-radius: 6px !important;
            margin: 4px 0 !important;
            transition: all 0.2s ease !important;
            display: block !important;
            cursor: pointer !important;
        }
        
        .css-1d391kg .stRadio label:hover {
            background: #374151 !important;
            color: #ffffff !important;
        }
        
        .css-1d391kg .stRadio input:checked + label {
            background: #3b82f6 !important;
            color: #ffffff !important;
            font-weight: 600 !important;
        }
        
        /* Main headers */
        h1 {
            color: #1e40af !important;
            font-weight: 600 !important;
            font-size: 28px !important;
            margin-bottom: 8px !important;
            border-bottom: 3px solid #3b82f6 !important;
            padding-bottom: 12px !important;
        }
        
        h2 {
            color: #374151 !important;
            font-weight: 500 !important;
            font-size: 22px !important;
            margin-top: 25px !important;
            margin-bottom: 15px !important;
        }
        
        h3 {
            color: #4b5563 !important;
            font-weight: 500 !important;
            font-size: 18px !important;
            margin-bottom: 10px !important;
        }
        
        /* Professional status indicators */
        .stSuccess {
            background: #d1fae5 !important;
            border: 1px solid #10b981 !important;
            border-radius: 6px !important;
            padding: 12px 16px !important;
            color: #065f46 !important;
            font-weight: 500 !important;
        }
        
        .stError {
            background: #fee2e2 !important;
            border: 1px solid #ef4444 !important;
            border-radius: 6px !important;
            padding: 12px 16px !important;
            color: #991b1b !important;
            font-weight: 500 !important;
        }
        
        .stWarning {
            background: #fef3c7 !important;
            border: 1px solid #f59e0b !important;
            border-radius: 6px !important;
            padding: 12px 16px !important;
            color: #92400e !important;
            font-weight: 500 !important;
        }
        
        .stInfo {
            background: #dbeafe !important;
            border: 1px solid #3b82f6 !important;
            border-radius: 6px !important;
            padding: 12px 16px !important;
            color: #1e40af !important;
            font-weight: 500 !important;
        }
        
        /* Professional buttons */
        .stButton > button {
            background: linear-gradient(135deg, #3b82f6, #2563eb) !important;
            color: white !important;
            border: none !important;
            border-radius: 6px !important;
            padding: 10px 20px !important;
            font-weight: 500 !important;
            font-size: 14px !important;
            transition: all 0.2s ease !important;
            box-shadow: 0 2px 4px rgba(59, 130, 246, 0.2) !important;
        }
        
        .stButton > button:hover {
            background: linear-gradient(135deg, #2563eb, #1d4ed8) !important;
            box-shadow: 0 4px 8px rgba(59, 130, 246, 0.3) !important;
            transform: translateY(-1px) !important;
        }
        
        /* Download buttons */
        .stDownloadButton > button {
            background: linear-gradient(135deg, #059669, #047857) !important;
            color: white !important;
            border: none !important;
            border-radius: 6px !important;
            padding: 10px 20px !important;
            font-weight: 500 !important;
        }
        
        /* Professional data tables */
        .stDataFrame {
            border: 1px solid #e5e7eb !important;
            border-radius: 8px !important;
            overflow: hidden !important;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1) !important;
        }
        
        .stDataFrame th {
            background: #f8fafc !important;
            color: #374151 !important;
            font-weight: 600 !important;
            padding: 12px 10px !important;
            border-bottom: 2px solid #e2e8f0 !important;
            text-align: left !important;
        }
        
        .stDataFrame td {
            padding: 10px !important;
            border-bottom: 1px solid #f1f5f9 !important;
            color: #4b5563 !important;
        }
        
        .stDataFrame tr:hover {
            background: #f8fafc !important;
        }
        
        /* Professional input fields */
        .stTextInput > div > div > input {
            border: 1px solid #d1d5db !important;
            border-radius: 6px !important;
            padding: 10px 12px !important;
            font-size: 14px !important;
            transition: border-color 0.2s ease !important;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #3b82f6 !important;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
        }
        
        /* Select boxes */
        .stSelectbox > div > div {
            border: 1px solid #d1d5db !important;
            border-radius: 6px !important;
        }
        
        /* Checkboxes */
        .stCheckbox > label {
            color: #374151 !important;
            font-weight: 500 !important;
        }
        
        /* File uploader */
        .stFileUploader > div {
            border: 2px dashed #d1d5db !important;
            border-radius: 8px !important;
            padding: 20px !important;
            background: #f9fafb !important;
        }
        
        .stFileUploader > div:hover {
            border-color: #3b82f6 !important;
            background: #eff6ff !important;
        }
        
        /* Professional tabs */
        .stTabs > div > div > div {
            background: #f9fafb !important;
            border-radius: 8px 8px 0 0 !important;
        }
        
        .stTabs > div > div > div > button {
            background: transparent !important;
            color: #6b7280 !important;
            font-weight: 500 !important;
            padding: 12px 20px !important;
        }
        
        .stTabs > div > div > div > button[aria-selected="true"] {
            background: #ffffff !important;
            color: #1f2937 !important;
            border-bottom: 2px solid #3b82f6 !important;
        }
        
        /* Admin sections */
        .admin-section {
            background: linear-gradient(135deg, #fef2f2, #fee2e2) !important;
            border: 1px solid #fca5a5 !important;
            border-left: 4px solid #ef4444 !important;
            border-radius: 8px !important;
            padding: 20px !important;
            margin: 20px 0 !important;
        }
        
        .admin-section h2 {
            color: #991b1b !important;
            margin-top: 0 !important;
        }
        
        /* Professional expanders */
        .streamlit-expanderHeader {
            background: #f9fafb !important;
            border: 1px solid #e5e7eb !important;
            border-radius: 6px !important;
            padding: 12px 16px !important;
            font-weight: 500 !important;
            color: #374151 !important;
        }
        
        .streamlit-expanderContent {
            border: 1px solid #e5e7eb !important;
            border-top: none !important;
            border-radius: 0 0 6px 6px !important;
            padding: 16px !important;
            background: #ffffff !important;
        }
        
        /* Loading spinner */
        .stSpinner > div {
            border-color: #3b82f6 !important;
        }
        
        /* Metrics styling */
        .metric-card {
            background: #ffffff;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            text-align: center;
            margin: 10px 0;
        }
        
        .metric-value {
            font-size: 32px;
            font-weight: 700;
            color: #1f2937;
            margin-bottom: 5px;
        }
        
        .metric-label {
            font-size: 13px;
            color: #6b7280;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.8px;
        }
        
        /* Status badges */
        .status-ready { color: #10b981; }
        .status-pending { color: #f59e0b; }
        .status-error { color: #ef4444; }
        .status-processing { color: #3b82f6; }
        
    </style>
    """, unsafe_allow_html=True)

def create_mvs_header(title, subtitle=None):
    """Create professional MVS header"""
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #1e40af, #3b82f6);
        color: white;
        padding: 25px;
        border-radius: 8px;
        margin-bottom: 25px;
        box-shadow: 0 4px 12px rgba(30, 64, 175, 0.2);
    ">
        <h1 style="margin: 0; color: white; border: none; font-size: 26px; font-weight: 600;">
            {title}
        </h1>
        {f'<p style="margin: 8px 0 0 0; color: #e0e7ff; font-size: 15px;">{subtitle}</p>' if subtitle else ''}
    </div>
    """, unsafe_allow_html=True)

def create_mvs_metrics(metrics_data):
    """Create professional status metrics for MVS"""
    cols = st.columns(len(metrics_data))
    
    for i, (label, value, status, description) in enumerate(metrics_data):
        with cols[i]:
            color = {
                'success': '#10b981',
                'warning': '#f59e0b', 
                'error': '#ef4444',
                'info': '#3b82f6'
            }.get(status, '#6b7280')
            
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value" style="color: {color};">
                    {value}
                </div>
                <div class="metric-label">{label}</div>
                <div style="font-size: 12px; color: #6b7280; margin-top: 5px;">
                    {description}
                </div>
            </div>
            """, unsafe_allow_html=True)

# ====================================================================
# END OF COPY-PASTE SECTION
# ====================================================================


# ====================================================================
# USAGE EXAMPLE - ADD THIS TO YOUR WRAPPER FUNCTIONS
# ====================================================================

def render_foundation_data_management():
    """Example of how to use the professional theme"""
    
    # STEP 1: Apply theme (FIRST LINE)
    apply_professional_mvs_theme()
    
    # STEP 2: Create professional header
    create_mvs_header(
        "Foundation Data Management", 
        "Organizational Hierarchy Processing & Validation"
    )
    
    # STEP 3: Create status metrics
    metrics_data = [
        ("HRP1000", "✓", "success", "25,430 records"),
        ("HRP1001", "✓", "success", "12,850 records"), 
        ("Hierarchy", "8", "info", "8 levels processed"),
        ("Output", "24", "success", "Files generated")
    ]
    create_mvs_metrics(metrics_data)
    
    # STEP 4: Your existing code continues normally...
    with st.sidebar:
        st.title("Foundation Data")
        # ... rest of sidebar code
    
    # ... rest of your existing wrapper code


# ====================================================================
# QUICK IMPLEMENTATION FOR ALL THREE SYSTEMS
# ====================================================================

# For Foundation System:
def foundation_metrics(state):
    hrp1000_loaded = 'source_hrp1000' in state and state['source_hrp1000'] is not None
    hrp1001_loaded = 'source_hrp1001' in state and state['source_hrp1001'] is not None
    hierarchy_processed = 'hierarchy_structure' in state and state['hierarchy_structure'] is not None
    output_generated = bool(state.get('generated_output_files', {}))
    
    return [
        ("HRP1000", "✓" if hrp1000_loaded else "✗", "success" if hrp1000_loaded else "error", 
         f"{len(state['source_hrp1000']):,} records" if hrp1000_loaded else "Not loaded"),
        ("HRP1001", "✓" if hrp1001_loaded else "✗", "success" if hrp1001_loaded else "error",
         f"{len(state['source_hrp1001']):,} records" if hrp1001_loaded else "Not loaded"),
        ("Hierarchy", str(max([info.get('level', 1) for info in state.get('hierarchy_structure', {}).values()]) if hierarchy_processed else 0), 
         "success" if hierarchy_processed else "warning", "Levels processed" if hierarchy_processed else "Pending"),
        ("Output", str(len(state.get('generated_output_files', {}).get('level_files', {})) + len(state.get('generated_output_files', {}).get('association_files', {}))),
         "success" if output_generated else "warning", "Files generated" if output_generated else "Not generated")
    ]

# For Employee System:
def employee_metrics(state):
    pa_files = ['PA0001', 'PA0002', 'PA0006', 'PA0105']
    files_loaded = sum(1 for file_key in pa_files if state.get(f'source_{file_key.lower()}') is not None)
    output_generated = bool(state.get('generated_employee_files', {}))
    
    return [
        ("PA Files", f"{files_loaded}/4", "success" if files_loaded >= 2 else "warning", "Employee data files"),
        ("Processing", "Ready" if files_loaded >= 2 else "Pending", "success" if files_loaded >= 2 else "error", "System status"),
        ("Output", "Generated" if output_generated else "Pending", "success" if output_generated else "warning", "Employee files"),
        ("Quality", "Validated" if files_loaded >= 2 else "Pending", "info" if files_loaded >= 2 else "warning", "Data validation")
    ]

# For Payroll System:
def payroll_metrics(payroll_state):
    pa_files = ['PA0008', 'PA0014']
    files_loaded = sum(1 for file_key in pa_files if payroll_state.get(f'source_{file_key.lower()}') is not None)
    output_generated = bool(payroll_state.get('generated_payroll_files', {}))
    
    return [
        ("PA Files", f"{files_loaded}/2", "success" if files_loaded >= 2 else "warning", "Payroll data files"),
        ("Processing", "Ready" if files_loaded >= 2 else "Pending", "success" if files_loaded >= 2 else "error", "System status"), 
        ("Output", "Generated" if output_generated else "Pending", "success" if output_generated else "warning", "Payroll files"),
        ("Wage Types", "Mapped" if files_loaded >= 2 else "Pending", "info" if files_loaded >= 2 else "warning", "Type validation")
    ]
    import streamlit as st
import sys
import os
import pandas as pd
from datetime import datetime

# Import the professional theme (add this to the top of each wrapper)
def apply_professional_theme():
    """Apply professional enterprise tool styling"""
    st.markdown("""
    <style>
        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Professional app background */
        .stApp {
            background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%);
            font-family: 'Segoe UI', 'Arial', sans-serif;
        }
        
        /* Clean content area */
        .main .block-container {
            background: #ffffff;
            border-radius: 8px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            margin: 10px;
            padding: 25px;
            max-width: 100%;
        }
        
        /* Professional sidebar */
        .css-1d391kg {
            background: #1f2937;
            padding-top: 20px;
        }
        
        .css-1d391kg .css-1v0mbdj {
            background: #1f2937;
            color: #f9fafb;
        }
        
        /* Sidebar title */
        .css-1d391kg h1 {
            color: #ffffff;
            font-size: 18px;
            font-weight: 600;
            border-bottom: 2px solid #4b5563;
            padding-bottom: 10px;
            margin-bottom: 20px;
            border-radius: 0;
        }
        
        /* Sidebar navigation */
        .css-1d391kg .stRadio label {
            color: #e5e7eb !important;
            font-weight: 500;
            padding: 10px 15px;
            border-radius: 6px;
            margin: 3px 0;
            transition: all 0.2s ease;
            display: block;
        }
        
        .css-1d391kg .stRadio label:hover {
            background: #374151;
            color: #ffffff !important;
        }
        
        .css-1d391kg .stRadio input:checked + label {
            background: #3b82f6 !important;
            color: #ffffff !important;
            font-weight: 600;
        }
        
        /* Professional headers */
        h1 {
            color: #1e40af;
            font-weight: 600;
            font-size: 28px;
            margin-bottom: 8px;
            border-bottom: 3px solid #3b82f6;
            padding-bottom: 12px;
        }
        
        /* Status indicators */
        .stSuccess {
            background: #d1fae5;
            border: 1px solid #10b981;
            border-radius: 6px;
            padding: 10px 15px;
            color: #065f46;
            font-weight: 500;
        }
        
        .stError {
            background: #fee2e2;
            border: 1px solid #ef4444;
            border-radius: 6px;
            padding: 10px 15px;
            color: #991b1b;
            font-weight: 500;
        }
        
        .stWarning {
            background: #fef3c7;
            border: 1px solid #f59e0b;
            border-radius: 6px;
            padding: 10px 15px;
            color: #92400e;
            font-weight: 500;
        }
        
        /* Professional buttons */
        .stButton > button {
            background: linear-gradient(135deg, #3b82f6, #2563eb);
            color: white;
            border: none;
            border-radius: 6px;
            padding: 10px 20px;
            font-weight: 500;
            font-size: 14px;
            transition: all 0.2s ease;
            box-shadow: 0 2px 4px rgba(59, 130, 246, 0.2);
        }
        
        .stButton > button:hover {
            background: linear-gradient(135deg, #2563eb, #1d4ed8);
            box-shadow: 0 4px 8px rgba(59, 130, 246, 0.3);
            transform: translateY(-1px);
        }
        
        /* Professional data tables */
        .stDataFrame {
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        
        .stDataFrame th {
            background: #f8fafc !important;
            color: #374151 !important;
            font-weight: 600 !important;
            padding: 12px 10px !important;
            border-bottom: 2px solid #e2e8f0 !important;
        }
        
        .stDataFrame td {
            padding: 10px !important;
            border-bottom: 1px solid #f1f5f9 !important;
            color: #4b5563;
        }
        
        .stDataFrame tr:hover {
            background: #f8fafc !important;
        }
        
        /* Input fields */
        .stTextInput > div > div > input {
            border: 1px solid #d1d5db;
            border-radius: 6px;
            padding: 10px 12px;
            font-size: 14px;
            transition: border-color 0.2s ease;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #3b82f6;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        }
        
        /* Admin sections */
        .admin-section {
            background: linear-gradient(135deg, #fef2f2, #fee2e2);
            border: 1px solid #fca5a5;
            border-left: 4px solid #ef4444;
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
        }
        
        /* Professional metrics */
        .metric-card {
            background: #ffffff;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            text-align: center;
            margin: 10px 0;
        }
        
        .metric-value {
            font-size: 32px;
            font-weight: 700;
            color: #1f2937;
            margin-bottom: 5px;
        }
        
        .metric-label {
            font-size: 13px;
            color: #6b7280;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.8px;
        }
    </style>
    """, unsafe_allow_html=True)

def create_professional_header(title, subtitle=None):
    """Create professional tool header"""
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #1e40af, #3b82f6);
        color: white;
        padding: 25px;
        border-radius: 8px;
        margin-bottom: 25px;
        box-shadow: 0 4px 12px rgba(30, 64, 175, 0.2);
    ">
        <h1 style="margin: 0; color: white; border: none; font-size: 26px; font-weight: 600;">
            {title}
        </h1>
        {f'<p style="margin: 8px 0 0 0; color: #e0e7ff; font-size: 15px;">{subtitle}</p>' if subtitle else ''}
    </div>
    """, unsafe_allow_html=True)

def create_status_metrics(data_status):
    """Create professional status metrics"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color: {'#10b981' if data_status['hrp1000'] else '#ef4444'};">
                {'✓' if data_status['hrp1000'] else '✗'}
            </div>
            <div class="metric-label">HRP1000</div>
            <div style="font-size: 12px; color: #6b7280; margin-top: 5px;">
                {f"{data_status.get('hrp1000_count', 0):,} records" if data_status['hrp1000'] else "Not loaded"}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color: {'#10b981' if data_status['hrp1001'] else '#ef4444'};">
                {'✓' if data_status['hrp1001'] else '✗'}
            </div>
            <div class="metric-label">HRP1001</div>
            <div style="font-size: 12px; color: #6b7280; margin-top: 5px;">
                {f"{data_status.get('hrp1001_count', 0):,} records" if data_status['hrp1001'] else "Not loaded"}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color: {'#10b981' if data_status['hierarchy'] else '#f59e0b'};">
                {data_status.get('max_level', 0)}
            </div>
            <div class="metric-label">Hierarchy Levels</div>
            <div style="font-size: 12px; color: #6b7280; margin-top: 5px;">
                {'Processed' if data_status['hierarchy'] else 'Pending'}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color: {'#10b981' if data_status['output'] else '#6b7280'};">
                {data_status.get('total_files', 0)}
            </div>
            <div class="metric-label">Output Files</div>
            <div style="font-size: 12px; color: #6b7280; margin-top: 5px;">
                {'Generated' if data_status['output'] else 'Not generated'}
            </div>
        </div>
        """, unsafe_allow_html=True)

def render_foundation_data_management():
    """Render Foundation Data Management with professional theme"""
    
    # Apply professional theme first
    apply_professional_theme()
    
    try:
        # Path and import logic (same as before)
        foundation_path = os.path.join(os.getcwd(), 'new_foundation')
        panels_path = os.path.join(foundation_path, 'panels')
        
        paths_to_add = [foundation_path, panels_path]
        original_path = sys.path.copy()
        
        for path in paths_to_add:
            if os.path.exists(path) and path not in sys.path:
                sys.path.insert(0, path)
        
        original_cwd = os.getcwd()
        
        try:
            if os.path.exists(foundation_path):
                os.chdir(foundation_path)
            
            # Import panels (same as before)
            try:
                from hierarchy_panel_fixed import show_hierarchy_panel
            except ImportError:
                try:
                    from panels.hierarchy_panel_fixed import show_hierarchy_panel
                except ImportError:
                    def show_hierarchy_panel(state):
                        st.error("Hierarchy panel not found")
            
            # Initialize session state (same as before)
            if 'state' not in st.session_state:
                st.session_state.state = {
                    'hrp1000': None, 'hrp1001': None, 'hierarchy': None,
                    'admin_mode': False, 'generated_output_files': {}
                }
            
            # Professional header
            create_professional_header(
                "Foundation Data Management", 
                "Organizational Hierarchy Processing & Validation"
            )
            
            # Check data status for metrics
            hrp1000_loaded = 'source_hrp1000' in st.session_state.state and st.session_state.state['source_hrp1000'] is not None
            hrp1001_loaded = 'source_hrp1001' in st.session_state.state and st.session_state.state['source_hrp1001'] is not None
            hierarchy_processed = 'hierarchy_structure' in st.session_state.state and st.session_state.state['hierarchy_structure'] is not None
            output_generated = bool(st.session_state.state.get('generated_output_files', {}))
            
            # Create data status object
            data_status = {
                'hrp1000': hrp1000_loaded,
                'hrp1001': hrp1001_loaded,
                'hierarchy': hierarchy_processed,
                'output': output_generated,
                'hrp1000_count': len(st.session_state.state['source_hrp1000']) if hrp1000_loaded else 0,
                'hrp1001_count': len(st.session_state.state['source_hrp1001']) if hrp1001_loaded else 0,
                'max_level': max([info.get('level', 1) for info in st.session_state.state.get('hierarchy_structure', {}).values()]) if hierarchy_processed else 0,
                'total_files': len(st.session_state.state.get('generated_output_files', {}).get('level_files', {})) + len(st.session_state.state.get('generated_output_files', {}).get('association_files', {}))
            }
            
            # Show professional status metrics
            create_status_metrics(data_status)
            
            # Professional sidebar navigation
            with st.sidebar:
                st.title("Foundation Data")
                
                # Admin mode toggle with professional styling
                current_admin_mode = st.session_state.state.get('admin_mode', False)
                admin_enabled = st.checkbox("Admin Mode", value=current_admin_mode, key="foundation_admin_mode")
                
                if admin_enabled and not current_admin_mode:
                    try:
                        admin_password = st.secrets.get("admin_password", None)
                        if admin_password:
                            entered_pw = st.text_input("Admin Password", type="password", key="foundation_admin_password")
                            if entered_pw == admin_password:
                                st.session_state.state['admin_mode'] = True
                                st.success("Admin mode activated")
                                st.rerun()
                            elif entered_pw:
                                st.error("Incorrect password")
                        else:
                            st.error("Admin password not configured")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
                elif not admin_enabled:
                    st.session_state.state['admin_mode'] = False
                elif admin_enabled and current_admin_mode:
                    st.success("Admin mode active")
                    if st.button("Logout Admin", key="foundation_admin_logout"):
                        st.session_state.state['admin_mode'] = False
                        st.rerun()
                
                st.markdown("---")
                
                # Navigation options
                if st.session_state.state.get('admin_mode', False):
                    panel_options = ["Admin", "Hierarchy", "Validation", "Statistics", "Health Monitor"]
                else:
                    panel_options = ["Hierarchy", "Validation", "Statistics", "Health Monitor"]
                
                panel = st.radio("Navigation", panel_options, key="foundation_panel_selection")
                
                # Professional status sidebar
                st.markdown("---")
                if st.session_state.state.get('admin_mode', False):
                    st.markdown("**Admin Mode:** :red[ACTIVE]")
                
                st.markdown("**System Status:**")
                if hrp1000_loaded:
                    st.markdown("🟢 HRP1000 Ready")
                else:
                    st.markdown("🔴 HRP1000 Missing")
                    
                if hrp1001_loaded:
                    st.markdown("🟢 HRP1001 Ready")
                else:
                    st.markdown("🔴 HRP1001 Missing")
                
                if output_generated:
                    st.markdown("🟢 Output Generated")
                else:
                    st.markdown("🟡 Output Pending")
            
            # Show welcome or panel content
            if not hrp1000_loaded and not hrp1001_loaded:
                st.markdown("""
                ## Getting Started with Foundation Data Management
                
                **Professional HR Data Processing Pipeline**
                
                ### Quick Start Guide:
                1. **📁 Upload Data** - Load HRP1000 and HRP1001 files
                2. **⚙️ Process Hierarchy** - Build organizational structure  
                3. **✅ Validate Quality** - Comprehensive data validation
                4. **📊 Generate Analytics** - End-to-end pipeline analysis
                5. **🏥 Monitor Health** - System performance tracking
                
                ### Enterprise Features:
                - **Advanced Validation Engine** - Complete pipeline validation
                - **Real-time Analytics** - Source-to-target analysis  
                - **Data Lineage Tracking** - Column-level transformations
                - **Quality Metrics** - Before/after analysis
                - **Health Monitoring** - System performance insights
                """)
            
            # Panel routing (same logic as before but with professional styling)
            try:
                if panel == "Admin" and st.session_state.state.get('admin_mode', False):
                    st.markdown("<div class='admin-section'>", unsafe_allow_html=True)
                    st.header("🔧 Admin Configuration Center")
                    st.info("Administrative functions for system configuration and management.")
                    # show_admin_panel() # Your existing admin panel function
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                elif panel == "Hierarchy":
                    st.markdown("### 📊 Hierarchy Processing")
                    show_hierarchy_panel(st.session_state.state)
                    
                elif panel == "Validation":
                    st.markdown("### ✅ Data Validation")
                    st.info("Comprehensive data quality validation and analysis.")
                    # show_validation_panel(st.session_state.state)
                    
                elif panel == "Statistics":
                    st.markdown("### 📈 Statistics & Analytics")
                    st.info("End-to-end pipeline analysis and reporting.")
                    # show_statistics_panel(st.session_state.state)
                    
                elif panel == "Health Monitor":
                    st.markdown("### 🏥 System Health Monitor")
                    st.info("System performance monitoring and diagnostics.")
                    # show_health_monitor_panel(st.session_state.state)
                    
            except Exception as e:
                st.error(f"Panel Error: {str(e)}")
                with st.expander("Technical Details"):
                    st.code(str(e))
            
        finally:
            os.chdir(original_cwd)
            sys.path = original_path
        
    except Exception as e:
        st.error(f"Foundation System Error: {str(e)}")

# Status function remains the same
def get_foundation_system_status():
    # ... same as before ...
