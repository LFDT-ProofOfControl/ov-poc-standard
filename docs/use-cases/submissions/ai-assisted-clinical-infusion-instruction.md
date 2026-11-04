---
industry: healthcare
use_case: An AI clinical agent prepares an infusion instruction that must be separately accepted and exactly matched before a pump controller can actuate.
submission_type: scenario
claimed_tier: 4
threats:
  - memory-poisoning
  - rag-weakness
  - unsafe-actuation
  - improper-output-handling
  - misinformation
  - context-blind-authorization
  - identity-abuse
  - evidence-repudiation
---

# AI-assisted clinical instruction bound to infusion-pump actuation

> *Illustrative, hypothetical scenario for calibration. Not necessarily
> indicative of any specific organization's current state.*

## Scenario

An oncology service uses an AI clinical agent to assemble a proposed infusion
instruction from the patient's electronic health record, current laboratory
results, allergies, pharmacy data and a retrieved treatment protocol. The
proposal identifies the patient, medicine, concentration, total dose, rate,
route, timing and monitoring conditions.

The inputs are not inherently trustworthy merely because they are available to
the agent. A copied-forward clinical note can contain a wrong weight, a memory
entry can be contaminated, retrieval can select an obsolete protocol, and the
agent can generate a plausible but incorrect calculation.

The agent is allowed to propose and transport the instruction. It cannot give
the instruction accepted clinical status. The healthcare organisation defines
the required acceptance conditions, such as a currently authorised prescriber,
pharmacy verification, patient-and-encounter match, and acceptance of one exact
instruction digest. The organisation performs that acceptance, and the accepted
state is preserved independently of the clinical agent, EHR interface and pump
vendor.

The pump controller treats that evidence as an input, not as a substitute for
its own action control. Before loading or changing the infusion parameters, it
verifies the exact instruction digest, patient and device identifiers, current
authority, validity window, allowed operating envelope, policy version and
replay state. The actuation request and its evidence are committed together. A
missing, stale, mismatched or replayed condition leaves the pump state unchanged.

The protected Tier 4 action is the controller's configuration of the infusion.
Clinical judgment, organisational acceptance and the patient's physiological
response remain separate propositions.

## Claimed tier: Tier 4

The actuation boundary is fail-closed. No in-scope interface can change the
protected infusion parameters without successfully verifying and durably
recording evidence bound to the exact instruction, patient, device and current
state. The controller enforces the boundary outside the agent's operating
environment, so disabling an agent-side log cannot authorize the change.

The Tier 4 claim does not say that the accepted instruction is clinically
correct. It says the controller cannot perform the protected actuation unless
the declared, exact and current conditions are satisfied and evidenced.

## Why not one tier down?

At Tier 3, the hospital or an external verifier could confirm that retained
records were authentic and that a recorded configuration matched an instruction.
The pump could still be configured through an uninstrumented maintenance path,
local keypad, emergency override or vendor interface without generating the
same evidence.

**Reversibility.** Once medicine has entered the patient, rollback cannot restore
the prior biological state. Detecting a wrong or unauthorised configuration after
delivery is not an adequate remedy.

**Completeness.** Tier 3 can show that visible configuration records were not
altered, but silence does not show that no other configuration occurred. Tier 4
requires every protected write path, including emergency use within the declared
scope, to generate the evidence or refuse the state change. Any bypass path must
be disclosed as outside the claim; if it can mutate the same protected state,
the Tier 4 claim is not met.

## Tier by domain

| Domain | Tier | Why |
|---|---|---|
| Provenance | 3 | Patient inputs, retrieved protocol, model version, pharmacy verification and instruction digest are linked in records whose integrity and linkage can be verified with published tooling. The lineage does not establish that a value or protocol is clinically correct. |
| Privacy | 3 | Evidence can disclose only the minimum identifiers needed for verification, with selective disclosure and auditable boundary crossings. The healthcare and credential issuers remain disclosed trust roots. |
| Portability | 3 | The exact instruction and evidence bindings cross the EHR, pharmacy, acceptance mechanism and pump controller in a schema-defined form independent of one vendor's account. |
| Authorization | 4 | The controller refuses to change protected parameters unless authority, scope, patient, device, exact accepted instruction, policy, current state and freshness all match. |
| Identity | 3 | Prescriber, pharmacist, agent, device and controller actions are cryptographically attributable under disclosed credential and revocation assumptions. |
| Security | 3 | Controller integrity and enforcement are supported by verifiable configuration and attestation evidence, while hardware, firmware and provisioning roots remain disclosed assumptions. |

## Threats exercised

| Threat | What it looks like here |
|---|---|
| `memory-poisoning` | A contaminated or incorrectly copied-forward clinical memory entry changes the weight, allergy, prior reaction or dose context used by the agent. |
| `rag-weakness` | Retrieval selects an obsolete protocol, the wrong cancer regimen or a superficially similar dosing table. |
| `unsafe-actuation` | The controller loads a dose, concentration or rate outside the instruction and permitted device envelope. |
| `improper-output-handling` | Free-form generated text is parsed into pump parameters without a typed, range-checked and exact binding to the accepted instruction. |
| `misinformation` | The agent invents a laboratory value, contraindication assessment or dose calculation that appears clinically plausible. |
| `context-blind-authorization` | A valid prescriber or pharmacy approval for one patient, encounter, medicine or time window is reused for another. |
| `identity-abuse` | An agent or user presents another clinician's credential or an invalid delegation to obtain acceptance or actuation. |
| `evidence-repudiation` | After an adverse event, parties dispute which exact instruction acquired accepted status and which parameters the controller applied. |

## What Proof-of-Control does not verify here

Proof-of-Control does not determine whether the diagnosis, protocol, medicine,
dose, rate or monitoring plan is clinically appropriate. It does not establish
that a patient record is true, that retrieved guidance is current, or that a
clinician and pharmacist exercised sound judgment. It cannot turn a validly
sourced but misleading note into safe clinical information.

It does not itself perform organisational acceptance. The organisation defines
and performs that status transition. Proof-of-Control can require evidence of
that separately protected transition as an actuation condition and verify the
binding to the exact instruction, without claiming that authorization to actuate
and acceptance of the clinical instruction are the same event.

It also does not establish that the medicine reached the intended vein, that the
pump's physical delivery matched its command, or that the patient experienced
the intended outcome. Sensor calibration, bedside controls, pharmacovigilance and
clinical accountability remain necessary.

## Residual trust assumptions to disclose

- Credential issuance, key custody, revocation and authority data for the
  prescriber, pharmacist, agent, device and controller.
- The organisation's acceptance policy and authority register, including who
  can alter them and how the accepted instruction is bound to exact bytes.
- The EHR, laboratory and pharmacy systems as issuers of input data; their
  signatures establish source, not clinical truth.
- Protocol publishers, retrieval indexes and update processes, including how a
  withdrawn or superseded protocol becomes unusable.
- The full inventory of pump-configuration paths, emergency modes and service
  credentials. A path capable of changing protected parameters outside the
  verifier defeats completeness.
- Pump hardware, firmware, secure boot, attestation and sensor-calibration roots,
  plus the evidence store outside the agent operator's control, canonicalization, monitors and recovery
  procedure.

## Notes / open questions

- The scenario separates proposed instruction, accepted organisational state,
  controller authorization, physical actuation and clinical outcome. Should the
  standard recommend linked evidence objects for all five while preserving the
  different propositions each supports?
- `unsafe-actuation` expressly leaves the soundness of an in-envelope action out
  of scope. This example shows why an acceptance boundary may be required without
  treating acceptance as evidence of clinical correctness.
- See [issue #166](https://github.com/LFDT-ProofOfControl/ov-poc-standard/issues/166)
  for the organisational-acceptance distinction.
- Submitted by Justin Roberts (GitHub @Sasine-ai), sasine.ai™.

