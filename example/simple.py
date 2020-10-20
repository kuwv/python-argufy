'''Simple argparse.'''
import sys

from argufy import Parser

module = sys.modules[__name__]


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


__parser = Parser()
__parser.add_commands(module)
__parser.dispatch()
