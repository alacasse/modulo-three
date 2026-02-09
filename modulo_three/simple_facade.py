"""Simple public facade for modulo-three computation."""

from __future__ import annotations

from functools import lru_cache

from modulo_three.builder import build_binary_mod_machine
from modulo_three.machine import FiniteMachine


def _require_str(input_value: object) -> str:
    if not isinstance(input_value, str):
        raise TypeError("input must be str")
    if input_value == "":
        raise ValueError("input must be non-empty")
    return input_value


@lru_cache(maxsize=1)
def _get_mod_three_machine() -> FiniteMachine[int, str]:
    return build_binary_mod_machine(3)


def modThree(input: str) -> int:
    input_value = _require_str(input)
    machine = _get_mod_three_machine()
    return int(machine.run(input_value))
