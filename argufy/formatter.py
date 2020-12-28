'''Simple argparse.'''

# from pprint import pprint
import argparse
from argparse import Action, HelpFormatter
from typing import Iterable, Optional

import colorama
from colorama import Fore, Style

colorama.init()


class ArgufyHelpFormatter(HelpFormatter):
    '''Provide formatting for Argufy.'''
    # argparse.HelpFormatter(prog, max_help_position=80, width=130)

    def add_usage(
        self,
        usage: str,
        actions: Iterable[Action],
        groups: Iterable[argparse._ArgumentGroup],
        prefix: Optional[str] = 'usage: '
    ) -> None:
        '''Format usage message.'''
        if prefix is not None:
            prefix = Style.BRIGHT + prefix + Style.RESET_ALL
        super(ArgufyHelpFormatter, self).add_usage(
            usage, actions, groups, prefix
        )

    def _format_action_invocation(self, action: Action) -> str:
        '''Format arguments summary.'''
        # print('action:', pprint(action))  # type: ignore
        if isinstance(action, argparse._SubParsersAction):
            if action.choices is not None:
                for choice in list(action.choices):
                    parser = action.choices.pop(choice)
                    choice = Fore.CYAN + choice + Fore.RESET
                    action.choices[choice] = parser
        return super(
            ArgufyHelpFormatter, self
        )._format_action_invocation(action)

    def _expand_help(self, action: Action) -> str:
        '''Format help message.'''
        if action.help:
            return (
                Style.NORMAL +
                Fore.YELLOW +
                super(ArgufyHelpFormatter, self)._expand_help(action) +
                Style.RESET_ALL
            )
        else:
            return ''

    def _format_action(self, action: Action) -> str:
        '''Format arguments.'''
        if isinstance(
            action, argparse._SubParsersAction._ChoicesPseudoAction
        ):
            subcommand = (
                Style.BRIGHT +
                Fore.CYAN +
                self._format_action_invocation(action) +
                Style.RESET_ALL
            )
            help_text = self._expand_help(action)
            return f"    {subcommand.ljust(33)}{help_text}\n"
        else:
            # action.option_strings = [
            #     Fore.MAGENTA + x + Fore.RESET
            #     for x in action.option_strings
            # ]
            return super(ArgufyHelpFormatter, self)._format_action(action)
