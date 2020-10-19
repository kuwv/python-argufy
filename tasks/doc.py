# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Provide documentation tasks.'''

from invoke import task


@task
def lint(ctx):  # type: ignore
    '''Check code for documentation errors.'''
    ctx.run('pydocstyle')


@task
def coverage(ctx):  # type: ignore
    '''Ensure all code is documented.'''
    ctx.run('docstr-coverage **/*.py')


@task(pre=[lint], post=[coverage])
def test(ctx):  # type: ignore
    '''Test documentation build.'''
    ctx.run('mkdocs build')


@task
def build(ctx):  # type: ignore
    '''Build documentation site.'''
    ctx.run('mkdocs build')


@task
def publish(ctx):  # type: ignore
    '''Publish project documentation.'''
    ctx.run('mkdocs gh-deploy')
