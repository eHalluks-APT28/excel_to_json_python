import pandas as pd
import json
import uuid
import os
from datetime import datetime


def log_error(message):
    log_file_path = 'logs.txt'
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"({current_time}) {message}\n"
    with open(log_file_path, 'a', encoding='utf-8') as log_file:
        log_file.write(log_entry)


input_file_path = 'list.xlsx'
output_file_name = os.path.splitext(os.path.basename(input_file_path))[0] + '.json'
output_file_path = os.path.join(os.path.dirname(input_file_path), output_file_name)

df = pd.DataFrame()
try:
    df = pd.read_excel(input_file_path, usecols=[0, 1], skiprows=1, names=['product_name', 'category_name'])
except Exception as e:
    error_message = f"Error loading sheet with restrictions: {e}"
    log_error(error_message)
    print(error_message)

if not df.empty:
    json_data = []
    for index, row in df.iterrows():
        record = {
            "id": str(uuid.uuid4()),
            "product": row['product_name'],
            "category": row['category_name']
        }
        json_data.append(record)

    try:
        with open(output_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(json_data, json_file, ensure_ascii=False, indent=4)
        print(f"Done writing to {output_file_path}")
    except Exception as e:
        error_message = f"Error writing JSON to file: {e}"
        log_error(error_message)
        print(error_message)
else:
    error_message = "DataFrame is empty. No data to write to JSON file."
    log_error(error_message)
    print(error_message)
