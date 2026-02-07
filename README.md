# Modulo Three

A Moore machine implementation that computes the remainder of a binary input string when divided by three.

## Overview

This project implements a deterministic finite automaton with output (Moore machine) designed to process binary input sequences and determine their remainder modulo 3. The machine maintains its current state as the accumulated remainder, transitioning between states based on each input digit processed.

## Commands

Local test commands:

- `make test`
- `python -m pytest -q tests`
- `make lint`
- `make typecheck`
- `make check`
- `make pre-commit-install`
- `make pre-commit-run`
- `make docs`

Testing framework:

- `pytest` is the standard and exclusive test runner for this project.
- New tests should be written as standalone `pytest` tests (functions, fixtures, and plain `assert` statements).

Static analysis tooling:

- `ruff` for linting and formatting checks.
- `mypy` and `pyright` for static type checking.
- `pre-commit` for running these checks automatically before commits.
- `pre-commit` runs lint/type checks on commit and `pytest` on push.

Docker workflow commands:

- `make app-build`
- `make app-run ARGS=1011`
- `make test-build`
- `make test-run`

## Testing Scope

The following tests are intentionally excluded as overkill for this project stage:

- public API smoke tests for package attribute existence
- command-target wiring tests for `Makefile` and `pyproject.toml`

Do not re-add dedicated test modules for those two categories unless the scope changes and this section is updated first.

Command policy:

- `test-fast` is intentionally removed.
- Do not add a `test-fast` target or alias back without an explicit scope change and documentation update.
