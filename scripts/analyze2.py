import json

with open('chaindata/chaindata-v9.json') as f:
    data = json.load(f)

networks = data.get('networks', [])
tokens = data.get('tokens', [])

# Separate testnets
testnets = [n for n in networks if n.get('isTestnet')]
mainnets = [n for n in networks if not n.get('isTestnet')]

print(f'=== SUMMARY ===')
print(f'Total networks: {len(networks)}')
print(f'  Testnets: {len(testnets)}')
print(f'  Mainnets: {len(mainnets)}')
print(f'Total tokens: {len(tokens)}')

# Platforms
from collections import Counter
platforms = Counter(n.get('platform','unknown') for n in mainnets)
print(f'\n=== MAINNET PLATFORMS ===')
for p, c in platforms.most_common():
    print(f'  {p}: {c}')

# List all mainnet names  
print(f'\n=== ALL MAINNETS ({len(mainnets)}) ===')
for n in mainnets:
    rpcs = n.get('rpcs', [])
    print(f"  {n['id']}|{n.get('name','?')}|{n.get('platform','?')}|rpcs={len(rpcs)}|native={n.get('nativeCurrency',{}).get('symbol','?')}")

# Token analysis
print(f'\n=== TOKEN STRUCTURE ===')
if tokens:
    print(f'Keys: {list(tokens[0].keys())}')
    
# Unique token symbols and coingecko ids
token_symbols = Counter(t.get('symbol','?') for t in tokens)
print(f'\nUnique token symbols: {len(token_symbols)}')

# Tokens with coingecko ids
cg_tokens = [t for t in tokens if t.get('coingeckoId')]
print(f'Tokens with coingeckoId: {len(cg_tokens)}')

# Unique coingecko ids
cg_ids = set(t.get('coingeckoId') for t in cg_tokens)
print(f'Unique coingeckoIds: {len(cg_ids)}')

# Print all unique coingecko IDs
print(f'\n=== ALL UNIQUE COINGECKO IDs ({len(cg_ids)}) ===')
for cid in sorted(cg_ids):
    print(f'  {cid}')

# Print top 50 most common token symbols
print(f'\n=== TOP 50 TOKEN SYMBOLS ===')
for sym, cnt in token_symbols.most_common(50):
    print(f'  {sym}: {cnt}')
