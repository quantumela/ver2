import streamlit as st
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
