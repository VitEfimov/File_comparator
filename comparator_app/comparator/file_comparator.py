import os
from tabulate import tabulate
from comparator_app.reports.report_methods import total_report
from comparator_app.utils.colors import Colors
from comparator_app.comparator.sheet_comparator import compare_sheets
from comparator_app.configurator import package_report_path, package1_directory, package2_directory, errors, one_file_report,print_total_table


def compare_directory(create_reports):
    TOTAL_REPORT_FILE = os.path.join(package_report_path, "Total_Results.xlsx")
    total_print = []
    missed_files = []
    
    try:
        if set(x for x in os.listdir(package1_directory)) != set(x for x in os.listdir(package2_directory)):
            package1_files = set(os.listdir(package1_directory))
            package2_files = set(os.listdir(package2_directory))
            
            only_in_package1 = package1_files - package2_files
            only_in_package2 = package2_files - package1_files
            missed_files = sorted(only_in_package1 | only_in_package2)
            
            errors.append(Colors.colored_print(f'ERROR: directories: {package1_directory} and {package2_directory} do not have the same files', 'FAIL', True))
            
            if only_in_package1:
                errors.append(Colors.colored_print(f'Files only in {package1_directory}: {only_in_package1}', 'FAIL', True))
            if only_in_package2:
                errors.append(Colors.colored_print(f'Files only in {package2_directory}: {only_in_package2}', 'FAIL', True))
                
    except FileNotFoundError as e:
        Colors.colored_print(f'{e}', "FAIL")
        
    files1 = {x for x in os.listdir(package1_directory) if x.endswith(('.xlsx', 'csv'))}
    files2 = {x for x in os.listdir(package2_directory) if x.endswith(('.xlsx', 'csv'))}
    
    common_files = files1.intersection(files2)
    critical = {'number': 0, 'file_name': []}
    critical_file_details = []
    files_qty = len(common_files)
    i = 0
    
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
    
    if len(missed_files) > 0:
        for x in missed_files:
            missed_each = {
                'file_name': f'{x}, file missed: NOT EXECUTED',
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
            total_print.append(missed_each)
            
    for file_name in common_files:
        i = i + 1
        file_path1 = os.path.join(package1_directory, file_name)
        file_path2 = os.path.join(package2_directory, file_name)
        if one_file_report == file_name:
            create_reports = True
        
        total = compare_sheets(file_path1, file_path2, create_reports)
        
        for each in total:
            if each['file_name'] in total_print:
                total_each_file = {
                    'file_name': '',
                    'file_executions': 0,
                    'sheet_name': each['sheet_name'],
                    'executed_sheets': each['executed_sheets'],
                    'total_rows': each['total_rows'],
                    'pass': each['pass'],
                    'number_fail': each['number_fail'],
                    'key_fail': each['key_fail'],
                    'sum_value_differences': each['sum_value_differences'],
                    'max_difference': each['max_difference']
                }
            else:
                total_each_file = {
                    'file_name': file_name,
                    'file_executions': i,
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
            
        if one_file_report == file_name:
            create_reports = False
            
        # print(total_print)
            
        if not total:
            critical['number'] += 1
            critical['file_name'].append(file_name)
            critical_file_details.append(critical)
            Colors.colored_print(f'ERROR: comparation failed for {file_name}', 'FAIL')
            
    Colors.colored_print(f'\n#############################################################'
                         f'\n                   COMPIlATION COMPLEATED'
                         f'\n#############################################################'
                         f'\n from {files_qty} files compared', 'HEADER')
    
    if critical['number'] > 0:
        Colors.colored_print(f'PAY ATTENTION\nCRITICAL ERROR {critical["file_name"]} NOT EXECUTED', 'FAIL')
        
    error_print = {'file_name': '', 'sheet_name': ''}
    
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
            ]
                for x in total_print
        ]
        
        table = tabulate(data, headers=headers, tablefmt='double')
        print(table)
    else:
        for x in total_print:
            file_name = x['file_name']
            file_executions = x['file_executions']
            sheet_name = x['sheet_name']
            executed_sheets = x['executed_sheets']
            total_rows = x['total_rows']
            passed = x['pass']
            number_fail =x['number_fail']
            key_fail = x['key_fail']
            total_each_file = x['sum_value_differences']
            maximal_difference = x['max_difference']

            if executed_sheets > 0:
                summary['executed_sheets'] += 1

            summary['total_rows'] += total_rows
            summary['pass'] += passed
            summary['number_fail'] += number_fail
            summary['key_fail'] += key_fail
            summary['sum_value_differences'] += x['sum_value_differences']
            summary['max_difference'] = max(summary['max_difference'], x['max_difference'])
            
            if number_fail > 0:
                number_fail = Colors.colored_print(number_fail, "FAIL", True)
            if key_fail > 0:
                key_fail = Colors.colored_print(key_fail, "FAIL", True)
                
            if 0.1 >= total_each_file >= -0.1:
                total_each_file = Colors.colored_print(total_each_file, "OKGREEN", True)
            elif 0.9 >= total_each_file >= -0.9:
                total_each_file = Colors.colored_print(total_each_file, "WARNING", True)
            else:
                total_each_file = Colors.colored_print(total_each_file, "FAIL", True)
            
            if 0.1 >= maximal_difference >= -0.1:
                maximal_difference = Colors.colored_print(maximal_difference, "OKGREEN", True)
            elif 0.9 >= maximal_difference >= -0.9:
                maximal_difference = Colors.colored_print(maximal_difference, "WARNING", True)
            else:
                maximal_difference = Colors.colored_print(maximal_difference, "FAIL", True)
                
            if passed < 1:
                passed = Colors.colored_print(passed, "FAIL", True)
            else:
                passed = Colors.colored_print(passed, "OKGREEN", True)
                
            if 'NOT EXECUTED' in sheet_name or 'missed' in sheet_name or 'NOT EXECUTED' in file_name:
                file_name = Colors.colored_print(file_name, "FAIL", True)
                sheet_name = Colors.colored_print(sheet_name, "FAIL", True)
            
            print(
                f'file_name: {file_name} | '
                f'file_executions: {file_executions} | '
                f'sheet_name: {sheet_name} | '
                f'executed_sheets: {executed_sheets} | '
                f'total_rows: {total_rows} | '
                f'passed: {passed} | '
                f'number_fail: {number_fail} | '
                f'key_fail: {key_fail} | '
                f'sum_value_differences: {total_each_file} | '
                f'max_difference: {maximal_difference}'
            )
    print()

    total_print.append(summary)
    
    if len(errors) > 0:
        i = 0
        for x in errors:
            Colors.colored_print(f'{x}')
            
            error_print.update({
                'file_name': i,
                'sheet_name': x
            })
    if len(total_print) - critical['number'] < files_qty:
        unmatched_files = [x for x in common_files if x  not in [file['file_name'] for file in total_print]]
        Colors.colored_print(f'FATAL ERROR: {critical["number"]} file(s) did not compare: {unmatched_files}', 'FAIL')
        
    total_report(total_print, TOTAL_REPORT_FILE)


