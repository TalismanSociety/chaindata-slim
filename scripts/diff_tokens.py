#!/usr/bin/env python3
"""Compare tokens between the pre-branch and post-branch slim files to find removals."""
import json
import subprocess

# Get the slim file at the commit before the branch (3528060)
before = subprocess.run(
    ['git', 'show', '3528060:chaindata/chaindata-v9-slim.json'],
    capture_output=True, text=True
)
# Get the slim file at the branch tip (4ab8a4b)
after = subprocess.run(
    ['git', 'show', '4ab8a4b:chaindata/chaindata-v9-slim.json'],
    capture_output=True, text=True
)

before_data = json.loads(before.stdout)
after_data = json.loads(after.stdout)

before_tokens = {t['id']: t for t in before_data['tokens']}
after_tokens = {t['id']: t for t in after_data['tokens']}

before_networks = {n['id']: n for n in before_data['networks']}
after_networks = {n['id']: n for n in after_data['networks']}

removed_tokens = set(before_tokens.keys()) - set(after_tokens.keys())
added_tokens = set(after_tokens.keys()) - set(before_tokens.keys())
removed_networks = set(before_networks.keys()) - set(after_networks.keys())
added_networks = set(after_networks.keys()) - set(before_networks.keys())

print(f"=== NETWORKS ===")
print(f"Before: {len(before_networks)}, After: {len(after_networks)}")
print(f"Added: {len(added_networks)}, Removed: {len(removed_networks)}")
if removed_networks:
    print(f"\nRemoved networks:")
    for nid in sorted(removed_networks):
        n = before_networks[nid]
        print(f"  {nid} ({n.get('name', '?')})")
if added_networks:
    print(f"\nAdded networks:")
    for nid in sorted(added_networks):
        n = after_networks[nid]
        print(f"  {nid} ({n.get('name', '?')})")

print(f"\n=== TOKENS ===")
print(f"Before: {len(before_tokens)}, After: {len(after_tokens)}")
print(f"Added: {len(added_tokens)}, Removed: {len(removed_tokens)}")

if removed_tokens:
    print(f"\nRemoved tokens ({len(removed_tokens)}):")
    for tid in sorted(removed_tokens):
        t = before_tokens[tid]
        print(f"  {tid} ({t.get('symbol', '?')}) type={t.get('type', '?')}")

if added_tokens:
    print(f"\nAdded tokens ({len(added_tokens)}):")
    for tid in sorted(added_tokens):
        t = after_tokens[tid]
        print(f"  {tid} ({t.get('symbol', '?')}) type={t.get('type', '?')}")

# Check if removed tokens were re-added (i.e. same content, different position)
print(f"\n=== ANALYSIS ===")
if removed_tokens:
    in_after = removed_tokens & set(after_tokens.keys())
    truly_removed = removed_tokens - set(after_tokens.keys())
    print(f"Truly removed (not re-added): {len(truly_removed)}")
    for tid in sorted(truly_removed):
        t = before_tokens[tid]
        net = tid.split(':')[0]
        net_still_exists = net in after_networks
        print(f"  {tid} ({t.get('symbol', '?')}) — network '{net}' {'still in slim' if net_still_exists else 'ALSO REMOVED'}")
