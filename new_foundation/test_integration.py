#!/usr/bin/env python3
"""
Integration Test Script
Tests the complete flow from configuration to export
"""

import pandas as pd
import json
import os
from pathlib import Path
import sys

# Add utils to path
sys.path.append('.')
from utils.hierarchy_utils import build_hierarchy, format_for_export, load_config

def test_configuration_loading():
    """Test that configurations can be loaded"""
    print("Testing configuration loading...")
    
    # Test template loading
    level_template = load_config("level")
    assoc_template = load_config("association")
    mappings = load_config("column_mappings")
    
    if level_template:
        print(f"✓ Level template loaded: {len(level_template)} columns")
    else:
        print("✗ Level template not found")
        return False
    
    if assoc_template:
        print(f"✓ Association template loaded: {len(assoc_template)} columns")
    else:
        print("✗ Association template not found")
        return False
    
    if mappings:
        print(f"✓ Column mappings loaded: {len(mappings)} mappings")
    else:
        print("✗ Column mappings not found")
        return False
    
    return True

def test_sample_data_loading():
    """Test that sample data can be loaded"""
    print("Testing sample data loading...")
    
    try:
        hrp1000_path = "source_samples/HRP1000_sample.csv"
        hrp1001_path = "source_samples/HRP1001_sample.csv"
        
        if not os.path.exists(hrp1000_path):
            print(f"✗ HRP1000 sample not found: {hrp1000_path}")
            return False, None, None
        
        if not os.path.exists(hrp1001_path):
            print(f"✗ HRP1001 sample not found: {hrp1001_path}")
            return False, None, None
        
        hrp1000 = pd.read_csv(hrp1000_path)
        hrp1001 = pd.read_csv(hrp1001_path)
        
        print(f"✓ HRP1000 loaded: {len(hrp1000)} rows, {len(hrp1000.columns)} columns")
        print(f"✓ HRP1001 loaded: {len(hrp1001)} rows, {len(hrp1001.columns)} columns")
        
        return True, hrp1000, hrp1001
        
    except Exception as e:
        print(f"✗ Error loading sample data: {e}")
        return False, None, None

def test_hierarchy_building(hrp1000, hrp1001):
    """Test hierarchy building functionality"""
    print("Testing hierarchy building...")
    
    try:
        hierarchy = build_hierarchy(hrp1000, hrp1001)
        
        required_keys = ['hierarchy_table', 'associations_table', 'level_data', 'level_associations', 'max_level']
        for key in required_keys:
            if key not in hierarchy:
                print(f"✗ Missing key in hierarchy: {key}")
                return False, None
        
        print(f"✓ Hierarchy built successfully")
        print(f"  - Total units: {len(hierarchy['hierarchy_table'])}")
        print(f"  - Max levels: {hierarchy['max_level']}")
        print(f"  - Total associations: {len(hierarchy['associations_table'])}")
        
        return True, hierarchy
        
    except Exception as e:
        print(f"✗ Error building hierarchy: {e}")
        return False, None

def test_format_for_export(hierarchy, hrp1000, hrp1001):
    """Test export formatting functionality"""
    print("Testing export formatting...")
    
    try:
        # Test Level export
        if 1 in hierarchy['level_data']:
            level_1_data = hierarchy['level_data'][1]
            formatted_level = format_for_export(level_1_data, "Level", None, 1, hrp1000, hrp1001)
            
            print(f"✓ Level export formatted: {len(formatted_level)} rows, {len(formatted_level.columns)} columns")
            print(f"  - Level columns: {list(formatted_level.columns)}")
        
        # Test Association export
        if 2 in hierarchy['level_associations']:
            assoc_data = hierarchy['level_associations'][2]
            formatted_assoc = format_for_export(assoc_data, "Association", None, 2, hrp1000, hrp1001)
            
            print(f"✓ Association export formatted: {len(formatted_assoc)} rows, {len(formatted_assoc.columns)} columns")
            print(f"  - Association columns: {list(formatted_assoc.columns)}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error formatting for export: {e}")
        return False

def test_transformations():
    """Test transformation functionality"""
    print("Testing transformations...")
    
    try:
        # Test basic transformations
        test_data = pd.DataFrame({
            'test_col': ['  TEST VALUE  ', 'another value', '2024-01-01'],
            'date_col': ['16.02.2009', '01.08.2023', '18.02.2014']
        })
        
        # Test trim
        test_data['trimmed'] = test_data['test_col'].apply(lambda x: str(x).strip())
        
        # Test uppercase
        test_data['upper'] = test_data['test_col'].apply(lambda x: str(x).upper())
        
        # Test date formatting
        test_data['formatted_date'] = pd.to_datetime(test_data['date_col'], format='%d.%m.%Y', errors='coerce').dt.strftime('%Y-%m-%d')
        
        print("✓ Basic transformations working")
        
        return True
        
    except Exception as e:
        print(f"✗ Error testing transformations: {e}")
        return False

def test_picklist_lookup():
    """Test picklist lookup functionality"""
    print("Testing picklist lookup...")
    
    try:
        # Check if picklist files exist
        picklist_files = ['status_mapping.csv', 'relationship_mapping.csv', 'department_mapping.csv']
        
        for file in picklist_files:
            path = f"picklists/{file}"
            if os.path.exists(path):
                df = pd.read_csv(path)
                print(f"✓ Picklist {file}: {len(df)} rows")
            else:
                print(f"⚠ Picklist {file} not found")
        
        return True
        
    except Exception as e:
        print(f"✗ Error testing picklist lookup: {e}")
        return False

def test_full_integration():
    """Test complete integration flow"""
    print("🔄 Running full integration test...")
    print("=" * 50)
    
    # Test 1: Configuration loading
    if not test_configuration_loading():
        print("❌ Configuration test failed")
        return False
    
    print()
    
    # Test 2: Sample data loading
    success, hrp1000, hrp1001 = test_sample_data_loading()
    if not success:
        print("❌ Sample data test failed")
        return False
    
    print()
    
    # Test 3: Hierarchy building
    success, hierarchy = test_hierarchy_building(hrp1000, hrp1001)
    if not success:
        print("❌ Hierarchy building test failed")
        return False
    
    print()
    
    # Test 4: Export formatting
    if not test_format_for_export(hierarchy, hrp1000, hrp1001):
        print("❌ Export formatting test failed")
        return False
    
    print()
    
    # Test 5: Transformations
    if not test_transformations():
        print("❌ Transformations test failed")
        return False
    
    print()
    
    # Test 6: Picklist lookup
    if not test_picklist_lookup():
        print("❌ Picklist lookup test failed")
        return False
    
    print()
    print("=" * 50)
    print("✅ All integration tests passed!")
    print()
    print("✨ Your Hierarchy Builder is ready to use!")
    return True

def generate_test_report():
    """Generate a test report"""
    print("Generating test report...")
    
    report = {
        "test_timestamp": pd.Timestamp.now().isoformat(),
        "test_results": {
            "configuration_loading": "PASS",
            "sample_data_loading": "PASS",
            "hierarchy_building": "PASS",
            "export_formatting": "PASS",
            "transformations": "PASS",
            "picklist_lookup": "PASS"
        },
        "file_status": {
            "configs_directory": os.path.exists("configs"),
            "picklists_directory": os.path.exists("picklists"),
            "source_samples_directory": os.path.exists("source_samples"),
            "level_config": os.path.exists("configs/level_config.json"),
            "association_config": os.path.exists("configs/association_config.json"),
            "column_mappings": os.path.exists("configs/column_mappings_config.json")
        }
    }
    
    with open("test_report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    print("✓ Test report saved to test_report.json")

if __name__ == "__main__":
    print("🧪 Organizational Hierarchy Builder - Integration Test")
    print()
    
    # Check if setup has been run
    if not os.path.exists("configs"):
        print("⚠️  Configuration directory not found.")
        print("Please run: python setup_default_config.py")
        sys.exit(1)
    
    # Run full integration test
    success = test_full_integration()
    
    if success:
        generate_test_report()
        print("🎉 Integration test completed successfully!")
        print()
        print("Next steps:")
        print("1. Run: streamlit run main_app.py")
        print("2. Test with your own data files")
        print("3. Customize configurations as needed")
    else:
        print("❌ Integration test failed!")
        print("Please check the error messages above and fix any issues.")
        sys.exit(1)