"""Tests for CLI wiring to modThree."""

from __future__ import annotations

import subprocess
from collections.abc import Callable

CliRunner = Callable[..., subprocess.CompletedProcess[str]]


def test_cli_happy_path_prints_remainder(
    cli_runner: CliRunner,
) -> None:
    result = cli_runner("1011")

    assert result.returncode == 0
    assert result.stdout.strip() == "2"
    assert result.stderr == ""


def test_cli_invalid_binary_input_returns_error(
    cli_runner: CliRunner,
) -> None:
    result = cli_runner("1021")

    assert result.returncode == 1
    assert result.stdout == ""
    assert "invalid symbol" in result.stderr


def test_cli_missing_input_exits_with_usage_error(
    cli_runner: CliRunner,
) -> None:
    result = cli_runner()

    assert result.returncode == 2
    assert result.stdout == ""
    assert "usage:" in result.stderr.lower()


def test_cli_interactive_accepts_binary_input_and_exit(
    cli_runner: CliRunner,
) -> None:
    result = cli_runner("--interactive", input_text="1011\nexit\n")

    assert result.returncode == 0
    assert "2" in result.stdout
    assert result.stderr == ""


def test_cli_interactive_keeps_running_after_error(
    cli_runner: CliRunner,
) -> None:
    result = cli_runner("--interactive", input_text="1021\n101\nq\n")

    assert result.returncode == 0
    assert "2" in result.stdout
    assert "invalid symbol" in result.stderr


def test_cli_interactive_rejects_empty_input(
    cli_runner: CliRunner,
) -> None:
    result = cli_runner("--interactive", input_text="\nq\n")

    assert result.returncode == 0
    assert "input must be non-empty" in result.stderr
