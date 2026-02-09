"""Tests for the simple facade without singleton coupling."""

from __future__ import annotations

from collections.abc import Callable
from itertools import product

import modulo_three.simple_facade as simple_facade_module
import pytest
from modulo_three.builder import build_binary_mod_machine
from modulo_three.machine import FiniteMachine
from modulo_three.simple_facade import modThree

MIN_LENGTH = 1
MAX_LENGTH = 8


def _reference_mod_three(binary_string: str) -> int:
    remainder = 0
    for char in binary_string:
        remainder = (2 * remainder + int(char)) % 3
    return remainder


@pytest.mark.parametrize(
    ("input_value", "expected"),
    [
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


def test_mod_three_rejects_empty_input() -> None:
    with pytest.raises(ValueError, match=r"input must be non-empty"):
        modThree("")


def test_mod_three_rejects_invalid_symbol() -> None:
    with pytest.raises(ValueError, match=r"invalid symbol at index 1: '2'"):
        modThree("12")


def test_mod_three_reuses_cached_machine(monkeypatch: pytest.MonkeyPatch) -> None:
    cache_factory = simple_facade_module.__dict__["_get_mod_three_machine"]
    cache_factory.cache_clear()
    build_count = 0
    original_build: Callable[[int], FiniteMachine[int, str]] = build_binary_mod_machine

    def counting_build(config: int) -> FiniteMachine[int, str]:
        nonlocal build_count
        build_count += 1
        return original_build(config)

    monkeypatch.setattr(simple_facade_module, "build_binary_mod_machine", counting_build)
    try:
        assert 2 == simple_facade_module.modThree("1011")
        assert 1 == simple_facade_module.modThree("1101")
        assert 1 == build_count
    finally:
        cache_factory.cache_clear()


@pytest.mark.parametrize("input_length", range(MIN_LENGTH, MAX_LENGTH + 1))
def test_mod_three_matches_reference_for_all_binary_strings_by_length(
    input_length: int,
) -> None:
    for bits in product("01", repeat=input_length):
        binary = "".join(bits)
        assert modThree(binary) == _reference_mod_three(binary)
