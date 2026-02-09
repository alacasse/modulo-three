# Modulo Three

A **deterministic finite-state machine (FSM)** implementation that computes remainders for streaming input without converting the full input to an integer. The primary use case is binary modulo-three computation, and the generic FSM engine supports custom alphabets/moduli when you provide a machine specification.

## Quick Start

```bash
# Run with Docker (no setup required)
make run ARGS=1011        # Output: 2
make run ARGS=-i          # Interactive mode (-i/--interactive)
# Exit interactive mode with: exit, quit, or q

# Run locally (requires Python 3.12+)
python -m modulo_three 1011

# Run tests
make test
```

## Architecture Overview

This project implements a **reusable FSM engine** that can be configured for any deterministic finite automaton. The modulo-three solution is a concrete consumer of this generic engine.

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                           Layer Architecture                                │
├─────────────────────────────────────────────────────────────────────────────┤
│  Public API Layer                                                           │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  modThree(input: str) -> int                                        │   │
│  │  (in modulo_three/simple_facade.py)                                 │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────────────────────┤
│  FSM Engine Layer (Generic, Reusable)                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  FiniteMachine[StateT, SymbolT]                                      │   │
│  │  - run(input_symbols) -> StateT                                     │   │
│  │  - accepts(input_symbols) -> bool                                   │   │
│  │  (in modulo_three/machine.py)                                       │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────────────────────┤
│  Specification/Builder Layer                                                 │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  DeterministicMachineSpec[StateT, SymbolT] (machine specification)  │   │
│  │  DeterministicTableMachineBuilder                                   │   │
│  │  build_binary_mod_machine(mod: int)                                 │   │
│  │  (in modulo_three/builder.py)                                       │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Design Choices

### 1. Separation of Concerns

The architecture deliberately separates three distinct responsibilities:

| Layer | Responsibility | File | Reusable? |
| ----- | -------------- | ---- | --------- |
| **Engine** | Pure transition execution, state management | [`machine.py`](modulo_three/machine.py) | Yes - no domain logic |
| **Builder** | Transition table construction, validation | [`builder.py`](modulo_three/builder.py) | Yes - configurable |
| **Facade** | Input parsing, public API, caching | [`simple_facade.py`](modulo_three/simple_facade.py) | Domain-specific |

**Why this matters**: The engine contains **no modulo arithmetic**. This is a hard requirement from the specification—the FSM must be a pure lookup executor, not a calculator.

### 2. Table-Driven Transitions

The FSM uses a **lookup table** (`delta: Mapping[tuple[StateT, SymbolT], StateT]`) instead of computing transitions dynamically:

```python
# Machine definition (engine-agnostic)
machine = FiniteMachine(
    Q={0, 1, 2},              # States (remainders)
    Sigma={"0", "1"},          # Alphabet (binary digits)
    q0=0,                      # Initial state (remainder 0)
    F={0, 1, 2},              # All states are accepting
    delta={
        (0, "0"): 0, (0, "1"): 1,
        (1, "0"): 2, (1, "1"): 0,
        (2, "0"): 1, (2, "1"): 2,
    },
)
```

The transition function is constructed at build-time, not computed at runtime:

```python
# Builder creates the table (contains % operator)
transitions = {
    (state, symbol): (2 * state + int(symbol)) % mod  # % is OK here
    for state in states
    for symbol in alphabet
}
```

### 3. Generic Type Parameters

The FSM uses Python's generics to support arbitrary state and symbol types:

```python
class FiniteMachine[StateT: Hashable, SymbolT: Hashable]:
    ...
```

This enables:

- **Integer states** (modulo remainders: `0, 1, 2`)
- **Enum states** (for readable state names)
- **Custom types** (any hashable type)

### 4. Dataclasses with Slots

All data classes use `@dataclass(slots=True)` for:

- Memory efficiency (no `__dict__` overhead)
- Type safety (explicit field declarations)
- IDE support (autocomplete, go-to-definition)

### 5. Runtime Validation

The [`FiniteMachine`](modulo_three/machine.py:51) validates its definition on construction:

```python
def _validate_definition_total(self) -> None:
    # Validates:
    # 1. Q and Sigma are non-empty
    # 2. q0 ∈ Q
    # 3. F ⊆ Q
    # 4. All transitions reference valid states and symbols
    # 5. Transition function is TOTAL (complete) over Q × Σ
```

This catches misconfiguration early and provides clear error messages.

## Technology Choices

| Technology | Purpose | Justification |
| ---------- | ------- | ------------- |
| **Python 3.12+** | Core language | Type parameter syntax (`[T: Bound]`), no external dependencies |
| **Standard Library Only** | Dependencies | Zero runtime dependencies for the FSM engine |
| **pytest** | Testing | Industry standard, minimal config |
| **ruff** | Linting/formatting | Fast, single tool for lint + format |
| **mypy** + **pyright** | Type checking | Strict type safety verification |
| **pre-commit** | Git hooks | Enforces quality gates before commit |
| **Docker** | Reproducibility | Consistent environment, no setup required |

## Public API

### High-Level (Modulo-Three)

```python
from modulo_three import modThree

result = modThree("1011")  # Returns: 2
```

### Mid-Level (Reusable FSM)

```python
from modulo_three.builder import build_binary_mod_machine

machine = build_binary_mod_machine(3)  # Modulo-3 machine
remainder = machine.run("1011")         # Returns: 2
is_accepted = machine.accepts("1011")  # Returns: True
```

### Low-Level (Generic FSM Engine)

```python
from modulo_three.machine import FiniteMachine
from modulo_three.builder import DeterministicMachineSpec, DeterministicTableMachineBuilder

# Define a machine via configuration
spec = DeterministicMachineSpec(
    Q={0, 1, 2},
    Sigma={"0", "1"},
    q0=0,
    F={0, 1, 2},
    delta={...},  # Complete transition table
)

# Build and run
builder = DeterministicTableMachineBuilder()
machine = builder.from_spec(spec)
result = machine.run("011")
```

## Makefile Commands Reference

### Docker-Based Commands (Recommended)

All Make targets currently defined in `Makefile`:

| Target | Purpose | Notes / Example |
| ------ | ------- | --------------- |
| `make ensure-dev-image` | Ensures the dev image exists and is up to date | Compares a fingerprint from `pyproject.toml` + `Dockerfile.dev`; rebuilds only if changed |
| `make build-dev` | Builds the dev image | `make build-dev` |
| `make build` | Builds the app image from `Dockerfile` | `make build` |
| `make run ARGS=...` | Runs the app image | Builds app image first (`make build`), example: `make run ARGS=1011` |
| `make run-dev ARGS=...` | Runs app in dev container with source bind-mounted | Ensures dev image first, example: `make run-dev ARGS=1011` |
| `make test` | Runs pytest in dev container | Equivalent container command: `pytest -q tests` |
| `make lint` | Runs Ruff lint checks | Equivalent container command: `ruff check modulo_three tests` |
| `make format` | Runs Ruff formatter | Equivalent container command: `ruff format modulo_three tests` |
| `make typecheck` | Runs static type checks | Runs `mypy modulo_three tests && pyright` in dev container |
| `make check` | Runs full quality gate | Executes `lint`, `typecheck`, and `test` |
| `make pre-commit-install` | Installs git hooks through pre-commit | Installs `pre-commit` and `pre-push` hooks |
| `make pre-commit` | Runs all pre-commit hooks | Uses cached hook environment under `.cache/pre-commit` |
| `make docs` | Lists bundled markdown docs | Prints `README.md` and markdown files in `docs/` |

### Pre-commit Workflow

Use these two targets together:

1. Run `make pre-commit-install` once after cloning the repository (or again after hook config changes).
2. Run `make pre-commit` anytime you want to manually run all pre-commit-stage hooks against the full repo.
3. Commit normally with `git commit`; installed `pre-commit` hooks run automatically.
4. Push normally with `git push`; installed `pre-push` hooks run automatically.

Current hook behavior in this repository:

- `pre-commit` stage runs lint and type checks.
- `pre-push` stage runs `pytest`.
- Hook entries point to `.venv/bin/...`, so make sure the local virtual environment exists and dependencies are installed (for example, `pip install -e ".[dev]"`).

### Local Commands (Requires Python 3.12+)

```bash
# Install dependencies
pip install -e ".[dev]"

# Run directly (both flags are supported)
python -m modulo_three 1011
python -m modulo_three -i
python -m modulo_three --interactive
# Exit interactive mode with: exit, quit, or q

# Run tests
pytest tests

# Type check
mypy modulo_three tests
pyright

# Lint
ruff check modulo_three tests
ruff format modulo_three tests
```

## Extensibility Patterns

### Adding a New Modulo Machine

```python
from modulo_three.builder import build_binary_mod_machine

# Modulo-7 machine (reuses same engine!)
machine = build_binary_mod_machine(7)
result = machine.run("101101")  # Returns remainder mod 7
```

### Custom State Types with Enums

```python
from enum import Enum, auto
from modulo_three.builder import DeterministicMachineSpec, DeterministicTableMachineBuilder

class Phase(Enum):
    START = auto()
    MID = auto()
    END = auto()

spec = DeterministicMachineSpec(
    Q={Phase.START, Phase.MID, Phase.END},
    Sigma={0, 1},
    q0=Phase.START,
    F={Phase.END},
    delta={
        (Phase.START, 1): Phase.MID,
        (Phase.MID, 0): Phase.END,
    },
)

machine = DeterministicTableMachineBuilder().from_spec(spec)
```

### Custom Base/Modulus Combinations

The built-in helper supports binary (`base=2`) with any modulus (`>= 1`):

```python
# Build a modulo-5 machine for binary input
from modulo_three.builder import build_binary_mod_machine

machine = build_binary_mod_machine(5)
```

For non-binary bases, define a `DeterministicMachineSpec` with the right alphabet and transitions, then build it with `DeterministicTableMachineBuilder`.

```python
from modulo_three.builder import DeterministicMachineSpec, DeterministicTableMachineBuilder

base = 10
mod = 5
states = set(range(mod))
alphabet = {str(d) for d in range(base)}
transitions = {
    (state, digit): (base * state + int(digit)) % mod
    for state in states
    for digit in alphabet
}

spec = DeterministicMachineSpec(Q=states, Sigma=alphabet, q0=0, F=states, delta=transitions)
machine = DeterministicTableMachineBuilder[int, str]().from_spec(spec)
```

## Mathematical Foundation

### FSM State Invariant

For a modulo-`N` machine with base `b`:

```text
state == (value of consumed prefix) mod N
```

This invariant is maintained after each symbol processed. The transition function is:

```text
δ(r, d) = (b * r + d) mod N
```

Where:

- `r` = current remainder (state)
- `d` = next digit (symbol)
- `b` = base (2 for binary)
- `N` = modulus

### MSB-First Processing

The machine processes input left-to-right (MSB-first):

```python
"1011"  # 11 in decimal
# Process: '1' (8), then '0' (4), then '1' (2), then '1' (1)
# Result: 8 + 0 + 2 + 1 = 11 → 11 mod 3 = 2
```

## Testing Strategy

The test suite validates:

| Category | Coverage |
| -------- | -------- |
| Correctness | All required examples, comprehensive binary strings up to length 8 |
| Boundary | Empty string, leading zeros, modulus=1, binary alphabet coverage |
| Invalid Input | Non-string types, invalid characters, digits out of range |
| Separation | Engine contains no `%` operator (source-level check) |
| Performance | Long inputs (≥100,000 characters) for streaming verification |
| Equivalence | FSM results match mathematical recurrence |

See [`tests/`](tests/) for complete coverage.

## File Structure

```text
modulo-three/
├── modulo_three/           # Main package
│   ├── __init__.py        # Public API export
│   ├── __main__.py        # CLI entrypoint
│   ├── machine.py         # Generic FSM engine
│   ├── builder.py         # FSM construction
│   └── simple_facade.py   # Modulo-three facade
├── tests/                  # Test suite
│   ├── test_simple_facade.py
│   ├── test_machine_*.py
│   ├── test_builder_*.py
│   └── conftest.py
├── Makefile               # Build/test commands
├── pyproject.toml         # Project config
├── Dockerfile             # Production image
├── Dockerfile.dev         # Development image
└── README.md
```

## Assumptions and Constraints

1. **Input is MSB-first binary strings** (as specified)
2. **No external dependencies** for runtime execution
3. **No integer conversion** of the full input string
4. **Pure lookup** in the FSM engine (no `%` operator)
5. **Runtime validation** catches configuration errors early
