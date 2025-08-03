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

def analyze_data_size_and_performance(state):
    """Analyze data sizes and their impact on performance"""
    
    analysis = {
        'total_data_size_mb': 0,
        'file_sizes': {},
        'processing_recommendations': [],
        'performance_score': 100
    }
    
    try:
        # Analyze source files
        source_files = ['PA0001', 'PA0002', 'PA0006', 'PA0105']
        
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
        
        # Analyze output files
        output_files = state.get('generated_employee_files', {})
        if output_files and 'employee_data' in output_files:
            try:
                output_data = output_files['employee_data']
                output_size_mb = output_data.memory_usage(deep=True).sum() / 1024 / 1024
                analysis['file_sizes']['Employee Output'] = {
                    'size_mb': round(output_size_mb, 1),
                    'rows': len(output_data),
                    'columns': len(output_data.columns)
                }
                analysis['total_data_size_mb'] += output_size_mb
            except:
                pass
        
        analysis['total_data_size_mb'] = round(analysis['total_data_size_mb'], 1)
        
        # Generate performance recommendations
        if analysis['total_data_size_mb'] > 100:
            analysis['processing_recommendations'].append("Large dataset detected - processing may take longer")
            analysis['performance_score'] -= 20
        
        if analysis['total_data_size_mb'] > 500:
            analysis['processing_recommendations'].append("Very large dataset - consider processing in smaller batches")
            analysis['performance_score'] -= 30
        
        # Check for many files
        if len(analysis['file_sizes']) > 6:
            analysis['processing_recommendations'].append("Many files loaded - clear unused data to improve performance")
            analysis['performance_score'] -= 10
        
        # Check session state size
        if hasattr(st, 'session_state'):
            session_keys = len(st.session_state.keys())
            if session_keys > 20:
                analysis['processing_recommendations'].append("Session has many stored items - consider clearing old data")
                analysis['performance_score'] -= 10
        
    except Exception as e:
        analysis['processing_recommendations'].append(f"Error analyzing data: {str(e)}")
    
    return analysis

def check_data_health(state):
    """Check overall health of employee data"""
    
    health_status = {
        'overall_score': 100,
        'issues': [],
        'warnings': [],
        'recommendations': [],
        'status': 'healthy'
    }
    
    try:
        # Check if required files are present
        pa0002 = state.get('source_pa0002')
        pa0001 = state.get('source_pa0001')
        
        if pa0002 is None or pa0002.empty:
            health_status['issues'].append("Missing PA0002 (Personal Data) - Required for processing")
            health_status['overall_score'] -= 40
        
        if pa0001 is None or pa0001.empty:
            health_status['issues'].append("Missing PA0001 (Work Info) - Required for processing")
            health_status['overall_score'] -= 30
        
        # Check for output file
        output_files = state.get('generated_employee_files', {})
        if not output_files or 'employee_data' not in output_files:
            health_status['warnings'].append("No employee output file generated yet")
            health_status['overall_score'] -= 10
        
        # Check data quality if files exist
        if pa0002 is not None and not pa0002.empty:
            # Check for duplicates
            if 'Pers.No.' in pa0002.columns:
                duplicates = pa0002['Pers.No.'].duplicated().sum()
                if duplicates > 0:
                    health_status['warnings'].append(f"Found {duplicates} duplicate employee IDs in PA0002")
                    health_status['overall_score'] -= 15
            
            # Check for missing data
            missing_pct = (pa0002.isnull().sum().sum() / (len(pa0002) * len(pa0002.columns))) * 100
            if missing_pct > 30:
                health_status['warnings'].append(f"PA0002 has {missing_pct:.1f}% missing data")
                health_status['overall_score'] -= 10
        
        # Generate recommendations
        if health_status['overall_score'] < 70:
            health_status['recommendations'].append("Fix critical issues before processing employee data")
        
        if health_status['warnings']:
            health_status['recommendations'].append("Review warnings to improve data quality")
        
        if not health_status['issues'] and not health_status['warnings']:
            health_status['recommendations'].append("Data looks good! Ready for processing")
        
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
        health_status['issues'].append(f"Error checking data health: {str(e)}")
        health_status['overall_score'] = 0
        health_status['status'] = 'error'
    
    return health_status

def show_employee_dashboard_panel(state):
    """Simple, actionable dashboard for employee data processing"""
    
    # Clean header
    st.markdown("""
    <div style="background: linear-gradient(90deg, #7c3aed 0%, #a855f7 100%); 
                color: white; padding: 2rem; border-radius: 10px; margin-bottom: 2rem;">
        <h1 style="margin: 0; font-size: 2.5rem;">Employee Dashboard</h1>
        <p style="margin: 0.5rem 0 0 0; font-size: 1.2rem; opacity: 0.9;">
            Monitor your system performance and data health
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Get current performance and data analysis
    system_perf = get_system_performance()
    data_analysis = analyze_data_size_and_performance(state)
    health_status = check_data_health(state)
    
    # System Status Overview
    st.subheader("🖥️ System Status")
    
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
            help="Free memory available for processing"
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
            "Data Size", 
            f"{data_size:.1f} MB",
            help="Total size of your loaded employee data"
        )
        if data_size > 500:
            st.caption("⚠️ Large dataset")
        elif data_size > 100:
            st.caption("😐 Medium dataset")
        else:
            st.caption("😊 Small dataset")
    
    # Data Health Status
    st.subheader("📊 Data Health Check")
    
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
        # Show issues and warnings
        if health_status['issues']:
            st.error("**Critical Issues:**")
            for issue in health_status['issues']:
                st.write(f"• {issue}")
        
        if health_status['warnings']:
            st.warning("**Warnings:**")
            for warning in health_status['warnings']:
                st.write(f"• {warning}")
        
        if not health_status['issues'] and not health_status['warnings']:
            st.success("**All systems healthy!** Your data is ready for processing.")
    
    # Performance Recommendations
    st.subheader("💡 Performance Recommendations")
    
    if data_analysis['processing_recommendations'] or health_status['recommendations']:
        all_recommendations = data_analysis['processing_recommendations'] + health_status['recommendations']
        
        for i, recommendation in enumerate(all_recommendations, 1):
            st.info(f"**{i}.** {recommendation}")
    else:
        st.success("**No recommendations needed** - Your system is running optimally!")
    
    # Data Overview
    st.subheader("📂 Data Overview")
    
    if data_analysis['file_sizes']:
        st.info("**What this shows:** Size and structure of your loaded employee data files")
        
        # Create data overview table
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
        
        # Show total summary
        total_records = sum(info['rows'] for info in data_analysis['file_sizes'].values())
        total_size = data_analysis['total_data_size_mb']
        
        st.caption(f"**Total:** {total_size:.1f} MB across {total_records:,} records in {len(data_analysis['file_sizes'])} files")
    else:
        st.warning("No employee data files loaded yet")
        st.info("**What to do:** Go to Employee panel → Upload your PA files → Return here to monitor performance")
    
    # Quick Actions
    st.subheader("⚡ Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🧹 Clear Session Data", help="Free up memory by clearing old data"):
            # Clear non-essential session state items
            keys_to_clear = []
            if hasattr(st, 'session_state'):
                for key in st.session_state.keys():
                    if 'temp' in key.lower() or 'cache' in key.lower():
                        keys_to_clear.append(key)
            
            for key in keys_to_clear:
                if key in st.session_state:
                    del st.session_state[key]
            
            if keys_to_clear:
                st.success(f"Cleared {len(keys_to_clear)} temporary items")
            else:
                st.info("No temporary items to clear")
    
    with col2:
        if st.button("🔄 Refresh Status", help="Update all performance metrics"):
            st.rerun()
    
    with col3:
        if st.button("📊 Check Data Health", help="Re-analyze your data quality"):
            # Force refresh of health check
            st.session_state.force_health_refresh = True
            st.rerun()
    
    # Performance Tips
    with st.expander("💡 Performance Tips", expanded=False):
        st.markdown("""
        **To improve performance:**
        
        **System Performance:**
        - Close other programs if memory usage is high
        - Wait for CPU usage to drop before processing large files
        - Restart your browser if the system feels slow
        
        **Data Management:**
        - Clear old data using the "Clear Session Data" button
        - Process smaller batches if you have very large files
        - Upload only the files you need for current work
        
        **Processing Tips:**
        - Upload required files first (PA0002, PA0001)
        - Add optional files (PA0006, PA0105) only if needed
        - Generate output files one at a time
        - Download results immediately after generation
        
        **When to be concerned:**
        - Memory usage consistently above 85%
        - CPU usage above 80% for more than a few minutes
        - Data health score below 70
        - Many critical issues or warnings
        """)
    
    # System Information (for technical users who want details)
    with st.expander("🔧 System Information", expanded=False):
        st.markdown("**Technical Details:**")
        
        try:
            # Session state info
            if hasattr(st, 'session_state'):
                session_keys = len(st.session_state.keys())
                st.write(f"**Session State Items:** {session_keys}")
            
            # File info
            loaded_files = len(data_analysis['file_sizes'])
            st.write(f"**Loaded Files:** {loaded_files}")
            
            # Memory details
            memory_info = psutil.virtual_memory()
            st.write(f"**Total System Memory:** {memory_info.total / 1024 / 1024 / 1024:.1f} GB")
            st.write(f"**Used System Memory:** {memory_info.used / 1024 / 1024 / 1024:.1f} GB")
            
            # Timestamp
            st.write(f"**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
        except Exception as e:
            st.write(f"**System Info Error:** {str(e)}")
    
    # Auto-refresh option
    st.markdown("---")
    
    auto_refresh = st.checkbox(
        "🔄 Auto-refresh every 30 seconds", 
        value=False,
        help="Automatically update performance metrics"
    )
    
    if auto_refresh:
        # Simple auto-refresh mechanism
        import time
        time.sleep(30)
        st.rerun()
