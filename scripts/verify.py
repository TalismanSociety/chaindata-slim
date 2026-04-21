#!/usr/bin/env python3
"""Verify the slim chaindata was updated correctly."""
import json

with open('chaindata/chaindata-v9-slim.json') as f:
    slim = json.load(f)

print(f'Networks: {len(slim["networks"])}')
print(f'Tokens: {len(slim["tokens"])}')

for n in slim['networks']:
    if n['id'] in ['81457', '999', '5234', '9745', '1408']:
        print(f'Network: {n["id"]} ({n["name"]}) isDefault={n["isDefault"]}')

for t in slim['tokens']:
    if t['id'] in ['81457:evm-native', '999:evm-native', '5234:evm-native', '9745:evm-native', '1408:evm-native']:
        print(f'Token: {t["id"]} sym={t["symbol"]} isDefault={t["isDefault"]}')
