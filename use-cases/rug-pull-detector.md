# USE CASE 3: Rug Pull Detector Agent

> Illustrative, hypothetical scenario for calibration. Not necessarily indicative of any specific organization's current state.

**industry:** defi-retail / token-launchpad
**use_case:** On-demand rug pull risk assessment for a token contract - combines behavioral prediction with a 10-module security audit and returns a risk score (0–100) with flagged signals.
**submission_type:** Scenario
**claimed_tier:** Tier 3
**threats:** training-data-poisoning, audit-tampering, supply-chain-poisoned-tools, identity-and-privilege-abuse


## Scenario

A retail investor is about to buy a newly launched token on PancakeSwap. They submit the contract address to the Rug Pull Detector before purchasing. The agent runs `predictive_rug_pull` (behavioral prediction trained on a proprietary curated dataset of labeled blockchain addresses) and `run_token_audit` (10-module audit: honeypot, LP lock, mint authority, ownership renouncement, proxy, buy/sell tax, and four others). Within 60 seconds, the investor receives a risk score, a risk tier (SAFE / CAUTION / HIGH RISK / CRITICAL), and a list of flagged signals. If the agent can be manipulated - if a fraudulent token creator can suppress a CRITICAL score - an investor loses funds to a preventable rug.

The Rug Pull Detector is ChainAware's most-used product, live in production and callable via the REST API (swagger.chainaware.ai) and MCP server (prediction.mcp.chainaware.ai).

The system achieves 90% prediction accuracy before rug completion, validated against CryptoScam DB (public dataset, independently verifiable).


## Claimed tier: Tier 3

Audit modules query publicly verifiable on-chain contract state (honeypot simulation, LP lock registry, mint authority flag). The fraud detection model is trained on a proprietary curated dataset of labeled addresses (ChainAware IP), validated against 4 years of real-world fraud patterns. The delivered report is short hash hashed. Any verifier can re-run the on-chain queries independently and check the hash matches.

**Why not Tier 2?** A third-party auditor attesting to the model's design cannot verify a specific token's score was not suppressed at query time by a compromised operator.

**Why not Tier 4?** The risk score is advisory. The purchase transaction is not gated on-chain by the PoC report. Tier 4 would require a smart contract to verify the PoC report before allowing a buy - a possible future extension.


## Verifiability Tier by domain

| Domain | Tier | Why |
|---|---|---|
| Provenance | 3 | Audit module results (honeypot, LP lock, etc.) are derived from public on-chain contract state. Any verifier can re-query the contract. The fraud detection model is trained on a proprietary curated dataset of labeled addresses maintained as ChainAware IP. |
| Privacy | 2 | The token contract is public. The investor's wallet address is not processed. No privacy concern applies to the subject of the query. Tier 2 is correct - privacy is not a risk domain here. |
| Portability | 3 | Supported across ETH, BSC, Base, Polygon. Each chain's contract state is independently verifiable on that chain. |
| Authorization | 2 | The agent is invoked by an end user. No privileged authorization is required or exercised beyond reading public contract state. |
| Identity | 2 | The token contract address is the identity anchor. The investor is anonymous. Identity is not a risk domain here. |
| Security | 3 | 90% prediction accuracy before rug completion, validated against CryptoScam DB. Deliverable hash is short hash of the full report JSON. |


## Threats exercised

| Threat | What it looks like here |
|---|---|
| training-data-poisoning | A bad actor could deploy contracts designed to look safe to the training corpus, then rug after accumulating positions. Historical on-chain data is immutable; new poisoning attempts require real on-chain activity that is itself detectable. Four years of rug pull, honeypot, address poisoning, and impersonator data provides a broad baseline that is hard to evade without detectable on-chain footprints. |
| audit-tampering | A token creator could want to suppress or alter an audit result. On-chain contract state is immutable and independently verifiable. |
| supply-chain-poisoned-tools | The honeypot simulation tool could be targeted by a contract designed to fool the simulator. This is a known attack surface; the 10-module audit provides redundant signals. |
| identity-and-privilege-abuse | A malicious operator could attempt to whitelist specific contract addresses from scoring. The on-chain verifiability of audit module results is the defense. |


## What Proof-of-Control does not verify here

- Whether the predictive model's 90% accuracy holds for novel fraud patterns not represented in its proprietary training dataset.
- Whether the investor acted on the report.
- Flash rugs occurring within the 15–30 minute window before the audit completes.
- Whether the LP lock registry used is complete (some lock protocols may not be indexed).


## Residual trust assumptions

- ChainAware's proprietary labeled address dataset is accurately maintained. A dataset error would affect the behavioral prediction but not the on-chain audit modules.
- Honeypot simulation accuracy depends on the simulator version. Simulator version is not currently included in the deliverable hash.


