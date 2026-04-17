import json

with open('chaindata/chaindata-v9.json') as f:
    data = json.load(f)

networks = data.get('networks', [])
tokens = data.get('tokens', [])
mainnets = [n for n in networks if not n.get('isTestnet')]

# Write mainnet names to a file for analysis
with open('/tmp/mainnet_names.txt', 'w') as f:
    for n in mainnets:
        f.write(f"{n.get('name','?')}\n")

# Write unique coingecko IDs to a file
cg_ids = sorted(set(t.get('coingeckoId') for t in tokens if t.get('coingeckoId')))
with open('/tmp/token_cgids.txt', 'w') as f:
    for cid in cg_ids:
        f.write(f"{cid}\n")

# Write a condensed summary for analysis
with open('/tmp/chaindata_condensed.txt', 'w') as f:
    f.write(f"MAINNETS: {len(mainnets)}\n")
    f.write(f"TOKENS: {len(tokens)}\n")
    f.write(f"UNIQUE_COINGECKO_IDS: {len(cg_ids)}\n\n")
    
    # Group mainnets by rough category
    # Known major chains
    major_evm = ['Ethereum Mainnet', 'Optimism', 'Binance Smart Chain', 'Polygon', 'Arbitrum One', 
                 'Avalanche C-Chain', 'Base', 'zkSync Mainnet', 'Gnosis', 'Fantom Opera',
                 'Cronos Mainnet', 'Celo Mainnet', 'Moonbeam', 'Moonriver', 'Harmony Mainnet Shard 0',
                 'Metis Andromeda Mainnet', 'Boba Network', 'Aurora Mainnet', 'Astar',
                 'Scroll', 'Linea', 'Mantle', 'Blast Mainnet', 'Mode Mainnet',
                 'Manta Pacific Mainnet', 'Sonic Mainnet', 'PulseChain', 'Kroma',
                 'Fraxtal', 'Zora', 'opBNB Mainnet', 'Polygon zkEVM']
    
    major_polkadot = ['Polkadot', 'Kusama', 'Acala', 'Astar', 'Moonbeam', 'Moonriver',
                      'Phala', 'Bifrost', 'Centrifuge', 'HydraDX', 'Interlay', 'Nodle']
    
    f.write("=== MAINNET NETWORK NAMES ===\n")
    for n in mainnets:
        name = n.get('name', '?')
        platform = n.get('platform', '?')
        rpcs = len(n.get('rpcs', []))
        native = n.get('nativeCurrency', {}).get('symbol', '?')
        cg = n.get('nativeCurrency', {}).get('coingeckoId', '')
        f.write(f"{name} | {platform} | rpcs={rpcs} | {native} | cg={cg}\n")

print(f"Wrote {len(mainnets)} mainnet names to /tmp/mainnet_names.txt")
print(f"Wrote {len(cg_ids)} coingecko IDs to /tmp/token_cgids.txt")
print(f"Wrote condensed summary to /tmp/chaindata_condensed.txt")

# Also produce categorized summary
# Count networks with 0 RPCs
no_rpcs = [n for n in mainnets if len(n.get('rpcs', [])) == 0]
print(f"\nMainnets with 0 RPCs: {len(no_rpcs)}")
for n in no_rpcs:
    print(f"  {n.get('name', '?')}")

# Count networks with native token coingecko ID
has_cg = [n for n in mainnets if n.get('nativeCurrency', {}).get('coingeckoId')]
print(f"\nMainnets with native token coingeckoId: {len(has_cg)}")
print(f"Mainnets without native token coingeckoId: {len(mainnets) - len(has_cg)}")
