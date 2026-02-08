"""CLI entrypoint for modulo_three."""

from __future__ import annotations

import argparse
import sys

from modulo_three import modThree


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="modulo_three")
    parser.add_argument("input_value", help="Binary input string (MSB first)")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        result = modThree(args.input_value)
    except (TypeError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
