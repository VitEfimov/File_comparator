from comparator_app.comparator.comparator_utils import check_headers, round_number, is_a_number
import pandas as pd

def compare_table_by_sorted_strings(file_name,
                                    file_path1,
                                    file_path2,
                                    sheet_name,
                                    df1, df2, config):

    errors = config.get('errors', [])
    decimal = config.get('decimal', 5)
    # print(decimal)

    total = {
        'number_fail': 0,
        'key_fail': 0,  # string values
        'pass': 0,
        'total_rows': 0,
        'sum_value_differences': 0,
        'max_difference': 0,
        'max': 0,
        'missed_headers': 0,
        'summary_differences': []
    }

    total['missed_headers'] = check_headers(df1, df2, file_path1, file_path2, sheet_name, errors)

    string_cols = [col for col in df1.columns if not all(is_a_number(v) for v in df1[col])]
    if not string_cols:
        errors.append(f'FAIL: No string columns found in {sheet_name}')
        return total, []
    
    # print("string_cols\n\n\n",string_cols)

    df1 = df1.copy()
    df2 = df2.copy()
    df1['original_index'] = df1.index
    df2['original_index'] = df2.index

    df1_sorted = df1.sort_values(by=string_cols).reset_index(drop=True)
    df2_sorted = df2.sort_values(by=string_cols).reset_index(drop=True)
    
    
    for x in df1_sorted:
        print("df1_sorted:   ",x)
        
    for x in df2_sorted:
        print("df2_sorted:   ",x)

    differences = []
    highlighted = []
    
    
    len1 = len(df1_sorted)
    len2 = len(df2_sorted)


    if len1 != len2:
        errors.append(f'ERROR: {file_name} - number of rows mismatch ({len1} vs {len2})')
        
        longer_df = df1_sorted if len1 > len2 else df2_sorted
        shorter_len = min(len1, len2)
        source_file = "file1" if len1 > len2 else "file2"

        for i in range(shorter_len, len(longer_df)):
            row = longer_df.iloc[i]
            row_result = [str(val).strip() for col, val in row.items() if col != 'original_index']
            original_index = int(row.get('original_index', -1))

            differences.append({
                'row_index': i,
                f'original_row_{source_file}': original_index,
                'value_file1': row_result if source_file == "file1" else [],
                'value_file2': row_result if source_file == "file2" else [],
                'difference': ["MISSING ROW"],
                'max_diff': None
            })

            highlighted.append({
                'row_index': i,
                f'original_row_{source_file}': original_index,
                'value_file1': row_result if source_file == "file1" else [],
                'value_file2': row_result if source_file == "file2" else [],
                'match': 'FAIL',
                'difference': ["MISSING ROW"],
                'max_diff': None
            })
            
            if len1 < len2:
                padding = pd.DataFrame([{col: '' for col in df1_sorted.columns}], index=[0] * (len2 - len1))
                df1_sorted = pd.concat([df1_sorted, padding], ignore_index=True)
            elif len2 < len1:
                padding = pd.DataFrame([{col: '' for col in df2_sorted.columns}], index=[0] * (len1 - len2))
                df2_sorted = pd.concat([df2_sorted, padding], ignore_index=True)

    # max_rows = max(len(df1_sorted), len(df2_sorted))
    max_rows = max(len1, len2)
    
    # key_difference = []
    # number_difference = []
    # differences = []
    # highlighted = []

    for i in range(max_rows):
        total['total_rows'] += 1
        try:
            row1 = df1_sorted.iloc[i] if i < len(df1_sorted) else pd.Series(dtype=object)
            row2 = df2_sorted.iloc[i] if i < len(df2_sorted) else pd.Series(dtype=object)
            
            print("row1:    ",row1)
            print("row2:    ",row2)


            match_status_val = 'PASS'
            key_difference = []
            number_difference = []
            difference = []
            max_diff = 0

            row_result1 = []
            row_result2 = []

            string_mismatch_found = False

            for col in df1.columns:
                if col == 'original_index':
                    continue  # Skip this helper column

                val1 = row1.get(col, '')
                val2 = row2.get(col, '')

                if is_a_number(val1) and is_a_number(val2):
                    val1 = round_number(val1, decimal)
                    val2 = round_number(val2, decimal)
                    diff = round_number(abs(val2 - val1), decimal)

                    if diff > 10 ** -decimal:
                        match_status_val = 'FAIL'
                        difference.append(val2 - val1)
                        max_diff = max(max_diff, diff)
                        total['sum_value_differences'] += diff

                    row_result1.append(val1)
                    row_result2.append(val2)

                else:
                    val1_str = str(val1).strip()
                    val2_str = str(val2).strip()
                    row_result1.append(val1_str)
                    row_result2.append(val2_str)

                    if val1_str != val2_str:
                        match_status_val = 'FAIL'
                        difference.append(f"'{val1_str}' vs '{val2_str}'")
                        string_mismatch_found = True
                        
            # print("row_result1: ",row_result1)
            # print("row_result2: ",row_result2)

            if match_status_val == 'PASS':
                total['pass'] += 1
            else:
                total['number_fail'] += 1
                total['max_difference'] = max(total['max_difference'], max_diff)
                total['max'] = max(total['max'], max_diff)
                if string_mismatch_found:
                    total['key_fail'] += 1

                differences.append({
                    'row_index': i,
                    'original_row_file1': int(row1.get('original_index', -1)),
                    'original_row_file2': int(row2.get('original_index', -1)),
                    'value_file1': row_result1,
                    'value_file2': row_result2,
                    'difference': difference,
                    'max_diff': max_diff
                })

            highlighted.append({
                'row_index': i,
                'original_row_file1': int(row1.get('original_index', -1)),
                'original_row_file2': int(row2.get('original_index', -1)),
                'value_file1': row_result1,
                'value_file2': row_result2,
                'match': match_status_val,
                'difference': difference,
                'max_diff': max_diff
            })

        except Exception as e:
            errors.append(f'FAIL: Error comparing row {i} in {sheet_name}: {e}')

    total['summary_differences'] = differences
    
    # print(highlighted)
    return total, highlighted


# from comparator_app.comparator.comparator_utils import check_headers, round_number, is_a_number
# import pandas as pd


# def compare_table_by_sorted_strings(file_name,
#                                     file_path1,
#                                     file_path2,
#                                     sheet_name,
#                                     df1, df2, config):

#     errors = config.get('errors', [])
#     decimal = config.get('decimal', 5)

#     total = {
#         'number_fail': 0,
#         'pass': 0,
#         'total_rows': 0,
#         'sum_value_differences': 0,
#         'max_difference': 0,
#         'max': 0,
#         'missed_headers': 0,
#         'summary_differences': []
#     }

#     # Header check
#     total['missed_headers'] = check_headers(df1, df2, file_path1, file_path2, sheet_name, errors)

#     # Identify string columns
#     string_cols = [col for col in df1.columns if not all(is_a_number(v) for v in df1[col])]
#     if not string_cols:
#         errors.append(f'FAIL: No string columns found in {sheet_name}')
#         return total, []

#     # Sort by all string columns
#     df1_sorted = df1.sort_values(by=string_cols).reset_index(drop=True)
#     df2_sorted = df2.sort_values(by=string_cols).reset_index(drop=True)

#     if len(df1_sorted) != len(df2_sorted):
#         errors.append(f'ERROR: {file_name} - number of rows mismatch ({len(df1_sorted)} vs {len(df2_sorted)})')

#     max_rows = max(len(df1_sorted), len(df2_sorted))
#     differences = []
#     highlighted = []

#     for i in range(max_rows):
#         total['total_rows'] += 1
#         try:
#             row1 = df1_sorted.iloc[i] if i < len(df1_sorted) else pd.Series(dtype=object)
#             row2 = df2_sorted.iloc[i] if i < len(df2_sorted) else pd.Series(dtype=object)

#             match_status_val = 'PASS'
#             difference = []
#             max_diff = 0

#             row_result1 = []
#             row_result2 = []

#             for col in df1.columns:
#                 val1 = row1.get(col, '')
#                 val2 = row2.get(col, '')

#                 if is_a_number(val1) and is_a_number(val2):
#                     val1 = round_number(val1, decimal)
#                     val2 = round_number(val2, decimal)
#                     diff = round_number(abs(val2 - val1), decimal)

#                     if diff > 10 ** -decimal:
#                         match_status_val = 'FAIL'
#                         difference.append(val2 - val1)
#                         max_diff = max(max_diff, diff)
#                         total['sum_value_differences'] += diff
#                     row_result1.append(val1)
#                     row_result2.append(val2)
#                 else:
#                     if str(val1).strip() != str(val2).strip():
#                         match_status_val = 'FAIL'
#                         difference.append(f"'{val1}' vs '{val2}'")
#                     row_result1.append(str(val1).strip())
#                     row_result2.append(str(val2).strip())

#             if match_status_val == 'PASS':
#                 total['pass'] += 1
#             else:
#                 total['number_fail'] += 1
#                 total['max_difference'] = max(total['max_difference'], max_diff)
#                 total['max'] = max(total['max'], max_diff)

#                 differences.append({
#                     'row_index': i,
#                     'value_file1': row_result1,
#                     'value_file2': row_result2,
#                     'difference': difference,
#                     'max_diff': max_diff
#                 })

#             highlighted.append({
#                 'row_index': i,
#                 'value_file1': row_result1,
#                 'value_file2': row_result2,
#                 'match': match_status_val,
#                 'difference': difference,
#                 'max_diff': max_diff
#             })

#         except Exception as e:
#             errors.append(f'FAIL: Error comparing row {i} in {sheet_name}: {e}')

#     total['summary_differences'] = differences
#     return total, highlighted
