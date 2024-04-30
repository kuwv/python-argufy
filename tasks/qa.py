# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
"""Test Task-Runner."""

from typing import TYPE_CHECKING, Optional

from invoke import task

if TYPE_CHECKING:
    from invoke import Context


@task
def style(ctx: 'Context', check: bool = True) -> None:
    """Format project source code to PEP-8 standard."""
    args = ['--skip-string-normalization']
    if check:
        args.append('--check')
    ctx.run('isort --atomic **/*.py')
    ctx.run(f"black **/*.py {' '.join(args)}")


@task
def lint(ctx: 'Context') -> None:
    """Check project source code for linting errors."""
    ctx.run('flake8')


@task
def type_check(ctx: 'Context', path: str = '.') -> None:
    """Check project source types."""
    ctx.run(f"mypy {path}")


@task
def unit_test(ctx: 'Context', capture: Optional[str] = None) -> None:
    """Perform unit tests."""
    args = []
    if capture:
        args.append(f"--capture={capture}")
    ctx.run(f"pytest {' '.join(args)}")


@task
def static_analysis(ctx: 'Context') -> None:
    """Perform static code analysis on imports."""
    ctx.run('safety check')
    ctx.run('bandit -r argufy')


@task
def coverage(ctx: 'Context', report: Optional[str] = None) -> None:
    """Perform coverage checks for tests."""
    args = ['--cov=argufy']
    if report:
        args.append(f"--cov-report={report}")
    ctx.run(f"pytest {' '.join(args)} ./tests/")


@task(pre=[style, lint, unit_test, static_analysis, coverage])
def test(ctx: 'Context') -> None:
    """Run all tests."""
    pass
