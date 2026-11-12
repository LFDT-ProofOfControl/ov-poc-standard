# USE CASE 1: AML Investigation Agent

> Illustrative, hypothetical scenario for calibration. Not necessarily indicative of any specific organization's current state.

**industry:** defi-compliance / blockchain-aml
**use_case:** On-demand AML screening of a wallet - traces transaction hops, scores contamination, checks AML flags and OFAC sanctions, and returns a tamper-evident investigation report without exposing the wallet owner's identity.
**submission_type:** Scenario
**claimed_tier:** Tier 3
**threats:** identity-and-privilege-abuse, sensitive-data-exfiltration, audit-tampering, context-blind-authorization, undisclosed-ai


## Scenario

A DeFi lending platform receives a borrow request from wallet `0xA1...`. Before approving, a compliance officer instructs an AML investigation agent to screen the wallet. The agent traces the wallet's transaction history across up to five hops, checks each intermediate address against 25.1M scored addresses, checks AML flags derived from ChainAware's behavioral database, queries OFAC in real time, and returns a contamination score with a full hop-by-hop evidence chain. The lending decision is made within 90 seconds. If verification is weak - if a fraudulent operator could alter the hop trace or suppress an OFAC hit - the platform unknowingly lends to a sanctioned counterparty.

ChainAware's AML Investigation agent is live and callable via the production REST API (swagger.chainaware.ai).


## Claimed tier: Tier 3

The investigation agent calls ChainAware's FastAPI service, which reads from a MariaDB database populated by on-chain event indexers. Every hop in the trace is sourced from public blockchain transaction history (Etherscan, with a Redis 30-minute TTL). The contamination score and OFAC result are computed at query time against publicly verifiable on-chain data, and the full report is short hash hashed before delivery. Any counterparty can re-derive the same hop trace from the public blockchain and verify the hash matches the delivered report. The operator cannot alter a submitted transaction's on-chain record.

**Why not Tier 2?** A third-party auditor attesting to the system's design cannot prevent a compromised operator from suppressing a specific OFAC hit at query time. Only independently re-derivable evidence closes that gap.

**Why not Tier 4?** The lending decision executes off-chain. Proof-of-Control does not enforce the decision - it produces the evidence the decision was made on. Tier 4 self-enforcement would require the loan contract to verify the PoC report on-chain before disbursement; that is not the current deployment.


## Verifiability Tier by domain

| Domain | Tier | Why |
|---|---|---|
| Provenance | 3 | Every hop sourced from public blockchain history. Transaction hashes are immutable on-chain; the operator cannot alter them. Any verifier can independently re-derive the hop chain. |
| Privacy | 3 | 25.1M addresses are scored pseudonymously - no KYC data is required or stored. The contamination score is computed from on-chain behavioral patterns only. The wallet owner's real-world identity is never an input or output. |
| Portability | 3 | Evidence spans ETH, BSC, Base, and Polygon in a single investigation. Cross-chain hop traces are sourced from each chain's public record independently. |
| Authorization | 2 | OFAC real-time check is operator-run via API. The operator cannot fabricate an on-chain transaction, but could in principle suppress or delay an OFAC query. AML flags from ChainAware's own database are independently derivable from on-chain data; OFAC completeness is not. Tier 3 for Authorization would require the OFAC check to be verifiable by a third party independently of the operator. |
| Identity | 3 | Wallet address is the only identity anchor. No real-world identity is linked. The pseudonymous model is intentional and consistent with on-chain AML practice. |
| Security | 3 | 95% fraud prediction accuracy validated against CryptoScam DB (public dataset). Report delivered as short hash hash of the full JSON - tamper-evident, operator-independent. |


## Threats exercised

| Threat | What it looks like here |
|---|---|
| identity-and-privilege-abuse | A compromised operator might inject a fake "clean" hop to shield a sanctioned wallet. The on-chain hop derivation is independently verifiable and closes this gap. |
| sensitive-data-exfiltration | The agent processes wallet transaction history that, in aggregate, could reveal a user's financial behavior. Pseudonymous scoring without identity linkage is the mitigation. |
| audit-tampering | An operator under regulatory pressure might want to alter the investigation record. The short hash deliverable hash and on-chain derivability prevent silent alteration. |
| context-blind-authorization | The agent scores contamination at the address level, not the user level. If the user switches wallets, the new wallet starts with a clean score - the agent cannot see cross-wallet linkage. |
| undisclosed-ai | The lending platform's end users are not informed that an AI agent screened their wallet. This is a consent and disclosure gap the standard should consider. |


## What Proof-of-Control does not verify here

- Whether the contamination scoring algorithm is fair or accurate for all wallet types. PoC verifies the evidence is tamper-evident; it does not validate the scoring model.
- Whether the OFAC query returned a complete and current sanctions list. PoC cannot verify the completeness of a sanctions database response. AML flags from ChainAware's behavioral database are independently verifiable; OFAC completeness is a residual dependency.
- Whether the lending decision maker acted on the PoC report or overrode it. PoC produces evidence for the decision; it does not enforce the decision.
- Whether cross-wallet linkage (same user, different addresses) is detected. The agent operates at the address level only.


## Residual trust assumptions

- ChainAware's MariaDB is assumed to reflect accurate on-chain indexing. An indexer bug could produce incorrect hop data not detectable from the delivered hash alone.
- The 30-minute Redis TTL on Etherscan data means very recent transactions (< 30 minutes old) may not appear in the trace.
- OFAC query depends on OFAC's data availability and update cadence. AML flags from ChainAware's behavioral database are operator-controlled and independently derivable from on-chain data.


