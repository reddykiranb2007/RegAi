import pandas as pd
import os

files = [
    'd:/RegAi/IVD md - Medical Devices (1).xlsx',
    'd:/RegAi/MD - Medical Devices.xlsx',
    'd:/RegAi/classification_of_medical_devices.xlsx',
    'd:/RegAi/import - IVD Devices (1).xlsx',
    'd:/RegAi/import - Medical Devices.xlsx'
]

print(f"Pandas version: {pd.__version__}")
try:
    import openpyxl
    print(f"Openpyxl version: {openpyxl.__version__}")
except ImportError:
    print("Openpyxl not found via import")

for file_path in files:
    try:
        print(f"--- {os.path.basename(file_path)} ---")
        # Read only the first few rows to get headers, explicit engine
        df = pd.read_excel(file_path, nrows=5, engine='openpyxl')
        print(df.columns.tolist())
        print(df.head(2))
        print("\n")
    except Exception as e:
        print(f"Error reading {file_path}: {e}\n")
