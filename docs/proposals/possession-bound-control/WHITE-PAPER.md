# What the evidence model does not show: possession of a non-transmitted witness

**Status:** white paper proposed for the Proof-of-Control working groups. Informative. No requirement in this file is normative until a group adopts the sketches in the companion gap notes.
**Audience:** Identity, Authorization, Security, and the insurance group.
**Date:** 2026-11-06.
**Instance:** ENI6MA PassPlus, architecture as of 2026-10-02. The paper uses that instance to show the pattern is running. It does not propose that the standard depend on the instance.

## 1. The paper to contribute, and the papers to leave behind

Two ENI6MA monographs are the ancestors of this argument and the wrong files to open as pull requests.

*The Void in Agentic Security* says agent stacks still authenticate with stored secrets, rotating API tokens, OAuth delegations, and TLS, and that a live demonstration of a witness is a different object from those mechanisms. That diagnosis matches a hole in this draft. The monograph states it with soundness expressions and a register this repository's editorial rules will not carry. An assessor cannot close "the witness never leaves the prover" against a named artifact unless the evidence schema forbids the witness and a test tries to write one.

*Agent-to-Agent Protocols and Security* surveys A2A, ACP, and FIPA. C5.2 already requires signed agent-to-agent messages and, at Level 3, validation from published key material. A survey of those protocols does not add a requirement the draft lacks.

This paper is the contribution. It states the holes as properties the current chapters do not test, then states the pattern that closes them, then states what PassPlus already runs.

## 2. The hole, in one paragraph

Chapters C5 and C4 can be satisfied by a bearer credential. C5.1.2 asks the agent to authenticate with a certificate, a key pair, or a DID, and to record validation. C5.1.3 asks each tool call to carry a delegation token: a short-lived OAuth or JWT, a verifiable credential, or a capability URL. C4.2.1 validates that token's signature, expiry, audience, and scope. An attacker who copies the token meets every one of those sentences. The draft then has a record that a credential was presented. It does not have a record that the principal still holds a witness that was not in the token. PassPlus is built around that missing record. A fresh challenge is issued. The human returns bearings. A pinned wasm guest accepts or rejects. The secret configuration is not the object that moves. The clients grant a local session only when the guest accepts. That is the pattern. The draft has no name for it, no profile for it, and no auditor note that would fail a deployment which skipped it.

## 3. Six problems the current text does not catch

### 3.1 A stolen bearer token is a passing C5 record

The parenthetical examples in C5.1.2 and C5.1.3 are not a closed list, and the technology-neutral rule forbids closing the list around them. The failure is the other way. Nothing in the chapter is unsatisfiable for a copied token. Level 3 adds binding of the credential to an attested enclave or TPM (C5.1.4), which stops the token being exercised from an unattested machine. It does not stop the token being exercised by a process inside the attested machine that does not hold the human's witness. PassPlus separates those facts. The guest's acceptance is a check that the response matches the challenge under the witness. The device is still a trusted execution place for that check. The pattern does not pretend the phone is a TEE quote. It refuses to let a TEE quote stand in for the human check.

### 3.2 The unlinkable profile withholds the principal

Appendix D issue 2 asks for verifiable-but-unlinkable binding. P05 answers by suspending C5.1.1, because a persistent principal identifier cannot be carried when the design exists to hide the principal. That answer fits a procurement agent that must not reveal who it buys for. It is the wrong answer for a system whose accountability requirement is "which enrolled principal answered." PassPlus keeps the handle and the device enrollment. It withholds the witness. A profile mechanism is worth having. A profile mechanism with only `identified` and `unlinkable` forces this pattern into one of two false descriptions: either the evidence record contains the witness, or the evidence record has no principal. Both descriptions fail the pattern.

### 3.3 The approval record is not bound to the challenge the human answered

C4.1.6 records the approver's identity, the content presented, the decision, and a timestamp. The threat file's `approval-fatigue` row says Proof-of-Control addresses the raw content presented and the decision, and leaves the fatigue itself out of scope. The row is right about the limit and incomplete about the artifact. A mutable interface can present sentence A and store a digest of action B, and the record still has an approver, a blob called "content," a yes, and a time. PassPlus makes the response a function of the presented challenge: the planes come from the challenge, the bearings come from the human, and the guest accepts only the pair. That binding is the pattern C4.1.6 does not require. It does not detect a prompt injection. It stops the injected instruction from being the thing that was authorized, once a gateway is required to release only the action whose digest is the challenge digest.

### 3.4 Release does not cite a possession check

C7.1.4 already has the right shape for effect mediation: a single-use capability bound to the evaluated snapshot, checked before execution. C4.1.3 blocks out-of-scope actions at a gateway. C4.1.5 forbids a standing broad credential. None of those sentences require the capability to cite a fresh possession record. A deployment can be conformant at those IDs and never ask a human to hold a witness. That is allowed for agents that have no human on the action. It is a hole for actions whose policy says a human must have answered this challenge. PassPlus runs the check and then stops. The web app, the extension, and the iOS app do not call reserve or consume, and they do not stand in front of a tool gateway. The pattern's missing half is the capability. The draft's missing half is the requirement that would make that capability mandatory when the action class says so. Both sentences belong in the contribution. Claiming the phone already refuses a payment would be false.

### 3.5 An operator boolean is being asked to carry Tier 3

C8 grades evidence by who must be trusted and whether their dishonesty is publicly detectable. P01 has already deleted the claim that Tier 3 removes the trusted party. A boolean emitted by a checker the claimant runs is detectable as a lie only by someone who re-runs the checker or recomputes the decision from public inputs. PassPlus exports the boolean. The guest runs on the same device as the claimant. An outsider who sees `validated: true` and cannot recompute it is trusting the device. That is Tier 2 at most: an attestation of a local decision. The pattern reaches the Tier 3 candidate only when the commitment, the challenge, and the response are enough for a published checker to accept, and the boolean is not an input. The monograph describes that transcript. The clients, on the architecture page, do not hand that transcript to an outsider. The draft's hole is the absence of a sentence that forbids grading the boolean as the transcript. PassPlus is the example that makes the sentence concrete, including the example of what not to grade.

The Authority path makes the same distinction sharper. When `handle-app` is configured with an Authority URL, validate posts `proof_ok` and the nonce to consume. The Authority does not re-run the guest. A consume record is then a stored bit from the caller. The pattern's fix is either re-execution by the relying party or outsider recomputation from published artifacts. The clients have the guest that could be re-run. The consume API does not re-run it. This paper does not offer that API as the Tier 3 design.

### 3.6 A witness is not a signing key, and a seal margin is not a signature margin

C6.3 requires evidence-signing keys to be generated in hardware, non-exportable, rotated, and recoverable by key identifier. A human witness fails those sentences in a way that is not a defect. It is not generated in an HSM. It is not rotated on a key calendar. Compromise is re-enrollment under a new commitment, not a signature-algorithm migration. If the chapter is the only key story, assessors will reject the pattern or will accept the witness as if it were the evidence-signing key. The second failure drops C6.3 for the log. PassPlus already treats the objects as different. The witness is sealed with E6PS v2. The seal's hybrid encapsulation is X25519 plus ML-KEM-768. That margin is about reading the enrollment later. C6.3.5 is about forging the signature on a retained evidence record at examination time. The draft does not say the two margins are different claims. A contributor who offers the seal as the evidence signature will pass a careless reading of C6.3.5. The pattern forbids that reading.

## 4. The pattern

Stated without a product, the pattern is six obligations.

1. The evidence record of a human-gated action carries a principal reference, a challenge digest, a response digest, a checker digest, and a nonce identifier, all inside the signature.
2. The witness is not in the record. A schema test that inserts it must fail.
3. The checker rejects a mismatched response and rejects a consumed nonce. Both rejections are records.
4. When the action class requires a human possession check, the gateway releases the effect only under a single-use capability that cites that possession record and the canonical action digest.
5. An outsider's acceptance decision does not take the operator boolean as an input. A deployment that cannot show this recomputation states Level 2 for the check and does not state Level 3.
6. The evidence-signing key and the possession witness are different disclosed objects, with different compromise procedures and different quantum margins.

PassPlus runs 1 through 3 in local form: the challenge and the bearings exist, the guest decides, the secret configuration is not the validation payload's secret, and a local session is written only on acceptance. Obligation 4 is the gateway the clients do not have. Obligation 5 is the published recomputation the clients do not export. Obligation 6 is how the seal and the guest are already separated, and it is the sentence the draft should copy.

## 5. What this asks the groups to add

The asks are collateral, listed in [README.md](README.md). In short: glossary entries, a third identity profile, four signed fields, negative vectors, an auditor note on C4.1.6, a citation rule on C7.1.4, two disclosure categories, one Appendix B row, and one use case. None of those artifacts names a vendor. Each one is inhabited by the PassPlus instance so the group can see a deployment that already has the possession half and still must not claim the release half.

## 6. What this does not ask

It does not ask the standard to replace OAuth, DIDs, verifiable credentials, TEE attestation, or Merkle logs. Those mechanisms evidence what they evidence. A bearer token evidences presentation. A TEE quote evidences a measurement. A possession record evidences a response to a challenge under a witness that stayed out of the record. A conformant system can use all three, cited from the capability, and an assessor can fail any one of them without failing the others.

It does not ask for PassPlus, ENI6MA, or a wasm guest to be a reference implementation. `impl/` remains the evidence pipeline. The pattern is a grant that pipeline should be able to require.

It does not claim Proof-of-Control for the shipping clients. No domain of those clients reaches Tier 3 on an artifact an outsider recomputes. The paper's purpose is to make that line visible in the requirements, and to show why a draft that cannot see the line will accept a stolen token, an unbound approval, and a local boolean as control.
