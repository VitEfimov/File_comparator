import os

decimal = 5
print_in_compiler = False
print_total_table = False
create_reports = True
create_highlight_reports = True
one_file_report = ''
project_name = 'test_data'

errors = []
package_1= "package_1"
package_2= "package_2"
base_directory = ''
project_path = os.path.join(base_directory, project_name).replace('\\', '/')
package1_directory = os.path.join(project_path, package_1).replace('\\', '/')
package2_directory = os.path.join(project_path, package_2).replace('\\', '/')
package_report_name = f'REPORT_{project_name}'
package_report_path = os.path.join(project_path, package_report_name).replace('\\', '/')
# BASE_DIRECTORY = ''
# PROJECT_PATH = os.path.join(BASE_DIRECTORY, project_name).replace('\\', '/')
# PACKAGE1_DIRECTORY = os.path.join(BASE_DIRECTORY, project_name).replace('\\', '/')
# PACKAGE2_DIRECTORY = os.path.join(BASE_DIRECTORY, project_name).replace('\\', '/')
# PACKAGE_REPORT_NAME = f'REPORT_{project_name}'
# PACKAGE_REPORT_PATH = os.path.join(PROJECT_PATH, PACKAGE_REPORT_NAME).replace('\\', '/')

# import yaml

# with open("config.yml", "r", encoding="utf-8") as f:
#     config = yaml.safe_load(f)

# decimal = config["decimal"]
# print_in_compiler = config["print_in_compiler"]
# create_reports = config["create_reports"]
# project_name = config["project_name"]
# base_directory = config["base_directory"]
# create_highlight_reports = config["create_highlight_reports"]
# one_file_report = config["one_file_report"]
# print_total_table = config["print_total_table"]

# project_path = config["paths"]["project_path"].format(
#     base_directory=base_directory,
#     project_name=project_name
# )
# package1_directory = config["paths"]["package1_directory"].format(
#     base_directory=base_directory,
#     project_name=project_name
# )
# package2_directory = config["paths"]["package2_directory"].format(
#     base_directory=base_directory,
#     project_name=project_name
# )
# package_report_path = config["paths"]["package_report_path"].format(
#     base_directory=base_directory,
#     project_name=project_name
# )

errors = []
