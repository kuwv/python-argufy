'''Simple argparse.'''

import logging
import sys
from typing import Optional, Union

from argufy import Parser

module = sys.modules[__name__]

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

t = Union[str, None]
if t.__origin__ is Union and isinstance(None, t.__args__):  # type: ignore
    print('awesome')
else:
    print('blah')


def switch():  # type: ignore
    '''Empty function to check switch.'''
    print('test empty switch')


def positional(test: str):  # type: ignore
    '''Run example positional.'''
    print(test)


def example_bool(bool_check=False):  # type: ignore
    '''Run example bool.'''
    print(bool_check)


def example_choice(choice_check='A'):  # type: ignore
    '''Run example choice.'''
    print(choice_check)


def optional(variable: Optional[str] = None) -> None:
    if variable:
        print(variable)
    else:
        print('optional is not set')


parser = Parser(version='1.2.3', log_level='DEBUG')
parser.add_commands(module)
parser.dispatch()
