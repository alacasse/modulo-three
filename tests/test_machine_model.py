"""Tests for the finite-machine 5-tuple data model."""

from __future__ import annotations

import pytest
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


def test_init_raises_when_q0_not_in_q() -> None:
    with pytest.raises(ValueError, match=r"q0 must be a member of Q"):
        FiniteMachine(
            Q={1, 2},
            Sigma={"a"},
            q0=0,
            F={1},
            delta={(1, "a"): 2},
        )


def test_init_raises_when_f_is_not_subset_of_q() -> None:
    with pytest.raises(ValueError, match=r"F must be a subset of Q"):
        FiniteMachine(
            Q={0, 1},
            Sigma={"a"},
            q0=0,
            F={0, 2},
            delta={(0, "a"): 1},
        )


def test_init_raises_when_transition_state_not_in_q() -> None:
    with pytest.raises(ValueError, match=r"delta key state must be in Q"):
        FiniteMachine(
            Q={0, 1},
            Sigma={"a"},
            q0=0,
            F={1},
            delta={(2, "a"): 1},
        )


def test_init_raises_when_transition_symbol_not_in_sigma() -> None:
    with pytest.raises(ValueError, match=r"delta key symbol must be in Sigma"):
        FiniteMachine(
            Q={0, 1},
            Sigma={"a"},
            q0=0,
            F={1},
            delta={(0, "b"): 1},
        )


def test_init_raises_when_transition_target_not_in_q() -> None:
    with pytest.raises(ValueError, match=r"delta value must be in Q"):
        FiniteMachine(
            Q={0, 1},
            Sigma={"a"},
            q0=0,
            F={1},
            delta={(0, "a"): 2},
        )
