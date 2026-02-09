"""Shared assertion helpers for finite-machine tests."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from modulo_three.machine import FiniteMachine


def assert_machine_definition(
    machine: FiniteMachine[Any, Any],
    *,
    Q: set[Any],
    Sigma: set[Any],
    q0: Any,
    F: set[Any],
    delta: Mapping[tuple[Any, Any], Any],
) -> None:
    assert machine.Q == Q
    assert machine.Sigma == Sigma
    assert machine.q0 == q0
    assert machine.F == F
    assert dict(machine.delta) == dict(delta)
