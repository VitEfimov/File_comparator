import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from comparator.file_comparator import compare_dirictory
from configurator import create_reports

compare_dirictory(create_reports)