'''Simple argparse.'''

import inspect
import logging
import sys
from typing import Optional

from argufy import Parser

module = sys.modules[__name__]

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


def switch():  # type: ignore
    '''Run empty function to check switch.'''
    print('test empty switch')


def positional(test: str) -> None:
    '''Run example positional.

    Parameters
    ----------
    test: str
        example test variable

    '''
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


def arguments(arg: str = 'test', *args: str, **kwargs: str) -> None:
    '''Run example optional.

    Parameters
    ----------
    test1: str
        kwargs test one

    test2: str
        kwargs test two

    '''
    if args != []:
        print(args)

    if kwargs != {}:
        print(kwargs)


print(inspect.getfullargspec(arguments))
parser = Parser(
    prog=__name__,
    version='1.2.3',
    log_level='DEBUG',
    log_handler=sys.stderr,  # type: ignore
)
parser.add_commands(module)
parser.dispatch()
