'''Simple argparse.'''

import logging
import sys
from typing import Optional

from argufy import Parser

module = sys.modules[__name__]

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


def switch():  # type: ignore
    '''Empty function to check switch.'''
    print('test empty switch')


def positional(test: str):  # type: ignore
    '''Run example positional.'''
    print(test)


def boolean(bool_check=False):  # type: ignore
    '''Run example bool.'''
    print(bool_check)


def choice(choice_check='A'):  # type: ignore
    '''Run example choice.

    Parameters
    ----------
    choice_check: str, {'A', 'B', 'C'}
        example choice

    '''
    print(choice_check)


def optional(variable: Optional[str] = None) -> None:
    '''Run example optional.'''
    if variable:
        print(variable)
    else:
        print('optional is not set')


def arguments(*args: str, **kwargs: str) -> None:
    '''Run example optional.'''
    if args != []:
        print(args)

    if kwargs != {}:
        print(kwargs)


parser = Parser(version='1.2.3', log_level='DEBUG')
parser.add_commands(module)
parser.dispatch()
