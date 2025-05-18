import pandas as pd
from utils.colors import Colors

def read_file(file_path):
    try:
        if file_path.endswith('.xlsx'):
            sheets = pd.read_excel(file_path, dtype=str, keep_default_na=False, sheet_name=None)
            return sheets
        elif file_path.endswith('.csv'):
            df = pd.read_csv(file_path, dtype=str, keep_default_na=False)
            return {'sheet': df}
        else:
            raise ValueError("VALUE ERROR! Use .csv or .xlsx files")
    except FileNotFoundError:
        Colors.colored_print(f"FILE NOT FOUND: {file_path}", "FAIL")