import os
import pandas as pd
import hashlib
from pathlib import Path

# Output directory
clean_dir = Path("data/clean")
clean_dir.mkdir(parents=True, exist_ok=True)

# Hashing function
# def hash_phone(phone):
#     return hashlib.sha256(phone.encode()).hexdigest()

def hash_phone(phone, length=8):
    return hashlib.sha256(phone.encode()).hexdigest()[:length]

# Global hash map for consistency
global_phone_map = {}

# Input directory
input_dir = Path("data/tabular")

# Read CSV with fallback encoding
def safe_read_csv(file):
    try:
        return pd.read_csv(file, encoding='utf-8')
    except UnicodeDecodeError:
        return pd.read_csv(file, encoding='ISO-8859-1')

# Process all CSV files
for file in input_dir.glob("*.csv"):
    try:
        df = safe_read_csv(file)

        if "phone_number" in df.columns:
            user_ids = []
            for number in df["phone_number"].astype(str):
                if number not in global_phone_map:
                    global_phone_map[number] = hash_phone(number)
                user_ids.append(global_phone_map[number])

            df["user_id"] = user_ids
            df.drop(columns=["phone_number"], inplace=True)

            output_path = clean_dir / file.name
            df.to_csv(output_path, index=False)
            print(f"Processed and saved: {output_path}")
        else:
            print(f"Skipped (no phone_number column): {file}")

    except Exception as e:
        print(f"Failed to process {file.name}: {e}")
