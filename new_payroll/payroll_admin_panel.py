import streamlit as st
import pandas as pd
import numpy as np
import os
import json
from pathlib import Path
from typing import List, Dict, Optional, Union
import io
from datetime import datetime

# Configuration directories
CONFIG_DIR = "payroll_configs"
PICKLIST_DIR = "payroll_picklists"
SOURCE_SAMPLES_DIR = "payroll_source_samples"
MAX_SAMPLE_ROWS = 1000

def initialize_directories() -> None:
    """Create required directories if they don't exist"""
    for directory in [CONFIG_DIR, PICKLIST_DIR, SOURCE_SAMPLES_DIR]:
        Path(directory).mkdir(exist_ok=True)

def get_payroll_source_columns(source_file: str) -> List[str]:
    """Get available columns from payroll source files"""
    try:
        sample_path = os.path.join(SOURCE_SAMPLES_DIR, f"{source_file}_sample.csv")
        if os.path.exists(sample_path):
            df = pd.read_csv(sample_path, nrows=1)
            return df.columns.tolist()
    except Exception as e:
        st.error(f"Error loading source columns: {str(e)}")
    
    # Fallback to standard PA file columns for payroll
    standard_columns = {
        "PA0008": ["Pers.No.", "Wage Type", "Amount", "Currency", "Pay Period", "Payment Date", 
                   "Cost Center", "Status", "Overtime Hours", "Regular Hours", "Bonus Type",
                   "Tax Code", "Gross Amount", "Net Amount", "Start Date", "End Date"],
        "PA0014": ["Pers.No.", "Recurring Amount", "Deduction Type", "Benefit Type", "Frequency",
                   "Start Date", "End Date", "Annual Amount", "Monthly Amount", "Percentage",
                   "Maximum Amount", "Status", "Priority", "Tax Treatment"]
    }
    
    return standard_columns.get(source_file, [])

def save_config_with_session_state(config_type: str, config_data: Union[Dict, List]) -> None:
    """Save configuration to both file and session state"""
    
    # Save to file
    save_config(config_type, config_data)
    
    # Also save to session state for immediate access
    if config_type == "payroll_column_mappings":
        if isinstance(config_data, list):
            mapping_df = pd.DataFrame(config_data)
        else:
            mapping_df = config_data
            
        # Save to multiple session state keys for compatibility
        st.session_state['payroll_mapping_config'] = mapping_df
        st.session_state['payroll_current_mappings'] = mapping_df
        st.session_state['payroll_admin_mappings'] = mapping_df
        
        st.success("✅ Payroll configuration saved and ready to use!")
        
    elif config_type == "payroll_template":
        st.session_state['payroll_template_config'] = config_data
        st.success("✅ Payroll template saved!")

def load_config_with_session_state(config_type: str) -> Optional[Union[Dict, List]]:
    """Load configuration from session state first, then fall back to file"""
    
    if config_type == "payroll_column_mappings":
        # Check session state first
        if 'payroll_mapping_config' in st.session_state:
            config_data = st.session_state['payroll_mapping_config']
            if isinstance(config_data, pd.DataFrame):
                return config_data.to_dict('records')
            return config_data
    
    # Fall back to file-based loading
    return load_config(config_type)

def save_config(config_type: str, config_data: Union[Dict, List]) -> None:
    """Save configuration to file"""
    try:
        config_path = f"{CONFIG_DIR}/{config_type}_config.json"
        with open(config_path, "w") as f:
            json.dump(config_data, f, indent=2)
    except Exception as e:
        st.error(f"Error saving config: {str(e)}")

def load_config(config_type: str) -> Optional[Union[Dict, List]]:
    """Load configuration from file"""
    try:
        config_path = f"{CONFIG_DIR}/{config_type}_config.json"
        if not os.path.exists(config_path):
            return None
            
        with open(config_path, "r") as f:
            data = json.load(f)
            return data
    except Exception as e:
        st.error(f"Error loading config: {str(e)}")
        return None

def get_simple_transformation_options():
    """Get simple transformation options for payroll data"""
    return {
        "None": "Use data as-is",
        "Number Format": "Format as decimal (123.45)",
        "Currency Format": "Format as currency ($123.45)",
        "Date Format (YYYY-MM-DD)": "Convert dates to standard format",
        "Date Format (YYYY-MM)": "Convert to month format (for pay periods)",
        "UPPERCASE": "All capital letters (USD, ACTIVE)",
        "Title Case": "Proper capitalization (Regular Pay)",
        "lowercase": "All small letters (bonus)",
        "Trim Whitespace": "Remove extra spaces",
        "Status Mapping": "Convert status codes to readable text",
        "Wage Type Mapping": "Convert wage type codes to descriptions"
    }

def get_default_payroll_template():
    """Get the standard payroll data template"""
    return [
        {"target_column": "EMPLOYEE_ID", "display_name": "Employee ID", "description": "Unique identifier for each employee"},
        {"target_column": "WAGE_TYPE", "display_name": "Wage Type", "description": "Type of payment (salary, bonus, overtime)"},
        {"target_column": "AMOUNT", "display_name": "Amount", "description": "Payment amount"},
        {"target_column": "CURRENCY", "display_name": "Currency", "description": "Currency code (USD, EUR, etc.)"},
        {"target_column": "PAY_PERIOD", "display_name": "Pay Period", "description": "Period this payment covers"},
        {"target_column": "PAYMENT_DATE", "display_name": "Payment Date", "description": "When the payment was made"},
        {"target_column": "RECURRING_AMOUNT", "display_name": "Recurring Amount", "description": "Regular recurring payments/deductions"},
        {"target_column": "DEDUCTION_TYPE", "display_name": "Deduction Type", "description": "Type of deduction (tax, insurance, etc.)"},
        {"target_column": "STATUS", "display_name": "Status", "description": "Payment status (processed, pending, etc.)"},
        {"target_column": "COST_CENTER", "display_name": "Cost Center", "description": "Accounting cost center"},
        {"target_column": "GROSS_AMOUNT", "display_name": "Gross Amount", "description": "Amount before deductions"},
        {"target_column": "NET_AMOUNT", "display_name": "Net Amount", "description": "Amount after deductions"},
        {"target_column": "TAX_CODE", "display_name": "Tax Code", "description": "Tax classification code"}
    ]

def show_configuration_status():
    """Show current payroll configuration status"""
    st.subheader("📋 Payroll Configuration Status")
    st.info("**What this shows:** Whether your payroll data configuration is ready to use")
    
    # Check what's configured
    template = load_config("payroll_template")
    mappings = load_config("payroll_column_mappings")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if template:
            st.success("✅ **Payroll Template**")
            st.caption(f"{len(template)} fields configured")
        else:
            st.error("❌ **Payroll Template**")
            st.caption("Not set up yet")
    
    with col2:
        if mappings:
            st.success("✅ **Field Mappings**")
            st.caption(f"{len(mappings)} mappings created")
        else:
            st.error("❌ **Field Mappings**")
            st.caption("Not configured yet")
    
    with col3:
        # Check if sample files exist
        sample_files = 0
        for pa_file in ['PA0008', 'PA0014']:
            sample_path = os.path.join(SOURCE_SAMPLES_DIR, f"{pa_file}_sample.csv")
            if os.path.exists(sample_path):
                sample_files += 1
        
        if sample_files > 0:
            st.success(f"✅ **Sample Files**")
            st.caption(f"{sample_files}/2 files uploaded")
        else:
            st.warning("⚪ **Sample Files**")
            st.caption("None uploaded yet")
    
    # Overall readiness
    if template and mappings:
        st.success("🎉 **Configuration Complete!** Ready to process payroll data")
    elif template or mappings:
        st.warning("⚠️ **Configuration Partial** - Some setup still needed")
    else:
        st.info("ℹ️ **Configuration Not Started** - Follow the setup steps below")

def upload_sample_files():
    """Handle sample file uploads for payroll with simple explanations"""
    st.subheader("📂 Upload Payroll Sample Files")
    st.info("**What this does:** Upload small samples of your PA files so we can see what payroll data fields are available")
    
    # Select file type
    file_type = st.selectbox(
        "Which type of payroll file are you uploading?",
        ["PA0008 (Wage Types)", "PA0014 (Recurring Elements)"],
        help="Choose the type that matches your file"
    )
    
    # Extract PA code
    pa_code = file_type.split()[0]  # Gets PA0008, PA0014
    
    # File descriptions
    descriptions = {
        "PA0008": "Contains wage types, salary amounts, bonuses, overtime, and payment information",
        "PA0014": "Contains recurring payments and deductions like benefits, taxes, and regular allowances"
    }
    
    st.write(f"**{pa_code}:** {descriptions.get(pa_code, 'Payroll data file')}")
    
    # File upload
    uploaded_file = st.file_uploader(
        f"Upload your {pa_code} sample file:",
        type=['csv', 'xlsx', 'xls'],
        help="Upload a small sample (first 1000 rows is enough)"
    )
    
    if uploaded_file:
        try:
            # Read the file
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file, nrows=MAX_SAMPLE_ROWS)
            else:
                df = pd.read_excel(uploaded_file, nrows=MAX_SAMPLE_ROWS)
            
            # Save sample
            sample_path = os.path.join(SOURCE_SAMPLES_DIR, f"{pa_code}_sample.csv")
            df.to_csv(sample_path, index=False)
            
            st.success(f"✅ **{pa_code} sample uploaded successfully!**")
            
            # Show preview
            st.subheader("📋 File Preview")
            st.dataframe(df.head(3), use_container_width=True)
            
            # Show field information
            st.subheader("📊 Available Fields")
            st.write(f"**Total Records:** {len(df):,}")
            st.write(f"**Available Fields:** {len(df.columns)}")
            
            # Show columns in a neat way
            col_chunks = [df.columns[i:i+3] for i in range(0, len(df.columns), 3)]
            for chunk in col_chunks:
                cols = st.columns(3)
                for i, col_name in enumerate(chunk):
                    with cols[i]:
                        st.write(f"• {col_name}")
            
        except Exception as e:
            st.error(f"❌ Error reading file: {str(e)}")
            st.info("**Tips:** Make sure your file is a valid CSV or Excel file with payroll data")

def configure_payroll_template():
    """Configure the payroll data template with simple interface"""
    st.subheader("🎯 Payroll Data Template")
    st.info("**What this does:** Define what fields you want in your final payroll file (payroll.csv)")
    
    # Load current template or use default
    current_template = load_config("payroll_template") or get_default_payroll_template()
    
    # Initialize session state
    if "payroll_template_edit" not in st.session_state:
        st.session_state["payroll_template_edit"] = current_template.copy()
    
    st.markdown("**Instructions:** These are the fields that will appear in your final payroll file. You can add, remove, or reorder them.")
    
    # Reset to default
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write("**Current Payroll Fields:**")
    with col2:
        if st.button("🔄 Reset to Default", help="Restore the standard payroll fields"):
            st.session_state["payroll_template_edit"] = get_default_payroll_template()
            st.rerun()
    
    # Show current fields in a simple table
    if st.session_state["payroll_template_edit"]:
        for i, field in enumerate(st.session_state["payroll_template_edit"]):
            cols = st.columns([3, 3, 3, 1, 1])
            
            with cols[0]:
                field['target_column'] = st.text_input(
                    "Field Code",
                    value=field['target_column'],
                    key=f"payroll_field_code_{i}",
                    help="Technical name (e.g., EMPLOYEE_ID, WAGE_TYPE)"
                )
            
            with cols[1]:
                field['display_name'] = st.text_input(
                    "Display Name", 
                    value=field['display_name'],
                    key=f"payroll_field_name_{i}",
                    help="Human-readable name (e.g., Employee ID, Wage Type)"
                )
            
            with cols[2]:
                field['description'] = st.text_input(
                    "Description",
                    value=field.get('description', ''),
                    key=f"payroll_field_desc_{i}",
                    help="What this field contains"
                )
            
            with cols[3]:
                if st.button("⬆️", key=f"payroll_up_{i}", disabled=(i == 0), help="Move up"):
                    st.session_state["payroll_template_edit"][i], st.session_state["payroll_template_edit"][i-1] = \
                        st.session_state["payroll_template_edit"][i-1], st.session_state["payroll_template_edit"][i]
                    st.rerun()
            
            with cols[4]:
                if st.button("🗑️", key=f"payroll_del_{i}", help="Delete field"):
                    del st.session_state["payroll_template_edit"][i]
                    st.rerun()
    
    # Add new field
    st.markdown("### ➕ Add New Payroll Field")
    new_cols = st.columns([3, 3, 3, 1])
    
    with new_cols[0]:
        new_code = st.text_input("Field Code", key="new_payroll_field_code", placeholder="e.g., OVERTIME_RATE")
    with new_cols[1]:
        new_name = st.text_input("Display Name", key="new_payroll_field_name", placeholder="e.g., Overtime Rate")
    with new_cols[2]:
        new_desc = st.text_input("Description", key="new_payroll_field_desc", placeholder="e.g., Hourly rate for overtime work")
    with new_cols[3]:
        if st.button("➕ Add", help="Add this field to the payroll template", key="add_payroll_field"):
            if new_code and new_name:
                st.session_state["payroll_template_edit"].append({
                    "target_column": new_code,
                    "display_name": new_name,
                    "description": new_desc
                })
                st.success(f"Added {new_name}")
                st.rerun()
            else:
                st.error("Please fill in Field Code and Display Name")
    
    # Save template
    if st.button("💾 Save Payroll Template", type="primary"):
        # Validate
        errors = []
        for i, field in enumerate(st.session_state["payroll_template_edit"]):
            if not field.get('target_column'):
                errors.append(f"Field {i+1}: Missing Field Code")
            if not field.get('display_name'):
                errors.append(f"Field {i+1}: Missing Display Name")
        
        if errors:
            st.error("**Please fix these issues:**")
            for error in errors:
                st.write(f"• {error}")
        else:
            save_config_with_session_state("payroll_template", st.session_state["payroll_template_edit"])
            
            # Show preview of saved template
            st.subheader("✅ Saved Payroll Template Preview")
            template_df = pd.DataFrame(st.session_state["payroll_template_edit"])
            st.dataframe(template_df[['target_column', 'display_name', 'description']], use_container_width=True)

def configure_field_mappings():
    """Configure field mappings for payroll with simple explanations"""
    st.subheader("🔗 Payroll Field Mapping Configuration")
    st.info("**What this does:** Tell the system which fields from your PA files should go into which payroll data fields")
    
    # Load current mappings
    current_mappings = load_config_with_session_state("payroll_column_mappings") or []
    
    # Show current mappings
    if current_mappings:
        st.markdown("### 📋 Current Payroll Mappings")
        
        mapping_summary = []
        for mapping in current_mappings:
            mapping_summary.append({
                'Payroll Field': mapping.get('target_column', ''),
                'Source File': mapping.get('source_file', ''),
                'Source Field': mapping.get('source_column', ''),
                'Transformation': mapping.get('transformation', 'None')
            })
        
        if mapping_summary:
            mapping_df = pd.DataFrame(mapping_summary)
            st.dataframe(mapping_df, use_container_width=True)
            
            # Download current mappings
            csv_data = mapping_df.to_csv(index=False)
            st.download_button(
                "📥 Download Current Mappings",
                data=csv_data,
                file_name="payroll_field_mappings.csv",
                mime="text/csv"
            )
    
    # Add new mapping
    st.markdown("### ➕ Create New Payroll Field Mapping")
    st.write("**Instructions:** Choose a payroll field, select where the data comes from, and set any transformations needed.")
    
    cols = st.columns(2)
    
    with cols[0]:
        # Target field selection
        template = load_config("payroll_template") or get_default_payroll_template()
        target_options = [f"{field['target_column']} ({field['display_name']})" for field in template]
        
        if target_options:
            selected_target = st.selectbox(
                "1. Choose Payroll Field:",
                target_options,
                help="Which field in the final payroll file should this data go to?"
            )
            
            if selected_target:
                target_code = selected_target.split()[0]
                target_name = selected_target.split('(')[1].rstrip(')')
        else:
            st.error("❌ No payroll template configured. Set up the template first.")
            return
    
    with cols[1]:
        # Source file selection
        source_file = st.selectbox(
            "2. Choose Source File:",
            ["PA0008 (Wage Types)", "PA0014 (Recurring Elements)"],
            help="Which PA file contains the data you want to use?"
        )
        
        # Extract PA code
        source_code = source_file.split()[0]
    
    # Source field selection
    source_columns = get_payroll_source_columns(source_code)
    if source_columns:
        source_column = st.selectbox(
            "3. Choose Source Field:",
            [""] + source_columns,
            help="Which field in the source file contains the data?"
        )
    else:
        st.warning(f"⚠️ No sample file uploaded for {source_code}. Upload a sample first to see available fields.")
        source_column = st.text_input(
            "3. Enter Source Field Name:",
            help="Type the exact field name from your source file"
        )
    
    # Transformation selection
    transformation_options = get_simple_transformation_options()
    transformation = st.selectbox(
        "4. Choose Transformation:",
        list(transformation_options.keys()),
        format_func=lambda x: f"{x} - {transformation_options[x]}",
        help="How should the data be processed?"
    )
    
    # Default value
    default_value = st.text_input(
        "5. Default Value (Optional):",
        help="Value to use if the source field is empty"
    )
    
    # Add mapping button
    if st.button("➕ Add This Mapping", type="primary", key="add_payroll_mapping"):
        if not source_column and not default_value:
            st.error("❌ Please choose a source field OR enter a default value")
        else:
            new_mapping = {
                "target_column": target_code,
                "target_display": target_name,
                "source_file": source_code,
                "source_column": source_column,
                "transformation": transformation,
                "default_value": default_value
            }
            
            updated_mappings = current_mappings + [new_mapping]
            save_config_with_session_state("payroll_column_mappings", updated_mappings)
            st.success(f"✅ Added payroll mapping: {target_name} ← {source_code}:{source_column}")
            st.rerun()
    
    # Manage existing mappings
    if current_mappings:
        st.markdown("### 🗑️ Manage Existing Payroll Mappings")
        
        # Select mapping to delete
        mapping_options = [f"{m.get('target_column', '')} ← {m.get('source_file', '')}:{m.get('source_column', '')}" 
                          for m in current_mappings]
        
        selected_to_delete = st.selectbox(
            "Select payroll mapping to delete:",
            [""] + mapping_options,
            key="delete_payroll_mapping"
        )
        
        if selected_to_delete and st.button("🗑️ Delete Selected Mapping", key="delete_payroll_mapping_btn"):
            # Find and remove the selected mapping
            index_to_delete = mapping_options.index(selected_to_delete)
            del current_mappings[index_to_delete]
            save_config_with_session_state("payroll_column_mappings", current_mappings)
            st.success("✅ Payroll mapping deleted")
            st.rerun()

def quick_setup_wizard():
    """Quick setup wizard for payroll first-time users"""
    st.subheader("🚀 Quick Payroll Setup Wizard")
    st.info("**What this does:** Get your payroll data processing set up quickly with a step-by-step guide")
    
    # Check current setup status
    template = load_config("payroll_template")
    mappings = load_config("payroll_column_mappings")
    
    # Step indicators
    steps = [
        ("1. Payroll Template", template is not None, "Define output fields"),
        ("2. Sample Files", False, "Upload PA file samples"),  # We'll check this differently
        ("3. Field Mappings", mappings is not None and len(mappings) > 0, "Connect fields"),
        ("4. Test & Use", False, "Ready to process")
    ]
    
    # Check sample files
    sample_count = 0
    for pa_file in ['PA0008', 'PA0014']:
        sample_path = os.path.join(SOURCE_SAMPLES_DIR, f"{pa_file}_sample.csv")
        if os.path.exists(sample_path):
            sample_count += 1
    steps[1] = ("2. Sample Files", sample_count >= 2, f"Upload PA file samples ({sample_count}/2 uploaded)")
    
    # Final step
    all_ready = all(step[1] for step in steps[:3])
    steps[3] = ("4. Test & Use", all_ready, "Ready to process" if all_ready else "Complete steps 1-3")
    
    # Show progress
    st.markdown("### 📊 Setup Progress")
    
    for step_name, completed, description in steps:
        if completed:
            st.success(f"✅ {step_name}: {description}")
        else:
            st.error(f"❌ {step_name}: {description}")
    
    # Calculate progress
    completed_steps = sum(1 for _, completed, _ in steps if completed)
    progress = completed_steps / len(steps)
    st.progress(progress)
    st.caption(f"Setup is {progress*100:.0f}% complete ({completed_steps}/{len(steps)} steps)")
    
    # Next step recommendation
    st.markdown("### 👉 What to do next:")
    
    if not template:
        st.info("**Start with Step 1:** Set up your payroll template to define what fields you want in the final file")
        if st.button("📋 Go to Payroll Template Setup"):
            st.session_state.payroll_admin_tab = "Payroll Template"
            st.rerun()
    elif sample_count < 2:
        st.info("**Continue with Step 2:** Upload sample files (need both PA0008 and PA0014)")
        if st.button("📂 Go to Sample File Upload"):
            st.session_state.payroll_admin_tab = "Sample Files"
            st.rerun()
    elif not mappings or len(mappings) == 0:
        st.info("**Continue with Step 3:** Create field mappings to connect your PA files to payroll fields")
        if st.button("🔗 Go to Field Mapping"):
            st.session_state.payroll_admin_tab = "Field Mapping"
            st.rerun()
    else:
        st.success("🎉 **Setup Complete!** You're ready to process payroll data")
        st.info("**What to do now:** Go to the Payroll panel and upload your full PA files to start processing")
        
        # Show summary of what's configured
        st.markdown("### ✅ Configuration Summary")
        st.write(f"• **Payroll Template:** {len(template)} fields configured")
        st.write(f"• **Sample Files:** {sample_count}/2 files uploaded")
        st.write(f"• **Field Mappings:** {len(mappings)} mappings created")

def show_payroll_admin_panel():
    """Main payroll admin panel with clean, simple interface"""
    
    # Clean header
    st.markdown("""
    <div style="background: linear-gradient(90deg, #16a085 0%, #27ae60 100%); 
                color: white; padding: 2rem; border-radius: 10px; margin-bottom: 2rem;">
        <h1 style="margin: 0; font-size: 2.5rem;">Payroll Configuration Center</h1>
        <p style="margin: 0.5rem 0 0 0; font-size: 1.2rem; opacity: 0.9;">
            Set up how your PA files should be converted to payroll data
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize directories
    initialize_directories()
    
    # Configuration status at top
    show_configuration_status()
    
    st.markdown("---")
    
    # Main tabs
    tabs = st.tabs([
        "🚀 Quick Setup",
        "📂 Sample Files", 
        "📋 Payroll Template",
        "🔗 Field Mapping"
    ])
    
    with tabs[0]:
        quick_setup_wizard()
    
    with tabs[1]:
        upload_sample_files()
    
    with tabs[2]:
        configure_payroll_template()
    
    with tabs[3]:
        configure_field_mappings()
    
    # Help section
    st.markdown("---")
    with st.expander("❓ Need Help with Payroll Configuration?", expanded=False):
        st.markdown("""
        **Payroll Configuration Overview:**
        
        📋 **Payroll Template:** Defines what fields you want in your final payroll file (payroll.csv)
        📂 **Sample Files:** Small samples of your PA files so we can see what payroll data is available
        🔗 **Field Mapping:** Connects fields from your PA files to fields in the payroll template
        
        **Setup Order:**
        1. **Upload Sample Files** - Upload PA0008 and PA0014 files
        2. **Configure Template** - Define what fields you want in the output
        3. **Create Mappings** - Connect PA file fields to payroll template fields
        4. **Test Processing** - Go to Payroll panel to test with real data
        
        **Common Questions:**
        
        **Q: Which PA files do I need for payroll?**
        A: PA0008 (Wage Types) and PA0014 (Recurring Elements) are both required for complete payroll processing.
        
        **Q: What's the difference between sample files and real files?**
        A: Sample files are small portions used for configuration. Real files are your full payroll data used for processing.
        
        **Q: How do payroll transformations work?**
        A: Transformations format data appropriately (e.g., "123.456" → "$123.46" with Currency Format).
        
        **Q: What if I make a mistake in payroll configuration?**
        A: You can always come back and change mappings, add/remove fields, or reset to defaults.
        
        **Q: What are wage types vs recurring elements?**
        A: Wage types (PA0008) are payments like salary, bonuses, overtime. Recurring elements (PA0014) are regular deductions/benefits like taxes, insurance.
        """)
