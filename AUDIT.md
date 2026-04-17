# chaindata-v9.json Audit — April 2026

## Overview

| Metric         | Value  |
| -------------- | ------ |
| Total networks | 1,713  |
| Testnets       | 650    |
| Mainnets       | 1,063  |
| Total tokens   | 23,829 |

Sources: [CoinGecko](https://www.coingecko.com), [DeFiLlama](https://defillama.com/chains)

---

## Network Relevance

### By tier (mainnets only)

| Tier                    | Description                                                                                         | Count | % of Mainnets |
| ----------------------- | --------------------------------------------------------------------------------------------------- | ----- | ------------- |
| **1 — Major**           | High TVL, large user base (ETH, BSC, Polygon, Arbitrum, Base, Solana, Polkadot, Kusama, etc.)       | ~50   | 4.7%          |
| **2 — Active**          | Moderate TVL/activity — L2s, parachains, newer chains (Monad, Berachain, Lens, Scroll, Linea, etc.) | ~185  | 17.4%         |
| **3 — Marginal**        | Minimal TVL/activity but technically alive (Harmony, Canto, Oasis, Nautilus, etc.)                  | ~95   | 8.9%          |
| **4 — Dead/irrelevant** | Abandoned, no users, defunct, or unknown micro-chains                                               | ~733  | 69.0%         |

### Summary

| Scope                               | Relevant       | Irrelevant       |
| ----------------------------------- | -------------- | ---------------- |
| Mainnets only (1,063)               | **~330 (31%)** | **~733 (69%)**   |
| All networks incl. testnets (1,713) | **~330 (19%)** | **~1,383 (81%)** |

### Examples of dead/irrelevant mainnets in the file

Expanse Network (deactivated on CoinGecko), GoChain, ThaiChain, ThaiChain 2.0, Ubiq, Metadium, Garizon Stage 0–3, SoterOne, Hoo Smart Chain, Nova Network, PrimusChain, GeneChain, IDChain, SecureChain, Zyx, SwissDLT, CamDL, DaVinci, Diode Prenet, ELA-DID-Sidechain, SUR Blockchain, High Performance Blockchain, EgonCoin, BPX Chain, VirBiCoin, Coinbit, Dehvo, Fuse Sparknet, Defi Oracle Meta, Eteria, JITO Public Network, Roburna, OTC, CO2e Chain, ENI, Seele, FileFileGo, firachain, WowChain, Structx, SiriusNet V2, BlockEx, OPN Chain, ChooChain, and hundreds more.

---

## Token Relevance

### By chain status

| Category                                     | Count   | % of 23,829 |
| -------------------------------------------- | ------- | ----------- |
| On relevant chains (Tier 1–3) + CoinGecko ID | ~20,800 | **87%**     |
| On relevant chains (all, incl. unlisted)     | ~21,450 | 90%         |
| On dead/irrelevant chains                    | ~1,225  | 5%          |
| On testnets                                  | ~1,156  | 5%          |

### Estimated real-world relevance

Tokens are heavily concentrated on major chains — Ethereum alone accounts for the majority of entries. While ~87% have CoinGecko tracking, many of those are dead memecoins, rugged projects, or zero-volume tokens.

| Measure                                      | Estimate    |
| -------------------------------------------- | ----------- |
| Tokens on active chains with market tracking | **~87%**    |
| Tokens with meaningful activity/volume       | **~50–60%** |
| Clearly irrelevant (dead chains + testnets)  | **~10%**    |

---

## Platform Breakdown (mainnets)

| Platform           | Count |
| ------------------ | ----- |
| EVM (ethereum)     | 976   |
| Polkadot/Substrate | 86    |
| Solana             | 1     |

---

## Key Findings

1. **~69% of mainnets are dead weight.** The file lists 1,063 mainnets but only ~330 have any meaningful activity, TVL, or user base as of April 2026. The long tail is dominated by obscure, abandoned, or never-launched chains.

2. **Testnets add further bloat.** 650 testnets (38% of all entries) are irrelevant to end users. Goerli, for instance, was deprecated years ago.

3. **Tokens are better curated.** ~90% of tokens live on relevant chains, and ~87% have CoinGecko market tracking. The token list is far cleaner than the network list.

4. **EVM chains dominate.** 976 of 1,063 mainnets are EVM-based. Polkadot ecosystem accounts for 86. Only 1 Solana entry.

5. **380 of 1,063 mainnets have a native token CoinGecko ID** — the other 683 mainnets don't even have a tracked native token, which is a strong signal of irrelevance.

---

## Recommendations

- Remove or archive dead mainnets with no TVL, no users, and no CoinGecko-listed native token (~700 candidates)
- Remove deprecated testnets (Goerli, Ropsten, Rinkeby, etc.)
- Flag marginal Tier 3 chains for periodic review
- Consider pruning tokens on dead chains (~1,225 entries)
- Add a `status` or `active` field to networks for programmatic filtering
