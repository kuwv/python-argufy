from argufy import Parser
import sys

module = sys.modules[__name__]


def example_bool(bool_check = False):
    print(bool_check)


def example_choice(choice_check = 'A'):
    print(choice_check)


__parser = Parser()
__parser.add_commands(module)
__parser.dispatch()
