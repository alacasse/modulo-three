"""Tests for the finite-machine builder base abstraction."""

from __future__ import annotations

import unittest

from modulo_three.builder import FiniteMachineBuilder
from modulo_three.machine import FiniteMachine


class MissingBuildBuilder(FiniteMachineBuilder):
    pass


class DummyBuilder(FiniteMachineBuilder):
    def build(self) -> FiniteMachine[int, str]:
        return FiniteMachine(
            Q={0},
            Sigma={"a"},
            q0=0,
            F={0},
            delta={(0, "a"): 0},
        )


class FiniteMachineBuilderBaseTests(unittest.TestCase):
    def test_base_builder_is_abstract(self) -> None:
        with self.assertRaises(TypeError):
            FiniteMachineBuilder()

    def test_concrete_builder_must_implement_build(self) -> None:
        with self.assertRaises(TypeError):
            MissingBuildBuilder()

    def test_concrete_builder_can_construct_finite_machine(self) -> None:
        builder = DummyBuilder()
        machine = builder.build()
        self.assertIsInstance(machine, FiniteMachine)


if __name__ == "__main__":
    unittest.main()
