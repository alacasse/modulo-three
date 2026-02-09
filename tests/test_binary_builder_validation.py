"""Tests for binary builder modulus validation."""

from __future__ import annotations

import pytest
from modulo_three.builder import build_binary_mod_spec


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
    large_mod = 10_000

    spec = build_binary_mod_spec(large_mod)

    assert len(spec.Q) == large_mod
    assert len(spec.delta) == large_mod * 2
