#!/usr/bin/env python3
"""
Download the latest chaindata-v9.json from the TalismanSociety/chaindata repository.
"""

import argparse
import json
import os
import urllib.request
from pathlib import Path

parser = argparse.ArgumentParser(
    description="Download chaindata.json for a given version from upstream"
)
parser.add_argument("version", help="Chaindata version to fetch, e.g. v11")
args = parser.parse_args()

version = args.version
URL = f"https://raw.githubusercontent.com/TalismanSociety/chaindata/main/pub/{version}/chaindata.json"
OUT = Path("chaindata") / version / "chaindata.json"

print(f"Fetching {URL} ...")
with urllib.request.urlopen(URL) as resp:
    data = resp.read()

# Validate that we got valid JSON
parsed = json.loads(data)

OUT.parent.mkdir(parents=True, exist_ok=True)
with OUT.open("w", encoding="utf-8") as f:
    json.dump(parsed, f, indent=2)

size_mb = len(data) / (1024 * 1024)
print(f"Saved {OUT} ({size_mb:.1f} MB)")
