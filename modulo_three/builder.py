"""Builder abstractions for finite-machine construction."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from modulo_three.machine import FiniteMachine

StateT = TypeVar("StateT")
SymbolT = TypeVar("SymbolT")


class FiniteMachineBuilder(ABC, Generic[StateT, SymbolT]):
    """Base contract for builders that construct finite machines."""

    @abstractmethod
    def build(self) -> FiniteMachine[StateT, SymbolT]:
        """Construct and return a finite machine instance."""
