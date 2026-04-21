# Pop Networks & Tokens Analysis

Cross-reference of ~175 requested network entries against `chaindata-v9-slim.json`.

**Date:** 2025-04-21
**Branch:** `feat/pop-networks-and-tokens`
**Slim chaindata:** 236 networks (157 EVM + 79 Substrate), 1005 tokens

## Summary

| Category                    | Count   |
| --------------------------- | ------- |
| Found in slim               | 91      |
| Testnets (excluded)         | 33      |
| Mainnets missing from slim  | 11      |
| Unknown EVM chain IDs       | 5       |
| Unidentified genesis hashes | 34      |
| **Total**                   | **175** |

### Resolution of Missing Mainnets

| Chain                   | Status                                       |
| ----------------------- | -------------------------------------------- |
| Peaq                    | Already in slim (substrate)                  |
| Sora Standalone         | Already in slim (substrate)                  |
| Tanssi                  | Already in slim (substrate)                  |
| Blast (81457)           | **Added** — `isDefault: false`, ETH native   |
| HyperEVM (999)          | **Added** — `isDefault: false`, HYPE native  |
| Humanode Mainnet (5234) | **Added** — `isDefault: false`, eHMND native |
| Plasma Mainnet (9745)   | **Added** — `isDefault: false`, XPL native   |
| VFlow (1408)            | **Added** — `isDefault: false`, VFY native   |
| Crust Mainnet           | **Not in chaindata-v9.json** (see below)     |
| Gen6 Public Chain       | **Not in chaindata-v9.json** (see below)     |
| Polkadex                | **Not in chaindata-v9.json** (see below)     |

### Chains Not Found in chaindata-v9.json

The following 3 substrate chains were identified via SubWallet but have **no entry** in `chaindata-v9.json` (neither by genesis hash nor by name). They cannot be added without manual chain data.

| Chain             | Genesis Hash                                                         | SubWallet ID          |
| ----------------- | -------------------------------------------------------------------- | --------------------- |
| Crust Mainnet     | `0x8b404e7ed8789d813982b9cb4c8b664c05b3fbf433309f603af014ec9ce56a8c` | `crust_mainnet`       |
| Gen6 Public Chain | `0x9226d527cd7fb37ea0f466e06182c3c5f330f3f522799cb8cc17e0a080b49a2d` | (active in SubWallet) |
| Polkadex          | `0x3920bcb4960a1eef5580cd5367ff3f430eef052774f78468852f7b9cb39f8a3c` | (active in SubWallet) |

**Note:** `crust-parachain` exists in the full chaindata but has a different genesis hash (`0x4319cc49...`) — it is the Crust parachain, not the standalone Crust Mainnet.

---

## 1. Found in Slim (91)

These entries are already present in `chaindata-v9-slim.json`.

### EVM Networks (37)

| Entry  | Slim Name             |
| ------ | --------------------- |
| 1      | Ethereum Mainnet      |
| 10     | Optimism              |
| 56     | Binance Smart Chain   |
| 100    | Gnosis                |
| 130    | Unichain              |
| 137    | Polygon               |
| 143    | Monad                 |
| 146    | Sonic Mainnet         |
| 169    | Manta Pacific Mainnet |
| 232    | Lens                  |
| 324    | zkSync Mainnet        |
| 592    | Astar                 |
| 787    | Acala                 |
| 964    | Bittensor EVM         |
| 1284   | Moonbeam              |
| 1285   | Moonriver             |
| 1625   | Gravity Alpha Mainnet |
| 1868   | Soneium               |
| 2020   | Ronin                 |
| 2043   | NeuroWeb              |
| 3338   | peaq                  |
| 4326   | MegaETH               |
| 6283   | LAOS                  |
| 8453   | Base                  |
| 33139  | ApeChain              |
| 42161  | Arbitrum One          |
| 42220  | Celo Mainnet          |
| 43114  | Avalanche C-Chain     |
| 46     | Darwinia              |
| 55244  | Superposition         |
| 57073  | Ink                   |
| 59144  | Linea                 |
| 60808  | BOB                   |
| 80094  | Berachain             |
| 98866  | Plume Mainnet         |
| 222222 | Hydration EVM         |
| 534352 | Scroll                |

### Substrate Networks (54)

| Entry                | Slim Name            |
| -------------------- | -------------------- |
| acala                | Acala                |
| acurast              | Acurast Canary       |
| acurast-polkadot     | Acurast              |
| ajuna                | Ajuna                |
| altair               | Altair               |
| analog-timechain     | Analog Timechain     |
| astar                | Astar                |
| autonomys            | Autonomys            |
| avail                | Avail                |
| basilisk             | Basilisk             |
| bifrost-kusama       | Bifrost Kusama       |
| bifrost-polkadot     | Bifrost Polkadot     |
| bittensor            | Bittensor            |
| Bittensor            | Bittensor            |
| centrifuge-polkadot  | Centrifuge           |
| chainx               | ChainX               |
| enjin-relay          | Enjin                |
| ewx                  | Energy Web X         |
| humanode             | Humanode             |
| hydradx              | Hydration            |
| hyperbridge-polkadot | Hyperbridge          |
| interlay             | Interlay             |
| joystream            | Joystream            |
| karura               | Karura               |
| kintsugi             | Kintsugi             |
| kusama               | Kusama               |
| kusama-asset-hub     | Kusama Asset Hub     |
| laos                 | LAOS                 |
| liberland            | Liberland            |
| manta                | Manta                |
| moonbeam             | Moonbeam             |
| moonriver            | Moonriver            |
| mythos               | Mythos               |
| neuroweb             | NeuroWeb             |
| pendulum             | Pendulum             |
| polkadot             | Polkadot             |
| polkadot-asset-hub   | Polkadot Asset Hub   |
| polkadot-bridge-hub  | Polkadot Bridge Hub  |
| polkadot-collectives | Polkadot Collectives |
| polkadot-coretime    | Polkadot Coretime    |
| polkadot-people      | Polkadot People      |
| robonomics-kusama    | Robonomics Kusama    |
| shiden-kusama        | Shiden               |
| ternoa               | Ternoa               |
| unique               | Unique               |
| vara                 | Vara                 |
| xode-polkadot        | Xode                 |
| xxnetwork            | XX Network           |
| zeitgeist            | Zeitgeist            |
| zkverify             | zkVerify             |

### Matched via genesis hash / custom ID (5, duplicates of above)

| Entry                          | Slim Match       |
| ------------------------------ | ---------------- |
| `0x4b5f95ee...` (genesis hash) | acurast-polkadot |
| `0x5a51e04b...` (genesis hash) | ewx              |
| `0x50dd5d20...` (genesis hash) | xxnetwork        |
| `custom-0x6bd89e05...`         | liberland        |

---

## 2. Testnets Excluded (33)

These were identified as testnets and excluded from consideration.

### By name/convention (29)

```
avail-turing-testnet
bittensor-testnet
enjin-matrixchain-testnet
paseo-asset-hub
paseo-testnet
shibuya-testnet
vara-testnet
westend-asset-hub-testnet
westend-testnet
```

### By EVM chain ID (20 numeric testnets)

```
267, 945, 984, 1336, 1952, 5042002, 11142220, 11155111, 14853,
20994, 42431, 46630, 80002, 84532, 91342, 421614, 420420417,
560048, 688689, 747474
```

Notable: `747474` = Katana (dev/test chain)

### Newly identified as testnets (4)

| Entry               | Chain                   | Source                                                 |
| ------------------- | ----------------------- | ------------------------------------------------------ |
| `97`                | BNB Smart Chain Testnet | Full chaindata (`isTestnet: true`)                     |
| `1287`              | Moonbase Alpha          | Full chaindata (`isTestnet: true`)                     |
| `0x15b34a3b7443...` | Bifrost Testnet         | SubWallet (`bifrost_testnet`)                          |
| `0xddb89973361a...` | Shibuya Testnet         | SubWallet (`shibuya`) — duplicate of `shibuya-testnet` |

---

## 3. Mainnets Missing from Slim (11 unique chains)

These are identified mainnet chains that should be considered for addition.

| Entry                           | Chain                      | Type      | Source                              |
| ------------------------------- | -------------------------- | --------- | ----------------------------------- |
| `peaq` / `custom-0xd2a5d385...` | **Peaq**                   | Substrate | Full chaindata (id: `peaq`)         |
| `sora-standalone`               | **Sora Standalone**        | Substrate | Full chaindata                      |
| `tanssi`                        | **Tanssi**                 | Substrate | Full chaindata                      |
| `81457`                         | **Blast**                  | EVM       | Full chaindata + chainid.network    |
| `999`                           | **HyperEVM**               | EVM       | Full chaindata                      |
| `5234`                          | **Humanode Mainnet** (EVM) | EVM       | Full chaindata                      |
| `9745`                          | **Plasma Mainnet**         | EVM       | Full chaindata                      |
| `1408`                          | **VFlow**                  | EVM       | Full chaindata                      |
| `0x8b404e7ed878...`             | **Crust Mainnet**          | Substrate | SubWallet (`crust_mainnet`, ACTIVE) |
| `custom-0x9226d527...`          | **Gen6 Public Chain**      | Substrate | SubWallet (ACTIVE)                  |
| `0x3920bcb4960a...`             | **Polkadex**               | Substrate | SubWallet (ACTIVE)                  |

---

## 4. Unknown EVM Chain IDs (5)

Not found in chainid.network (2570+ chains), full chaindata (1713 networks), or any other registry.

| Chain ID           | Notes                                                    |
| ------------------ | -------------------------------------------------------- |
| `1281`             | Not in any registry                                      |
| `6252`             | Not in any registry                                      |
| `10778`            | Not in any registry                                      |
| `42101`            | Not in any registry                                      |
| `1212385660403083` | Unusually large chain ID — likely a custom/private chain |

---

## 5. Unidentified Genesis Hashes (34)

Not found in any checked source:

- Talisman `chaindata-v9.json` (1713 networks)
- SubWallet `ChainInfo.json` (228 genesis hashes)
- `@polkadot/networks` genesis registry (81 hashes)
- DuckDuckGo web search

These are likely very niche Substrate chains, defunct/sunset chains, or custom deployments.

```
0x2bd1a2aa5c768692550e5d34e2a7ec295125239a7b7795e9fd8ee31a599ccc85
0x35eadc576f10dac447f3f0a41443fa75b545c0b85473e118a30b0fe2d41832c1
0x38e8c158d58662ea7d9919a589906a1a440ac25f5c1f084dbc3b113ff0c09446
0x424f8764bb498528c41fa22ba4b9fcb890ac318e55b12309e256555b163b03cf
0x432e176a6b0aa7ece9d4a884a1866219672e27dce777e4f2651cb6b18675e235
0x452496f50c9201c4b21ac57100eb471e1ebf763f498351d93f5dfe3602def643
0x5388faf792c5232566d21493929b32c1f20a9c2b03e95615eefec2aa26d64b73
0x5884733732ab5a115ae82e0b45491e994c731326d937af1f6960ec58efad0316
0x5e37bab89576bc4e8a6419bdd044cb0d21d8284031688f5252f45c211b8744bc
0x607eb79a6afc998768feeede697e21aef1fdf3565e8df2a9cb09daa64932c724
0x6684b23d3020601285a1bf165dedf84bd6f04dc33fbcd95de6128bd284feee74
0x68af83b70cd2ada556e6a5ea29de3d397e0966a7a07525bd1c7d90ad03a64d38
0x6a525eb1cd3e76c04c8c637022f12d28d05875f8726b8d231ba923209d755de5
0x7327427af12ba1875a69e4024c724388aacd40e971dc31cff3839d4941618e10
0x744960c32e3a3df5440e1ecd4d34096f1ce2230d7016a5ada8a765d5a622b4ea
0x767cfb547500ee59b6116207bc33a2be780503233930bf7df6cc7d40c4000fed
0x897c91bdab20cf6c6e5c3499ed11b75284f567e5b91871f1a0a37e7956a10ca9
0x8b1cd0beeefb3760767de217697fbaa6152c0a1033f5f0d5b3eb46da39ee044c
0x8c3f75eb85807968bfcc316629bdfe4c778b91cf67e25ad6a75bbb4bc8bd313d
0x97dc37ed537bfa3a740757e02c7a466503908364b1a359d8d5f9cb44def0deac
0xa8c96b5526aa6f845650f8f6eeaf701779cac543b8c512baa22cc721adf03a5a
0xb0a6fadc9efc64e10efe816d9a403c886011a2e69d326657953a5d1921081f8e
0xbd924b8b2c4d3d16b22a4281c018fab8b9f4bcd1cebcfb5232837232ebfac0dd
0xc005581011570331f99e4071ab491cacae17553e0c8e17e6302ae1eebf89fdf4
0xc04fce5f049432a987c2288bfa9c99889387f35e944d545e31e894fa0fc0d1fc
0xc806038cc1d06766f23074ade7c5511326be41646deabc259970ff280c82a464
0xd0a2c75ad080394edaaa9cd1c766b543478efb415db1b6cd7772536c9a413167
0xd282ee1b23d5ae92e4550e1501b0160b5ee771015c58af715cb0949839e1fa58
0xdb27fa0ebc235bad916ca832023a261ba2e062da07c27605c0cb751647ab2070
0xdc6df9fa7aa108741193e54c0b15ba647ba09e165e59f801459e6519997bee03
0xe5212ad89524946253f5017927e78b016beb3d66203cafa67e99223e80b034a2
0xe6c30d6e148f250b887105237bcaa5cb9f16dd203bf7b5b9d4f1da7387cb86ec
0xee971a91ef92d733d86d3acc67a6394caa105f37a7757155f623bc5d0c4b690f
0xeebb5d05763801e54d6a7a60a4b7998ac125c4d050dcec418dd07ea959a54464
```

---

## 6. Networks & Tokens Added to Slim

The following 5 EVM networks and their native tokens were added to `chaindata-v9-slim.json` from `chaindata-v9.json`. All networks have `isDefault: false`, all native tokens have `isDefault: true`.

| Network ID | Network Name     | Native Token ID    | Symbol | Decimals | CoinGecko ID  |
| ---------- | ---------------- | ------------------ | ------ | -------- | ------------- |
| `81457`    | Blast            | `81457:evm-native` | ETH    | 18       | `ethereum`    |
| `999`      | HyperEVM         | `999:evm-native`   | HYPE   | 18       | `hyperliquid` |
| `5234`     | Humanode Mainnet | `5234:evm-native`  | eHMND  | 18       | `humanode`    |
| `9745`     | Plasma Mainnet   | `9745:evm-native`  | XPL    | 18       | `plasma`      |
| `1408`     | VFlow            | `1408:evm-native`  | VFY    | 18       | `zkverify`    |

**3 substrate chains already present** (no changes needed): `peaq`, `sora-standalone`, `tanssi`

**3 substrate chains could not be added** (not in `chaindata-v9.json`): Crust Mainnet, Gen6 Public Chain, Polkadex — see [Chains Not Found](#chains-not-found-in-chaindata-v9json) above.

**Updated slim stats:** 236 networks, 1005 tokens.

---

## Data Sources

| Source                  | Records            | URL / Path                                                                      |
| ----------------------- | ------------------ | ------------------------------------------------------------------------------- |
| Talisman slim chaindata | 236 networks       | `chaindata/chaindata-v9-slim.json`                                              |
| Talisman full chaindata | 1713 networks      | `chaindata/chaindata-v9.json`                                                   |
| chainid.network         | 2570+ EVM chains   | `https://chainid.network/chains_mini.json`                                      |
| SubWallet ChainInfo     | 228 genesis hashes | `Koniverse/SubWallet-ChainList` → `packages/chain-list/src/data/ChainInfo.json` |
| polkadot-js/common      | 81 genesis hashes  | `polkadot-js/common` → `packages/networks/src/defaults/genesis.ts`              |
