"""Deterministic finite-machine construction.

This module defines:
- a deterministic machine specification (`DeterministicMachineSpec`)
- a deterministic builder interface (`DeterministicMachineBuilder`)
- the standard table-based builder (`DeterministicTableMachineBuilder`)
- binary modulo helpers (`build_binary_mod_spec`, `build_binary_mod_machine`)
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Hashable, Mapping
from dataclasses import dataclass

from modulo_three.machine import FiniteMachine


@dataclass(slots=True)
class DeterministicMachineSpec[StateT: Hashable, SymbolT: Hashable]:
    """Lightweight specification for deterministic finite machines.

    Captures the state set, input alphabet, start state, accepting states, and
    deterministic transition table used to build a :class:`FiniteMachine`.
    """

    Q: set[StateT]
    Sigma: set[SymbolT]
    q0: StateT
    F: set[StateT]
    delta: Mapping[tuple[StateT, SymbolT], StateT]


class DeterministicMachineBuilder[StateT: Hashable, SymbolT: Hashable](ABC):
    """Build a FiniteMachine from a deterministic specification."""

    @abstractmethod
    def from_spec(
        self, spec: DeterministicMachineSpec[StateT, SymbolT]
    ) -> FiniteMachine[StateT, SymbolT]:
        """Construct and return a finite machine instance."""


class DeterministicTableMachineBuilder[StateT: Hashable, SymbolT: Hashable](
    DeterministicMachineBuilder[StateT, SymbolT]
):
    """Standard builder that materializes a finite machine from a deterministic spec.

    It supports arbitrary hashable state and symbol types with an explicit
    transition table.
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
