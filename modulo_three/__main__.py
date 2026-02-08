"""CLI entrypoint for modulo_three."""

from __future__ import annotations

import argparse
import sys

from modulo_three import modThree


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="modulo_three")
    parser.add_argument("input_value", nargs="?", help="Binary input string (MSB first)")
    parser.add_argument(
        "-i",
        "--interactive",
        action="store_true",
        help="Run in interactive mode",
    )
    return parser


def _interactive_mode() -> int:
    prompt = "Enter binary number (or 'exit' to quit): "
    while True:
        try:
            raw_value = input(prompt)
        except EOFError:
            return 0
        input_value = raw_value.strip()
        if input_value.lower() in {"exit", "quit", "q"}:
            return 0
        try:
            result = modThree(input_value)
        except (TypeError, ValueError) as exc:
            print(str(exc), file=sys.stderr)
            continue
        print(result)


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    if args.interactive:
        return _interactive_mode()
    if args.input_value is None:
        parser.error("the following arguments are required: input_value")
    try:
        result = modThree(args.input_value)
    except (TypeError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
