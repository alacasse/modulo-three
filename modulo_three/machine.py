"""Finite machine model."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import SupportsInt, cast


@dataclass(slots=True)
class FiniteMachine[StateT: SupportsInt, SymbolT]:
    """Generic finite-machine 5-tuple data model."""

    Q: set[StateT]
    Sigma: set[SymbolT]
    q0: StateT
    F: set[StateT]
    delta: Mapping[tuple[StateT, SymbolT], StateT]

    def run(self, input: str) -> int:
        """Process input left-to-right and return the final state."""
        self._validate_input_type(input)
        current_state = self.q0
        for index, raw_symbol in enumerate(input):
            self._validate_symbol(index, raw_symbol)
            symbol = cast(SymbolT, raw_symbol)
            current_state = self.delta[(current_state, symbol)]
        return int(current_state)

    def _validate_input_type(self, input: object) -> None:
        """Hook for run input type validation."""
        if not isinstance(input, str):
            raise TypeError("input must be str")

    def _validate_symbol(self, index: int, symbol: object) -> None:
        """Hook for run symbol validation."""
        if symbol not in self.Sigma:
            raise ValueError(f"invalid symbol at index {index}: {symbol!r}")
