#!/usr/bin/env python3
"""
Strip blacklisted RPC endpoints from chaindata-v9-slim.json.

Some upstream RPC URLs embed third-party API keys (e.g. OnFinality) or are
otherwise undesirable for a public wallet bundle. This script removes any RPC
whose URL starts with one of the prefixes in RPC_BLACKLIST_PREFIXES.

Runs as the final stage before minification so the strip survives a full
pipeline re-run from upstream chaindata.
"""

import json
import sys

INPUT = 'chaindata/chaindata-v9-slim.json'
OUTPUT = 'chaindata/chaindata-v9-slim.json'

# Match by URL prefix so query-string variants (e.g. ?apikey=...) are also caught.
RPC_BLACKLIST_PREFIXES = (
    'wss://bittensor-finney.api.onfinality.io',
)


def is_blacklisted(url: str) -> bool:
    return isinstance(url, str) and url.startswith(RPC_BLACKLIST_PREFIXES)


def strip_rpcs(networks):
    removed = 0
    for net in networks:
        rpcs = net.get('rpcs')
        if not isinstance(rpcs, list):
            continue
        filtered = [r for r in rpcs if not is_blacklisted(r)]
        dropped = len(rpcs) - len(filtered)
        if dropped:
            removed += dropped
            net['rpcs'] = filtered
            print(f"  - {net.get('id', '?')}: removed {dropped} blacklisted rpc(s)")
    return removed


def main():
    with open(INPUT) as f:
        data = json.load(f)

    networks = data.get('networks', [])
    removed = strip_rpcs(networks)

    with open(OUTPUT, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write('\n')

    print(f"Stripped {removed} blacklisted RPC URL(s) from {len(networks)} networks.")
    return 0


if __name__ == '__main__':
    sys.exit(main())
