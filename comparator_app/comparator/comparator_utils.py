import re

def is_a_number(value):
    return bool(re.fullmatch(r'-?\d+(\.\d+)?', str(value)))

def round_number(number, decimal):
    try:
        return round(float(number), decimal)
    except ValueError:
        return number
    
def check_headers(df1, df2, file_path1, file_path2, sheet_name, errors):
    if list(df1.columns) != list(df2.columns):
        df1_columns = set(df1.columns) - set(df2.columns)
        df2_columns = set(df2.columns) - set(df1.columns)
        missed_columns = df1.columns | df2.columns
        normalized_path1 = file_path1.replace('\\', '/')
        normalized_path2 = file_path2.replace('\\', '/')
        file1 = normalized_path1.split('/')[-2:]
        file2 = normalized_path2.split('/')[-2:]
        errors.append(f'FAIL: Headers do not match {sheet_name},'
                             f' file {file1}: {df1_columns}'
                             f' and file {file2}: {df2_columns}')
        return missed_columns
    return []
        
        
def dictionary(df, errors):
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
        errors.append(f'FAIL createing dictionary, {e}')
        return []
    
def key_creator(data, prefix='key'):
    for i, item in enumerate(data, start=1):
        item['key'] = [f'{prefix}{i}']
    return data

        

