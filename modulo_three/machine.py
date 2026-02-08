"""Finite machine model."""

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

    def __post_init__(self) -> None:
        self._validate_definition()

    def run(self, input_symbols: Iterable[SymbolT]) -> StateT:
        """Process input left-to-right and return the final state."""
        current_state = self.q0
        for index, symbol in enumerate(input_symbols):
            if symbol not in self.Sigma:
                raise ValueError(f"invalid symbol at index {index}: {symbol!r}")
            current_state = self.delta[(current_state, symbol)]
        return current_state

    def _validate_definition(self) -> None:
        if self.q0 not in self.Q:
            raise ValueError("q0 must be a member of Q")
        if not self.F.issubset(self.Q):
            raise ValueError("F must be a subset of Q")

        for key, next_state in self.delta.items():
            state, symbol = key
            if state not in self.Q:
                raise ValueError("delta key state must be in Q")
            if symbol not in self.Sigma:
                raise ValueError("delta key symbol must be in Sigma")
            if next_state not in self.Q:
                raise ValueError("delta value must be in Q")
