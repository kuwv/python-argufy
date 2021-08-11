'''Simple argparse.'''

import logging
import sys

from argufy import Parser

module = sys.modules[__name__]

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


def arguments(test: str, *args: str, **kwargs: str) -> None:
    '''Run example key arguments.

    Parameters
    ----------
    test: str
        positional argument
    test1: str, optional
        kwargs test one
    test2: str, optional
        kwargs test two

    '''
    if args != []:
        print('args', args)

    if kwargs != {}:
        print('kwargs', kwargs)


parser = Parser(
    prog='complete',
    version='1.2.3',
    log_level='debug',
    log_handler=sys.stderr,
    # command_scheme='chain',
)
parser.add_commands(module)
parser.dispatch()
