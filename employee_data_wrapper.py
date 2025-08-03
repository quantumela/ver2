import streamlit as st
import sys
import os

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
        
        /* Professional navigation buttons */
        .css-1d391kg .stRadio label {
            color: #e5e7eb !important;
            font-weight: 500 !important;
            padding: 12px 16px !important;
            border-radius: 6px !important;
            margin: 4px 0 !important;
            transition: all 0.2s ease !important;
            display: block !important;
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
        }
        
        .stDataFrame td {
            padding: 10px !important;
            border-bottom: 1px solid #f1f5f9 !important;
            color: #4b5563 !important;
        }
        
        /* Professional input fields */
        .stTextInput > div > div > input {
            border: 1px solid #d1d5db !important;
            border-radius: 6px !important;
            padding: 10px 12px !important;
            font-size: 14px !important;
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

def employee_metrics(state):
    """Generate metrics for employee system"""
    pa_files = ['PA0001', 'PA0002', 'PA0006', 'PA0105']
    files_loaded = sum(1 for file_key in pa_files if state.get(f'source_{file_key.lower()}') is not None)
    output_generated = bool(state.get('generated_employee_files', {}))
    
    return [
        ("PA Files", f"{files_loaded}/4", "success" if files_loaded >= 2 else "warning", "Employee data files"),
        ("Processing", "Ready" if files_loaded >= 2 else "Pending", "success" if files_loaded >= 2 else "error", "System status"),
        ("Output", "Generated" if output_generated else "Pending", "success" if output_generated else "warning", "Employee files"),
        ("Quality", "Validated" if files_loaded >= 2 else "Pending", "info" if files_loaded >= 2 else "warning", "Data validation")
    ]

def render_employee_data_management():
    """Render the Employee Data Management System with professional theme"""
    # Apply professional theme first
    apply_professional_mvs_theme()
    
    try:
        # Add the new_employee path to sys.path
        employee_path = os.path.join(os.getcwd(), 'new_employee')
        panels_path = os.path.join(employee_path, 'panels')
        
        paths_to_add = [employee_path, panels_path]
        original_path = sys.path.copy()
        
        for path in paths_to_add:
            if os.path.exists(path) and path not in sys.path:
                sys.path.insert(0, path)
        
        original_cwd = os.getcwd()
        
        try:
            if os.path.exists(employee_path):
                os.chdir(employee_path)
            
            # Import panel functions with error handling
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
            
            # Initialize session state
            if 'state' not in st.session_state:
                st.session_state.state = {'admin_mode': False}
            
            if 'admin_mode' not in st.session_state.state:
                st.session_state.state['admin_mode'] = False
            
            state = st.session_state.state

            # Professional header
            create_mvs_header(
                "Employee Data Management", 
                "Personnel Information Processing & Analytics"
            )
            
            # Professional status metrics
            metrics_data = employee_metrics(st.session_state.state)
            create_mvs_metrics(metrics_data)

            # Sidebar navigation
            with st.sidebar:
                st.title("Employee Data")
                
                # Admin mode toggle
                current_admin_mode = st.session_state.state.get('admin_mode', False)
                admin_enabled = st.checkbox("Admin Mode", value=current_admin_mode, key="employee_admin_mode")
                
                if admin_enabled and not current_admin_mode:
                    try:
                        admin_password = st.secrets.get("admin_password", None)
                        if admin_password:
                            entered_pw = st.text_input("Admin Password", type="password", key="employee_admin_password")
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
                    if st.button("Logout Admin", key="employee_admin_logout"):
                        st.session_state.state['admin_mode'] = False
                        st.rerun()
                
                st.markdown("---")
                
                # Navigation options
                if st.session_state.state.get('admin_mode', False):
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
                
                panel = st.radio("Choose Panel:", panel_options, key="employee_panel_selection")
                
                # Status indicators
                st.markdown("---")
                if st.session_state.state.get('admin_mode', False):
                    st.markdown("**Admin Mode:** :red[ACTIVE]")
                
                pa_files_loaded = sum(1 for file_key in ['PA0001', 'PA0002', 'PA0006', 'PA0105'] 
                                     if state.get(f'source_{file_key.lower()}') is not None)
                output_generated = 'generated_employee_files' in state and state['generated_employee_files']
                
                st.markdown("**Quick Status:**")
                st.write(f"PA Files: {pa_files_loaded}/4 loaded")
                st.write(f"Output: {'Generated' if output_generated else 'Not yet'}")
                
                if pa_files_loaded >= 2:
                    st.success("Ready to process")
                else:
                    st.error("Need PA0001 & PA0002")
                
                st.markdown("**Quick Tips:**")
                st.info("1. Upload PA files first\n2. Process employee data\n3. Validate results\n4. Analyze statistics")

            # Show welcome or panel content
            if pa_files_loaded == 0:
                st.markdown("""
                ## Getting Started with Employee Data Management
                
                **Professional Employee Information Processing**
                
                ### Quick Start Guide:
                1. **Upload PA Files** - Load PA0001, PA0002, PA0006, PA0105
                2. **Process Data** - Transform employee data for target system
                3. **Validate Results** - Check data quality and completeness
                4. **Analyze Statistics** - Use Statistics & Detective for detailed analysis
                5. **Monitor Progress** - Track processing in the Dashboard
                
                ### Supported PA Files:
                - **PA0001**: Organizational Assignment
                - **PA0002**: Personal Data
                - **PA0006**: Address Information  
                - **PA0105**: Communication Data
                
                ### Features:
                - Employee data validation and quality checks
                - Statistics and detective analysis
                - Dashboard monitoring and reporting
                - Admin configuration options (password protected)
                """)

            # Panel routing
            try:
                if panel == "Employee Processing":
                    show_employee_panel(state)
                elif panel == "Statistics & Detective":
                    # Add warning for large datasets
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
                    if st.session_state.state.get('admin_mode', False):
                        st.markdown("<div class='admin-section'>", unsafe_allow_html=True)
                        st.header("Employee Admin Configuration Center")
                        show_employee_admin_panel()
                        st.markdown("</div>", unsafe_allow_html=True)
                    else:
                        st.error("Admin access required")
                        st.info("Please enable Admin Mode and enter the correct password to access this panel.")
            
            except Exception as e:
                st.error(f"Panel Error: {str(e)}")
                st.info("Try refreshing the page or switching to a different panel")
                
                with st.expander("Technical Details", expanded=False):
                    st.code(str(e))
                    if st.button("Reset Session", key="reset_employee_session"):
                        for key in list(st.session_state.keys()):
                            del st.session_state[key]
                        st.rerun()
            
        finally:
            os.chdir(original_cwd)
            sys.path = original_path
        
    except Exception as e:
        st.error(f"Employee System Error: {str(e)}")

def get_employee_system_status():
    """Get the status of the Employee Data Management System"""
    try:
        employee_path = os.path.join(os.getcwd(), 'new_employee')
        
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
        
        employee_state = getattr(st.session_state, 'state', {})
        
        pa_files = ['PA0001', 'PA0002', 'PA0006', 'PA0105']
        files_loaded = sum(1 for file_key in pa_files if employee_state.get(f'source_{file_key.lower()}') is not None)
        
        if files_loaded >= 2:
            status_msg = f"Employee system ready - {files_loaded}/4 PA files loaded"
        else:
            status_msg = "Employee system ready - Load PA files"
        
        return {
            'available': True,
            'status': status_msg,
            'details': {'pa_files_loaded': files_loaded},
            'enhanced_features': [
                'PA Files Processing (PA0001, PA0002, PA0006, PA0105)',
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
