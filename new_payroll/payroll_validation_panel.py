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

class PayrollDataValidator:
    """Payroll-specific validator for data quality with clear explanations"""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.error_counts = defaultdict(int)
        self.data_transfer_tracking = {}
    
    def validate_payroll_data_pipeline(self, state) -> Dict:
        """Validate payroll data from source to output with transfer tracking"""
        
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
        pa0008_df = safe_get_dataframe(state, 'source_pa0008')
        pa0014_df = safe_get_dataframe(state, 'source_pa0014')
        output_files = state.get('generated_payroll_files', {})
        
        # 1. Validate source data
        if any([pa0008_df is not None, pa0014_df is not None]):
            self._validate_payroll_source_files(pa0008_df, pa0014_df)
            validation_results['source_data_validated'] = True
        
        # 2. Validate data transfer (how many records made it through)
        if pa0008_df is not None and output_files:
            transfer_stats = self._validate_payroll_data_transfer(pa0008_df, pa0014_df, output_files)
            validation_results['data_transfer_stats'] = transfer_stats
            validation_results['data_transfer_validated'] = True
        
        # 3. Validate output data
        if output_files:
            self._validate_payroll_output_data(output_files)
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
    
    def _validate_payroll_source_files(self, pa0008_df, pa0014_df):
        """Validate payroll source files with clear explanations"""
        
        # Check for required files
        if pa0008_df is None:
            self._add_error(
                'MISSING_PA0008',
                'CRITICAL',
                'PA0008 (Wage Types) file is missing',
                'This file contains wage information and payment amounts. Without it, we cannot process any payroll data.',
                'Upload your PA0008 file in the Payroll panel',
                'PA0008',
                'File Missing'
            )
        else:
            # Check PA0008 structure
            self._validate_pa0008_structure(pa0008_df)
        
        if pa0014_df is None:
            self._add_error(
                'MISSING_PA0014',
                'CRITICAL',
                'PA0014 (Recurring Elements) file is missing',
                'This file contains recurring payments and deductions. Without it, payroll processing will be incomplete.',
                'Upload your PA0014 file in the Payroll panel',
                'PA0014',
                'File Missing'
            )
        else:
            # Check PA0014 structure
            self._validate_pa0014_structure(pa0014_df)
        
        # Validate data consistency across files
        if pa0008_df is not None and pa0014_df is not None:
            self._validate_payroll_employee_consistency(pa0008_df, pa0014_df)
    
    def _validate_pa0008_structure(self, pa0008_df):
        """Validate PA0008 file structure"""
        
        required_columns = ['Pers.No.']
        recommended_columns = ['Wage Type', 'Amount', 'Currency', 'Pay Period']
        
        for col in required_columns:
            if col not in pa0008_df.columns:
                self._add_error(
                    'MISSING_REQUIRED_COLUMN',
                    'CRITICAL',
                    f'Missing required column: {col}',
                    f'PA0008 must have a "{col}" column for payroll processing',
                    f'Add the "{col}" column to your PA0008 file',
                    'PA0008',
                    col
                )
        
        # Check for recommended columns
        for col in recommended_columns:
            if col not in pa0008_df.columns:
                self._add_warning(
                    'MISSING_RECOMMENDED_COLUMN',
                    'MEDIUM',
                    f'Missing recommended column: {col}',
                    f'PA0008 should have a "{col}" column for complete payroll processing',
                    f'Consider adding the "{col}" column to your PA0008 file',
                    'PA0008',
                    col
                )
        
        # Check for empty required columns
        if 'Pers.No.' in pa0008_df.columns:
            empty_ids = pa0008_df['Pers.No.'].isnull().sum()
            if empty_ids > 0:
                self._add_error(
                    'EMPTY_EMPLOYEE_IDS',
                    'CRITICAL',
                    f'{empty_ids} payroll records have empty employee IDs',
                    f'Found {empty_ids} rows where the employee ID (Pers.No.) is empty. These payroll records cannot be processed.',
                    'Fill in the missing employee IDs in your PA0008 file',
                    'PA0008',
                    'Pers.No.',
                    {'empty_count': empty_ids, 'total_rows': len(pa0008_df)}
                )
        
        # Check for negative amounts
        amount_columns = [col for col in pa0008_df.columns if 'amount' in col.lower()]
        for amount_col in amount_columns:
            if pd.api.types.is_numeric_dtype(pa0008_df[amount_col]):
                negative_amounts = (pa0008_df[amount_col] < 0).sum()
                if negative_amounts > 0:
                    self._add_warning(
                        'NEGATIVE_AMOUNTS',
                        'MEDIUM',
                        f'{negative_amounts} negative amounts found in {amount_col}',
                        f'Found {negative_amounts} negative amounts which may indicate deductions or data errors.',
                        'Review negative amounts to ensure they are intended (deductions) or fix data errors',
                        'PA0008',
                        amount_col,
                        {'negative_count': negative_amounts}
                    )
        
        # Check for duplicate payroll records
        if len(pa0008_df.columns) >= 2:
            duplicates = pa0008_df.duplicated().sum()
            if duplicates > 0:
                self._add_warning(
                    'DUPLICATE_PAYROLL_RECORDS',
                    'MEDIUM',
                    f'{duplicates} duplicate payroll records found',
                    f'Found {duplicates} completely identical payroll records. This may cause double payments.',
                    'Remove duplicate payroll records from your PA0008 file',
                    'PA0008',
                    'All Columns',
                    {'duplicate_count': duplicates}
                )
    
    def _validate_pa0014_structure(self, pa0014_df):
        """Validate PA0014 file structure"""
        
        if 'Pers.No.' not in pa0014_df.columns:
            self._add_error(
                'MISSING_EMPLOYEE_ID_COLUMN',
                'CRITICAL',
                'PA0014 missing employee ID column',
                'PA0014 must have a "Pers.No." column to link recurring elements to employees',
                'Add the "Pers.No." column to your PA0014 file',
                'PA0014',
                'Pers.No.'
            )
        
        # Check for recurring amount columns
        recurring_columns = [col for col in pa0014_df.columns if 'recurring' in col.lower() or 'amount' in col.lower()]
        if not recurring_columns:
            self._add_warning(
                'NO_RECURRING_AMOUNTS',
                'MEDIUM',
                'No recurring amount columns found in PA0014',
                'PA0014 should contain recurring payment or deduction amounts',
                'Verify that PA0014 contains the expected recurring payment data',
                'PA0014',
                'Recurring Amounts'
            )
    
    def _validate_payroll_employee_consistency(self, pa0008_df, pa0014_df):
        """Validate consistency of employee IDs across payroll files"""
        
        if 'Pers.No.' not in pa0008_df.columns or 'Pers.No.' not in pa0014_df.columns:
            return
        
        # Get employee IDs from both files
        pa0008_employee_ids = set(pa0008_df['Pers.No.'].astype(str))
        pa0014_employee_ids = set(pa0014_df['Pers.No.'].astype(str))
        
        # Find employees in PA0014 but not in PA0008
        orphaned_ids = pa0014_employee_ids - pa0008_employee_ids
        if orphaned_ids:
            self._add_warning(
                'ORPHANED_EMPLOYEES_PA0014',
                'MEDIUM',
                f'{len(orphaned_ids)} employees in PA0014 not found in PA0008',
                f'Found employee IDs in PA0014 that do not exist in PA0008. These recurring elements cannot be linked to wage payments.',
                'Either add these employees to PA0008 or remove them from PA0014',
                'PA0014',
                'Pers.No.',
                {'orphaned_count': len(orphaned_ids), 'orphaned_ids': list(orphaned_ids)[:10]}
            )
        
        # Find employees in PA0008 but not in PA0014 (less critical)
        missing_recurring = pa0008_employee_ids - pa0014_employee_ids
        if len(missing_recurring) > len(pa0008_employee_ids) * 0.5:  # More than 50% missing
            self._add_warning(
                'MANY_EMPLOYEES_WITHOUT_RECURRING',
                'LOW',
                f'{len(missing_recurring)} employees have no recurring elements',
                f'More than half of employees in PA0008 do not have corresponding entries in PA0014.',
                'This may be normal if not all employees have recurring payments/deductions',
                'PA0014',
                'Coverage',
                {'missing_count': len(missing_recurring)}
            )
    
    def _validate_payroll_data_transfer(self, pa0008_df, pa0014_df, output_files):
        """Track how many payroll records transferred from source to output"""
        
        transfer_stats = {
            'source_record_count': 0,
            'output_record_count': 0,
            'records_transferred': 0,
            'records_lost': 0,
            'transfer_rate': 0.0,
            'source_file_stats': {},
            'data_loss_details': []
        }
        
        # Count source records (from PA0008)
        if pa0008_df is not None:
            source_records = len(pa0008_df)
            transfer_stats['source_record_count'] = source_records
            
            # Track source file statistics
            transfer_stats['source_file_stats'] = {
                'PA0008': {'rows': len(pa0008_df), 'unique_employees': pa0008_df['Pers.No.'].nunique() if 'Pers.No.' in pa0008_df.columns else 0}
            }
            
            if pa0014_df is not None:
                transfer_stats['source_file_stats']['PA0014'] = {
                    'rows': len(pa0014_df),
                    'unique_employees': pa0014_df['Pers.No.'].nunique() if 'Pers.No.' in pa0014_df.columns else 0
                }
        
        # Count output records
        if output_files and 'payroll_data' in output_files:
            output_data = output_files['payroll_data']
            output_records = len(output_data)
            transfer_stats['output_record_count'] = output_records
            
            # Calculate transfer metrics
            if transfer_stats['source_record_count'] > 0:
                raw_transfer_rate = (output_records / transfer_stats['source_record_count']) * 100
                transfer_stats['transfer_rate'] = min(100.0, raw_transfer_rate)  # Cap at 100%
                
                # Calculate actual transferred and lost
                if output_records <= transfer_stats['source_record_count']:
                    transfer_stats['records_transferred'] = output_records
                    transfer_stats['records_lost'] = transfer_stats['source_record_count'] - output_records
                else:
                    # If output > source, something is wrong with processing
                    transfer_stats['records_transferred'] = transfer_stats['source_record_count']
                    transfer_stats['records_lost'] = 0
                    self._add_warning(
                        'UNEXPECTED_RECORD_INCREASE',
                        'HIGH',
                        f'Output has more records ({output_records}) than source ({transfer_stats["source_record_count"]})',
                        'This suggests duplicate records may have been created during processing.',
                        'Check the processing logic and source data for duplicates',
                        'Data Transfer',
                        'Record Count',
                        transfer_stats
                    )
                
                # Check for significant data loss
                if transfer_stats['transfer_rate'] < 90 and transfer_stats['records_lost'] > 0:
                    self._add_error(
                        'SIGNIFICANT_PAYROLL_DATA_LOSS',
                        'HIGH',
                        f'Lost {transfer_stats["records_lost"]} payroll records during processing',
                        f'Started with {transfer_stats["source_record_count"]} records but only {output_records} made it to the output file. This is a {100 - transfer_stats["transfer_rate"]:.1f}% loss.',
                        'Check for data quality issues in source files or processing errors',
                        'Data Transfer',
                        'Record Count',
                        transfer_stats
                    )
                elif transfer_stats['transfer_rate'] < 95 and transfer_stats['records_lost'] > 0:
                    self._add_warning(
                        'MINOR_PAYROLL_DATA_LOSS',
                        'MEDIUM',
                        f'Lost {transfer_stats["records_lost"]} payroll records during processing',
                        f'Small number of records did not make it to output file. This could be due to data quality issues.',
                        'Review source data for incomplete or invalid payroll records',
                        'Data Transfer',
                        'Record Count',
                        transfer_stats
                    )
        
        return transfer_stats
    
    def _validate_payroll_output_data(self, output_files):
        """Validate the output payroll data"""
        
        if 'payroll_data' not in output_files:
            self._add_error(
                'MISSING_PAYROLL_OUTPUT_FILE',
                'CRITICAL',
                'Payroll output file not generated',
                'No payroll.csv file has been created yet',
                'Go to Payroll panel and click "Generate Payroll File"',
                'Output',
                'Payroll File'
            )
            return
        
        output_data = output_files['payroll_data']
        
        if len(output_data) == 0:
            self._add_error(
                'EMPTY_PAYROLL_OUTPUT_FILE',
                'CRITICAL',
                'Payroll output file is empty',
                'The payroll output file was created but contains no payroll records',
                'Check source data quality and mapping configuration',
                'Output',
                'Payroll Data'
            )
            return
        
        # Check for missing critical payroll fields
        critical_fields = ['EMPLOYEE_ID', 'WAGE_TYPE', 'AMOUNT']
        for field in critical_fields:
            if field not in output_data.columns:
                self._add_error(
                    'MISSING_CRITICAL_PAYROLL_FIELD',
                    'HIGH',
                    f'Missing critical payroll field: {field}',
                    f'The output file is missing the "{field}" field which is essential for payroll records',
                    'Check your payroll mapping configuration in Admin panel',
                    'Output',
                    field
                )
        
        # Check for excessive empty data
        total_cells = len(output_data) * len(output_data.columns)
        empty_cells = output_data.isnull().sum().sum()
        empty_percentage = (empty_cells / total_cells) * 100
        
        if empty_percentage > 50:
            self._add_warning(
                'HIGH_EMPTY_PAYROLL_DATA',
                'MEDIUM',
                f'{empty_percentage:.1f}% of payroll output data is empty',
                'More than half of the payroll data fields are empty. This suggests mapping or source data issues.',
                'Review your payroll mapping configuration and source data quality',
                'Output',
                'Data Completeness',
                {'empty_percentage': empty_percentage, 'empty_cells': empty_cells, 'total_cells': total_cells}
            )
        
        # Payroll-specific validations
        if 'AMOUNT' in output_data.columns:
            # Check for zero amounts
            zero_amounts = (output_data['AMOUNT'].astype(str) == '0.00').sum()
            if zero_amounts > len(output_data) * 0.1:  # More than 10% zero amounts
                self._add_warning(
                    'MANY_ZERO_AMOUNTS',
                    'LOW',
                    f'{zero_amounts} payroll records have zero amounts',
                    f'{(zero_amounts/len(output_data)*100):.1f}% of payroll records have zero payment amounts.',
                    'Review if zero amounts are expected or if there are mapping issues',
                    'Output',
                    'AMOUNT',
                    {'zero_count': zero_amounts, 'zero_percentage': zero_amounts/len(output_data)*100}
                )
        
        if 'CURRENCY' in output_data.columns:
            # Check currency consistency
            unique_currencies = output_data['CURRENCY'].nunique()
            if unique_currencies > 3:
                self._add_warning(
                    'MULTIPLE_CURRENCIES',
                    'LOW',
                    f'{unique_currencies} different currencies found',
                    'Multiple currencies in payroll data may complicate processing.',
                    'Verify if multiple currencies are expected for your organization',
                    'Output',
                    'CURRENCY',
                    {'currency_count': unique_currencies}
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

def show_payroll_data_transfer_details(transfer_stats):
    """Show detailed payroll data transfer analysis with fixed progress bar"""
    
    st.subheader("📊 Payroll Data Transfer Analysis")
    st.info("**What this shows:** How many payroll records moved from your source files to the final output")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        source_count = transfer_stats.get('source_record_count', 0)
        st.metric("Source Records", f"{source_count:,}")
        st.caption("Found in PA0008")
    
    with col2:
        output_count = transfer_stats.get('output_record_count', 0)
        st.metric("Output Records", f"{output_count:,}")
        st.caption("In final payroll.csv")
    
    with col3:
        transferred = transfer_stats.get('records_transferred', 0)
        st.metric("Successfully Transferred", f"{transferred:,}")
        st.caption("Made it through processing")
    
    with col4:
        lost = transfer_stats.get('records_lost', 0)
        if lost > 0:
            st.error(f"❌ Lost: {lost:,}")
            st.caption("Missing from output")
        else:
            st.success("✅ Lost: 0")
            st.caption("No data loss")
    
    # Transfer rate visualization
    transfer_rate = transfer_stats.get('transfer_rate', 0)
    
    st.subheader("🎯 Transfer Success Rate")
    
    if transfer_rate >= 99:
        st.success(f"🏆 **Excellent:** {transfer_rate:.1f}% of payroll records successfully transferred")
    elif transfer_rate >= 95:
        st.success(f"✅ **Good:** {transfer_rate:.1f}% of payroll records successfully transferred")
    elif transfer_rate >= 90:
        st.warning(f"⚠️ **Acceptable:** {transfer_rate:.1f}% of payroll records successfully transferred")
    else:
        st.error(f"❌ **Poor:** {transfer_rate:.1f}% of payroll records successfully transferred")
    
    # Progress bar
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

def generate_payroll_fix_suggestions(error):
    """Generate simple fix suggestions for common payroll errors"""
    
    error_type = error['type']
    
    if error_type == 'MISSING_PA0008':
        return """
**How to fix:**
1. Go to the Payroll panel
2. Click "Upload Your Files"
3. Select your PA0008 file (contains wage types and payment amounts)
4. Make sure the filename contains "PA0008"
5. Click "Process All Payroll Files"
        """
    
    elif error_type == 'NEGATIVE_AMOUNTS':
        return """
**How to fix:**
1. Open your PA0008 file in Excel
2. Look for negative amounts in payment columns
3. Verify if these are intended deductions or data errors
4. For deductions: Consider moving to PA0014 (recurring elements)
5. For errors: Correct the amounts and re-upload
        """
    
    elif error_type == 'DUPLICATE_PAYROLL_RECORDS':
        return """
**How to fix:**
1. Open your PA0008 file in Excel
2. Use Data → Remove Duplicates feature
3. Review any removed records to ensure they weren't legitimate
4. Save the file and re-upload
        """
    
    elif error_type == 'ORPHANED_EMPLOYEES_PA0014':
        orphaned_ids = error.get('details', {}).get('orphaned_ids', [])
        return f"""
**How to fix:**
1. These employee IDs are in PA0014 but not in PA0008: {', '.join(map(str, orphaned_ids[:5]))}
2. Option A: Add these employees to PA0008 with their wage information
3. Option B: Remove these IDs from PA0014 if they shouldn't have recurring elements
4. Save and re-upload both files
        """
    
    elif error_type == 'SIGNIFICANT_PAYROLL_DATA_LOSS':
        return """
**How to fix payroll data loss:**
1. Check your PA0008 file for records with missing employee IDs
2. Ensure all required fields are filled in (no empty cells in critical columns)
3. Remove any completely duplicate payroll records
4. Verify that employee IDs in PA0008 and PA0014 match
5. Re-upload and regenerate your payroll file
        """
    
    else:
        return """
**General fix steps:**
1. Check the error details above
2. Fix the issue in your source files
3. Re-upload the corrected files
4. Generate a new payroll output file
        """

def show_payroll_validation_panel(state):
    """Enhanced payroll validation panel with clear explanations for non-technical users"""
    
    # Clean header
    st.markdown("""
    <div style="background: linear-gradient(90deg, #e74c3c 0%, #c0392b 100%); 
                color: white; padding: 2rem; border-radius: 10px; margin-bottom: 2rem;">
        <h1 style="margin: 0; font-size: 2.5rem;">Payroll Data Validation</h1>
        <p style="margin: 0.5rem 0 0 0; font-size: 1.2rem; opacity: 0.9;">
            Check your payroll data quality and find issues before processing
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize validator
    if 'payroll_validator' not in st.session_state:
        st.session_state.payroll_validator = PayrollDataValidator()
    
    # Run validation with progress indicator
    with st.spinner("Checking your payroll data..."):
        validation_results = st.session_state.payroll_validator.validate_payroll_data_pipeline(state)
    
    # Show validation status
    st.subheader("✅ Payroll Validation Status")
    
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
        st.success("🎉 **Your payroll data is ready for processing!** No critical issues found.")
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
    
    # Data transfer analysis (if available)
    if validation_results['data_transfer_validated']:
        transfer_stats = validation_results['data_transfer_stats']
        show_payroll_data_transfer_details(transfer_stats)
    
    # Issues details
    st.subheader("🔍 Issues Details")
    
    if validation_results['total_errors'] == 0 and validation_results['total_warnings'] == 0:
        st.success("🎉 **Excellent!** No issues found with your payroll data.")
        st.info("Your payroll data is clean and ready for processing. You can proceed with confidence!")
    else:
        # Show issues by severity
        for severity in ['CRITICAL', 'HIGH', 'MEDIUM']:
            issues = categories[severity]['errors']
            if issues:
                if severity == 'CRITICAL':
                    st.error(f"🚨 **Critical Issues ({len(issues)}) - Must Fix These First**")
                    st.write("These issues will prevent payroll processing from working:")
                elif severity == 'HIGH':
                    st.warning(f"⚠️ **High Priority Issues ({len(issues)}) - Should Fix Soon**")
                    st.write("These issues may cause payroll data problems:")
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
                            fix_suggestions = generate_payroll_fix_suggestions(issue)
                            st.markdown(fix_suggestions)
                        
                        st.markdown("---")
    
    # Export validation report
    st.subheader("📥 Export Payroll Validation Report")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📄 Generate Summary Report", type="primary"):
            timestamp = datetime.now().strftime('%B %d, %Y at %I:%M %p')
            
            # Create simple text report
            report = f"""
PAYROLL DATA VALIDATION REPORT
Generated: {timestamp}

VALIDATION STATUS:
{'✅ READY FOR PROCESSING' if validation_results['migration_ready'] else '❌ ISSUES NEED FIXING'}

SUMMARY:
- Critical Issues: {categories['CRITICAL']['count']} (must fix)
- High Priority: {categories['HIGH']['count']} (should fix)
- Medium Priority: {categories['MEDIUM']['count']} (consider fixing)
- Total Issues: {validation_results['total_errors'] + validation_results['total_warnings']}

PAYROLL DATA TRANSFER:
"""
            
            if validation_results['data_transfer_validated']:
                transfer_stats = validation_results['data_transfer_stats']
                report += f"""- Source Records: {transfer_stats.get('source_record_count', 0):,}
- Output Records: {transfer_stats.get('output_record_count', 0):,}
- Transfer Rate: {transfer_stats.get('transfer_rate', 0):.1f}%
- Records Lost: {transfer_stats.get('records_lost', 0):,}
"""
            else:
                report += "- Not yet processed\n"
            
            report += f"""
RECOMMENDATIONS:
"""
            if validation_results['migration_ready']:
                report += "✅ Your payroll data looks good! Ready to process payroll files.\n"
            else:
                report += "❌ Fix the critical issues listed above before processing.\n"
                if categories['CRITICAL']['count'] > 0:
                    report += f"🚨 Focus on {categories['CRITICAL']['count']} critical issues first.\n"
            
            st.download_button(
                label="📥 Download Report",
                data=report,
                file_name=f"payroll_validation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
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
                'payroll_data_transfer': validation_results.get('data_transfer_stats', {}),
                'all_issues': validation_results['all_errors'] + validation_results['all_warnings']
            }
            
            report_json = json.dumps(detailed_report, indent=2, default=str)
            
            st.download_button(
                label="📥 Download Detailed Report",
                data=report_json,
                file_name=f"payroll_validation_detailed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    
    # Help section
    with st.expander("❓ Need Help Understanding These Payroll Results?", expanded=False):
        st.markdown("""
        **What This Payroll Validation Checks:**
        
        🔍 **Source Data:** Makes sure your PA0008 and PA0014 files have the right structure and required information
        📊 **Data Transfer:** Tracks how many payroll records make it from source files to final output
        📤 **Output Data:** Verifies the final payroll file is complete and usable
        
        **Issue Severity Levels:**
        
        🚨 **Critical:** These WILL prevent payroll processing from working. Must fix first.
        ⚠️ **High Priority:** These MAY cause payroll data problems or errors. Should fix soon.
        ℹ️ **Medium Priority:** These are minor issues that won't break anything but are worth reviewing.
        
        **Common Payroll Issues and Quick Fixes:**
        
        📂 **Missing Files:** Upload the required PA0008 and PA0014 files
        💰 **Negative Amounts:** Check if these are deductions or data errors
        🔄 **Duplicate Records:** Remove duplicate payroll records from your files
        🔗 **Orphaned Records:** Make sure employee IDs match across all files
        📊 **Data Loss:** Check for empty or invalid payroll records in source files
        
        **What to Do:**
        1. Fix critical issues first (they block processing)
        2. Address high priority issues (they cause data problems)
        3. Consider medium priority issues (they improve quality)
        4. Re-run validation after making fixes
        """)
