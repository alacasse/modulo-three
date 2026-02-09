# Modulo Three

A Moore machine implementation that computes the remainder of a binary input string when divided by three.

## Overview

This project implements a deterministic finite automaton with output (Moore machine) designed to process binary input sequences and determine their remainder modulo 3. The machine maintains its current state as the accumulated remainder, transitioning between states based on each input digit processed.

## Public API

App-level entrypoint:

- `modThree(input: str) -> int`

Reusable finite machine API:

- `FiniteMachine[StateT, SymbolT]` in `modulo_three/machine.py`
  - `run(input_symbols: Iterable[SymbolT]) -> StateT`
  - `accepts(input_symbols: Iterable[SymbolT]) -> bool`
  - Use run() when you need the final state (e.g., modulo remainder). Use accepts() when you need an accept/reject verdict.
- `build_binary_mod_machine(mod: int) -> FiniteMachine[int, str]` in `modulo_three/builder.py`
- `build_binary_mod_spec(mod: int) -> DeterministicMachineSpec[int, str]` in `modulo_three/builder.py`
- `DeterministicTableMachineBuilder` + `DeterministicMachineSpec` in `modulo_three/builder.py`

## Deterministic Construction

Deterministic machines are constructed from a specification via the
`DeterministicTableMachineBuilder`. The binary modulo helpers are convenience
functions that assemble a modulo-specific spec and build it with the same
builder.

## FiniteMachine Scope

This implementation intentionally targets a small, focused subset of finite state machines.

It supports:

- deterministic, table-driven state machines (DFA-style)
- one transition per (state, symbol)
- single-pass execution over an input sequence

The goal is to keep the core easy to read, easy to test, and easy to replicate by configuration.

It does not attempt to support more advanced FSM features (e.g. nondeterminism, state hooks, hierarchical models, or runtime mutation), as they are not required for the intended use cases and would add unnecessary complexity.

## Reusable Example

The following example builds a non-modulo machine with custom state types:

```python
from enum import Enum, auto

from modulo_three.builder import (
    DeterministicMachineSpec,
    DeterministicTableMachineBuilder,
)


class Phase(Enum):
    START = auto()
    MID = auto()
    END = auto()


builder = DeterministicTableMachineBuilder[Phase, int]()
machine = builder.from_spec(
    DeterministicMachineSpec(
        Q={Phase.START, Phase.MID, Phase.END},
        Sigma={0, 1},
        q0=Phase.START,
        F={Phase.END},
        delta={
            (Phase.START, 1): Phase.MID,
            (Phase.MID, 0): Phase.END,
        },
    )
)

final_state = machine.run([1, 0])
assert final_state is Phase.END
```

For the modulo-three machine used in this project, see `build_binary_mod_machine`.

## Commands

App usage:

### No venv needed

- `make app-run` (Docker, interactive mode)
- `make app-run ARGS=1011` (Docker, one-shot input)

### Setup venv needed
- `python -m modulo_three 1011`
- `python -m modulo_three --interactive`

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
- `make app-run` (defaults to `--interactive`)
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
