from comparator_app.comparator.comparator_utils import dictionary, key_creator, check_headers, round_number
# from comparator.comparator_utils import dictionary, key_creator, check_headers, round_number

def compare_table(file_name,
                  file_path1,
                  file_path2,
                  sheet_name,
                  df1, df2, config):
    
    errors = config.get('errors', [])
    decimal = config.get('decimal', 5)
    print_difference = config.get('print_difference', False)


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

    total['missed_headers'] = check_headers(df1, df2, file_path1, file_path2, sheet_name, errors)

    data1 = dictionary(df1,errors)
    data2 = dictionary(df2,errors)

    if len(data1) != len(data2):
        msg = f'ERROR: {file_name} - number of rows mismatch'
        errors.append(msg)

    differences = []
    highlighted = []
    missed_keys = []

    dict1 = {tuple(row['key']): row['values'] for row in data1}
    dict2 = {tuple(row['key']): row['values'] for row in data2}
    
    # print(dict1)

    if len(dict1) != len(data1) or len(dict2) != len(data2):
        is_str = False
        for x in data1[1]:
            if isinstance(x, str):
                is_str = True
                
        if not is_str:
            data1 = key_creator(data1)
            data2 = key_creator(data2)
            dict1 = {tuple(row['key']): row['values'] for row in data1}
            dict2 = {tuple(row['key']): row['values'] for row in data2}
            errors.append(f'FAIL {file_name}, {sheet_name} - custom keys added')
    
    keys1 = set(dict1.keys())
    keys2 = set(dict2.keys())
    all_keys = keys1 | keys2

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

        row1_val = [round_number(val, decimal) for val in dict1[key]]
        row2_val = [round_number(val, decimal) for val in dict2[key]]

        total['total_rows'] += 1
        difference = {}

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
                # difference = [round_number(diff, decimal) for diff in significant_diffs]
                difference = {i+1: round_number(abs(v2 - v1), decimal) for i, (v1, v2) in enumerate(zip(row1_val, row2_val)) if abs(v2 - v1) > 10 ** -decimal}
                print(difference)

                total['sum_value_differences'] += round_number(sum(difference.values()), decimal)

                if total['max'] < max_diff:
                    total['max'] = round_number(max_diff, decimal)
            else:
                diff1 = [val for val in row1_val if val not in row2_val]
                diff2 = [val for val in row2_val if val not in row1_val]
                # difference = [abs(round_number(d, decimal)) for d in (diff1 + diff2) if abs(d) > 10 ** -decimal]
                difference = {
                    i: round_number(v2 - v1, decimal)
                    for i, (v1, v2) in enumerate(zip(row1_val, row2_val))
                    if i < len(row1_val) and i < len(row2_val) and abs(v2 - v1) > 10 ** -decimal
                }
                # print(difference)
                total['sum_value_differences'] += round_number(sum(difference.values()), decimal)

            differences.append({
                'key': key,
                'value_file1': row1_val,
                'value_file2': row2_val,
                'max_diff': round_number(max(difference) if difference else 0, decimal),
                'difference': difference
            })

        highlighted.append({
            'key': key,
            'value_file1': row1_val,
            'value_file2': row2_val,
            'match': match_status_val,
            'difference': difference,
            'max_diff': round_number(max(difference.values()) if difference.values() else 0, decimal)

        })
        
    

    for x in missed_keys:
        differences.append({'key': x})
        highlighted.append({'key': x})
        
    if print_difference:
        print(f'----- file name: {file_name}, sheet name: {sheet_name} -----\n')
        for x in highlighted:
            try:
                if x.get('difference'):  
                    print("KEY:", x['key'])
                    print("File 1 Values:", x['value_file1'])
                    print("File 2 Values:", x['value_file2'])
                    print("Differences:", x['difference'])
                    print("Max Diff:", x['max_diff'])
                    print("------")

            except KeyError as e:
                print(f"⚠️ Missing key: {e}")
                print(f"Full record: {x}")
        if missed_keys:
            for x in missed_keys:
                print(f'Missed keys: {x}')
        # print()
    total['summary_differences'] = differences
    
    return total, highlighted


