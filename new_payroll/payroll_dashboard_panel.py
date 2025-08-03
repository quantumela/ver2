import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import psutil
import os
from collections import defaultdict

def get_system_performance():
    """Get simple system performance metrics"""
    try:
        memory_info = psutil.virtual_memory()
        cpu_percent = psutil.cpu_percent(interval=0.1)
        
        return {
            'memory_used_percent': memory_info.percent,
            'memory_available_gb': round(memory_info.available / 1024 / 1024 / 1024, 1),
            'cpu_percent': cpu_percent,
            'timestamp': datetime.now().isoformat()
        }
    except:
        return {
            'memory_used_percent': 0,
            'memory_available_gb': 0,
            'cpu_percent': 0,
            'timestamp': datetime.now().isoformat()
        }

def analyze_payroll_data_size_and_performance(state):
    """Analyze payroll data sizes and their impact on performance"""
    
    analysis = {
        'total_data_size_mb': 0,
        'file_sizes': {},
        'processing_recommendations': [],
        'performance_score': 100
    }
    
    try:
        # Analyze payroll source files
        source_files = ['PA0008', 'PA0014']
        
        for file_key in source_files:
            source_data = state.get(f'source_{file_key.lower()}')
            if source_data is not None and not source_data.empty:
                try:
                    size_mb = source_data.memory_usage(deep=True).sum() / 1024 / 1024
                    analysis['file_sizes'][file_key] = {
                        'size_mb': round(size_mb, 1),
                        'rows': len(source_data),
                        'columns': len(source_data.columns)
                    }
                    analysis['total_data_size_mb'] += size_mb
                except:
                    analysis['file_sizes'][file_key] = {
                        'size_mb': 0,
                        'rows': 0,
                        'columns': 0
                    }
        
        # Analyze merged payroll data if available
        merged_data = state.get('merged_payroll_data')
        if merged_data is not None and not merged_data.empty:
            try:
                merged_size_mb = merged_data.memory_usage(deep=True).sum() / 1024 / 1024
                analysis['file_sizes']['Merged Payroll Data'] = {
                    'size_mb': round(merged_size_mb, 1),
                    'rows': len(merged_data),
                    'columns': len(merged_data.columns)
                }
                analysis['total_data_size_mb'] += merged_size_mb
            except:
                pass
        
        # Analyze payroll output files
        output_files = state.get('generated_payroll_files', {})
        if output_files and 'payroll_data' in output_files:
            try:
                output_data = output_files['payroll_data']
                output_size_mb = output_data.memory_usage(deep=True).sum() / 1024 / 1024
                analysis['file_sizes']['Payroll Output'] = {
                    'size_mb': round(output_size_mb, 1),
                    'rows': len(output_data),
                    'columns': len(output_data.columns)
                }
                analysis['total_data_size_mb'] += output_size_mb
            except:
                pass
        
        analysis['total_data_size_mb'] = round(analysis['total_data_size_mb'], 1)
        
        # Generate payroll-specific performance recommendations
        if analysis['total_data_size_mb'] > 200:
            analysis['processing_recommendations'].append("Large payroll dataset detected - processing may take longer")
            analysis['performance_score'] -= 20
        
        if analysis['total_data_size_mb'] > 1000:
            analysis['processing_recommendations'].append("Very large payroll dataset - consider processing in smaller batches")
            analysis['performance_score'] -= 30
        
        # Check for payroll data caching
        if 'merged_payroll_data' in state:
            analysis['processing_recommendations'].append("Payroll data is cached in memory for faster processing")
            analysis['performance_score'] += 10
        else:
            analysis['processing_recommendations'].append("Consider caching payroll data for faster repeated processing")
        
        # Check session state size
        if hasattr(st, 'session_state'):
            session_keys = len(st.session_state.keys())
            if session_keys > 30:
                analysis['processing_recommendations'].append("Session has many stored items - consider clearing old payroll data")
                analysis['performance_score'] -= 10
        
        # Check for duplicate storage
        total_source_rows = sum(info['rows'] for key, info in analysis['file_sizes'].items() 
                               if key in ['PA0008', 'PA0014'])
        merged_rows = analysis['file_sizes'].get('Merged Payroll Data', {}).get('rows', 0)
        
        if merged_rows > 0 and total_source_rows > 0:
            storage_efficiency = merged_rows / total_source_rows
            if storage_efficiency < 0.8:
                analysis['processing_recommendations'].append("Potential data loss during merging - check payroll validation")
                analysis['performance_score'] -= 15
        
    except Exception as e:
        analysis['processing_recommendations'].append(f"Error analyzing payroll data: {str(e)}")
    
    return analysis

def check_payroll_data_health(state):
    """Check overall health of payroll data"""
    
    health_status = {
        'overall_score': 100,
        'issues': [],
        'warnings': [],
        'recommendations': [],
        'status': 'healthy'
    }
    
    try:
        # Check if required payroll files are present
        pa0008 = state.get('source_pa0008')
        pa0014 = state.get('source_pa0014')
        
        if pa0008 is None or pa0008.empty:
            health_status['issues'].append("Missing PA0008 (Wage Types) - Required for payroll processing")
            health_status['overall_score'] -= 40
        
        if pa0014 is None or pa0014.empty:
            health_status['issues'].append("Missing PA0014 (Recurring Elements) - Required for complete payroll")
            health_status['overall_score'] -= 30
        
        # Check for payroll output file
        output_files = state.get('generated_payroll_files', {})
        if not output_files or 'payroll_data' not in output_files:
            health_status['warnings'].append("No payroll output file generated yet")
            health_status['overall_score'] -= 10
        
        # Check payroll data quality if files exist
        if pa0008 is not None and not pa0008.empty:
            # Check for employee ID column
            if 'Pers.No.' not in pa0008.columns:
                health_status['issues'].append("PA0008 missing employee ID column (Pers.No.)")
                health_status['overall_score'] -= 25
            else:
                # Check for duplicate employee records
                duplicates = pa0008['Pers.No.'].duplicated().sum()
                if duplicates > 0:
                    health_status['warnings'].append(f"Found {duplicates} duplicate employee records in PA0008")
                    health_status['overall_score'] -= 15
                
                # Check for empty employee IDs
                empty_ids = pa0008['Pers.No.'].isnull().sum()
                if empty_ids > 0:
                    health_status['issues'].append(f"Found {empty_ids} payroll records with empty employee IDs")
                    health_status['overall_score'] -= 20
            
            # Check for missing payroll data
            missing_pct = (pa0008.isnull().sum().sum() / (len(pa0008) * len(pa0008.columns))) * 100
            if missing_pct > 30:
                health_status['warnings'].append(f"PA0008 has {missing_pct:.1f}% missing payroll data")
                health_status['overall_score'] -= 10
            
            # Check for wage type information
            wage_type_cols = [col for col in pa0008.columns if 'wage' in col.lower() and 'type' in col.lower()]
            if not wage_type_cols:
                health_status['warnings'].append("No wage type columns found in PA0008")
                health_status['overall_score'] -= 10
            
            # Check for amount columns
            amount_cols = [col for col in pa0008.columns if 'amount' in col.lower()]
            if not amount_cols:
                health_status['warnings'].append("No amount columns found in PA0008")
                health_status['overall_score'] -= 15
            else:
                # Check for negative amounts (might be errors)
                for col in amount_cols:
                    if pd.api.types.is_numeric_dtype(pa0008[col]):
                        negative_count = (pa0008[col] < 0).sum()
                        if negative_count > len(pa0008) * 0.1:  # More than 10% negative
                            health_status['warnings'].append(f"Many negative amounts in {col} - verify if intended")
                            health_status['overall_score'] -= 5
        
        # Check PA0014 quality
        if pa0014 is not None and not pa0014.empty:
            if 'Pers.No.' not in pa0014.columns:
                health_status['issues'].append("PA0014 missing employee ID column (Pers.No.)")
                health_status['overall_score'] -= 20
        
        # Check data consistency between files
        if pa0008 is not None and pa0014 is not None and not pa0008.empty and not pa0014.empty:
            if 'Pers.No.' in pa0008.columns and 'Pers.No.' in pa0014.columns:
                pa0008_employees = set(pa0008['Pers.No.'].astype(str))
                pa0014_employees = set(pa0014['Pers.No.'].astype(str))
                
                orphaned_pa0014 = pa0014_employees - pa0008_employees
                if len(orphaned_pa0014) > 0:
                    health_status['warnings'].append(f"{len(orphaned_pa0014)} employees in PA0014 not found in PA0008")
                    health_status['overall_score'] -= 10
        
        # Check merged data health
        merged_data = state.get('merged_payroll_data')
        if merged_data is not None and not merged_data.empty:
            if pa0008 is not None and not pa0008.empty:
                merge_efficiency = len(merged_data) / len(pa0008)
                if merge_efficiency < 0.9:
                    health_status['warnings'].append("Significant data loss during payroll merging")
                    health_status['overall_score'] -= 15
        
        # Generate payroll-specific recommendations
        if health_status['overall_score'] < 70:
            health_status['recommendations'].append("Fix critical payroll issues before processing")
        
        if health_status['warnings']:
            health_status['recommendations'].append("Review payroll warnings to improve data quality")
        
        if not health_status['issues'] and not health_status['warnings']:
            health_status['recommendations'].append("Payroll data looks excellent! Ready for processing")
        
        # Check if payroll mapping is configured
        if 'payroll_mapping_config' not in st.session_state:
            health_status['recommendations'].append("Configure payroll field mapping in Admin panel for better results")
        
        # Determine overall status
        if health_status['overall_score'] >= 90:
            health_status['status'] = 'excellent'
        elif health_status['overall_score'] >= 70:
            health_status['status'] = 'good'
        elif health_status['overall_score'] >= 50:
            health_status['status'] = 'warning'
        else:
            health_status['status'] = 'critical'
    
    except Exception as e:
        health_status['issues'].append(f"Error checking payroll data health: {str(e)}")
        health_status['overall_score'] = 0
        health_status['status'] = 'error'
    
    return health_status

def create_payroll_processing_timeline(state):
    """Create a visual timeline of payroll processing steps"""
    
    timeline_steps = [
        {'step': 'Upload PA Files', 'status': 'pending', 'description': 'Upload PA0008 and PA0014 files'},
        {'step': 'Merge Data', 'status': 'pending', 'description': 'Combine payroll files'},
        {'step': 'Generate Output', 'status': 'pending', 'description': 'Create final payroll file'},
        {'step': 'Validate Results', 'status': 'pending', 'description': 'Check data quality'},
        {'step': 'Download Files', 'status': 'pending', 'description': 'Export processed data'}
    ]
    
    # Update status based on current state
    pa0008 = state.get('source_pa0008')
    pa0014 = state.get('source_pa0014')
    
    # Step 1: Upload PA Files
    if pa0008 is not None and pa0014 is not None:
        timeline_steps[0]['status'] = 'completed'
    elif pa0008 is not None or pa0014 is not None:
        timeline_steps[0]['status'] = 'partial'
    
    # Step 2: Merge Data
    if 'merged_payroll_data' in state:
        timeline_steps[1]['status'] = 'completed'
    elif timeline_steps[0]['status'] == 'completed':
        timeline_steps[1]['status'] = 'ready'
    
    # Step 3: Generate Output
    output_files = state.get('generated_payroll_files', {})
    if output_files and 'payroll_data' in output_files:
        timeline_steps[2]['status'] = 'completed'
    elif timeline_steps[1]['status'] == 'completed':
        timeline_steps[2]['status'] = 'ready'
    
    # Step 4: Validate Results
    if timeline_steps[2]['status'] == 'completed':
        timeline_steps[3]['status'] = 'ready'
    
    # Step 5: Download Files
    if timeline_steps[2]['status'] == 'completed':
        timeline_steps[4]['status'] = 'ready'
    
    return timeline_steps

def show_payroll_dashboard_panel(state):
    """Comprehensive payroll dashboard for monitoring system performance and data health"""
    
    # Clean header
    st.markdown("""
    <div style="background: linear-gradient(90deg, #16a085 0%, #27ae60 100%); 
                color: white; padding: 2rem; border-radius: 10px; margin-bottom: 2rem;">
        <h1 style="margin: 0; font-size: 2.5rem;">Payroll Dashboard</h1>
        <p style="margin: 0.5rem 0 0 0; font-size: 1.2rem; opacity: 0.9;">
            Monitor your payroll system performance and data health
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Get current performance and data analysis
    system_perf = get_system_performance()
    data_analysis = analyze_payroll_data_size_and_performance(state)
    health_status = check_payroll_data_health(state)
    
    # System Status Overview
    st.subheader("🖥️ System Performance")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        memory_pct = system_perf['memory_used_percent']
        st.metric(
            "Memory Usage", 
            f"{memory_pct:.1f}%",
            help="How much of your computer's memory is being used"
        )
        if memory_pct > 85:
            st.caption("⚠️ High usage")
        elif memory_pct > 70:
            st.caption("😐 Moderate usage")
        else:
            st.caption("😊 Normal usage")
    
    with col2:
        cpu_pct = system_perf['cpu_percent']
        st.metric(
            "CPU Usage", 
            f"{cpu_pct:.1f}%",
            help="How hard your computer is working"
        )
        if cpu_pct > 80:
            st.caption("⚠️ High load")
        elif cpu_pct > 50:
            st.caption("😐 Moderate load")
        else:
            st.caption("😊 Normal load")
    
    with col3:
        available_memory = system_perf['memory_available_gb']
        st.metric(
            "Available Memory", 
            f"{available_memory:.1f} GB",
            help="Free memory available for payroll processing"
        )
        if available_memory < 2:
            st.caption("⚠️ Low available")
        elif available_memory < 4:
            st.caption("😐 Moderate available")
        else:
            st.caption("😊 Plenty available")
    
    with col4:
        data_size = data_analysis['total_data_size_mb']
        st.metric(
            "Payroll Data Size", 
            f"{data_size:.1f} MB",
            help="Total size of your loaded payroll data"
        )
        if data_size > 500:
            st.caption("⚠️ Large dataset")
        elif data_size > 100:
            st.caption("😐 Medium dataset")
        else:
            st.caption("😊 Small dataset")
    
    # Payroll Data Health Status
    st.subheader("💰 Payroll Data Health Check")
    
    health_score = health_status['overall_score']
    
    # Health score display
    col1, col2 = st.columns([1, 3])
    
    with col1:
        if health_status['status'] == 'excellent':
            st.success(f"🏆 Excellent ({health_score}/100)")
        elif health_status['status'] == 'good':
            st.success(f"👍 Good ({health_score}/100)")
        elif health_status['status'] == 'warning':
            st.warning(f"⚠️ Needs Attention ({health_score}/100)")
        else:
            st.error(f"❌ Critical Issues ({health_score}/100)")
    
    with col2:
        # Show payroll-specific issues and warnings
        if health_status['issues']:
            st.error("**Critical Payroll Issues:**")
            for issue in health_status['issues']:
                st.write(f"• {issue}")
        
        if health_status['warnings']:
            st.warning("**Payroll Warnings:**")
            for warning in health_status['warnings']:
                st.write(f"• {warning}")
        
        if not health_status['issues'] and not health_status['warnings']:
            st.success("**All payroll systems healthy!** Your data is ready for processing.")
    
    # Payroll Processing Timeline
    st.subheader("📋 Payroll Processing Progress")
    timeline_steps = create_payroll_processing_timeline(state)
    
    for i, step in enumerate(timeline_steps, 1):
        col1, col2, col3 = st.columns([1, 3, 1])
        
        with col1:
            if step['status'] == 'completed':
                st.success(f"✅ Step {i}")
            elif step['status'] == 'ready':
                st.info(f"🔵 Step {i}")
            elif step['status'] == 'partial':
                st.warning(f"⚠️ Step {i}")
            else:
                st.error(f"⭕ Step {i}")
        
        with col2:
            st.write(f"**{step['step']}**")
            st.caption(step['description'])
        
        with col3:
            if step['status'] == 'completed':
                st.caption("Done ✅")
            elif step['status'] == 'ready':
                st.caption("Ready 🔵")
            elif step['status'] == 'partial':
                st.caption("Partial ⚠️")
            else:
                st.caption("Pending ⭕")
    
    # Performance Recommendations
    st.subheader("💡 Payroll Performance Recommendations")
    
    if data_analysis['processing_recommendations'] or health_status['recommendations']:
        all_recommendations = data_analysis['processing_recommendations'] + health_status['recommendations']
        
        for i, recommendation in enumerate(all_recommendations, 1):
            st.info(f"**{i}.** {recommendation}")
    else:
        st.success("**No recommendations needed** - Your payroll system is running optimally!")
    
    # Payroll Data Overview
    st.subheader("📂 Payroll Data Overview")
    
    if data_analysis['file_sizes']:
        st.info("**What this shows:** Size and structure of your loaded payroll data files")
        
        # Create payroll data overview table
        file_data = []
        for file_name, file_info in data_analysis['file_sizes'].items():
            file_data.append({
                'File': file_name,
                'Size (MB)': f"{file_info['size_mb']:.1f}",
                'Records': f"{file_info['rows']:,}",
                'Fields': file_info['columns'],
                'Status': '✅ Loaded' if file_info['rows'] > 0 else '❌ Empty'
            })
        
        file_df = pd.DataFrame(file_data)
        st.dataframe(file_df, use_container_width=True)
        
        # Show payroll summary
        total_records = sum(info['rows'] for info in data_analysis['file_sizes'].values())
        total_size = data_analysis['total_data_size_mb']
        
        st.caption(f"**Total:** {total_size:.1f} MB across {total_records:,} payroll records in {len(data_analysis['file_sizes'])} files")
        
        # Show unique employees if possible
        pa0008 = state.get('source_pa0008')
        if pa0008 is not None and 'Pers.No.' in pa0008.columns:
            unique_employees = pa0008['Pers.No.'].nunique()
            st.caption(f"**Unique Employees:** {unique_employees:,}")
    else:
        st.warning("No payroll data files loaded yet")
        st.info("**What to do:** Go to Payroll panel → Upload your PA files → Return here to monitor performance")
    
    # Quick Actions
    st.subheader("⚡ Quick Actions")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🧹 Clear Payroll Cache", help="Free up memory by clearing cached payroll data"):
            keys_to_clear = ['merged_payroll_data', 'payroll_merge_stats']
            cleared_count = 0
            
            for key in keys_to_clear:
                if key in state:
                    del state[key]
                    cleared_count += 1
            
            if cleared_count > 0:
                st.success(f"Cleared {cleared_count} cached items")
            else:
                st.info("No cached payroll data to clear")
    
    with col2:
        if st.button("🔄 Refresh Status", help="Update all performance metrics"):
            st.rerun()
    
    with col3:
        if st.button("📊 Check Data Health", help="Re-analyze your payroll data quality"):
            # Force refresh of health check
            st.session_state.force_payroll_health_refresh = True
            st.rerun()
    
    with col4:
        if st.button("⚡ Optimize Performance", help="Clear temporary data and optimize memory"):
            # Clear temporary session state items
            keys_to_clear = []
            if hasattr(st, 'session_state'):
                for key in st.session_state.keys():
                    if any(temp_key in key.lower() for temp_key in ['temp', 'cache', 'preview']):
                        keys_to_clear.append(key)
            
            for key in keys_to_clear:
                if key in st.session_state:
                    del st.session_state[key]
            
            if keys_to_clear:
                st.success(f"Optimized! Cleared {len(keys_to_clear)} temporary items")
            else:
                st.info("Already optimized!")
    
    # Performance Tips
    with st.expander("💡 Payroll Performance Tips", expanded=False):
        st.markdown("""
        **To improve payroll processing performance:**
        
        **System Performance:**
        - Close other programs if memory usage is high
        - Wait for CPU usage to drop before processing large payroll files
        - Restart your browser if the system feels slow
        
        **Payroll Data Management:**
        - Clear payroll cache using the "Clear Payroll Cache" button when switching projects
        - Process payroll files in smaller batches if you have very large datasets
        - Upload only the PA files you need (PA0008 and PA0014 are required)
        
        **Processing Tips:**
        - Upload PA0008 (Wage Types) and PA0014 (Recurring Elements) first
        - Use the "Merge & Cache" option for faster repeated processing
        - Generate preview files before full processing to test your setup
        - Download results immediately after generation
        
        **When to be concerned:**
        - Memory usage consistently above 85%
        - CPU usage above 80% for more than a few minutes
        - Payroll data health score below 70
        - Many critical issues or warnings in payroll data
        - Significant data loss during processing (check validation panel)
        
        **Payroll-Specific Optimizations:**
        - Ensure employee IDs are consistent across PA0008 and PA0014
        - Remove duplicate payroll records before processing
        - Verify wage types and amounts are properly formatted
        - Use the validation panel to check data quality before processing
        """)
    
    # System Information (for technical users who want details)
    with st.expander("🔧 Payroll System Information", expanded=False):
        st.markdown("**Technical Details:**")
        
        try:
            # Session state info
            if hasattr(st, 'session_state'):
                session_keys = len(st.session_state.keys())
                payroll_keys = sum(1 for key in st.session_state.keys() if 'payroll' in key.lower())
                st.write(f"**Total Session Items:** {session_keys}")
                st.write(f"**Payroll Session Items:** {payroll_keys}")
            
            # File info
            loaded_files = len(data_analysis['file_sizes'])
            st.write(f"**Loaded Payroll Files:** {loaded_files}")
            
            # Memory details
            memory_info = psutil.virtual_memory()
            st.write(f"**Total System Memory:** {memory_info.total / 1024 / 1024 / 1024:.1f} GB")
            st.write(f"**Used System Memory:** {memory_info.used / 1024 / 1024 / 1024:.1f} GB")
            
            # Payroll-specific info
            pa0008 = state.get('source_pa0008')
            pa0014 = state.get('source_pa0014')
            
            if pa0008 is not None:
                st.write(f"**PA0008 Status:** Loaded ({len(pa0008):,} records)")
            else:
                st.write(f"**PA0008 Status:** Not loaded")
            
            if pa0014 is not None:
                st.write(f"**PA0014 Status:** Loaded ({len(pa0014):,} records)")
            else:
                st.write(f"**PA0014 Status:** Not loaded")
            
            if 'merged_payroll_data' in state:
                merged_data = state['merged_payroll_data']
                st.write(f"**Merged Data:** Cached ({len(merged_data):,} records)")
            else:
                st.write(f"**Merged Data:** Not cached")
            
            # Timestamp
            st.write(f"**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
        except Exception as e:
            st.write(f"**System Info Error:** {str(e)}")
    
    # Auto-refresh option
    st.markdown("---")
    
    auto_refresh = st.checkbox(
        "🔄 Auto-refresh every 30 seconds", 
        value=False,
        help="Automatically update payroll performance metrics"
    )
    
    if auto_refresh:
        # Simple auto-refresh mechanism
        import time
        time.sleep(30)
        st.rerun()