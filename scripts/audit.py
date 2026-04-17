import json

with open('chaindata/chaindata-v9.json') as f:
    data = json.load(f)

networks = data.get('networks', [])
tokens = data.get('tokens', [])
mainnets = [n for n in networks if not n.get('isTestnet')]
testnets = [n for n in networks if n.get('isTestnet')]

# ============================================================
# NETWORK RELEVANCE CLASSIFICATION (April 2026)
# Based on DeFiLlama TVL data, CoinGecko market data, ecosystem activity
# ============================================================

# Tier 1: Major chains with significant TVL/activity/users
tier1_networks = {
    'Ethereum Mainnet', 'Optimism', 'Binance Smart Chain', 'Polygon', 
    'Arbitrum One', 'Avalanche C-Chain', 'Base', 'zkSync Mainnet',
    'Gnosis', 'Fantom Opera', 'Cronos Mainnet', 'Scroll', 'Linea',
    'Mantle', 'Blast Mainnet', 'Manta Pacific Mainnet', 'Sonic Mainnet',
    'PulseChain', 'opBNB Mainnet', 'Polygon zkEVM', 'Celo Mainnet',
    'Hedera Mainnet', 'Filecoin - Mainnet', 'Ronin', 'Immutable zkEVM',
    'NEAR Protocol', 'Kaia Mainnet', 'Chiliz Chain', 'Berachain',
    'Unichain', 'Monad', 'Solana Mainnet',
    # Polkadot major
    'Polkadot', 'Kusama', 'Moonbeam', 'Moonriver', 'Acala',
    'Astar', 'Hydration', 'Bifrost Polkadot', 'Mythos',
}

# Tier 2: Active chains with moderate activity/TVL
tier2_networks = {
    'Flare Mainnet', 'Ethereum Classic', 'LUKSO Mainnet', 'Shiden',
    'Zora', 'Metis Andromeda Mainnet', 'Shibarium', 'Telos EVM Mainnet',
    'Boba Network', 'Energy Web Chain', 'Theta Mainnet', 'Fuse Mainnet',
    'Rootstock Mainnet', 'Oasys Mainnet', 'KCC Mainnet', 'OKXChain Mainnet',
    'IoTeX Network Mainnet', 'Cronos zkEVM Mainnet', 'Darwinia',
    'Songbird Canary-Network', 'GateChain Mainnet', 'Conflux eSpace',
    'IOTA EVM', 'Haqq Network', 'ZetaChain Mainnet', 'Taiko Alethia',
    'Injective', 'Sei Network', 'Flow EVM Mainnet', 'XDC Network',
    'BitTorrent Chain Mainnet', 'Syscoin Mainnet', 'Viction',
    'Elastos Smart Chain', 'Evmos', 'Aurora Mainnet', 'X Layer Mainnet',
    'HashKey Chain', 'Shape', 'Ink', 'World Chain', 'BOB', 'Treasure',
    'Abstract', 'Morph', 'Story', 'Lens', 'MegaETH', 'Soneium',
    'B3', 'Xai Mainnet', 'Degen Chain', 'Ancient8', 'Fraxtal',
    'EDU Chain', 'ApeChain', 'Lisk', 'Mint Mainnet', 'Mode',
    'Bitlayer Mainnet', 'Merlin Mainnet', 'CoinEx Smart Chain Mainnet',
    'Neon EVM Mainnet', 'Metal L2', 'Swellchain', 'Plume Mainnet',
    'Kinto Mainnet', 'Gravity Alpha Mainnet', 'Redstone',
    'Corn', 'RARI Chain', 'Reya Network', 'Zircuit Mainnet',
    'peaq', 'AIOZ Network', 'Lightlink Phoenix Mainnet', 'ZKFair Mainnet',
    'Kroma', 'ShimmerEVM', 'Bahamut', 'Etherlink Mainnet',
    'Cyber Mainnet', 'Superseed', 'Polynomial', 'Orderly Mainnet',
    'Neo X Mainnet', 'Hemi', 'Sophon', 'Superposition',
    'SKALE Calypso Hub', 'SKALE Europa Hub', 'SKALE Nebula Hub', 'SKALE Titan Hub',
    'Vana', 'Autonomous', 'Fluence', 
    'DuckChain Mainnet', 'Scolcoin Mainnet',
    'Silicon zkEVM', 'GOAT Network', 'KiteAI',
    # Polkadot tier 2
    'Bifrost Kusama', 'Centrifuge', 'Interlay', 'Phala Network',
    'Unique', 'NeuroWeb', 'Frequency', 'Pendulum', 'Krest Network',
    'Tangle', 'Ternoa', 'LAOS', 'Heima', 'Aleph Zero',
    'Vara', 'Avail', 'Autonomys', 'zkVerify', 'Ajuna',
    'Polkadot Asset Hub', 'Kusama Asset Hub', 'Polkadot Bridge Hub',
    'Kusama Bridge Hub', 'Polkadot Collectives', 'Polkadot Coretime',
    'Polkadot People', 'Kusama Coretime', 'Kusama People',
    'Manta', 'Crust', 'Robonomics Kusama', 'Robonomics Polkadot',
    'Karura', 'Kabocha', 'Kreivo', 'Sora', 'Encointer',
    'Enjin Matrix', 'Enjin', 'Energy Web X', 'Polymesh',
    'Amplitude', 'Altair', 'Torus', 'Crust Shadow',
    'Humanode', 'Analog Timechain', 'Chainflip', 'ChainX',
    'Bittensor', 'Cere', 'Liberland', 'XX Network',
    'Acurast', 'Acurast Canary', 'Allfeat',
    'Joystream', 'DAO IPCI', 'Zeitgeist', 'Xode',
    'Hyperbridge', 'Kintsugi', 'Basilisk',
    'CC Enterprise', 'Creditcoin', 'Curio', 'Elysium',
}

# Tier 3: Marginal/niche but technically alive
tier3_networks = {
    'Meter Mainnet', 'Ontology Mainnet', 'WEMIX3.0 Mainnet',
    'Dogechain Mainnet', 'Harmony Mainnet Shard 0', 'Canto',
    'Callisto Mainnet', 'Klaytn', 'Taraxa Mainnet', 'Oasis Sapphire',
    'Oasis Emerald', 'Swan Chain Mainnet', 'Prom', 'HyperEVM',
    'MANTRACHAIN Mainnet', 'Dymension', 'Palm', 'Bit Torrent Chain Donau',
    'Core Blockchain Mainnet', 'BounceBit Mainnet', 'BEVM Canary',
    'Humans.ai Mainnet', 'Map Protocol', 'Tenet', 'REI Network',
    'Shardeum', 'U2U Solaris Mainnet', 'Xpla Mainnet', 'Bitgert Mainnet',
    'KUB Mainnet', 'ENULS Mainnet', 'ThunderCore Mainnet',
    'Milkomeda C1 Mainnet', 'Godwoken Mainnet', 'Kava', 'Arthera Mainnet',
    'Bittensor EVM', 'Nibiru cataclysm-1', 'Starknet',
    'Citrea Mainnet', 'CrossFi Mainnet', 'Beam',
    'The Root Network - Mainnet', 'Planq Mainnet', 'Humanode Mainnet',
    'Realio', 'Nillion Network', 'Oraichain Mainnet',
    'COTI', 'Humanity Protocol', 'XRPL EVM',
    'AlienX Mainnet', 'Electroneum Mainnet', 'MXC zkEVM Moonchain',
    'EOS EVM Network', 'Nautilus Mainnet', 'Entangle Mainnet',
    'Saakuru Mainnet', 'Game7', 'PLAYA3ULL GAMES',
    'Forma', 'B2 Mainnet', 'IOST Mainnet', 'Ethernity',
    'Bitrock Mainnet', 'Lumia Mainnet', '0G Mainnet',
    'Irys Mainnet Beta', 'Botanix Mainnet',
    'Abey Mainnet', 'Waterfall Network', 'Catena Mainnet',
    'Whitechain', 'Nordek Mainnet', 'RSS3 VSL Mainnet',
    'Haust Network', 'HUMAN Protocol', 'Wanchain', 'Creditscore',
    'CratD2C', 'BOMB Chain', 'Vanar Mainnet',
    'Stratos', 'Horizen Mainnet', 'Numbers Mainnet',
    'Atleta Network', 'Graphite Mainnet', 'Gensyn Mainnet',
    'Somnia Mainnet', 'FormNetwork', 'Camp Network Mainnet',
    'River',
    # Polkadot marginal
    'VFlow', 'Vtb', 'Sora Standalone',
}

# Count matches
def classify_network(name):
    if name in tier1_networks:
        return 'tier1'
    elif name in tier2_networks:
        return 'tier2'
    elif name in tier3_networks:
        return 'tier3'
    else:
        return 'irrelevant'

tier1_count = 0
tier2_count = 0
tier3_count = 0
irrelevant_count = 0
irrelevant_names = []

for n in mainnets:
    name = n.get('name', '?')
    tier = classify_network(name)
    if tier == 'tier1':
        tier1_count += 1
    elif tier == 'tier2':
        tier2_count += 1
    elif tier == 'tier3':
        tier3_count += 1
    else:
        irrelevant_count += 1
        irrelevant_names.append(name)

total = len(mainnets)
relevant = tier1_count + tier2_count + tier3_count

print("=" * 60)
print("NETWORK RELEVANCE AUDIT - April 2026")
print("=" * 60)
print(f"\nTotal entries: {len(networks)}")
print(f"  Testnets: {len(testnets)} (all irrelevant for users)")
print(f"  Mainnets: {total}")
print()
print(f"Tier 1 (Major active chains): {tier1_count} ({tier1_count/total*100:.1f}%)")
print(f"Tier 2 (Active, moderate usage): {tier2_count} ({tier2_count/total*100:.1f}%)")
print(f"Tier 3 (Marginal/niche, alive): {tier3_count} ({tier3_count/total*100:.1f}%)")
print(f"Tier 4 (Dead/abandoned/irrelevant): {irrelevant_count} ({irrelevant_count/total*100:.1f}%)")
print()
print(f"RELEVANT (Tier 1+2): {tier1_count + tier2_count} ({(tier1_count+tier2_count)/total*100:.1f}%)")
print(f"BROADLY RELEVANT (Tier 1+2+3): {relevant} ({relevant/total*100:.1f}%)")
print(f"IRRELEVANT: {irrelevant_count} ({irrelevant_count/total*100:.1f}%)")
print()
print(f"INCLUDING TESTNETS:")
all_total = len(networks)
all_relevant = relevant
print(f"  Relevant: {all_relevant} / {all_total} = {all_relevant/all_total*100:.1f}%")
print(f"  Irrelevant (dead mainnets + all testnets): {all_total - all_relevant} / {all_total} = {(all_total-all_relevant)/all_total*100:.1f}%")

# ============================================================
# TOKEN RELEVANCE
# ============================================================
print()
print("=" * 60)
print("TOKEN RELEVANCE AUDIT - April 2026")
print("=" * 60)

# Tokens on relevant chains
relevant_chain_ids = set()
for n in mainnets:
    name = n.get('name', '?')
    tier = classify_network(name)
    if tier in ('tier1', 'tier2', 'tier3'):
        relevant_chain_ids.add(n['id'])

# Also add testnet IDs to ignore
testnet_ids = set(n['id'] for n in testnets)

# Classify tokens
tokens_on_relevant = 0
tokens_on_irrelevant = 0
tokens_on_testnet = 0
tokens_with_cg = 0
tokens_on_relevant_with_cg = 0
tokens_on_irrelevant_with_cg = 0

for t in tokens:
    tid = t.get('id', '')
    # Extract chain id from token id (format: "chainId:rest")
    chain_id = tid.split(':')[0] if ':' in tid else ''
    has_cg = bool(t.get('coingeckoId'))
    
    if chain_id in testnet_ids:
        tokens_on_testnet += 1
    elif chain_id in relevant_chain_ids:
        tokens_on_relevant += 1
        if has_cg:
            tokens_on_relevant_with_cg += 1
    else:
        tokens_on_irrelevant += 1
        if has_cg:
            tokens_on_irrelevant_with_cg += 1
    
    if has_cg:
        tokens_with_cg += 1

total_tokens = len(tokens)
print(f"\nTotal tokens: {total_tokens}")
print(f"  Tokens with CoinGecko ID: {tokens_with_cg} ({tokens_with_cg/total_tokens*100:.1f}%)")
print(f"  Tokens without CoinGecko ID: {total_tokens - tokens_with_cg} ({(total_tokens-tokens_with_cg)/total_tokens*100:.1f}%)")
print()
print(f"Tokens on relevant chains (Tier 1-3): {tokens_on_relevant} ({tokens_on_relevant/total_tokens*100:.1f}%)")
print(f"  ...with CoinGecko ID: {tokens_on_relevant_with_cg}")
print(f"Tokens on irrelevant/dead chains: {tokens_on_irrelevant} ({tokens_on_irrelevant/total_tokens*100:.1f}%)")
print(f"  ...with CoinGecko ID: {tokens_on_irrelevant_with_cg}")
print(f"Tokens on testnets: {tokens_on_testnet} ({tokens_on_testnet/total_tokens*100:.1f}%)")
print()

# Relevant tokens = on relevant chains AND have coingecko ID (i.e., actually tradeable)
# Conservative: only tokens with CoinGecko IDs on relevant chains
relevant_tokens = tokens_on_relevant_with_cg
print(f"RELEVANT TOKENS (on active chains + CoinGecko ID): {relevant_tokens} ({relevant_tokens/total_tokens*100:.1f}%)")
# Broader: all tokens on relevant chains (includes unlisted DeFi tokens, LP tokens etc)
print(f"BROADLY RELEVANT (all tokens on active chains): {tokens_on_relevant} ({tokens_on_relevant/total_tokens*100:.1f}%)")
print(f"IRRELEVANT (dead chains + testnets + no market): {total_tokens - tokens_on_relevant} ({(total_tokens-tokens_on_relevant)/total_tokens*100:.1f}%)")

print()
print("=" * 60)
print("UNMATCHED MAINNET NAMES (classified as irrelevant)")
print("=" * 60)
for name in sorted(irrelevant_names):
    print(f"  {name}")
