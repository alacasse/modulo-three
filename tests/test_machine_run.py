"""Tests for finite-machine run-loop behavior."""

from __future__ import annotations

from modulo_three.machine import FiniteMachine


def test_empty_input_returns_start_state() -> None:
    machine = FiniteMachine(
        Q={0, 1, 2},
        Sigma={"a", "b"},
        q0=1,
        F={0, 1, 2},
        delta={},
    )

    assert 1 == machine.run("")


def test_simple_deterministic_trace_returns_final_state() -> None:
    machine = FiniteMachine(
        Q={0, 1, 2},
        Sigma={"a", "b"},
        q0=0,
        F={0, 1, 2},
        delta={
            (0, "a"): 1,
            (1, "b"): 2,
        },
    )

    assert 2 == machine.run("ab")


def test_run_supports_non_string_symbols() -> None:
    machine = FiniteMachine(
        Q={0, 1, 2},
        Sigma={0, 1},
        q0=0,
        F={0, 1, 2},
        delta={
            (0, 0): 1,
            (1, 1): 2,
        },
    )

    assert 2 == machine.run([0, 1])


def test_run_returns_non_int_state_type() -> None:
    machine = FiniteMachine(
        Q={"START", "MID", "END"},
        Sigma={"a", "b"},
        q0="START",
        F={"END"},
        delta={
            ("START", "a"): "MID",
            ("MID", "b"): "END",
        },
    )

    assert "END" == machine.run("ab")


def test_accepts_returns_true_when_final_state_is_accepting() -> None:
    machine = FiniteMachine(
        Q={0, 1},
        Sigma={"a"},
        q0=0,
        F={1},
        delta={
            (0, "a"): 1,
        },
    )

    assert machine.accepts("a") is True


def test_accepts_returns_false_when_final_state_is_not_accepting() -> None:
    machine = FiniteMachine(
        Q={0, 1},
        Sigma={"a"},
        q0=0,
        F={1},
        delta={
            (0, "a"): 0,
        },
    )

    assert machine.accepts("a") is False
