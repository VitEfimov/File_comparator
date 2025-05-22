import os
import pandas as pd

from tabulate import tabulate
from comparator_app.utils.colors import Colors
from comparator_app.comparator.sheet_comparator import compare_sheets


def compare_directory(dir1, dir2, config):
    create_reports = config.get('create_reports', False)
    one_file_report = config.get('one_file_report', None)
    print_total_table = config.get('print_total_table', False)
    errors = config.get('errors', [])

    # TOTAL_REPORT_FILE = total_report_path
    total_print = []
    missed_files = []

    try:
        if set(os.listdir(dir1)) != set(os.listdir(dir2)):
            files1_set = set(os.listdir(dir1))
            files2_set = set(os.listdir(dir2))
            only_in_1 = files1_set - files2_set
            only_in_2 = files2_set - files1_set
            missed_files = sorted(only_in_1 | only_in_2)

            errors.append(Colors.colored_print(
                f'ERROR: directories: {dir1} and {dir2} do not have the same files', 'FAIL', True))
            if only_in_1:
                errors.append(Colors.colored_print(
                    f'Files only in {dir1}: {only_in_1}', 'FAIL', True))
            if only_in_2:
                errors.append(Colors.colored_print(
                    f'Files only in {dir2}: {only_in_2}', 'FAIL', True))
    except FileNotFoundError as e:
        Colors.colored_print(f'{e}', "FAIL")

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
            'file_name': f'{missed}, file missed: NOT EXECUTED',
            'file_executions': 0,
            'sheet_name': 'NONE',
            'executed_sheets': 0,
            'total_rows': 0,
            'pass': 0,
            'number_fail': 0,
            'key_fail': 0,
            'sum_value_differences': 0,
            'max_difference': 0
        }
        total_print.append(missed_entry)

    for idx, file_name in enumerate(common_files, start=1):
        file_path1 = os.path.join(dir1, file_name)
        file_path2 = os.path.join(dir2, file_name)
        local_create_reports = create_reports or (one_file_report == file_name)

        total, highlighted, differences = compare_sheets(file_path1, file_path2, local_create_reports)

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
            Colors.colored_print(f'ERROR: comparation failed for {file_name}', 'FAIL')

    print(f'\n\nCOMPILATION RESULTS'
          f'\n\n{files_qty} files compared')

    if critical['number'] > 0:
        Colors.colored_print(f'PAY ATTENTION\nCRITICAL ERROR {critical["file_name"]} NOT EXECUTED', 'FAIL')

    if print_total_table:
        headers = [
            'file_name', 'file_executions', 'sheet_name',
            'executed_sheets', 'total_rows', 'pass',
            'number_fail', 'key_fail',
            'sum_value_differences', 'max_difference'
        ]
        data = [[
            x['file_name'], x['file_executions'], x['sheet_name'],
            x['executed_sheets'], x['total_rows'], x['pass'],
            x['number_fail'], x['key_fail'],
            x['sum_value_differences'], x['max_difference']
        ] for x in total_print]

        print(tabulate(data, headers=headers, tablefmt='double'))

    else:
        for x in total_print:
            file_name = x['file_name']
            file_executions = x['file_executions']
            sheet_name = x['sheet_name']
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



            print(
                f'file_name: {file_name} | '
                f'file_executions: {file_executions} | '
                f'sheet_name: {sheet_name} | '
                f'executed_sheets: {executed_sheets} | '
                f'total_rows: {total_rows} | '
                f'passed: {passed} | '
                f'number_fail: {number_fail} | '
                f'key_fail: {key_fail} | '
                f'sum_value_differences: {sum_diff} | '
                f'max_difference: {max_diff}'
            )

    print()
    total_print.append(summary)

    if len(errors) > 0:
        for i, err in enumerate(errors):
            Colors.colored_print(f'{err}')
    
    unmatched_files = [x for x in common_files if x not in [file['file_name'] for file in total_print]]
    if len(total_print) - critical['number'] < files_qty:
        Colors.colored_print(f'FATAL ERROR: {critical["number"]} file(s) did not compare: {unmatched_files}', 'FAIL')

    df_total = pd.DataFrame(total_print)

    df_diff = differences
    highlighted_dfs = highlighted
    # print('\n\n\nhighlighted_dfs from compare.zip',highlighted_dfs)
    # print('\n\n\ndf_diff from compare.zip',df_diff)
    
    # print(len(highlighted_dfs))
    # for i, item in enumerate(highlighted_dfs):
    #     print(f"{i}: file_name={item['file_name']}, sheet={item['sheet_name']}, highlights={len(item['highlighted'])}")


    return df_total, df_diff, highlighted_dfs

