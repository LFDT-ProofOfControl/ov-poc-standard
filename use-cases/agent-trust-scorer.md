# USE CASE 5: Agent Trust Scorer (ERC-8004)

> Illustrative, hypothetical scenario for calibration. Not necessarily indicative of any specific organization's current state.

**industry:** ai-agent-marketplace / defi-automation
**use_case:** Continuous trust scoring for on-chain AI agent addresses - derives ERC-8004-compliant trust scores (0–1000) from behavioral on-chain data, detects owner anomalies, feeder manipulation, and agent farm patterns.
**submission_type:** Scenario
**claimed_tier:** Tier 3
**threats:** sybil-attack, identity-and-privilege-abuse, rogue-agent-behavioral-drift, marketplace-reputation-manipulation


## Scenario

A DeFi protocol allows AI agents to execute trades on behalf of users. Before granting an agent execution rights, the protocol queries the Agent Trust Scorer for the agent's wallet address. The scorer returns an ERC-8004 trust score, an owner risk assessment, a feeder wallet analysis, and a farm detection flag. The protocol uses scores above 700 as a threshold for autonomous execution rights; agents below 700 require a human co-signer. If trust scores can be gamed - if a malicious agent operator can manufacture a high score through fake activity - the protocol grants execution rights to a rogue agent.

ChainAware publishes weekly ERC-8004 Agent Trust Score updates. 1,587,689 ERC-8004 registered agents have been trust-scored to date (+14.2% this month) across Base, BNB Chain, Ethereum, Arbitrum, Polygon, Avalanche, Optimism, and Mantle. 1,406,358 distinct owners are tracked; 137,867 carry high-risk flags.


## Claimed tier: Tier 3

Trust scores are derived from on-chain behavioral data: the agent's own transaction history, its owner wallet's history, its feeder wallet patterns, and cross-agent farm detection. All source data is public on-chain. Weekly score updates are published openly. Any verifier can independently assess an agent's on-chain activity and check it against the published score.

This directly addresses the standard's Layer 7 open problem: "Full manipulation resistance of ranking algorithms is a Research-level open problem." ChainAware's position: scoring against 25.1M real wallets using a proprietary labeled address dataset is Sybil-resistant by construction. A fake agent cannot manufacture a genuine on-chain history that evades detection across rug pull, honeypot, address poisoning, and impersonator patterns. This is not a complete solution to algorithmic manipulation, but it moves the feasibility rating from Research toward Emerging for identity-based reputation systems.

**Why not Tier 2?** A static auditor attesting to the scoring system cannot prevent a malicious operator from suppressing a specific agent's score at query time.

**Why not Tier 4?** The trust score is advisory. Protocol execution rights are granted off-chain (or by an on-chain check the protocol controls). Tier 4 would require the execution smart contract to verify the ERC-8004 score on-chain before allowing the agent to act - a natural next step in the architecture.


## Verifiability Tier by domain

| Domain | Tier | Why |
|---|---|---|
| Provenance | 3 | Agent behavioral history sourced from public on-chain transaction data. Any verifier can inspect the agent wallet's history. |
| Privacy | 2 | Agent wallets are public by design. No privacy concern applies. |
| Portability | 3 | Scoring covers BSC and ETH. Cross-chain agent patterns are independently verifiable on each chain. |
| Authorization | 3 | ERC-8004 on-chain registration binds the trust score to the agent's registered identity. The registration transaction is publicly verifiable. The score update is tied to the agent's on-chain address. |
| Identity | 3 | ERC-8004 on-chain agent identity. The agent's address, owner, and registered metadata are publicly verifiable on-chain. |
| Security | 3 | Farm detection, feeder analysis, and owner risk scoring are all derived from public on-chain behavioral data. Weekly published scores are openly verifiable. |


## Threats exercised

| Threat | What it looks like here |
|---|---|
| sybil-attack | An agent farm operator deploys many agent wallets to accumulate collectively high reputations. Feeder wallet analysis and farm detection address this - agents sharing feeder patterns are flagged as correlated. Fresh farm wallets score low by default - they lack the on-chain footprint to score as genuine across ChainAware's rug pull, honeypot, address poisoning, and impersonator detection models. |
| identity-and-privilege-abuse | A compromised operator could attempt to inflate a specific agent's trust score. On-chain derivability of the behavioral data is the defense. |
| rogue-agent-behavioral-drift | An agent with a historically high trust score begins behaving anomalously. Weekly score updates detect behavioral drift. Sudden score drops trigger re-evaluation before the next protocol interaction. |
| marketplace-reputation-manipulation | An agent marketplace operator could game listing rankings by suppressing low-scoring agents. Published weekly scores are operator-independent - any verifier can cross-check marketplace rankings against the public score data. |


## What Proof-of-Control does not verify here

- Whether the trust scoring algorithm correctly weights all relevant behavioral signals. PoC verifies the evidence is tamper-evident; it does not validate the algorithm.
- Whether a high trust score means the agent will behave correctly in the future. Past behavioral data is the signal; future behavior is not guaranteed.
- Cross-chain agent identity linkage (same operator, different chain addresses).
- Whether the ERC-8004 registry contract itself has been compromised.


## Residual trust assumptions

- ChainAware's weekly score computation is accurately derived from on-chain indexing.
- The ERC-8004 contract on BSC/ETH has not been exploited or paused.
- Weekly cadence means intra-week behavioral changes are not reflected until the next update cycle.


