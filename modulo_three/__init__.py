"""Streaming modulo computation via finite-state machine."""

from modulo_three.builder import DeterministicMachineSpec, DeterministicTableMachineBuilder
from modulo_three.machine import FiniteMachine
from modulo_three.simple_facade import modThree

__all__ = [
    "modThree",
    "FiniteMachine",
    "DeterministicMachineSpec",
    "DeterministicTableMachineBuilder",
]
