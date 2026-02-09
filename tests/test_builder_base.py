"""Tests for the finite-machine builder base abstraction."""

from __future__ import annotations

from typing import Any, cast

import pytest
from modulo_three.builder import DeterministicMachineSpec, MachineBuilder
from modulo_three.machine import FiniteMachine


class MissingSpecBuilder(MachineBuilder[int, str]):
    pass


class DummyBuilder(MachineBuilder[int, str]):
    def from_spec(self, spec: DeterministicMachineSpec[int, str]) -> FiniteMachine[int, str]:
        return FiniteMachine(
            Q=set(spec.Q),
            Sigma=set(spec.Sigma),
            q0=spec.q0,
            F=set(spec.F),
            delta=dict(spec.delta),
        )


def test_base_builder_is_abstract() -> None:
    builder_cls = cast(Any, MachineBuilder[int, str])
    with pytest.raises(TypeError):
        builder_cls()


def test_concrete_builder_must_implement_from_spec() -> None:
    missing_builder_cls = cast(Any, MissingSpecBuilder)
    with pytest.raises(TypeError):
        missing_builder_cls()


def test_concrete_builder_can_construct_finite_machine() -> None:
    builder = DummyBuilder()
    spec = DeterministicMachineSpec(
        Q={0},
        Sigma={"a"},
        q0=0,
        F={0},
        delta={(0, "a"): 0},
    )
    machine = builder.from_spec(spec)
    assert isinstance(machine, FiniteMachine)


def test_spec_is_mutable() -> None:
    spec = DeterministicMachineSpec(
        Q={0, 1},
        Sigma={"a"},
        q0=0,
        F={1},
        delta={(0, "a"): 1, (1, "a"): 1},
    )

    spec.q0 = 1
    spec.F.add(0)
    spec.delta[(1, "a")] = 0

    assert spec.q0 == 1
    assert spec.F == {0, 1}
    assert spec.delta[(1, "a")] == 0
