import os, sys
import streamlit as st
import base64
from streamlit_option_menu import option_menu
from employee_app import render_employee_tool

# Import the foundation data management wrapper
try:
    from foundation_data_wrapper import render_foundation_data_management, get_foundation_system_status
    FOUNDATION_WRAPPER_AVAILABLE = True
except ImportError as e:
    FOUNDATION_WRAPPER_AVAILABLE = False
    print(f"Foundation wrapper not available: {e}")
    # Fallback to old foundation system
    try:
        from foundation_module.foundation_app import render as render_foundation
        OLD_FOUNDATION_AVAILABLE = True
    except ImportError:
        OLD_FOUNDATION_AVAILABLE = False

# Import the employee data management wrapper
try:
    from employee_data_wrapper import render_employee_data_management, get_employee_system_status
    EMPLOYEE_WRAPPER_AVAILABLE = True
except ImportError as e:
    EMPLOYEE_WRAPPER_AVAILABLE = False
    print(f"Employee wrapper not available: {e}")

# Import the payroll data management wrapper
try:
    from payroll_data_wrapper import render_payroll_data_management, get_payroll_system_status
    PAYROLL_WRAPPER_AVAILABLE = True
except ImportError as e:
    PAYROLL_WRAPPER_AVAILABLE = False
    print(f"Payroll wrapper not available: {e}")
    # Fallback to old payroll system
    try:
        from payroll import app as payroll_app
        OLD_PAYROLL_AVAILABLE = True
    except ImportError:
        OLD_PAYROLL_AVAILABLE = False

# Professional tool styling
st.markdown("""
    <style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Dark professional theme */
    .stApp {
        background: linear-gradient(135deg, #1e3a5f 0%, #2d5282 50%, #1e3a5f 100%);
        color: #ffffff;
    }
    
    /* Main container styling */
    .main .block-container {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1.5rem;
        margin-top: 1rem;
    }
    
    /* Professional header */
    .tool-header {
        background: linear-gradient(90deg, #2563eb 0%, #1d4ed8 100%);
        padding: 1rem 2rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .tool-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: white;
        margin: 0;
    }
    
    .tool-subtitle {
        font-size: 0.9rem;
        color: rgba(255, 255, 255, 0.8);
        margin: 0;
    }
    
    /* Status cards */
    .status-card {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
    }
    
    .status-card:hover {
        background: rgba(255, 255, 255, 0.12);
        transform: translateY(-2px);
    }
    
    .metric-large {
        font-size: 2rem;
        font-weight: 700;
        color: #3b82f6;
        margin: 0;
    }
    
    .metric-label {
        font-size: 0.8rem;
        color: rgba(255, 255, 255, 0.7);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Progress indicators */
    .progress-container {
        background: rgba(0, 0, 0, 0.2);
        border-radius: 10px;
        height: 8px;
        margin: 0.5rem 0;
    }
    
    .progress-bar {
        height: 100%;
        border-radius: 10px;
        transition: width 0.3s ease;
    }
    
    .progress-success { background: #10b981; }
    .progress-warning { background: #f59e0b; }
    .progress-error { background: #ef4444; }
    
    /* System status indicators */
    .status-indicator {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        margin-right: 0.5rem;
    }
    
    .status-online { background: #10b981; }
    .status-warning { background: #f59e0b; }
    .status-offline { background: #ef4444; }
    
    /* Professional buttons */
    .stButton > button {
        background: linear-gradient(90deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .stButton > button:hover {
        background: linear-gradient(90deg, #2563eb 0%, #1d4ed8 100%);
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    
    /* Navigation styling */
    .nav-link {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: white !important;
    }
    
    .nav-link-selected {
        background: linear-gradient(90deg, #3b82f6 0%, #2563eb 100%) !important;
        border: 1px solid #3b82f6 !important;
    }
    
    /* Data table styling */
    .dataframe {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 8px;
    }
    
    /* Module cards */
    .module-card {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .module-card:hover {
        background: rgba(255, 255, 255, 0.12);
        border-color: #3b82f6;
        transform: translateY(-2px);
    }
    
    .module-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #3b82f6;
        margin-bottom: 0.5rem;
    }
    
    .module-description {
        font-size: 0.9rem;
        color: rgba(255, 255, 255, 0.8);
        line-height: 1.4;
    }
    </style>
""", unsafe_allow_html=True)

# Page setup
st.set_page_config(layout="wide", page_title="Data Tool", page_icon="⚙️")

# Session state
if "selected" not in st.session_state:
    st.session_state.selected = "Dashboard"
if "demo_page" not in st.session_state:
    st.session_state.demo_page = "main"

# Helper function to get system status
def get_system_status():
    status = {
        "foundation": "online" if FOUNDATION_WRAPPER_AVAILABLE else "offline",
        "employee": "online" if EMPLOYEE_WRAPPER_AVAILABLE else "offline", 
        "payroll": "online" if PAYROLL_WRAPPER_AVAILABLE else "offline",
        "validation": "online",  # Assume always available
    }
    return status

# Sidebar navigation
with st.sidebar:
    st.markdown("""
        <div style='text-align: center; padding: 1rem; margin-bottom: 1rem; 
                    background: rgba(255,255,255,0.1); border-radius: 8px;'>
            <h3 style='color: #3b82f6; margin: 0;'>Data Tool</h3>
            <p style='color: rgba(255,255,255,0.7); font-size: 0.8rem; margin: 0;'>
                SAP HR Data Processing
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    selected = option_menu(
        menu_title=None,
        options=["Dashboard", "Data Tools", "Analytics", "System Config"],
        icons=["speedometer2", "arrow-repeat", "graph-up", "gear"],
        default_index=0,
        styles={
            "container": {"padding": "0px", "background-color": "transparent"},
            "icon": {"color": "#3b82f6", "font-size": "16px"},
            "nav-link": {
                "font-size": "14px",
                "text-align": "left",
                "margin": "2px",
                "padding": "8px 12px",
                "background-color": "rgba(255,255,255,0.05)",
                "border": "1px solid rgba(255,255,255,0.1)",
                "border-radius": "6px",
                "color": "white",
                "--hover-color": "rgba(255,255,255,0.1)",
            },
            "nav-link-selected": {
                "background": "linear-gradient(90deg, #3b82f6 0%, #2563eb 100%)",
                "border": "1px solid #3b82f6",
                "font-weight": "500"
            },
        },
    )
    st.session_state.selected = selected

    # System status in sidebar
    st.markdown("---")
    st.markdown("**System Status**")
    status = get_system_status()
    
    for system, state in status.items():
        status_class = f"status-{state}"
        st.markdown(f"""
            <div style='margin: 0.3rem 0;'>
                <span class='status-indicator {status_class}'></span>
                <span style='font-size: 0.8rem; color: rgba(255,255,255,0.8);'>
                    {system.title()}
                </span>
            </div>
        """, unsafe_allow_html=True)

# -------------------- DASHBOARD --------------------
if selected == "Dashboard":
    # Header
    st.markdown("""
        <div class='tool-header'>
            <h1 class='tool-title'>Data Processing Dashboard</h1>
            <p class='tool-subtitle'>SAP HR Data Migration Dashboard</p>
        </div>
    """, unsafe_allow_html=True)

    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
            <div class='status-card'>
                <div class='metric-large'>156</div>
                <div class='metric-label'>Total Records</div>
                <div class='progress-container'>
                    <div class='progress-bar progress-success' style='width: 85%;'></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class='status-card'>
                <div class='metric-large'>142</div>
                <div class='metric-label'>Processed</div>
                <div class='progress-container'>
                    <div class='progress-bar progress-success' style='width: 91%;'></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class='status-card'>
                <div class='metric-large'>11</div>
                <div class='metric-label'>Warnings</div>
                <div class='progress-container'>
                    <div class='progress-bar progress-warning' style='width: 20%;'></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
            <div class='status-card'>
                <div class='metric-large'>3</div>
                <div class='metric-label'>Errors</div>
                <div class='progress-container'>
                    <div class='progress-bar progress-error' style='width: 15%;'></div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # Migration modules
    st.markdown("### Available Migration Modules")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Foundation Data", key="dash_foundation", use_container_width=True):
            st.session_state.selected = "Data Tools"
            st.session_state.demo_page = "foundation_data_view"
            st.rerun()
        
        st.markdown(f"""
            <div style='font-size: 0.8rem; color: rgba(255,255,255,0.7); margin-top: 0.5rem;'>
                <span class='status-indicator status-{"online" if FOUNDATION_WRAPPER_AVAILABLE else "offline"}'></span>
                {"Enhanced Processing Available" if FOUNDATION_WRAPPER_AVAILABLE else "Legacy System"}
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("Employee Data", key="dash_employee", use_container_width=True):
            st.session_state.selected = "Data Tools"
            st.session_state.demo_page = "employee_data_management"
            st.rerun()
            
        st.markdown(f"""
            <div style='font-size: 0.8rem; color: rgba(255,255,255,0.7); margin-top: 0.5rem;'>
                <span class='status-indicator status-{"online" if EMPLOYEE_WRAPPER_AVAILABLE else "offline"}'></span>
                {"Enhanced Processing Available" if EMPLOYEE_WRAPPER_AVAILABLE else "Legacy System"}
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if st.button("Payroll Data", key="dash_payroll", use_container_width=True):
            st.session_state.selected = "Data Tools"
            st.session_state.demo_page = "payroll_data_tool"
            st.rerun()
            
        st.markdown(f"""
            <div style='font-size: 0.8rem; color: rgba(255,255,255,0.7); margin-top: 0.5rem;'>
                <span class='status-indicator status-{"online" if PAYROLL_WRAPPER_AVAILABLE else "offline"}'></span>
                {"Enhanced Processing Available" if PAYROLL_WRAPPER_AVAILABLE else "Legacy System"}
            </div>
        """, unsafe_allow_html=True)
        
        st.button("Time Data", key="dash_time", disabled=True, use_container_width=True)
        st.markdown("""
            <div style='font-size: 0.8rem; color: rgba(255,255,255,0.7); margin-top: 0.5rem;'>
                <span class='status-indicator status-offline'></span>
                Coming Soon
            </div>
        """, unsafe_allow_html=True)

    # Recent activity
    st.markdown("### Recent Activity")
    recent_data = [
        {"Time": "14:32", "Module": "Foundation", "Action": "Data Validation", "Status": "✅ Complete"},
        {"Time": "14:15", "Module": "Employee", "Action": "File Upload", "Status": "⚠️ Warning"},
        {"Time": "13:45", "Module": "Payroll", "Action": "Mapping Rules", "Status": "🔄 Processing"},
        {"Time": "13:22", "Module": "Foundation", "Action": "Export Data", "Status": "✅ Complete"},
    ]
    
    st.dataframe(recent_data, use_container_width=True, hide_index=True)

# -------------------- DATA TOOLS --------------------
elif selected == "Data Tools":
    if st.session_state.demo_page == "main":
        st.markdown("""
            <div class='tool-header'>
                <h1 class='tool-title'>Data Processing Tools</h1>
                <p class='tool-subtitle'>Select a data module to begin processing</p>
            </div>
        """, unsafe_allow_html=True)

        # Tool cards
        col1, col2 = st.columns(2)
        
        with col1:
            # Foundation Data Card
            st.markdown(f"""
                <div class='module-card'>
                    <div class='module-title'>Foundation Data</div>
                    <div class='module-description'>
                        {"Enhanced organizational hierarchy processing with HRP1000/HRP1001 support" if FOUNDATION_WRAPPER_AVAILABLE else "Organizational structure and hierarchy management"}
                    </div>
                    <div style='margin-top: 1rem; font-size: 0.8rem;'>
                        <span class='status-indicator status-{"online" if FOUNDATION_WRAPPER_AVAILABLE else "offline"}'></span>
                        {"Enhanced System" if FOUNDATION_WRAPPER_AVAILABLE else "Legacy System"}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button("Open Foundation Data", key="found_btn", use_container_width=True):
                st.session_state.demo_page = "foundation_data_view"
                st.rerun()
            
            # Employee Data Card
            st.markdown(f"""
                <div class='module-card'>
                    <div class='module-title'>Employee Data</div>
                    <div class='module-description'>
                        {"Complete employee information processing with PA0001/PA0002/PA0006/PA0105 files" if EMPLOYEE_WRAPPER_AVAILABLE else "Employee personal and job information management"}
                    </div>
                    <div style='margin-top: 1rem; font-size: 0.8rem;'>
                        <span class='status-indicator status-{"online" if EMPLOYEE_WRAPPER_AVAILABLE else "offline"}'></span>
                        {"Enhanced System" if EMPLOYEE_WRAPPER_AVAILABLE else "Legacy System"}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button("Open Employee Data", key="emp_btn", use_container_width=True):
                st.session_state.demo_page = "employee_data_management"
                st.rerun()
        
        with col2:
            # Payroll Data Card
            st.markdown(f"""
                <div class='module-card'>
                    <div class='module-title'>Payroll Data</div>
                    <div class='module-description'>
                        {"Advanced payroll processing with PA0008/PA0014 wage type validation" if PAYROLL_WRAPPER_AVAILABLE else "Payroll and compensation data management"}
                    </div>
                    <div style='margin-top: 1rem; font-size: 0.8rem;'>
                        <span class='status-indicator status-{"online" if PAYROLL_WRAPPER_AVAILABLE else "offline"}'></span>
                        {"Enhanced System" if PAYROLL_WRAPPER_AVAILABLE else "Legacy System"}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button("Open Payroll Data", key="pay_btn", use_container_width=True):
                st.session_state.demo_page = "payroll_data_tool"
                st.rerun()
            
            # Time Data Card (disabled)
            st.markdown("""
                <div class='module-card' style='opacity: 0.5; cursor: not-allowed;'>
                    <div class='module-title' style='color: rgba(255,255,255,0.5);'>Time Data</div>
                    <div class='module-description'>
                        Time management and absence tracking
                    </div>
                    <div style='margin-top: 1rem; font-size: 0.8rem;'>
                        <span class='status-indicator status-offline'></span>
                        Coming Soon
                    </div>
                </div>
            """, unsafe_allow_html=True)

    # Individual tool pages
    elif st.session_state.demo_page == "foundation_data_view":
        col1, col2 = st.columns([1, 6])
        with col1:
            if st.button("← Back", key="back_from_foundation", use_container_width=True):
                st.session_state.demo_page = "main"
                st.rerun()
        
        if FOUNDATION_WRAPPER_AVAILABLE:
            render_foundation_data_management()
        else:
            try:
                if 'OLD_FOUNDATION_AVAILABLE' in globals() and OLD_FOUNDATION_AVAILABLE:
                    st.markdown("### Foundation Data Processing")
                    render_foundation()
                else:
                    st.error("❌ Foundation system not available")
            except Exception as e:
                st.error("❌ Foundation system not available")

    elif st.session_state.demo_page == "employee_data_management":
        col1, col2 = st.columns([1, 6])
        with col1:
            if st.button("← Back", key="back_from_employee", use_container_width=True):
                st.session_state.demo_page = "main"
                st.rerun()

        if EMPLOYEE_WRAPPER_AVAILABLE:
            render_employee_data_management()
        else:
            st.error("❌ Employee Data Management system not available")

    elif st.session_state.demo_page == "payroll_data_tool":
        col1, col2 = st.columns([1, 6])
        with col1:
            if st.button("← Back", key="back_from_payroll", use_container_width=True):
                st.session_state.demo_page = "main"
                st.rerun()

        if PAYROLL_WRAPPER_AVAILABLE:
            render_payroll_data_management()
        else:
            try:
                if 'OLD_PAYROLL_AVAILABLE' in globals() and OLD_PAYROLL_AVAILABLE:
                    payroll_app.render_payroll_tool()
                else:
                    st.error("❌ Payroll system not available")
            except Exception as e:
                st.error("❌ Payroll system not available")

# -------------------- ANALYTICS --------------------
elif selected == "Analytics":
    st.markdown("""
        <div class='tool-header'>
            <h1 class='tool-title'>Data Analytics</h1>
            <p class='tool-subtitle'>Data validation and quality reporting</p>
        </div>
    """, unsafe_allow_html=True)

    # Analytics tabs
    tab1, tab2, tab3 = st.tabs(["Validation Report", "Data Quality", "Performance"])
    
    with tab1:
        st.subheader("Validation Summary")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
                <div class='status-card'>
                    <div class='metric-large' style='color: #10b981;'>89%</div>
                    <div class='metric-label'>Validation Pass Rate</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
                <div class='status-card'>
                    <div class='metric-large' style='color: #f59e0b;'>47</div>
                    <div class='metric-label'>Items Requiring Attention</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
                <div class='status-card'>
                    <div class='metric-large' style='color: #3b82f6;'>2.3s</div>
                    <div class='metric-label'>Avg Processing Time</div>
                </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        st.subheader("Data Quality Metrics")
        st.info("Data quality analysis tools coming soon")
    
    with tab3:
        st.subheader("Performance Monitoring")
        st.info("Performance monitoring dashboard coming soon")

# -------------------- SYSTEM CONFIG --------------------
elif selected == "System Config":
    st.markdown("""
        <div class='tool-header'>
            <h1 class='tool-title'>System Configuration</h1>
            <p class='tool-subtitle'>Manage system settings and connections</p>
        </div>
    """, unsafe_allow_html=True)

    # Config tabs
    tab1, tab2, tab3 = st.tabs(["Connections", "User Management", "System Settings"])
    
    with tab1:
        st.subheader("System Connections")
        
        connections = [
            {"System": "SAP HCM", "Status": "Connected", "Last Sync": "2 min ago"},
            {"System": "SuccessFactors", "Status": "Connected", "Last Sync": "5 min ago"},
            {"System": "S/4HANA", "Status": "Disconnected", "Last Sync": "Never"},
        ]
        
        st.dataframe(connections, use_container_width=True, hide_index=True)
    
    with tab2:
        st.subheader("User Access Control")
        st.info("User management interface coming soon")
    
    with tab3:
        st.subheader("System Preferences")
        st.info("System settings interface coming soon")
