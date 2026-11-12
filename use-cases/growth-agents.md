# USE CASE 8: Growth Agents (Personalized DeFi Onboarding)

> Illustrative, hypothetical scenario for calibration. Not necessarily indicative of any specific organization's current state.

**industry:** defi-marketing / dapp-growth
**use_case:** Continuous personalization of a DeFi dApp - detects wallet behavior at connect, derives a behavioral persona scored against 25.1M wallets using ChainAware's proprietary fraud detection model, generates personalized headlines and CTAs via LLM (Claude Haiku), and suppresses fraud-flagged wallets from incentive campaigns - all in under 100ms.
**submission_type:** Scenario
**claimed_tier:** Tier 3
**threats:** sensitive-data-exfiltration, sybil-attack, excessive-agency, undisclosed-ai, context-blind-authorization


## Scenario

SmartCredit.io deploys Growth Agents via a single JavaScript pixel. When a user connects their wallet, the pixel fires. ChainAware's behavioral prediction API derives a persona (Beginner / Intermediate / Expert, risk willingness, trust score) from the wallet's on-chain history in under 100ms. The persona and page context are passed to Claude Haiku, which generates a personalized headline and CTA. If the wallet is flagged as an airdrop farmer or Sybil wallet, it is silently excluded from reward campaigns - no personalized offer is served. The result: 8x engagement uplift and 2x conversion improvement in a 6-month production deployment at SmartCredit.io.

The key PoC contribution: this agent generates personalized content scored against 25.1M wallets using ChainAware's proprietary fraud detection model *without ever processing or exposing the wallet owner's real-world identity*. Privacy is preserved by design - the persona is a behavioral abstraction, not an identity profile.

This use case directly addresses the standard's open issue (§4, Issue 2): anonymity and pseudonymity in the Identity domain. Growth Agents prove that meaningful, high-value personalization is achievable with verifiable-but-unlinkable wallet identity - no KYC, no real-world identity linkage, no consent gap for identity disclosure.

It also directly addresses the implementer guidance: "Carrying a signal is not enforcing it." Growth Agents do not merely carry a Sybil flag - they enforce it. A flagged wallet never receives the reward offer. The enforcement is in the execution path, not the documentation.


## Claimed tier: Tier 3

Behavioral personas are derived from public on-chain data, scored against 25.1M wallets using ChainAware's proprietary fraud detection model (trained on a curated labeled address dataset, ChainAware IP). The fraud suppression decision is made at query time using the same behavioral scoring system validated against CryptoScam DB (95% accuracy). Any verifier can independently inspect a wallet's on-chain history and assess whether its behavioral signals match the persona tier assigned. The LLM-generated content (Claude Haiku) is not on-chain verifiable - it is generated at request time and not hashed. This is a known limitation; see "What PoC does not verify."

**Why not Tier 2?** A static third-party audit cannot verify that a specific Sybil wallet was correctly suppressed during a live session. The behavioral derivability from public on-chain data is what moves this to Tier 3.

**Why not Tier 4?** The personalization enforcement (showing or hiding an offer) is client-side. A technically sophisticated user could potentially bypass client-side suppression. Tier 4 would require the reward distribution to be governed by a smart contract that verifies the PoC persona report on-chain before distributing tokens.


## Verifiability Tier by domain

| Domain | Tier | Why |
|---|---|---|
| Provenance | 3 | Behavioral personas scored against 25.1M wallets using ChainAware's proprietary fraud detection model. The underlying wallet transaction data is public on-chain; any verifier can independently assess the wallet's behavioral signals against the scored output. |
| Privacy | 3 | Personalization is generated from on-chain behavioral patterns only. No real-world identity is processed or disclosed. The headline does not contain raw numbers, percentages, or wallet ranks - behavioral inference without identity exposure. This is a live production example of verifiable-but-unlinkable identity in the marketing context. |
| Portability | 3 | Supported on ETH, BNB, Base, HAQQ, Solana. Each chain's behavioral history is independently sourced. Cross-chain wallet behavior is aggregated without identity linkage across chains. |
| Authorization | 3 | Fraud suppression is enforced at execution time - a flagged wallet never receives the reward offer. This is not a documented policy that could be bypassed; it is in the execution path. The control boundary is enforced, not merely carried. |
| Identity | 3 | Wallet address is the sole identity anchor. Behavioral persona is derived without any real-world identity linkage. This is a production implementation of the pseudonymous personalization model the standard's open issue (§4, Issue 2) asks for a worked example of. |
| Security | 3 | Sybil detection and airdrop farmer suppression derived from behavioral signals validated against CryptoScam DB. 95% fraud detection accuracy in production. |


## Threats exercised

| Threat | What it looks like here |
|---|---|
| sensitive-data-exfiltration | Behavioral personas aggregate significant on-chain financial data. The mitigation: personas are keyed to wallet address only, with no real-world identity linkage. The LLM prompt never includes raw financial figures. |
| sybil-attack | Airdrop farmers deploy many fresh wallets to claim incentives. Fraud signal history requirement means fresh Sybil wallets are detectable - they lack the 4-year on-chain footprint needed to score as genuine users across rug pull, honeypot, address poisoning, and impersonator models. |
| excessive-agency | The agent generates content and suppresses wallet offers. If the suppression logic is miscalibrated, a legitimate user could be incorrectly excluded from a campaign. The 95% accuracy figure means ~5% of suppression decisions may be incorrect - a residual risk. |
| undisclosed-ai | End users are not explicitly informed that an AI agent generated their personalized headline or that their wallet was scored. The dApp operator is responsible for disclosure; Growth Agents does not enforce it. This is a gap the standard should address in the Authorization domain: consent for AI-personalized content. |
| context-blind-authorization | Pre-connect personalization uses page-behavior signals only (dwell time, page visited) - the wallet is unknown until connect. This is intentional but creates a narrow window where the agent acts without wallet-level context. |


## What Proof-of-Control does not verify here

- The LLM-generated content (headline, CTA). Claude Haiku generates text at request time; the generated output is not hashed or verifiable. PoC covers the persona derivation, not the content generation step.
- Whether the dApp operator disclosed AI personalization to end users. PoC does not enforce consent disclosure.
- Whether client-side suppression of fraud-flagged wallets was bypassed by a technically sophisticated user.
- Whether the behavioral persona correctly captures the user's current intent (a DeFi expert may be exploring a new protocol as a novice).


## Residual trust assumptions

- ChainAware's on-chain behavioral indexing is accurate and current.
- Claude Haiku's content generation is assumed to be appropriate for the persona context; content quality is not covered by PoC.
- Client-side rendering of the headline and CTA is controlled by the dApp operator, not by ChainAware.
- The 5% fraud suppression error rate means approximately 1 in 20 suppressed wallets may be a false positive.


*Submitted via: chainaware.ai@gmail.com*
*GitHub: github.com/ChainAware*
