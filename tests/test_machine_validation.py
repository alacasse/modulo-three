"""Tests for finite-machine run input validation."""

from __future__ import annotations

import unittest

from modulo_three.machine import FiniteMachine


class FiniteMachineValidationTests(unittest.TestCase):
    def _machine(self) -> FiniteMachine[int, str]:
        return FiniteMachine(
            Q={0, 1},
            Sigma={"a", "b"},
            q0=0,
            F={0, 1},
            delta={
                (0, "a"): 1,
                (1, "b"): 0,
            },
        )

    def test_run_raises_type_error_for_non_string_input(self) -> None:
        machine = self._machine()
        with self.assertRaisesRegex(TypeError, r"input must be str"):
            machine.run(123)  # type: ignore[arg-type]

    def test_run_raises_value_error_for_invalid_symbol_with_index(self) -> None:
        machine = self._machine()
        with self.assertRaisesRegex(
            ValueError,
            r"invalid symbol at index 1: 'z'",
        ):
            machine.run("az")


if __name__ == "__main__":
    unittest.main()
