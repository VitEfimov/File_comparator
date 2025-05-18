import os
from reader.csv_xlsx_reader import read_file
from configurator import decimal, errors
from comparator.table_comparator import compare_table
from utils.colors import Colors

# Optional: Reusable default structure
def default_sheet_result():
    return {
        'file_name': '',
        'sheet_name': '',
        'executed_sheets': 0,
        'total_rows': 0,
        'pass': 0,
        'number_fail': 0,
        'key_fail': 0,
        'sum_value_differences': 0,
        'max_difference': 0,
        'summary_differences': []
    }

def compare_sheets(file_path1, file_path2, create_reports):
    sheets_file1 = read_file(file_path1)
    sheets_file2 = read_file(file_path2)

    common_sheets = set(sheets_file1.keys()) & set(sheets_file2.keys())
    missed_sheets = []

    if len(sheets_file1) != len(sheets_file2):
        missed_sheets = list((set(sheets_file1.keys()) | set(sheets_file2.keys())) - common_sheets)
    
    total_sheets_print = []

    if missed_sheets:
        errors.append(
            Colors.colored_print(
                f'ERROR: Sheet(s) {missed_sheets} missing in {file_path2}', 'FAIL', True
            )
        )
        total_missed_sheets = default_sheet_result()
        total_missed_sheets.update({
            'file_name': 'missed',
            'sheet_name': f'{missed_sheets} missing: NOT EXECUTED'
        })
        total_sheets_print.append(total_missed_sheets)

    for i, sheet in enumerate(common_sheets, start=1):
        file_name = os.path.basename(file_path1)

        try:
            df1 = sheets_file1[sheet]
            df2 = sheets_file2[sheet]
        except Exception as e:
            errors.append(
                Colors.colored_print(
                    f'ERROR: {e} - Sheet name mismatch or missing in {file_path1}', 'FAIL', True
                )
            )
            total_sheets = default_sheet_result()
            total_sheets.update({
                'file_name': file_name,
                'sheet_name': f'{sheet} sheet mismatch: NOT EXECUTED'
            })
            total_sheets_print.append(total_sheets)
            continue

        total_sheets = default_sheet_result()
        total_sheets.update({
            'file_name': file_name,
            'sheet_name': sheet,
            'executed_sheets': i
        })

        total = compare_table(
            file_name,
            file_path1,
            file_path2,
            sheet,
            df1, df2,
            create_reports
        )

        total_sheets.update({
            'total_rows': total['total_rows'],
            'pass': total['pass'],
            'number_fail': total['number_fail'],
            'key_fail': total['key_fail'],
            'sum_value_differences': total['sum_value_differences'],
            'max_difference': total['max'],
            'summary_differences': total['summary_differences']
        })

        if total['missed_headers']:
            total_sheets['sheet_name'] = f"{sheet} headers missed: {total['missed_headers']}"

        total_sheets_print.append(total_sheets)

    return total_sheets_print


# import os
# import re
# from reader.csv_xlsx_reader import read_file
# from configurator import decimal,errors
# from comparator.table_comparator import compare_table
# from utils.colors import Colors



# def compare_sheets(file_path1,
#                    file_path2,
#                    create_reports):
#     sheets_file1 = read_file(file_path1)
#     sheets_file2 = read_file(file_path2)
#     common_sheets = set(sheets_file1.keys()) & set(sheets_file2.keys())

#     missed_sheets = list(set(sheets_file1.keys()) - set(sheets_file2.keys()))
#     total_sheets_print = []
    
#     if len(missed_sheets) > 0:
#         errors.append(Colors.colored_print(f'ERROR: Sheet(s) {missed_sheets} missing in {file_path2}'))
#         total_missed_sheets = {
#             'file_name': 'missed',
#             'sheet_name': f'{missed_sheets} has missed: NOT EXECUTED',
#             'executed_sheets': 0,
#             'total_rows': 0,
#             'pass': 0,
#             'number_fail': 0,
#             'key_fail': 0,
#             'sum_value_differences': 0,
#             'max_difference': 0
#         }
#         total_sheets_print.append(total_missed_sheets)
    
#     # i = 0
    
#     # for sheet in common_sheets:
#     #     i = i + 1
#     for i, sheet in enumerate(common_sheets, start=1):
#         file_name = os.path.basename(file_path1)
        
#         try:
#             df1 = sheets_file1[sheet]
#             df2 = sheets_file2[sheet]
#         except Exception as e:
#             errors.append(Colors.colored_print(f'ERROR {e} sheet has a different name: {file_path1}'))
            
#             total_sheets = {
#                 'file_name': file_name,
#                 'sheet_name': f'{sheet} seets is not the same, NOT EXECUTED',
#                 'executed_sheets': 0,
#                 'total_rows': 0,
#                 'pass': 0,
#                 'number_fail': 0,
#                 'key_fail': 0,
#                 'sum_value_differences': 0,
#                 'max_difference': 0,
#                 'summary_differences': []
#             }
#             total_sheets_print.append(total_sheets)
#             continue
        
#         total_sheets = {
#             'file_name': file_name,
#             'sheet_name': sheet,
#             'executed_sheets': 0,
#             'total_rows': 0,
#             'pass': 0,
#             'number_fail': 0,
#             'key_fail': 0,
#             'sum_value_differences': 0,
#             'max_difference': 0,
#             'summary_differences': []
#         }
        
#         total = compare_table(
#             file_name,
#             file_path1,
#             file_path2,
#             sheet,
#             df1, df2,
#             create_reports
#         )
        
#         total_sheets.update({
#             'executed_sheets': i,
#             'total_rows': total['total_rows'],
#             'pass': total['pass'],
#             'number_fail': total['number_fail'],
#             'key_fail': total['key_fail'],
#             'sum_value_differences': total['sum_value_differences'],
#             'max_difference': total['max'],
#             'summary_differences': total['summary_differences']
#         })
        
#         if len(total['missed_headers']) > 0:
#             total_sheets.update({
#                 'sheet_name': f"{sheet} headers missed: {total['missed_headers']}"

#             })
#         # if len(total['summary_differences']) > 0:
#         #     total_sheets.update({
#         #         'sheet_name': f'{sheet} headers missed: {total['missed_headers']}'
#         #     })
        
#         total_sheets_print.append(total_sheets)
#         # print('total_sheets_print', total_sheets_print)
#     return total_sheets_print