#!/usr/bin/env python3
"""
Reduce chaindata-v9-slimg.json tokens to max ~1000 of the most popular.
Priority:
  1. All Bittensor mainnet tokens (subnets + native) - always kept
  2. Native tokens of all remaining networks - always kept
  3. Top tokens by CoinGecko market cap rank - fill remaining slots
"""

import json
import re

# ============================================================
# Top ~500 CoinGecko IDs by market cap (April 2026), scraped from coingecko.com
# ============================================================
TOP_COINGECKO_IDS = {
    # Top 100
    "bitcoin", "ethereum", "tether", "xrp", "bnb", "usdc", "solana", "tron",
    "dogecoin", "whitebit-coin", "usds", "hyperliquid", "cardano", "leo-token",
    "bitcoin-cash", "chainlink", "memecore", "monero", "ethena-usde", "canton",
    "zcash", "stellar", "dai", "litecoin", "avalanche", "usd1", "paypal-usd",
    "sui", "hedera", "rain", "shiba-inu", "toncoin", "cronos", "circle-usyc",
    "tether-gold", "world-liberty-financial", "bittensor", "pax-gold",
    "global-dollar", "mantle", "polkadot", "uniswap", "near-protocol", "okb",
    "sky", "pi-network", "aave", "aster", "pepe", "htx-dao", "usdd",
    "ripple-usd", "internet-computer", "ethena-usde", "ondo-us-dollar-yield",
    "ethereum-classic", "bitget-token", "ondo", "pump-fun", "kucoin",
    "gate", "quant", "worldcoin", "algorand", "morpho", "render",
    "ethena", "pol-ex-matic", "kaspa", "cosmos-hub", "nexo",
    "aptos", "arbitrum", "filecoin", "official-trump", "flare",
    "jupiter", "vechain", "xdc-network", "beldex",
    "gho", "bonk", "usual-usd", "just",
    # 101-200
    "dexe", "pancakeswap", "artificial-superintelligence-alliance",
    "trueusd", "layerzero", "pudgy-penguins", "virtuals-protocol",
    "dash", "stacks", "chiliz", "eurc", "first-digital-usd",
    "tezos", "ether-fi", "monad", "venice-token", "sei",
    "aerodrome-finance", "prime", "lido-dao", "celestia", "decred",
    "sun-token", "conflux", "curve-dao", "injective",
    "spx6900", "bittorrent", "bitcoin-sv", "gnosis", "floki",
    "kite", "maple-finance", "optimism", "kaia", "jasmycoin",
    "the-graph", "pyth-network", "story", "ethereum-name-service",
    "compound", "the-sandbox", "fartcoin", "dogwifhat", "starknet",
    "telcoin", "pendle", "humanity", "grass", "neo",
    "axie-infinity", "theta-network", "helium", "swissborg",
    "raydium", "decentraland", "onyxcoin", "ordi",
    "trust-wallet", "sonic", "convex-finance",
    # 201-300
    "gala", "enjin-coin", "jito", "zksync", "basic-attention",
    "safepal", "stasis-euro", "arweave", "thorchain", "ecash",
    "immutable", "origintrail", "vaulta", "golem",
    "eigencloud-prev-eigenlayer", "1inch", "sosovalue",
    "centrifuge", "multiversx", "aethir", "akash-network", "0g",
    "livepeer", "melania-meme", "nexus-mutual", "cow-protocol",
    "synthetix", "apecoin", "kamino", "lombard",
    "mask-network", "casper-network",
    "siacoin", "terra", "ankr-network", "xyo-network", "celo",
    "redstone", "request", "reserve-rights",
    "beam", "chutes", "sushi",
    "vvs-finance", "orca", "mog-coin",
    "moca-network", "cat-in-a-dogs-world", "hashkey-platform-token",
    "magic-eden", "mantra", "numeraire",
    "popcat", "neiro",
    # 301-500 (selected top ones)
    "berachain", "wemix", "horizen", "kava", "flow",
    "aleo", "merlin-chain", "openledger", "changenow",
    "safe", "dydx", "bio-protocol",
    "ronin", "astar", "movement", "plume",
    "polymesh", "aelf", "nano", "verus",
    "iota", "fasttoken",
    "creditcoin", "dusk", "mina-protocol",
    "aioz-network", "zetachain",
    "oasis", "digibyte", "plasma",
    "irys", "fevm", "spark",
    "babydoge", "moon-deng", "frax-usd",
    "maker", "wrapped-bitcoin", "lido-staked-ether",
    "wrapped-steth", "coinbase-wrapped-btc",
    "wrapped-eeth", "rocket-pool-eth",
    "frax-ether", "binance-staked-sol",
    "mantle-staked-ether", "renzo-restaked-eth",
    "kelp-dao-restaked-eth", "puffer-restaked-eth",
    "lbtc", "tbtc", "solvbtc",
    # Major DeFi / wrapped / stablecoins
    "frax", "crvusd", "usdai", "usx",
    "olympus", "ribbon-finance",
    "balancer", "yearn-finance", "gmx",
    "benqi", "trader-joe", "spell-token",
    "quickswap", "camelot-token",
    # Major memecoins
    "pepe", "bonk", "dogwifhat", "floki", "shiba-inu",
    "brett", "cat-in-a-dogs-world", "popcat", "mog-coin",
    "turbo-2", "myro", "book-of-meme",
    # Gaming / Metaverse
    "immutable", "gala", "axie-infinity", "the-sandbox", "decentraland",
    "illuvium", "enjin-coin", "ronin",
    # AI tokens
    "artificial-superintelligence-alliance", "render", "akash-network",
    "bittensor", "ocean-protocol", "singularitynet",
    # Polkadot ecosystem tokens
    "polkadot", "kusama", "moonbeam", "moonriver", "acala",
    "astar", "hydradx", "bifrost-native-coin", "phala",
    "centrifuge", "interlay", "nodle-network", "unique-network",
    "zeitgeist", "ternoa", "vara-network", "ajuna-network",
    "frequency-network", "pendulum-chain", "krest",
    "enjin-coin", "polymesh", "robonomics-network",
    "aleph-zero", "xx-network", "origintrail",
    "crust-network", "darwinia-network-native-token",
    "chainx", "chainflip", "creditcoin",
    "energy-web-token", "mythos",
    # Bittensor subnet tokens (many have CG ids)
    "apex-5", "sturdy-subnet", "dippy", "compute-horde", "data-universe",
    "taohash", "bitquant", "bitads", "404-gen", "zeus-5",
    "nineteen-ai", "bitagent-rizzo", "omega-any-to-any", "desearch",
    "nuance-2", "omega-labs", "mainframe-2", "storb", "ni-compute",
    "coldint", "bettensor", "candles", "itsai", "readyai",
    "bitmind", "logicnet", "web-agents-autoppia", "finetuning",
    "distributed-training", "chunking", "sportstensor",
    "real-time-data-by-masa", "graphite", "score", "swe-rizzo",
    "neural3d", "for-sale", "nextplace", "polariscloud-ai",
    "openkaito", "subvortex", "proprietary-trading-network",
    "templar", "targon", "omron", "iota-2",
    "pla-form", "better-therapy", "happyai-2", "soundsright",
    "liquidity-provisioning", "tiger-alpha", "internet-of-intelligence",
    "taoillium", "rich-kids-of-tao", "oneoneone", "minotaur-2",
    "taonado", "level-114", "cognify", "solmev", "rna-2",
    "hodl-etf", "satori", "affine", "sundae-bar", "bitrecs",
    "mantis-2", "swarm-3", "8-ball", "cel-ai",
    "bitsec-ai", "redteam", "ridges-ai",
    "alpha-trader-exchange-atx", "chutes", "tao-private-network",
    "fakenews", "tenex", "nova-3", "vericore", "kora",
    "streetvision-by-natix", "merit-2", "gittensor", "hippius",
    "safe-scan", "liquidity", "loosh", "aos-2", "ai-factory",
    "patrol-tao-com", "hermes-3", "docs-insight-tatsu", "vidaio",
    "miao", "checkerchain-2", "staking-2", "infinitehash",
    "brain", "tensorprox", "reinforced-ai", "bitcast", "eastworld",
    "flamewire", "creator-2", "neza",
    "dojo-3", "efficientfrontier", "webgenieai", "precog",
    "gradients", "gaia-2", "dippy-speech", "agent-arena-by-masa",
    "w-ai-parked",
    # Additional major DeFi tokens present on multiple chains
    "weth", "wrapped-bitcoin", "usdc", "tether",
    "rocket-pool", "lido-dao", "eigen-layer",
    "ens", "graph", "chainlink",
    "compound-governance-token", "maker",
    "synthetix-network-token",
    # L2 tokens
    "arbitrum", "optimism", "polygon", "mantle", "scroll",
    "linea", "base", "zksync", "blast", "mode-network",
    "kroma", "starknet", "fraxtal",
}

INPUT_FILE = 'chaindata/chaindata-v9-slim.json'
OUTPUT_FILE = 'chaindata/chaindata-v9-slim.json'  # overwrite in-place

with open(INPUT_FILE) as f:
    data = json.load(f)
input_size = __import__('os').path.getsize(INPUT_FILE)

networks = data['networks']
tokens = data['tokens']
mini_metadatas = data['miniMetadatas']

# Collect network IDs and their nativeTokenIds
native_token_ids = set()
for n in networks:
    ntid = n.get('nativeTokenId')
    if ntid:
        native_token_ids.add(ntid)

def is_bittensor_mainnet_token(token):
    network_id = str(token.get('networkId', '')).lower()
    tid = str(token.get('id', '')).lower()
    if network_id == 'bittensor' or (tid.startswith('bittensor:') and not tid.startswith('bittensor-testnet')):
        return True
    return False

# ============================================================
# Classify tokens into priority buckets
# ============================================================
bucket_bittensor = []  # Always keep
bucket_native = []     # Always keep
bucket_top = []        # Keep if space
bucket_rest = []       # Don't keep

for t in tokens:
    tid = t.get('id', '')
    cg_id = t.get('coingeckoId', '') or ''

    if is_bittensor_mainnet_token(t):
        bucket_bittensor.append(t)
    elif tid in native_token_ids:
        bucket_native.append(t)
    elif cg_id.lower() in TOP_COINGECKO_IDS:
        bucket_top.append(t)
    else:
        bucket_rest.append(t)

MAX_TOKENS = 1000

# Always-keep tokens
always_keep = bucket_bittensor + bucket_native
remaining_slots = MAX_TOKENS - len(always_keep)

print(f"Bittensor tokens: {len(bucket_bittensor)}")
print(f"Native tokens: {len(bucket_native)}")
print(f"Top market cap tokens: {len(bucket_top)}")
print(f"Other tokens: {len(bucket_rest)}")
print(f"Always-keep: {len(always_keep)}")
print(f"Remaining slots: {remaining_slots}")

# Keep all chain instances of top tokens (e.g. USDC on ETH, Polygon, Arbitrum, etc.)
# Take up to remaining_slots
selected_top = bucket_top[:remaining_slots]

kept_tokens = always_keep + selected_top

print(f"\n{'='*60}")
print(f"RESULT: {len(kept_tokens)} tokens (target: {MAX_TOKENS})")
print(f"  Bittensor: {len(bucket_bittensor)}")
print(f"  Native: {len(bucket_native)}")
print(f"  Top market cap: {len(selected_top)}")
print(f"{'='*60}")

# Write output
output = {
    'networks': networks,
    'tokens': kept_tokens,
    'miniMetadatas': mini_metadatas,
}

output_path = OUTPUT_FILE
with open(output_path, 'w') as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

import os
new_size = os.path.getsize(output_path)
print(f"\nFile size: {input_size/1024/1024:.1f} MB -> {new_size/1024/1024:.1f} MB ({(1-new_size/input_size)*100:.0f}% reduction)")

# Verify
net_ids = set(n['id'] for n in networks)
native_kept = sum(1 for t in kept_tokens if t.get('id') in native_token_ids)
bt_kept = sum(1 for t in kept_tokens if is_bittensor_mainnet_token(t))
has_cg = sum(1 for t in kept_tokens if t.get('coingeckoId'))
print(f"\nNative tokens kept: {native_kept}")
print(f"Bittensor tokens kept: {bt_kept}")
print(f"Tokens with coingeckoId: {has_cg}")
print(f"Tokens without coingeckoId: {len(kept_tokens) - has_cg}")

# Check all native tokens are present
missing_native = [ntid for ntid in native_token_ids if not any(t.get('id') == ntid for t in kept_tokens)]
if missing_native:
    print(f"\nWARNING: Missing native tokens: {missing_native}")
else:
    print(f"\nAll native tokens present ✓")

print(f"\nOutput written to: {output_path}")
