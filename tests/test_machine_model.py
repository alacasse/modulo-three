"""Tests for the finite-machine 5-tuple data model."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any, TypedDict, cast

import pytest
from modulo_three.machine import FiniteMachine

from tests._machine_assertions import assert_machine_definition

type MachineFactory = Callable[
    [set[Any], set[Any], Any, set[Any], Mapping[tuple[Any, Any], Any]],
    FiniteMachine[Any, Any],
]


class IntStrMachineArgs(TypedDict):
    Q: set[int]
    Sigma: set[str]
    q0: int
    F: set[int]
    delta: dict[tuple[int, str], int]


@pytest.fixture
def valid_machine_args() -> IntStrMachineArgs:
    return {
        "Q": {0, 1, 2},
        "Sigma": {"a", "b"},
        "q0": 0,
        "F": {0, 2},
        "delta": {
            (0, "a"): 1,
            (0, "b"): 0,
            (1, "a"): 2,
            (1, "b"): 2,
            (2, "a"): 0,
            (2, "b"): 1,
        },
    }


@pytest.fixture
def valid_machine(
    machine_factory: MachineFactory,
    valid_machine_args: IntStrMachineArgs,
) -> FiniteMachine[int, str]:
    return cast(
        FiniteMachine[int, str],
        machine_factory(
            valid_machine_args["Q"],
            valid_machine_args["Sigma"],
            valid_machine_args["q0"],
            valid_machine_args["F"],
            valid_machine_args["delta"],
        ),
    )


def _copy_machine_args(args: IntStrMachineArgs) -> IntStrMachineArgs:
    return {
        "Q": set(args["Q"]),
        "Sigma": set(args["Sigma"]),
        "q0": args["q0"],
        "F": set(args["F"]),
        "delta": dict(args["delta"]),
    }


def test_fields_exist_and_are_readable(
    valid_machine: FiniteMachine[int, str],
    valid_machine_args: IntStrMachineArgs,
) -> None:
    assert_machine_definition(
        valid_machine,
        Q=valid_machine_args["Q"],
        Sigma=valid_machine_args["Sigma"],
        q0=valid_machine_args["q0"],
        F=valid_machine_args["F"],
        delta=valid_machine_args["delta"],
    )


def test_init_copies_input_collections(
    machine_factory: MachineFactory,
    valid_machine_args: IntStrMachineArgs,
) -> None:
    args = _copy_machine_args(valid_machine_args)
    machine = machine_factory(
        args["Q"],
        args["Sigma"],
        args["q0"],
        args["F"],
        args["delta"],
    )

    args["Q"].add(3)
    args["Sigma"].add("c")
    args["F"].add(3)
    args["delta"][(0, "c")] = 0

    assert_machine_definition(
        machine,
        Q={0, 1, 2},
        Sigma={"a", "b"},
        q0=0,
        F={0, 2},
        delta={
            (0, "a"): 1,
            (0, "b"): 0,
            (1, "a"): 2,
            (1, "b"): 2,
            (2, "a"): 0,
            (2, "b"): 1,
        },
    )


INVALID_DEFINITION_CASES: list[tuple[dict[str, Any], str]] = [
    (
        {"Q": {1, 2}, "q0": 0},
        r"q0 must be a member of Q",
    ),
    (
        {"Q": {0, 1}, "Sigma": {"a"}, "F": {0, 2}},
        r"F must be a subset of Q",
    ),
    (
        {"Q": {0, 1}, "Sigma": {"a"}, "F": {1}, "delta": {(2, "a"): 1}},
        r"delta key state must be in Q",
    ),
    (
        {"Q": {0, 1}, "Sigma": {"a"}, "F": {1}, "delta": {(0, "b"): 1}},
        r"delta key symbol must be in Sigma",
    ),
    (
        {"Q": {0, 1}, "Sigma": {"a"}, "F": {1}, "delta": {(0, "a"): 2}},
        r"delta value must be in Q",
    ),
    (
        {
            "Q": set[int](),
            "Sigma": {"a"},
            "q0": 0,
            "F": set[int](),
            "delta": dict[tuple[int, str], int](),
        },
        r"Q must be non-empty",
    ),
    (
        {
            "Q": {0},
            "Sigma": set[str](),
            "q0": 0,
            "F": {0},
            "delta": dict[tuple[int, str], int](),
        },
        r"Sigma must be non-empty",
    ),
    (
        {
            "Q": {0, 1},
            "Sigma": {"a"},
            "q0": 0,
            "F": {0, 1},
            "delta": {(0, "a"): 0},
        },
        r"delta must be total over QxSigma: expected=2, actual=1",
    ),
]


@pytest.mark.parametrize(
    ("overrides", "match"),
    INVALID_DEFINITION_CASES,
)
def test_init_raises_for_invalid_machine_definition(
    machine_factory: MachineFactory,
    valid_machine_args: IntStrMachineArgs,
    overrides: dict[str, Any],
    match: str,
) -> None:
    args: dict[str, Any] = {**_copy_machine_args(valid_machine_args), **overrides}

    with pytest.raises(ValueError, match=match):
        machine_factory(
            cast(set[Any], args["Q"]),
            cast(set[Any], args["Sigma"]),
            args["q0"],
            cast(set[Any], args["F"]),
            cast(Mapping[tuple[Any, Any], Any], args["delta"]),
        )
