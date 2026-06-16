#!/usr/bin/env python3
"""Run the full slim pipeline for a given chaindata version.

Usage:
    python3 scripts/pipeline.py <version>

Example:
    python3 scripts/pipeline.py v11

Stages (run in order):
    0. fetch_chaindata — download chaindata.json from upstream
    1. slim_filter     — filter networks/tokens
    2. slim_tokens     — reduce to max 1 000 tokens
    3. fix_defaults    — curate isDefault flags
    4. strip_rpcs      — remove blacklisted RPC endpoints
    5. minify          — write chaindata.min.json
"""

import argparse
import sys
from pathlib import Path

# Import each stage's main() directly so we don't shell out to subprocesses.
# We temporarily patch sys.argv before each call so argparse inside each
# module receives the folder argument.

import importlib
import importlib.util


def run_stage(module_name: str, version: str) -> None:
    """Import and run a pipeline stage module with the version argument."""
    scripts_dir = Path(__file__).parent
    spec = importlib.util.spec_from_file_location(module_name, scripts_dir / f"{module_name}.py")
    mod = importlib.util.module_from_spec(spec)
    old_argv = sys.argv
    sys.argv = [f"{module_name}.py", version]
    try:
        spec.loader.exec_module(mod)
    finally:
        sys.argv = old_argv


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run the full slim pipeline for a chaindata version"
    )
    parser.add_argument("version", help="Chaindata version, e.g. v11")
    args = parser.parse_args()

    version = args.version

    stages = [
        "fetch_chaindata",
        "slim_filter",
        "slim_tokens",
        "fix_defaults",
        "strip_rpcs",
        "minify",
    ]

    for stage in stages:
        print(f"\n{'='*60}")
        print(f"Stage: {stage}")
        print(f"{'='*60}")
        run_stage(stage, version)

    print(f"\nPipeline complete. Output: chaindata/{version}/chaindata-slim.min.json")


if __name__ == "__main__":
    main()
