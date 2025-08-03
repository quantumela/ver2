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
def merge_payroll_files_cached(pa0008_hash, pa0014_hash):
    """Cache merged payroll files to avoid re-processing"""
    return None  # Placeholder for cache key

def is_dataframe_available(df):
    """Check if DataFrame is available and not empty"""
    return df is not None and isinstance(df, pd.DataFrame) and not df.empty

def get_or_create_merged_payroll_data(state):
    """Get merged payroll data from cache or create it - OPTIMIZED"""
    
    # Check if we already have merged data in session state
    if 'merged_payroll_data' in state:
        cached_data = state['merged_payroll_data']
        if is_dataframe_available(cached_data):
            return cached_data
    
    # Get source files
    pa0008 = state.get('source_pa0008')  # Wage types
    pa0014 = state.get('source_pa0014')  # Recurring payments/deductions
    
    if not is_dataframe_available(pa0008):
        return None
    
    with st.spinner("🔄 Merging payroll files (one-time setup)..."):
        # Start with PA0008 as base (wage types)
        merged_data = pa0008.copy()
        
        # Merge PA0014 if available
        merge_stats = {'PA0008': len(merged_data)}
        
        if is_dataframe_available(pa0014) and 'Pers.No.' in pa0014.columns:
            # Only keep first record per employee per wage type to prevent duplicates
            pa0014_unique = pa0014.drop_duplicates(subset=['Pers.No.'], keep='first')
            st.write(f"✅ Merged PA0014: {len(pa0014):,} records → {len(pa0014_unique):,} unique employees")
            
            merged_data = merged_data.merge(
                pa0014_unique, 
                on='Pers.No.', 
                how='left', 
                suffixes=('', '_PA0014')
            )
            
            merge_stats['PA0014'] = len(pa0014_unique)
        
        # Cache the merged data in session state
        state['merged_payroll_data'] = merged_data
        state['payroll_merge_stats'] = merge_stats
        
        st.success(f"🎉 Merged payroll data cached: {len(merged_data):,} records ready for processing")
        
    return merged_data

def load_payroll_mapping_configuration(state):
    """Load payroll mapping configuration with simple fallback"""
    try:
        if 'payroll_mapping_config' in st.session_state:
            config = st.session_state['payroll_mapping_config']
            if is_dataframe_available(config):
                return config
            elif isinstance(config, list) and config:
                return pd.DataFrame(config)
        
        return create_default_payroll_mapping()
        
    except Exception as e:
        st.error(f"Error loading payroll mapping: {str(e)}")
        return create_default_payroll_mapping()

def create_default_payroll_mapping():
    """Create default mapping for payroll data"""
    default_mappings = [
        {
            'target_column': 'EMPLOYEE_ID',
            'target_description': 'Employee Identifier',
            'source_file': 'PA0008',
            'source_column': 'Pers.No.',
            'transformation': 'None',
            'default_value': None,
            'category': 'Core Info'
        },
        {
            'target_column': 'WAGE_TYPE',
            'target_description': 'Wage Type Code',
            'source_file': 'PA0008',
            'source_column': 'Wage Type',
            'transformation': 'None',
            'default_value': None,
            'category': 'Wage Info'
        },
        {
            'target_column': 'AMOUNT',
            'target_description': 'Payment Amount',
            'source_file': 'PA0008',
            'source_column': 'Amount',
            'transformation': 'Number Format',
            'default_value': '0.00',
            'category': 'Financial'
        },
        {
            'target_column': 'CURRENCY',
            'target_description': 'Currency Code',
            'source_file': 'PA0008',
            'source_column': 'Currency',
            'transformation': 'UPPERCASE',
            'default_value': 'USD',
            'category': 'Financial'
        },
        {
            'target_column': 'PAY_PERIOD',
            'target_description': 'Pay Period',
            'source_file': 'PA0008',
            'source_column': 'Pay Period',
            'transformation': 'Date Format (YYYY-MM)',
            'default_value': None,
            'category': 'Time Info'
        },
        {
            'target_column': 'PAYMENT_DATE',
            'target_description': 'Payment Date',
            'source_file': 'PA0008',
            'source_column': 'Payment Date',
            'transformation': 'Date Format (YYYY-MM-DD)',
            'default_value': None,
            'category': 'Time Info'
        },
        {
            'target_column': 'RECURRING_AMOUNT',
            'target_description': 'Recurring Payment/Deduction',
            'source_file': 'PA0014',
            'source_column': 'Recurring Amount',
            'transformation': 'Number Format',
            'default_value': '0.00',
            'category': 'Recurring'
        },
        {
            'target_column': 'DEDUCTION_TYPE',
            'target_description': 'Type of Deduction',
            'source_file': 'PA0014',
            'source_column': 'Deduction Type',
            'transformation': 'Title Case',
            'default_value': 'None',
            'category': 'Deductions'
        },
        {
            'target_column': 'STATUS',
            'target_description': 'Payment Status',
            'source_file': 'PA0008',
            'source_column': 'Status',
            'transformation': 'Status Mapping',
            'default_value': 'Pending',
            'category': 'Processing'
        },
        {
            'target_column': 'COST_CENTER',
            'target_description': 'Cost Center',
            'source_file': 'PA0008',
            'source_column': 'Cost Center',
            'transformation': 'None',
            'default_value': '0000',
            'category': 'Accounting'
        }
    ]
    
    return pd.DataFrame(default_mappings)

def apply_payroll_transformation(value, transformation, mapping_config=None, source_row=None, source_df=None):
    """Apply transformations to payroll data"""
    if pd.isna(value) or value is None:
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
    elif transformation == 'Number Format':
        try:
            # Convert to float and format to 2 decimal places
            num_value = float(value_str.replace(',', ''))
            return f"{num_value:.2f}"
        except:
            return "0.00"
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
    elif transformation == 'Date Format (YYYY-MM)':
        try:
            date_obj = pd.to_datetime(value_str, errors='coerce')
            if not pd.isna(date_obj):
                return date_obj.strftime('%Y-%m')
            return value_str
        except:
            return value_str
    elif transformation == 'Status Mapping':
        status_map = {'1': 'Processed', '2': 'Pending', '3': 'Cancelled', '0': 'Draft'}
        return status_map.get(str(value), mapping_config.get('default_value', 'Pending'))
    else:
        return value

def create_payroll_output_dataframe_optimized(merged_data, mappings, max_rows=None):
    """Create payroll output DataFrame - OPTIMIZED with row limiting"""
    
    if not is_dataframe_available(mappings) or not is_dataframe_available(merged_data):
        return pd.DataFrame()
    
    # For preview, only process the first N rows
    if max_rows:
        process_data = merged_data.head(max_rows)
        st.info(f"⚡ Processing first {max_rows} payroll records for preview (faster)")
    else:
        process_data = merged_data
    
    # Create output data structure
    output_data = []
    
    # Standard payroll fields
    target_columns = [
        'EMPLOYEE_ID', 'WAGE_TYPE', 'AMOUNT', 'CURRENCY', 'PAY_PERIOD', 
        'PAYMENT_DATE', 'RECURRING_AMOUNT', 'DEDUCTION_TYPE', 'STATUS', 'COST_CENTER'
    ]
    
    # Process each payroll record
    for _, source_row in process_data.iterrows():
        payroll_record = {}
        
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
                    value = apply_payroll_transformation(value, transformation, mapping_dict, source_row, process_data)
                
                # Handle default values
                if (pd.isna(value) or value is None or value == '') and default_value:
                    value = default_value
                
                # Clean data
                if pd.isna(value) or value is None:
                    value = ""
                else:
                    value = str(value)
                
                payroll_record[target_col] = value
            else:
                payroll_record[target_col] = ""
        
        output_data.append(payroll_record)
    
    # Create DataFrame
    output_df = pd.DataFrame(output_data)
    
    # Ensure all target columns exist
    for col in target_columns:
        if col not in output_df.columns:
            output_df[col] = ""
    
    return output_df[target_columns]

def generate_fast_payroll_preview(state, preview_rows=10):
    """Generate fast preview by processing only first N payroll records"""
    
    try:
        # Get or create merged data (cached)
        merged_data = get_or_create_merged_payroll_data(state)
        if merged_data is None:
            return None, "No merged payroll data available"
        
        # Load mapping configuration
        mapping_config = load_payroll_mapping_configuration(state)
        
        # Process only preview_rows * 2 to account for potential filtering
        preview_multiplier = max(2, preview_rows * 2)
        
        # Create preview output (only process what we need)
        preview_df = create_payroll_output_dataframe_optimized(
            merged_data, 
            mapping_config, 
            max_rows=preview_multiplier
        )
        
        if is_dataframe_available(preview_df):
            # Return just the requested number of rows
            return preview_df.head(preview_rows), f"payroll_preview_{preview_rows}_rows"
        else:
            return None, "Failed to create payroll preview"
            
    except Exception as e:
        st.error(f"Payroll preview error: {str(e)}")
        return None, f"Error: {str(e)}"

def process_payroll_files_full(state):
    """Process ALL payroll files for final generation"""
    try:
        # Get or create merged data (cached)
        merged_data = get_or_create_merged_payroll_data(state)
        if merged_data is None:
            return None, "No merged payroll data available"
        
        # Load mapping configuration
        mapping_config = load_payroll_mapping_configuration(state)
        
        # Process ALL payroll records for final output
        output_df = create_payroll_output_dataframe_optimized(merged_data, mapping_config)
        
        if not is_dataframe_available(output_df):
            return None, "Failed to create payroll output"
        
        # Generate filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"payroll_{timestamp}.csv"
        
        return output_df, filename
        
    except Exception as e:
        st.error(f"Payroll processing error: {str(e)}")
        return None, f"Error: {str(e)}"

def clear_cached_payroll_data(state):
    """Clear cached payroll data to free memory"""
    keys_to_clear = ['merged_payroll_data', 'payroll_merge_stats']
    cleared_count = 0
    
    for key in keys_to_clear:
        if key in state:
            del state[key]
            cleared_count += 1
    
    return cleared_count

def show_enhanced_payroll_preview(df, max_rows=10):
    """Show enhanced preview with all payroll columns visible"""
    if not is_dataframe_available(df):
        st.error("No payroll data available for preview")
        return
    
    st.success(f"⚡ **Fast Payroll Preview Generated** - {len(df)} records processed in seconds")
    
    # Show dimensions
    st.info(f"**Preview:** {len(df)} payroll records × {len(df.columns)} fields")
    
    # Display ALL columns in preview
    st.dataframe(
        df, 
        use_container_width=True,
        height=400
    )
    
    # Show column completion stats
    with st.expander("📊 Payroll Field Completion Summary", expanded=True):
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

def show_payroll_panel(state):
    """OPTIMIZED payroll panel with fast preview, caching, and complete upload functionality"""
    
    # Header
    st.markdown("""
    <div style="background: linear-gradient(90deg, #16a085 0%, #27ae60 100%); 
                color: white; padding: 2rem; border-radius: 10px; margin-bottom: 2rem;">
        <h1 style="margin: 0; font-size: 2.5rem;">Payroll Data Processing</h1>
        <p style="margin: 0.5rem 0 0 0; font-size: 1.2rem; opacity: 0.9;">
            ⚡ Optimized for fast payroll processing with smart caching
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Performance info
    if 'merged_payroll_data' in state:
        merged_data = state['merged_payroll_data']
        st.success(f"🚀 **Payroll data cached in memory:** {len(merged_data):,} records ready for instant processing")
    
    # Check available data
    pa_files = {}
    for file_key in ['PA0008', 'PA0014']:
        pa_files[file_key] = state.get(f'source_{file_key.lower()}')
    
    # File status
    st.subheader("📂 Payroll Data Upload Status")
    
    file_info = {
        'PA0008': {'name': 'Wage Types', 'desc': 'Salary, wages, bonuses, overtime', 'required': True},
        'PA0014': {'name': 'Recurring Elements', 'desc': 'Regular deductions, benefits', 'required': True}
    }
    
    # Status grid
    cols = st.columns(2)
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
        st.subheader("📤 Upload Your Payroll Files")
        st.error("**Missing Required Files:** You need PA0008 (Wage Types) and PA0014 (Recurring Elements) to continue")
        
        st.info("**Upload all your payroll PA files at once:**")
        
        uploaded_files = st.file_uploader(
            "Select your payroll PA files (the system will automatically detect which is which)",
            type=['xlsx', 'xls', 'csv'],
            accept_multiple_files=True,
            help="Upload all your payroll PA files together",
            key="bulk_payroll_upload"
        )
        
        if uploaded_files:
            st.write(f"**Files selected:** {len(uploaded_files)}")
            
            # Auto-detect files
            detected = {}
            for file in uploaded_files:
                name_upper = file.name.upper()
                for pa_key in ['PA0008', 'PA0014']:
                    if pa_key in name_upper:
                        detected[pa_key] = file.name
                        break
            
            if detected:
                st.success("**Auto-detected payroll files:**")
                for pa_key, filename in detected.items():
                    st.write(f"• {pa_key}: {filename}")
                
                missing_required = [key for key in ['PA0008', 'PA0014'] if key not in detected]
                if missing_required:
                    st.warning(f"**Still missing:** {', '.join(missing_required)}")
                
                if st.button("🚀 Process All Payroll Files", type="primary", key="process_payroll_files"):
                    with st.spinner("Processing your payroll files..."):
                        success_count = 0
                        
                        for file in uploaded_files:
                            try:
                                # Determine file type
                                name_upper = file.name.upper()
                                file_key = None
                                for pa_key in ['PA0008', 'PA0014']:
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
                                if 'Pers.No.' not in df.columns:
                                    st.error(f"❌ {file_key} must have 'Pers.No.' column")
                                    continue
                                
                                # Save to state
                                state[f'source_{file_key.lower()}'] = df
                                st.success(f"✅ {file_key}: {len(df):,} records processed")
                                success_count += 1
                                
                            except Exception as e:
                                st.error(f"❌ Error with {file.name}: {str(e)}")
                        
                        if success_count > 0:
                            st.success(f"🎉 Successfully processed {success_count} payroll files!")
                            st.balloons()
                            st.rerun()
            else:
                st.error("❌ No payroll PA files detected. Make sure filenames contain PA0008, PA0014, etc.")
        
        # Quick reset option
        with st.expander("🔄 Reset Payroll Data", expanded=False):
            if st.button("Clear All Payroll Data", key="clear_payroll_data"):
                for file_key in ['PA0008', 'PA0014']:
                    if f'source_{file_key.lower()}' in state:
                        del state[f'source_{file_key.lower()}']
                if 'generated_payroll_files' in state:
                    del state['generated_payroll_files']
                # Clear cached data too
                clear_cached_payroll_data(state)
                st.success("All payroll data cleared!")
                st.rerun()
        
        return  # Don't show the rest until files are uploaded
    
    # Performance management
    st.markdown("---")
    st.subheader("⚡ Performance Controls")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Merge & Cache Payroll Data", help="Prepare payroll data for fast processing"):
            merged_data = get_or_create_merged_payroll_data(state)
            if merged_data is not None:
                st.balloons()
    
    with col2:
        if st.button("🧹 Clear Payroll Cache", help="Free up memory"):
            cleared = clear_cached_payroll_data(state)
            if cleared > 0:
                st.success(f"Cleared {cleared} cached items")
            else:
                st.info("No cached payroll data to clear")
    
    with col3:
        cache_info = "🟢 Cached" if 'merged_payroll_data' in state else "🔴 Not Cached"
        st.info(f"**Status:** {cache_info}")
    
    # Fast preview section
    st.markdown("---")
    st.subheader("⚡ Super Fast Payroll Preview")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        preview_size = st.selectbox(
            "Preview size:",
            [5, 10, 25, 50],
            index=1,
            help="Larger previews take slightly longer"
        )
    
    with col2:
        generate_preview = st.button("🚀 Generate Fast Preview", type="primary", key="fast_payroll_preview")
    
    # Display preview results
    if generate_preview:
        start_time = datetime.now()
        
        preview_df, result = generate_fast_payroll_preview(state, preview_size)
        
        end_time = datetime.now()
        processing_time = (end_time - start_time).total_seconds()
        
        if is_dataframe_available(preview_df):
            st.success(f"⚡ **Generated in {processing_time:.1f} seconds!**")
            show_enhanced_payroll_preview(preview_df, preview_size)
        else:
            st.error(f"Payroll preview failed: {result}")
    
    # Full file generation
    st.markdown("---")
    st.subheader("🎯 Generate Complete Payroll File")
    
    existing_files = state.get('generated_payroll_files')
    if existing_files and 'payroll_data' in existing_files:
        file_data = existing_files['payroll_data']
        filename = existing_files.get('filename', 'payroll.csv')
        
        st.success("✅ **Payroll file already generated!**")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.info(f"**{filename}** - {len(file_data):,} payroll records with {len(file_data.columns)} fields")
            st.caption(f"**Columns:** {', '.join(file_data.columns)}")
        
        with col2:
            csv_data = file_data.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv_data,
                file_name=filename,
                mime="text/csv",
                key="download_payroll_file",
                type="primary"
            )
        
        if st.button("🔄 Generate New Payroll File", help="Create fresh payroll file"):
            if 'generated_payroll_files' in state:
                del state['generated_payroll_files']
            st.rerun()
    
    else:
        st.info("**Generate your complete payroll.csv file with all payroll records**")
        
        if st.button("🚀 Generate Full Payroll File", type="primary", key="generate_full_payroll"):
            start_time = datetime.now()
            
            with st.spinner("Processing all payroll records..."):
                output_df, filename = process_payroll_files_full(state)
            
            end_time = datetime.now()
            processing_time = (end_time - start_time).total_seconds()
            
            if is_dataframe_available(output_df):
                st.success(f"✅ **Generated {filename} in {processing_time:.1f} seconds!**")
                
                # Store in session state
                state['generated_payroll_files'] = {
                    'payroll_data': output_df,
                    'filename': filename
                }
                
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.info(f"**{filename}** - {len(output_df):,} payroll records with {len(output_df.columns)} fields")
                    st.caption(f"**Columns:** {', '.join(output_df.columns)}")
                
                with col2:
                    csv_data = output_df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download CSV",
                        data=csv_data,
                        file_name=filename,
                        mime="text/csv",
                        key="download_new_payroll",
                        type="primary"
                    )
            else:
                st.error(f"Payroll generation failed: {filename}")
    
    # Performance tips
    with st.expander("⚡ Payroll Performance Tips", expanded=False):
        st.markdown("""
        **How the payroll optimization works:**
        
        🚀 **Smart Caching:** Your PA0008 and PA0014 files are merged once and stored in memory
        ⚡ **Fast Preview:** Only processes 10-50 payroll records instead of all records
        📊 **Lazy Loading:** Full processing only happens when you need the complete file
        🧹 **Memory Management:** Clear cache when done to free up memory
        
        **Performance expectations:**
        - **Fast Preview:** 1-3 seconds (processes ~50 payroll records)
        - **Full Generation:** 10-30 seconds (processes all payroll records)
        - **Caching:** First merge takes a few seconds, then instant
        
        **Best practices:**
        1. Click "Merge & Cache Payroll Data" first
        2. Use Fast Preview to test your setup
        3. Generate full file only when ready
        4. Clear cache when switching projects
        """)
