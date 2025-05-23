# import sys
# import io

# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
# from comparator.file_comparator import compare_directory
# from configurator import create_reports

# from comparator.compare_zip import compare_directory

# compare_directory(dir1, dir2, config)

# compare_directory(create_reports)

import sys
import io
import os
from comparator.compare_zip import compare_directory  # Use the correct version
# from comparator.file_comparator import compare_directory  # Use this only if needed instead

# Ensure UTF-8 output in terminal
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Optional: define dummy test directories and config
if __name__ == '__main__':
    dir1 = '/path/to/extracted/dir1'
    dir2 = '/path/to/extracted/dir2'

    config = {
        'decimal': 2,
        'create_reports': True,
        'print_total_table': False,
        'project_name': 'manual_test',
        'report_dir': 'reports/manual_test',  # <== Save reports here
        'errors': []
    }
    
    compare_directory(dir1, dir2, config)

    # result = compare_directory(dir1, dir2, config)
    # print(result)