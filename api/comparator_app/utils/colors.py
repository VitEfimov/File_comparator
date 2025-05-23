from colorama import init, Fore, Style

# Initialize colorama (enables ANSI codes on Windows)
init(autoreset=True)

class Colors:
    HEADER = '\033[95m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m' 
    color_map = {
        'HEADER': Fore.MAGENTA,
        'OKGREEN': Fore.GREEN,
        'WARNING': Fore.YELLOW,
        'FAIL': Fore.RED,
        'BOLD': Style.BRIGHT,
        'UNDERLINE': '\033[4m',
        'RESET': Style.RESET_ALL
    }

    # @staticmethod
    # def colored_print(text, color='FAIL'):
    #     color_code = Colors.color_map.get(color.upper(), Colors.color_map['RESET'])
    #     # Underline requires special handling as it's not in colorama
    #     if color.upper() == 'UNDERLINE':
    #         print(f"\033[4m{text}{Style.RESET_ALL}")
    #     else:
    #         print(f"{color_code}{text}")
            
    @staticmethod
    def colored_print(text, color='FAIL', return_text=False):
    #     color_map = {
    #         'HEADER': Colors.HEADER,
    #         'OKGREEN': Colors.OKGREEN,
    #         'WARNING': Colors.WARNING,
    #         'FAIL': Colors.FAIL,
    #         'BOLD': Colors.BOLD,
    #         'UNDERLINE': Colors.UNDERLINE
    # }
        color_code = Colors.color_map.get(color.upper(), Colors.ENDC)
        colored = f"{color_code}{text}{Colors.ENDC}"
    
        if return_text:
            return colored
        else:
            print(colored)

# from colorama import init, Fore, Style


# class Colors:
#     HEADER = '\033[95m'
#     OKGREEN = '\033[92m'
#     WARNING = '\033[93m'
#     FAIL = '\033[91m'
#     ENDC = '\033[0m'
#     BOLD = '\033[1m'
#     UNDERLINE = '\033[4m' 
    
#     @staticmethod
#     def colored_print(text, color='FAIL'):
#         color_map = {
#             'HEADER': Colors.HEADER,
#             'OKGREEN': Colors.OKGREEN,
#             'WARNING': Colors.WARNING,
#             'FAIL': Colors.FAIL,
#             'BOLD': Colors.BOLD,
#             'UNDERLINE': Colors.UNDERLINE
#         }

#         color_code = color_map.get(color.upper(), Colors.ENDC)
#         print(f"{color_code}{text}{Colors.ENDC}")
        
        
#     # @staticmethod
#     # def colored_print_test(text, color='FAIL', return_text=False):
#     #     color_map = {
#     #         'HEADER': Colors.HEADER,
#     #         'OKGREEN': Colors.OKGREEN,
#     #         'WARNING': Colors.WARNING,
#     #         'FAIL': Colors.FAIL,
#     #         'BOLD': Colors.BOLD,
#     #         'UNDERLINE': Colors.UNDERLINE
#     # }
#     #     color_code = color_map.get(color.upper(), Colors.ENDC)
#     #     colored = f"{color_code}{text}{Colors.ENDC}"
    
#     #     if return_text:
#     #         return colored
#     #     print(colored)
        
# Colors.colored_print('test', 'FAIL')
# # Colors.colored_print_test('test', 'FAIL', True)
# # print(Colors.colored_print_test('test', 'FAIL', True))
# print(f"{Colors.FAIL} some text {Colors.ENDC}")


