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
- `BinaryModFiniteMachineBuilder` in `modulo_three/builder.py`
- `DeterministicTableMachineBuilder` + `DeterministicMachineSpec` in `modulo_three/builder.py`

## FiniteMachine Scope

Intended to support:

- static deterministic finite machines (DFA-style) with hashable states/symbols
- table-driven transitions from `(state, symbol)` to exactly one next state
- single-pass processing of an input sequence to produce a final state

Not intended to support:

- nondeterminism (NFA), epsilon transitions, or probabilistic branching
- guarded/contextual transitions (timers, external state checks, payload-aware events)
- runtime mutation of machine structure (`add_state`, `add_transition`, hot-reload updates)
- state behavior hooks (entry/exit actions, transition callbacks, metrics/listeners)
- hierarchical/composite/parallel state models (statecharts/HFSM semantics)
- built-in import/export or interoperability formats (DOT/SCXML/JSON schemas)

## Reusable Example (Non-Modulo)

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
machine = builder.build(
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

## Commands

App usage:

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
