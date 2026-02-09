"""Tests for generic deterministic table-based machine builder."""

from __future__ import annotations

from enum import Enum, auto

from modulo_three.builder import (
    DeterministicMachineSpec,
    DeterministicTableMachineBuilder,
)


class Phase(Enum):
    START = auto()
    MID = auto()
    END = auto()


def test_table_builder_supports_non_modulo_state_and_symbol_types() -> None:
    builder: DeterministicTableMachineBuilder[Phase, int] = DeterministicTableMachineBuilder()
    spec = DeterministicMachineSpec(
        Q={Phase.START, Phase.MID, Phase.END},
        Sigma={0, 1},
        q0=Phase.START,
        F={Phase.END},
        delta={
            (Phase.START, 1): Phase.MID,
            (Phase.MID, 0): Phase.END,
        },
    )

    machine = builder.from_spec(spec)

    assert machine.q0 == Phase.START
    assert machine.run([1, 0]) == Phase.END


def test_table_builder_copies_input_collections() -> None:
    states = {"A", "B"}
    symbols = {"x"}
    accepting_states = {"B"}
    transitions = {("A", "x"): "B"}

    builder: DeterministicTableMachineBuilder[str, str] = DeterministicTableMachineBuilder()
    machine = builder.from_spec(
        DeterministicMachineSpec(
            Q=states,
            Sigma=symbols,
            q0="A",
            F=accepting_states,
            delta=transitions,
        )
    )

    states.add("C")
    symbols.add("y")
    accepting_states.add("C")
    transitions[("B", "x")] = "A"

    assert machine.Q == {"A", "B"}
    assert machine.Sigma == {"x"}
    assert machine.F == {"B"}
    assert dict(machine.delta) == {("A", "x"): "B"}
