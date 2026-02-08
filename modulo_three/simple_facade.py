"""Simple public facade for modulo-three computation."""

from __future__ import annotations

from modulo_three.builder import BinaryModFiniteMachineBuilder


def _require_str(input_value: object) -> str:
    if not isinstance(input_value, str):
        raise TypeError("input must be str")
    return input_value


def modThree(input: str) -> int:
    input_value = _require_str(input)
    builder = BinaryModFiniteMachineBuilder()
    machine = builder.build(3)
    return int(machine.run(input_value))
