'''Simple argparse.'''
from pprint import pprint
from argparse import _ArgumentGroup, Action, HelpFormatter
from typing import Iterable, Optional

import colorama
from colorama import Fore, Style

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
        if prefix is not None:
            prefix = Style.BRIGHT + prefix + Style.RESET_ALL
        super(ArgufyHelpFormatter, self).add_usage(
            usage, actions, groups, prefix
        )

    def add_argument(self, action: Action) -> None:
        '''Format arguments.'''
        print(pprint(action))
        if action.choices is not None:
            for choice in list(action.choices):
                parser = action.choices.pop(choice)
                choice = Fore.CYAN + choice + Style.RESET_ALL
                action.choices[choice] = parser
        print(action)
        super(ArgufyHelpFormatter, self).add_argument(action)
