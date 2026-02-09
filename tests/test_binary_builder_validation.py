"""Tests for binary builder modulus validation."""

from __future__ import annotations

import pytest
from modulo_three.builder import build_binary_mod_machine, build_binary_mod_spec
from modulo_three.machine import FiniteMachine

LARGE_MOD = 10_000


@pytest.mark.parametrize("mod", [True, False])
def test_bool_mod_values_raise_type_error_even_though_bool_is_int_subclass(
    mod: bool,
) -> None:
    with pytest.raises(TypeError):
        build_binary_mod_spec(mod)


def test_non_int_mod_raises_type_error() -> None:
    with pytest.raises(TypeError):
        build_binary_mod_spec("3")  # type: ignore[arg-type]


@pytest.mark.parametrize("mod", [-1, -10])
def test_negative_mod_values_raise_value_error(mod: int) -> None:
    with pytest.raises(ValueError):
        build_binary_mod_spec(mod)


def test_mod_zero_raises_value_error() -> None:
    with pytest.raises(ValueError):
        build_binary_mod_spec(0)


def test_mod_one_builds_single_state_spec() -> None:
    spec = build_binary_mod_spec(1)

    assert spec.Q == {0}
    assert spec.Sigma == {"0", "1"}
    assert spec.q0 == 0
    assert spec.F == {0}
    assert dict(spec.delta) == {
        (0, "0"): 0,
        (0, "1"): 0,
    }


def test_large_mod_builds_expected_state_and_transition_counts() -> None:
    spec = build_binary_mod_spec(LARGE_MOD)

    assert len(spec.Q) == LARGE_MOD
    assert len(spec.delta) == LARGE_MOD * 2


def test_build_binary_mod_machine_returns_finite_machine() -> None:
    machine = build_binary_mod_machine(3)

    assert isinstance(machine, FiniteMachine)


def test_build_binary_mod_machine_mod_2_produces_correct_transitions() -> None:
    machine = build_binary_mod_machine(2)

    assert machine.Q == {0, 1}
    assert machine.Sigma == {"0", "1"}
    assert machine.q0 == 0
    assert machine.F == {0, 1}
    assert dict(machine.delta) == {
        (0, "0"): 0,
        (0, "1"): 1,
        (1, "0"): 0,
        (1, "1"): 1,
    }


def test_build_binary_mod_machine_mod_4_produces_correct_transitions() -> None:
    machine = build_binary_mod_machine(4)

    assert machine.Q == {0, 1, 2, 3}
    assert machine.Sigma == {"0", "1"}
    assert machine.q0 == 0
    assert machine.F == {0, 1, 2, 3}
    assert dict(machine.delta) == {
        (0, "0"): 0,
        (0, "1"): 1,
        (1, "0"): 2,
        (1, "1"): 3,
        (2, "0"): 0,
        (2, "1"): 1,
        (3, "0"): 2,
        (3, "1"): 3,
    }
