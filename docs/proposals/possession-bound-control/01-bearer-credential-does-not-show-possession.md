# Gap: a bearer credential satisfies C5 without possession

**Status:** proposal. Issue text for the Identity group.
**Targets:** `0.1/en/0x10-C05-Identity.md`, C5.1.2, C5.1.3, C5.1.4.
**Pattern:** possession protocol. **Instance:** ENI6MA PassPlus.

## The problem the draft allows

C5.1.2 is met when an agent presents a certificate, a key pair, or a DID and the validation is logged. C5.1.3 is met when the tool call carries an OAuth token, a JWT, a verifiable credential, or a capability URL issued for the principal. C4.2.1 then checks signature, expiry, audience, and scope.

Copy the token. Present it from the same audience before expiry. Every check above succeeds. The execution record shows a valid credential and a named principal. It does not show that the principal's witness was used for this call. The record cannot distinguish the principal from anyone who holds the token.

C5.1.4 moves the credential into an attested environment. That stops use from a machine whose measurement does not match. A process inside a matching measurement can still present the token without the human witness. Attestation and possession answer different questions. The chapter has a requirement for the first and none for the second.

The technology-neutral rule is intact if the fix adds a check rather than deleting the examples. OAuth remains a legal way to meet C5.1.3. It is not a way to meet a possession requirement the chapter does not yet contain.

## The pattern that closes it

A possession protocol adds a second artifact beside the bearer token.

- A verifier selects a fresh challenge.
- The prover returns a response computed from a witness.
- A checker accepts or rejects.
- The evidence record stores the challenge digest, the response digest, the checker digest, and the nonce identifier.
- The witness is not in the record.
- A later tool call that claims human possession cites that record.

A stolen bearer token does not produce a fresh accepted response. A replay of an old response fails the nonce. A response for a different challenge fails the checker.

## What PassPlus runs

On device, the clients already run the protocol.

- Web `runProof("challenge")` passes `tau` and `nonce`. Validate sends the challenge and the bearings to the guest.
- The extension grants a session only when `validated` is true.
- iOS calls `challengeV2`, then `validate`, and writes `LocalSession` only when `validated` is true. The practice verifier does not grant.
- The secret configuration is not what the guest is asked to echo. The response witness used in the broader design, `eni6ma.proof.v1`, carries ordered bearings and a proof hash and omits the secret, the permutation, the offsets, epsilon, and pi.
- Enrollment plaintext stays on the device until an E6PS seal. The Authority's stored rows are hashes and sealed bytes.

What this shows the group: the check is not a research sketch. A pinned wasm guest, a fresh nonce, and a fail-closed local grant are enough to make C5.1.2's credential check and a possession check into different log lines.

## What PassPlus does not run

The clients do not attach that possession record to an agent tool call. Web, extension, and iOS do not call `POST /v1/reserve` or `POST /v1/consume`. Meeting the new requirement end to end means a gateway cites the record. The phone's local session is the possession half only.

## Requirement sketch

**5.1.5, Level 2.** Verify that, where the action class requires human possession, the execution record cites a possession record for that action, that the possession record's nonce was unconsumed at acceptance, and that a test presenting a bearer token with no possession record is rejected and logged.

**Auditor evidence.** One accepted possession record with challenge digest, response digest, checker digest, and nonce. One rejected call that presented a still-valid bearer token and no possession record. Confirm the witness is absent from both records.

**5.1.4 stays.** A possession record does not satisfy 5.1.4. A TEE quote does not satisfy 5.1.5.
