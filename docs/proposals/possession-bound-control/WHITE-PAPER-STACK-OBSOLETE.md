# The Standard's stack is obsolete under ENI6MA patterns

**Frank Dylan Rosario**  
**Dr. Lin Wang**  
**Dr. Octavia Sulea**

6 November 2026

Working paper for the Proof-of-Control working groups. Informative. The published draft remains the normative text under `0.1/en/`. The standard remains technology-neutral. This paper states what happens to that stack when an agent runs under ENI6MA patterns [1] [3] [5].

## Abstract

The Proof-of-Control stack is one architecture. Identity issues a durable token. Authorization checks it. The gateway releases on it. The log signs a record of it. The tier grades it. Conformance then reports that the agent has Proof-of-Control [8] [6] [7] [11].

An agent that runs under ENI6MA patterns authorizes each act with a per-act proof. One-shot burns that proof on each interactive step. Oscillation burns the same proof on each direction between two service processes. The next step, and the reply, each receive a new proof [4] [5].

Under that pattern the stack's pass and the act's authority come apart. The token can still be valid, and the record can still score Tier 3 or Tier 4, after the proof for these bytes has already been burned or has already been refused. The stack keeps describing a control plane the agent has left. That is what "obsolete" means here.

## 1. Obsolete, in plain English

**Obsolete.** A proposed control is obsolete for an agent when two facts hold at once. The act's authority is a burned per-act proof of that act's bytes. The control's pass is a record of a durable token, and that token remains presentable for a later act.

The stack stays a coherent description of token systems. For an agent on the pattern, the stack's yes and the pattern's yes answer different questions. A conformance claim that reports the stack's yes as Proof-of-Control reports the token [11] [12].

## 2. The stack the Standard proposes

The draft is ten domains plus a mechanism inventory, and the authority path is one pile [1].

| Layer | What it proposes | Authority it reads |
| --- | --- | --- |
| C5 Identity | A certificate, key pair, DID, OAuth token, JWT, verifiable credential, or capability URL, optionally inside an attested environment. Agent-to-agent messages signed by the agent's key [8]. | The durable credential issued to the agent. |
| C4 Authorization | Per-task tokens, an approval record, a path check, a signed authorization token [6]. | The same token, plus a session and an approval slip that outlive the step. |
| C7 Evidence | A gateway. A single-use capability bound to a snapshot. Evidence signed by a mechanism key [7]. | The snapshot and the capability the agent can present. |
| C6 Security | Hardware-backed keys, rotation, and a signature margin for the evidence key [16]. | The key that signs the token's record. |
| C2 Privacy | Minimized evidence [16]. | Whatever of the token the record kept. |
| C8 Tiers | Proof-of-Control only at Tier 3 or Tier 4 [11]. | The record of the layers above. |
| C9 Surface | Every fact placed on a stack map [1]. | A label for where the token evidence sits. |
| C10 Conformance | Self-declared, third-party assessed, or continuously monitored, with trust assumptions disclosed. | A grade of the token claim. |
| C3 Portability | Evidence that survives a boundary crossing. | The token record carried to the next vendor. |
| Appendix B | A menu of signatures, credentials, attestations, commitments, and zero-knowledge proofs [1]. | A filing name for the token. |
| C1 Provenance | Which model ran, and its lineage. | A different fact: the model, not the act's authority. |

C1 records model lineage. The other rows record the token, or they record a grade, a map, a filing, or a boundary crossing of the token. The binary question "does this agent have Proof-of-Control?" is answered at C8 from that pile [11]. When the pile's input is a durable token, the yes is a yes about the token.

## 3. The pattern the agent runs

**Per-act proof.** Authority for this act binds the canonical bytes of this act, a fresh nonce, and the anchored checker digest. The ledger burns the nonce before the checker accepts. The checker returns one terminal decision. The witness remains inside the protected boundary. The released record holds the challenge digest, the masked-response digest, the checker digest, and the nonce identifier [2] [5].

**One-shot (interactive step rounds).** Each interactive step is one act. The allocator reserves the step. The proof binds that step. The ledger burns the nonce before the checker accepts. The next step receives a new proof. The API protocol implements challenge, respond, validate, and ledger nonce burn. Future-time reservation and the service check of `request_hash` are in formalization [5].

**Oscillation (the same proof between two service processes).** Each direction is one one-shot act. The sender binds the message. The receiver burns the nonce before the checker accepts. The reply is a new act. The protocol marks the continuous exchange as proposed and partial [4] [5].

**Checker.** PassPlus runs the human-facing check on device: a pinned guest, a terminal decision on the bearings, a local grant when the decision is accept, enrollment sealed, Authority rows holding hashes and sealed bytes [3]. Web, extension, and iOS run that on-device path. The pattern's authority for a tool act is the burned proof. The on-device grant by itself is the ceremony decision [3].

The witness stays inside the boundary. The agent process receives the terminal decision and the burned record. It does not receive a reusable call key inside the published binary [5].

## 4. Why the pile comes apart

Each layer below uses the same three sentences.

**What the stack records.** The pass the chapter can mark from a durable token.

**What the pattern already decided.** The burned proof of these bytes, or the refusal of these bytes.

**Why the layer is obsolete.** The stack's pass remains available for a later act after the pattern has finished this one. Reporting that pass as the act's authority reinstalls the token beside the proof.

### 4.1 Identity

**What the stack records.** C5.1.2 and C5.1.3 accept the agent's credential and the delegation token. C5.1.4 accepts the same key from inside a matching measurement. C5.2 accepts the agent's signature [8].

**What the pattern already decided.** This step's proof bound these bytes and this checker, and the nonce is burned. The credential presentation sits beside that record.

**Why the layer is obsolete.** The token remains in the agent through expiry. A later step can present it and receive a C5 pass after the previous step's proof is spent. The identity chapter then names a principal for an act the pattern has already closed or has not yet proved.

### 4.2 Authorization

**What the stack records.** C4.1.5 accepts a task token. C4.1.6 accepts an approval slip. C4.2.1 accepts a signed authorization token. C4.1.7 accepts a path of upstream parameters [6].

**What the pattern already decided.** One-shot burned the interactive step. Oscillation burned this direction. The next command is a new proof.

**Why the layer is obsolete.** The session, the slip, and the path permission remain presentable. They authorize the 20-unit payment and a later amount on the same object. The pattern has already required a new burn for the later amount.

### 4.3 Gateway

**What the stack records.** C7.1.1 routes the call through a gateway. C7.1.4 releases a capability bound to a snapshot. C7.1.3 writes a before-record and then forwards [7].

**What the pattern already decided.** The ledger burned this act's nonce before the checker accepted. Release follows that decision.

**Why the layer is obsolete.** The gateway's pass is a pass on the snapshot and the capability. Both can be objects the agent composed and can present again until the capability's own lifetime ends. The pattern's burn has already ended authority for these bytes. A gateway that still forwards on the capability is enforcing the obsolete token.

### 4.4 Keys and the log

**What the stack records.** C6.3 manages the evidence-signing key. C7.3.2 keeps that key with the gateway. C2.4.1 minimizes what the row stores [7] [16].

**What the pattern already decided.** The released row holds four digests. The witness remains inside the protected boundary. The evidence-signing key signs that row and stays in its own class.

**Why the layer is obsolete.** Applied to the witness, C6.3 turns the witness into a durable signing secret, or it grades the witness as that secret. The signed log can then be perfect and still be a signed story of the token. Signature integrity of an obsolete authority is a durable copy of the obsolete authority.

### 4.5 Tiers

**What the stack records.** Tier 3 is an outsider's check of the evidence. Tier 4 is a release that follows the check. Proof-of-Control is those two tiers [11].

**What the pattern already decided.** An outsider recomputes the per-act proof from the commitment, the challenge, the masked response, and the checker digest, and the spent nonce stays spent. Tier 3 is that recomputation. Tier 4 is release after the burn.

**Why the layer is obsolete.** The draft's Tier 3 and Tier 4 grade the token record the lower layers produced. A deployment can reach the binary yes on that record while the pattern refused the act, and it can miss the binary yes while the pattern burned a valid proof the token chapter never named. The threshold stays. The artifact it grades is the obsolete one. C8's open item on "every execution interval" is the same split: the pattern's interval is the step, or the direction, and the token's interval is the expiry [11].

### 4.6 Surface, conformance, portability, inventory

**What the stack records.** C9 places the token evidence on a layer map. C10 stages who checked the token claim and names residual trust. C3 carries the token record across a vendor boundary. Appendix B files the mechanism as a signature, a credential, an attestation, a commitment, or a zero-knowledge proof [1].

**What the pattern already decided.** The act's evidence is the per-act proof. One-shot is a sequence of interactive steps. Oscillation is that proof between two service processes.

**Why the layer is obsolete.** A map, a conformance stage, a portability package, and an inventory row inherit the artifact they are given. Point them at the token and they export the token. The pattern's row is the interactive per-act proof. Filing it as a verifiable credential exports a durable token again.

### 4.7 Provenance

**What the stack records.** C1 records which model ran and the lineage of that model.

**What the pattern already decided.** The pattern decided which bytes were authorized. It records the checker digest for that decision.

**Why this layer stays a separate record.** Model lineage remains a fact about the weights. It becomes part of the obsolete pile only when a conformance claim treats a C1 pass, stacked on a C5 pass, as Proof-of-Control for the act. The act's authority stays the burned proof.

## 5. Why the whole stack goes, not one chapter

The chapters are coupled by the token.

1. C5 puts the token in the agent.
2. C4 treats the token as permission for later commands.
3. C7 releases the tool when the token's snapshot checks.
4. C6 and C2 sign and store a record of that release.
5. C8 grades the record, and the binary threshold turns the grade into Proof-of-Control.
6. C9, C10, C3, and Appendix B publish, disclose, carry, and name that grade.

Remove any one chapter and the token still enters at C5 and exits as a tier if the others remain. Add the pattern beside the stack and the token remains a second authority: the proof can burn, and the token can still pass step 2 on the next command. The agent, which holds the token at every step of section 2 of the companion paper, is the party who presents it [9].

So the stack is obsolete as a unit. An agent on the pattern that keeps the stack as its conformance story has two control planes. The live plane is the burn. The reported plane is the token. Buyers, auditors, and the next agent see the reported plane [11] [12].

## 6. What the running agent records instead

For each interactive step, and for each direction between two service processes, the record is the per-act proof:

- the canonical bytes of this act,
- the fresh nonce,
- the anchored checker digest,
- the burn before the decision,
- the four digests in the released row,
- the witness inside the protected boundary.

One-shot writes that record per step. Oscillation writes that record per direction, and the reply is a new record. A later act writes a new record. The conformance claim for those paths cites that record at Tier 3 when an outsider recomputes it, and at Tier 4 when release follows the burn [5] [11].

The construction that produces the proof is the ENI6MA / PassPlus checker: protected witness, pinned checker, burn before the decision [2] [3] [5]. Declaring "single-use" in C4 or C7 while the object remains a token leaves the stack in place.

## 7. Scope of this obsolescence

The claim covers the authority stack for agents that run the pattern on their commands and messages.

The continuous oscillation tunnel remains proposed and partial. The implemented path is one-shot challenge, respond, validate, and ledger nonce burn [5]. A party that already shares a running endpoint and its ignited allocation shares that allocation until it ends [5].

The endpoint's applied effect remains a separate record: a published mapping from the proved bytes to the effect [14] [15]. The unlinkable profile remains a separate record: a session pseudonym and an opening policy [13]. Model lineage remains the C1 record. Those records sit beside the per-act proof. They do not restore the durable token as the act's authority.

## 8. Conclusion

The Standard proposes a stack whose authority is a durable token: issued in C5, checked in C4, released in C7, signed in C6, graded in C8, and exported by C3, C9, C10, and Appendix B. An agent under ENI6MA patterns authorizes each act by a proof that is burned before acceptance. One-shot does that on every interactive step. Oscillation does that on every direction between two service processes. After the burn, the token can still pass the stack. The stack's Proof-of-Control answer is then a grade of an object the pattern has finished with. For that agent, the stack is obsolete as the control plane, and keeping it beside the pattern reinstalls the token as a second authority.

## References

[1] Advanced AI Society and the Proof-of-Control Initiative. *Open Verification: the Proof-of-Control Standard for Agents*. Working Draft v0.1. https://github.com/LFDT-ProofOfControl/ov-poc-standard. Normative files under `0.1/en/`, domains C1–C10 and Appendix B.

[2] Frank Dylan Rosario and Dr. Lin Grant Wang. *Perfect Geometric Proof of Identity*. Formal evidence preprint, 18 September 2026. Local copy: `LEAN4-PUBLISH/01-CORE-FORMAL/CORE-02-comprehensive-native-evidence/source/PERFECT_GEOMETRIC_PROOF_OF_IDENTITY.md`. The declared channel is the challenge, the masked response, and one terminal decision. The witness remains inside the protected boundary.

[3] ENI6MA. *Pass+ and ENI6MA Sequoia architecture*, 2 October 2026, `PASS PLUS/Docs/SYSTEM/ARCHITECTURE.md`, and *Login ceremony*, `PASS PLUS/Docs/SYSTEM/lifecycles/login-ceremony.md`. On-device guest. Local grant when `validated` is true. Authority rows store hashes and sealed bytes.

[4] Frank Dylan Rosario. *Geometric One-Time Pads*, section "Paired-clone oscillation and durable consumption." Review manuscript, 5 November 2026. Local copy: `BOOK-PUBLISH/_ZENODO-WHITE-PAPERS-2026-11-05-r4/papers/geometric-one-time-pads/source/manuscript.md`. Ordered alternation. Separate allocation per direction. Consumption before the check.

[5] ENI6MA. *API authentication protocol V3*. Local copy: `LEAN4-PUBLISH/03-TECHNICAL-SYSTEMS/TECH-06-api-auth-pii/source/ENI6MA_API_AUTH_PROTOCOL_V3.md`. One-shot path: challenge, respond, validate, ledger nonce burn. Oscillation between two processes: proposed and partial.

[6] Proof-of-Control Initiative. *C4 Authorization*. In [1], `0.1/en/0x10-C04-Authorization.md`.

[7] Proof-of-Control Initiative. *C7 Evidence Generation and Properties*. In [1], `0.1/en/0x10-C07-Evidence-Generation-and-Properties.md`. C7.1.1, C7.1.3, C7.1.4, C7.3.2.

[8] Proof-of-Control Initiative. *C5 Identity*. In [1], `0.1/en/0x10-C05-Identity.md`.

[9] Proof-of-Control Initiative. *Threat vocabulary*. In [1], `docs/use-cases/THREATS.md`. The companion walk of where the agent reaches each secret is `WHITE-PAPER-ONESHOT-OSCILLATION.md`, section 2.

[10] Proof-of-Control Initiative. *C1 Provenance*, *C3 Portability*, *C8 Verifiability Tiers*, *C9 System Surface*, *C10 Conformance*. In [1], `0.1/en/0x10-C01-Provenance.md`, `0x10-C03-Portability.md`, `0x10-C08-Verifiability-Tiers.md`, `0x10-C09-System-Surface-MAESTRO.md`, `0x10-C10-Conformance-and-Disclosure.md`. Proof-of-Control is Tier 3 or Tier 4.

[11] Proof-of-Control Initiative. *C8 Verifiability Tiers*. In [1], `0.1/en/0x10-C08-Verifiability-Tiers.md`.

[12] Proof-of-Control Initiative. *Introduction*. In [1], `docs/introduction.md`.

[13] Proof-of-Control research programme. *P05 unlinkable identity*. In [1], `docs/proposals/P05-unlinkable-identity.md`.

[14] Proof-of-Control research programme. *P02 effect binding*. In [1], `docs/proposals/P02-effect-binding.md`.

[15] Frank Dylan Rosario, Dr. Lin Wang, Dr. Francisco Perez, and Dr. Octavia Sulea. *Authorization Beyond Consensus*. Review manuscript, 5 November 2026. Local copy: `BOOK-PUBLISH/_ZENODO-WHITE-PAPERS-2026-11-05-r4/papers/authorization-beyond-consensus/source/manuscript.md`.

[16] Proof-of-Control Initiative. *C2 Privacy* and *C6 Security*. In [1], `0.1/en/0x10-C02-Privacy.md` and `0.1/en/0x10-C06-Security.md`.
