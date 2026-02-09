"""Tests for binary builder modulus validation."""

from __future__ import annotations

import pytest
from modulo_three.builder import build_binary_mod_spec


def test_bool_mod_raises_type_error() -> None:
    with pytest.raises(TypeError):
        build_binary_mod_spec(True)


def test_non_int_mod_raises_type_error() -> None:
    with pytest.raises(TypeError):
        build_binary_mod_spec("3")  # type: ignore[arg-type]


def test_mod_less_than_one_raises_value_error() -> None:
    with pytest.raises(ValueError):
        build_binary_mod_spec(0)
