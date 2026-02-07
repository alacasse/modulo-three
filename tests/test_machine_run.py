"""Tests for finite-machine run-loop behavior."""

from __future__ import annotations

import unittest

from modulo_three.machine import FiniteMachine


class FiniteMachineRunTests(unittest.TestCase):
    def test_empty_input_returns_start_state(self) -> None:
        machine = FiniteMachine(
            Q={0, 1, 2},
            Sigma={"a", "b"},
            q0=1,
            F={0, 1, 2},
            delta={},
        )

        self.assertEqual(1, machine.run(""))

    def test_simple_deterministic_trace_returns_final_state(self) -> None:
        machine = FiniteMachine(
            Q={0, 1, 2},
            Sigma={"a", "b"},
            q0=0,
            F={0, 1, 2},
            delta={
                (0, "a"): 1,
                (1, "b"): 2,
            },
        )

        self.assertEqual(2, machine.run("ab"))


if __name__ == "__main__":
    unittest.main()
