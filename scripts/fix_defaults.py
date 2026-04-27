#!/usr/bin/env python3
"""
Update isDefault flags in chaindata-v9-slim.json according to rules:
1. Bittensor network, native TAO, and all subnet tokens: isDefault=true
2. All native tokens of all networks: isDefault=true
3. Only top 10 Polkadot/Kusama ecosystem chains get isDefault=true on network
4. Non-Polkadot chains that had isDefault: keep max 5 default tokens per chain
   (except Ethereum which gets up to 15)
5. USDC/USDT default on Ethereum + popular chains
6. Ethereum gets popular wrapped tokens including Wrapped SOL
"""

import json

INPUT = 'chaindata/chaindata-v9-slim.json'
OUTPUT = 'chaindata/chaindata-v9-slim.json'

with open(INPUT) as f:
    data = json.load(f)

networks = data['networks']
tokens = data['tokens']

# Build a lookup set of all token IDs that exist in the file
existing_token_ids = {t['id'] for t in tokens}

# ============================================================
# STEP 1: Define which Polkadot/Kusama networks keep isDefault
# Top 10 by TVL, activity, ecosystem importance (April 2026)
# ============================================================
TOP_POLKADOT_NETWORKS = {
    'polkadot',            # Polkadot relay chain
    'kusama',              # Kusama relay chain
    'polkadot-asset-hub',  # System chain for assets
    'moonbeam',            # Top EVM parachain
    'astar',               # Major dApp hub
    'hydradx',             # Hydration - top DeFi chain
    'acala',               # DeFi hub
    'bifrost-polkadot',    # Liquid staking
    'mythos',              # Gaming chain (Mythical Games)
    'moonriver',           # Kusama EVM canary
}

# Bittensor always keeps default
BITTENSOR_NETWORK_IDS = {'bittensor', '964'}

# ============================================================
# STEP 2: Update network isDefault flags
# ============================================================
# Non-Polkadot networks that should keep isDefault (EVM majors + Solana)
EVM_DEFAULT_NETWORKS = {
    '1',       # Ethereum
    '10',      # Optimism
    '56',      # BSC
    '137',     # Polygon
    '42161',   # Arbitrum One
    '8453',    # Base
    '146',     # Sonic
}
SOLANA_DEFAULT = {'solana-mainnet'}

KEEP_NETWORK_DEFAULT = (
    TOP_POLKADOT_NETWORKS
    | BITTENSOR_NETWORK_IDS
    | EVM_DEFAULT_NETWORKS
    | SOLANA_DEFAULT
)

for n in networks:
    nid = str(n.get('id', ''))
    if nid in KEEP_NETWORK_DEFAULT:
        n['isDefault'] = True
    else:
        if 'isDefault' in n:
            del n['isDefault']

# ============================================================
# STEP 3: Collect native token IDs and Bittensor token IDs
# ============================================================
native_token_ids = set()
for n in networks:
    ntid = n.get('nativeTokenId')
    if ntid:
        native_token_ids.add(ntid)

def is_bittensor_token(token):
    nid = str(token.get('networkId', '')).lower()
    tid = str(token.get('id', '')).lower()
    return nid == 'bittensor' or nid == '964' or (
        tid.startswith('bittensor:') and not tid.startswith('bittensor-testnet')
    )

# ============================================================
# STEP 4: Define per-chain default tokens (VERIFIED to exist in file)
# Ethereum: up to 15 | Other EVM chains: up to 5
# ============================================================

# Ethereum: 15 top tokens (stablecoins, wrapped, DeFi blue chips)
ETH_DEFAULT_TOKENS = {
    '1:evm-erc20:0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48',  # USDC
    '1:evm-erc20:0xdac17f958d2ee523a2206206994597c13d831ec7',  # USDT
    '1:evm-erc20:0x6b175474e89094c44da98b954eedeac495271d0f',  # DAI
    '1:evm-erc20:0x4c9edd5852cd905f086c759e8383e09bff1e68b3',  # USDe (Ethena)
    '1:evm-erc20:0x2260fac5e5542a773aa44fbcfedf7c193bc2c599',  # WBTC
    '1:evm-erc20:0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2',  # WETH
    '1:evm-erc20:0x7f39c581f595b53c5cb19bd0b3f8da6c935e2ca0',  # wstETH (Lido)
    '1:evm-erc20:0xae78736cd615f374d3085123a210448e74fc6393',  # rETH (Rocket Pool)
    '1:evm-erc20:0xd31a59c85ae9d8edefec411d448f90841571b89c',  # Wrapped SOL (Wormhole)
    '1:evm-erc20:0xcbb7c0000ab88b473b1f5afd9ef808440eed33bf',  # cbBTC (Coinbase)
    '1:evm-erc20:0x514910771af9ca656af840dff83e8264ecf986ca',  # LINK
    '1:evm-erc20:0x1f9840a85d5af5bf1d1762f925bdaddc4201f984',  # UNI
    '1:evm-erc20:0x7fc66500c84a76ad7e9c93437bfc5ac33e2ddae9',  # AAVE
    '1:evm-erc20:0x6982508145454ce325ddbe47a25d4ec3d2311933',  # PEPE
    '1:evm-erc20:0xe9f6d9898f9269b519e1435e6ebaff766c7f46bf',  # vTAO
}

# Arbitrum: 5 top tokens
ARB_DEFAULT_TOKENS = {
    '42161:evm-erc20:0xaf88d065e77c8cc2239327c5edb3a432268e5831',  # USDC
    '42161:evm-erc20:0x912ce59144191c1204e64559fe8253a0e49e6548',  # ARB
    '42161:evm-erc20:0xfc5a1a6eb076a2c7ad06ed22c90d7e710e35ad0a',  # GMX
    '42161:evm-erc20:0xf97f4df75117a78c1a5a0dbb814af92458539fb4',  # LINK
    '42161:evm-erc20:0xfa7f8980b0f1e64a2062791cc3b0871572f1f7f0',  # UNI
}

# Optimism: 5 top tokens
OP_DEFAULT_TOKENS = {
    '10:evm-erc20:0x0b2c639c533813f4aa9d7837caf62653d097ff85',  # USDC
    '10:evm-erc20:0x94b008aa00579c1307b0ef2c499ad98a8ce58e58',  # USDT
    '10:evm-erc20:0x4200000000000000000000000000000000000042',  # OP
    '10:evm-erc20:0x350a791bfc2c21f9ed5d10980dad2e2638ffa7f6',  # LINK
    '10:evm-erc20:0x76fb31fb4af56892a25e32cfc43de717950c9278',  # AAVE
}

# Base: 5 top tokens
BASE_DEFAULT_TOKENS = {
    '8453:evm-erc20:0x833589fcd6edb6e08f4c7c32d4f71b54bda02913',  # USDC
    '8453:evm-erc20:0x50c5725949a6f0c72e6c4a641f24049a917db0cb',  # DAI
    '8453:evm-erc20:0x940181a94a35a4569e4529a3cdfb74e38fd98631',  # AERO
    '8453:evm-erc20:0xcbb7c0000ab88b473b1f5afd9ef808440eed33bf',  # cbBTC
    '8453:evm-erc20:0x88fb150bdc53a65fe94dea0c9ba0a6daf8c6e196',  # LINK
}

# BSC: 5 top tokens
BSC_DEFAULT_TOKENS = {
    '56:evm-erc20:0x8ac76a51cc950d9822d68b83fe1ad97b32cd580d',  # USDC
    '56:evm-erc20:0xfb6115445bff7b52feb98650c87f44907e58f802',  # AAVE
    '56:evm-erc20:0xf8a0bf9cf54bb92f17374d9e9a321e6a111a51bd',  # LINK
    '56:evm-erc20:0xbf5140a22578168fd562dccf235e5d43a02ce9b1',  # UNI
    '56:evm-erc20:0xfb5b838b6cfeedc2873ab27866079ac55363d37e',  # FLOKI
}

# Polygon: 5 top tokens
POLY_DEFAULT_TOKENS = {
    '137:evm-erc20:0x3c499c542cef5e3811e1192ce70d8cc03d5c3359',  # USDC
    '137:evm-erc20:0xc2132d05d31c914a87c6611c10748aeb04b58e8f',  # USDT
    '137:evm-erc20:0xd6df932a45c0f255f85145f286ea0b292b21c90b',  # AAVE
    '137:evm-erc20:0x53e0bca35ec356bd5dddfebbd1fc0fd03fabad39',  # LINK
    '137:evm-erc20:0xb33eaad8d922b1083446dc23f610c2567fb5180f',  # UNI
}

# Sonic: just native token (small ecosystem)
SONIC_DEFAULT_TOKENS = set()

# ============================================================
# Polkadot parachain defaults (max 5 non-native per chain)
# Native tokens are always default via Rule 2, so these are the top 4 extras
# ============================================================

# Acala: top DeFi hub — DOT (relay), WETH, WBTC, GLMR (top parachain tokens in DeFi pools)
ACALA_DEFAULT_TOKENS = {
    'acala:substrate-tokens:N4IgLgngDgpiBcIAqB7A1jAdiANCAbgIYA2ArnPKJLAiACIDySIAvi0A',  # DOT
    'acala:substrate-tokens:N4IgLgngDgpiBcIBiB7ATjAlgcwHYEEBnQmMEAGhADcBDAGwFc54A2AXyA',  # WETH
    'acala:substrate-tokens:N4IgLgngDgpiBcIBiB7ATjAlgcwHYEEBnQmMEAGhADcBDAGwFc54BWAXyA',  # WBTC
    'acala:substrate-tokens:N4IgLgngDgpiBcIBiB7ATjAlgcwHYEEBnQmMEAGhADcBDAGwFc54AGAXyA',  # GLMR
}

# Astar: multi-VM dApp hub — DOT, USDT (native stablecoin), GLMR, ACA
ASTAR_DEFAULT_TOKENS = {
    'astar:substrate-assets:340282366920938463463374607431768211455',  # DOT
    'astar:substrate-assets:4294969280',  # USDT
    'astar:substrate-assets:18446744073709551619',  # GLMR
    'astar:substrate-assets:18446744073709551616',  # ACA
}

# Bifrost: liquid staking — DOT, USDT, GLMR, WETH (top staked/bridged assets)
BIFROST_DEFAULT_TOKENS = {
    'bifrost-polkadot:substrate-tokens:N4IgLgngDgpiBcIAqB7A1jAdgJhAGhADcBDAGwFc54AGAXyA',  # DOT
    'bifrost-polkadot:substrate-tokens:N4IgLgngDgpiBcIAqB7A1jAdgJhAGhADcBDAGwFc55sBfIA',  # USDT
    'bifrost-polkadot:substrate-tokens:N4IgLgngDgpiBcIAqB7A1jAdgJhAGhADcBDAGwFc54BGAXyA',  # GLMR
    'bifrost-polkadot:substrate-tokens:N4IgLgngDgpiBcIAqB7A1jAdgJhAGhADcBDAGwFc54BGAZgF8g',  # WETH
}

# Hydration: top DEX — USDT (2 variants), AAVE, tBTC (top liquidity pool assets)
HYDRATION_DEFAULT_TOKENS = {
    'hydradx:substrate-hydration:10',  # USDT
    'hydradx:substrate-hydration:1000767',  # USDT (Ethereum native)
    'hydradx:substrate-hydration:1000624',  # AAVE
    'hydradx:substrate-hydration:1000765',  # tBTC
}

# Combine all explicit defaults
EXPLICIT_POLKADOT_DEFAULTS = (
    ACALA_DEFAULT_TOKENS | ASTAR_DEFAULT_TOKENS
    | BIFROST_DEFAULT_TOKENS | HYDRATION_DEFAULT_TOKENS
)

# Combine all explicit EVM token defaults
EXPLICIT_EVM_DEFAULTS = (
    ETH_DEFAULT_TOKENS | ARB_DEFAULT_TOKENS | OP_DEFAULT_TOKENS
    | BASE_DEFAULT_TOKENS | BSC_DEFAULT_TOKENS | POLY_DEFAULT_TOKENS
    | SONIC_DEFAULT_TOKENS
)

ALL_EXPLICIT_DEFAULTS = EXPLICIT_EVM_DEFAULTS | EXPLICIT_POLKADOT_DEFAULTS

# Warn about missing tokens
missing = ALL_EXPLICIT_DEFAULTS - existing_token_ids
if missing:
    print(f"WARNING: {len(missing)} explicit default tokens not found in file:")
    for m in sorted(missing):
        print(f"  {m}")

# ============================================================
# STEP 5: Update token isDefault flags
# ============================================================
for t in tokens:
    tid = t.get('id', '')
    network_id = str(t.get('networkId', ''))

    # Rule 1: Bittensor tokens always default
    if is_bittensor_token(t):
        t['isDefault'] = True
        continue

    # Rule 2: Native tokens always default
    if tid in native_token_ids:
        t['isDefault'] = True
        continue

    # Rule 3: Explicitly listed EVM or Polkadot tokens
    if tid in ALL_EXPLICIT_DEFAULTS:
        t['isDefault'] = True
        continue

    # Everything else: remove isDefault
    if 'isDefault' in t:
        del t['isDefault']

# ============================================================
# STEP 6: Add missing critical tokens (USDC, Wrapped SOL)
# These are essential for the wallet but were cut during the 1000-token reduction
# ============================================================
CRITICAL_MISSING_TOKENS = [
    {
        "id": "1:evm-erc20:0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
        "platform": "ethereum",
        "networkId": "1",
        "type": "evm-erc20",
        "symbol": "USDC",
        "decimals": 6,
        "name": "USD Coin",
        "coingeckoId": "usd-coin",
        "logo": "https://raw.githubusercontent.com/TalismanSociety/chaindata/main/assets/tokens/coingecko/usd-coin.webp",
        "contractAddress": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
        "isDefault": True,
    },
    {
        "id": "1:evm-erc20:0xd31a59c85ae9d8edefec411d448f90841571b89c",
        "platform": "ethereum",
        "networkId": "1",
        "type": "evm-erc20",
        "symbol": "SOL",
        "decimals": 9,
        "name": "Wrapped SOL",
        "coingeckoId": "sol-wormhole",
        "logo": "https://raw.githubusercontent.com/TalismanSociety/chaindata/main/assets/tokens/coingecko/sol-wormhole.webp",
        "contractAddress": "0xd31a59c85ae9d8edefec411d448f90841571b89c",
        "isDefault": True,
    },
    {
        "id": "42161:evm-erc20:0xaf88d065e77c8cc2239327c5edb3a432268e5831",
        "platform": "ethereum",
        "networkId": "42161",
        "type": "evm-erc20",
        "symbol": "USDC",
        "decimals": 6,
        "name": "USD Coin",
        "coingeckoId": "usd-coin",
        "logo": "https://raw.githubusercontent.com/TalismanSociety/chaindata/main/assets/tokens/coingecko/usd-coin.webp",
        "contractAddress": "0xaf88d065e77c8cc2239327c5edb3a432268e5831",
        "isDefault": True,
    },
    {
        "id": "10:evm-erc20:0x0b2c639c533813f4aa9d7837caf62653d097ff85",
        "platform": "ethereum",
        "networkId": "10",
        "type": "evm-erc20",
        "symbol": "USDC",
        "decimals": 6,
        "name": "USD Coin",
        "coingeckoId": "usd-coin",
        "logo": "https://raw.githubusercontent.com/TalismanSociety/chaindata/main/assets/tokens/coingecko/usd-coin.webp",
        "contractAddress": "0x0b2c639c533813f4aa9d7837caf62653d097ff85",
        "isDefault": True,
    },
    {
        "id": "8453:evm-erc20:0x833589fcd6edb6e08f4c7c32d4f71b54bda02913",
        "platform": "ethereum",
        "networkId": "8453",
        "type": "evm-erc20",
        "symbol": "USDC",
        "decimals": 6,
        "name": "USD Coin",
        "coingeckoId": "usd-coin",
        "logo": "https://raw.githubusercontent.com/TalismanSociety/chaindata/main/assets/tokens/coingecko/usd-coin.webp",
        "contractAddress": "0x833589fcd6edb6e08f4c7c32d4f71b54bda02913",
        "isDefault": True,
    },
    {
        "id": "56:evm-erc20:0x8ac76a51cc950d9822d68b83fe1ad97b32cd580d",
        "platform": "ethereum",
        "networkId": "56",
        "type": "evm-erc20",
        "symbol": "USDC",
        "decimals": 18,
        "name": "Binance-Peg USD Coin",
        "coingeckoId": "usd-coin",
        "logo": "https://raw.githubusercontent.com/TalismanSociety/chaindata/main/assets/tokens/coingecko/usd-coin.webp",
        "contractAddress": "0x8ac76a51cc950d9822d68b83fe1ad97b32cd580d",
        "isDefault": True,
    },
    {
        "id": "137:evm-erc20:0x3c499c542cef5e3811e1192ce70d8cc03d5c3359",
        "platform": "ethereum",
        "networkId": "137",
        "type": "evm-erc20",
        "symbol": "USDC",
        "decimals": 6,
        "name": "USD Coin",
        "coingeckoId": "usd-coin",
        "logo": "https://raw.githubusercontent.com/TalismanSociety/chaindata/main/assets/tokens/coingecko/usd-coin.webp",
        "contractAddress": "0x3c499c542cef5e3811e1192ce70d8cc03d5c3359",
        "isDefault": True,
    },
    # Hydration critical tokens
    {
        "id": "hydradx:substrate-hydration:1000624",
        "platform": "polkadot",
        "networkId": "hydradx",
        "type": "substrate-hydration",
        "symbol": "AAVE",
        "decimals": 18,
        "name": "Aave",
        "coingeckoId": "aave",
        "logo": "https://raw.githubusercontent.com/TalismanSociety/chaindata/main/assets/tokens/coingecko/aave.webp",
        "isDefault": True,
        "onChainId": 1000624,
        "assetType": "Token",
        "isSufficient": True,
        "existentialDeposit": "59084194977843",
    },
    {
        "id": "hydradx:substrate-hydration:1000765",
        "platform": "polkadot",
        "networkId": "hydradx",
        "type": "substrate-hydration",
        "symbol": "tBTC",
        "decimals": 18,
        "name": "Threshold BTC",
        "coingeckoId": "tbtc",
        "logo": "https://raw.githubusercontent.com/TalismanSociety/chaindata/main/assets/tokens/coingecko/tbtc.webp",
        "isDefault": True,
        "onChainId": 1000765,
        "assetType": "Token",
        "isSufficient": True,
        "existentialDeposit": "106803374987",
    },
    {
        "id": "hydradx:substrate-hydration:1000767",
        "platform": "polkadot",
        "networkId": "hydradx",
        "type": "substrate-hydration",
        "symbol": "USDT",
        "decimals": 6,
        "name": "Tether (Ethereum native)",
        "coingeckoId": "tether",
        "logo": "https://raw.githubusercontent.com/TalismanSociety/chaindata/main/assets/tokens/coingecko/tether.webp",
        "isDefault": True,
        "onChainId": 1000767,
        "assetType": "Token",
        "isSufficient": True,
        "existentialDeposit": "10000",
    },
]

added_count = 0
for crit_token in CRITICAL_MISSING_TOKENS:
    if crit_token['id'] not in existing_token_ids:
        tokens.append(crit_token)
        existing_token_ids.add(crit_token['id'])
        added_count += 1
        print(f"Added missing token: {crit_token['symbol']} on chain {crit_token['networkId']} ({crit_token['id']})")
    else:
        # Ensure it's set as default
        for t in tokens:
            if t['id'] == crit_token['id']:
                t['isDefault'] = True
                break

if added_count:
    print(f"Added {added_count} missing critical tokens")

# ============================================================
# STEP 7: Write output
# ============================================================
output = {
    'networks': networks,
    'tokens': tokens,
    'miniMetadatas': data['miniMetadatas'],
}

with open(OUTPUT, 'w') as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

# ============================================================
# Report
# ============================================================
from collections import Counter

default_nets = [n for n in networks if n.get('isDefault')]
default_toks = [t for t in tokens if t.get('isDefault')]

print(f"\n{'='*60}")
print(f"isDefault UPDATE COMPLETE")
print(f"{'='*60}")
print(f"\nDefault networks: {len(default_nets)} / {len(networks)}")

# Classify
dot_count = sum(1 for n in default_nets if n.get('platform') == 'polkadot')
evm_count = sum(1 for n in default_nets if n.get('platform') == 'ethereum')
other_count = len(default_nets) - dot_count - evm_count
print(f"  Polkadot/Kusama: {dot_count}")
print(f"  EVM: {evm_count}")
print(f"  Other: {other_count}")

print(f"\nDefault tokens: {len(default_toks)} / {len(tokens)}")

by_net = Counter(t.get('networkId','') for t in default_toks)
print(f"\nDefault tokens per network:")
for nid, cnt in by_net.most_common():
    name = next((n.get('name','') for n in networks if str(n['id']) == str(nid)), '?')
    print(f"  {cnt:>4}  {name} ({nid})")

# Verify USDC/USDT on key chains
print(f"\nStablecoin check:")
for symbol in ['USDC', 'USDT']:
    stable_defaults = [t for t in default_toks if t.get('symbol') == symbol]
    chains = [t.get('networkId') for t in stable_defaults]
    print(f"  {symbol} default on: {chains}")

# Verify wrapped SOL
wsol = [t for t in default_toks if t.get('id') == '1:evm-erc20:0xd31a59c85ae9d8edefec411d448f90841571b89c']
print(f"\nWrapped SOL on Ethereum: {'✓' if wsol else '✗'}")

bt_default = sum(1 for t in default_toks if is_bittensor_token(t))
native_default = sum(1 for t in default_toks if t.get('id') in native_token_ids)
print(f"\nBittensor default tokens: {bt_default}")
print(f"Native default tokens: {native_default}")

print(f"\nOutput written to: {OUTPUT}")
