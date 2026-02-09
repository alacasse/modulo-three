"""Tests for generic deterministic table-based machine builder."""

from __future__ import annotations

from enum import Enum, auto

import pytest
from modulo_three.builder import (
    DeterministicMachineSpec,
    DeterministicTableMachineBuilder,
)


class Phase(Enum):
    START = auto()
    MID = auto()
    END = auto()


@pytest.fixture
def phase_builder() -> DeterministicTableMachineBuilder[Phase, int]:
    return DeterministicTableMachineBuilder()


@pytest.fixture
def phase_spec() -> DeterministicMachineSpec[Phase, int]:
    return DeterministicMachineSpec(
        Q={Phase.START, Phase.MID, Phase.END},
        Sigma={0, 1},
        q0=Phase.START,
        F={Phase.END},
        delta={
            (Phase.START, 0): Phase.START,
            (Phase.START, 1): Phase.MID,
            (Phase.MID, 0): Phase.END,
            (Phase.MID, 1): Phase.MID,
            (Phase.END, 0): Phase.END,
            (Phase.END, 1): Phase.END,
        },
    )


@pytest.fixture
def string_builder() -> DeterministicTableMachineBuilder[str, str]:
    return DeterministicTableMachineBuilder()


@pytest.fixture
def string_spec_inputs() -> tuple[set[str], set[str], set[str], dict[tuple[str, str], str]]:
    return {"A", "B"}, {"x"}, {"B"}, {("A", "x"): "B", ("B", "x"): "A"}


def test_table_builder_supports_non_modulo_state_and_symbol_types(
    phase_builder: DeterministicTableMachineBuilder[Phase, int],
    phase_spec: DeterministicMachineSpec[Phase, int],
) -> None:
    machine = phase_builder.from_spec(phase_spec)

    assert machine.q0 == Phase.START
    assert machine.run([1, 0]) == Phase.END


def test_table_builder_copies_input_collections(
    string_builder: DeterministicTableMachineBuilder[str, str],
    string_spec_inputs: tuple[set[str], set[str], set[str], dict[tuple[str, str], str]],
) -> None:
    states, symbols, accepting_states, transitions = string_spec_inputs
    machine = string_builder.from_spec(
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
    transitions[("A", "y")] = "A"

    assert machine.Q == {"A", "B"}
    assert machine.Sigma == {"x"}
    assert machine.F == {"B"}
    assert dict(machine.delta) == {("A", "x"): "B", ("B", "x"): "A"}
