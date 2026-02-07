"""Tests for the finite-machine 5-tuple data model."""

from __future__ import annotations

from modulo_three.machine import FiniteMachine


def test_fields_exist_and_are_readable() -> None:
    states = {0, 1, 2}
    alphabet = {"a", "b"}
    start_state = 0
    accepting_states = {0, 2}
    transitions = {
        (0, "a"): 1,
        (1, "b"): 2,
    }

    machine = FiniteMachine(
        Q=states,
        Sigma=alphabet,
        q0=start_state,
        F=accepting_states,
        delta=transitions,
    )

    assert states == machine.Q
    assert alphabet == machine.Sigma
    assert start_state == machine.q0
    assert accepting_states == machine.F
    assert transitions == machine.delta
