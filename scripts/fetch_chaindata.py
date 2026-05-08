#!/usr/bin/env python3
"""
Download the latest chaindata-v9.json from the TalismanSociety/chaindata repository.
"""

import json
import os
import urllib.request

URL = "https://raw.githubusercontent.com/TalismanSociety/chaindata/main/pub/v9/chaindata.json"
OUT = "chaindata/chaindata-v9.json"

print(f"Fetching {URL} ...")
with urllib.request.urlopen(URL) as resp:
    data = resp.read()

# Validate that we got valid JSON
parsed = json.loads(data)

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w") as f:
    json.dump(parsed, f, indent=2)

size_mb = len(data) / (1024 * 1024)
print(f"Saved {OUT} ({size_mb:.1f} MB)")
