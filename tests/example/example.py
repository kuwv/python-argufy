# -*- coding: utf-8 -*-
# :copyright: (c) 2020 by Jesse Johnson.
# :license: Apache 2.0, see LICENSE for more details.
'''Test parser.

Attributes
----------
check_attribute: bool
    Check document attributes

'''

example_variable = 'ex_var'


def example_bool(bool_check: bool = False):
    '''Example bool.

    Parameters
    ----------
    bool_check: bool, optional
        list packages and version

    '''
    print(bool_check)


def example_choice(choice_check: str = 'A'):
    '''Example choice.

    Parameters
    ----------
    choice_check: str, {'A', 'B', 'C'}
        example choice

    '''
    print(choice_check)
