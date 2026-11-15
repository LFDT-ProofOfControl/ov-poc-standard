# Crosswalk: CSA AARM (Autonomous Action Runtime Management)

| | |
| --- | --- |
| **Framework type** | Runtime enforcement standard (Cloud Security Alliance, contributed by Vanta) |
| **Corpus version** | 2026 publication — [access](https://cloudsecurityalliance.org/) · [corpus provenance](corpus/README.md) |
| **Relationship** | Complementary halves of agentic assurance — AARM is the enforcement half, Proof-of-Control the evidence half |
| **Coding status** | Draft seed coding, single coder — [rubric](rubric.md) |

## The Relationship

CSA's AARM defines runtime enforcement: it intercepts agent actions at the boundary and approves, modifies, defers, or denies them. Proof-of-Control defines the open, tamper-evident evidence of what the agent did. The two share the same architectural spot — the action boundary — which is why the mapping below contains exact matches precisely there (action interception, the runtime gateway) and no-matches everywhere evidence-independence begins.

| AARM (runtime enforcement) | Proof-of-Control (open evidence) |
| --- | --- | --- |
| Question | What may the agent do at the action boundary? | What did the agent actually do, and can anyone verify it? |
| When | At execution, before the action | At execution, producing evidence of the action |
| Trust | Operator-run enforcement and audit trail | Independent, tamper-evident, verifiable by others |
| Scope | Agent actions inside one deployment (the runtime gateway) | System-wide and portable, across vendors, systems, and jurisdictions |
| Certifiable? | Yes; a vendor-neutral CSA standard with a conformance regime | Yes; the standard, plus forthcoming independent certification |

Where they meet: AARM mints the tamper-evident receipt at the runtime gateway inside one deployment; Proof-of-Control carries that evidence outward and makes it openly verifiable across organizations. Enforcement decides what an agent may do; verification shows what it actually did. Prevention can fail silently; detection cannot.

## Requirement-Level Mapping

<!-- BEGIN GENERATED MAPPING (tools/generate_crosswalks.py) -->

**Coverage: 20%** of the 127 Proof-of-Control requirements (1 exact matches, 25 partial matches, 101 not covered), computed per the [mapping rubric](rubric.md) from the row-level [coding sheet](coding_sheet.csv). *Draft seed coding — pending working-group validation.* To change this table, edit the coding sheet and run `python3 tools/generate_crosswalks.py`.

**How to read the Match column** ([full rubric](rubric.md)): **Exact** — the framework has a clause equivalent in scope and intent. **Partial** — the framework covers the topic, but not with Proof-of-Control's operator-independent evidence (or not at the same depth). **None** — the framework has no analogous provision. Where a section holds a mix, the badge shows the strongest match present and the **Covered** column shows how many of its requirements are matched at all — so a section reading *Partial 3/5* has two requirements this framework does not reach.

| Section | Reqs | Covered | Match | Closest framework clause(s) | Rationale |
| --- | :---: | :---: | :---: | --- | --- |
| [C1.1 Model and Artifact Provenance](../0.1/en/0x10-C01-Provenance.md) | 5 | 0/5 | None | — | Artifact provenance outside runtime-enforcement scope |
| [C1.2 Input and Data Lineage](../0.1/en/0x10-C01-Provenance.md) | 4 | 0/4 | None | — | Outside scope |
| [C1.3 Compute Substrate Provenance](../0.1/en/0x10-C01-Provenance.md) | 2 | 0/2 | None | — | Outside scope |
| [C1.4 Privacy-Preserving Provenance](../0.1/en/0x10-C01-Provenance.md) | 2 | 0/2 | None | — | Outside scope |
| [C2.1 Data-Access Evidence](../0.1/en/0x10-C02-Privacy.md) | 3 | 1/3 | Partial | R1 Pre-execution Interception; R5 Tamper-evident Receipts | R1 intercepts every agent-initiated action, which AARM's definitions say include file writes and API calls, and R5 records the original action and a timestamp for each, but AARM requires no data-store identifier, record or object reference, or operation type in the receipt. Not reached: 2.1.2, 2.1.3. |
| [C2.2 Policy and Consent Enforcement](../0.1/en/0x10-C02-Privacy.md) | 5 | 4/5 | Partial | R3 Policy Evaluation with Intent Alignment; R4 Five Authorization Decisions; R5 Tamper-evident Receipts; R2 Context Accumulation; R3 Policy Evaluation with Intent Alignment; R5 Tamper-evident Receipts; R4 Five Authorization Decisions (MODIFY); R9 Least Privilege Enforcement (SHOULD); R3 Policy Evaluation with Intent Alignment; R5 Tamper-evident Receipts | R3 evaluates every intercepted action against policy before execution, R4 supplies DENY, and R5 records the decision, but AARM's policy is not a consent record and nothing requires one to be consulted. Not reached: 2.2.5. |
| [C2.3 Privacy-Preserving Verification Mechanisms](../0.1/en/0x10-C02-Privacy.md) | 3 | 0/3 | None | — | Cryptographic privacy mechanisms not addressed |
| [C2.4 Evidence Handling for Protected Data](../0.1/en/0x10-C02-Privacy.md) | 2 | 0/2 | None | — | Evidence-store handling not addressed |
| [C3.1 Boundary-Crossing Evidence](../0.1/en/0x10-C03-Portability.md) | 2 | 0/2 | None | — | Boundary-crossing evidence not addressed |
| [C3.2 Cross-Environment Continuity](../0.1/en/0x10-C03-Portability.md) | 3 | 0/3 | None | — | Not addressed |
| [C4.1 Authority and Scope Enforcement](../0.1/en/0x10-C04-Authorization.md) | 8 | 7/8 | Exact | R5 Tamper-evident Receipts; R9 Least Privilege Enforcement (SHOULD); R3 Policy Evaluation with Intent Alignment; R5 Tamper-evident Receipts; R1 Pre-execution Interception; R4 Five Authorization Decisions (ALLOW, DENY, MODIFY, STEP_UP, DEFER); R5 Tamper-evident Receipts; R3 Policy Evaluation with Intent Alignment; R9 Least Privilege Enforcement (SHOULD); R4 Five Authorization Decisions (STEP_UP); R5 Tamper-evident Receipts; R2 Context Accumulation; R3 Policy Evaluation with Intent Alignment | R1 stops the action before execution rather than flagging it, R4 supplies DENY as a decision, and R5 records the original action and the decision, so the block and its rejection record match in scope and specificity. Not reached: 4.1.8. |
| [C4.2 Delegation](../0.1/en/0x10-C04-Authorization.md) | 4 | 1/4 | Partial | R9 Least Privilege Enforcement (SHOULD); R5 Tamper-evident Receipts | R9 enforces credential scope at the time of action execution and R5 records the evaluation, but R9 is a SHOULD, and AARM requires no signed authorization token and no validation of its signature, expiry or audience. Not reached: 4.2.2, 4.2.3, 4.2.4. |
| [C5.1 Agent and Principal Binding](../0.1/en/0x10-C05-Identity.md) | 4 | 2/4 | Partial | R6 Identity Binding | R6 binds every receipt to the identity of the agent that initiated the action, but AARM has no principal on whose behalf the action ran, so a sampled action resolves to an agent and never to a named principal. Not reached: 5.1.3, 5.1.4. |
| [C5.2 Inter-Agent Identity](../0.1/en/0x10-C05-Identity.md) | 2 | 0/2 | None | — | Inter-agent identity not addressed |
| [C6.1 Execution Environment Integrity](../0.1/en/0x10-C06-Security.md) | 4 | 2/4 | Partial | Section 5 Conformance Criteria; R1 Pre-execution Interception; R5 Tamper-evident Receipts | Section 5 requires each conformance claim to be backed by evidence compiled for each requirement and reviewed by the AARM Technical Working Group, but the evidence is a package assembled for review, not a named evidence stream showing each declared control operating. Not reached: 6.1.3, 6.1.4. |
| [C6.2 Isolation and Confidential Execution](../0.1/en/0x10-C06-Security.md) | 3 | 0/3 | None | — | Isolation proof not addressed |
| [C6.3 Cryptographic Key Lifecycle](../0.1/en/0x10-C06-Security.md) | 5 | 0/5 | None | — | Key lifecycle not addressed |
| [C7.1 Generation at the Action Boundary](../0.1/en/0x10-C07-Evidence-Generation-and-Properties.md) | 5 | 2/5 | Partial | R1 Pre-execution Interception; R5 Tamper-evident Receipts; R6 Identity Binding | R1 forbids any action bypassing the control plane, but it is architecture-neutral and AARM section 6.2 expressly recognizes SDK instrumentation that may miss non-instrumented paths, so a gateway running out-of-process from the agent is not required. Not reached: 7.1.3, 7.1.4, 7.1.5. |
| [C7.2 The Contemporaneous Property](../0.1/en/0x10-C07-Evidence-Generation-and-Properties.md) | 4 | 1/4 | Partial | R5 Tamper-evident Receipts | R5 requires a receipt with a timestamp for every evaluated action, and AARM's abstract describes recording every action before it is executed, but AARM does not require the receipt to be written within the executing transaction or define what the timestamp marks. Not reached: 7.2.2, 7.2.3, 7.2.4. |
| [C7.3 The Tamper-Evident Property](../0.1/en/0x10-C07-Evidence-Generation-and-Properties.md) | 5 | 1/5 | Partial | R5 Tamper-evident Receipts | R5 requires each receipt to be tamper-evident and verifiable against unauthorized modification, but tamper-evidence is per receipt: AARM requires no hash chain or Merkle structure across receipts, so insertion and reordering are not detectable, and no scheduled chain verification. Not reached: 7.3.2, 7.3.3, 7.3.4, 7.3.5. |
| [C7.4 The Transparent Property](../0.1/en/0x10-C07-Evidence-Generation-and-Properties.md) | 1 | 0/1 | None | — | No trust-assumption disclosure |
| [C7.5 The Determinism Boundary](../0.1/en/0x10-C07-Evidence-Generation-and-Properties.md) | 2 | 0/2 | None | — | Not addressed |
| [C7.6 Evidence Custody and Resilience](../0.1/en/0x10-C07-Evidence-Generation-and-Properties.md) | 6 | 0/6 | None | — | AARM's failure handling is the policy decision on the agent's action; it has no requirement for alerting on, or logging, failures of the receipt pipeline itself. |
| [C7.7 The Interoperable Property](../0.1/en/0x10-C07-Evidence-Generation-and-Properties.md) | 5 | 1/5 | Partial | R5 Tamper-evident Receipts; R8 Telemetry Export (SHOULD) | R5 fixes a minimum receipt content and R8 asks for telemetry in a standard, interoperable format, but R8 is a SHOULD, and AARM v1.0 publishes no field-complete schema that a deployment's output must validate against. Not reached: 7.7.2, 7.7.3, 7.7.4, 7.7.5. |
| [C8.1 Tier Placement](../0.1/en/0x10-C08-Verifiability-Tiers.md) | 8 | 0/8 | None | — | No verifiability grading |
| [C8.2 Mechanism-to-Requirement Fit](../0.1/en/0x10-C08-Verifiability-Tiers.md) | 2 | 0/2 | None | — | No mechanism-fit rule |
| [C8.3 Chain Integrity and Self-Enforcement (Tier 4)](../0.1/en/0x10-C08-Verifiability-Tiers.md) | 5 | 0/5 | None | — | No self-enforcement concept |
| [C9.1 Locating Evidence on the System Surface](../0.1/en/0x10-C09-System-Surface-MAESTRO.md) | 3 | 0/3 | None | — | Not addressed |
| [C9.2 Layer Coverage](../0.1/en/0x10-C09-System-Surface-MAESTRO.md) | 3 | 0/3 | None | — | Not addressed |
| [C10.1 Conformance Claims](../0.1/en/0x10-C10-Conformance-and-Disclosure.md) | 8 | 2/8 | Partial | Section 5 Conformance Criteria | Section 5 has a claim name its conformance level, Core or Extended, and routes it through review by the AARM Technical Working Group, but the level grades requirements satisfied rather than how rigorously the claim was assessed. Not reached: 10.1.2, 10.1.4, 10.1.5, 10.1.6, 10.1.7, 10.1.8. |
| [C10.2 Trust-Assumption Disclosure](../0.1/en/0x10-C10-Conformance-and-Disclosure.md) | 2 | 0/2 | None | — | No trust-assumption disclosure |
| [C10.3 Continuously Monitored Operation](../0.1/en/0x10-C10-Conformance-and-Disclosure.md) | 7 | 2/7 | Partial | R5 Tamper-evident Receipts; R1 Pre-execution Interception; R5 Tamper-evident Receipts | R5 requires tamper-evident, verifiable receipts, but AARM requires no store with chain verification and no provision of verification results to an assessor. Not reached: 10.3.3, 10.3.4, 10.3.5, 10.3.6, 10.3.7. |

### Gap Analysis (what this framework does not cover)

* **C1.1 Model and Artifact Provenance** — Artifact provenance outside runtime-enforcement scope
* **C1.2 Input and Data Lineage** — Outside scope
* **C1.3 Compute Substrate Provenance** — Outside scope
* **C1.4 Privacy-Preserving Provenance** — Outside scope
* **C2.1 Data-Access Evidence** — partially reached; no provision for 2.1.2, 2.1.3: R5 requires the receipt to contain the original action and sets no limit on the data it carries, so AARM has no rule keeping protected content out of the evidence and no scan of the receipt store; T3 data exfiltration is a threat class, not a record-minimization duty.
* **C2.2 Policy and Consent Enforcement** — partially reached; no provision for 2.2.5: AARM has no deidentification requirement and no rule on re-identification by joining against restricted sources; a policy written under R3 could block such joins, but nothing in AARM requires it.
* **C2.3 Privacy-Preserving Verification Mechanisms** — Cryptographic privacy mechanisms not addressed
* **C2.4 Evidence Handling for Protected Data** — Evidence-store handling not addressed
* **C3.1 Boundary-Crossing Evidence** — Boundary-crossing evidence not addressed
* **C3.2 Cross-Environment Continuity** — Not addressed
* **C4.1 Authority and Scope Enforcement** — partially reached; no provision for 4.1.8: No AARM requirement pins approval thresholds to the original grant; R2 does the opposite by accumulating prior actions and tool output into the evaluation context, and R7 semantic distance tracking is a SHOULD aimed at intent drift rather than at authorization state.
* **C4.2 Delegation** — partially reached; no provision for 4.2.2, 4.2.3, 4.2.4: AARM v1.0 has no delegation requirement; multi-agent coordination is deferred to v2.0, and T7 cross-agent propagation is named as a threat with no requirement to validate a delegation chain back to a principal.
* **C5.1 Agent and Principal Binding** — partially reached; no provision for 5.1.3, 5.1.4: AARM has no principal and no grant issued by one, so no tool call carries a token linking it to a principal's authority.
* **C5.2 Inter-Agent Identity** — Inter-agent identity not addressed
* **C6.1 Execution Environment Integrity** — partially reached; no provision for 6.1.3, 6.1.4: AARM has no attestation of the runtime environment and no comparison against reference values.
* **C6.2 Isolation and Confidential Execution** — Isolation proof not addressed
* **C6.3 Cryptographic Key Lifecycle** — Key lifecycle not addressed
* **C7.1 Generation at the Action Boundary** — partially reached; no provision for 7.1.3, 7.1.4, 7.1.5: AARM orders interception before execution but places no ordering or durability requirement on the receipt, so evidence emission is never a precondition of action release.
* **C7.2 The Contemporaneous Property** — partially reached; no provision for 7.2.2, 7.2.3, 7.2.4: R5's timestamp is the system's own; AARM requires no timestamp authority, transparency-log inclusion or consensus time and no anchoring interval.
* **C7.3 The Tamper-Evident Property** — partially reached; no provision for 7.3.2, 7.3.3, 7.3.4, 7.3.5: AARM sets no key-custody requirement; R6 binds receipts to the agent's identity, which places the signing identity with the agent rather than with a generating mechanism the agent and operator cannot reach.
* **C7.4 The Transparent Property** — No trust-assumption disclosure
* **C7.5 The Determinism Boundary** — Not addressed
* **C7.6 Evidence Custody and Resilience** — AARM's failure handling is the policy decision on the agent's action; it has no requirement for alerting on, or logging, failures of the receipt pipeline itself.
* **C7.7 The Interoperable Property** — partially reached; no provision for 7.7.2, 7.7.3, 7.7.4, 7.7.5: Canonicalization unaddressed
* **C8.1 Tier Placement** — No verifiability grading
* **C8.2 Mechanism-to-Requirement Fit** — No mechanism-fit rule
* **C8.3 Chain Integrity and Self-Enforcement (Tier 4)** — No self-enforcement concept
* **C9.1 Locating Evidence on the System Surface** — Not addressed
* **C9.2 Layer Coverage** — Not addressed
* **C10.1 Conformance Claims** — partially reached; no provision for 10.1.2, 10.1.4, 10.1.5, 10.1.6, 10.1.7, 10.1.8: An AARM claim is to a level covering a fixed requirement set, R1 to R6 or R1 to R9, so there are no claimed domains to list and no rule on marketing for unclaimed ones.
* **C10.2 Trust-Assumption Disclosure** — No trust-assumption disclosure
* **C10.3 Continuously Monitored Operation** — partially reached; no provision for 10.3.3, 10.3.4, 10.3.5, 10.3.6, 10.3.7: AARM has no automated validator of receipts against a claimed level within a validation window.

*Coding granularity is the individual requirement; the section rows above summarize the requirements beneath them. Where a section is coded uniformly the summary is exact, and where it is mixed the Covered column and the gap list name what is missing. Row-level detail is in the [coding sheet](coding_sheet.csv). This is seed coding by a single coder and has not yet had the second-coder pass the [rubric](rubric.md) requires.*

<!-- END GENERATED MAPPING -->

---

*Proof-of-Control is stewarded by the [Advanced AI Society](https://advancedaisociety.org/) —
**[join at advancedaisociety.org](https://advancedaisociety.org/)**.*
