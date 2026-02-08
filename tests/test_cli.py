"""Tests for CLI wiring to modThree."""

from __future__ import annotations

import subprocess
import sys


def _run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "modulo_three", *args],
        check=False,
        capture_output=True,
        text=True,
    )


def test_cli_happy_path_prints_remainder() -> None:
    result = _run_cli("1011")

    assert result.returncode == 0
    assert result.stdout.strip() == "2"
    assert result.stderr == ""


def test_cli_invalid_binary_input_returns_error() -> None:
    result = _run_cli("1021")

    assert result.returncode == 1
    assert result.stdout == ""
    assert "invalid symbol" in result.stderr


def test_cli_missing_input_exits_with_usage_error() -> None:
    result = _run_cli()

    assert result.returncode == 2
    assert result.stdout == ""
    assert "usage:" in result.stderr.lower()
