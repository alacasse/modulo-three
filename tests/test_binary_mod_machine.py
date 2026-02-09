"""Tests for binary modulo-machine construction and transition coverage."""

from __future__ import annotations

from modulo_three.machine import FiniteMachine


def test_mod_three_builds_exact_transition_graph(
    mod_three_machine: FiniteMachine[int, str],
) -> None:
    machine = mod_three_machine
    assert machine.Q == {0, 1, 2}
    assert machine.Sigma == {"0", "1"}
    assert machine.q0 == 0
    assert machine.F == {0, 1, 2}
    assert dict(machine.delta) == {
        (0, "0"): 0,
        (0, "1"): 1,
        (1, "0"): 2,
        (1, "1"): 0,
        (2, "0"): 1,
        (2, "1"): 2,
    }


def test_transition_graph_is_total_for_every_state_symbol_pair(
    mod_three_machine: FiniteMachine[int, str],
) -> None:
    machine = mod_three_machine
    for state in machine.Q:
        for symbol in machine.Sigma:
            assert (state, symbol) in machine.delta

    assert len(machine.delta) == len(machine.Q) * len(machine.Sigma)
