"""Tests for the finite-machine 5-tuple data model."""

from __future__ import annotations

import unittest

from modulo_three.machine import FiniteMachine


class FiniteMachineModelTests(unittest.TestCase):
    def test_fields_exist_and_are_readable(self) -> None:
        states = {0, 1, 2}
        alphabet = {"a", "b"}
        start_state = 0
        accepting_states = {0, 2}
        transitions = {
            (0, "a"): 1,
            (1, "b"): 2,
        }

        machine = FiniteMachine(
            Q=states,
            Sigma=alphabet,
            q0=start_state,
            F=accepting_states,
            delta=transitions,
        )

        self.assertEqual(states, machine.Q)
        self.assertEqual(alphabet, machine.Sigma)
        self.assertEqual(start_state, machine.q0)
        self.assertEqual(accepting_states, machine.F)
        self.assertEqual(transitions, machine.delta)


if __name__ == "__main__":
    unittest.main()
