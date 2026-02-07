"""Tests for binary builder modulus validation."""

from __future__ import annotations

import pytest
from modulo_three.builder import BinaryModFiniteMachineBuilder


@pytest.fixture
def builder() -> BinaryModFiniteMachineBuilder:
    return BinaryModFiniteMachineBuilder()


def test_bool_mod_raises_type_error(builder: BinaryModFiniteMachineBuilder) -> None:
    with pytest.raises(TypeError):
        builder.build(True)


def test_non_int_mod_raises_type_error(builder: BinaryModFiniteMachineBuilder) -> None:
    with pytest.raises(TypeError):
        builder.build("3")  # type: ignore[arg-type]


def test_mod_less_than_one_raises_value_error(
    builder: BinaryModFiniteMachineBuilder,
) -> None:
    with pytest.raises(ValueError):
        builder.build(0)
