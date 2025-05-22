import os
from comparator_app.reader.csv_xlsx_reader import read_file
from comparator_app.configurator import errors
from comparator_app.comparator.table_comparator import compare_table
from comparator_app.utils.colors import Colors

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
    all_differences = []
    all_highlighted = []


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

        total, highlighted, differences, = compare_table(
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
        
        all_differences.append({
            'file_name': file_name,
            'sheet_name': sheet,
            'differences': differences
        })
        
        all_highlighted.append({
            'file_name': file_name,
            'sheet_name': sheet,
            'highlighted': highlighted
        })

        if total['missed_headers']:
            total_sheets['sheet_name'] = f"{sheet} headers missed: {total['missed_headers']}"
            
        print(len(all_highlighted))
        for i, item in enumerate(all_highlighted):
            print(f"{i}: file_name={item['file_name']}, sheet={item['sheet_name']}, highlights={len(item['highlighted'])}")

        total_sheets_print.append(total_sheets)
        
        # for x in all_differences:
        #     print(f'\n {x}')
            
        # for x in all_full_records:
        #     print(f'\n {x}')
        
        # print('\n\n\ntotal_sheets_print from sheet_comparator',total_sheets_print)
        # print('\n\n\nall_all_highlighted ########################',all_highlighted)
        # print('\n\n\nall_differences ########################',all_differences)

        

    return total_sheets_print, all_highlighted, all_differences

