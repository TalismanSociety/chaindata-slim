#!/usr/bin/env python3
"""Final comprehensive analysis: user's ~175 networks vs chaindata-v9-slim.json"""
import json

# Load slim chaindata
with open("chaindata/chaindata-v9-slim.json") as f:
    slim = json.load(f)

slim_networks = slim["networks"]

# Build lookup indices for slim
slim_ids = {n["id"].lower(): n for n in slim_networks}
slim_genesis = {}
slim_evm = {}
for n in slim_networks:
    gh = n.get("genesisHash")
    if gh:
        slim_genesis[gh.lower()] = n
    evm = n.get("evmChainId")
    if evm is not None:
        slim_evm[str(evm)] = n

# The user's complete list
user_entries = [
    "bittensor", "vara-testnet", "hydradx", "964", "420420417",
    "acurast-polkadot", "polkadot-asset-hub", "8453", "1",
    "bittensor-testnet", "astar", "paseo-asset-hub", "interlay",
    "0xee971a91ef92d733d86d3acc67a6394caa105f37a7757155f623bc5d0c4b690f",
    "bifrost-polkadot", "1281", "1284", "acurast", "liberland", "manta",
    "11155111", "137", "kusama-asset-hub", "42161",
    "0x4b5f95eefedf0d0fb514339edc24d2d411310520f687b4146145bcedb99885b9",
    "kintsugi", "560048", "xode-polkadot", "97", "56", "999", "84532",
    "acala", "57073",
    "0x8b404e7ed8789d813982b9cb4c8b664c05b3fbf433309f603af014ec9ce56a8c",
    "bifrost-kusama", "10778", "80094", "karura", "hyperbridge-polkadot",
    "paseo-testnet", "vara", "pendulum", "analog-timechain",
    "0x607eb79a6afc998768feeede697e21aef1fdf3565e8df2a9cb09daa64932c724",
    "5042002", "polkadot", "46630",
    "0x15b34a3b7443c73fa1f687cce2d8e5981f6a2eaad54809a6b6af28e83d2adaff",
    "2043", "polkadot-people", "10", "592", "avail", "42431", "43114",
    "0xc005581011570331f99e4071ab491cacae17553e0c8e17e6302ae1eebf89fdf4",
    "3338", "984", "46", "688689", "ewx", "polkadot-collectives", "unique",
    "0xd282ee1b23d5ae92e4550e1501b0160b5ee771015c58af715cb0949839e1fa58",
    "1868", "autonomys", "neuroweb",
    "0xc806038cc1d06766f23074ade7c5511326be41646deabc259970ff280c82a464",
    "0xd0a2c75ad080394edaaa9cd1c766b543478efb415db1b6cd7772536c9a413167",
    "0xdc6df9fa7aa108741193e54c0b15ba647ba09e165e59f801459e6519997bee03",
    "100", "222222", "enjin-matrixchain-testnet", "westend-asset-hub-testnet",
    "0xdb27fa0ebc235bad916ca832023a261ba2e062da07c27605c0cb751647ab2070",
    "0xc04fce5f049432a987c2288bfa9c99889387f35e944d545e31e894fa0fc0d1fc",
    "0xe6c30d6e148f250b887105237bcaa5cb9f16dd203bf7b5b9d4f1da7387cb86ec",
    "1212385660403083", "5234",
    "0x8b1cd0beeefb3760767de217697fbaa6152c0a1033f5f0d5b3eb46da39ee044c",
    "146", "1952",
    "custom-0x9226d527cd7fb37ea0f466e06182c3c5f330f3f522799cb8cc17e0a080b49a2d",
    "moonbeam", "1285", "mythos", "westend-testnet",
    "0xddb89973361a170839f80f152d2e9e38a376a5a7eccefcade763f46a8e567019",
    "1287", "centrifuge-polkadot",
    "0xa8c96b5526aa6f845650f8f6eeaf701779cac543b8c512baa22cc721adf03a5a",
    "peaq", "14853", "324", "42220", "747474", "ternoa", "zkverify",
    "0x897c91bdab20cf6c6e5c3499ed11b75284f567e5b91871f1a0a37e7956a10ca9",
    "59144", "945", "basilisk", "moonriver",
    "0x6684b23d3020601285a1bf165dedf84bd6f04dc33fbcd95de6128bd284feee74",
    "0x452496f50c9201c4b21ac57100eb471e1ebf763f498351d93f5dfe3602def643",
    "0xb0a6fadc9efc64e10efe816d9a403c886011a2e69d326657953a5d1921081f8e",
    "11142220", "143", "81457", "joystream", "shiden-kusama",
    "0x2bd1a2aa5c768692550e5d34e2a7ec295125239a7b7795e9fd8ee31a599ccc85",
    "0x3920bcb4960a1eef5580cd5367ff3f430eef052774f78468852f7b9cb39f8a3c",
    "169", "787", "98866", "tanssi",
    "0x38e8c158d58662ea7d9919a589906a1a440ac25f5c1f084dbc3b113ff0c09446",
    "0x68af83b70cd2ada556e6a5ea29de3d397e0966a7a07525bd1c7d90ad03a64d38",
    "1336", "20994", "267", "42101", "534352", "6252", "91342", "chainx",
    "shibuya-testnet", "xxnetwork",
    "0x35eadc576f10dac447f3f0a41443fa75b545c0b85473e118a30b0fe2d41832c1",
    "0x424f8764bb498528c41fa22ba4b9fcb890ac318e55b12309e256555b163b03cf",
    "0x50dd5d206917bf10502c68fb4d18a59fc8aa31586f4e8856b493e43544aa82aa",
    "0x5388faf792c5232566d21493929b32c1f20a9c2b03e95615eefec2aa26d64b73",
    "0x5e37bab89576bc4e8a6419bdd044cb0d21d8284031688f5252f45c211b8744bc",
    "0x767cfb547500ee59b6116207bc33a2be780503233930bf7df6cc7d40c4000fed",
    "0xbd924b8b2c4d3d16b22a4281c018fab8b9f4bcd1cebcfb5232837232ebfac0dd",
    "0xe5212ad89524946253f5017927e78b016beb3d66203cafa67e99223e80b034a2",
    "80002", "Bittensor", "avail-turing-testnet", "humanode", "laos",
    "polkadot-bridge-hub",
    "0x5a51e04b88a4784d205091aa7bada002f3e5da3045e5b05655ee4db2589c33b5",
    "0x6a525eb1cd3e76c04c8c637022f12d28d05875f8726b8d231ba923209d755de5",
    "0x744960c32e3a3df5440e1ecd4d34096f1ce2230d7016a5ada8a765d5a622b4ea",
    "0x8c3f75eb85807968bfcc316629bdfe4c778b91cf67e25ad6a75bbb4bc8bd313d",
    "1625", "232", "33139", "421614", "4326", "55244", "6283", "9745",
    "altair",
    "custom-0xd2a5d385932d1f650dae03ef8e2748983779ee342c614f80854d32b8cd8fa48c",
    "enjin-relay", "kusama",
    "0x432e176a6b0aa7ece9d4a884a1866219672e27dce777e4f2651cb6b18675e235",
    "0x5884733732ab5a115ae82e0b45491e994c731326d937af1f6960ec58efad0316",
    "0x7327427af12ba1875a69e4024c724388aacd40e971dc31cff3839d4941618e10",
    "0x97dc37ed537bfa3a740757e02c7a466503908364b1a359d8d5f9cb44def0deac",
    "0xeebb5d05763801e54d6a7a60a4b7998ac125c4d050dcec418dd07ea959a54464",
    "130", "1408", "2020", "60808", "ajuna",
    "custom-0x6bd89e052d67a45bb60a9a23e8581053d5e0d619f15cb9865946937e690c42d6",
    "polkadot-coretime", "robonomics-kusama", "sora-standalone", "zeitgeist",
]

# Known testnets (to be excluded)
KNOWN_TESTNETS = {
    "vara-testnet", "bittensor-testnet", "paseo-asset-hub", "paseo-testnet",
    "enjin-matrixchain-testnet", "westend-asset-hub-testnet", "westend-testnet",
    "shibuya-testnet", "avail-turing-testnet",
    "11155111",  # Ethereum Sepolia
    "84532",     # Base Sepolia
    "80002",     # Polygon Amoy
    "421614",    # Arbitrum Sepolia
    "560048",    # Ethereum Hoodi
    "5042002",   # Arc Testnet
    "46630",     # Robinhood Chain Testnet
    "42431",     # Tempo Testnet
    "984",       # OPN Chain Testnet
    "688689",    # Pharos Atlantic Testnet
    "14853",     # Humanode Testnet 5
    "945",       # Subtensor EVM Testnet
    "11142220",  # Celo Sepolia Testnet
    "1336",      # Kii Testnet Oro
    "20994",     # Fluent Testnet
    "267",       # Neura Testnet
    "91342",     # GIWA Sepolia Testnet
    "1952",      # X Layer Testnet
    "420420417", # Polkadot Testnet
    "80094",     # Berachain bArtio Testnet
    "33139",     # ApeChain Testnet
    "60808",     # BOB Testnet
}

# Web research results: genesis hash -> identified chain name + status
WEB_RESEARCH = {
    # From SubWallet ChainInfo.json
    "0x742a2ca70c2fda6cee4f8df98d64c4c670a052d9568058982dad9d5a7a135c5b": ("Edgeware", "ACTIVE mainnet"),
    "0xd611f22d291c5b7b69f1e105cca03352984c344c4421977efaa4cbdd1834e2aa": ("Mangata X", "ACTIVE mainnet"),
    "0x6811a339673c9daa897944dcdac99c6e2939cc88245ed21951a0a3c9a2be75bc": ("Picasso", "INACTIVE"),
    "0xd43540ba6d3eb4897c28a77d48cb5b729fea37603cbbfc7a86a73b72adb3be8d": ("Khala", "INACTIVE"),
    "0xe61a41c53f5dcd0beb09df93b34402aada44cb05117b71059cce40a2723a4e97": ("Parallel", "INACTIVE"),
    "0x411f057b9107718c9624d6aa4a3f23c1653898297f3d4d529d9bb6511a39dd21": ("KILT Spiritnet", "ACTIVE mainnet"),
    "0x9226d527cd7fb37ea0f466e06182c3c5f330f3f522799cb8cc17e0a080b49a2d": ("Gen6 Public Chain", "ACTIVE mainnet"),
    "0x3920bcb4960a1eef5580cd5367ff3f430eef052774f78468852f7b9cb39f8a3c": ("Polkadex", "ACTIVE mainnet"),
    # From DuckDuckGo + Dwellir RPC Docs
    "0xb3db41421702df9a7fcac62abc82e18b6e5b39b6e17a0d352a50c24d0637c0e9": ("Bittensor", "ACTIVE mainnet"),
    # From chainid.network
    # 747474 = katana (likely dev/test chain)
}

# Unknown EVM chain IDs (NOT found in chainid.network's 2570 chains)
UNKNOWN_EVM_IDS = {"1281", "10778", "42101", "6252", "1212385660403083"}

# ---- Analysis ----
found_in_slim = []
testnets_excluded = []
missing_mainnets = []
inactive_chains = []
unknown_entries = []
duplicates = []  # entries pointing to same chain already in slim via different identifier

def find_in_slim(entry):
    """Try to match entry against slim chaindata by id, genesis hash, or EVM chain ID."""
    e = entry.lower()

    # Direct ID match
    if e in slim_ids:
        return slim_ids[e]

    # custom- prefix genesis hash match
    if e.startswith("custom-"):
        gh = e[7:]  # strip "custom-"
        if gh in slim_genesis:
            return slim_genesis[gh]

    # Genesis hash match (0x prefix)
    if e.startswith("0x") and len(e) == 66:
        if e in slim_genesis:
            return slim_genesis[e]

    # EVM chain ID match (numeric)
    if e.isdigit():
        if e in slim_evm:
            return slim_evm[e]

    # Also try uppercase "Bittensor" -> "bittensor"
    return None

for entry in user_entries:
    match = find_in_slim(entry)

    if match:
        found_in_slim.append((entry, match["id"], match["name"]))
    elif entry.lower() in {t.lower() for t in KNOWN_TESTNETS} or entry in KNOWN_TESTNETS:
        testnets_excluded.append(entry)
    else:
        # Check web research for genesis hashes
        e = entry.lower()
        gh = e[7:] if e.startswith("custom-") else e
        if gh in WEB_RESEARCH:
            name, status = WEB_RESEARCH[gh]
            if "INACTIVE" in status:
                inactive_chains.append((entry, name, status))
            else:
                missing_mainnets.append((entry, name, status))
        elif entry in UNKNOWN_EVM_IDS:
            unknown_entries.append((entry, "Unknown EVM chain (not in chainid.network)"))
        elif entry == "747474":
            testnets_excluded.append(entry)  # katana = dev chain
        else:
            unknown_entries.append((entry, "Unidentified"))

# ---- Report ----
print("=" * 80)
print("FINAL COMPREHENSIVE REPORT: User's Networks vs chaindata-v9-slim.json")
print("=" * 80)
print(f"\nTotal entries from user: {len(user_entries)}")
print(f"Slim chaindata has: {len(slim_networks)} networks")

print(f"\n{'=' * 80}")
print(f"1. FOUND IN SLIM ({len(found_in_slim)} entries)")
print(f"{'=' * 80}")
for entry, sid, name in sorted(found_in_slim, key=lambda x: x[1]):
    print(f"  {entry:>30} => {sid} ({name})")

print(f"\n{'=' * 80}")
print(f"2. TESTNETS EXCLUDED ({len(testnets_excluded)} entries)")
print(f"{'=' * 80}")
for entry in sorted(testnets_excluded):
    print(f"  {entry}")

print(f"\n{'=' * 80}")
print(f"3. IDENTIFIED MAINNETS MISSING FROM SLIM ({len(missing_mainnets)} entries)")
print(f"{'=' * 80}")
for entry, name, status in sorted(missing_mainnets, key=lambda x: x[1]):
    print(f"  {entry:>30} => {name} [{status}]")

print(f"\n{'=' * 80}")
print(f"4. IDENTIFIED BUT INACTIVE/DEAD CHAINS ({len(inactive_chains)} entries)")
print(f"{'=' * 80}")
for entry, name, status in sorted(inactive_chains, key=lambda x: x[1]):
    print(f"  {entry:>30} => {name} [{status}]")

print(f"\n{'=' * 80}")
print(f"5. UNIDENTIFIED ENTRIES ({len(unknown_entries)} entries)")
print(f"{'=' * 80}")
for entry, note in sorted(unknown_entries, key=lambda x: x[0]):
    print(f"  {entry:>30} => {note}")

print(f"\n{'=' * 80}")
print("SUMMARY")
print(f"{'=' * 80}")
print(f"  Found in slim:              {len(found_in_slim)}")
print(f"  Testnets (excluded):        {len(testnets_excluded)}")
print(f"  Mainnets to add:            {len(missing_mainnets)}")
print(f"  Inactive/dead chains:       {len(inactive_chains)}")
print(f"  Unidentified:               {len(unknown_entries)}")
print(f"  TOTAL:                      {len(found_in_slim) + len(testnets_excluded) + len(missing_mainnets) + len(inactive_chains) + len(unknown_entries)}")
