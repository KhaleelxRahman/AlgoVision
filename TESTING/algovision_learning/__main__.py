"""Export the learning catalog as JSON.

Usage (run from the ``python/`` directory)::

    python -m algovision_learning                      # print JSON to stdout
    python -m algovision_learning --output data/algovision_learning.json
    python -m algovision_learning --check data/algovision_learning.json

``--check`` exits with status 1 if the file is missing or out of date.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .metadata import catalog_to_json


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="python -m algovision_learning", description=__doc__.splitlines()[0])
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--output", type=Path, help="write the JSON catalog to this file")
    group.add_argument("--check", type=Path, help="verify this JSON file is up to date")
    args = parser.parse_args(argv)

    text = catalog_to_json()
    if args.check is not None:
        if not args.check.is_file() or args.check.read_text(encoding="utf-8") != text:
            print(f"{args.check} is missing or out of date; regenerate with --output.", file=sys.stderr)
            return 1
        print(f"{args.check} is up to date.")
        return 0
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
        print(f"Wrote {args.output}")
        return 0
    sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
