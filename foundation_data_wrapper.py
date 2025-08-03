import streamlit as st
import sys
import os
import pandas as pd
from datetime import datetime

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

def foundation_metrics(state):
    """Generate metrics for foundation system"""
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

def render_foundation_data_management():
    """Render the Foundation Data Management System with professional theme"""
    # Apply professional theme first
    apply_professional_mvs_theme()
    
    try:
        # Add the new_foundation path to sys.path
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
            
            # Import panels with error handling
            try:
                from hierarchy_panel_fixed import show_hierarchy_panel
            except ImportError:
                try:
                    from panels.hierarchy_panel_fixed import show_hierarchy_panel
                except ImportError:
                    def show_hierarchy_panel(state):
                        st.error("Hierarchy panel not found")
                        st.info("Please ensure hierarchy_panel_fixed.py exists")

            # Initialize session state
            if 'state' not in st.session_state:
                st.session_state.state = {
                    'hrp1000': None, 'hrp1001': None, 'hierarchy': None,
                    'admin_mode': False, 'generated_output_files': {}
                }

            # Professional header
            create_mvs_header(
                "Foundation Data Management", 
                "Organizational Hierarchy Processing & Validation"
            )
            
            # Professional status metrics
            metrics_data = foundation_metrics(st.session_state.state)
            create_mvs_metrics(metrics_data)

            # Sidebar navigation
            with st.sidebar:
                st.title("Foundation Data")
                
                # Admin mode toggle
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
                
                # Status indicators
                st.markdown("---")
                if st.session_state.state.get('admin_mode', False):
                    st.markdown("**Admin Mode:** :red[ACTIVE]")
                
                hrp1000_loaded = 'source_hrp1000' in st.session_state.state and st.session_state.state['source_hrp1000'] is not None
                hrp1001_loaded = 'source_hrp1001' in st.session_state.state and st.session_state.state['source_hrp1001'] is not None
                output_generated = bool(st.session_state.state.get('generated_output_files', {}))
                
                st.markdown("**System Status:**")
                st.markdown("🟢 HRP1000 Ready" if hrp1000_loaded else "🔴 HRP1000 Missing")
                st.markdown("🟢 HRP1001 Ready" if hrp1001_loaded else "🔴 HRP1001 Missing")
                st.markdown("🟢 Output Generated" if output_generated else "🟡 Output Pending")

            # Show welcome or panel content
            if not hrp1000_loaded and not hrp1001_loaded:
                st.markdown("""
                ## Getting Started with Foundation Data Management
                
                **Professional HR Data Processing Pipeline**
                
                ### Quick Start Guide:
                1. **Upload Data** - Load HRP1000 and HRP1001 files
                2. **Process Hierarchy** - Build organizational structure  
                3. **Validate Quality** - Comprehensive data validation
                4. **Generate Analytics** - End-to-end pipeline analysis
                5. **Monitor Health** - System performance tracking
                
                ### Enterprise Features:
                - Advanced Validation Engine
                - Real-time Analytics  
                - Data Lineage Tracking
                - Quality Metrics
                - Health Monitoring
                """)

            # Panel routing
            try:
                if panel == "Admin" and st.session_state.state.get('admin_mode', False):
                    st.markdown("<div class='admin-section'>", unsafe_allow_html=True)
                    st.header("Admin Configuration Center")
                    st.info("Administrative functions for system configuration and management.")
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                elif panel == "Hierarchy":
                    st.markdown("### Hierarchy Processing")
                    show_hierarchy_panel(st.session_state.state)
                    
                elif panel == "Validation":
                    st.markdown("### Data Validation")
                    st.info("Comprehensive data quality validation and analysis.")
                    
                elif panel == "Statistics":
                    st.markdown("### Statistics & Analytics")
                    st.info("End-to-end pipeline analysis and reporting.")
                    
                elif panel == "Health Monitor":
                    st.markdown("### System Health Monitor")
                    st.info("System performance monitoring and diagnostics.")
                    
            except Exception as e:
                st.error(f"Panel Error: {str(e)}")
                with st.expander("Technical Details"):
                    st.code(str(e))
            
        finally:
            os.chdir(original_cwd)
            sys.path = original_path
        
    except Exception as e:
        st.error(f"Foundation System Error: {str(e)}")

def get_foundation_system_status():
    """Get the status of the Foundation Data Management System"""
    try:
        foundation_path = os.path.join(os.getcwd(), 'new_foundation')
        
        if not os.path.exists(foundation_path):
            return {
                'available': False,
                'status': 'Foundation directory not found',
                'details': f'Path: {foundation_path}'
            }
        
        main_app_path = os.path.join(foundation_path, 'main_app.py')
        if not os.path.exists(main_app_path):
            return {
                'available': False,
                'status': 'main_app.py not found',
                'details': 'Foundation system incomplete'
            }
        
        foundation_state = getattr(st.session_state, 'state', {})
        
        hrp1000_loaded = foundation_state.get('source_hrp1000') is not None
        hrp1001_loaded = foundation_state.get('source_hrp1001') is not None
        hierarchy_processed = foundation_state.get('hierarchy_structure') is not None
        output_generated = bool(foundation_state.get('generated_output_files', {}))
        
        status_details = {
            'hrp1000_loaded': hrp1000_loaded,
            'hrp1001_loaded': hrp1001_loaded,
            'hierarchy_processed': hierarchy_processed,
            'output_generated': output_generated,
            'files_ready': hrp1000_loaded and hrp1001_loaded
        }
        
        if output_generated:
            status_msg = "Foundation system ready - Output files generated"
        elif hierarchy_processed:
            status_msg = "Foundation system ready - Generate output files"
        elif hrp1000_loaded and hrp1001_loaded:
            status_msg = "Foundation system ready - Process hierarchy"
        else:
            status_msg = "Foundation system ready - Load data files"
        
        return {
            'available': True,
            'status': status_msg,
            'details': status_details,
            'enhanced_features': [
                'Hierarchy Processing (HRP1000 & HRP1001)',
                'Advanced Validation Engine', 
                'Statistics & Analytics',
                'Health Monitor Dashboard',
                'Admin Configuration'
            ]
        }
        
    except Exception as e:
        return {
            'available': False,
            'status': f'Foundation system check failed: {str(e)}',
            'details': {'error': str(e)}
        }
