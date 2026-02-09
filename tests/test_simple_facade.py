"""Tests for the simple facade without singleton coupling."""

from __future__ import annotations

import importlib
from collections.abc import Callable
from itertools import product

import modulo_three.simple_facade as simple_facade_module
import pytest
from modulo_three.builder import BinaryModFiniteMachineBuilder
from modulo_three.machine import FiniteMachine
from modulo_three.simple_facade import modThree


@pytest.mark.parametrize(
    ("input_value", "expected"),
    [
        ("", 0),
        ("1101", 1),
        ("1110", 2),
        ("1111", 0),
        ("110", 0),
        ("1011", 2),
        ("0001011", 2),
    ],
)
def test_mod_three_returns_expected_remainder(input_value: str, expected: int) -> None:
    assert modThree(input_value) == expected


def test_mod_three_rejects_non_string_input() -> None:
    with pytest.raises(TypeError, match=r"input must be str"):
        modThree(123)  # type: ignore[arg-type]


def test_mod_three_rejects_invalid_symbol() -> None:
    with pytest.raises(ValueError, match=r"invalid symbol at index 1: '2'"):
        modThree("12")


def test_mod_three_reuses_cached_machine(monkeypatch: pytest.MonkeyPatch) -> None:
    facade = importlib.reload(simple_facade_module)
    build_count = 0
    original_build: Callable[[BinaryModFiniteMachineBuilder, int], FiniteMachine[int, str]] = (
        facade.BinaryModFiniteMachineBuilder.build
    )

    def counting_build(
        self: BinaryModFiniteMachineBuilder,
        config: int,
    ) -> FiniteMachine[int, str]:
        nonlocal build_count
        build_count += 1
        return original_build(self, config)

    monkeypatch.setattr(facade.BinaryModFiniteMachineBuilder, "build", counting_build)

    assert 2 == facade.modThree("1011")
    assert 1 == facade.modThree("1101")
    assert 1 == build_count


def test_mod_three_produces_correct_result_for_all_binary_strings_of_length_0_to_8() -> None:
    """Verify modThree matches the mathematical formula for all binary inputs up to length 8.

    This is an exhaustive test that generates every possible binary string
    from length 0 ("") to length 8 ("11111111") and compares the result
    against a known-correct reference implementation.
    """

    # Reference: mathematical formula for computing binary modulo 3
    def reference_mod_three(binary_string: str) -> int:
        remainder = 0
        for char in binary_string:
            remainder = (2 * remainder + int(char)) % 3
        return remainder

    # Generate all possible binary strings from length 0 to 8
    # "01" represents the two valid symbols, and repeat controls string length
    for length in range(9):  # lengths 0 through 8 inclusive
        # product generates every combination of "0" and "1" of this length
        for bits in product("01", repeat=length):
            binary_input = "".join(bits)
            assert modThree(binary_input) == reference_mod_three(binary_input)
