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
    format_choices = False

    def add_usage(
        self,
        usage: str,
        actions: Iterable[Action],
        groups: Iterable[argparse._ArgumentGroup],
        prefix: Optional[str] = 'usage: ',
    ) -> None:
        '''Format usage message.'''
        if prefix is not None:
            prefix = self.font(prefix)
        # print('usage', usage, actions, groups, prefix)
        super(ArgufyHelpFormatter, self).add_usage(
            usage, actions, groups, prefix
        )

    # def start_section(self, heading: Optional[str]) -> None:
    #     print('start section', heading)
    #     super().start_section(heading)

    # def end_section(self) -> None:
    #     print('end section')
    #     super().end_section()

    # def add_text(self, text: Optional[str]) -> None:
    #     print('add text', text)
    #     super().add_text(text)

    @staticmethod
    def font(text: str, width: str = 'BRIGHT') -> str:
        '''Set the string thickness.'''
        return getattr(Style, width) + text + Style.RESET_ALL

    @staticmethod
    def shade(text: str, color: str = 'CYAN') -> str:
        '''Set the string color.'''
        return getattr(Fore, color.upper()) + text + Style.RESET_ALL

    def add_argument(self, action: Action) -> None:
        '''Format arguments summary.'''
        # XXX: action.choice fails tests when colored
        if(
            ArgufyHelpFormatter.format_choices
            and isinstance(action, argparse._SubParsersAction)
        ):
            if action.choices is not None:
                for choice in list(action.choices):
                    parser = action.choices.pop(choice)
                    choice = self.shade(choice)
                    action.choices[choice] = parser
        super(ArgufyHelpFormatter, self).add_argument(action)

    def _expand_help(self, action: Action) -> str:
        '''Format help message.'''
        if action.help:
            return self.shade(
                super(ArgufyHelpFormatter, self)
                ._expand_help(action)
                .rstrip('.')
                .lower(),
                'YELLOW',
            )
        else:
            return ''

    def _format_action(self, action: Action) -> str:
        '''Format arguments.'''
        # TODO: calculate correct spacing
        if isinstance(action, argparse._SubParsersAction._ChoicesPseudoAction):
            subcommand = self.shade(
                self.font(self._format_action_invocation(action))
            )
            help_text = self._expand_help(action)
            return f"    {subcommand.ljust(50)}{help_text}\n"
        elif (
            isinstance(action, argparse.Action)
            and not isinstance(action, argparse._SubParsersAction)
        ):
            # XXX: normal and short flags ident is not parallel
            option_strings = ', '.join([
                self.font(self.shade(option))
                for option in action.option_strings
            ])
            help_text = self._expand_help(action)
            # set multi-argument justification for single flags
            if len(action.option_strings) > 1:
                width = 67
                start = 4
            else:
                width = 46
                start = 8
            out = f"{' ' * start}{option_strings.ljust(width)}{help_text}\n"
            return out
        else:
            return super(ArgufyHelpFormatter, self)._format_action(action)
