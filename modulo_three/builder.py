"""Builder abstractions for finite-machine construction."""

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
    """Definition object for constructing deterministic finite machines."""

    Q: set[StateT]
    Sigma: set[SymbolT]
    q0: StateT
    F: set[StateT]
    delta: Mapping[tuple[StateT, SymbolT], StateT]


class DeterministicTableMachineBuilder[StateT: Hashable, SymbolT: Hashable](
    FiniteMachineBuilder[StateT, SymbolT, DeterministicMachineSpec[StateT, SymbolT]]
):
    """Builder that creates a finite machine from an explicit transition table."""

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
