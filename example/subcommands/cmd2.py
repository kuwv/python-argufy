# -*- coding: utf-8 -*-
# :copyright: (c) 2020 by Jesse Johnson.
# :license: Apache 2.0, see LICENSE for more details.
'''Test parser two.

Attributes
----------
example_variable: str
    Example variable for testing

'''
example_variable1 = 'test1'
example_variable2 = 'test2'


def example_bool(bool_check: bool = False):
    '''Demonstrate example bool.

    Parameters
    ----------
    bool_check: bool, optional
        example boolean

    '''
    print(bool_check)


def example_choice(choice_check: str = 'A'):
    '''Demonstrate example choice.

    Parameters
    ----------
    choice_check: str, {'A', 'B', 'C'}
        example choice

    '''
    print(choice_check)
