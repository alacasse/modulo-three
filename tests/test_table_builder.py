"""Tests for generic deterministic table-based machine builder."""

from __future__ import annotations

from enum import Enum, auto

import pytest
from modulo_three.builder import (
    DeterministicMachineSpec,
    DeterministicTableMachineBuilder,
)

from tests._machine_assertions import assert_machine_definition


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

    assert_machine_definition(
        machine,
        Q={"A", "B"},
        Sigma={"x"},
        q0="A",
        F={"B"},
        delta={("A", "x"): "B", ("B", "x"): "A"},
    )


def test_table_builder_machine_is_stable_after_spec_is_mutated_post_build(
    string_builder: DeterministicTableMachineBuilder[str, str],
) -> None:
    transitions = {("A", "x"): "B", ("B", "x"): "A"}
    spec = DeterministicMachineSpec(
        Q={"A", "B"},
        Sigma={"x"},
        q0="A",
        F={"B"},
        delta=transitions,
    )
    machine = string_builder.from_spec(spec)

    initial_states = set(machine.Q)
    initial_symbols = set(machine.Sigma)
    initial_accepting = set(machine.F)
    initial_transitions = dict(machine.delta)

    spec.Q.add("C")
    spec.Q.remove("B")
    spec.Sigma.add("y")
    spec.Sigma.remove("x")
    spec.F.clear()
    spec.F.add("A")
    transitions[("A", "x")] = "A"
    transitions[("B", "x")] = "B"
    transitions[("A", "y")] = "C"

    assert spec.Q == {"A", "C"}
    assert spec.Sigma == {"y"}
    assert spec.F == {"A"}
    assert dict(spec.delta) == {
        ("A", "x"): "A",
        ("B", "x"): "B",
        ("A", "y"): "C",
    }

    assert_machine_definition(
        machine,
        Q=initial_states,
        Sigma=initial_symbols,
        q0="A",
        F=initial_accepting,
        delta=initial_transitions,
    )
