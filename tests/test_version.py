# -*- coding: utf-8 -*-
# :copyright: (c) 2020 by Jesse Johnson.
# :license: Apache 2.0, see LICENSE for more details.
'''Test version.'''

from argufy.__version__ import __version__


def test_version() -> None:
    '''Test project version is managed.'''
    assert __version__ == "0.1.1"
