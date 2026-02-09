"""Tests for DeterministicMachineSpec behavior and validation pathways."""

from __future__ import annotations

import pytest
from modulo_three.builder import DeterministicMachineSpec, DeterministicTableMachineBuilder


@pytest.fixture
def table_builder() -> DeterministicTableMachineBuilder[int, str]:
    return DeterministicTableMachineBuilder()


def test_spec_happy_path_stores_minimal_fields_as_provided() -> None:
    states = {0}
    symbols = {"a"}
    accepting_states = {0}
    transitions = {(0, "a"): 0}

    spec = DeterministicMachineSpec(
        Q=states,
        Sigma=symbols,
        q0=0,
        F=accepting_states,
        delta=transitions,
    )

    assert spec.Q == {0}
    assert spec.Sigma == {"a"}
    assert spec.q0 == 0
    assert spec.F == {0}
    assert dict(spec.delta) == {(0, "a"): 0}


def test_spec_is_lightweight_and_keeps_collection_references() -> None:
    states = {0}
    symbols = {"a"}
    accepting_states = {0}
    transitions = {(0, "a"): 0}

    spec = DeterministicMachineSpec(
        Q=states,
        Sigma=symbols,
        q0=0,
        F=accepting_states,
        delta=transitions,
    )

    assert spec.Q is states
    assert spec.Sigma is symbols
    assert spec.F is accepting_states
    assert spec.delta is transitions


def test_builder_rejects_spec_when_q0_is_not_in_Q(
    table_builder: DeterministicTableMachineBuilder[int, str],
) -> None:
    spec = DeterministicMachineSpec(
        Q={1},
        Sigma={"a"},
        q0=0,
        F={1},
        delta={(1, "a"): 1},
    )

    with pytest.raises(ValueError, match=r"q0 must be a member of Q"):
        table_builder.from_spec(spec)


def test_builder_rejects_spec_when_accepting_states_are_not_subset_of_Q(
    table_builder: DeterministicTableMachineBuilder[int, str],
) -> None:
    spec = DeterministicMachineSpec(
        Q={0, 1},
        Sigma={"a"},
        q0=0,
        F={2},
        delta={(0, "a"): 1, (1, "a"): 0},
    )

    with pytest.raises(ValueError, match=r"F must be a subset of Q"):
        table_builder.from_spec(spec)


def test_builder_rejects_spec_when_delta_uses_symbol_outside_sigma(
    table_builder: DeterministicTableMachineBuilder[int, str],
) -> None:
    spec = DeterministicMachineSpec(
        Q={0},
        Sigma={"a"},
        q0=0,
        F={0},
        delta={(0, "b"): 0},
    )

    with pytest.raises(ValueError, match=r"delta key symbol must be in Sigma"):
        table_builder.from_spec(spec)


def test_builder_rejects_spec_when_delta_is_not_total(
    table_builder: DeterministicTableMachineBuilder[int, str],
) -> None:
    spec = DeterministicMachineSpec(
        Q={0, 1},
        Sigma={"a"},
        q0=0,
        F={0, 1},
        delta={(0, "a"): 1},
    )

    with pytest.raises(ValueError, match=r"delta must be total over QxSigma: expected=2, actual=1"):
        table_builder.from_spec(spec)
