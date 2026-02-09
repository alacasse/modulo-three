"""Tests for finite-machine run-loop behavior."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any

import pytest
from modulo_three.machine import FiniteMachine

type MachineFactory = Callable[
    [set[Any], set[Any], Any, set[Any], Mapping[tuple[Any, Any], Any]],
    FiniteMachine[Any, Any],
]


def test_delta_must_be_total(
    machine_factory: MachineFactory,
) -> None:
    with pytest.raises(
        ValueError,
        match=r"delta must be total over QxSigma: expected=6, actual=0",
    ):
        machine_factory({0, 1, 2}, {"a", "b"}, 1, {0, 1, 2}, {})


def test_simple_deterministic_trace_returns_final_state(
    machine_factory: MachineFactory,
) -> None:
    machine = machine_factory(
        {0, 1, 2},
        {"a", "b"},
        0,
        {0, 1, 2},
        {
            (0, "a"): 1,
            (0, "b"): 0,
            (1, "a"): 1,
            (1, "b"): 2,
            (2, "a"): 2,
            (2, "b"): 2,
        },
    )

    assert 2 == machine.run("ab")


def test_run_supports_non_string_symbols(machine_factory: MachineFactory) -> None:
    machine = machine_factory(
        {0, 1, 2},
        {0, 1},
        0,
        {0, 1, 2},
        {
            (0, 0): 1,
            (0, 1): 0,
            (1, 0): 1,
            (1, 1): 2,
            (2, 0): 2,
            (2, 1): 2,
        },
    )

    assert 2 == machine.run([0, 1])


def test_run_returns_non_int_state_type(machine_factory: MachineFactory) -> None:
    machine = machine_factory(
        {"START", "MID", "END"},
        {"a", "b"},
        "START",
        {"END"},
        {
            ("START", "a"): "MID",
            ("START", "b"): "START",
            ("MID", "a"): "MID",
            ("MID", "b"): "END",
            ("END", "a"): "END",
            ("END", "b"): "END",
        },
    )

    assert "END" == machine.run("ab")


def test_run_empty_input_returns_initial_state(
    ab_step_machine: FiniteMachine[int, str],
) -> None:
    assert ab_step_machine.run([]) == ab_step_machine.q0


def test_run_empty_string_returns_initial_state(
    ab_step_machine: FiniteMachine[int, str],
) -> None:
    assert ab_step_machine.run("") == ab_step_machine.q0


def test_accepts_returns_true_when_final_state_is_accepting(
    machine_factory: MachineFactory,
) -> None:
    machine = machine_factory(
        {0, 1},
        {"a"},
        0,
        {1},
        {
            (0, "a"): 1,
            (1, "a"): 1,
        },
    )

    assert machine.accepts("a") is True


def test_accepts_returns_false_when_final_state_is_not_accepting(
    machine_factory: MachineFactory,
) -> None:
    machine = machine_factory(
        {0, 1},
        {"a"},
        0,
        {1},
        {
            (0, "a"): 0,
            (1, "a"): 1,
        },
    )

    assert machine.accepts("a") is False


def test_accepts_empty_input_true_when_q0_is_accepting(
    ab_step_machine: FiniteMachine[int, str],
) -> None:
    assert ab_step_machine.accepts([]) is True


def test_accepts_empty_input_false_when_q0_is_not_accepting(
    machine_factory: MachineFactory,
) -> None:
    machine = machine_factory(
        {0, 1},
        {"a"},
        0,
        {1},
        {
            (0, "a"): 0,
            (1, "a"): 1,
        },
    )

    assert machine.accepts([]) is False


def test_accepts_empty_string_true_when_q0_is_accepting(
    ab_step_machine: FiniteMachine[int, str],
) -> None:
    assert ab_step_machine.accepts("") is True


def test_accepts_empty_string_false_when_q0_is_not_accepting(
    machine_factory: MachineFactory,
) -> None:
    machine = machine_factory(
        {0, 1},
        {"a"},
        0,
        {1},
        {
            (0, "a"): 0,
            (1, "a"): 1,
        },
    )

    assert machine.accepts("") is False


@pytest.mark.parametrize(
    ("from_state", "input_symbol", "expected_next_state"),
    [
        (0, "a", 1),
        (1, "b", 0),
    ],
)
def test_step_returns_next_state(
    ab_step_machine: FiniteMachine[int, str],
    from_state: int,
    input_symbol: str,
    expected_next_state: int,
) -> None:
    assert ab_step_machine.step(from_state, input_symbol) == expected_next_state


def test_step_raises_value_error_for_invalid_symbol_without_index(
    ab_step_machine: FiniteMachine[int, str],
) -> None:
    with pytest.raises(ValueError, match=r"invalid symbol: 'z'"):
        ab_step_machine.step(0, "z")
