#!/usr/bin/env python3
"""Add missing networks and their native tokens to chaindata-v9-slim.json."""

import json
import sys
import copy

def main():
    with open('chaindata/chaindata-v9.json') as f:
        full = json.load(f)
    with open('chaindata/chaindata-v9-slim.json') as f:
        slim = json.load(f)

    # Build indices
    full_networks = {n['id']: n for n in full['networks']}
    slim_network_ids = {n['id'] for n in slim['networks']}
    slim_token_ids = {t['id'] for t in slim['tokens']}

    # Find tokens for each network in full chaindata
    full_tokens_by_network = {}
    for t in full['tokens']:
        tid = t['id']
        # Token IDs start with "networkId:"
        parts = tid.split(':')
        if len(parts) >= 2:
            nid = parts[0]
            full_tokens_by_network.setdefault(nid, []).append(t)

    # Chain IDs to add (found in full chaindata but not in slim)
    chains_to_add = ['81457', '999', '5234', '9745', '1408']

    # Report what we find
    added_networks = []
    added_tokens = []
    not_found = []

    for cid in chains_to_add:
        network = full_networks.get(cid)
        if not network:
            not_found.append(cid)
            continue

        if cid in slim_network_ids:
            print(f"SKIP: {cid} ({network['name']}) already in slim")
            continue

        # Copy network and set isDefault to false
        net_copy = copy.deepcopy(network)
        net_copy['isDefault'] = False
        added_networks.append(net_copy)

        # Find native token
        chain_tokens = full_tokens_by_network.get(cid, [])
        native_tokens = [t for t in chain_tokens if t['type'] in ['substrate-native', 'evm-native']]

        if native_tokens:
            for t in native_tokens:
                tok_copy = copy.deepcopy(t)
                tok_copy['isDefault'] = True
                added_tokens.append(tok_copy)
                print(f"ADD: {cid} ({network['name']}) + native token {tok_copy['id']}")
        else:
            # No separate token object - create from nativeCurrency
            nc = network.get('nativeCurrency', {})
            native_token_id = network.get('nativeTokenId', f"{cid}:evm-native")
            token = {
                "id": native_token_id,
                "platform": network.get('platform', 'ethereum'),
                "networkId": cid,
                "type": "evm-native",
                "symbol": nc.get('symbol', ''),
                "decimals": nc.get('decimals', 18),
                "name": nc.get('name', network['name']),
                "isDefault": True,
            }
            if nc.get('coingeckoId'):
                token['coingeckoId'] = nc['coingeckoId']
            if nc.get('logo'):
                token['logo'] = nc['logo']
            added_tokens.append(token)
            print(f"ADD: {cid} ({network['name']}) + created native token {native_token_id}")

    # Also check the 3 substrate chains NOT in full chaindata
    substrate_missing = [
        {'genesis': '0x8b404e7ed8789d813982b9cb4c8b664c05b3fbf433309f603af014ec9ce56a8c', 'name': 'Crust Mainnet'},
        {'genesis': '0x9226d527cd7fb37ea0f466e06182c3c5f330f3f522799cb8cc17e0a080b49a2d', 'name': 'Gen6 Public Chain'},
        {'genesis': '0x3920bcb4960a1eef5580cd5367ff3f430eef052774f78468852f7b9cb39f8a3c', 'name': 'Polkadex'},
    ]

    for entry in substrate_missing:
        # Try to find by genesis hash
        found = False
        for n in full['networks']:
            gh = n.get('genesisHash', '')
            if gh.lower() == entry['genesis'].lower():
                found = True
                if n['id'] not in slim_network_ids:
                    net_copy = copy.deepcopy(n)
                    net_copy['isDefault'] = False
                    added_networks.append(net_copy)

                    chain_tokens = full_tokens_by_network.get(n['id'], [])
                    native_tokens = [t for t in chain_tokens if t['type'] in ['substrate-native', 'evm-native']]
                    for t in native_tokens:
                        tok_copy = copy.deepcopy(t)
                        tok_copy['isDefault'] = True
                        added_tokens.append(tok_copy)
                    print(f"ADD: {n['id']} ({n['name']}) from genesis match + {len(native_tokens)} native tokens")
                else:
                    print(f"SKIP: {n['id']} ({n['name']}) already in slim")
                break
        if not found:
            not_found.append(f"{entry['name']} (genesis: {entry['genesis'][:20]}...)")

    # Add to slim
    slim['networks'].extend(added_networks)
    slim['tokens'].extend(added_tokens)

    # Write output
    with open('chaindata/chaindata-v9-slim.json', 'w') as f:
        json.dump(slim, f, indent=2, ensure_ascii=False)
        f.write('\n')

    print(f"\n=== SUMMARY ===")
    print(f"Added {len(added_networks)} networks")
    print(f"Added {len(added_tokens)} tokens")
    print(f"Not found in chaindata-v9.json: {len(not_found)}")
    for nf in not_found:
        print(f"  - {nf}")

    # Print details of what was added
    print(f"\n=== ADDED NETWORKS ===")
    for n in added_networks:
        print(f"  {n['id']}: {n['name']} (isDefault={n['isDefault']})")

    print(f"\n=== ADDED TOKENS ===")
    for t in added_tokens:
        print(f"  {t['id']}: {t['symbol']} (isDefault={t['isDefault']})")

if __name__ == '__main__':
    main()
