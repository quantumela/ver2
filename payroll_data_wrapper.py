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

def render_payroll_data_management():
    """Render the Payroll Data Management System with full feature preservation"""
    try:
        # Add the new_payroll path to sys.path
        payroll_path = os.path.join(os.getcwd(), 'new_payroll')
        panels_path = os.path.join(payroll_path, 'payroll_panels')  # Note: different folder name
        
        # Add both paths to sys.path if they exist
        paths_to_add = [payroll_path, panels_path]
        original_path = sys.path.copy()
        
        for path in paths_to_add:
            if os.path.exists(path) and path not in sys.path:
                sys.path.insert(0, path)
        
        # Save current working directory
        original_cwd = os.getcwd()
        
        try:
            # Change to payroll directory if it exists
            if os.path.exists(payroll_path):
                os.chdir(payroll_path)
            
            # Import the payroll panel functions with better error handling
            try:
                from payroll_main_panel import show_payroll_panel
                from payroll_statistics_panel import show_payroll_statistics_panel  
                from payroll_validation_panel import show_payroll_validation_panel
                from payroll_dashboard_panel import show_payroll_dashboard_panel
                from payroll_admin_panel import show_payroll_admin_panel
            except ImportError:
                try:
                    from payroll_panels.payroll_main_panel import show_payroll_panel
                    from payroll_panels.payroll_statistics_panel import show_payroll_statistics_panel  
                    from payroll_panels.payroll_validation_panel import show_payroll_validation_panel
                    from payroll_panels.payroll_dashboard_panel import show_payroll_dashboard_panel
                    from payroll_panels.payroll_admin_panel import show_payroll_admin_panel
                except ImportError as e:
                    st.error(f"Failed to import payroll panels: {str(e)}")
                    st.info("Please ensure all payroll panel files exist in new_payroll/payroll_panels/")
                    return
            
            # Initialize session state for payroll system with admin_mode (exact from app.py)
            if 'payroll_state' not in st.session_state:
                st.session_state.payroll_state = {'admin_mode': False}
            
            # Ensure admin_mode key exists
            if 'admin_mode' not in st.session_state.payroll_state:
                st.session_state.payroll_state['admin_mode'] = False
            
            payroll_state = st.session_state.payroll_state
            
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
            st.title("Payroll Data Management System")
            
            # Sidebar navigation with radio buttons (exact from app.py)
            st.sidebar.title("Payroll Data Management")
            st.sidebar.markdown("---")
            
            # Admin mode toggle with improved UX
            current_admin_mode = st.session_state.payroll_state.get('admin_mode', False)
            
            # Show checkbox as checked if already authenticated
            admin_enabled = st.checkbox("Admin Mode", 
                                      value=current_admin_mode, 
                                      help="Enable configuration options", 
                                      key="payroll_admin_mode")
            
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
                        entered_pw = st.text_input("Admin Password", type="password", key="payroll_admin_password")
                        if entered_pw == admin_password:
                            st.session_state.payroll_state['admin_mode'] = True
                            st.success("Admin mode activated")
                            st.rerun()  # Refresh to update UI
                        elif entered_pw:
                            st.error("Incorrect password")
                            st.session_state.payroll_state['admin_mode'] = False
                    else:
                        st.error("Admin password not configured")
                        st.info("Please configure admin_password in Streamlit Cloud secrets")
                        st.session_state.payroll_state['admin_mode'] = False
                except Exception as e:
                    st.error(f"Error reading secrets: {str(e)}")
                    st.session_state.payroll_state['admin_mode'] = False
                    
            elif not admin_enabled:
                # User unchecked admin mode
                st.session_state.payroll_state['admin_mode'] = False
            elif admin_enabled and current_admin_mode:
                # Already authenticated
                st.success("Admin mode active")
                if st.button("Logout Admin", key="payroll_admin_logout"):
                    st.session_state.payroll_state['admin_mode'] = False
                    st.rerun()
            
            # Update panel options based on admin mode
            if st.session_state.payroll_state['admin_mode']:
                panel_options = [
                    "Payroll Processing",
                    "Statistics & Analytics", 
                    "Data Validation",
                    "Dashboard",
                    "Admin Configuration"
                ]
            else:
                panel_options = [
                    "Payroll Processing",
                    "Statistics & Analytics", 
                    "Data Validation",
                    "Dashboard"
                ]
            
            panel = st.sidebar.radio(
                "**Choose Panel:**",
                panel_options,
                key="payroll_panel_selection"
            )
            
            # Add quick stats in sidebar (exact from app.py)
            st.sidebar.markdown("---")
            st.sidebar.markdown("**Quick Status:**")
            
            # Check data status (exact logic from app.py)
            pa_files_loaded = sum(1 for file_key in ['PA0008', 'PA0014'] 
                                 if payroll_state.get(f'source_{file_key.lower()}') is not None)
            output_generated = 'generated_payroll_files' in payroll_state and payroll_state['generated_payroll_files']
            
            st.sidebar.write(f"PA Files: {pa_files_loaded}/2 loaded")
            st.sidebar.write(f"Output: {'Generated' if output_generated else 'Not yet'}")
            
            if pa_files_loaded >= 2:
                st.sidebar.success("Ready to process")
            else:
                st.sidebar.error("Need PA0008 & PA0014")
            
            st.sidebar.markdown("---")
            st.sidebar.markdown("**Quick Tips:**")
            st.sidebar.info("1. Upload PA0008 & PA0014 files\n2. Process payroll data\n3. Validate results\n4. Analyze wage types")
            
            # Show admin status in sidebar ONLY if authenticated
            st.sidebar.markdown("---")
            if st.session_state.payroll_state.get('admin_mode', False):
                st.sidebar.markdown("**Admin Mode:** :red[ACTIVE]")
            # Don't show admin status if not authenticated
            
            # Show welcome message for first-time users
            if pa_files_loaded == 0:
                st.markdown("""
                ### Welcome to Payroll Data Management!
                
                **Getting Started:**
                1. **Upload PA Files**: Go to Payroll Processing to upload PA0008 and PA0014
                2. **Process Data**: Transform payroll data for target system
                3. **Validate Results**: Check data quality and wage type mappings
                4. **Analyze Statistics**: Review payroll analytics and trends
                5. **Monitor Progress**: Track processing in the Dashboard
                
                **Supported PA Files:**
                - **PA0008**: Basic Pay Information
                - **PA0014**: Recurring Payments/Deductions
                
                **Features:**
                - Wage type mapping and validation
                - Payroll statistics and analytics
                - Dashboard monitoring and reporting
                - Admin configuration for wage types (password protected)
                """)
            
            # Show selected panel with performance optimization (exact from app.py)
            try:
                if panel == "Payroll Processing":
                    show_payroll_panel(payroll_state)
                elif panel == "Statistics & Analytics":
                    # Add warning for large datasets (exact from app.py)
                    pa0008_data = payroll_state.get('source_pa0008')
                    if pa0008_data is not None and len(pa0008_data) > 10000:
                        st.warning("Large dataset detected. Statistics panel may take a moment to load...")
                    
                    with st.spinner("Loading payroll statistics..."):
                        show_payroll_statistics_panel(payroll_state)
                elif panel == "Data Validation":
                    with st.spinner("Running validation checks..."):
                        show_payroll_validation_panel(payroll_state)
                elif panel == "Dashboard":
                    show_payroll_dashboard_panel(payroll_state)
                elif panel == "Admin Configuration":
                    if st.session_state.payroll_state['admin_mode']:
                        st.markdown("<div class='admin-section'>", unsafe_allow_html=True)
                        st.header("Payroll Admin Configuration Center")
                        show_payroll_admin_panel()
                        st.markdown("</div>", unsafe_allow_html=True)
                    else:
                        st.error("Admin access required")
                        st.info("Please enable Admin Mode and enter the correct password to access this panel.")
            
            except Exception as e:
                # Exact error handling from app.py
                st.error(f"Panel Error: {str(e)}")
                st.info("**What to do:** Try refreshing the page or switching to a different panel")
                
                # Show error details in expander (exact from app.py)
                with st.expander("Technical Details", expanded=False):
                    st.code(str(e))
                    if st.button("Reset Session", key="reset_payroll_session"):
                        for key in list(st.session_state.keys()):
                            if key.startswith('payroll'):
                                del st.session_state[key]
                        st.rerun()
            
            # Footer (exact from app.py)
            st.sidebar.markdown("---")
            st.sidebar.caption("Payroll Data Management System v1.0")
            
        finally:
            # Always restore original working directory and path
            os.chdir(original_cwd)
            sys.path = original_path
        
    except ImportError as e:
        st.error(f"Payroll System Import Error: {str(e)}")
        st.info("**Troubleshooting:**")
        st.write("1. Ensure `new_payroll/app.py` exists")
        st.write("2. Check that all payroll panel files are in `new_payroll/payroll_panels/`")
        st.write("3. Verify the payroll system structure")
        st.write("4. Ensure required panel files exist:")
        
        required_panels = [
            "payroll_main_panel.py",
            "payroll_statistics_panel.py", 
            "payroll_validation_panel.py",
            "payroll_dashboard_panel.py",
            "payroll_admin_panel.py"
        ]
        
        payroll_path = os.path.join(os.getcwd(), 'new_payroll')
        panels_path = os.path.join(payroll_path, 'payroll_panels')
        
        for panel in required_panels:
            panel_path = os.path.join(panels_path, panel)
            if os.path.exists(panel_path):
                st.success(f"✅ {panel}")
            else:
                st.error(f"❌ {panel}")
        
        with st.expander("Technical Details"):
            st.code(f"Import Error: {str(e)}")
            st.write(f"**Looking for payroll system at:** `{payroll_path}`")
            st.write(f"**Looking for panels at:** `{panels_path}`")
            st.write("**Note:** Payroll system uses `app.py` instead of `main_app.py`")
    
    except Exception as e:
        st.error(f"Payroll System Error: {str(e)}")
        st.info("Please check the payroll system configuration and try again.")
        
        with st.expander("Technical Details"):
            st.code(f"Error Type: {type(e).__name__}\nError Message: {str(e)}")

def get_payroll_system_status():
    """Get the status of the Payroll Data Management System"""
    try:
        payroll_path = os.path.join(os.getcwd(), 'new_payroll')
        
        # Check if payroll system exists
        if not os.path.exists(payroll_path):
            return {
                'available': False,
                'status': 'Payroll directory not found',
                'details': f'Path: {payroll_path}'
            }
        
        # Note: Payroll uses app.py instead of main_app.py
        app_path = os.path.join(payroll_path, 'app.py')
        if not os.path.exists(app_path):
            return {
                'available': False,
                'status': 'app.py not found',
                'details': 'Payroll system incomplete'
            }
        
        # Check required panels (note: payroll_panels folder)
        panels_path = os.path.join(payroll_path, 'payroll_panels')
        required_panels = [
            "payroll_main_panel.py",
            "payroll_statistics_panel.py", 
            "payroll_validation_panel.py",
            "payroll_dashboard_panel.py",
            "payroll_admin_panel.py"
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
        
        # Check session state for data status (note: payroll uses payroll_state)
        payroll_state = getattr(st.session_state, 'payroll_state', {})
        
        pa_files_status = {}
        pa_files = ['PA0008', 'PA0014']  # Payroll uses different PA files
        files_loaded = 0
        
        for pa_file in pa_files:
            key = f'source_{pa_file.lower()}'
            is_loaded = payroll_state.get(key) is not None
            pa_files_status[pa_file] = is_loaded
            if is_loaded:
                files_loaded += 1
        
        output_generated = bool(payroll_state.get('generated_payroll_files', {}))
        
        status_details = {
            'pa_files_loaded': files_loaded,
            'total_pa_files': len(pa_files),
            'pa_files_status': pa_files_status,
            'output_generated': output_generated,
            'ready_to_process': files_loaded >= 2  # Need both PA0008 & PA0014
        }
        
        if output_generated:
            status_msg = "Payroll system ready - Output files generated"
        elif files_loaded >= 2:
            status_msg = "Payroll system ready - All PA files loaded"
        elif files_loaded >= 1:
            status_msg = f"Payroll system ready - {files_loaded}/2 PA files loaded"
        else:
            status_msg = "Payroll system ready - Load PA files"
        
        return {
            'available': True,
            'status': status_msg,
            'details': status_details,
            'enhanced_features': [
                'PA Files Processing (PA0008 Basic Pay, PA0014 Recurring Payments)',
                'Wage Type Mapping & Validation',
                'Payroll Statistics & Analytics',
                'Dashboard & Monitoring', 
                'Admin Configuration (Password Protected)'
            ]
        }
        
    except Exception as e:
        return {
            'available': False,
            'status': f'Payroll system check failed: {str(e)}',
            'details': {'error': str(e)}
        }
