import streamlit as st
import sys
sys.path.append('payroll_panels')

# Import payroll panel functions
from payroll_main_panel import show_payroll_panel
from payroll_statistics_panel import show_payroll_statistics_panel  
from payroll_validation_panel import show_payroll_validation_panel
from payroll_dashboard_panel import show_payroll_dashboard_panel
from payroll_admin_panel import show_payroll_admin_panel

# Configure Streamlit for better performance
st.set_page_config(
    page_title="Payroll Data Management",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'payroll_state' not in st.session_state:
    st.session_state.payroll_state = {}

payroll_state = st.session_state.payroll_state

# Sidebar navigation with radio buttons
st.sidebar.title("💰 Payroll Data Management")
st.sidebar.markdown("---")

panel = st.sidebar.radio(
    "**Choose Panel:**",
    [
        "🏠 Payroll Processing",
        "📊 Statistics & Analytics", 
        "✅ Data Validation",
        "📈 Dashboard",
        "⚙️ Admin Configuration"
    ],
    key="payroll_panel_selection"
)

# Add quick stats in sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("**📋 Quick Status:**")

# Check data status
pa_files_loaded = sum(1 for file_key in ['PA0008', 'PA0014'] 
                     if payroll_state.get(f'source_{file_key.lower()}') is not None)
output_generated = 'generated_payroll_files' in payroll_state and payroll_state['generated_payroll_files']

st.sidebar.write(f"📂 PA Files: {pa_files_loaded}/2 loaded")
st.sidebar.write(f"📤 Output: {'✅ Generated' if output_generated else '❌ Not yet'}")

if pa_files_loaded >= 2:
    st.sidebar.success("✅ Ready to process")
else:
    st.sidebar.error("❌ Need PA0008 & PA0014")

st.sidebar.markdown("---")
st.sidebar.markdown("**💡 Quick Tips:**")
st.sidebar.info("1. Upload PA0008 & PA0014 files\n2. Process payroll data\n3. Validate results\n4. Analyze wage types")

# Show selected panel with performance optimization
try:
    if panel == "🏠 Payroll Processing":
        show_payroll_panel(payroll_state)
    elif panel == "📊 Statistics & Analytics":
        # Add warning for large datasets
        pa0008_data = payroll_state.get('source_pa0008')
        if pa0008_data is not None and len(pa0008_data) > 10000:
            st.warning("⚠️ Large dataset detected. Statistics panel may take a moment to load...")
        
        with st.spinner("Loading payroll statistics..."):
            show_payroll_statistics_panel(payroll_state)
    elif panel == "✅ Data Validation":
        with st.spinner("Running validation checks..."):
            show_payroll_validation_panel(payroll_state)
    elif panel == "📈 Dashboard":
        show_payroll_dashboard_panel(payroll_state)
    elif panel == "⚙️ Admin Configuration":
        show_payroll_admin_panel()

except Exception as e:
    st.error(f"❌ **Panel Error:** {str(e)}")
    st.info("**What to do:** Try refreshing the page or switching to a different panel")
    
    # Show error details in expander
    with st.expander("🔍 Technical Details", expanded=False):
        st.code(str(e))
        if st.button("🔄 Reset Session"):
            for key in list(st.session_state.keys()):
                if key.startswith('payroll'):
                    del st.session_state[key]
            st.rerun()

# Footer
st.sidebar.markdown("---")
st.sidebar.caption("💰 Payroll Data Management System v1.0")
