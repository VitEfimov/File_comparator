# from comparator_app.configurator import decimal, print_in_compiler, create_highlight_reports
# from comparator_app.reports.report_methods import difference_report, highlighted_report
# from comparator_app.utils.colors import Colors

# def create_report(differences,
#                   highlighted,
#                   different_file_path,
#                   report_file,
#                   create_reports):
#     if print_in_compiler:
#         if differences:
#             Colors.colored_print(f'############################### FAILS {len(differences)} ###############################')
#             for diff in differences:
#                 print(diff)
#         else:
#             Colors.colored_print('############################### PASS ###############################')
            
#     if create_reports:
#         if len(differences) > 0:
#             difference_report(differences, different_file_path, decimal)
#         if create_highlight_reports:
#             highlighted_report(highlighted, report_file)