"""Builder abstractions for finite-machine construction.

This module provides builder classes and helpers for constructing finite machines.

Note
----
The :class:`DeterministicTableMachineBuilder` and its associated tests are
primarily included to demonstrate the flexibility and extensibility of the
Builder pattern and the :class:`FiniteMachine` abstraction. They show how the
framework can be used with custom state types and explicit transition tables.

The binary modulo machine is provided via :func:`build_binary_mod_spec` and
:func:`build_binary_mod_machine`.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Hashable, Mapping
from dataclasses import dataclass

from modulo_three.machine import FiniteMachine


@dataclass(slots=True)
class DeterministicMachineSpec[StateT: Hashable, SymbolT: Hashable]:
    """Definition object for constructing deterministic finite machines.

    This class is primarily used to demonstrate the flexibility of the Builder
    pattern. See :class:`DeterministicTableMachineBuilder` for usage examples.
    It is intentionally lightweight to keep test setup and experimentation simple.
    """

    Q: set[StateT]
    Sigma: set[SymbolT]
    q0: StateT
    F: set[StateT]
    delta: Mapping[tuple[StateT, SymbolT], StateT]


class MachineBuilder[StateT: Hashable, SymbolT: Hashable](ABC):
    """Build a FiniteMachine from a deterministic specification."""

    @abstractmethod
    def from_spec(
        self, spec: DeterministicMachineSpec[StateT, SymbolT]
    ) -> FiniteMachine[StateT, SymbolT]:
        """Construct and return a finite machine instance."""


class DeterministicTableMachineBuilder[StateT: Hashable, SymbolT: Hashable](
    MachineBuilder[StateT, SymbolT]
):
    """Builder that creates a finite machine from an explicit transition table.

    This builder is included to demonstrate the flexibility of the Builder
    pattern and the :class:`FiniteMachine` abstraction. It allows constructing
    machines with arbitrary hashable state and symbol types using an explicit
    transition table.

    Note
    ----
    This class and its test suite (:mod:`tests.test_table_builder`) are primarily
    for demonstration purposes. The binary modulo helpers are the actual
    construction path used in this project.
    """

    def from_spec(
        self,
        spec: DeterministicMachineSpec[StateT, SymbolT],
    ) -> FiniteMachine[StateT, SymbolT]:
        return FiniteMachine(
            Q=set(spec.Q),
            Sigma=set(spec.Sigma),
            q0=spec.q0,
            F=set(spec.F),
            delta=dict(spec.delta),
        )


def build_binary_mod_spec(mod: int) -> DeterministicMachineSpec[int, str]:
    _validate_mod(mod)

    states = set(range(mod))
    alphabet = {"0", "1"}
    transitions: dict[tuple[int, str], int] = {
        (state, symbol): (2 * state + int(symbol)) % mod
        for state in states
        for symbol in alphabet
    }

    return DeterministicMachineSpec(
        Q=states,
        Sigma=alphabet,
        q0=0,
        F=set(states),
        delta=transitions,
    )


def build_binary_mod_machine(mod: int) -> FiniteMachine[int, str]:
    spec = build_binary_mod_spec(mod)
    return DeterministicTableMachineBuilder[int, str]().from_spec(spec)


def _validate_mod(mod: object) -> None:
    if isinstance(mod, bool) or not isinstance(mod, int):
        raise TypeError("mod must be int")
    if mod < 1:
        raise ValueError("mod must be >= 1")
