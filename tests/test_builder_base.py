"""Tests for the finite-machine builder base abstraction."""

from __future__ import annotations

from typing import Any, cast

import pytest
from modulo_three.builder import DeterministicMachineBuilder, DeterministicMachineSpec
from modulo_three.machine import FiniteMachine


class MissingSpecBuilder(DeterministicMachineBuilder[int, str]):
    pass


class DummyBuilder(DeterministicMachineBuilder[int, str]):
    def from_spec(self, spec: DeterministicMachineSpec[int, str]) -> FiniteMachine[int, str]:
        return FiniteMachine(
            Q=set(spec.Q),
            Sigma=set(spec.Sigma),
            q0=spec.q0,
            F=set(spec.F),
            delta=dict(spec.delta),
        )


@pytest.fixture
def singleton_spec() -> DeterministicMachineSpec[int, str]:
    return DeterministicMachineSpec(
        Q={0},
        Sigma={"a"},
        q0=0,
        F={0},
        delta={(0, "a"): 0},
    )


def test_base_builder_is_abstract() -> None:
    builder_cls = cast(Any, DeterministicMachineBuilder[int, str])
    with pytest.raises(TypeError):
        builder_cls()


def test_concrete_builder_must_implement_from_spec() -> None:
    missing_builder_cls = cast(Any, MissingSpecBuilder)
    with pytest.raises(TypeError):
        missing_builder_cls()


def test_concrete_builder_can_construct_finite_machine(
    singleton_spec: DeterministicMachineSpec[int, str],
) -> None:
    builder = DummyBuilder()
    machine = builder.from_spec(singleton_spec)
    assert isinstance(machine, FiniteMachine)
