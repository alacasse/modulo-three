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

from collections.abc import Hashable, Iterable, Mapping
from dataclasses import dataclass


@dataclass(slots=True)
class FiniteMachine[StateT: Hashable, SymbolT: Hashable]:
    """Generic finite-machine 5-tuple data model.

    A deterministic finite automaton (DFA) processes an input sequence of symbols
    from left to right, transitioning between states according to a transition
    function. If the machine ends in a state that is a member of F, the input
    is considered accepted.

    This class enforces the mathematical constraints of a valid finite automaton
    through runtime validation in :meth:`_validate_definition`.

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
        self._validate_definition()

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
            ValueError: If any input symbol is not in the alphabet Σ, or if a
                transition is undefined for a valid (state, symbol) pair.

        Note:
            This implements a deterministic finite automaton (DFA), where each
            (state, symbol) pair has exactly one transition defined in delta.
        """
        current_state = self.q0
        for index, symbol in enumerate(input_symbols):
            if symbol not in self.Sigma:
                raise ValueError(f"invalid symbol at index {index}: {symbol!r}")
            transition_key = (current_state, symbol)
            if transition_key not in self.delta:
                raise ValueError(
                    f"missing transition at index {index}: "
                    f"state={current_state!r}, symbol={symbol!r}"
                )
            current_state = self.delta[transition_key]
        return current_state

    def _validate_definition(self) -> None:
        """Validate the mathematical constraints of a finite automaton.

        A valid finite machine definition must satisfy:
        1. The initial state q0 must exist in Q
        2. All accepting states F must be valid states in Q
        3. All transition source states must be in Q
        4. All transition input symbols must be in Σ
        5. All transition destination states must be in Q

        These constraints ensure the machine is well-formed and can process
        any valid input without encountering undefined states or symbols.
        """
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
