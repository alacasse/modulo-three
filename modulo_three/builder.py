"""Builder abstractions for finite-machine construction."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import SupportsInt

from modulo_three.machine import FiniteMachine


class FiniteMachineBuilder[StateT: SupportsInt, SymbolT](ABC):
    """Base contract for builders that construct finite machines."""

    @abstractmethod
    def build(self, mod: int) -> FiniteMachine[StateT, SymbolT]:
        """Construct and return a finite machine instance."""


class BinaryModFiniteMachineBuilder(FiniteMachineBuilder[int, str]):
    """Builder for binary modulo finite machines."""

    def build(self, mod: int) -> FiniteMachine[int, str]:
        self._validate_mod(mod)
        states = set(range(mod))
        return FiniteMachine(
            Q=states,
            Sigma={"0", "1"},
            q0=0,
            F=set(states),
            delta={},
        )

    def _validate_mod(self, mod: object) -> None:
        if isinstance(mod, bool) or not isinstance(mod, int):
            raise TypeError("mod must be int")
        if mod < 1:
            raise ValueError("mod must be >= 1")
