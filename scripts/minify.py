#!/usr/bin/env python3
"""Minify chaindata-v9-slim.json → chaindata-v9-slim.min.json (no whitespace)."""

import json, os

INPUT  = 'chaindata/chaindata-v9-slim.json'
OUTPUT = 'chaindata/chaindata-v9-slim.min.json'

with open(INPUT) as f:
    data = json.load(f)

with open(OUTPUT, 'w') as f:
    json.dump(data, f, ensure_ascii=False, separators=(',', ':'))

orig = os.path.getsize(INPUT)
mini = os.path.getsize(OUTPUT)
print(f"{orig/1024/1024:.2f} MB -> {mini/1024/1024:.2f} MB ({(1-mini/orig)*100:.0f}% smaller)")
