'''Simple argparse.'''
import sys

from argufy import Parser

module = sys.modules[__name__]


def example_bool(bool_check=False):
    '''Run example bool.'''
    print(bool_check)


def example_choice(choice_check='A'):
    '''Run example choice.'''
    print(choice_check)


__parser = Parser()
__parser.add_commands(module)
__parser.dispatch()
