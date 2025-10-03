import json
import os
from typing import Dict, Any

def load_data(file_path: str) -> Dict[str, Any]:
    """Load data from JSON file. Returns default if file doesn't exist."""
    default_data = {
        "expenses": [],
        "monthly_budget": 0.0,
        "goals": []
    }
    if not os.path.exists(file_path):
        return default_data
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
            # Ensure default keys exist
            for key in default_data:
                if key not in data:
                    data[key] = default_data[key]
            return data
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error loading data: {e}. Using default data.")
        return default_data

def save_data(file_path: str, data: Dict[str, Any]) -> bool:
    """Save data to JSON file."""
    try:
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)
        return True
    except IOError as e:
        print(f"Error saving data: {e}")
        return False
