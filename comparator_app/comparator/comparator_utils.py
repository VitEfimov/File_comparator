import re
from comparator_app.configurator import decimal, errors
from comparator_app.utils.colors import Colors


def is_a_number(value):
    return bool(re.fullmatch(r'-?\d+(\.\d+)?', str(value)))

def round_number(number):
    try:
        return round(float(number), decimal)
    except ValueError:
        return number
    
def check_headers(df1, df2, file_path1, file_path2, sheet_name):
    if list(df1.columns) != list(df2.columns):
        df1_columns = set(df1.columns) - set(df2.columns)
        df2_columns = set(df2.columns) - set(df1.columns)
        missed_columns = df1.columns | df2.columns
        normalized_path1 = file_path1.replace('\\', '/')
        normalized_path2 = file_path1.replace('\\', '/')
        file1 = normalized_path1.split('/')[-2:]
        file2 = normalized_path2.split('/')[-2:]
        Colors.colored_print(f'FAIL: Headers do not match {sheet_name},'
                             f' file {file1}: {df1_columns}'
                             f' and file {file2}: {df2_columns}', 'FAIL')
        errors.append(f'FAIL: Headers do not match {sheet_name},'
                             f' file {file1}: {df1_columns}'
                             f' and file {file2}: {df2_columns}', 'FAIL', True)
        return missed_columns
    return []
        
        
def dictionary(df):
    try: 
        list_of_dict = []
        for _, row in df.iterrows():
            row_dictionary = {'key': [], 'values': []}
            for each in row:
                each = str(each).strip()
                if is_a_number(each):
                    row_dictionary['values'].append(float(each) if '.' in each else int(each))
                else:
                    row_dictionary['key'].append(each)
            list_of_dict.append(row_dictionary)
        return list_of_dict
    except ValueError as e:
        Colors.colored_print(f'FAIL createing dictionary, {e}', 'FAIL')
        return []
    
def key_creator(data, prefix='key'):
    for i, item in enumerate(data, start=1):
        item['key'] = [f'{prefix}{i}']
    return data

        

