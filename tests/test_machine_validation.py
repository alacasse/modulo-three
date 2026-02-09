"""Tests for finite-machine run input validation."""

from __future__ import annotations

import pytest
from modulo_three.machine import FiniteMachine


def test_run_raises_type_error_for_non_iterable_input(
    ab_step_machine: FiniteMachine[int, str],
) -> None:
    with pytest.raises(TypeError):
        ab_step_machine.run(123)  # type: ignore[arg-type]


def test_run_raises_value_error_for_invalid_symbol_with_index(
    ab_step_machine: FiniteMachine[int, str],
) -> None:
    with pytest.raises(
        ValueError,
        match=r"invalid symbol at index 1: 'z'",
    ):
        ab_step_machine.run("az")
