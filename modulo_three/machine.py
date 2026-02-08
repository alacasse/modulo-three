"""Finite machine model."""

from __future__ import annotations

from collections.abc import Hashable, Iterable, Mapping
from dataclasses import dataclass


@dataclass(slots=True)
class FiniteMachine[StateT: Hashable, SymbolT: Hashable]:
    """Generic finite-machine 5-tuple data model."""

    Q: set[StateT]
    Sigma: set[SymbolT]
    q0: StateT
    F: set[StateT]
    delta: Mapping[tuple[StateT, SymbolT], StateT]

    def run(self, input_symbols: Iterable[SymbolT]) -> StateT:
        """Process input left-to-right and return the final state."""
        try:
            symbols = iter(input_symbols)
        except TypeError as exc:
            raise TypeError("input_symbols must be iterable") from exc

        current_state = self.q0
        for index, symbol in enumerate(symbols):
            self._validate_symbol(index, symbol)
            current_state = self.delta[(current_state, symbol)]
        return current_state

    def _validate_symbol(self, index: int, symbol: SymbolT) -> None:
        """Hook for run symbol validation."""
        if symbol not in self.Sigma:
            raise ValueError(f"invalid symbol at index {index}: {symbol!r}")
