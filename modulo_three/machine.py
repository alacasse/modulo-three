"""Finite machine model."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, Mapping, TypeVar

StateT = TypeVar("StateT")
SymbolT = TypeVar("SymbolT")


@dataclass(slots=True)
class FiniteMachine(Generic[StateT, SymbolT]):
    """Generic finite-machine 5-tuple data model."""

    Q: set[StateT]
    Sigma: set[SymbolT]
    q0: StateT
    F: set[StateT]
    delta: Mapping[tuple[StateT, SymbolT], StateT]
