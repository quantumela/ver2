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
    ]import streamlit as st
import sys
import os

def render_employee_data_management():
    """Render the Employee Data Management System with full feature preservation"""
    try:
        # Add the new_employee path to sys.path
        employee_path = os.path.join(os.getcwd(), 'new_employee')
        panels_path = os.path.join(employee_path, 'panels')
        
        # Add both paths to sys.path if they exist
        paths_to_add = [employee_path, panels_path]
        original_path = sys.path.copy()
        
        for path in paths_to_add:
            if os.path.exists(path) and path not in sys.path:
                sys.path.insert(0, path)
        
        # Save current working directory
        original_cwd = os.getcwd()
        
        try:
            # Change to employee directory if it exists
            if os.path.exists(employee_path):
                os.chdir(employee_path)
            
            # Import panel functions with better error handling
            try:
                from employee_main_panel import show_employee_panel
                from employee_statistics_panel import show_employee_statistics_panel  
                from employee_validation_panel import show_employee_validation_panel
                from employee_dashboard_panel import show_employee_dashboard_panel
                from employee_admin_panel import show_employee_admin_panel
            except ImportError:
                try:
                    from panels.employee_main_panel import show_employee_panel
                    from panels.employee_statistics_panel import show_employee_statistics_panel  
                    from panels.employee_validation_panel import show_employee_validation_panel
                    from panels.employee_dashboard_panel import show_employee_dashboard_panel
                    from panels.employee_admin_panel import show_employee_admin_panel
                except ImportError as e:
                    st.error(f"Failed to import employee panels: {str(e)}")
                    st.info("Please ensure all employee panel files exist in new_employee/panels/")
                    return
            
            # Initialize session state with admin_mode (exact from main_app.py)
            if 'state' not in st.session_state:
                st.session_state.state = {'admin_mode': False}
            
            # Ensure admin_mode key exists
            if 'admin_mode' not in st.session_state.state:
                st.session_state.state['admin_mode'] = False
            
            state = st.session_state.state
            
            # CSS for professional display
            st.markdown("""
                <style>
                    .stDataFrame { width: 100% !important; }
                    .stDataFrame div[data-testid="stHorizontalBlock"] { overflow-x: auto; }
                    .stDataFrame table { width: 100%; font-size: 14px; }
                    .stDataFrame th { font-weight: bold !important; background-color: #f0f2f6 !important; }
                    .stDataFrame td { white-space: nowrap; max-width: 300px; overflow: hidden; text-overflow: ellipsis; }
                    .css-1v0mbdj { max-width: 100%; }
                    .block-container { padding-top: 2rem; padding-bottom: 2rem; max-width: 1200px; }
                    .stButton>button { width: 100%; }
                    .stDownloadButton>button { width: 100%; }
                    .admin-section { background-color: #f8f9fa; padding: 1rem; border-radius: 0.5rem; border-left: 4px solid #ff4b4b; margin-bottom: 1rem; }
                </style>
            """, unsafe_allow_html=True)
            
            # Main title
            st.title("Employee Data Management System")
            
            # Sidebar navigation with radio buttons (exact from main_app.py)
            st.sidebar.title("Employee Data Management")
            st.sidebar.markdown("---")
            
            # Admin mode toggle with improved UX
            current_admin_mode = st.session_state.state.get('admin_mode', False)
            
            # Show checkbox as checked if already authenticated
            admin_enabled = st.checkbox("Admin Mode", 
                                      value=current_admin_mode, 
                                      help="Enable configuration options", 
                                      key="employee_admin_mode")
            
            if admin_enabled and not current_admin_mode:
                # User wants admin mode but not authenticated yet
                try:
                    # Try to get admin password from secrets
                    admin_password = None
                    try:
                        admin_password = st.secrets["admin_password"]
                    except (KeyError, FileNotFoundError):
                        try:
                            admin_password = st.secrets.get("admin_password", None)
                        except:
                            admin_password = None
                    
                    if admin_password and admin_password.strip():
                        entered_pw = st.text_input("Admin Password", type="password", key="employee_admin_password")
                        if entered_pw == admin_password:
                            st.session_state.state['admin_mode'] = True
                            st.success("Admin mode activated")
                            st.rerun()  # Refresh to update UI
                        elif entered_pw:
                            st.error("Incorrect password")
                            st.session_state.state['admin_mode'] = False
                    else:
                        st.error("Admin password not configured")
                        st.info("Please configure admin_password in Streamlit Cloud secrets")
                        st.session_state.state['admin_mode'] = False
                except Exception as e:
                    st.error(f"Error reading secrets: {str(e)}")
                    st.session_state.state['admin_mode'] = False
                    
            elif not admin_enabled:
                # User unchecked admin mode
                st.session_state.state['admin_mode'] = False
            elif admin_enabled and current_admin_mode:
                # Already authenticated
                st.success("Admin mode active")
                if st.button("Logout Admin", key="employee_admin_logout"):
                    st.session_state.state['admin_mode'] = False
                    st.rerun()
            
            # Update panel options based on admin mode
            if st.session_state.state['admin_mode']:
                panel_options = [
                    "Employee Processing",
                    "Statistics & Detective", 
                    "Data Validation",
                    "Dashboard",
                    "Admin Configuration"
                ]
            else:
                panel_options = [
                    "Employee Processing",
                    "Statistics & Detective", 
                    "Data Validation",
                    "Dashboard"
                ]
            
            panel = st.sidebar.radio(
                "**Choose Panel:**",
                panel_options,
                key="employee_panel_selection"
            )
            
            # Add quick stats in sidebar (exact from main_app.py)
            st.sidebar.markdown("---")
            st.sidebar.markdown("**Quick Status:**")
            
            # Check data status (exact logic from main_app.py)
            pa_files_loaded = sum(1 for file_key in ['PA0001', 'PA0002', 'PA0006', 'PA0105'] 
                                 if state.get(f'source_{file_key.lower()}') is not None)
            output_generated = 'generated_employee_files' in state and state['generated_employee_files']
            
            st.sidebar.write(f"PA Files: {pa_files_loaded}/4 loaded")
            st.sidebar.write(f"Output: {'Generated' if output_generated else 'Not yet'}")
            
            if pa_files_loaded >= 2:
                st.sidebar.success("Ready to process")
            else:
                st.sidebar.error("Need PA0001 & PA0002")
            
            st.sidebar.markdown("---")
            st.sidebar.markdown("**Quick Tips:**")
            st.sidebar.info("1. Upload PA files first\n2. Process employee data\n3. Validate results\n4. Analyze statistics")
            
            # Show admin status in sidebar ONLY if authenticated
            st.sidebar.markdown("---")
            if st.session_state.state.get('admin_mode', False):
                st.sidebar.markdown("**Admin Mode:** :red[ACTIVE]")
            # Don't show admin status if not authenticated
            
            # Show welcome message for first-time users
            if pa_files_loaded == 0:
                st.markdown("""
                ### Welcome to Employee Data Management!
                
                **Getting Started:**
                1. **Upload PA Files**: Go to Employee Processing to upload PA0001, PA0002, PA0006, PA0105
                2. **Process Data**: Transform employee data for target system
                3. **Validate Results**: Check data quality and completeness
                4. **Analyze Statistics**: Use Statistics & Detective for detailed analysis
                5. **Monitor Progress**: Track processing in the Dashboard
                
                **Supported PA Files:**
                - **PA0001**: Organizational Assignment
                - **PA0002**: Personal Data
                - **PA0006**: Address Information  
                - **PA0105**: Communication Data
                
                **Features:**
                - Employee data validation and quality checks
                - Statistics and detective analysis
                - Dashboard monitoring and reporting
                - Admin configuration options (password protected)
                """)
            
            # Show selected panel with performance optimization (exact from main_app.py)
            try:
                if panel == "Employee Processing":
                    show_employee_panel(state)
                elif panel == "Statistics & Detective":
                    # Add warning for large datasets (exact from main_app.py)
                    pa0002_data = state.get('source_pa0002')
                    if pa0002_data is not None and len(pa0002_data) > 10000:
                        st.warning("Large dataset detected. Statistics panel may take a moment to load...")
                    
                    with st.spinner("Loading statistics..."):
                        show_employee_statistics_panel(state)
                elif panel == "Data Validation":
                    with st.spinner("Running validation checks..."):
                        show_employee_validation_panel(state)
                elif panel == "Dashboard":
                    show_employee_dashboard_panel(state)
                elif panel == "Admin Configuration":
                    if st.session_state.state['admin_mode']:
                        st.markdown("<div class='admin-section'>", unsafe_allow_html=True)
                        st.header("Employee Admin Configuration Center")
                        show_employee_admin_panel()
                        st.markdown("</div>", unsafe_allow_html=True)
                    else:
                        st.error("Admin access required")
                        st.info("Please enable Admin Mode and enter the correct password to access this panel.")
            
            except Exception as e:
                # Exact error handling from main_app.py
                st.error(f"Panel Error: {str(e)}")
                st.info("**What to do:** Try refreshing the page or switching to a different panel")
                
                # Show error details in expander (exact from main_app.py)
                with st.expander("Technical Details", expanded=False):
                    st.code(str(e))
                    if st.button("Reset Session", key="reset_employee_session"):
                        for key in list(st.session_state.keys()):
                            del st.session_state[key]
                        st.rerun()
            
            # Footer (exact from main_app.py)
            st.sidebar.markdown("---")
            st.sidebar.caption("Employee Data Management System v2.0")
            
        finally:
            # Always restore original working directory and path
            os.chdir(original_cwd)
            sys.path = original_path
        
    except ImportError as e:
        st.error(f"Employee System Import Error: {str(e)}")
        st.info("**Troubleshooting:**")
        st.write("1. Ensure `new_employee/main_app.py` exists")
        st.write("2. Check that all employee panel files are in `new_employee/panels/`")
        st.write("3. Verify the employee system structure")
        st.write("4. Ensure required panel files exist:")
        
        required_panels = [
            "employee_main_panel.py",
            "employee_statistics_panel.py", 
            "employee_validation_panel.py",
            "employee_dashboard_panel.py",
            "employee_admin_panel.py"
        ]
        
        employee_path = os.path.join(os.getcwd(), 'new_employee')
        panels_path = os.path.join(employee_path, 'panels')
        
        for panel in required_panels:
            panel_path = os.path.join(panels_path, panel)
            if os.path.exists(panel_path):
                st.success(f"✅ {panel}")
            else:
                st.error(f"❌ {panel}")
        
        with st.expander("Technical Details"):
            st.code(f"Import Error: {str(e)}")
            st.write(f"**Looking for employee system at:** `{employee_path}`")
            st.write(f"**Looking for panels at:** `{panels_path}`")
    
    except Exception as e:
        st.error(f"Employee System Error: {str(e)}")
        st.info("Please check the employee system configuration and try again.")
        
        with st.expander("Technical Details"):
            st.code(f"Error Type: {type(e).__name__}\nError Message: {str(e)}")

def get_employee_system_status():
    """Get the status of the Employee Data Management System"""
    try:
        employee_path = os.path.join(os.getcwd(), 'new_employee')
        
        # Check if employee system exists
        if not os.path.exists(employee_path):
            return {
                'available': False,
                'status': 'Employee directory not found',
                'details': f'Path: {employee_path}'
            }
        
        main_app_path = os.path.join(employee_path, 'main_app.py')
        if not os.path.exists(main_app_path):
            return {
                'available': False,
                'status': 'main_app.py not found',
                'details': 'Employee system incomplete'
            }
        
        # Check required panels
        panels_path = os.path.join(employee_path, 'panels')
        required_panels = [
            "employee_main_panel.py",
            "employee_statistics_panel.py", 
            "employee_validation_panel.py",
            "employee_dashboard_panel.py",
            "employee_admin_panel.py"
        ]
        
        missing_panels = []
        for panel in required_panels:
            if not os.path.exists(os.path.join(panels_path, panel)):
                missing_panels.append(panel)
        
        if missing_panels:
            return {
                'available': False,
                'status': f'Missing panels: {", ".join(missing_panels)}',
                'details': {'missing_panels': missing_panels}
            }
        
        # Check session state for data status (uses 'state' like foundation)
        employee_state = getattr(st.session_state, 'state', {})
        
        pa_files_status = {}
        pa_files = ['PA0001', 'PA0002', 'PA0006', 'PA0105']  # Employee uses 4 PA files
        files_loaded = 0
        
        for pa_file in pa_files:
            key = f'source_{pa_file.lower()}'
            is_loaded = employee_state.get(key) is not None
            pa_files_status[pa_file] = is_loaded
            if is_loaded:
                files_loaded += 1
        
        output_generated = bool(employee_state.get('generated_employee_files', {}))
        
        status_details = {
            'pa_files_loaded': files_loaded,
            'total_pa_files': len(pa_files),
            'pa_files_status': pa_files_status,
            'output_generated': output_generated,
            'ready_to_process': files_loaded >= 2  # Need at least PA0001 & PA0002
        }
        
        if output_generated:
            status_msg = "Employee system ready - Output files generated"
        elif files_loaded >= 2:
            status_msg = f"Employee system ready - {files_loaded}/4 PA files loaded"
        elif files_loaded >= 1:
            status_msg = f"Employee system ready - {files_loaded}/4 PA files loaded"
        else:
            status_msg = "Employee system ready - Load PA files"
        
        return {
            'available': True,
            'status': status_msg,
            'details': status_details,
            'enhanced_features': [
                'PA Files Processing (PA0001 Org Assignment, PA0002 Personal Data, PA0006 Address, PA0105 Communication)',
                'Employee Data Validation & Quality Checks',
                'Statistics & Detective Analysis',
                'Dashboard & Monitoring',
                'Admin Configuration (Password Protected)'
            ]
        }
        
    except Exception as e:
        return {
            'available': False,
            'status': f'Employee system check failed: {str(e)}',
            'details': {'error': str(e)}
        }
