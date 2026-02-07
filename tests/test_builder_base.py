"""Tests for the finite-machine builder base abstraction."""

from __future__ import annotations

from typing import Any, cast

import pytest
from modulo_three.builder import FiniteMachineBuilder
from modulo_three.machine import FiniteMachine


class MissingBuildBuilder(FiniteMachineBuilder[int, str]):
    pass


class DummyBuilder(FiniteMachineBuilder[int, str]):
    def build(self, mod: int) -> FiniteMachine[int, str]:
        return FiniteMachine(
            Q={0},
            Sigma={"a"},
            q0=0,
            F={0},
            delta={(0, "a"): 0},
        )


def test_base_builder_is_abstract() -> None:
    builder_cls = cast(Any, FiniteMachineBuilder[int, str])
    with pytest.raises(TypeError):
        builder_cls()


def test_concrete_builder_must_implement_build() -> None:
    missing_builder_cls = cast(Any, MissingBuildBuilder)
    with pytest.raises(TypeError):
        missing_builder_cls()


def test_concrete_builder_can_construct_finite_machine() -> None:
    builder = DummyBuilder()
    machine = builder.build(1)
    assert isinstance(machine, FiniteMachine)
