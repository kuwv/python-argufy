# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Provide CLI for example.'''

from argufy import Parser

from . import example

example_variable = 'ex_var'


def main():
    parser = Parser()
    parser.add_commands(example)
    parser.dispatch()

if __name__ == '__main__':
    main()
