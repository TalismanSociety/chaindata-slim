#!/usr/bin/env python3
import json
import urllib.request

# Fetch chains data from chainid.network
url = 'https://chainid.network/chains_mini.json'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as resp:
    chains = json.loads(resp.read())

print(f"Total chains in registry: {len(chains)}")

# Look up specific chain IDs
target_ids = [1281, 10778, 42101, 6252, 1212385660403083, 747474]
print("\n=== EVM Chain ID Lookups ===")
for tid in target_ids:
    found = [c for c in chains if c['chainId'] == tid]
    if found:
        c = found[0]
        print(f"  {tid}: {c['name']}")
    else:
        print(f"  {tid}: NOT FOUND in chainid.network")

# Now look up genesis hashes against our full chaindata
print("\n=== Genesis Hash Lookups in Full Chaindata ===")
with open('chaindata/chaindata-v9.json', 'r') as f:
    full_data = json.load(f)

full_networks = full_data.get('networks', [])
print(f"Total networks in full chaindata: {len(full_networks)}")

# Build genesis hash index
gh_index = {}
for n in full_networks:
    gh = n.get('genesisHash', '')
    if gh:
        gh_index[gh.lower()] = n

# The unknown genesis hashes from the user's list
unknown_hashes = [
    "0x742a2ca70c2fda6cee4f8df98d64c4c670a052d9568058982dad9d5a7a135c5b",
    "0x68d56f15f85d3136970ec16946040bc1752654e906147f7e43e9d539d7c3de2f",
    "0xb3db41421702df9a7fcac62abc82e18b6e5b39b6e17a0d352a50c24d0637c0e9",
    "0xafdc188f45c71dacbaa0b62e16a91f726c7b8699a9748cdf715459de6b7f366d",
    "0x1bb969d85965e4bb5a651abbedf21a54b6b31a21f66b5401cc3f1e286268d736",
    "0xd2a5d385932d1f650dae03ef8e2748983779ee342c614f80854d32b8cd8fa48c",
    "0x262e1b2ad728475fd6fe88e62d34c200abe6fd693931ddad144059b1eb884e5b",
    "0xe143f23803ac50e8f6f8e62695d1ce9e4e1d68aa36c1cd2cfd15340213f3423e",
    "0xb0a8d493285c2df73290dfb7e61f870f17b41801197a149ca93654499ea3dafe",
    "0x48239ef607d7928874027a43a67689209727dfb3d3dc5e5b03a39bdc2edd57c5",
    "0xd4f71f8cb9ae10b5c4ca5e7627b55ff6b11cf36b5c59b5f0e1e82de1bdbd81d5",
    "0xd611f22d291c5b7b69f1e105cca03352984c344c4421977efaa4cbdd1834e2aa",
    "0x91b171bb158e2d3848fa23a9f1c25182fb8e20313b2c1eb49219da7a70ce90c3",
    "0xf1cf9022c7ebb34b162d5b5e34e705a5a740b2d0ecc1009f2bda2e33a64114c8",
    "0x6bd89e052d67a45bb60a9a23e8581053d5e0d619f15cb9865946937e690c42d6",
    "0xfe58ea77779b7abda7da4ec526d14db9b1e9cd40a217c34892af80a9b332b76d",
    "0x6811a339673c9daa897944dcdac99c6e2939cc88245ed21951a0a3c9a2be75bc",
    "0x9eb76c5184c4ab8679d2d5d819fdf90b9c001403e9e17da2e14b6d8aec4029c6",
    "0xddb89973361a170839f80f152d2e9e276c0aef8a36c548dc74b2048d38b29bba",
    "0x9f28c6a68e0fc9646eff64935684f6eeeece527e37bbe1f213d22caa1d9d6bed",
    "0x631ccc82a078481513b33a7f1195e276a91cf328e0bbb3dca3d7a0fbc1200844",
    "0xd43540ba6d3eb4897c28a77d48cb5b729fea37603cbbfc7a86a73b72adb3be8d",
    "0xcafb30298f0c74042b352c0f7a8a1b9ed6c56da tried",
    "0xe61a41c53f5dcd0beb09df93b34402aada44cb05117b71059cce40a2723a4e97",
    "0x6408de7b5bb18bfe1458e04e7dd3ffddd0d63fa2065334dade7d8782cf60f73d",
    "0x65b4a58aafda7dcc7c7e14bc3d7651035c4efdd58dd5f3d15abb5ca0e8f65f1a",
    "0xfc41b9bd8ef8fe53d58c7ea67c794c7ec9a73daf05e6d54b14ff6342c99ba64c",
    "0x411f057b9107718c9624d6aa4a3f23c1653898297f3d4d529d9bb6511a39dd21",
    "0x10af6e84234477d84dc572bbc3c70e11e7eaa46086c2a12a43d40997527e5e14",
    "0x3fd7b9eb6a00376e5be61f01abb429ffb0b104be05eaff4d458da48fcd425baf",
    "0x4ac80c99289841dd946ef92765bf659a307c5c205e2e5b3e86e67a22bb4e052a",
    "0x5d2143f1cccb27c0341b83a192fe0e8051993058c55e143eb4fb061b2db5e970",
    "0x9226d527cd7fb37ea0f466e06182c3c5f330f3f522799cb8cc17e0a080b49a2d",
]

# Fix any typos in the hashes
unknown_hashes = [h.strip() for h in unknown_hashes if h.startswith('0x') and len(h) >= 66]

for gh in unknown_hashes:
    gh_lower = gh.lower()
    if gh_lower in gh_index:
        n = gh_index[gh_lower]
        print(f"  {gh[:18]}...{gh[-8:]}: {n.get('name', 'UNNAMED')} (id: {n.get('id', 'N/A')})")
    else:
        print(f"  {gh[:18]}...{gh[-8:]}: NOT FOUND in full chaindata")
