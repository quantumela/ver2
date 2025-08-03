#!/usr/bin/env python3
"""
Configuration setup for your real HRP1000/HRP1001 data
Based on the analysis of your uploaded files
"""

import json
import pandas as pd
import os
from pathlib import Path

def create_directories():
    """Create necessary directories"""
    directories = ["configs", "picklists", "source_samples"]
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)

def setup_real_data_config():
    """Set up configuration based on your actual data structure"""
    
    # HRP1000 columns from your file:
    # ["Client", "Plan version", "Object type", "Object ID", "Planning status", 
    #  "Start date", "End Date", "Language", "IT record no.", "Obj.type/obj.ID", 
    #  "Infotype", "Changed on", "User Name", "Reason", "Historical rec.", 
    #  "Text Module", "Object abbr.", "Name", "Delimit date", "Object abbr..1", 
    #  "Name.1", "Search term"]
    
    # HRP1001 columns (typical structure based on your sample):
    # ["Client", "Object type", "Source ID", "Plan version", "Relationship", 
    #  "Relnship", "Planning status", "Priority", "Start date", "End Date", 
    #  "Variation field", "IT record no.", "Infotype", "Obj.type/obj.ID", 
    #  "Subtype", "Changed on", "User Name", "Reason", "Historical rec.", 
    #  "Text Module", "Rel.obj.type", "Target object ID", "Percentage", "ADATA number"]
    
    # Level template based on your mappings
    level_template = [
        {
            "target_column1": "externalCode",
            "target_column2": "External Code",
            "description": "Unique identifier for the organizational unit"
        },
        {
            "target_column1": "Operator",
            "target_column2": "Operator",
            "description": "Operator information"
        },
        {
            "target_column1": "effectiveStartDate",
            "target_column2": "Effective Start Date",
            "description": "When the organizational unit becomes effective"
        },
        {
            "target_column1": "effectiveEndDate",
            "target_column2": "Effective End Date",
            "description": "When the organizational unit expires"
        },
        {
            "target_column1": "name.en_US",
            "target_column2": "Name (English US)",
            "description": "Name of the unit in US English"
        },
        {
            "target_column1": "name.defaultValue",
            "target_column2": "Name (Default)",
            "description": "Default name value"
        },
        {
            "target_column1": "effectiveStatus",
            "target_column2": "Status",
            "description": "Current status of the organizational unit"
        },
        {
            "target_column1": "Object abbr.",
            "target_column2": "Object Abbreviation",
            "description": "Object abbreviation from source system"
        }
    ]
    
    # Association template
    association_template = [
        {
            "target_column1": "externalCode",
            "target_column2": "External Code",
            "description": "Unique identifier for the association"
        },
        {
            "target_column1": "effectiveStartDate",
            "target_column2": "Effective Start Date",
            "description": "When the relationship becomes effective"
        },
        {
            "target_column1": "effectiveEndDate",
            "target_column2": "Effective End Date",
            "description": "When the relationship expires"
        },
        {
            "target_column1": "cust_toLegalEntity.externalCode",
            "target_column2": "Parent Entity Code",
            "description": "Reference to parent organizational unit"
        },
        {
            "target_column1": "relationshipType",
            "target_column2": "Relationship Type",
            "description": "Type of organizational relationship"
        },
        {
            "target_column1": "effectiveStatus",
            "target_column2": "Status",
            "description": "Current status of the relationship"
        }
    ]
    
    # Your actual column mappings (from current_mappings 6.csv)
    column_mappings = [
        {
            "target_column1": "externalCode",
            "target_column2": "External Code",
            "source_file": "HRP1000",
            "source_column": "Object ID",
            "transformation": "None",
            "transformation_code": "value",
            "default_value": "",
            "picklist_source": "",
            "picklist_column": "",
            "applies_to": "Level",
            "secondary_column": ""
        },
        {
            "target_column1": "Operator",
            "target_column2": "Operator",
            "source_file": "HRP1000",
            "source_column": "",
            "transformation": "None",
            "transformation_code": "value",
            "default_value": "N/A",
            "picklist_source": "",
            "picklist_column": "",
            "applies_to": "Level",
            "secondary_column": ""
        },
        {
            "target_column1": "effectiveStartDate",
            "target_column2": "Effective Start Date",
            "source_file": "HRP1000",
            "source_column": "Start date",
            "transformation": "None",
            "transformation_code": "value",
            "default_value": "",
            "picklist_source": "",
            "picklist_column": "",
            "applies_to": "Level",
            "secondary_column": ""
        },
        {
            "target_column1": "effectiveEndDate",
            "target_column2": "Effective End Date",
            "source_file": "HRP1000",
            "source_column": "End Date",
            "transformation": "None",
            "transformation_code": "value",
            "default_value": "",
            "picklist_source": "",
            "picklist_column": "",
            "applies_to": "Level",
            "secondary_column": ""
        },
        {
            "target_column1": "name.en_US",
            "target_column2": "Name (English US)",
            "source_file": "HRP1000",
            "source_column": "Name",
            "transformation": "Trim Whitespace",
            "transformation_code": "str(value).strip()",
            "default_value": "",
            "picklist_source": "",
            "picklist_column": "",
            "applies_to": "Level",
            "secondary_column": ""
        },
        {
            "target_column1": "name.defaultValue",
            "target_column2": "Name (Default)",
            "source_file": "HRP1000",
            "source_column": "Name",
            "transformation": "Title Case",
            "transformation_code": "str(value).title()",
            "default_value": "",
            "picklist_source": "",
            "picklist_column": "",
            "applies_to": "Level",
            "secondary_column": ""
        },
        {
            "target_column1": "effectiveStatus",
            "target_column2": "Status",
            "source_file": "HRP1000",
            "source_column": "Planning status",
            "transformation": "Lookup Value",
            "transformation_code": "lookup_value(value, picklist_source, picklist_column, default_value)",
            "default_value": "Active",
            "picklist_source": "status_mapping.csv",
            "picklist_column": "status_label",
            "applies_to": "Level",
            "secondary_column": ""
        },
        {
            "target_column1": "Object abbr.",
            "target_column2": "Object Abbreviation",
            "source_file": "HRP1000",
            "source_column": "Object abbr.",
            "transformation": "None",
            "transformation_code": "value",
            "default_value": "",
            "picklist_source": "",
            "picklist_column": "",
            "applies_to": "Level",
            "secondary_column": ""
        },
        # Association mappings
        {
            "target_column1": "externalCode",
            "target_column2": "External Code",
            "source_file": "HRP1001",
            "source_column": "Source ID",
            "transformation": "None",
            "transformation_code": "value",
            "default_value": "",
            "picklist_source": "",
            "picklist_column": "",
            "applies_to": "Association",
            "secondary_column": ""
        },
        {
            "target_column1": "cust_toLegalEntity.externalCode",
            "target_column2": "Parent Entity Code",
            "source_file": "HRP1001",
            "source_column": "Target object ID",
            "transformation": "None",
            "transformation_code": "value",
            "default_value": "",
            "picklist_source": "",
            "picklist_column": "",
            "applies_to": "Association",
            "secondary_column": ""
        },
        {
            "target_column1": "effectiveStartDate",
            "target_column2": "Effective Start Date",
            "source_file": "HRP1001",
            "source_column": "Start date",
            "transformation": "None",
            "transformation_code": "value",
            "default_value": "",
            "picklist_source": "",
            "picklist_column": "",
            "applies_to": "Association",
            "secondary_column": ""
        },
        {
            "target_column1": "relationshipType",
            "target_column2": "Relationship Type",
            "source_file": "HRP1001",
            "source_column": "Relationship",
            "transformation": "UPPERCASE",
            "transformation_code": "str(value).upper()",
            "default_value": "REPORTS_TO",
            "picklist_source": "",
            "picklist_column": "",
            "applies_to": "Association",
            "secondary_column": ""
        }
    ]
    
    # Save configurations
    create_directories()
    
    with open("configs/level_config.json", "w") as f:
        json.dump(level_template, f, indent=2)
    
    with open("configs/association_config.json", "w") as f:
        json.dump(association_template, f, indent=2)
    
    with open("configs/column_mappings_config.json", "w") as f:
        json.dump(column_mappings, f, indent=2)
    
    print("✓ Created configurations for your real data")
    
    # Copy your status mapping to picklists directory
    try:
        status_df = pd.read_csv("status_mapping.csv")
        status_df.to_csv("picklists/status_mapping.csv", index=False)
        print("✓ Copied status mapping to picklists directory")
    except Exception as e:
        print(f"⚠️  Could not copy status mapping: {e}")
    
    # Create sample files from your actual data structure
    create_sample_files()

def create_sample_files():
    """Create sample files based on your actual data structure"""
    
    # Create HRP1000 sample
    hrp1000_sample = pd.DataFrame({
        'Client': ['913'] * 5,
        'Plan version': ['01'] * 5,
        'Object type': ['O'] * 5,
        'Object ID': ['51002422', '51002453', '51002459', '51002486', '51002527'],
        'Planning status': ['1', '1', '1', '1', '1'],
        'Start date': ['16.02.2009', '01.08.2023', '18.02.2014', '03.12.2023', '01.05.2008'],
        'End Date': ['31.12.9999'] * 5,
        'Language': ['E'] * 5,
        'IT record no.': ['000'] * 5,
        'Obj.type/obj.ID': ['O 51002422', 'O 51002453', 'O 51002459', 'O 51002486', 'O 51002527'],
        'Infotype': ['1000'] * 5,
        'Changed on': ['30.05.2013', '01.08.2023', '18.02.2014', '28.11.2023', '30.05.2013'],
        'User Name': ['RFC_TIK', 'AZAMPOGNA', 'JKOVACS', 'BOBRIEN', 'RFC_TIK'],
        'Reason': [None] * 5,
        'Historical rec.': [None] * 5,
        'Text Module': ['00000000'] * 5,
        'Object abbr.': ['B33/Z0244', 'B42/F0054', 'B62/H0870', 'B62/H0872', 'B33/R1955'],
        'Name': ['MACRAE RESEARCH', 'TRANSITIONAL CARE WARD', 'HOMHS - IWAMHS', 'SENIOR CONSUMER CONSULTANT', 'EMPLOYEE SERVICES'],
        'Delimit date': ['00.00.0000'] * 5,
        'Object abbr..1': ['B33/Z0244', 'B42/F0054', 'B62/H0870', 'B62/H0872', 'B33/R1955'],
        'Name.1': ['MACRAE RESEARCH', 'TRANSITIONAL CARE WARD', 'HOMHS - IWAMHS', 'SENIOR CONSUMER CONSULTANT', 'EMPLOYEE SERVICES'],
        'Search term': ['B33/Z0244   MACRAE RESEARCH', 'B42/F0054   TRANSITIONAL CARE WARD', 'B62/H0870   HOMHS - IWAMHS', 'B62/H0872   SENIOR CONSUMER CONSULTANT', 'B33/R1955   EMPLOYEE SERVICES']
    })
    
    # Create HRP1001 sample
    hrp1001_sample = pd.DataFrame({
        'Client': ['913'] * 5,
        'Object type': ['O'] * 5,
        'Source ID': ['51002422', '51002453', '51002459', '51002486', '51002527'],
        'Plan version': ['1'] * 5,
        'Relationship': ['A', 'A', 'A', 'A', 'A'],
        'Relnship': ['2'] * 5,
        'Planning status': ['1'] * 5,
        'Priority': ['', '', '', '', ''],
        'Start date': ['16.02.2009', '01.08.2023', '18.02.2014', '03.12.2023', '01.05.2008'],
        'End Date': ['31.12.9999'] * 5,
        'Variation field': ['O 51003517', 'O 51003492', 'O 51003495', 'O 51003495', 'O 51003517'],
        'IT record no.': ['0'] * 5,
        'Infotype': ['1001'] * 5,
        'Obj.type/obj.ID': ['O 51002422', 'O 51002453', 'O 51002459', 'O 51002486', 'O 51002527'],
        'Subtype': ['A002'] * 5,
        'Changed on': ['31.05.2013', '23.05.2024', '04.08.2022', '17.05.2024', '31.05.2013'],
        'User Name': ['ZCVAUGHAN', 'MIZZIJ', 'RUSSELLC', 'MIZZIJ', 'ZCVAUGHAN'],
        'Reason': [None] * 5,
        'Historical rec.': [None] * 5,
        'Text Module': ['0'] * 5,
        'Rel.obj.type': ['O'] * 5,
        'Target object ID': ['51003517', '51003492', '51003495', '51003495', '51003517'],
        'Percentage': ['0'] * 5,
        'ADATA number': [''] * 5
    })
    
    hrp1000_sample.to_csv("source_samples/HRP1000_sample.csv", index=False)
    hrp1001_sample.to_csv("source_samples/HRP1001_sample.csv", index=False)
    
    print("✓ Created sample files matching your data structure")

if __name__ == "__main__":
    print("🔧 Setting up configuration for your real data...")
    print()
    
    setup_real_data_config()
    
    print()
    print("✅ Configuration setup complete!")
    print()
    print("Your configuration includes:")
    print("- Level template with 8 fields")
    print("- Association template with 6 fields") 
    print("- 12 column mappings")
    print("- Status mapping picklist")
    print("- Sample files matching your data structure")
    print()
    print("Next steps:")
    print("1. Run: streamlit run main_app.py")
    print("2. Go to Admin panel to review/modify configurations")
    print("3. Upload your full HRP1000_Org_Units.xlsx and HRP1001_OrgRelationships.xlsx files")
    print("4. Test the hierarchy processing")
