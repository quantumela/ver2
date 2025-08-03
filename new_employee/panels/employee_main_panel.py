import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import re
import io
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
import traceback

# Performance optimization with caching
@st.cache_data(ttl=600)  # Cache for 10 minutes
def merge_pa_files_cached(pa0002_hash, pa0001_hash, pa0006_hash, pa0105_hash):
    """Cache merged PA files to avoid re-processing"""
    return None  # Placeholder for cache key

def is_dataframe_available(df):
    """Check if DataFrame is available and not empty"""
    return df is not None and isinstance(df, pd.DataFrame) and not df.empty


def get_or_create_merged_data(state):
    """Get merged data from cache or create it - OPTIMIZED"""
    
    # Check if we already have merged data in session state
    if 'merged_employee_data' in state:
        cached_data = state['merged_employee_data']
        if is_dataframe_available(cached_data):
            return cached_data
    
    # Get source files
    pa0002 = state.get('source_pa0002')
    pa0001 = state.get('source_pa0001') 
    pa0006 = state.get('source_pa0006')
    pa0105 = state.get('source_pa0105')
    
    if not is_dataframe_available(pa0002):
        return None
    
    with st.spinner("🔄 Merging PA files (one-time setup)..."):
        # Start with PA0002 as base
        merged_data = pa0002.copy()
        
        # Merge other files efficiently - FIXED CODE
        merge_stats = {'PA0002': len(merged_data)}
        
        # FIXED CODE - Only keep first record per employee to prevent duplicates:
        for file_key, file_df in [('PA0001', pa0001), ('PA0006', pa0006), ('PA0105', pa0105)]:
            if is_dataframe_available(file_df) and 'Pers.No.' in file_df.columns:
                # 🔧 FIX: Only keep first record per employee to prevent duplicates
                file_df_unique = file_df.drop_duplicates(subset=['Pers.No.'], keep='first')
                st.write(f"✅ Merged {file_key}: {len(file_df):,} records → {len(file_df_unique):,} unique employees")
                
                merged_data = merged_data.merge(
                    file_df_unique, 
                    on='Pers.No.', 
                    how='left', 
                    suffixes=('', f'_{file_key}')
                )
                
                merge_stats[file_key] = len(file_df_unique)  # Use unique count
        
        # Cache the merged data in session state
        state['merged_employee_data'] = merged_data
        state['merge_stats'] = merge_stats
        
        st.success(f"🎉 Merged data cached: {len(merged_data):,} employees ready for processing")
        
    return merged_data



def load_employee_mapping_configuration(state):
    """Load employee mapping configuration with simple fallback"""
    try:
        if 'employee_mapping_config' in st.session_state:
            config = st.session_state['employee_mapping_config']
            if is_dataframe_available(config):
                return config
            elif isinstance(config, list) and config:
                return pd.DataFrame(config)
        
        return create_default_employee_mapping()
        
    except Exception as e:
        st.error(f"Error loading mapping: {str(e)}")
        return create_default_employee_mapping()

def create_default_employee_mapping():
    """Create default mapping for employee data"""
    default_mappings = [
        {
            'target_column': 'STATUS',
            'target_description': 'Employment Status',
            'source_file': 'PA0002',
            'source_column': 'Employee status',
            'transformation': 'Status Mapping',
            'default_value': 'Active',
            'category': 'Work Info'
        },
        {
            'target_column': 'USERID',
            'target_description': 'Unique Employee ID',
            'source_file': 'PA0002',
            'source_column': 'Pers.No.',
            'transformation': 'None',
            'default_value': None,
            'category': 'Core Info'
        },
        {
            'target_column': 'USERNAME',
            'target_description': 'Employee Display Name',
            'source_file': 'PA0002',
            'source_column': 'First name',
            'transformation': 'Concatenate',
            'secondary_column': 'Last name',
            'default_value': None,
            'category': 'Core Info'
        },
        {
            'target_column': 'FIRSTNAME',
            'target_description': 'First Name',
            'source_file': 'PA0002',
            'source_column': 'First name',
            'transformation': 'Title Case',
            'default_value': None,
            'category': 'Core Info'
        },
        {
            'target_column': 'LASTNAME',
            'target_description': 'Last Name',
            'source_file': 'PA0002',
            'source_column': 'Last name',
            'transformation': 'Title Case',
            'default_value': None,
            'category': 'Core Info'
        },
        {
            'target_column': 'EMAIL',
            'target_description': 'Email Address',
            'source_file': 'PA0105',
            'source_column': 'Communication',
            'transformation': 'lowercase',
            'default_value': None,
            'category': 'Contact Info'
        },
        {
            'target_column': 'DEPARTMENT',
            'target_description': 'Department',
            'source_file': 'PA0001',
            'source_column': 'Organizational unit',
            'transformation': 'Title Case',
            'default_value': 'General',
            'category': 'Work Info'
        },
        {
            'target_column': 'HIREDATE',
            'target_description': 'Hire Date',
            'source_file': 'PA0001',
            'source_column': 'Start date',
            'transformation': 'Date Format (YYYY-MM-DD)',
            'default_value': None,
            'category': 'Work Info'
        },
        {
            'target_column': 'BIZ_PHONE',
            'target_description': 'Business Phone',
            'source_file': 'PA0105',
            'source_column': 'Communication',
            'transformation': 'None',
            'default_value': None,
            'category': 'Contact Info'
        },
        {
            'target_column': 'MANAGER',
            'target_description': 'Manager',
            'source_file': 'PA0001',
            'source_column': 'Name of superior (OM)',
            'transformation': 'Title Case',
            'default_value': 'NO_MANAGER',
            'category': 'Work Info'
        }
    ]
    
    return pd.DataFrame(default_mappings)

def apply_employee_transformation(value, transformation, mapping_config=None, source_row=None, source_df=None):
    """Apply transformations to employee data"""
    if pd.isna(value) or value is None:
        if transformation != 'Concatenate':
            return value
    
    value_str = str(value) if not pd.isna(value) else ""
    
    if transformation == 'Title Case':
        return value_str.title()
    elif transformation == 'UPPERCASE':
        return value_str.upper()
    elif transformation == 'lowercase':
        return value_str.lower()
    elif transformation == 'Trim Whitespace':
        return value_str.strip()
    elif transformation == 'Concatenate':
        if mapping_config and 'secondary_column' in mapping_config and source_row is not None:
            secondary_column = mapping_config['secondary_column']
            if secondary_column and secondary_column in source_row.index:
                secondary_value = source_row[secondary_column]
                secondary_str = str(secondary_value) if not pd.isna(secondary_value) else ""
                
                if value_str and secondary_str:
                    return f"{value_str} {secondary_str}"
                elif value_str:
                    return value_str
                elif secondary_str:
                    return secondary_str
        return value_str
    elif transformation == 'Date Format (YYYY-MM-DD)':
        try:
            if '.' in value_str:  # German format dd.mm.yyyy
                parts = value_str.split('.')
                if len(parts) == 3:
                    day, month, year = parts
                    return f"{year.zfill(4)}-{month.zfill(2)}-{day.zfill(2)}"
            elif '/' in value_str:  # US format mm/dd/yyyy
                date_obj = pd.to_datetime(value_str, errors='coerce')
                if not pd.isna(date_obj):
                    return date_obj.strftime('%Y-%m-%d')
            return value_str
        except:
            return value_str
    elif transformation == 'Status Mapping':
        status_map = {'1': 'Active', '2': 'Inactive', '3': 'Pending', '0': 'Terminated'}
        return status_map.get(str(value), mapping_config.get('default_value', 'Active'))
    else:
        return value

def create_employee_output_dataframe_optimized(merged_data, mappings, max_rows=None):
    """Create employee output DataFrame - OPTIMIZED with row limiting"""
    
    if not is_dataframe_available(mappings) or not is_dataframe_available(merged_data):
        return pd.DataFrame()
    
    # For preview, only process the first N rows
    if max_rows:
        process_data = merged_data.head(max_rows)
        st.info(f"⚡ Processing first {max_rows} employees for preview (faster)")
    else:
        process_data = merged_data
    
    # Create output data structure
    output_data = []
    
    # Standard employee fields
    target_columns = [
        'STATUS', 'USERID', 'USERNAME', 'FIRSTNAME', 'LASTNAME', 
        'EMAIL', 'DEPARTMENT', 'HIREDATE', 'BIZ_PHONE', 'MANAGER'
    ]
    
    # Process each employee record
    for _, source_row in process_data.iterrows():
        employee_record = {}
        
        # Apply mappings for each target column
        for target_col in target_columns:
            mapping = mappings[mappings['target_column'] == target_col]
            
            if not mapping.empty:
                mapping_row = mapping.iloc[0]
                source_column = mapping_row.get('source_column')
                transformation = mapping_row.get('transformation', 'None')
                default_value = mapping_row.get('default_value')
                
                # Get value from source
                value = None
                if source_column and source_column in source_row.index:
                    value = source_row[source_column]
                elif default_value:
                    value = default_value
                
                # Apply transformation
                if transformation and transformation != 'None':
                    mapping_dict = mapping_row.to_dict()
                    value = apply_employee_transformation(value, transformation, mapping_dict, source_row, process_data)
                
                # Handle default values
                if (pd.isna(value) or value is None or value == '') and default_value:
                    value = default_value
                
                # Clean data
                if pd.isna(value) or value is None:
                    value = ""
                else:
                    value = str(value)
                
                employee_record[target_col] = value
            else:
                employee_record[target_col] = ""
        
        output_data.append(employee_record)
    
    # Create DataFrame
    output_df = pd.DataFrame(output_data)
    
    # Ensure all target columns exist
    for col in target_columns:
        if col not in output_df.columns:
            output_df[col] = ""
    
    return output_df[target_columns]

def generate_fast_preview(state, preview_rows=10):
    """Generate fast preview by processing only first N employees"""
    
    try:
        # Get or create merged data (cached)
        merged_data = get_or_create_merged_data(state)
        if merged_data is None:
            return None, "No merged data available"
        
        # Load mapping configuration
        mapping_config = load_employee_mapping_configuration(state)
        
        # Process only preview_rows * 2 to account for potential filtering
        preview_multiplier = max(2, preview_rows * 2)
        
        # Create preview output (only process what we need)
        preview_df = create_employee_output_dataframe_optimized(
            merged_data, 
            mapping_config, 
            max_rows=preview_multiplier
        )
        
        if is_dataframe_available(preview_df):
            # Return just the requested number of rows
            return preview_df.head(preview_rows), f"preview_{preview_rows}_rows"
        else:
            return None, "Failed to create preview"
            
    except Exception as e:
        st.error(f"Preview error: {str(e)}")
        return None, f"Error: {str(e)}"

def process_employee_files_full(state):
    """Process ALL employee files for final generation"""
    try:
        # Get or create merged data (cached)
        merged_data = get_or_create_merged_data(state)
        if merged_data is None:
            return None, "No merged data available"
        
        # Load mapping configuration
        mapping_config = load_employee_mapping_configuration(state)
        
        # Process ALL employees for final output
        output_df = create_employee_output_dataframe_optimized(merged_data, mapping_config)
        
        if not is_dataframe_available(output_df):
            return None, "Failed to create employee output"
        
        # Generate filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"emp_{timestamp}.csv"
        
        return output_df, filename
        
    except Exception as e:
        st.error(f"Processing error: {str(e)}")
        return None, f"Error: {str(e)}"

def clear_cached_data(state):
    """Clear cached data to free memory"""
    keys_to_clear = ['merged_employee_data', 'merge_stats']
    cleared_count = 0
    
    for key in keys_to_clear:
        if key in state:
            del state[key]
            cleared_count += 1
    
    return cleared_count

def show_enhanced_preview(df, max_rows=10):
    """Show enhanced preview with all columns visible"""
    if not is_dataframe_available(df):
        st.error("No data available for preview")
        return
    
    st.success(f"⚡ **Fast Preview Generated** - {len(df)} employees processed in seconds")
    
    # Show dimensions
    st.info(f"**Preview:** {len(df)} employees × {len(df.columns)} fields")
    
    # Display ALL columns in preview
    st.dataframe(
        df, 
        use_container_width=True,
        height=400
    )
    
    # Show column completion stats
    with st.expander("📊 Field Completion Summary", expanded=True):
        completion_data = []
        for col in df.columns:
            non_empty = df[col].notna().sum()
            completion_pct = (non_empty / len(df)) * 100
            completion_data.append({
                'Field': col,
                'Completed': f"{completion_pct:.1f}%",
                'Sample Value': str(df[col].dropna().iloc[0]) if non_empty > 0 else 'Empty'
            })
        
        completion_df = pd.DataFrame(completion_data)
        st.dataframe(completion_df, use_container_width=True)

def show_employee_panel(state):
    """OPTIMIZED employee panel with fast preview, caching, and complete upload functionality"""
    
    # Header
    st.markdown("""
    <div style="background: linear-gradient(90deg, #1e40af 0%, #3b82f6 100%); 
                color: white; padding: 2rem; border-radius: 10px; margin-bottom: 2rem;">
        <h1 style="margin: 0; font-size: 2.5rem;">Employee Data Processing</h1>
        <p style="margin: 0.5rem 0 0 0; font-size: 1.2rem; opacity: 0.9;">
            ⚡ Optimized for fast processing with smart caching
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Performance info
    if 'merged_employee_data' in state:
        merged_data = state['merged_employee_data']
        st.success(f"🚀 **Data cached in memory:** {len(merged_data):,} employees ready for instant processing")
    
    # Check available data
    pa_files = {}
    for file_key in ['PA0001', 'PA0002', 'PA0006', 'PA0105']:
        pa_files[file_key] = state.get(f'source_{file_key.lower()}')
    
    # File status
    st.subheader("📂 Data Upload Status")
    
    file_info = {
        'PA0002': {'name': 'Personal Data', 'desc': 'Names, IDs, birth dates', 'required': True},
        'PA0001': {'name': 'Work Info', 'desc': 'Jobs, departments, hire dates', 'required': True}, 
        'PA0006': {'name': 'Addresses', 'desc': 'Employee addresses', 'required': False},
        'PA0105': {'name': 'Contact Info', 'desc': 'Emails and phone numbers', 'required': False}
    }
    
    # Status grid
    cols = st.columns(4)
    files_ready = 0
    required_ready = 0
    
    for i, (file_key, info) in enumerate(file_info.items()):
        with cols[i]:
            if is_dataframe_available(pa_files[file_key]):
                st.success(f"✅ **{file_key}**")
                st.write(f"**{info['name']}**")
                st.caption(f"{len(pa_files[file_key]):,} records")
                files_ready += 1
                if info['required']:
                    required_ready += 1
            else:
                status = "❌ Required" if info['required'] else "⚪ Optional"
                color = "error" if info['required'] else "info"
                getattr(st, color)(f"{status} **{file_key}**")
                st.write(f"**{info['name']}**")
                st.caption(info['desc'])
    
    # If files missing, show upload section
    if required_ready < 2:
        st.markdown("---")
        st.subheader("📤 Upload Your Files")
        st.error("**Missing Required Files:** You need PA0002 (Personal Data) and PA0001 (Work Info) to continue")
        
        st.info("**Upload all your PA files at once:**")
        
        uploaded_files = st.file_uploader(
            "Select your PA files (the system will automatically detect which is which)",
            type=['xlsx', 'xls', 'csv'],
            accept_multiple_files=True,
            help="Upload all your PA files together",
            key="bulk_pa_upload"
        )
        
        if uploaded_files:
            st.write(f"**Files selected:** {len(uploaded_files)}")
            
            # Auto-detect files
            detected = {}
            for file in uploaded_files:
                name_upper = file.name.upper()
                for pa_key in ['PA0001', 'PA0002', 'PA0006', 'PA0105']:
                    if pa_key in name_upper:
                        detected[pa_key] = file.name
                        break
            
            if detected:
                st.success("**Auto-detected files:**")
                for pa_key, filename in detected.items():
                    st.write(f"• {pa_key}: {filename}")
                
                missing_required = [key for key in ['PA0001', 'PA0002'] if key not in detected]
                if missing_required:
                    st.warning(f"**Still missing:** {', '.join(missing_required)}")
                
                if st.button("🚀 Process All Files", type="primary", key="process_files"):
                    with st.spinner("Processing your files..."):
                        success_count = 0
                        
                        for file in uploaded_files:
                            try:
                                # Determine file type
                                name_upper = file.name.upper()
                                file_key = None
                                for pa_key in ['PA0001', 'PA0002', 'PA0006', 'PA0105']:
                                    if pa_key in name_upper:
                                        file_key = pa_key
                                        break
                                
                                if not file_key:
                                    continue
                                
                                # Read file
                                if file.name.endswith('.csv'):
                                    df = pd.read_csv(file)
                                else:
                                    df = pd.read_excel(file)
                                
                                # Basic validation
                                if file_key in ['PA0002', 'PA0001'] and 'Pers.No.' not in df.columns:
                                    st.error(f"❌ {file_key} must have 'Pers.No.' column")
                                    continue
                                
                                # Save to state
                                state[f'source_{file_key.lower()}'] = df
                                st.success(f"✅ {file_key}: {len(df):,} records processed")
                                success_count += 1
                                
                            except Exception as e:
                                st.error(f"❌ Error with {file.name}: {str(e)}")
                        
                        if success_count > 0:
                            st.success(f"🎉 Successfully processed {success_count} files!")
                            st.balloons()
                            st.rerun()
            else:
                st.error("❌ No PA files detected. Make sure filenames contain PA0001, PA0002, etc.")
        
        # Quick reset option
        with st.expander("🔄 Reset Data", expanded=False):
            if st.button("Clear All Data", key="clear_data"):
                for file_key in ['PA0001', 'PA0002', 'PA0006', 'PA0105']:
                    if f'source_{file_key.lower()}' in state:
                        del state[f'source_{file_key.lower()}']
                if 'generated_employee_files' in state:
                    del state['generated_employee_files']
                # Clear cached data too
                clear_cached_data(state)
                st.success("All data cleared!")
                st.rerun()
        
        return  # Don't show the rest until files are uploaded
    
    # Performance management
    st.markdown("---")
    st.subheader("⚡ Performance Controls")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Merge & Cache Data", help="Prepare data for fast processing"):
            merged_data = get_or_create_merged_data(state)
            if merged_data is not None:
                st.balloons()
    
    with col2:
        if st.button("🧹 Clear Cache", help="Free up memory"):
            cleared = clear_cached_data(state)
            if cleared > 0:
                st.success(f"Cleared {cleared} cached items")
            else:
                st.info("No cached data to clear")
    
    with col3:
        cache_info = "🟢 Cached" if 'merged_employee_data' in state else "🔴 Not Cached"
        st.info(f"**Status:** {cache_info}")
    
    # Fast preview section - FIXED LAYOUT
    st.markdown("---")
    st.subheader("⚡ Super Fast Preview")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        preview_size = st.selectbox(
            "Preview size:",
            [5, 10, 25, 50],
            index=1,
            help="Larger previews take slightly longer"
        )
    
    with col2:
        generate_preview = st.button("🚀 Generate Fast Preview", type="primary", key="fast_preview")
    
    # FIXED: Display preview results outside the column layout to use full page width
    if generate_preview:
        start_time = datetime.now()
        
        preview_df, result = generate_fast_preview(state, preview_size)
        
        end_time = datetime.now()
        processing_time = (end_time - start_time).total_seconds()
        
        if is_dataframe_available(preview_df):
            st.success(f"⚡ **Generated in {processing_time:.1f} seconds!**")
            # Preview now displays in full width
            show_enhanced_preview(preview_df, preview_size)
        else:
            st.error(f"Preview failed: {result}")
    
    # Full file generation
    st.markdown("---")
    st.subheader("🎯 Generate Complete Employee File")
    
    existing_files = state.get('generated_employee_files')
    if existing_files and 'employee_data' in existing_files:
        file_data = existing_files['employee_data']
        filename = existing_files.get('filename', 'emp.csv')
        
        st.success("✅ **Employee file already generated!**")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.info(f"**{filename}** - {len(file_data):,} employees with {len(file_data.columns)} fields")
            st.caption(f"**Columns:** {', '.join(file_data.columns)}")
        
        with col2:
            csv_data = file_data.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv_data,
                file_name=filename,
                mime="text/csv",
                key="download_employee_file",
                type="primary"
            )
        
        if st.button("🔄 Generate New File", help="Create fresh employee file"):
            if 'generated_employee_files' in state:
                del state['generated_employee_files']
            st.rerun()
    
    else:
        st.info("**Generate your complete emp.csv file with all employees**")
        
        if st.button("🚀 Generate Full Employee File", type="primary", key="generate_full"):
            start_time = datetime.now()
            
            with st.spinner("Processing all employees..."):
                output_df, filename = process_employee_files_full(state)
            
            end_time = datetime.now()
            processing_time = (end_time - start_time).total_seconds()
            
            if is_dataframe_available(output_df):
                st.success(f"✅ **Generated {filename} in {processing_time:.1f} seconds!**")
                
                # Store in session state
                state['generated_employee_files'] = {
                    'employee_data': output_df,
                    'filename': filename
                }
                
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.info(f"**{filename}** - {len(output_df):,} employees with {len(output_df.columns)} fields")
                    st.caption(f"**Columns:** {', '.join(output_df.columns)}")
                
                with col2:
                    csv_data = output_df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download CSV",
                        data=csv_data,
                        file_name=filename,
                        mime="text/csv",
                        key="download_new_employee",
                        type="primary"
                    )
            else:
                st.error(f"Generation failed: {filename}")
    
    # Performance tips
    with st.expander("⚡ Performance Tips", expanded=False):
        st.markdown("""
        **How the optimization works:**
        
        🚀 **Smart Caching:** Your PA files are merged once and stored in memory
        ⚡ **Fast Preview:** Only processes 10-50 employees instead of all 13,000+
        📊 **Lazy Loading:** Full processing only happens when you need the complete file
        🧹 **Memory Management:** Clear cache when done to free up memory
        
        **Performance expectations:**
        - **Fast Preview:** 1-3 seconds (processes ~50 employees)
        - **Full Generation:** 10-30 seconds (processes all 13,000+ employees)
        - **Caching:** First merge takes a few seconds, then instant
        
        **Best practices:**
        1. Click "Merge & Cache Data" first
        2. Use Fast Preview to test your setup
        3. Generate full file only when ready
        4. Clear cache when switching projects
        """)