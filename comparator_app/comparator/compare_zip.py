import os
import pandas as pd
from tabulate import tabulate
# from comparator_app.comparator.sheet_comparator import compare_sheets
# from comparator_app.comparator.comparator_utils import round_number

# from comparator.sheet_comparator import compare_sheets
# from comparator.comparator_utils import round_number

from comparator_app.comparator.sheet_comparator import compare_sheets
from comparator_app.comparator.comparator_utils import round_number


def compare_directory(dir1, dir2, config):
    errors = config.get('errors', [])
    decimal = config.get('decimal', 5)
    highlighted_output = config.get('highlighted_output', True)
    total_print = []
    missed_files = []

    try:
        if set(os.listdir(dir1)) != set(os.listdir(dir2)):
            files1_set = set(os.listdir(dir1))
            files2_set = set(os.listdir(dir2))
            only_in_1 = files1_set - files2_set
            only_in_2 = files2_set - files1_set
            missed_files = sorted(only_in_1 | only_in_2)

            errors.append(f'ERROR: directories: {dir1} and {dir2} do not have the same files')
            if only_in_1:
                errors.append(f'Files only in {dir1}: {only_in_1}')
            if only_in_2:
                errors.append(f'Files only in {dir2}: {only_in_2}')
    except FileNotFoundError as e:
        print(f'{e}', "FAIL")

    files1 = {f for f in os.listdir(dir1) if f.endswith(('.xlsx', 'csv'))}
    files2 = {f for f in os.listdir(dir2) if f.endswith(('.xlsx', 'csv'))}
    common_files = files1.intersection(files2)

    critical = {'number': 0, 'file_name': []}
    critical_file_details = []
    files_qty = len(common_files)
    summary = {
        'file_name': 'TOTAL',
        'file_executions': len(common_files),
        'sheet_name': '',
        'executed_sheets': 0,
        'total_rows': 0,
        'pass': 0,
        'number_fail': 0,
        'key_fail': 0,
        'sum_value_differences': 0,
        'max_difference': 0
    }

    for missed in missed_files:
        missed_entry = {
            'file_name': f'missed: {missed}',
            'file_executions': 0,
            'sheet_name': 'NOT EXECUTED',
            'executed_sheets': 0,
            'total_rows': 0,
            'pass': 0,
            'number_fail': 0,
            'key_fail': 0,
            'sum_value_differences': 0,
            'max_difference': 0
        }
        total_print.append(missed_entry)
        
    highlighted_dfs = []

    for idx, file_name in enumerate(common_files, start=1):
        file_path1 = os.path.join(dir1, file_name)
        file_path2 = os.path.join(dir2, file_name)

        total, highlighted = compare_sheets(file_path1, file_path2, config)

        highlighted_dfs.extend(highlighted)

        for each in total:
         
            total_each_file = {
                'file_name': file_name,
                'file_executions': idx,
                'sheet_name': each['sheet_name'],
                'executed_sheets': each['executed_sheets'],
                'total_rows': each['total_rows'],
                'pass': each['pass'],
                'number_fail': each['number_fail'],
                'key_fail': each['key_fail'],
                'sum_value_differences': each['sum_value_differences'],
                'max_difference': each['max_difference']
            }
            total_print.append(total_each_file)

        if not total:
            critical['number'] += 1
            critical['file_name'].append(file_name)
            critical_file_details.append(critical)
            print(f'ERROR: comparation failed for {file_name}', 'FAIL')

    if critical['number'] > 0:
        print(f'PAY ATTENTION\nCRITICAL ERROR {critical["file_name"]} NOT EXECUTED', 'FAIL')
        
    
    if not highlighted_output:
        
        print(f'\n\nCOMPILATION RESULTS'
          f'\n\n{files_qty} files compared')
        for x in total_print:

            executed_sheets = x['executed_sheets']
            total_rows = x['total_rows']
            passed = x['pass']
            number_fail = x['number_fail']
            key_fail = x['key_fail']
            sum_diff = x['sum_value_differences']
            max_diff = x['max_difference']
            
            if executed_sheets > 0:
                summary['executed_sheets'] += 1
            summary['total_rows'] += total_rows
            summary['pass'] += passed
            summary['number_fail'] += number_fail
            summary['key_fail'] += key_fail
            summary['sum_value_differences'] += sum_diff
            summary['max_difference'] = max(summary['max_difference'], max_diff)

        headers = [
            'file_name', 'file_executions', 'sheet_name',
            'executed_sheets', 'total_rows', 'pass',
            'number_fail', 'key_fail',
            'sum_value_differences', 'max_difference'
        ]
        
        for x in total_print:
            if len(x['file_name']) > 30:
                x['file_name'] = x['file_name'][:30] 
            if len(x['sheet_name']) > 30:
                x['sheet_name'] = x['sheet_name'][:30] 

            x['sum_value_differences'] = f"{round_number(x['sum_value_differences'], decimal):.{decimal}f}"
            x['max_difference'] = f"{round_number(x['max_difference'], decimal):.{decimal}f}"
                
        data = [[
            x['file_name'], x['file_executions'], x['sheet_name'],
            x['executed_sheets'], x['total_rows'], x['pass'],
            x['number_fail'], x['key_fail'],
            x['sum_value_differences'], x['max_difference']
        ] for x in total_print]
        # data.append(summary)


        print(tabulate(data, headers=headers, tablefmt='double'))
    else:
        for x in total_print:

            executed_sheets = x['executed_sheets']
            total_rows = x['total_rows']
            passed = x['pass']
            number_fail = x['number_fail']
            key_fail = x['key_fail']
            sum_diff = x['sum_value_differences']
            max_diff = x['max_difference']
            
            if executed_sheets > 0:
                summary['executed_sheets'] += 1
            summary['total_rows'] += total_rows
            summary['pass'] += passed
            summary['number_fail'] += number_fail
            summary['key_fail'] += key_fail
            summary['sum_value_differences'] += sum_diff
            summary['max_difference'] = max(summary['max_difference'], max_diff)

    print()

    total_print.append(summary)

    if len(errors) > 0:
        for i, err in enumerate(errors):
            print(f'{err}')
    
    unmatched_files = [x for x in common_files if x not in [file['file_name'] for file in total_print]]
    if len(total_print) - critical['number'] < files_qty:
        print(f'FATAL ERROR: {critical["number"]} file(s) did not compare: {unmatched_files}', 'FAIL')

    df_total = pd.DataFrame(total_print)

    return df_total, highlighted_dfs

