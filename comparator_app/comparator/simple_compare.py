from comparator_app.comparator.table_comparator import compare_table
from comparator_app.reader.csv_xlsx_reader import read_file
import pandas as pd
import os


# def simple_compare(dir1, dir2, config):
    
#     df1 = read_file(dir1)
#     df2 = read_file(dir2)
#     sheet="sheet"
#     file_name="COMPARISON.xlsx",
#     file_path1="path1",
#     file_path2="path2"
    
#     print(df1.keys())
    
#     total, highlighted = compare_table(
#                 file_name,
#                 file_path1,
#                 file_path2,
#                 sheet,
#                 df1, df2,config
#             )
#     return total, highlighted

def simple_compare(file1_path, file2_path, config):

    df1 = read_file(file1_path)
    df2 = read_file(file2_path)
    if isinstance(df1, dict):
        df1 = list(df1.values())[0]
    if isinstance(df2, dict):
        df2 = list(df2.values())[0]

    file_name = "SINGLE_COMPARISON"
    sheet_name = "sheet"
        
    total, highlighted = compare_table(
        file_name=file_name,
        file_path1=file1_path,
        file_path2=file2_path,
        sheet_name=sheet_name,
        df1=df1,
        df2=df2,
        config=config
    )
    
    summary = {
        'file_name': os.path.basename(file1_path) + " | " + os.path.basename(file2_path), 
        'file_executions': 1,
        'sheet_name': sheet_name,  
        'executed_sheets': 1,
        'total_rows': total.get('total_rows', 0),
        'pass': total.get('pass', 0),
        'number_fail': total.get('number_fail', 0),
        'key_fail': total.get('key_fail', 0),
        'sum_value_differences': total.get('sum_value_differences', 0),
        'max_difference': total.get('max_difference', 0)
    }

    df_total = pd.DataFrame([summary])
    highlighted_dfs = highlighted

    return df_total, highlighted_dfs