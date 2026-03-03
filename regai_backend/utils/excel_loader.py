import json
import os
import pandas as pd
from typing import List, Dict

DATA_FILE_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'device_data.json')

class ExcelLoader:
    """
    Utility to load and manage device data.
    """
    
    @staticmethod
    def load_device_data() -> List[Dict]:
        """
        Loads the device data from the JSON file.
        In a real scenario, this could also load from Excel if needed.
        """
        if not os.path.exists(DATA_FILE_PATH):
            # Fallback or empty
            return []
            
        try:
            with open(DATA_FILE_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data
        except Exception as e:
            print(f"Error loading device data: {e}")
            return []
