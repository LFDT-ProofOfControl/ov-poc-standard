---
industry: public-sector-emergency-communications
use_case: An AI agent drafts and publishes an emergency alert only after the exact message and audience have separately acquired accepted organisational status.
submission_type: scenario
claimed_tier: 4
threats:
  - prompt-injection
  - bent-goals
  - system-prompt-leakage
  - improper-output-handling
  - coverage-decay
  - misinformation
  - evidence-repudiation
---

# AI-assisted public emergency alert across multiple publication channels

> *Illustrative, hypothetical scenario for calibration. Not necessarily
> indicative of any specific organization's current state.*

## Scenario

A municipal emergency office uses an AI communications agent to combine sensor
feeds, weather bulletins, field reports and public submissions into a proposed
emergency alert. The agent drafts the message, translations, geographic target,
audience, channels and validity period, then prepares publication across SMS,
cell broadcast, social media, the municipal website and partner feeds.

Several inputs are adversarial or uncertain. A public submission can contain a
prompt injection. A changed goal specification can quietly prioritise reputation
over public warning. The agent can hallucinate an affected location, and generated
text can expose internal instructions, unpublished vulnerabilities or personal
information when a downstream channel republishes it without validation.

The agent may propose and distribute a candidate for review. It cannot decide
which exact message becomes the municipality's accepted public representation.
An authorised emergency officer applies the organisation's acceptance conditions
to the exact content, translations, map, audience, channels and validity window.
The resulting accepted state is preserved independently of the agent, its
provider and the content-management system.

Each publication adapter is behind a common enforcement boundary. Before release,
the boundary verifies the exact accepted-message digest, authority, incident scope,
audience, channel, validity, policy and current alert state. Every protected
publication commits its action evidence before release. If a channel adapter is
added, updated or found to bypass enforcement, publication on that path is halted
until coverage is re-established and evidenced.

The protected Tier 4 action is publication. Message drafting, organisational
acceptance, external delivery and public response are distinct events.

## Claimed tier: Tier 4

The public-release boundary is self-enforcing across the declared channel set.
An adapter cannot publish unless the action is bound to the exact accepted
message and satisfies the current authorization conditions. Missing or stale
evidence, a changed digest, an undeclared channel or failed coverage verification causes
refusal rather than a warning after publication.

The claim is conditional on the disclosed channel inventory and enforcement
topology. Tier 4 does not follow merely because one gateway is fail-closed while
staff, the agent or an integration can publish the same official alert elsewhere.

## Why not one tier down?

At Tier 3, an auditor could verify the integrity of the alert records that were
captured. A compromised or newly added channel adapter could still publish an
official-looking message outside the evidence path.

**Reversibility.** A false evacuation order, omitted warning or disclosure of
sensitive operational information can cause immediate movement, panic, injury
or loss of trust. Retraction cannot make every recipient unsee or unact on the
first message.

**Completeness.** Tier 3 cannot make absence of a record mean absence of
publication. Tier 4 requires every in-scope channel to generate evidence as a
condition of release. Continuous coverage verification matters because a control that
worked when commissioned can decay when credentials, adapters, APIs or routing
change.

## Tier by domain

| Domain | Tier | Why |
|---|---|---|
| Provenance | 3 | Sensor feeds, bulletins, field reports, model version and candidate-to-final lineage are content-addressed in records whose integrity and linkage can be verified with published tooling. Source provenance does not make a report true. |
| Privacy | 2 | Redaction and audience controls are assessed and evidenced, but no claim is made that every generated disclosure or covert channel is self-enforcing. |
| Portability | 3 | One schema-defined message and evidence package carries the same digest, incident and validity data across multiple publication providers and remains verifiable after provider change. |
| Authorization | 4 | Every declared official-publication path refuses release unless authority, incident, channel, audience, exact accepted message, policy and freshness match. |
| Identity | 3 | Officer, agent and publication-adapter actions are cryptographically attributable under disclosed credential and revocation assumptions. |
| Security | 2 | Adapter configuration, key custody and service integrity are assessed and attested. Platform and credential roots remain trusted parties. |

## Threats exercised

| Threat | What it looks like here |
|---|---|
| `prompt-injection` | A public report or scraped page instructs the agent to suppress a warning, alter a location or include attacker-selected text. |
| `bent-goals` | The authorised emergency-communication objective is silently changed to minimise reputational harm or avoid acknowledging uncertainty. |
| `system-prompt-leakage` | Generated public text discloses internal instructions, response procedures, hidden channel credentials or sensitive incident context. |
| `improper-output-handling` | A channel adapter publishes free-form generated text or map data without the validation, encoding or exact-message binding expected by that channel. |
| `coverage-decay` | A new social-media API, emergency credential or website integration bypasses the boundary after the original control assessment passed. |
| `misinformation` | The agent confidently states the wrong location, severity, safe route, time or protective action. |
| `evidence-repudiation` | After the event, the municipality or a provider disputes which exact message was accepted, which channels published it, or when it was superseded. |

## What Proof-of-Control does not verify here

Proof-of-Control does not establish that an emergency exists, that a sensor or
field report is accurate, that a warning is complete, or that the message is
clear, proportionate and safe. It can evidence which sources and goal version
informed the agent and gate publication against declared controls. It does not
detect every prompt injection, judge a subtly bent objective, prevent system-
prompt leakage in otherwise permitted text, or determine whether the message is
misinformation.

It also does not decide that the municipality accepted the message. The
organisation defines and performs that acceptance. Proof-of-Control can verify
that publication required separately preserved acceptance evidence bound to the
exact message, audience and validity window, without collapsing accepted status
into authorization of the publication action.

The publication record does not establish that every intended recipient received,
understood or acted on the alert, nor that a telecom or platform rendered it
correctly. Delivery, accessibility and real-world outcome require separate
evidence and evaluation.

## Residual trust assumptions to disclose

- Credential issuers, authority data, key custody, freshness and revocation for
  emergency officers, agents and channel adapters.
- The organisation's acceptance conditions and incident-authority register,
  including who may alter them and how supersession and expiry are represented.
- The source systems and publishers behind sensor, weather and field data. Their
  signatures establish origin, not factual accuracy.
- The completeness and continuous testing of the official-channel inventory,
  including emergency, manual and third-party publication routes.
- Adapter software, platform APIs, telecom delivery receipts and provider
  attestations, with their versions and failure behavior.
- The evidence store outside the agent operator's control, canonicalization rules, checkpoint witnesses,
  monitor set and response when coverage or evidence freshness lapses.

## Notes / open questions

- `coverage-decay` raises a scope question: should a Tier 4 multi-channel claim
  require continuous evidence that every declared publication path remains behind
  the enforcement boundary, rather than only evidence that the gateway itself is
  healthy?
- A control described in policy but never wired into one adapter produces no
  evidence and no violation. No tier repairs that gap; the claim boundary must
  identify it.
- The proposed, accepted, published, delivered and superseded states should remain
  separately identifiable. See [issue #166](https://github.com/LFDT-ProofOfControl/ov-poc-standard/issues/166).
- Submitted by Justin Roberts (GitHub @Sasine-ai), sasine.ai™.

