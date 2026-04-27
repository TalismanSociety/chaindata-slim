# Chaindata Slim

A curated, lightweight version of [Talisman's chaindata-v9.json](https://github.com/TalismanSociety/chaindata) optimised for wallet applications that need fast load times without sacrificing coverage of the most important networks and tokens.

## Approach

The original `chaindata-v9.json` (12.8 MB, 1 713 networks, 23 829 tokens) contains every network and token Talisman has ever indexed — including defunct chains, testnets, and thousands of low-activity tokens that most users will never interact with. The slim version applies a three-stage reduction pipeline:

1. **Network filtering** — All 650 testnets are removed. The remaining mainnets are evaluated against current TVL, on-chain activity, and ecosystem relevance (April 2026). Only ~232 active mainnets are retained, organised into Tier 1 (major chains with significant TVL/users) and Tier 2 (active chains with moderate activity). All Bittensor mainnet networks are preserved unconditionally.

2. **Token reduction** — The ~20 000 tokens on kept networks are reduced to a maximum of 1 000 by prioritising three categories in order: (a) all Bittensor mainnet tokens including subnet dTAO tokens, (b) the native token of every retained network, and (c) tokens whose CoinGecko ID matches the top ~500 cryptocurrencies by market capitalisation. Ten critical tokens that fall outside the top-1 000 cut are injected afterwards: USDC on six major EVM chains (Ethereum, Optimism, Arbitrum, Base, BSC, Polygon), Wrapped SOL on Ethereum, and three Hydration DeFi tokens (AAVE, tBTC, USDT).

3. **`isDefault` curation** — The `isDefault` flag is reset across all entries and then selectively re-applied: the top 10 Polkadot/Kusama ecosystem chains by importance (Polkadot, Kusama, Asset Hub, Moonbeam, Astar, Hydration, Acala, Bifrost, Mythos, Moonriver), plus 7 major EVM chains (Ethereum, Optimism, BSC, Polygon, Arbitrum, Base, Sonic), Solana, and both Bittensor networks are marked as default. For tokens, all Bittensor and native tokens are default; Ethereum gets up to 15 top tokens (stablecoins, wrapped assets, DeFi blue-chips); every other chain — including Polkadot parachains — gets a maximum of 5 default tokens (native + up to 4 curated extras chosen by market cap and ecosystem relevance).

## Comparison

| Metric            | Original |   Slim | Removed | % Removed |
| ----------------- | -------: | -----: | ------: | --------: |
| **Networks**      |    1 713 |    232 |   1 481 |     86.5% |
| **Tokens**        |   23 829 |  1 010 |  22 819 |     95.8% |
| **MiniMetadatas** |      819 |    546 |     273 |     33.3% |
| **File size**     |  12.8 MB | 1.4 MB | 11.4 MB |     89.1% |

### `isDefault` flags

| Metric               | Original | Slim |
| -------------------- | -------: | ---: |
| **Default networks** |       95 |   20 |
| **Default tokens**   |    3 047 |  430 |

### Slim breakdown

| Category                             |                                              Count |
| ------------------------------------ | -------------------------------------------------: |
| Total networks                       |                                                232 |
| Total tokens                         |                                              1 010 |
| Bittensor tokens (subnets + wrapped) |                                                149 |
| Native tokens                        |                                                232 |
| Top market-cap tokens                |                                                629 |
| USDC default chains                  |    7 (ETH, ARB, OP, Base, BSC, Polygon, Etherlink) |
| USDT default chains                  |                    5 (ETH, OP, Polygon, Astar, Hydration) |

## Default networks (20)

### Polkadot ecosystem (11)

| Network            | ID                   |
| ------------------ | -------------------- |
| Polkadot           | `polkadot`           |
| Kusama             | `kusama`             |
| Polkadot Asset Hub | `polkadot-asset-hub` |
| Moonbeam           | `moonbeam`           |
| Moonriver          | `moonriver`          |
| Astar              | `astar`              |
| Acala              | `acala`              |
| Bifrost Polkadot   | `bifrost-polkadot`   |
| Hydration          | `hydradx`            |
| Mythos             | `mythos`             |
| Bittensor          | `bittensor`          |

### EVM (8)

| Network             | ID      |
| ------------------- | ------- |
| Ethereum Mainnet    | `1`     |
| Optimism            | `10`    |
| Binance Smart Chain | `56`    |
| Polygon             | `137`   |
| Arbitrum One        | `42161` |
| Base                | `8453`  |
| Sonic Mainnet       | `146`   |
| Bittensor EVM       | `964`   |

### Solana (1)

| Network        | ID               |
| -------------- | ---------------- |
| Solana Mainnet | `solana-mainnet` |

## Scripts

All processing scripts live in `scripts/`:

| Script            | Purpose                                                                             |
| ----------------- | ----------------------------------------------------------------------------------- |
| `slim_filter.py`  | Stage 1 — removes testnets and irrelevant mainnets, filters tokens to kept networks |
| `slim_tokens.py`  | Stage 2 — reduces tokens to max 1 000 by market-cap priority                        |
| `fix_defaults.py` | Stage 3 — curates `isDefault` flags and injects 10 missing critical tokens          |
| `minify.py`       | Generates `chaindata-v9-slim.min.json` (whitespace-stripped)                         |

Run the full pipeline:

```sh
python3 scripts/slim_filter.py && python3 scripts/slim_tokens.py && python3 scripts/fix_defaults.py && python3 scripts/minify.py
```

The pipeline is idempotent — re-running it from a clean `chaindata-v9.json` always produces the same output.
