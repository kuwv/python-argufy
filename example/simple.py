'''Simple argparse.'''

import sys

from argparse import _ArgumentGroup, Action, HelpFormatter
from typing import Iterable, Optional

import colorama
from colorama import Fore, Back, Style

from argufy import Parser

module = sys.modules[__name__]

# print(Fore.RED + 'some red text')
# print(Back.GREEN + 'and with a green background')
# print(Style.DIM + 'and in dim text')
# print(Style.RESET_ALL)
# print(Fore.CYAN + 'testing')
# print('back to normal now')

colorama.init()


def empty():  # type: ignore
    '''Empty function to check switch.'''
    print('test empty switch')


def positional(test: str):  # type: ignore
    print(test)


def example_bool(bool_check=False):  # type: ignore
    '''Run example bool.'''
    print(bool_check)


def example_choice(choice_check='A'):  # type: ignore
    '''Run example choice.'''
    print(choice_check)


parser = Parser()
# parser = Parser(formatter_class=ArgufyHelpFormatter)  # type: ignore
parser.add_commands(module)
parser.dispatch()
