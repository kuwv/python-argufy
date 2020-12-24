'''Simple argparse.'''

from argparse import _ArgumentGroup, Action, HelpFormatter
from typing import Iterable, Optional

import colorama
from colorama import Fore, Back, Style

colorama.init()


class ArgufyHelpFormatter(HelpFormatter):
    def add_usage(
        self,
        usage: str,
        actions: Iterable[Action],
        groups: Iterable[_ArgumentGroup],
        prefix: Optional[str] = None
    ) -> None:
        '''Format usage message.'''
        if prefix is None:
            prefix = Fore.CYAN + 'USAGE: ' + Style.RESET_ALL
        super(ArgufyHelpFormatter, self).add_usage(
            usage, actions, groups, prefix
        )

    def add_argument(self, action: Action) -> None:
        '''Format arguments.'''
        print(action.choices)
        super(ArgufyHelpFormatter, self).add_argument(action)
