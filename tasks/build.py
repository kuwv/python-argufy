# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
"""Test Task-Runner."""

from typing import TYPE_CHECKING, Optional

from invoke import call, task

from argufy import __version__

if TYPE_CHECKING:
    from invoke import Context

if (
    'dev' in __version__
    or 'a' in __version__
    or 'b' in __version__
    or 'rc' in __version__
):
    part = 'build'
else:
    part = 'patch'


@task
def build(ctx: 'Context', format: Optional[bool] = None) -> None:
    """Build wheel package."""
    if format:
        ctx.run(f"flit build --format={format}")
    else:
        ctx.run('flit build')


@task(pre=[call(build, format='wheel')])  # type: ignore
def dev(ctx: 'Context') -> None:
    """Perform development runtime environment setup."""
    ctx.run('flit install --pth-file --python python3')


@task
def install(
    ctx: 'Context',
    symlink: bool = True,
    dev: bool = False,
) -> None:
    """Install within environment."""
    args = []
    if symlink:
        args.append('--symlink')
    if dev:
        args.append('--python=python3')
    ctx.run(f"flit install {' '.join(args)}")


@task
def publish(ctx: 'Context') -> None:
    """Publish project distribution."""
    ctx.run('flit publish')


@task
def clean(ctx: 'Context') -> None:
    """Clean project dependencies and build."""
    paths = ['dist', 'logs']
    paths.append('**/__pycache__')
    paths.append('**/*.pyc')
    paths.append('argufy.egg-info')
    for path in paths:
        ctx.run(f"rm -rf {path}")


@task
def version(
    ctx: 'Context',
    part: str = part,
    tag: bool = False,
    commit: bool = False,
    message: Optional[str] = None,
) -> None:
    """Update project version and apply tags."""
    args = [part]
    if commit:
        args.append('--commit')
    else:
        args.append('--dry-run')
        args.append('--allow-dirty')
        args.append('--verbose')
        print('Add "--commit" to actually bump the version.')
    if tag or message:
        args.append('--tag')
        if message:
            args.append(f"--tag-message '{message}'")
    ctx.run(f"bumpversion {' '.join(args)}")
