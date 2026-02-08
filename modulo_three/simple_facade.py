"""Simple public facade for modulo-three computation."""

from __future__ import annotations

from modulo_three.builder import BinaryModFiniteMachineBuilder


def modThree(input: str) -> int:
    builder = BinaryModFiniteMachineBuilder()
    machine = builder.build(3)
    return machine.run(input)
