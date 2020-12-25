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


class ArgufyHelpFormatter(HelpFormatter):
    def add_usage(
        self,
        usage: str,
        actions: Iterable[Action],
        groups: Iterable[_ArgumentGroup],
        prefix: Optional[str] = 'USAGE: '
    ) -> None:
        '''Format usage message.'''
        if prefix is None:
            prefix = Fore.CYAN + prefix + Style.RESET_ALL
        super(ArgufyHelpFormatter, self).add_usage(
            usage, actions, groups, prefix
        )

    def add_argument(self, action: Action) -> None:
        '''Format arguments.'''
        if action is not None and action.choices is not None:
            print('action: ', type(action.choices))
            for choice in action.choices.items():  # type: ignore
                print(type(choice))
            super(ArgufyHelpFormatter, self).add_argument(action)


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
