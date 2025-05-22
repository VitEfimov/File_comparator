import os
import pandas as pd
from openpyxl import load_workbook
from comparator_app.reports.report_utils import apply_border, column_widths, highlight_cells, has_not_expected_or_missed, has_not_expected, is_positive_number, is_zero
from comparator_app.reports.styles import red_fill, green_fill, bold_font
from comparator_app.utils.colors import Colors
from openpyxl import Workbook
from openpyxl.styles import PatternFill
from openpyxl.utils import get_column_letter
from comparator_app.configurator import decimal


def highlighted_report(file_name, sheet_name, records, output_file):
    wb = Workbook()
    ws = wb.active
    ws.title = sheet_name

    headers = ["Key", "Value File 1", "Value File 2", "Match", "Max_difference", "Difference"]
    ws.append(headers)
    

    pass_fill = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")
    fail_fill = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")
    print(f"highlighted: {records}")

    for record in records:
 
        
        key_raw = record.get('key', "")
    
        if isinstance(key_raw, str) or "missing" in str(key_raw).lower():
            key = str(key_raw)
        else:
            key = " | ".join(key_raw)
        value_file1 = str(record.get('value_file1', []))
        value_file2 = str(record.get('value_file2', []))
        match = record.get('match', "FAIL")
        difference = str(record.get('difference', []))
        max_diff = record.get('max_diff', "")
        
        row = [key, value_file1, value_file2, match, difference, max_diff]
        ws.append(row)
        
        fill = None
        try:
            if isinstance(max_diff, (int, float)) and abs(max_diff) > 10 ** -decimal:
                fill = fail_fill
        except:
            pass

        if fill:
            for col in range(1, len(headers)+1):
                ws.cell(row=ws.max_row, column=col).fill = fill

        fill = pass_fill if match == "PASS" else fail_fill
        for col in range(1, len(headers)+1):
            ws.cell(row=ws.max_row, column=col).fill = fill
            
        apply_border(ws)

    # Auto-width
    for col in ws.columns:
        max_length = max(len(str(cell.value)) if cell.value else 0 for cell in col)
        ws.column_dimensions[get_column_letter(col[0].column)].width = max_length + 2

    wb.save(output_file)

# def difference_report(file_name, sheet_name, records, output_file):
#     wb = Workbook()
#     ws = wb.active
#     ws.title = sheet_name

#     headers = ["Key", "Value File 1", "Value File 2", "Max Difference", "Difference"]
#     ws.append(headers)

#     pass_fill = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")
#     fail_fill = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")

#     for record in records:
#         key = " | ".join(record.get('key', ("", "")))
#         value_file1 = str(record.get('value_file1', [])) if 'value_file1' in record else ""
#         value_file2 = str(record.get('value_file2', [])) if 'value_file2' in record else ""
#         max_diff = record.get('max_diff', "")
#         difference = str(record.get('difference', [])) if 'difference' in record else ""

#         row = [key, value_file1, value_file2, max_diff, difference]
#         ws.append(row)

#         # Apply red fill only if max_diff is a number and > threshold
#         fill = None
#         try:
#             if isinstance(max_diff, (int, float)) and abs(max_diff) > 10 ** -decimal:
#                 fill = fail_fill
#         except:
#             pass

#         if fill:
#             for col in range(1, len(headers)+1):
#                 ws.cell(row=ws.max_row, column=col).fill = fill

#     for col in ws.columns:
#         max_length = max(len(str(cell.value)) if cell.value else 0 for cell in col)
#         ws.column_dimensions[get_column_letter(col[0].column)].width = max_length + 2

#     wb.save(output_file)

# def difference_report(file_name, sheet_name, records, output_file):
#     # from openpyxl import Workbook
#     # from openpyxl.styles import PatternFill
#     # from openpyxl.utils import get_column_letter

#     wb = Workbook()
#     ws = wb.active
#     ws.title = sheet_name

#     headers = ["Key", "Value File 1", "Value File 2", "Max_differnce", "Difference"]
#     ws.append(headers)
    
#     print(file_name, sheet_name)

#     # Styles
#     pass_fill = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")
#     fail_fill = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")
#     print(f"file_name: {file_name}")
#     print(f"sheet_name: {sheet_name}")
#     print(f"highlighted: {records}")
#     # print(f"differences: {differences}")

#     for record in records:
#         # print("record", record)
#         key = " | ".join(record.get('key', ("", "")))
#         # key = str(record.get('key', []))

#         value_file1 = str(record.get('value_file1', []))
#         value_file2 = str(record.get('value_file2', []))
#         max_diff = record.get('max_diff', None)
#         difference = str(record.get('difference', []))

#         row = [key, value_file1, value_file2, max_diff, difference]
#         ws.append(row)

#         fill = fail_fill if max_diff == (lambda v: isinstance(v, (int, float)) and abs(v) > 10 ** -decimal) else None
#         for col in range(1, len(headers)+1):
#             ws.cell(row=ws.max_row, column=col).fill = fill

#     # Auto-width
#     for col in ws.columns:
#         max_length = max(len(str(cell.value)) if cell.value else 0 for cell in col)
#         ws.column_dimensions[get_column_letter(col[0].column)].width = max_length + 2

#     wb.save(output_file)




def total_report(records, output_file):
    generate_excel_report(
        records=records,
        output_file=output_file,
        bold_header=True,
        highlight_rules=[
            {
                "coords": (2, 2),
                "condition": has_not_expected_or_missed,
                "fill_pass": red_fill
            },
            {
                "coords": (1, 1),
                "condition": has_not_expected,
                "fill_pass": red_fill
            },
            {
                "coords": (6, 6),
                "condition": is_positive_number,
                "fill_pass": green_fill,
                "fill_fail": red_fill
            },
            {
                "coords": (7, 10),
                "condition": is_zero,
                "fill_pass": green_fill,
                "fill_fail": red_fill
            }
        ]
    )

# def difference_report(records, output_file, decimal):
#     generate_excel_report(
#         records=records,
#         output_file=output_file,
#         highlight_rules=[
#             {
#                 "coords": "max_diff",
#                 "condition": lambda v: isinstance(v, (int, float)) and abs(v) > 10 ** -decimal,
#                 "fill_pass": red_fill,
#                 "fill_fail": green_fill
#             }
#         ]
#     )

def generate_excel_report(records, output_file: str, highlight_rules: list = None, bold_header: bool = False):
    try:
        df = pd.DataFrame(records)
        df.to_excel(output_file, index=False)

        wb = load_workbook(output_file)
        ws = wb.active

        column_widths(ws)
        apply_border(ws)
        col_name_to_idx = {cell.value: idx + 1 for idx, cell in enumerate(ws[1])}

        if highlight_rules:
            for rule in highlight_rules:
                column = rule.get("column")
                coords = rule.get("coords")
                condition = rule["condition"]
                fill_pass = rule.get("fill_pass")
                fill_fail = rule.get("fill_fail")

                if column:
                    if column not in col_name_to_idx:
                        continue
                    col_idx = col_name_to_idx[column]
                    highlight_cells(ws, (col_idx, col_idx), condition, fill_pass, fill_fail)
                elif coords:
                    highlight_cells(ws, coords, condition, fill_pass, fill_fail)

        if bold_header:
            for cell in ws[1]:
                cell.font = bold_font

        wb.save(output_file)
        Colors.colored_print(f'REPORT saved at: {output_file}', 'OKGREEN')

    except Exception as e:
        Colors.colored_print(f'ERROR creating REPORT: {e}', "FAIL")


# import pandas as pd
# from openpyxl import load_workbook
# from comparator_app.reports.report_utils import apply_border,column_widths,highlight_cells,has_not_expected_or_missed,has_not_expected,is_positive_number,is_zero
# from comparator_app.reports.styles import red_fill, green_fill, bold_font
# from comparator_app.utils.colors import Colors

# def highlighted_report(records, output_file):
#     generate_excel_report(
#         records=records,
#         output_file=output_file,
#         highlight_rules=[
#             {
#                 # "coords": (4, 4),
#                 "coords": 'match',
#                 "condition": lambda v: v == "PASS",
#                 "fill_pass": green_fill,
#                 "fill_fail": red_fill
#             }
#         ]
#     )

# def highlighted_report(records: list, sheet_name: str, output_folder: str):
#     # Prepare file path
#     file_name = f"MOCK_DATA_{sheet_name}.xlsx"
#     output_path = os.path.join(output_folder, file_name)

#     # Convert records into DataFrame
#     df = pd.DataFrame(records)

#     # Save DataFrame to Excel
#     df.to_excel(output_path, index=False, sheet_name=sheet_name)

#     # Load workbook and style
#     wb = load_workbook(output_path)
#     ws = wb.active

#     column_widths(ws)
#     apply_border(ws)

#     highlight_cells(
#         ws,
#         column_name="match",
#         condition=lambda v: v == "PASS",
#         fill_pass=green_fill,
#         fill_fail=red_fill
#     )

#     for cell in ws[1]:
#         cell.font = bold_font

#     wb.save(output_path)
#     return output_path

# def total_report(records, output_file):
#     generate_excel_report(
#         records=records,
#         output_file=output_file,
#         bold_header=True,
#         highlight_rules=[
#             {
#                 "coords": (2, 2),
#                 "condition": has_not_expected_or_missed,
#                 "fill_pass": red_fill
#             },
#             {
#                 "coords": (1, 1),
#                 "condition": has_not_expected,
#                 "fill_pass": red_fill
#             },
#             {
#                 "coords": (6, 6),
#                 "condition": is_positive_number,
#                 "fill_pass": green_fill,
#                 "fill_fail": red_fill
#             },
#             {
#                 "coords": (7, 10),
#                 "condition": is_zero,
#                 "fill_pass": green_fill,
#                 "fill_fail": red_fill
#             }
#         ]
#     )

# def difference_report(records, output_file, decimal):
#     generate_excel_report(
#         records=records,
#         output_file=output_file,
#         highlight_rules=[
#             {
#                 "coords": "max_diff",
#                 "condition": lambda v: isinstance(v, (int, float)) and abs(v) > 10 ** -decimal,
#                 "fill_pass": red_fill,
#                 "fill_fail": green_fill
#             }
#         ]
#     )

# def generate_excel_report(
#     records,
#     output_file: str,
#     highlight_rules: list = None,
#     bold_header: bool = False
# ):
#     try:
#         df = pd.DataFrame(records)
#         df.to_excel(output_file, index=False)

#         wb = load_workbook(output_file)
#         ws = wb.active

#         column_widths(ws)
#         apply_border(ws)
#         col_name_to_idx = {cell.value: idx + 1 for idx, cell in enumerate(ws[1])}

#         if highlight_rules:
#             for rule in highlight_rules:
#                 column = rule.get("column")
#                 if column not in col_name_to_idx:
#                     continue  

#                 col_idx = col_name_to_idx[column]
#                 condition = rule["condition"]
#                 fill_pass = rule.get("fill_pass")
#                 fill_fail = rule.get("fill_fail")

#                 highlight_cells(ws, (col_idx, col_idx), condition, fill_pass, fill_fail)

#         if bold_header:
#             for cell in ws[1]:
#                 cell.font = bold_font

#         wb.save(output_file)
#         Colors.colored_print(f'REPORT saved at: {output_file}', 'OKGREEN')

#     except Exception as e:
#         Colors.colored_print(f'ERROR creating REPORT: {e}', "FAIL")

