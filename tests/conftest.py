"""Shared pytest fixtures for the test suite."""

from __future__ import annotations

import subprocess
import sys
from collections.abc import Callable, Mapping
from typing import Any

import pytest
from modulo_three.builder import build_binary_mod_machine
from modulo_three.machine import FiniteMachine

MachineFactory = Callable[
    [set[Any], set[Any], Any, set[Any], Mapping[tuple[Any, Any], Any]],
    FiniteMachine[Any, Any],
]
CliRunner = Callable[..., subprocess.CompletedProcess[str]]


@pytest.fixture
def machine_factory() -> MachineFactory:
    """Build finite machines for tests with explicit 5-tuple inputs."""

    def _build(
        Q: set[Any],
        Sigma: set[Any],
        q0: Any,
        F: set[Any],
        delta: Mapping[tuple[Any, Any], Any],
    ) -> FiniteMachine[Any, Any]:
        return FiniteMachine(Q=Q, Sigma=Sigma, q0=q0, F=F, delta=delta)

    return _build


@pytest.fixture
def ab_step_machine(machine_factory: MachineFactory) -> FiniteMachine[int, str]:
    """Two-state machine used by step/run validation tests."""
    return machine_factory(
        {0, 1},
        {"a", "b"},
        0,
        {0, 1},
        {
            (0, "a"): 1,
            (0, "b"): 0,
            (1, "a"): 1,
            (1, "b"): 0,
        },
    )


@pytest.fixture
def mod_three_machine() -> FiniteMachine[int, str]:
    """Machine implementing binary modulo 3 transitions."""
    return build_binary_mod_machine(3)


@pytest.fixture
def cli_runner() -> CliRunner:
    """Run the package CLI as a subprocess with optional stdin."""

    def _run(*args: str, input_text: str | None = None) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "-m", "modulo_three", *args],
            check=False,
            capture_output=True,
            text=True,
            input=input_text,
        )

    return _run
