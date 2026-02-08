"""Builder abstractions for finite-machine construction.

This module provides builder classes for constructing finite machines.

Note
----
The :class:`DeterministicTableMachineBuilder` and its associated tests are
primarily included to demonstrate the flexibility and extensibility of the
Builder pattern and the :class:`FiniteMachine` abstraction. They show how the
framework can be used with custom state types and explicit transition tables.

The :class:`BinaryModFiniteMachineBuilder` is the primary implementation used
in this project for creating binary modulo finite machines.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Hashable, Mapping
from dataclasses import dataclass

from modulo_three.machine import FiniteMachine


class FiniteMachineBuilder[StateT: Hashable, SymbolT: Hashable, BuildInputT](ABC):
    """Base contract for builders that construct finite machines."""

    @abstractmethod
    def build(self, config: BuildInputT) -> FiniteMachine[StateT, SymbolT]:
        """Construct and return a finite machine instance."""


@dataclass(slots=True)
class DeterministicMachineSpec[StateT: Hashable, SymbolT: Hashable]:
    """Definition object for constructing deterministic finite machines.

    This class is primarily used to demonstrate the flexibility of the Builder
    pattern. See :class:`DeterministicTableMachineBuilder` for usage examples.
    """

    Q: set[StateT]
    Sigma: set[SymbolT]
    q0: StateT
    F: set[StateT]
    delta: Mapping[tuple[StateT, SymbolT], StateT]


class DeterministicTableMachineBuilder[StateT: Hashable, SymbolT: Hashable](
    FiniteMachineBuilder[StateT, SymbolT, DeterministicMachineSpec[StateT, SymbolT]]
):
    """Builder that creates a finite machine from an explicit transition table.

    This builder is included to demonstrate the flexibility of the Builder
    pattern and the :class:`FiniteMachine` abstraction. It allows constructing
    machines with arbitrary hashable state and symbol types using an explicit
    transition table.

    Note
    ----
    This class and its test suite (:mod:`tests.test_table_builder`) are primarily
    for demonstration purposes. The :class:`BinaryModFiniteMachineBuilder` is
    the actual builder used in this project.
    """

    def build(
        self,
        config: DeterministicMachineSpec[StateT, SymbolT],
    ) -> FiniteMachine[StateT, SymbolT]:
        return FiniteMachine(
            Q=set(config.Q),
            Sigma=set(config.Sigma),
            q0=config.q0,
            F=set(config.F),
            delta=dict(config.delta),
        )


class BinaryModFiniteMachineBuilder(FiniteMachineBuilder[int, str, int]):
    """Builder for binary modulo finite machines."""

    def build(self, config: int) -> FiniteMachine[int, str]:
        self._validate_mod(config)
        states = set(range(config))
        alphabet = {"0", "1"}
        transitions = {
            (state, symbol): (2 * state + int(symbol)) % config
            for state in states
            for symbol in alphabet
        }
        return FiniteMachine(
            Q=states,
            Sigma=alphabet,
            q0=0,
            F=set(states),
            delta=transitions,
        )

    def _validate_mod(self, mod: object) -> None:
        if isinstance(mod, bool) or not isinstance(mod, int):
            raise TypeError("mod must be int")
        if mod < 1:
            raise ValueError("mod must be >= 1")
