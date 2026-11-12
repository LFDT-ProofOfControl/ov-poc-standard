# USE CASE 6: Token Auditor Agent

> Illustrative, hypothetical scenario for calibration. Not necessarily indicative of any specific organization's current state.

**industry:** defi-retail / token-launchpad / cex-listing
**use_case:** On-demand 10-module security audit of a token contract - verifies honeypot, LP lock, mint authority, ownership renouncement, proxy patterns, buy/sell tax, and additional security modules.
**submission_type:** Scenario
**claimed_tier:** Tier 3
**threats:** supply-chain-poisoned-tools, audit-tampering, training-data-poisoning


## Scenario

A tier-2 CEX is evaluating a token for listing. The listing team submits the token contract to the Token Auditor. The agent runs 10 audit modules against the contract's on-chain state and returns pass/fail results per module, an overall verdict (SAFE / REVIEW NEEDED / HIGH RISK), and a full module-level report. The CEX requires a SAFE verdict before proceeding to commercial due diligence. If the audit can be manipulated - if a module result can be suppressed - the CEX lists a honeypot token and retail investors are harmed.

ChainAware has completed 15,008 token audits across CoinGecko and CoinMarketCap listed tokens, covering 7 chains, with 57.7% rated HIGH RISK (published case study, independently verifiable).


## Claimed tier: Tier 3

All 10 audit module results are derived from publicly verifiable on-chain contract state. Honeypot simulation calls the contract on a fork; LP lock status is queried from public lock registries; mint authority and ownership flags are read from the contract's on-chain state. Any verifier can re-run each module independently against the same contract address. The delivered audit report is short hash hashed.


## Verifiability Tier by domain

| Domain | Tier | Why |
|---|---|---|
| Provenance | 3 | All 10 modules query public on-chain contract state. Contract bytecode and storage are immutable and independently re-queryable. |
| Privacy | 2 | Token contracts are public. No private data is processed. |
| Portability | 3 | Supported across ETH, BSC, Base, Polygon, TON, Tron, Solana, HAQQ. Each chain's contract state is independently verifiable. |
| Authorization | 2 | Agent invoked by operator; reads public contract state only. No privileged access. |
| Identity | 2 | Token contract address is the identity anchor. No wallet identity is processed. |
| Security | 3 | 15,008 audits completed with published results (CoinGecko/CoinMarketCap corpus). Deliverable hash short hash of full audit report JSON. Results independently verifiable by re-running on-chain queries. |


## Threats exercised

| Threat | What it looks like here |
|---|---|
| supply-chain-poisoned-tools | A contract could be designed to fool the honeypot simulator specifically. 10-module redundancy reduces single-module bypass risk. |
| audit-tampering | A token creator could want a module result changed before the CEX sees it. On-chain contract state is immutable; module results are independently re-derivable. |
| training-data-poisoning | Not applicable - the Token Auditor uses rule-based on-chain checks, not a trained ML model. This is a strength: no training corpus to poison. |


## What Proof-of-Control does not verify here

- Whether all 10 modules are sufficient to detect novel token attack patterns.
- Whether the honeypot simulator correctly handles all proxy patterns.
- Whether LP lock registries indexed are complete (new lock protocols may not be supported).
- Whether the token's economic design is fair or sustainable (outside PoC scope).


## Residual trust assumptions

- LP lock registry indexing is current; new lock contracts require integration to be detected.
- Honeypot simulation is run on a fork at audit time; a contract with time-based behaviors may behave differently at different times.


