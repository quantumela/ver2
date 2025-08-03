import streamlit as st
import sys
sys.path.append('panels')

# Import panel functions - FIXED imports
from employee_main_panel import show_employee_panel
from employee_statistics_panel import show_employee_statistics_panel  
from employee_validation_panel import show_employee_validation_panel
from employee_dashboard_panel import show_employee_dashboard_panel
from employee_admin_panel import show_employee_admin_panel

# Configure Streamlit for better performance
st.set_page_config(
    page_title="Employee Data Management",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'state' not in st.session_state:
    st.session_state.state = {}

state = st.session_state.state

# Sidebar navigation with radio buttons
st.sidebar.title("👥 Employee Data Management")
st.sidebar.markdown("---")

panel = st.sidebar.radio(
    "**Choose Panel:**",
    [
        "🏠 Employee Processing",
        "📊 Statistics & Detective", 
        "✅ Data Validation",
        "📈 Dashboard",
        "⚙️ Admin Configuration"
    ],
    key="main_panel_selection"
)

# Add quick stats in sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("**📋 Quick Status:**")

# Check data status
pa_files_loaded = sum(1 for file_key in ['PA0001', 'PA0002', 'PA0006', 'PA0105'] 
                     if state.get(f'source_{file_key.lower()}') is not None)
output_generated = 'generated_employee_files' in state and state['generated_employee_files']

st.sidebar.write(f"📂 PA Files: {pa_files_loaded}/4 loaded")
st.sidebar.write(f"📤 Output: {'✅ Generated' if output_generated else '❌ Not yet'}")

if pa_files_loaded >= 2:
    st.sidebar.success("✅ Ready to process")
else:
    st.sidebar.error("❌ Need PA0001 & PA0002")

st.sidebar.markdown("---")
st.sidebar.markdown("**💡 Quick Tips:**")
st.sidebar.info("1. Upload PA files first\n2. Process employee data\n3. Validate results\n4. Analyze statistics")

# Show selected panel with performance optimization
try:
    if panel == "🏠 Employee Processing":
        show_employee_panel(state)
    elif panel == "📊 Statistics & Detective":
        # Add warning for large datasets
        pa0002_data = state.get('source_pa0002')
        if pa0002_data is not None and len(pa0002_data) > 10000:
            st.warning("⚠️ Large dataset detected. Statistics panel may take a moment to load...")
        
        with st.spinner("Loading statistics..."):
            show_employee_statistics_panel(state)
    elif panel == "✅ Data Validation":
        with st.spinner("Running validation checks..."):
            show_employee_validation_panel(state)
    elif panel == "📈 Dashboard":
        show_employee_dashboard_panel(state)
    elif panel == "⚙️ Admin Configuration":
        show_protected_employee_panel()

except Exception as e:
    st.error(f"❌ **Panel Error:** {str(e)}")
    st.info("**What to do:** Try refreshing the page or switching to a different panel")
    
    # Show error details in expander
    with st.expander("🔍 Technical Details", expanded=False):
        st.code(str(e))
        if st.button("🔄 Reset Session"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

# Footer
st.sidebar.markdown("---")
st.sidebar.caption("💻 Employee Data Management System v2.0")
