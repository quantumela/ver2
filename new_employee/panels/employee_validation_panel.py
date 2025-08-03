import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import re
from typing import Dict, List, Tuple, Any
from collections import defaultdict
import json
from io import BytesIO

def is_dataframe_available(df):
    """Check if DataFrame is available and not empty"""
    if df is None:
        return False
    if isinstance(df, pd.DataFrame):
        return not df.empty
    return False

def safe_get_dataframe(state, key):
    """Safely get DataFrame from state"""
    try:
        df = state.get(key)
        if df is None:
            return None
        if isinstance(df, pd.DataFrame) and not df.empty:
            return df
        return None
    except Exception as e:
        st.error(f"Error accessing {key}: {str(e)}")
        return None

@st.cache_data(ttl=300)  # Cache for 5 minutes
def validate_employee_data_pipeline_cached(pa0001_key, pa0002_key, pa0006_key, pa0105_key, output_key):
    """Cached version of validation to improve performance"""
    # This will be called by the main validation function
    pass

class EmployeeDataValidator:
    """Simple validator for employee data with clear explanations"""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.error_counts = defaultdict(int)
        self.data_transfer_tracking = {}
    
    def validate_employee_data_pipeline(self, state) -> Dict:
        """Validate employee data from source to output with transfer tracking"""
        
        self.errors = []
        self.warnings = []
        self.error_counts = defaultdict(int)
        self.data_transfer_tracking = {}
        
        validation_results = {
            'timestamp': datetime.now().isoformat(),
            'source_data_validated': False,
            'data_transfer_validated': False,
            'output_data_validated': False,
            'migration_ready': False,
            'data_transfer_stats': {}
        }
        
        # Get all data
        pa0001_df = safe_get_dataframe(state, 'source_pa0001')
        pa0002_df = safe_get_dataframe(state, 'source_pa0002')
        pa0006_df = safe_get_dataframe(state, 'source_pa0006')
        pa0105_df = safe_get_dataframe(state, 'source_pa0105')
        output_files = state.get('generated_employee_files', {})
        
        # 1. Validate source data
        if any([pa0001_df is not None, pa0002_df is not None, pa0006_df is not None, pa0105_df is not None]):
            self._validate_source_files(pa0001_df, pa0002_df, pa0006_df, pa0105_df)
            validation_results['source_data_validated'] = True
        
        # 2. Validate data transfer (how many records made it through)
        if pa0002_df is not None and output_files:
            transfer_stats = self._validate_data_transfer(pa0001_df, pa0002_df, pa0006_df, pa0105_df, output_files)
            validation_results['data_transfer_stats'] = transfer_stats
            validation_results['data_transfer_validated'] = True
        
        # 3. Validate output data
        if output_files:
            self._validate_output_data(output_files)
            validation_results['output_data_validated'] = True
        
        # Categorize results
        categorized_errors = self._categorize_errors()
        
        validation_results.update({
            'total_errors': len(self.errors),
            'total_warnings': len(self.warnings),
            'error_summary': dict(self.error_counts),
            'categorized_errors': categorized_errors,
            'all_errors': self.errors,
            'all_warnings': self.warnings,
            'migration_ready': len(self.errors) == 0,
            'critical_blockers': [e for e in self.errors if e['severity'] == 'CRITICAL']
        })
        
        return validation_results
    
    def _validate_source_files(self, pa0001_df, pa0002_df, pa0006_df, pa0105_df):
        """Validate source files with clear explanations"""
        
        # Check for required files
        if pa0002_df is None:
            self._add_error(
                'MISSING_PA0002',
                'CRITICAL',
                'PA0002 (Personal Data) file is missing',
                'This file contains employee names and IDs. Without it, we cannot process any employees.',
                'Upload your PA0002 file in the Employee panel',
                'PA0002',
                'File Missing'
            )
        else:
            # Check PA0002 structure
            self._validate_pa0002_structure(pa0002_df)
        
        if pa0001_df is None:
            self._add_error(
                'MISSING_PA0001',
                'CRITICAL',
                'PA0001 (Work Information) file is missing',
                'This file contains job titles, departments, and hire dates. Without it, employee work information will be incomplete.',
                'Upload your PA0001 file in the Employee panel',
                'PA0001',
                'File Missing'
            )
        else:
            # Check PA0001 structure
            self._validate_pa0001_structure(pa0001_df)
        
        # Check optional files
        if pa0006_df is None:
            self._add_warning(
                'MISSING_PA0006',
                'MEDIUM',
                'PA0006 (Address Data) file is missing',
                'Employee addresses will be empty in the output file',
                'Upload PA0006 if you need employee address information',
                'PA0006',
                'File Missing'
            )
        
        if pa0105_df is None:
            self._add_warning(
                'MISSING_PA0105',
                'MEDIUM',
                'PA0105 (Contact Info) file is missing',
                'Employee emails and phone numbers will be empty in the output file',
                'Upload PA0105 if you need employee contact information',
                'PA0105',
                'File Missing'
            )
        
        # Validate data consistency across files
        if pa0002_df is not None and pa0001_df is not None:
            self._validate_employee_consistency(pa0002_df, pa0001_df, pa0006_df, pa0105_df)
    
    def _validate_pa0002_structure(self, pa0002_df):
        """Validate PA0002 file structure"""
        
        required_columns = ['Pers.No.', 'First name', 'Last name']
        
        for col in required_columns:
            if col not in pa0002_df.columns:
                self._add_error(
                    'MISSING_REQUIRED_COLUMN',
                    'CRITICAL',
                    f'Missing required column: {col}',
                    f'PA0002 must have a "{col}" column for employee processing',
                    f'Add the "{col}" column to your PA0002 file',
                    'PA0002',
                    col
                )
        
        # Check for empty required columns
        if 'Pers.No.' in pa0002_df.columns:
            empty_ids = pa0002_df['Pers.No.'].isnull().sum()
            if empty_ids > 0:
                self._add_error(
                    'EMPTY_EMPLOYEE_IDS',
                    'CRITICAL',
                    f'{empty_ids} employees have empty IDs',
                    f'Found {empty_ids} rows where the employee ID (Pers.No.) is empty. These employees cannot be processed.',
                    'Fill in the missing employee IDs in your PA0002 file',
                    'PA0002',
                    'Pers.No.',
                    {'empty_count': empty_ids, 'total_rows': len(pa0002_df)}
                )
        
        # Check for duplicate employee IDs
        if 'Pers.No.' in pa0002_df.columns:
            duplicates = pa0002_df['Pers.No.'].duplicated().sum()
            if duplicates > 0:
                duplicate_ids = pa0002_df[pa0002_df['Pers.No.'].duplicated(keep=False)]['Pers.No.'].unique()
                self._add_error(
                    'DUPLICATE_EMPLOYEE_IDS',
                    'CRITICAL',
                    f'{duplicates} duplicate employee IDs found',
                    f'Found {len(duplicate_ids)} employee IDs that appear multiple times in PA0002. Each employee should have only one record.',
                    'Remove duplicate employee records from your PA0002 file',
                    'PA0002',
                    'Pers.No.',
                    {'duplicate_count': duplicates, 'duplicate_ids': duplicate_ids.tolist()[:10]}
                )
    
    def _validate_pa0001_structure(self, pa0001_df):
        """Validate PA0001 file structure"""
        
        if 'Pers.No.' not in pa0001_df.columns:
            self._add_error(
                'MISSING_EMPLOYEE_ID_COLUMN',
                'CRITICAL',
                'PA0001 missing employee ID column',
                'PA0001 must have a "Pers.No." column to link work information to employees',
                'Add the "Pers.No." column to your PA0001 file',
                'PA0001',
                'Pers.No.'
            )
    
    def _validate_employee_consistency(self, pa0002_df, pa0001_df, pa0006_df, pa0105_df):
        """Validate consistency of employee IDs across files"""
        
        if 'Pers.No.' not in pa0002_df.columns:
            return
        
        # Get employee IDs from main file
        main_employee_ids = set(pa0002_df['Pers.No.'].astype(str))
        
        # Check consistency with other files
        files_to_check = [
            ('PA0001', pa0001_df),
            ('PA0006', pa0006_df),
            ('PA0105', pa0105_df)
        ]
        
        for file_name, file_df in files_to_check:
            if file_df is not None and 'Pers.No.' in file_df.columns:
                file_employee_ids = set(file_df['Pers.No.'].astype(str))
                
                # Find employees in this file but not in main file
                orphaned_ids = file_employee_ids - main_employee_ids
                if orphaned_ids:
                    self._add_error(
                        f'ORPHANED_EMPLOYEES_{file_name}',
                        'HIGH',
                        f'{len(orphaned_ids)} employees in {file_name} not found in PA0002',
                        f'Found employee IDs in {file_name} that do not exist in PA0002. This data cannot be linked to employees.',
                        f'Either add these employees to PA0002 or remove them from {file_name}',
                        file_name,
                        'Pers.No.',
                        {'orphaned_count': len(orphaned_ids), 'orphaned_ids': list(orphaned_ids)[:10]}
                    )
    
    def _validate_data_transfer(self, pa0001_df, pa0002_df, pa0006_df, pa0105_df, output_files):
        """Track how many records transferred from source to output"""
        
        transfer_stats = {
            'source_employee_count': 0,
            'output_employee_count': 0,
            'employees_transferred': 0,
            'employees_lost': 0,
            'transfer_rate': 0.0,
            'source_file_stats': {},
            'data_loss_details': []
        }
        
        # Count source employees (unique from PA0002)
        if pa0002_df is not None and 'Pers.No.' in pa0002_df.columns:
            # Get unique employees from PA0002 only
            source_employees = pa0002_df['Pers.No.'].nunique()
            transfer_stats['source_employee_count'] = source_employees
            
            # Track source file statistics
            transfer_stats['source_file_stats'] = {
                'PA0002': {'rows': len(pa0002_df), 'unique_employees': source_employees}
            }
            
            for file_name, file_df in [('PA0001', pa0001_df), ('PA0006', pa0006_df), ('PA0105', pa0105_df)]:
                if file_df is not None:
                    transfer_stats['source_file_stats'][file_name] = {
                        'rows': len(file_df),
                        'unique_employees': file_df['Pers.No.'].nunique() if 'Pers.No.' in file_df.columns else 0
                    }
        
        # Count output employees
        if output_files and 'employee_data' in output_files:
            output_data = output_files['employee_data']
            output_employees = len(output_data)
            transfer_stats['output_employee_count'] = output_employees
            
            # Calculate transfer metrics - FIXED CALCULATION
            if transfer_stats['source_employee_count'] > 0:
                # Transfer rate should never exceed 100%
                raw_transfer_rate = (output_employees / transfer_stats['source_employee_count']) * 100
                transfer_stats['transfer_rate'] = min(100.0, raw_transfer_rate)  # Cap at 100%
                
                # Calculate actual transferred and lost
                if output_employees <= transfer_stats['source_employee_count']:
                    transfer_stats['employees_transferred'] = output_employees
                    transfer_stats['employees_lost'] = transfer_stats['source_employee_count'] - output_employees
                else:
                    # If output > source, something is wrong with processing
                    transfer_stats['employees_transferred'] = transfer_stats['source_employee_count']
                    transfer_stats['employees_lost'] = 0
                    self._add_warning(
                        'UNEXPECTED_EMPLOYEE_INCREASE',
                        'HIGH',
                        f'Output has more employees ({output_employees}) than source ({transfer_stats["source_employee_count"]})',
                        'This suggests duplicate records may have been created during processing.',
                        'Check the processing logic and source data for duplicates',
                        'Data Transfer',
                        'Employee Count',
                        transfer_stats
                    )
                
                # Check for significant data loss
                if transfer_stats['transfer_rate'] < 90 and transfer_stats['employees_lost'] > 0:
                    self._add_error(
                        'SIGNIFICANT_DATA_LOSS',
                        'HIGH',
                        f'Lost {transfer_stats["employees_lost"]} employees during processing',
                        f'Started with {transfer_stats["source_employee_count"]} employees but only {output_employees} made it to the output file. This is a {100 - transfer_stats["transfer_rate"]:.1f}% loss.',
                        'Check for data quality issues in source files or processing errors',
                        'Data Transfer',
                        'Employee Count',
                        transfer_stats
                    )
                elif transfer_stats['transfer_rate'] < 95 and transfer_stats['employees_lost'] > 0:
                    self._add_warning(
                        'MINOR_DATA_LOSS',
                        'MEDIUM',
                        f'Lost {transfer_stats["employees_lost"]} employees during processing',
                        f'Small number of employees did not make it to output file. This could be due to data quality issues.',
                        'Review source data for incomplete or invalid employee records',
                        'Data Transfer',
                        'Employee Count',
                        transfer_stats
                    )
        
        return transfer_stats
    
    def _validate_output_data(self, output_files):
        """Validate the output employee data"""
        
        if 'employee_data' not in output_files:
            self._add_error(
                'MISSING_OUTPUT_FILE',
                'CRITICAL',
                'Employee output file not generated',
                'No emp.csv file has been created yet',
                'Go to Employee panel and click "Generate Employee File"',
                'Output',
                'Employee File'
            )
            return
        
        output_data = output_files['employee_data']
        
        if len(output_data) == 0:
            self._add_error(
                'EMPTY_OUTPUT_FILE',
                'CRITICAL',
                'Output file is empty',
                'The employee output file was created but contains no employee records',
                'Check source data quality and mapping configuration',
                'Output',
                'Employee Data'
            )
            return
        
        # Check for missing critical fields
        critical_fields = ['USERID', 'FIRSTNAME', 'LASTNAME']
        for field in critical_fields:
            if field not in output_data.columns:
                self._add_error(
                    'MISSING_CRITICAL_FIELD',
                    'HIGH',
                    f'Missing critical field: {field}',
                    f'The output file is missing the "{field}" field which is essential for employee records',
                    'Check your mapping configuration in Admin panel',
                    'Output',
                    field
                )
        
        # Check for excessive empty data
        total_cells = len(output_data) * len(output_data.columns)
        empty_cells = output_data.isnull().sum().sum()
        empty_percentage = (empty_cells / total_cells) * 100
        
        if empty_percentage > 50:
            self._add_warning(
                'HIGH_EMPTY_DATA',
                'MEDIUM',
                f'{empty_percentage:.1f}% of output data is empty',
                'More than half of the employee data fields are empty. This suggests mapping or source data issues.',
                'Review your mapping configuration and source data quality',
                'Output',
                'Data Completeness',
                {'empty_percentage': empty_percentage, 'empty_cells': empty_cells, 'total_cells': total_cells}
            )
    
    def _add_error(self, error_type: str, severity: str, title: str, description: str, 
                   action: str, source: str, field: str, details: Dict = None):
        """Add an error with simple explanations"""
        error = {
            'type': error_type,
            'severity': severity,
            'title': title,
            'description': description,
            'action': action,
            'source': source,
            'field': field,
            'details': details or {},
            'timestamp': datetime.now().isoformat()
        }
        self.errors.append(error)
        self.error_counts[error_type] += 1
    
    def _add_warning(self, warning_type: str, severity: str, title: str, description: str,
                     action: str, source: str, field: str, details: Dict = None):
        """Add a warning with simple explanations"""
        warning = {
            'type': warning_type,
            'severity': severity,
            'title': title,
            'description': description,
            'action': action,
            'source': source,
            'field': field,
            'details': details or {},
            'timestamp': datetime.now().isoformat()
        }
        self.warnings.append(warning)
    
    def _categorize_errors(self) -> Dict:
        """Categorize errors by severity"""
        categories = {
            'CRITICAL': {'errors': [], 'count': 0},
            'HIGH': {'errors': [], 'count': 0},
            'MEDIUM': {'errors': [], 'count': 0},
            'LOW': {'errors': [], 'count': 0}
        }
        
        for error in self.errors:
            severity = error['severity']
            categories[severity]['errors'].append(error)
            categories[severity]['count'] += 1
        
        for warning in self.warnings:
            severity = warning['severity']
            categories[severity]['errors'].append(warning)
            categories[severity]['count'] += 1
        
        return categories

def show_data_transfer_details(transfer_stats):
    """Show detailed data transfer analysis with fixed progress bar"""
    
    st.subheader("📊 Data Transfer Analysis")
    st.info("**What this shows:** How many employee records moved from your source files to the final output")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        source_count = transfer_stats.get('source_employee_count', 0)
        st.metric("Source Employees", f"{source_count:,}")
        st.caption("Found in PA0002")
    
    with col2:
        output_count = transfer_stats.get('output_employee_count', 0)
        st.metric("Output Employees", f"{output_count:,}")
        st.caption("In final emp.csv")
    
    with col3:
        transferred = transfer_stats.get('employees_transferred', 0)
        st.metric("Successfully Transferred", f"{transferred:,}")
        st.caption("Made it through processing")
    
    with col4:
        lost = transfer_stats.get('employees_lost', 0)
        if lost > 0:
            st.error(f"❌ Lost: {lost:,}")
            st.caption("Missing from output")
        else:
            st.success("✅ Lost: 0")
            st.caption("No data loss")
    
    # Transfer rate visualization - FIXED
    transfer_rate = transfer_stats.get('transfer_rate', 0)
    
    st.subheader("🎯 Transfer Success Rate")
    
    if transfer_rate >= 99:
        st.success(f"🏆 **Excellent:** {transfer_rate:.1f}% of employees successfully transferred")
    elif transfer_rate >= 95:
        st.success(f"✅ **Good:** {transfer_rate:.1f}% of employees successfully transferred")
    elif transfer_rate >= 90:
        st.warning(f"⚠️ **Acceptable:** {transfer_rate:.1f}% of employees successfully transferred")
    else:
        st.error(f"❌ **Poor:** {transfer_rate:.1f}% of employees successfully transferred")
    
    # Progress bar - FIXED to handle values properly
    progress_value = min(1.0, max(0.0, transfer_rate / 100))  # Ensure 0.0 to 1.0 range
    st.progress(progress_value)
    
    # Source file details
    if transfer_stats.get('source_file_stats'):
        st.subheader("📂 Source File Details")
        
        file_details = []
        for file_name, stats in transfer_stats['source_file_stats'].items():
            file_details.append({
                'File': file_name,
                'Total Records': f"{stats['rows']:,}",
                'Unique Employees': f"{stats['unique_employees']:,}",
                'Status': '✅ Loaded' if stats['rows'] > 0 else '❌ Empty'
            })
        
        file_df = pd.DataFrame(file_details)
        st.dataframe(file_df, use_container_width=True)

def generate_simple_fix_suggestions(error):
    """Generate simple fix suggestions for common errors"""
    
    error_type = error['type']
    
    if error_type == 'MISSING_PA0002':
        return """
**How to fix:**
1. Go to the Employee panel
2. Click "Upload Your Files"
3. Select your PA0002 file (contains employee names and IDs)
4. Make sure the filename contains "PA0002"
5. Click "Process All Files"
        """
    
    elif error_type == 'DUPLICATE_EMPLOYEE_IDS':
        duplicate_ids = error.get('details', {}).get('duplicate_ids', [])
        return f"""
**How to fix:**
1. Open your PA0002 file in Excel
2. Look for these duplicate employee IDs: {', '.join(map(str, duplicate_ids[:5]))}
3. Keep only one record for each employee ID
4. Delete the duplicate rows
5. Save the file and re-upload
        """
    
    elif error_type == 'ORPHANED_EMPLOYEES_PA0001':
        orphaned_ids = error.get('details', {}).get('orphaned_ids', [])
        return f"""
**How to fix:**
1. These employee IDs are in PA0001 but not in PA0002: {', '.join(map(str, orphaned_ids[:5]))}
2. Option A: Add these employees to PA0002 with their names
3. Option B: Remove these IDs from PA0001
4. Save and re-upload both files
        """
    
    elif error_type == 'SIGNIFICANT_DATA_LOSS':
        return """
**How to fix data loss:**
1. Check your PA0002 file for employees with missing names or IDs
2. Ensure all employee IDs are filled in (no empty cells)
3. Remove any duplicate employee records
4. Make sure PA0001 employee IDs match those in PA0002
5. Re-upload and regenerate your employee file
        """
    
    else:
        return """
**General fix steps:**
1. Check the error details above
2. Fix the issue in your source files
3. Re-upload the corrected files
4. Generate a new employee output file
        """

def show_employee_validation_panel(state):
    """Enhanced validation panel with clear explanations for non-technical users"""
    
    # Clean header
    st.markdown("""
    <div style="background: linear-gradient(90deg, #dc2626 0%, #ef4444 100%); 
                color: white; padding: 2rem; border-radius: 10px; margin-bottom: 2rem;">
        <h1 style="margin: 0; font-size: 2.5rem;">Employee Data Validation</h1>
        <p style="margin: 0.5rem 0 0 0; font-size: 1.2rem; opacity: 0.9;">
            Check your data quality and find issues before processing
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize validator
    if 'employee_validator' not in st.session_state:
        st.session_state.employee_validator = EmployeeDataValidator()
    
    # Run validation with progress indicator
    with st.spinner("Checking your employee data..."):
        validation_results = st.session_state.employee_validator.validate_employee_data_pipeline(state)
    
    # Show validation status
    st.subheader("✅ Validation Status")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if validation_results['source_data_validated']:
            st.success("✅ Source Data Checked")
        else:
            st.error("❌ Source Data Missing")
    
    with col2:
        if validation_results['data_transfer_validated']:
            st.success("✅ Data Transfer Checked")
        else:
            st.warning("⚪ Data Transfer Not Available")
    
    with col3:
        if validation_results['output_data_validated']:
            st.success("✅ Output Data Checked")
        else:
            st.warning("⚪ Output Data Not Available")
    
    # Migration readiness
    if validation_results['migration_ready']:
        st.success("🎉 **Your data is ready for processing!** No critical issues found.")
    else:
        critical_count = len(validation_results['critical_blockers'])
        st.error(f"⚠️ **{critical_count} critical issue(s) must be fixed before processing**")
    
    # Error summary
    st.subheader("📊 Issues Summary")
    
    categories = validation_results['categorized_errors']
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        critical_count = categories['CRITICAL']['count']
        if critical_count > 0:
            st.error(f"🚨 {critical_count} Critical")
            st.caption("Must fix to continue")
        else:
            st.success("✅ 0 Critical")
            st.caption("No blockers")
    
    with col2:
        high_count = categories['HIGH']['count']
        if high_count > 0:
            st.warning(f"⚠️ {high_count} High Priority")
            st.caption("Should fix soon")
        else:
            st.success("✅ 0 High Priority")
            st.caption("No urgent issues")
    
    with col3:
        medium_count = categories['MEDIUM']['count']
        if medium_count > 0:
            st.info(f"ℹ️ {medium_count} Medium Priority")
            st.caption("Consider fixing")
        else:
            st.success("✅ 0 Medium Priority")
            st.caption("No warnings")
    
    with col4:
        total_issues = validation_results['total_errors'] + validation_results['total_warnings']
        if total_issues > 0:
            st.info(f"📋 {total_issues} Total Issues")
        else:
            st.success("🏆 Perfect Data")
        st.caption("All issues combined")
    
    # Data transfer analysis (if available) - FIXED
    if validation_results['data_transfer_validated']:
        transfer_stats = validation_results['data_transfer_stats']
        show_data_transfer_details(transfer_stats)
    
    # Issues details
    st.subheader("🔍 Issues Details")
    
    if validation_results['total_errors'] == 0 and validation_results['total_warnings'] == 0:
        st.success("🎉 **Excellent!** No issues found with your employee data.")
        st.info("Your data is clean and ready for processing. You can proceed with confidence!")
    else:
        # Show issues by severity
        for severity in ['CRITICAL', 'HIGH', 'MEDIUM']:
            issues = categories[severity]['errors']
            if issues:
                if severity == 'CRITICAL':
                    st.error(f"🚨 **Critical Issues ({len(issues)}) - Must Fix These First**")
                    st.write("These issues will prevent employee processing from working:")
                elif severity == 'HIGH':
                    st.warning(f"⚠️ **High Priority Issues ({len(issues)}) - Should Fix Soon**")
                    st.write("These issues may cause data problems:")
                else:
                    st.info(f"ℹ️ **Medium Priority Issues ({len(issues)}) - Consider Fixing**")
                    st.write("These issues are minor but worth reviewing:")
                
                for i, issue in enumerate(issues, 1):
                    with st.container():
                        st.markdown(f"### Issue {i}: {issue['title']}")
                        
                        col1, col2 = st.columns([2, 1])
                        
                        with col1:
                            st.write(f"**What's wrong:** {issue['description']}")
                            st.write(f"**How to fix:** {issue['action']}")
                            st.write(f"**Affected:** {issue['source']} - {issue['field']}")
                        
                        with col2:
                            # Show additional details if available
                            details = issue.get('details', {})
                            if details:
                                for key, value in details.items():
                                    if isinstance(value, (int, float)):
                                        st.metric(key.replace('_', ' ').title(), f"{value:,}")
                                    elif isinstance(value, list) and len(value) <= 5:
                                        st.write(f"**{key.replace('_', ' ').title()}:**")
                                        for item in value:
                                            st.write(f"• {item}")
                        
                        # Show fix suggestions
                        with st.expander(f"💡 Step-by-Step Fix Guide for Issue {i}", expanded=False):
                            fix_suggestions = generate_simple_fix_suggestions(issue)
                            st.markdown(fix_suggestions)
                        
                        st.markdown("---")
    
    # Export validation report
    st.subheader("📥 Export Validation Report")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📄 Generate Summary Report", type="primary"):
            timestamp = datetime.now().strftime('%B %d, %Y at %I:%M %p')
            
            # Create simple text report
            report = f"""
EMPLOYEE DATA VALIDATION REPORT
Generated: {timestamp}

VALIDATION STATUS:
{'✅ READY FOR PROCESSING' if validation_results['migration_ready'] else '❌ ISSUES NEED FIXING'}

SUMMARY:
- Critical Issues: {categories['CRITICAL']['count']} (must fix)
- High Priority: {categories['HIGH']['count']} (should fix)
- Medium Priority: {categories['MEDIUM']['count']} (consider fixing)
- Total Issues: {validation_results['total_errors'] + validation_results['total_warnings']}

DATA TRANSFER:
"""
            
            if validation_results['data_transfer_validated']:
                transfer_stats = validation_results['data_transfer_stats']
                report += f"""- Source Employees: {transfer_stats.get('source_employee_count', 0):,}
- Output Employees: {transfer_stats.get('output_employee_count', 0):,}
- Transfer Rate: {transfer_stats.get('transfer_rate', 0):.1f}%
- Employees Lost: {transfer_stats.get('employees_lost', 0):,}
"""
            else:
                report += "- Not yet processed\n"
            
            report += f"""
RECOMMENDATIONS:
"""
            if validation_results['migration_ready']:
                report += "✅ Your data looks good! Ready to process employee files.\n"
            else:
                report += "❌ Fix the critical issues listed above before processing.\n"
                if categories['CRITICAL']['count'] > 0:
                    report += f"🚨 Focus on {categories['CRITICAL']['count']} critical issues first.\n"
            
            st.download_button(
                label="📥 Download Report",
                data=report,
                file_name=f"employee_validation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )
    
    with col2:
        if st.button("📊 Generate Detailed Report", type="secondary"):
            # Create detailed JSON report
            detailed_report = {
                'validation_summary': {
                    'timestamp': validation_results['timestamp'],
                    'migration_ready': validation_results['migration_ready'],
                    'total_issues': validation_results['total_errors'] + validation_results['total_warnings']
                },
                'issue_summary': {
                    'critical': categories['CRITICAL']['count'],
                    'high': categories['HIGH']['count'],
                    'medium': categories['MEDIUM']['count']
                },
                'data_transfer': validation_results.get('data_transfer_stats', {}),
                'all_issues': validation_results['all_errors'] + validation_results['all_warnings']
            }
            
            report_json = json.dumps(detailed_report, indent=2, default=str)
            
            st.download_button(
                label="📥 Download Detailed Report",
                data=report_json,
                file_name=f"employee_validation_detailed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    
    # Help section
    with st.expander("❓ Need Help Understanding These Results?", expanded=False):
        st.markdown("""
        **What This Validation Checks:**
        
        🔍 **Source Data:** Makes sure your PA files have the right structure and required information
        📊 **Data Transfer:** Tracks how many employees make it from source files to final output
        📤 **Output Data:** Verifies the final employee file is complete and usable
        
        **Issue Severity Levels:**
        
        🚨 **Critical:** These WILL prevent processing from working. Must fix first.
        ⚠️ **High Priority:** These MAY cause data problems or errors. Should fix soon.
        ℹ️ **Medium Priority:** These are minor issues that won't break anything but are worth reviewing.
        
        **Common Issues and Quick Fixes:**
        
        📂 **Missing Files:** Upload the required PA0002 and PA0001 files
        🔄 **Duplicate IDs:** Remove duplicate employee records from your files
        🔗 **Orphaned Records:** Make sure employee IDs match across all files
        📊 **Data Loss:** Check for empty or invalid employee records in source files
        
        **What to Do:**
        1. Fix critical issues first (they block processing)
        2. Address high priority issues (they cause data problems)
        3. Consider medium priority issues (they improve quality)
        4. Re-run validation after making fixes
        """)
