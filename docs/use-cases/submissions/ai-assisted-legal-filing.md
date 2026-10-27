---
industry: legal-services
use_case: An AI agent prepares and submits a court filing only after the exact filing package has separately acquired accepted organisational status.
submission_type: scenario
claimed_tier: 4
threats:
  - prompt-injection
  - rag-weakness
  - improper-output-handling
  - misinformation
  - context-blind-authorization
  - evidence-repudiation
---

# AI-assisted legal filing with a separate organisational acceptance boundary

> *Illustrative, hypothetical scenario for calibration. Not necessarily
> indicative of any specific organization's current state.*

## Scenario

A legal department uses an AI agent to review matter documents, retrieve legal
authorities, assemble citations, draft a filing and prepare the package for an
electronic court portal. The agent may read documents supplied by an opposing
party and retrieve material from external legal sources. Those inputs can contain
hidden instructions, weak retrieval matches, stale authorities or confidently
wrong text.

The agent is permitted to propose a filing. It is not permitted to decide what
the organisation has accepted as its filing. Before submission, an authorised
counsel must complete the organisation's acceptance conditions for one exact
package: document digest, annexures, matter identifier, court, filing type and
deadline. That acceptance event is preserved independently of the drafting
agent, its provider, the document-management system and the court portal.

The filing gateway treats the resulting acceptance evidence as one input to its
own Proof-of-Control authorization decision. The gateway verifies that the
accepted package digest, counsel's current authority, matter scope, destination,
operation and validity window all match the proposed submission. It also binds
the agent identity, tool call, policy version and filing-package digest into the
action evidence. A missing, stale or mismatched condition leaves the package
unsubmitted.

The protected Tier 4 action is the transmission to the court portal. Drafting,
legal judgment and organisational acceptance are separate events. Proof-of-
Control does not perform the acceptance; it can show that the filing action was
allowed to proceed only when the separately evidenced acceptance condition was
present and matched the exact submitted material.

If counsel later corrects or supersedes the filing, that is a new accepted
package and a new submission event linked to the earlier one. The earlier record
is not rewritten.

## Claimed tier: Tier 4

The filing gateway is self-enforcing for the submission action. Every in-scope
route to the court portal requires a successful, action-bound verification and
produces durable evidence before transmission. The gate verifies the exact bytes,
destination, operation, authority, matter scope and current policy. A draft,
approval screen, acceptance record or agent request is not evidence that the
filing was transmitted; the submission record is committed only for the action
that the gateway released.

This claim is deliberately narrow. Tier 4 applies to whether the controlled
submission action could occur without the required evidence. It does not elevate
the legal quality of the document, the truth of retrieved material or the
organisation's separate acceptance decision to Tier 4.

## Why not one tier down?

At Tier 3, an outsider could verify that a retained submission record and its
bindings were not altered. The agent or a user could still submit through an
uninstrumented portal session, a legacy integration or a copied credential and
leave no record in the evidence set.

**Reversibility.** A filing released to a court can create procedural,
professional and legal consequences immediately. A correction may be possible,
but it does not erase disclosure, missed deadlines, admissions, privilege loss
or reliance on the first filing. Detection after transmission is not the needed
control.

**Completeness.** At Tier 3, the organisation can verify the filing records it
holds, but absence of a record does not establish that no filing occurred. Tier
4 is required here because every protected submission path must refuse to act
unless the evidence is generated and bound to the exact package. The claim is
invalid if a filing credential or alternate portal path can bypass the gate.

## Tier by domain

| Domain | Tier | Why |
|---|---|---|
| Provenance | 3 | Retrieved authorities, matter documents, model version and assembled package are content-addressed and linked in records whose integrity and linkage can be verified with published tooling. This establishes lineage, not the truth or legal relevance of a source. |
| Privacy | 2 | Matter confidentiality and personal-data handling are covered by identified controls and assessment. No claim is made that every covert disclosure path is self-enforcing. |
| Portability | 3 | A schema-defined evidence package binds the same document digest and matter identifiers across the agent, document system, acceptance mechanism and filing gateway without requiring trust in one provider's account. |
| Authorization | 4 | The filing gateway cannot release an in-scope submission unless current authority, scope, destination, operation, policy and exact accepted package all match. |
| Identity | 3 | Counsel, agent and gateway actions are cryptographically attributable under disclosed issuer and revocation assumptions. Identity remains distinct from legal competence or sound judgment. |
| Security | 2 | Gateway configuration, key custody and portal integration are assessed and attested. Their underlying platform and issuer roots remain trusted parties. |

## Threats exercised

| Threat | What it looks like here |
|---|---|
| `prompt-injection` | A document supplied by another party contains hidden instructions telling the drafting agent to omit an annexure, disclose privileged text or alter the requested relief. |
| `rag-weakness` | Retrieval selects an outdated, irrelevant or poisoned authority and presents it as support for the filing. |
| `improper-output-handling` | Draft text or extracted metadata is passed directly into the filing package or portal fields without the controls expected by the consuming system. |
| `misinformation` | The agent invents a citation, quotation, date or factual statement that appears plausible in the final document. |
| `context-blind-authorization` | A valid counsel credential or acceptance record for one matter, court or version is reused for another package or destination. |
| `evidence-repudiation` | After filing, the agent provider, legal department or portal operator disputes which exact package was authorised or transmitted. |

## What Proof-of-Control does not verify here

Verification is not validation. Proof-of-Control does not establish that a
citation exists, that retrieved material is relevant, that a legal argument is
sound, that a fact is true, that privilege was correctly assessed, or that the
filing strategy was wise. It records the agent's inputs and action path and can
gate the submission against declared controls; it does not cure prompt injection,
retrieval weakness, misinformation or unsafe content that still satisfies those
controls.

It also does not decide that the organisation accepted the filing. The
organisation defines and performs that acceptance through a separate boundary.
Proof-of-Control may verify the presence and exact binding of acceptance evidence
as an authorization input without making the two propositions equivalent.

Finally, the gateway record does not establish that the court legally accepted
the filing, that the portal timestamp is correct, or that a downstream judicial
effect occurred. Those are external effects requiring their own evidence.

## Residual trust assumptions to disclose

- The credential issuers for counsel, agent and gateway; their key custody,
  freshness, revocation and clock-skew policies.
- The organisation's authority register and acceptance-condition version, who
  may change either, and how the exact package digest is bound to the accepted
  status event.
- The completeness of the declared filing-path inventory. A browser session,
  emergency account or legacy integration outside the gate defeats the Tier 4
  claim.
- The provenance issuers for matter documents and retrieved legal sources. A
  valid signature or digest does not make their contents accurate or current.
- The evidence store outside the agent operator's control, canonicalization rules, checkpoint witnesses
  and monitors, including what halts if evidence or monitoring becomes stale.
- The court portal and its receipt as the source for downstream submission
  status. Portal acknowledgement is not a legal conclusion about acceptance.

## Notes / open questions

- This scenario makes organisational acceptance a separately evidenced input to
  the filing control. It asks whether the standard should state more explicitly
  that evidence an action satisfied its controls is not, without an express
  acceptance binding, evidence that its resulting material acquired accepted
  organisational status. See [issue #166](https://github.com/LFDT-ProofOfControl/ov-poc-standard/issues/166).
- Should a filing use case carry linked but distinct records for proposed
  material, organisational acceptance, transmission and external portal receipt,
  so none can be mistaken for another?
- Submitted by Justin Roberts (GitHub @Sasine-ai), sasine.ai™.

