import os
from sys import platform

def system_clear():
    # The original 'clear' command until I realized that terminal clear by outputting a ton of newlines.
    clear_command = 'cls' if platform == 'win32' else 'clear'
    os.system(clear_command)

def clear(number_of_lines = 50):
    # Clear the screen by outputting a number of newlines.
    print('\n' * number_of_lines)
