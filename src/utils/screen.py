import os
from sys import platform

def system_clear():
    clear_command = 'cls' if platform == 'win32' else 'clear'
    os.system(clear_command)

def clear(number_of_lines = 50):
    print('\n' * number_of_lines)
