"""Tests for the simple facade without singleton coupling."""

from __future__ import annotations

import pytest
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
