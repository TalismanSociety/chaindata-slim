#!/usr/bin/env python3
"""Minify chaindata-slim.json -> chaindata-slim.min.json (no whitespace)."""

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Minify chaindata-slim.json into chaindata-slim.min.json"
    )
    parser.add_argument("version", help="Chaindata version, e.g. v11")
    args = parser.parse_args()

    folder = Path("chaindata") / args.version
    input_path = folder / "chaindata-slim.json"
    output_path = folder / "chaindata-slim.min.json"

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    with input_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))

    orig = input_path.stat().st_size
    mini = output_path.stat().st_size
    reduction = (1 - mini / orig) * 100 if orig else 0
    print(
        f"{input_path} -> {output_path}: "
        f"{orig / 1024 / 1024:.2f} MB -> {mini / 1024 / 1024:.2f} MB "
        f"({reduction:.0f}% smaller)"
    )


main()
