# USE CASE 4: Wallet Fraud Detector Agent

> Illustrative, hypothetical scenario for calibration. Not necessarily indicative of any specific organization's current state.

**industry:** defi-lending / nft-marketplace
**use_case:** On-demand behavioral fraud scoring for a wallet address - detects rug pull, honeypot, address poisoning, and impersonator patterns using a proprietary curated model, scoring across 25.1M wallets, and returns a fraud score with behavioral profile.
**submission_type:** Scenario
**claimed_tier:** Tier 3
**threats:** identity-and-privilege-abuse, sensitive-data-exfiltration, context-blind-authorization, sybil-attack


## Scenario

An NFT marketplace is about to process a high-value bid from wallet `0xB2...`. Before confirming, the marketplace calls the Wallet Fraud Detector. The agent queries ChainAware's behavioral prediction model - trained on a proprietary curated dataset of labeled addresses, with scores computed across 25.1M wallets - and returns a fraud score (0–100) and behavioral profile (experience level, risk willingness, trust score, wallet rank). The marketplace uses this to decide whether to require additional verification. If the fraud score can be manipulated, a fraud wallet passes through and the seller loses funds.

The Wallet Fraud Detector has been live in production since 2023, making it one of the longest-running behavioral fraud detection systems in DeFi.


## Claimed tier: Tier 3

Behavioral scores are derived from on-chain transaction history - the same data any party can access from public blockchain explorers. The fraud detection model is trained on a proprietary curated dataset of labeled addresses (ChainAware IP). The delivered score is short hash hashed. Any verifier can independently assess the wallet's on-chain history and check behavioral signals against the hash.

**Why not Tier 2?** A static audit cannot verify a specific wallet's score was not suppressed or adjusted for a targeted wallet at query time.


## Verifiability Tier by domain

| Domain | Tier | Why |
|---|---|---|
| Provenance | 3 | Behavioral model trained on a proprietary curated dataset of labeled addresses (ChainAware IP), detecting rug pulls, honeypots, address poisoning, and impersonators. Any verifier can inspect the scored wallet's on-chain record. |
| Privacy | 3 | 25.1M addresses scored pseudonymously. No real-world identity is linked. The score is derived purely from on-chain behavioral patterns. This directly addresses the standard's open issue on verifiable-but-unlinkable identity: fraud risk is proven without identity disclosure. |
| Portability | 3 | Supported across ETH, BSC, Base, Polygon, TON, Tron, Solana, HAQQ. Each chain's behavioral history is sourced independently. |
| Authorization | 2 | The agent is invoked by the marketplace operator. No privileged authorization is exercised beyond reading behavioral data. |
| Identity | 3 | Wallet address is the sole identity anchor. The pseudonymous model is by design - matching the standard's open question on anonymity/pseudonymity (§4, Issue 2). |
| Security | 3 | 95% fraud prediction accuracy validated against CryptoScam DB (public). Deliverable hash short hash of full report JSON. |


## Threats exercised

| Threat | What it looks like here |
|---|---|
| identity-and-privilege-abuse | A compromised operator could suppress the fraud score for a specific targeted wallet. On-chain behavioral derivability is the defense - any verifier can independently assess the wallet's history. |
| sensitive-data-exfiltration | Behavioral profiles reveal DeFi activity patterns. Pseudonymous scoring without identity linkage is the mitigation; profiles are keyed to wallet address only. |
| context-blind-authorization | The agent scores one wallet in isolation. It does not detect coordinated multi-wallet fraud campaigns where each individual wallet appears clean. |
| sybil-attack | A fraudster using many fresh wallets, each below the fraud threshold, to aggregate positions. Wallets with no prior on-chain history score differently from established wallets - detectable but not a definitive signal. |


## What Proof-of-Control does not verify here

- Whether behavioral patterns accurately predict fraud for wallets with no prior on-chain history (new wallets are scored with limited signal).
- Whether the marketplace acted on the fraud score.
- Cross-wallet coordination below individual scoring thresholds.
- Whether the behavioral model is free from demographic or geographic bias in its training data.


## Residual trust assumptions

- ChainAware's proprietary labeled address dataset is accurately maintained and reflects current fraud patterns.
- Behavioral model version at query time. Model updates are not currently included in the deliverable hash.


