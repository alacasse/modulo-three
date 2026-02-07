# Modulo Three

A Moore machine implementation that computes the remainder of a binary input string when divided by three.

## Overview

This project implements a deterministic finite automaton with output (Moore machine) designed to process binary input sequences and determine their remainder modulo 3. The machine maintains its current state as the accumulated remainder, transitioning between states based on each input digit processed.

## Commands

Local test commands:

- `make test`
- `make docs`

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
