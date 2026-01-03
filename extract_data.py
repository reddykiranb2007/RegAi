import pandas as pd
import json
import os
import re

files_config = [
    # {'path': 'd:/RegAi/IVD md - Medical Devices (1).xlsx', 'type': 'IVD'},
    # {'path': 'd:/RegAi/MD - Medical Devices.xlsx', 'type': 'Medical Device'},
    {'path': 'd:/RegAi/classification_of_medical_devices.xlsx', 'type': 'Medical Device'},
    # {'path': 'd:/RegAi/import - IVD Devices (1).xlsx', 'type': 'IVD'},
    # {'path': 'd:/RegAi/import - Medical Devices.xlsx', 'type': 'Medical Device'}
]

all_devices = {}

def find_header_row(file_path):
    # Read first 10 rows
    try:
        df_preview = pd.read_excel(file_path, nrows=10, header=None, engine='openpyxl')
        for i, row in df_preview.iterrows():
            row_str = " ".join([str(x).lower() for x in row.values])
            if 'risk' in row_str and 'class' in row_str:
                return i
            if 'intended use' in row_str or 'indication' in row_str:
                return i
        return 0 # Default
    except:
        return 0

print("Starting data extraction...")

for config in files_config:
    file_path = config['path']
    if not os.path.exists(file_path):
        continue

    try:
        print(f"Processing {os.path.basename(file_path)}...")
        
        # Dynamic header finding
        header_row = find_header_row(file_path)
        print(f"  Detected header at row {header_row}")
        
        df = pd.read_excel(file_path, header=header_row, engine='openpyxl')
        
        # Normalize columns
        df.columns = [str(c).strip().replace('\n', ' ') for c in df.columns]
        cols = df.columns.tolist()
        
        # Heuristics
        name_col = next((c for c in cols if ('name' in c.lower() and 'device' in c.lower()) or 'proper name' in c.lower()), None)
        risk_col = next((c for c in cols if 'risk' in c.lower() or 'class' in c.lower()), None)
        use_col = next((c for c in cols if 'intended' in c.lower() or 'indication' in c.lower()), None)
        
        if not name_col or not risk_col:
            print(f"  SKIPPING: Could not identify Name/Class columns. Headers: {cols}")
            continue
            
        count = 0
        for _, row in df.iterrows():
            name_raw = row[name_col]
            if pd.isna(name_raw): continue
            name = str(name_raw).strip().replace('\n', ' ')
            name = re.sub(r'\s+', ' ', name) # collapse multiple spaces
            # Remove numbering if present (e.g., "1. DeviceName")
            name = re.sub(r'^\d+\.?\s*', '', name)
            
            risk_raw = row[risk_col]
            if pd.isna(risk_raw): continue
            risk = str(risk_raw).strip().upper()
            risk = risk.replace('CLASS', '').strip()
            
            # Sanity check risk
            if not risk: continue # Empty risk
            
            # Simple handling of "A", "B", "C", "D"
            found_class = None
            for c in ['A', 'B', 'C', 'D']:
                if c in risk:
                    found_class = c
                    break # Take first found
            
            if not found_class:
                found_class = risk # Keep original if not standard, but might need logic
                
            use = ""
            if use_col and pd.notna(row[use_col]):
                use = str(row[use_col]).strip()
            
            key_name = name.lower()
            
            all_devices[key_name] = {
                'originalName': name,
                'class': found_class,
                'type': config['type'],
                'use': use,
                'ivd': config['type'] == 'IVD'
            }
            count += 1
            
        print(f"  Extracted {count} items.")

    except Exception as e:
        print(f"  Error processing file: {e}")

print(f"\nTotal unique devices extracted: {len(all_devices)}")

js_content = f"const extractedDeviceDatabase = {json.dumps(all_devices, indent=2)};"

output_path = 'd:/RegAi/device_data.js'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(js_content)

print(f"Saved to {output_path}")
