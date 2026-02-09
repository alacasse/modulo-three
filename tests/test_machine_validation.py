"""Tests for finite-machine run input validation."""

from __future__ import annotations

import pytest
from modulo_three.machine import FiniteMachine


def _machine() -> FiniteMachine[int, str]:
    return FiniteMachine(
        Q={0, 1},
        Sigma={"a", "b"},
        q0=0,
        F={0, 1},
        delta={
            (0, "a"): 1,
            (1, "b"): 0,
        },
    )


def test_run_raises_type_error_for_non_iterable_input() -> None:
    machine = _machine()
    with pytest.raises(TypeError):
        machine.run(123)  # type: ignore[arg-type]


def test_run_raises_value_error_for_invalid_symbol_with_index() -> None:
    machine = _machine()
    with pytest.raises(
        ValueError,
        match=r"invalid symbol at index 1: 'z'",
    ):
        machine.run("az")


def test_run_raises_value_error_for_missing_transition() -> None:
    machine = _machine()
    with pytest.raises(
        ValueError,
        match=r"missing transition at index 1: state=1, symbol='a'",
    ):
        machine.run("aa")
