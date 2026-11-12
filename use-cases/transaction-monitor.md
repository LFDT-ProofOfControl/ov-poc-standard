# USE CASE 2: Transaction Monitor Agent

> Illustrative, hypothetical scenario for calibration. Not necessarily indicative of any specific organization's current state.

**industry:** defi-compliance / crypto-exchange
**use_case:** Continuous monitoring of a set of registered wallet addresses across ETH, BSC, Base, and Polygon - detects suspicious deposits, withdrawals, and behavioral changes in real time and fires alerts to the operator.
**submission_type:** Scenario
**claimed_tier:** Tier 3
**threats:** rogue-agent-behavioral-drift, audit-tampering, context-blind-authorization, excessive-agency


## Scenario

A crypto exchange registers 50,000 hot wallet addresses with the Transaction Monitor. The agent continuously scans new blocks across four chains. When a monitored address receives a deposit from a wallet scoring above the fraud threshold, or sends a withdrawal to a flagged address, the monitor fires an alert to the exchange's compliance system within seconds. The exchange uses these alerts to hold withdrawals for manual review. If the monitoring record can be silently altered - if an alert could be suppressed or a hop trace edited - the exchange is exposed to passing sanctioned funds without a compliance record.

ChainAware's Transaction Monitor is live in production. SmartCredit.io uses it for continuous deposit and withdrawal screening.


## Claimed tier: Tier 3

Block-scan data is sourced from public RPC endpoints. Each alert includes the triggering transaction hash (publicly verifiable on-chain), the fraud score of the counterparty address (derived from ChainAware's behavioral database, independently re-derivable from on-chain data), and a short hash hash of the full alert payload. Any auditor can verify the alert matches the on-chain transaction.

**Why not Tier 2?** A static third-party audit cannot verify that a specific alert was not suppressed during a live block window. The tamper-evident alert hash and on-chain transaction reference close this gap.

**Why not Tier 4?** The monitor fires alerts; it does not enforce holds. The hold decision is made by the exchange's downstream system. Tier 4 would require the hold to be enforced by a smart contract that verifies the PoC alert before allowing a withdrawal - a future architecture not yet deployed.


## Verifiability Tier by domain

| Domain | Tier | Why |
|---|---|---|
| Provenance | 3 | Every alert references a specific transaction hash on a public blockchain. The triggering event is publicly verifiable. |
| Privacy | 3 | Addresses are monitored pseudonymously. No KYC data is processed. Behavioral scores are derived from on-chain patterns only. |
| Portability | 3 | Monitoring spans ETH, BSC, Base, Polygon simultaneously. Each chain's block data is sourced independently from that chain's public record. |
| Authorization | 2 | The agent fires alerts to operator systems. The operator decides which addresses to register and can remove addresses from monitoring. This delegation is operator-controlled, not cryptographically enforced. |
| Identity | 3 | Wallet addresses are the identity anchor. ERC-8004 agent identity registration is used to identify the monitoring agent itself. |
| Security | 3 | Alert payloads are short hash hashed. Fraud scoring uses behavioral data validated against CryptoScam DB (public). |


## Threats exercised

| Threat | What it looks like here |
|---|---|
| rogue-agent-behavioral-drift | The monitoring agent's scoring thresholds could drift over time if the underlying behavioral model is updated without disclosure. Alert hash does not capture model version. |
| audit-tampering | An operator could want to delete alerts for addresses later found to be sanctioned. short hash hashing of each alert at creation time makes post-hoc deletion detectable. |
| context-blind-authorization | The monitor scores individual addresses. It does not detect coordinated behavior across a cluster of addresses acting together below individual thresholds. |
| excessive-agency | If the monitor were wired to automatically freeze funds (not the current deployment), an erroneous fraud score could cause an unauthorized freeze. The current architecture uses alerts only - a human is in the loop for action. |


## What Proof-of-Control does not verify here

- Whether all relevant transactions were captured (e.g., if an RPC endpoint missed a block). PoC verifies the evidence for transactions it did see; it cannot prove completeness of block coverage.
- Whether the fraud scoring threshold is calibrated correctly for the exchange's risk appetite.
- Whether the downstream compliance system acted on the alert.
- Coordinated behavior across multiple addresses below the individual scoring threshold.


## Residual trust assumptions

- RPC endpoint availability and accuracy per chain. A chain reorganization could produce a briefly incorrect alert.
- ChainAware's behavioral model version at the time of each alert. Model updates are not currently versioned in the alert payload.


