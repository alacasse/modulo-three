"""Shared assertion helpers for finite-machine tests."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from modulo_three.machine import FiniteMachine


def assert_machine_definition(
    machine: FiniteMachine[Any, Any],
    *,
    Q: set[Any],
    Sigma: set[Any],
    q0: Any,
    F: set[Any],
    delta: Mapping[tuple[Any, Any], Any],
) -> None:
    assert machine.Q == Q
    assert machine.Sigma == Sigma
    assert machine.q0 == q0
    assert machine.F == F
    assert dict(machine.delta) == dict(delta)


def assert_machine_is_snapshot_of_inputs_after_mutation(
    machine: FiniteMachine[Any, Any],
    *,
    source_states: set[Any],
    source_symbols: set[Any],
    source_accepting_states: set[Any],
    source_transitions: dict[tuple[Any, Any], Any],
    state_to_add: Any,
    symbol_to_add: Any,
    accepting_state_to_add: Any,
    transition_key_to_add: tuple[Any, Any],
    transition_value_to_add: Any,
) -> None:
    expected_states = set(machine.Q)
    expected_symbols = set(machine.Sigma)
    expected_q0 = machine.q0
    expected_accepting = set(machine.F)
    expected_transitions = dict(machine.delta)

    source_states.add(state_to_add)
    source_symbols.add(symbol_to_add)
    source_accepting_states.add(accepting_state_to_add)
    source_transitions[transition_key_to_add] = transition_value_to_add

    assert source_states != expected_states
    assert source_symbols != expected_symbols
    assert source_accepting_states != expected_accepting
    assert dict(source_transitions) != expected_transitions

    assert_machine_definition(
        machine,
        Q=expected_states,
        Sigma=expected_symbols,
        q0=expected_q0,
        F=expected_accepting,
        delta=expected_transitions,
    )
