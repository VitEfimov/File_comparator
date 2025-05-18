📁 File Comparator CLI Tool

This project is a Python-based application that compares .csv and .xlsx files from two directories or files. It checks for differences in sheet names, headers, keys, and numeric values, and generates a detailed report summarizing the results.

🧩 Features✅ Supports .csv and .xlsx file formats

✅ Compares files and sheets by name

✅ Compares values row-by-row (ignores order)

✅ Identifies mismatched keys, values, and totals

✅ Generates a complete Excel summary report

✅ Modular structure (reader, comparator, reporter)

📁 Project Structure:

file_comparator/
├── main.py
├── configuration.py
├── comparator/
├── reader/
├── reports/
├── utils/
├── requirements.txt/
└── README.md


🚀 How to Run

1. ✅ Install Dependencies
pip install -r requirements.txt

2. 📂 Prepare Your Directories

Make two folders (e.g. test_data/package_1/ and test_data/package_2/) and place corresponding .csv or .xlsx files you want to compare inside them.

Example:

test_data/
├── package_1/
│   ├── MOCK_DATA.csv
│   └── MOCK_DATA.xlsx
└── package_2/
    ├── MOCK_DATAold.csv
    └── MOCK_DATA.xlsx

3. ▶️ Run the Tool

python main.py
This script will:

Read and compare files from the predefined directories (you can update them inside main.py)

Generate a detailed summary saved as:

reports/Total_Results.xlsx


📄 Example Output (Console)

DIFFERENCE REPORT saved at: C:/.../test_data/REPORT_test_data\differences_MOCK_DATA.xlsx_mock_data.xlsx
HIGHLIGHTED REPORT saved at: C:/.../test_data/REPORT_test_data\report_MOCK_DATA.xlsx_mock_data.xlsx
HIGHLIGHTED REPORT saved at: C:/.../test_data/REPORT_test_data\report_MOCK_DATA.xlsx_some_data.xlsx
HIGHLIGHTED REPORT saved at: C:/.../test_data/REPORT_test_data\report_MOCK_DATA.csv_sheet.xlsx

#############################################################
                   COMPIlATION COMPLEATED
#############################################################
 from 2 files compared
file_name: MOCK_DATA.xlsx | file_executions: 1 | sheet_name: ['extra_sheet'] missing: NOT EXECUTED | executed_sheets: 0 | total_rows: 0 | passed: 0 | number_fail: 0 | key_fail: 0 | sum_value_differences: 0 | max_difference: 0 
file_name: MOCK_DATA.xlsx | file_executions: 1 | sheet_name: mock_data | executed_sheets: 1 | total_rows: 152 | passed: 144 | number_fail: 4 | key_fail: 4 | sum_value_differences: 114.00421 | max_difference: 70.0
file_name: MOCK_DATA.xlsx | file_executions: 1 | sheet_name: some_data | executed_sheets: 2 | total_rows: 49 | passed: 49 | number_fail: 0 | key_fail: 0 | sum_value_differences: 0 | max_difference: 0
file_name: MOCK_DATA.csv | file_executions: 2 | sheet_name: sheet | executed_sheets: 1 | total_rows: 150 | passed: 150 | number_fail: 0 | key_fail: 0 | sum_value_differences: 0 | max_difference: 0

ERROR: Sheet(s) ['extra_sheet'] missing in C:/.../test_data/package_2\MOCK_DATA.xlsx
TOTAL REPORT saved at: C:/.../test_data/REPORT_test_data\Total_Results.xlsx 


🧠 How It Works

reader.py: Loads .csv and .xlsx files into memory

sheet_comparator.py: Compares each sheet row-by-row using key-value logic

file_comparator.py: Pairs files and handles comparison flow

report_generator.py: Builds a comprehensive Excel report

main.py: Entry point to call everything


✅ Notes

Keys are all string values in a row

Values are all numeric values (supports floats and negatives)

Comparison is insensitive to row order

Excel reports highlight mismatches for analysis

🧼 Cleaning Up

Delete the reports/ or uploads/ folder manually after a run if needed. This folder is auto-created each time.

🛠️ Customization

You can modify:

decimal = 5                     # Rounding precision for float comparison
print_in_compiler = False       # If True, prints detailet report
print_total_table = False       # If True, prints table to terminal
create_reports = True           # If True, saves Excel result files (diferences)
create_highlight_reports = True # If True, adds highlights detailed report
one_file_report = ''            # Optional single report (specify file name)
project_name = 'test_project2'  # Name of your current project

errors = []
package_1=                                     # package folder names (save files here)
package_2=                                     # package folder names (save files here)
base_directory =                               # Base directory where all project folders live
project_path =                                 # Path to the current project folder
package1_directory =                           # Path to the package_1 project folder
package2_directory =                           # Path to the package_2 project folder
package_report_name = f'REPORT_{project_name}' # Folder and path where the report will be saved
package_report_path = 

📌 Author
Developed by Vitalii (2025)