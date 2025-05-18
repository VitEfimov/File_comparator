import os
from utils.colors import Colors
from reports.report_manager import create_report
from configurator import decimal, package_report_path, errors
from comparator.comparator_utils import dictionary, key_creator, check_headers, round_number


def compare_table(file_name,
                  file_path1,
                  file_path2,
                  sheet_name,
                  df1, df2,
                  create_reports):

    REPORT_FILE = os.path.join(package_report_path, f'report_{file_name}_{sheet_name}.xlsx')
    DIFFERENCE_FILE = os.path.join(package_report_path, f'differences_{file_name}_{sheet_name}.xlsx')
    os.makedirs(package_report_path, exist_ok=True)

    total = {
        'number_fail': 0,
        'key_fail': 0,
        'pass': 0,
        'total_rows': 0,
        'sum_value_differences': 0,
        'max_difference': 0,
        'max': 0,
        'missed_headers': 0,
        'summary_differences': []
    }

    total['missed_headers'] = check_headers(df1, df2, file_path1, file_path2, sheet_name)

    data1 = dictionary(df1)
    data2 = dictionary(df2)

    if len(data1) != len(data2):
        msg = f'ERROR: {file_name} - number of rows mismatch'
        errors.append(Colors.colored_print(msg, 'FAIL', True))

    differences = []
    full_record = []
    missed_keys = []

    dict1 = {tuple(row['key']): row['values'] for row in data1}
    dict2 = {tuple(row['key']): row['values'] for row in data2}

    if len(dict1) != len(data1) or len(dict2) != len(data2):
        data1 = key_creator(data1)
        data2 = key_creator(data2)
        dict1 = {tuple(row['key']): row['values'] for row in data1}
        dict2 = {tuple(row['key']): row['values'] for row in data2}
        Colors.colored_print(f'FAIL {file_name}, {sheet_name} - custom keys added', 'HEADER')

    keys1 = set(dict1.keys())
    keys2 = set(dict2.keys())
    all_keys = keys1.union(keys2)

    for key in all_keys:
        if key not in dict1:
            total['total_rows'] += 1
            total['key_fail'] += 1
            missed_keys.append(f'{key} missing in {file_path1}')
            continue
        if key not in dict2:
            total['total_rows'] += 1
            total['key_fail'] += 1
            missed_keys.append(f'{key} missing in {file_path2}')
            continue

        row1_val = [round_number(val) for val in dict1[key]]
        row2_val = [round_number(val) for val in dict2[key]]

        total['total_rows'] += 1
        difference = []

        if row1_val == row2_val:
            match_status_val = 'PASS'
            total['pass'] += 1
        else:
            match_status_val = 'FAIL'
            total['number_fail'] += 1

            if len(row1_val) == len(row2_val):
                row_diffs = [abs(v2 - v1) for v1, v2 in zip(row1_val, row2_val)]
                max_diff = max(row_diffs)
                total['max_difference'] = max(total['max_difference'], max_diff)

                significant_diffs = [v2 - v1 for v1, v2 in zip(row1_val, row2_val) if abs(v2 - v1) > 10 ** -decimal]
                difference = [round_number(diff) for diff in significant_diffs]

                total['sum_value_differences'] += round_number(sum(difference))

                if total['max'] < max_diff:
                    total['max'] = round_number(max_diff)
            else:
                diff1 = [val for val in row1_val if val not in row2_val]
                diff2 = [val for val in row2_val if val not in row1_val]
                difference = [abs(round_number(d)) for d in (diff1 + diff2) if abs(d) > 10 ** -decimal]
                total['sum_value_differences'] += round_number(sum(difference))

            differences.append({
                'key': key,
                'value_file1': row1_val,
                'value_file2': row2_val,
                'max_diff': round_number(max(difference) if difference else 0),
                'difference': difference
            })

        full_record.append({
            'key': key,
            'value_file1': row1_val,
            'value_file2': row2_val,
            'match': match_status_val,
            'difference': difference
        })

    for x in missed_keys:
        differences.append({'key': x})

    total['summary_differences'] = differences

    create_report(differences, full_record, DIFFERENCE_FILE, REPORT_FILE, create_reports)

    return total


# import os
# import sys
# from utils.colors import Colors
# from reports.report_manager import create_report
# from configurator import decimal, package_report_path, errors
# from comparator.comparator_utils import dictionary, key_creator, check_headers, round_number

# # sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# # from reports.manager import create_report


# def compare_table(file_name,
#                     file_path1,
#                     file_path2,
#                     sheet_name,
#                     df1, df2,
#                     create_reports):
#     REPORT_FILE = os.path.join(package_report_path, f'report_{file_name}_{sheet_name}.xlsx')
#     DIFFERENCE_FILE = os.path.join(package_report_path, f'differences_{file_name}_{sheet_name}.xlsx')
    
#     os.makedirs(package_report_path, exist_ok=True)
    
#     total = {'number_fail': 0,
#              'key_fail': 0,
#              'pass': 0,
#              'total_rows': 0,
#              'sum_value_differences': 0,
#              'max_difference': 0,
#              'max': 0,
#              'missed_headers': 0,
#              'summary_differences': 0,}
    
#     # package_label1 = 'from package1'
#     # package_label2 = 'from package2'
#     # if 'execution' 
    
#     total['missed_headers'] = check_headers(df1, df2, file_path1, file_path2, sheet_name)
    
#     data1 = dictionary(df1)
#     data2 = dictionary(df2)
    
#     if len(data1) != len(data2):
#         Colors.colored_print(f'ERROR: {file_name} length of data do not match', 'FAIL')
#         errors.append(Colors.colored_print(f'ERROR: {file_name} length of data do not match', 'FAIL'))
        
#     differences = []
#     full_record = []
#     missed_keys = []
    
#     dict1 = {tuple(row['key']): row['values'] for row in data1}
#     dict2 = {tuple(row['key']): row['values'] for row in data2}
    
#     if len(dict1) != len(data1) or len(dict2) != len(data2):
#         data1 = key_creator(data1)
#         data2 = key_creator(data2)
#         dict1 = {tuple(row['key']): row['values'] for row in data1}
#         dict2 = {tuple(row['key']): row['values'] for row in data2}
#         Colors.colored_print(f'FAIL {file_name}, {sheet_name} custom keys added', 'HEADER')
        
#     for key in dict1:
#         if key not in dict2:
#             total['total_rows'] += 1
#             total['key_fail'] += 1
#             missed_keys.append(f'{key} missed in {file_path2}')
#             continue
#     for key in dict2:
#         if key not in dict1:
#             total['total_rows'] += 1
#             total['key_fail'] += 1
#             missed_keys.append(f'{key} missed in {file_path1}')
#             continue
    
#         row1_val = [round_number(val) for val in dict1[key]]
#         row2_val = [round_number(val) for val in dict2[key]]
    
#         total['total_rows'] += 1
#         difference = []
    
#         if row1_val == row2_val:
#             match_status_val = 'PASS'
#             total['pass'] += 1
#         else:
#             match_status_val = 'FAIL'
#             total['number_fail'] += 1
#             if len(row1_val) == len(row2_val):
#                 total['max_difference'] = max(abs(v2 - v1) for v1, v2, in zip(row1_val, row2_val))
            
#                 if total['max'] < total['max_difference']:
#                     total['max'] = round_number(total['max_difference'])
                
#                 difference = [v2 - v1 for v1, v2 in zip(row1_val, row2_val) if abs(v2 - v1) > 10 ** -decimal]
#                 difference = [round_number(x) for x in difference]
#             else:
#                 difference_in_row1 = [each for each in row1_val if each not in row2_val]
#                 difference_in_row2 = [each for each in row2_val if each not in row1_val]
#                 difference = difference_in_row1 + difference_in_row2
#                 difference = [abs(diff) for diff in difference if abs(diff) > 10 ** -decimal]
            
#             # total['sum_value_differences'] = round_number(
#             #     total['sum_value_differences'] + sum(difference) if isinstance(difference, list) else difference
#             # )
#             if isinstance(difference, list):
#                 total['sum_value_differences'] += round_number(sum(difference))
        
#             differences.append({
#                 'key': key,
#                 'value_file1': row1_val,
#                 'value_file2': row2_val,
#                 'max_diff': round_number(max(difference) if isinstance(difference, list) and difference else 0),
#                 'difference': difference
#             })
#         full_record.append({
#             'key': key,
#             'value_file1': row1_val,
#             'value_file2': row2_val,
#             'match': match_status_val,
#             'difference': difference
#         })
#         # print(full_record)
#     for x in missed_keys:
#         differences.append({'key': x})
        
#     total.update({'summary_differences': differences})
    
#     create_report(differences,
#                   full_record,
#                   DIFFERENCE_FILE,
#                   REPORT_FILE,
#                   create_reports)
    
#     return total


        


