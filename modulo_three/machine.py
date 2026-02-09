"""Finite machine model.

This module provides a generic implementation of a deterministic finite automaton
(DFA), also known as a finite state machine (FSM). The implementation follows the
standard mathematical model of a 5-tuple: (Q, Σ, q₀, F, δ).

The 5-tuple components are:
    - Q: Set of states (the finite set of internal configurations)
    - Σ: Set of input symbols (the finite input alphabet)
    - q₀: Initial state (a distinguished member of Q)
    - F: Set of final/accepting states (a subset of Q)
    - δ: Transition function (Q × Σ → Q)

Type Parameters:
    StateT: The type of states. Must be hashable for use in sets and dict keys.
    SymbolT: The type of input symbols. Must be hashable for validation and dict keys.

Example:
    A simple parity machine that tracks whether the count of 1-bits is even or odd::

        from modulo_three.machine import FiniteMachine

        states = {0, 1}  # 0 = even, 1 = odd
        alphabet = {'1'}  # Only track '1' bits
        transitions = {
            (0, '1'): 1,
            (1, '1'): 0,
        }
        machine = FiniteMachine(
            Q=states,
            Sigma=alphabet,
            q0=0,
            F={0},  # Even count is accepting
            delta=transitions,
        )
        assert machine.run(['1', '1']) == 0  # even
        assert machine.run(['1']) == 1  # odd
"""

from __future__ import annotations

from collections.abc import Hashable, Iterable, Mapping
from dataclasses import dataclass


@dataclass(slots=True)
class FiniteMachine[StateT: Hashable, SymbolT: Hashable]:
    """Total deterministic finite-machine 5-tuple data model.

    A deterministic finite automaton (DFA) processes an input sequence of symbols
    from left to right, transitioning between states according to a transition
    function. If the machine ends in a state that is a member of F, the input
    is considered accepted.

    This class enforces the mathematical constraints of a valid total DFA through
    runtime validation in :meth:`_validate_definition_total`.

    Type Parameters:
        StateT: The type used for states. Must be hashable since states are stored
            in sets and used as dictionary keys in the transition function.
        SymbolT: The type used for input symbols. Must be hashable for validation
            against the alphabet and for use as dictionary keys.
    """

    Q: set[StateT]
    """Set of all possible states in the machine. Must contain q0 and all F states."""
    Sigma: set[SymbolT]
    """Set of valid input symbols (the alphabet). All input symbols processed by
    the machine must be members of this set."""
    q0: StateT
    """The initial/starting state. Must be a member of Q."""
    F: set[StateT]
    """Set of accepting/final states. A subset of Q. The machine 'accepts' input
    if it ends in a state that is a member of this set."""
    delta: Mapping[tuple[StateT, SymbolT], StateT]
    """Transition function mapping (state, symbol) pairs to next states.
    This is the core of the DFA: for each state and valid input symbol,
    exactly one next state is defined. Keys are (state, symbol) tuples."""

    def __post_init__(self) -> None:
        # Defensive copies to avoid aliasing surprises.
        object.__setattr__(self, "Q", set(self.Q))
        object.__setattr__(self, "Sigma", set(self.Sigma))
        object.__setattr__(self, "F", set(self.F))
        object.__setattr__(self, "delta", dict(self.delta))

        self._validate_definition_total()

    def run(self, input_symbols: Iterable[SymbolT]) -> StateT:
        """Process input left-to-right and return the final state.

        Starting from the initial state q0, this method sequentially applies
        the transition function δ for each input symbol. The transition lookup
        uses (current_state, symbol) as the key in the delta mapping.

        Args:
            input_symbols: An iterable of symbols from the alphabet Σ.

        Returns:
            The final state after processing all input symbols.

        Raises:
            ValueError: If any input symbol is not in the alphabet Σ.

        Note:
            This implements a deterministic finite automaton (DFA). The
            transition function is total, so every (state, symbol) pair is
            defined in delta.
        """
        current_state = self.q0
        for index, symbol in enumerate(input_symbols):
            if symbol not in self.Sigma:
                raise ValueError(f"invalid symbol at index {index}: {symbol!r}")
            current_state = self.delta[(current_state, symbol)]
        return current_state

    def accepts(self, input_symbols: Iterable[SymbolT]) -> bool:
        """Return True if the input is accepted by the machine.

        A DFA accepts input when the final state after processing the input
        belongs to the accepting set F.
        """
        return self.run(input_symbols) in self.F

    def _validate_definition_total(self) -> None:
        """Validate the mathematical constraints of a total DFA.

        A valid finite machine definition must satisfy:
        1. Q and Sigma must be non-empty
        2. The initial state q0 must exist in Q
        3. All accepting states F must be valid states in Q
        4. All transition source states must be in Q
        5. All transition input symbols must be in Sigma
        6. All transition destination states must be in Q
        7. The transition function is total over QxSigma

        These constraints ensure the machine is well-formed and can process
        any valid input without encountering undefined states or symbols.
        """
        if not self.Q:
            raise ValueError("Q must be non-empty")
        if not self.Sigma:
            raise ValueError("Sigma must be non-empty")
        if self.q0 not in self.Q:
            raise ValueError(f"q0 must be a member of Q: q0={self.q0!r}")
        if not self.F.issubset(self.Q):
            extra = self.F.difference(self.Q)
            raise ValueError(f"F must be a subset of Q: extra={extra!r}")

        for key, next_state in self.delta.items():
            state, symbol = key
            if state not in self.Q:
                raise ValueError(
                    f"delta key state must be in Q: state={state!r}, symbol={symbol!r}"
                )
            if symbol not in self.Sigma:
                raise ValueError(
                    f"delta key symbol must be in Sigma: state={state!r}, symbol={symbol!r}"
                )
            if next_state not in self.Q:
                raise ValueError(
                    f"delta value must be in Q: key={(state, symbol)!r}, next_state={next_state!r}"
                )

        expected_count = len(self.Q) * len(self.Sigma)
        if len(self.delta) != expected_count:
            missing = [
                (state, symbol)
                for state in self.Q
                for symbol in self.Sigma
                if (state, symbol) not in self.delta
            ]
            if missing:
                suffix = " (truncated)" if len(missing) > 10 else ""
                details = f"missing={missing[:10]!r}{suffix}"
            else:
                details = "delta size mismatch"
            raise ValueError(
                "delta must be total over QxSigma: "
                f"expected={expected_count}, actual={len(self.delta)}; {details}"
            )
