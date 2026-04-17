import json

with open('chaindata/chaindata-v9.json') as f:
    data = json.load(f)

networks = data.get('networks', [])
tokens = data.get('tokens', [])

print(f'Total networks: {len(networks)}')
print(f'Total tokens: {len(tokens)}')

testnets = [n for n in networks if n.get('isTestnet')]
print(f'Testnets: {len(testnets)}')
print(f'Non-testnet networks: {len(networks) - len(testnets)}')

print('\n--- ALL NETWORKS ---')
for n in networks:
    testnet = ' [TESTNET]' if n.get('isTestnet') else ''
    platform = n.get('platform', '?')
    print(f"  id={n['id']} platform={platform} name={n.get('name','?')}{testnet}")

print('\n--- TOKEN KEYS ---')
if tokens:
    print(list(tokens[0].keys()))

print('\n--- ALL TOKENS (id, symbol, coingeckoId) ---')
for t in tokens:
    print(f"  id={t.get('id','?')} | symbol={t.get('symbol','?')} | cg={t.get('coingeckoId','?')} | name={t.get('contractAddress', t.get('name','?'))}")
