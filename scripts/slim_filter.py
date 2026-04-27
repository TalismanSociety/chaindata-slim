#!/usr/bin/env python3
"""
Filter chaindata-v9.json into chaindata-v9-slim.json
Removes: testnets, dead/irrelevant/marginal chains, tokens without coingeckoId,
         tokens on removed chains, and associated miniMetadatas.
PRESERVES: All mainnet Bittensor entries (network, subnets, tokens) regardless of other criteria.
"""

import json
import sys

with open('chaindata/chaindata-v9.json') as f:
    data = json.load(f)

networks = data['networks']
tokens = data['tokens']
mini_metadatas = data['miniMetadatas']

# ============================================================
# STEP 1: Define which mainnet networks to KEEP (Tier 1 + Tier 2)
# ============================================================

# Tier 1: Major active chains with significant TVL/activity/users
tier1_networks = {
    'Ethereum Mainnet', 'Optimism', 'Binance Smart Chain', 'Polygon',
    'Arbitrum One', 'Avalanche C-Chain', 'Base', 'zkSync Mainnet',
    'Gnosis', 'Fantom Opera', 'Cronos Mainnet', 'Scroll', 'Linea',
    'Mantle', 'Blast', 'Manta Pacific Mainnet', 'Sonic Mainnet',
    'PulseChain', 'opBNB Mainnet', 'Polygon zkEVM', 'Celo Mainnet',
    'Hedera Mainnet', 'Filecoin - Mainnet', 'Ronin', 'Immutable zkEVM',
    'NEAR Protocol', 'Kaia Mainnet', 'Chiliz Chain', 'Berachain',
    'Unichain', 'Monad', 'Solana Mainnet',
    # Polkadot major
    'Polkadot', 'Kusama', 'Moonbeam', 'Moonriver', 'Acala',
    'Astar', 'Hydration', 'Bifrost Polkadot', 'Mythos',
    # Additional EVM
    'HyperEVM',
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
    'AIOZ Network', 'Lightlink Phoenix Mainnet', 'ZKFair Mainnet',
    'Kroma', 'ShimmerEVM', 'Bahamut', 'Etherlink Mainnet',
    'Cyber Mainnet', 'Superseed', 'Polynomial', 'Orderly Mainnet',
    'Neo X Mainnet', 'Hemi', 'Sophon', 'Superposition',
    'SKALE Calypso Hub', 'SKALE Europa Hub', 'SKALE Nebula Hub', 'SKALE Titan Hub',
    'Vana', 'Fluence',
    'DuckChain Mainnet',
    'Silicon zkEVM', 'GOAT Network', 'KiteAI',
    'Arbitrum Nova', 'Form Network',
    # Polkadot tier 2
    'Bifrost Kusama', 'Centrifuge', 'Interlay', 'Phala Network',
    'Unique', 'NeuroWeb', 'Frequency', 'Pendulum', 'Krest Network',
    'Tangle', 'Ternoa', 'LAOS', 'Heima', 'Aleph Zero',
    'Vara', 'Avail', 'Autonomys', 'zkVerify', 'Ajuna',
    'Polkadot Asset Hub', 'Kusama Asset Hub', 'Polkadot Bridge Hub',
    'Kusama Bridge Hub', 'Polkadot Collectives', 'Polkadot Coretime',
    'Polkadot People', 'Kusama Coretime', 'Kusama People',
    'Manta', 'Crust', 'Robonomics Kusama', 'Robonomics Polkadot',
    'Karura', 'Kabocha', 'Kreivo', 'Encointer',
    'Enjin Matrix', 'Enjin', 'Energy Web X', 'Polymesh',
    'Amplitude', 'Altair', 'Torus', 'Crust Shadow',
    'Humanode Mainnet', 'Analog Timechain', 'Chainflip', 'ChainX',
    'Bittensor', 'Cere', 'Liberland', 'XX Network',
    'Acurast', 'Acurast Canary', 'Allfeat',
    'Joystream', 'DAO IPCI', 'Zeitgeist', 'Xode',
    'Hyperbridge', 'Kintsugi', 'Basilisk', 'Tanssi',
    'CC Enterprise', 'Creditcoin', 'Curio', 'Elysium',
    'Hydration EVM',
    'Peaq', 'Sora Standalone',
    'Plasma Mainnet', 'VFlow',
}

keep_names = tier1_networks | tier2_networks


def is_bittensor_mainnet_network(network):
    """Check if a network is a Bittensor mainnet (not testnet)."""
    nid = str(network.get('id', '')).lower()
    name = network.get('name', '').lower()
    is_testnet = network.get('isTestnet', False)
    if is_testnet:
        return False
    return ('bittensor' in nid or 'bittensor' in name)


def is_bittensor_mainnet_token(token):
    """Check if a token belongs to the Bittensor mainnet."""
    network_id = str(token.get('networkId', '')).lower()
    tid = str(token.get('id', '')).lower()
    # Only mainnet bittensor, not bittensor-testnet
    if network_id == 'bittensor' or (tid.startswith('bittensor:') and not tid.startswith('bittensor-testnet')):
        return True
    return False


# ============================================================
# STEP 2: Filter networks
# ============================================================
kept_networks = []
kept_network_ids = set()

for n in networks:
    name = n.get('name', '')
    is_testnet = n.get('isTestnet', False)

    # Always keep Bittensor mainnet
    if is_bittensor_mainnet_network(n):
        kept_networks.append(n)
        kept_network_ids.add(n['id'])
        continue

    # Remove all testnets
    if is_testnet:
        continue

    # Keep Tier 1 + Tier 2
    if name in keep_names:
        kept_networks.append(n)
        kept_network_ids.add(n['id'])

# ============================================================
# STEP 3: Filter tokens
# ============================================================
kept_tokens = []

# Collect native token IDs from kept networks
native_token_ids = set()
for n in kept_networks:
    ntid = n.get('nativeTokenId')
    if ntid:
        native_token_ids.add(ntid)

for t in tokens:
    network_id = t.get('networkId', '')
    has_cg = bool(t.get('coingeckoId'))
    tid = t.get('id', '')

    # Always keep ALL mainnet Bittensor tokens (subnets included)
    if is_bittensor_mainnet_token(t):
        kept_tokens.append(t)
        continue

    # Must be on a kept network
    if network_id not in kept_network_ids:
        continue

    # Always keep native tokens of kept networks
    if tid in native_token_ids:
        kept_tokens.append(t)
        continue

    # Must have a coingeckoId
    if not has_cg:
        continue

    kept_tokens.append(t)

# ============================================================
# STEP 4: Filter miniMetadatas
# ============================================================
kept_minis = []

for m in mini_metadatas:
    chain_id = m.get('chainId', '')
    if chain_id in kept_network_ids:
        kept_minis.append(m)

# ============================================================
# STEP 5: Write output
# ============================================================
output = {
    'networks': kept_networks,
    'tokens': kept_tokens,
    'miniMetadatas': kept_minis,
}

output_path = 'chaindata/chaindata-v9-slim.json'
with open(output_path, 'w') as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

# ============================================================
# Report
# ============================================================
print("=" * 60)
print("FILTERING COMPLETE")
print("=" * 60)
print(f"\nNetworks: {len(networks)} -> {len(kept_networks)} (removed {len(networks) - len(kept_networks)})")
print(f"  Testnets removed: {sum(1 for n in networks if n.get('isTestnet'))}")
print(f"  Dead/irrelevant/marginal mainnets removed: {len(networks) - len(kept_networks) - sum(1 for n in networks if n.get('isTestnet'))}")
print(f"\nTokens: {len(tokens)} -> {len(kept_tokens)} (removed {len(tokens) - len(kept_tokens)})")

bittensor_tokens_kept = sum(1 for t in kept_tokens if is_bittensor_mainnet_token(t))
print(f"  Bittensor mainnet tokens kept: {bittensor_tokens_kept}")

non_cg_kept = sum(1 for t in kept_tokens if not t.get('coingeckoId'))
print(f"  Tokens without coingeckoId kept (Bittensor subnets): {non_cg_kept}")

print(f"\nMiniMetadatas: {len(mini_metadatas)} -> {len(kept_minis)} (removed {len(mini_metadatas) - len(kept_minis)})")

import os
orig_size = os.path.getsize('chaindata/chaindata-v9.json')
new_size = os.path.getsize(output_path)
print(f"\nFile size: {orig_size/1024/1024:.1f} MB -> {new_size/1024/1024:.1f} MB ({(1-new_size/orig_size)*100:.0f}% reduction)")

# Verify Bittensor
bt_nets = [n for n in kept_networks if 'bittensor' in str(n.get('id','')).lower() or 'bittensor' in n.get('name','').lower()]
print(f"\nBittensor networks in output: {len(bt_nets)}")
for n in bt_nets:
    print(f"  id={n['id']} name={n.get('name')}")

print(f"\nOutput written to: {output_path}")
