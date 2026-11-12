# USE CASE 7: DeFi Credit Scorer Agent

> Illustrative, hypothetical scenario for calibration. Not necessarily indicative of any specific organization's current state.

**industry:** defi-lending
**use_case:** On-demand on-chain credit scoring for a wallet address - produces a credit score and tier for undercollateralized DeFi lending decisions, using behavioral history across DeFi protocols.
**submission_type:** Scenario
**claimed_tier:** Tier 3
**threats:** context-blind-authorization, identity-and-privilege-abuse, sensitive-data-exfiltration


## Scenario

SmartCredit.io, a DeFi lending platform, receives a loan application from wallet `0xC3...` for an undercollateralized position. Before approving, the platform calls the DeFi Credit Scorer. The agent returns a credit score (0–1000) and credit tier (PRIME / NEAR-PRIME / SUBPRIME / NO-HISTORY), derived from the wallet's on-chain DeFi activity: repayment history, liquidation events, protocol diversity, position sizes, and behavioral risk signals. If the credit score can be manipulated, the platform extends credit to a high-risk wallet and suffers a loss.

SmartCredit.io is a live deployment. The credit scoring system powers real lending decisions in production.


## Claimed tier: Tier 3

Credit scores are derived from public on-chain DeFi activity. Repayment and liquidation events are recorded on-chain by lending protocols (Aave, Compound, etc.) and are publicly verifiable. The score computation uses behavioral signals from ChainAware's fraud detection model, trained on a proprietary curated dataset of labeled addresses. The delivered score is short hash hashed. Any verifier can independently assess the wallet's on-chain DeFi history and check the behavioral signals.


## Verifiability Tier by domain

| Domain | Tier | Why |
|---|---|---|
| Provenance | 3 | Repayment history, liquidation events, and protocol activity are on-chain and publicly verifiable. Any verifier can independently inspect the wallet's DeFi history. |
| Privacy | 3 | Credit scoring is pseudonymous - wallet address only, no KYC. The score reveals DeFi financial behavior without linking to real-world identity. This is the core privacy design: creditworthiness proven without identity disclosure. |
| Portability | 3 | DeFi activity spans ETH, BSC, and Polygon. Cross-chain credit history is aggregated from each chain's public record independently. |
| Authorization | 3 | The lending platform's loan approval is explicitly conditioned on the credit score. The delegation chain (user requests loan → platform calls credit scorer → platform approves/rejects) is recorded in the platform's on-chain transaction log. |
| Identity | 3 | Wallet address is the sole identity anchor. Pseudonymous by design - matching the privacy design of DeFi lending. |
| Security | 3 | Behavioral model accuracy validated against historical DeFi repayment data (SmartCredit.io production deployment). Deliverable hash short hash of full score JSON. |


## Threats exercised

| Threat | What it looks like here |
|---|---|
| context-blind-authorization | The credit score reflects past behavior, not future intent. A wallet with a high score could behave differently on the specific loan requested (e.g., borrow-and-bridge to avoid repayment). |
| identity-and-privilege-abuse | A compromised operator could suppress a negative credit signal for a targeted borrower. On-chain derivability of the DeFi activity record is the defense. |
| sensitive-data-exfiltration | DeFi activity patterns reveal financial behavior. Pseudonymous scoring without identity linkage is the mitigation. |


## What Proof-of-Control does not verify here

- Whether the credit scoring algorithm correctly weights all DeFi protocols. Under-indexed protocols produce credit gaps.
- Whether the borrower's intent matches their historical behavior (the classic credit risk problem).
- Whether the lending platform acted on the credit score or overrode it.


## Residual trust assumptions

- ChainAware's indexing of DeFi protocol events is accurate and current.
- The credit model is calibrated against SmartCredit.io's historical loan performance; generalization to other lending platforms requires recalibration.


