# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Provide CLI for example.'''

from argufy import Parser

from . import example

local_variable = 'local_result'


def main():
    '''Do main function for CLI.'''
    parser = Parser()
    parser.add_subcommands(example)
    parser.dispatch()


if __name__ == '__main__':
    '''Execute main.'''
    main()
