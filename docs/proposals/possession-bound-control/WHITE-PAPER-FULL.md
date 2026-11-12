# The chain of holes in agent identity: what the Proof-of-Control draft lets an attacker pass, and what the agent can pass without stealing anything

**Frank Dylan Rosario**  
**Dr. Lin Wang**  
**Dr. Octavia Sulea**

6 November 2026

Working paper for the Identity, Authorization, and Security groups of the Proof-of-Control Initiative. Informative. A requirement becomes normative only when a group adopts it into the draft. This paper is self-contained. Every load-bearing claim about the draft points at a requirement file in the public Working Draft. No other manuscript is required to read it.

## Abstract

Working Draft v0.1 of the Proof-of-Control Standard sets out to evidence which agent ran, for which principal, and whether the action stayed inside a granted boundary [1]. The identity chapter implements that question as presentation of a credential: a certificate, a key pair, a DID, an OAuth or JWT token, a verifiable credential, or a capability URL, optionally bound to an attested environment [2]. Authorization then checks the token's signature, expiry, audience, and scope [3]. Those checks record that an object was presented and that it was still valid. They do not record that a non-transmitted witness was used to answer a fresh challenge for this action.

The holes form a chain. Each one leaves an artifact that the next requirement accepts. An external attacker enters the chain by obtaining one of those artifacts. The agent does not need to enter from outside. The draft tells the implementer to put the artifact in the agent's hands, and the agent then walks the rest of the chain as the legitimate presenter, the approval intermediary, the inter-agent signer, and the composer of tool arguments. This paper states the chain, then the external surfaces, then the agent surfaces, then the tests that would break the chain. A control that no named test can fail is not yet a requirement.

## 1. Terms used in this paper

These terms are fixed here so the rest of the paper does not depend on any other vocabulary.

A **presented credential** is an object a party shows: a token, a certificate, a signature, a verifiable credential, a capability URL. Validity is a check on the object.

A **witness** is a secret configuration used to answer a challenge. It is an input. It is not itself the evidence record, and it is not an evidence-signing key.

A **possession check** is an interaction in which a verifier selects a fresh challenge, a prover returns a response computed from a witness, and a checker accepts or rejects. The evidence of the check is a challenge digest, a response digest, a checker digest, and a nonce identifier, all covered by a signature. The witness is not part of that evidence.

A **principal reference** names the enrolled party. It is not the witness.

An **operator boolean** is a bit emitted by a checker the claimant operates. It reports that the checker ran. It is not a recomputation by an outsider.

A **release** is the moment an effect is handed to a tool or to another agent. A record that an evaluation occurred is not a release.

**Consumption** means a named challenge or capability cannot authorize a second release. Expiry is a clock. Consumption is a use.

A **profile** is a switch, stated inside the signed record, that selects which identity requirements apply. It is not an assurance rating. Naming a profile does not make a system safe.

## 2. What the draft actually requires

Citations use the draft's own identifiers, `C<chapter>.<section>.<requirement>` [1].

C5's control objective is evidence of actors, agents, and delegated relationships, so that every action traces to a legitimate principal. The facts the chapter names are which agent ran and which principal it ran for [2].

C5.1.1, Level 1, requires every execution record to carry an agent-instance identifier and a principal identifier [2]. C5.1.2, Level 2, requires the agent to authenticate with a cryptographic credential, listing a certificate, a key pair, or a DID, and to record validation [2]. C5.1.3, Level 2, requires each tool call to carry a delegation token issued by or on behalf of the principal, listing a short-lived OAuth token or JWT, a W3C verifiable credential, or a capability URL [2]. C5.1.4, Level 3, requires that credential to be bound to an attested execution environment so it cannot be exercised where attestation fails [2]. C5.2.1, Level 2, requires agent-to-agent messages to be signed by the sending agent's credential, and requires receivers to reject unsigned or invalid messages [2]. C5.2.2, Level 3, requires the receiver to validate the sender from published key material without contacting the sender's operator [2].

Appendix D issue 1 records the working-group lean that Authorization owns the action boundary and takes Identity as an input [4]. C4.1.5 requires per-task scope and expiry and forbids a standing broad credential at runtime [3]. C4.2.1 requires validation of signature, expiry, audience, and scope before execution [3]. C4.1.6 requires a human approval record with the approver's identity, the content presented, the decision, and a timestamp [3]. C4.1.7 requires the authorization context of a call to include parameters carried from earlier calls in the same path, so individually authorized steps cannot compose into an excess [3]. C4.1.8 forbids diagnostic output from raising an approval threshold [3]. C4.2.2 requires each delegation hop to validate back to the originating principal [3].

C7.1.1 requires tool and effect invocations to pass an Action Interception Gateway the agent cannot bypass [5]. C7.1.4 requires the effect channel to be mediated with the policy decision, including by a single-use capability bound to the evaluated snapshot [5]. C7.1.5 says a system that evidences evaluation and does not mediate the effect may claim Tier 1 or Tier 2 only [5]. C7.5 forbids evidence fields that assert quality, correctness, or intent [5].

C8 grades evidence by who must be trusted [6]. The draft's own correction, recorded with the P01 notes, is that Tier 3 does not mean the trusted party has been removed [7]. C2.1.2 and C2.4.1 require retained privacy evidence to carry digests or classifications rather than protected content, enforced by schema [8]. C6.3.1 through C6.3.5 govern evidence-signing keys: hardware-backed generation, rotation, compromise recovery, algorithm identifiers, and post-quantum or hybrid signatures when retention outlives the classical scheme [9].

The threat vocabulary says `identity-abuse` is answered by cryptographic identity and a delegation chain, and it places credential theft and human social engineering out of scope [10]. It says `prompt-injection` is answered by gating the out-of-bounds action, not by detecting the injection [10]. It says `insecure-inter-agent-comms` is answered by signed messages [10]. Appendix B's mechanism menu lists signatures, zero-knowledge proofs, remote attestation, commitments, and verifiable credentials [11]. It has no row for an interactive possession check. The evidence schema, as P05 records it, requires `agent_id` and `initiating_user` [12] [13].

Read as a set, these documents specify presentation, signature, expiry, scope, and, at the top of the current identity ladder, an attested machine. They do not specify a witness that stays off the record.

## 3. The chain of holes

The holes are ordered. The output of one is an input the next requirement treats as success. Breaking a later hole without breaking the earlier one does not stop the walk.

**Hole A — Identity is presentation.** C5.1.2 and C5.1.3 are satisfied by showing a credential that validates [2]. The check's input is the object. The check's output is a pass plus a principal identifier taken from the object, which also satisfies C5.1.1 [2]. No input is a witness. No input is a challenge bound to this action.

**Hole B — The valid object is given to the agent.** C5.1.3 says the tool call carries the delegation token [2]. The agent is the caller. The token is therefore in the agent's hands for the life of the grant. Hole A's pass condition is now a condition the agent can meet without help.

**Hole C — Validity is not consumption.** C4.2.1 checks signature, expiry, audience, and scope [3]. C4.1.5 asks for per-task expiry and forbids a standing broad credential [3]. A token can be short-lived and still authorize every tool the agent might call until the clock runs out. Nothing in those two requirements consumes the grant when one action is released. The output of Hole B remains usable for the next action.

**Hole D — Approval is a record the presenter can write.** C4.1.6 stores approver identity, presented content, decision, and timestamp [3]. It does not require a comparison function from the bytes shown to a person to the bytes released to a tool. The agent that holds the token from Hole B is also the component that can show one action and submit another, and that can fill the four fields. The output is an approval record that validates, citing the principal from Hole A.

**Hole E — Path checks do not see the human challenge.** C4.1.7 and C4.1.8 constrain composition of tool parameters and forbid trust moving from a diagnostic output into an approval threshold [3]. They do not take a possession record as an input. An upstream step can widen a downstream call. The approval from Hole D still says yes. The path rule can pass on the widened call because the human's challenge was never in the context.

**Hole F — Inter-agent identity authenticates the agent key.** C5.2.1 and C5.2.2 accept a message signed by the sending agent's credential and checkable from published keys [2]. The agent holds that key for the same reason it holds the token in Hole B. A receiver that implements C5.2 correctly accepts the message. C4.2.2 will walk the signatures back to a principal identifier [3]. That identifier was copied forward from Hole A. No hop required a fresh possession check.

**Hole G — Release does not cite a possession check.** C7.1.4 can be met by a single-use capability bound to an evaluated snapshot [5]. The snapshot can be the widened call from Hole E, signed under the agent key from Hole F, justified by the approval record from Hole D. The capability verifies. Nothing in C7.1.4 requires the capability to cite a possession check the agent cannot mint alone. C7.1.1's separate gateway [5] stops the agent from bypassing the gate. It does not stop the gate from agreeing with the agent.

**Hole H — A boolean, or silence, stands in for the check.** C8 asks who must be trusted [6]. An operator boolean is trusted if the claimant's checker is trusted. The draft does not say that a missing proof bit fails closed. A verifier that treats absence as acceptance turns Hole G into a recorded pass with no checker result at all. C7.1.5 limits unmediated claims to Tier 1 or Tier 2 [5]. It does not define omission as failure. The `cascading-failure` row says the top of the model fails closed [10]. The identity and evidence chapters do not force that on a missing possession result.

**Hole I — The bound message is not the effect.** P02 states that the draft's binding result is about the request representation that was evaluated, and that an endpoint can still apply defaults, aliases, retries, and unsigned context, so the same bytes can cause two effects [14]. A capability that survives Hole G can name a request the endpoint does not execute. Identity remains valid. The effect changes after identity has finished.

**Hole J — The record either leaks the witness or drops the principal.** If an implementer logs the witness so a later auditor can "see what was checked," C5 is satisfied and C2.4.1 is missed [2] [8]. The log becomes a second copy of the secret. If an implementer instead adopts P05's unlinkable profile and suspends the principal identifier [13], the records from Holes A through G no longer name an enrollee. Incident response loses the party. P05 is a coherent answer where the relying party must not learn a stable principal [4] [13]. It is not a fix for Hole A. The draft has no third switch that keeps the principal reference and forbids the witness.

**Hole K — The checker and the signing key are unnamed or mis-labeled.** C5 does not put a checker digest inside the signed identity record [2]. A replaced checker that accepts every response still produces the boolean in Hole H. Appendix B will invite an assessor to file the check as a zero-knowledge proof or as remote attestation [11]. Remote attestation, including the architecture in RFC 9334, evidences platform state [15]. It does not evidence that a person answered a challenge. C6.3's rules fit an evidence-signing key [9]. Applied to a witness, they either reject the possession pattern, pushing deployments back to Hole A, or they accept the witness as the key that signs history. A confidentiality wrapper used to move a witness is a third object. Its algorithm is not the signature algorithm C6.3.5 is about [9].

Hole A is the root. Holes B through G are what a conformant agent path does with that root. Holes H through K are how the record of that path is graded, stored, and mistaken for a different mechanism. An assessor who closes Hole G and leaves Hole A open has built a gateway that releases whatever the presented credential asks for.

## 4. External attack surfaces

An external attacker is a party who does not start inside the agent process. Each surface is a place that party can join the chain. The threat file's exclusion of credential theft under `identity-abuse` [10] does not survive Hole A: theft of the object the requirement tells the implementer to mint is the requirement succeeding for the wrong holder.

**Surface E1. Copied credential.** The attacker copies the token, certificate, or capability URL produced for Hole A and presents it before expiry, to the listed audience, inside the listed scope. C5.1.2, C5.1.3, C5.1.1, and C4.2.1 all pass [2] [3]. No witness is required, so none is missing. The relying party attributes the call to the principal named in the object.

**Surface E2. Stolen session inside the expiry window.** Hole C leaves the grant alive after first use. The attacker who takes the session spends it until the clock, not until a consumption record, says stop. C4.1.5 is still met if the token was minted with an expiry and a written scope [3].

**Surface E3. Replayed response.** Where a deployment has added a challenge informally, and the nonce is not consumed at the relying party, a recorded response is a bearer object. C4.2.1 will not reject it on expiry if the surrounding token is still valid [3]. The draft has no identity requirement that a challenge identifier be single-use.

**Surface E4. Omitted proof bit.** Where a verifier implements Hole H by defaulting a missing result to success, the attacker who can submit the consume or attest operation without the bit obtains a pass record. No checker ran. C5 has no field that makes the omission fail [2].

**Surface E5. Witness taken from the evidence store.** Hole J's first branch stores the witness. The attacker who reads the log can answer later challenges. That position outlasts the token in Surface E1, because expiry does not rotate a witness. C2 would have forbidden the content if the witness had been named as protected content [8]. C5 does not name it [2].

**Surface E6. Substituted checker.** Hole K leaves the checker digest out of the signed record. The attacker who replaces the local checker with one that accepts every response produces the boolean in Hole H. Validation logs for C5.1.2 show success [2]. There is no signed field to disagree.

**Surface E7. Attested machine, wrong holder.** C5.1.4 stops use from a machine whose measurement does not match [2]. It does not stop use from a process inside a matching measurement. An attacker with code execution inside the attested boundary presents the credential. The attestation report matches the golden value under C6.1.3 [9]. The report is about the platform [15]. The principal did not answer a challenge.

**Surface E8. Endpoint alias after a valid check.** Hole I. The attacker influences an unsigned default, alias, or context between evaluation and effect [14]. The identity record from Hole A remains true of the request that was checked. The effect is a different one. Closing identity harder does not close this surface. It has to be named as outside the identity claim, or deployments will report it as an identity success.

Surfaces E1 through E7 are available only because Hole A defines identity as an object that can be copied, replayed, omitted, or exercised by whoever reaches the environment. Surface E8 remains even after a possession check, unless the endpoint conditions in P02 also hold [14].

## 5. Agent attack surfaces

The agent is the software C5 is trying to identify. It is also a party that already satisfies Hole B. It does not steal the credential. The draft's design puts the credential in its runtime so it can call tools [2]. The agent surfaces below are walks that start there. A prompt injection, a bent goal, or an ordinary tool policy that is wider than the human's latest instruction all use the same walks. The `prompt-injection` row correctly refuses to claim detection of the injection string [10]. The failure is earlier: the walk is in bounds under the requirements, so there is no out-of-bounds action for the row to gate.

**Surface A1. The agent presents its own token.** No copy step. The agent calls the tool with the delegation token from C5.1.3 [2]. Signature, expiry, audience, and scope pass under C4.2.1 [3]. The execution record names the principal. The principal did not perform a possession check for this call. This is the agent's form of Surface E1, and it is available on every deployment that implements the chapter as written.

**Surface A2. The agent spends the unconsumed grant.** After one consent or one check, Hole C leaves the grant alive. The agent issues further tool calls inside the expiry and the written scope. Each call is a fresh C5.1.3 presentation of the same token [2]. `excessive-agency` and `autonomy-creep` are the threat-file names [10]. The exploit condition is that scope was defined as a set of tools over a clock interval, not as one consumed action.

**Surface A3. The agent splits the screen from the tool arguments.** The agent shows a person action P and submits action Q. It writes the C4.1.6 record with a real approver identity, a blob it calls the presented content, a yes, and a timestamp [3]. The auditor note on C4.1.6 says the presented content should match what executed. The requirement does not define the match, and the agent is the party that both renders and records. `approval-fatigue` leaves fatigue out of scope [10]. Substitution is not fatigue. It is Hole D used by the only component that sees both representations. A human who is tired and a human who was shown the wrong bytes produce the same four fields.

**Surface A4. The agent composes past the check.** The agent runs an upstream tool that returns a wider target, then a downstream tool that uses it. C4.1.7 looks at tool parameters [3]. It does not look at a human challenge, because Hole E never stored one. C4.1.8 stops a diagnostic output from raising an approval threshold [3]. It does not stop the agent from choosing arguments that were already inside a broad threshold. The approval record from Surface A3 still matches whatever content the agent stored.

**Surface A5. The agent signs to its peers.** The agent holds the key C5.2.1 tells it to use [2]. It signs a message that asks another agent to perform the effect. The receiver implements C5.2.2 and accepts [2]. C4.2.2 walks the chain to the principal identifier copied from the original token [3]. Every signature is valid. The principal's witness was not used for that message. `insecure-inter-agent-comms` is satisfied in the sense the threat row states — authenticity and integrity of the agent key [10] — and the principal is still absent. A collective of agents can move a request across hops under the draft and remain conformant at C5.2.

**Surface A6. The agent mints the capability the gateway wants.** Hole G's capability is bound to a snapshot [5]. The agent, or a gateway that trusts the agent's evaluation, can produce that snapshot from Surfaces A3 through A5. The gateway verifies the capability and releases the tool. C7.1.1 has been met: the agent did not bypass the gateway [5]. The gateway agreed with the agent. A single-use capability that does not cite a possession check the agent cannot create is a single-use wrapper around Hole A.

**Surface A7. The agent emits or withholds the boolean.** If the only possession-shaped artifact in the deployment is an operator boolean, the agent runs on the same side of the checker as the claimant. It can relay a success bit. If the verifier treats a missing bit as success, the agent omits the field and Hole H records a pass. The agent does not need to break the checker. The record schema never required a result the agent could not assert.

**Surface A8. The agent reads the witness back.** If Hole J stored the witness in the execution log, and the agent can read its own records, the agent obtains the witness. Later challenges are then answerable by the agent alone. The external attacker needed a separate read in Surface E5. The agent is already on the host. C2.4.1 would have blocked this if the schema named the field [8]. An identity implementation that logs "the inputs the checker saw" will not consult that privacy sentence unless C5 points at it.

**Surface A9. The agent drops its own name.** If the deployment selects the unlinkable profile to avoid putting a person in the tool record [13], the agent's calls no longer carry a stable principal. Surfaces A1 through A6 still produce valid cryptographic records. After the release, there is no enrollee to disable. The agent has not hidden a witness. It has hidden the only accountability field Hole A was using as a substitute for a witness.

**Surface A10. The agent replaces its checker.** Hole K. The agent points the local check at a module that returns success for any response, and the signed record has no checker digest to make that swap visible. C5.1.2 logs a validation event [2]. The event is the agent's module reporting on itself.

The agent's chain, in the order a single task runs, is A1, then A3 or A9, then A4, then A5 if another agent is involved, then A6. A2 is the same chain on the second call. A7, A8, and A10 are how the agent keeps the record aligned with the chain. None of these steps requires the attacker capabilities in Section 4. An external attacker who later steals the token joins at A1 and continues through A6 as if they were the agent. After that join, C5 cannot tell them apart.

## 6. Where the chain becomes a release

C7.1.5 is the draft's own warning that evaluation without a mediated effect is not executed-action evidence [5]. The chain shows a sharper case. Mediation can be present and still release the wrong action, because the artifact the gateway checks was produced by Holes A through F.

The release condition the draft can meet today is: a credential validated, a token in scope, an approval record stored, a snapshot signed, a capability verified. The release condition that would break the agent chain is narrower. For an action class that claims a human principal as the source of authority, the gateway releases only when a single-use capability verifies and the capability cites a possession record whose challenge digest is the canonical digest of the action, whose nonce is unconsumed, and whose checker digest is inside the signature. Consumption is recorded before release. A second presentation is a rejection. The witness is not in the capability.

That condition does not detect an injection string. It refuses the release the injection was trying to cause, which is the split the threat row already draws [10]. It does not make the human's understanding a field. C7.5 still forbids an intent claim [5]. It does not force a remote endpoint to execute the canonical request. Hole I and P02 remain [14]. A paper that treated a possession record as evidence that a payment settled would rebuild the overclaim P02 exists to stop.

C8 open item 2 asks whether required human authorization belongs in the Tier 4 root [6]. Putting the human in that cell means Tier 4 is "trust this person," which is the structure the P01 correction removed from Tier 3 [7]. The fail-closed halt can be a Tier 4 property of the gateway: the effect does not leave when the capability is absent or replayed. The human remains a disclosed party who can be coerced and who can answer a challenge the screen did not bind to the tool bytes. Those facts belong in the trust-assumption disclosure of C10 [16]. They are not a root that promotes an operator boolean.

Until an outsider can recompute acceptance from a commitment, a challenge, and a response, and the operator boolean is not an input, the possession record is an attestation of a local decision. That is at most the draft's Tier 2 [6]. Grading the boolean as Tier 3 is Hole H used as a conformance claim.

## 7. Tests that break the chain

Each test fails a hole. A deployment that cannot run the test does not meet the corresponding claim. The tests name artifacts. They do not name an implementation.

**T1, against Hole A and Surface A1.** Present a credential that passes C5.1.2, C5.1.3, and C4.2.1, and present no possession record. The gateway must reject the release and write a rejection that names the credential's principal reference. A pass is a finding.

**T2, against Hole C and Surface A2.** After one accepted release, present the same grant for a second action without a new unconsumed challenge. The second release must be rejected. An expiry that is still in the future must not be accepted as a reason to allow it.

**T3, against Hole D and Surface A3.** Show challenge bytes P to the approval path and submit action bytes Q. The release must be rejected. The rejection record must contain both digests. If the shown bytes and the action bytes differ in kind, a published mapping must recompute one from the other. A missing mapping means the approval record is not authorization for the tool call.

**T4, against Hole E and Surface A4.** An upstream result widens a downstream target relative to the challenge digest cited by the possession record. The path evaluation must reject. A C4.1.7 implementation that never reads the possession record fails this test even if it reads tool parameters [3].

**T5, against Hole F and Surface A5.** A peer message signed by the agent key, with no possession citation for that message digest, must be rejected by a receiver that claims human-gated release. A receiver that only implements C5.2.2 will accept it [2]. That acceptance is conformant to C5.2 and non-conformant to the human-gated claim. The conformance statement has to say which action classes are human-gated, or the two results are silently both "pass."

**T6, against Hole G and Surface A6.** Submit snapshot A to the mechanism and attempt to dispatch action B. B must not reach the tool. Submit snapshot A with a valid bearer token and no possession digest. A must not reach the tool. This extends the substitution test already stated for C7.1.4 [5] with a third arm the current text does not require.

**T7, against Hole H and Surface A7.** Omit the proof result. The verifier must reject. Submit an operator boolean and ask an outsider to recompute acceptance without using the boolean and without calling the operator. If they cannot, the claim's tier for that check is not Tier 3 [6].

**T8, against Hole J and Surfaces A8 and A9.** Insert a witness into a possession-profile record. Schema validation must fail [8] [12]. Omit the principal reference on that same profile. Validation must fail. A profile that needs the principal omitted is a different profile, the one P05 specifies [13], and it must not be inferred from a missing field.

**T9, against Hole K and Surfaces A10 and E6.** Alter the checker digest under an otherwise valid signature. Verification must fail. A record with no checker digest must not be accepted as a possession record.

**T10, against Hole I.** State, in the claim, that the evidence describes the evaluated request, and do not state that it describes the endpoint's effect, unless the endpoint conditions P02 names are met and tested [14]. A claim that skips this sentence fails C7.1.5's modesty rule even when T1 through T9 pass [5].

C6.3.1 through C6.3.5 stay as written, assessed against the evidence-signing key only [9]. The witness has a different recovery action: revoke the commitment and require a new enrollment. A seal or encapsulation used to move a witness discloses its recipient and its algorithms in a cell that is not the C6.3.5 cell. One measurement must not be copied into both.

A profile token inside the signature selects the rules. `identified` keeps today's C5 text. The unlinkable profile, if the group adopts P05, suspends the principal under P05's substitute requirements [13]. A third token, possession-bound, keeps the principal reference, adds the fields in the possession check defined in Section 1, and forbids the witness. An unknown token is rejected. A missing token means `identified`, so existing evidence keeps its meaning. Suspension is never inferred from absence. P05's reason for refusing to make `agent_id` optional applies here [13].

## 8. What this paper does not conclude

The draft's presentation checks should stay. A signed token, a DID, a verifiable credential, and an attestation report evidence what they evidence. They are not a possession check, and a possession check is not a hardware quote and not a zero-knowledge presentation unless a separate requirement says so. Appendix B needs a row so assessors do not file the check under those neighbors [11]. The row's verification requirement is T7 and T8. Its non-claims are legal personhood beyond the principal reference, the wisdom of the action, and the endpoint effect.

The chain does not show that every agent deployment must put a human on every call. It shows that a claim "this action was the principal's" is false under the current text whenever the principal's authority is a credential the agent holds. Action classes with no human source of authority should say so, and should not be described as possession-bound. Action classes that do claim a human source and cannot run T1 through T9 should be graded at the tier of the artifact they actually have, which for a local boolean is not Tier 3 [6].

No safety, fairness, or correctness result follows from closing the chain. C7.5 is the boundary [5]. Closing the chain attributes a release, or a refusal, to a challenge and a principal reference. It does not grade the model that proposed the call.

## 9. Conclusion

Hole A defines identity as presentation of a movable credential. The draft then hands that credential to the agent, leaves it valid until expiry, accepts an approval record the agent can compose, authorizes peer messages the agent can sign, and allows a gateway to release a snapshot the agent can mint. An external attacker joins by copying, replaying, omitting, or reading one artifact on that path. The agent starts already on the path. After the join, the requirements treat the attacker and the agent as the same principal, because both can produce the artifact the requirements name.

The break is a possession record the agent cannot mint alone, cited by the capability that releases the effect, consumed on use, stored without the witness, and graded as an operator boolean until an outsider can recompute it. The tests in Section 7 are the form of that break. The requirement files in the bibliography are the files that do not yet contain it.

## References

[1] Advanced AI Society and the Proof-of-Control Initiative. *Open Verification: the Proof-of-Control Standard for Agents*. Working Draft v0.1. Repository header identifies v0.1.4. https://github.com/LFDT-ProofOfControl/ov-poc-standard. Normative text under `0.1/en/`. Identifier syntax is in the repository README. Public-comment window printed there: 1 August 2026 through 30 October 2026. Version 1.0 target in `docs/roadmap.md`: 1 February 2027.

[2] Proof-of-Control Initiative. *C5 Identity*. In [1], `0.1/en/0x10-C05-Identity.md`. Requirements C5.1.1, C5.1.2, C5.1.3, C5.1.4, C5.2.1, C5.2.2.

[3] Proof-of-Control Initiative. *C4 Authorization*. In [1], `0.1/en/0x10-C04-Authorization.md`. Requirements C4.1.5, C4.1.6, C4.1.7, C4.1.8, C4.2.1, C4.2.2, C4.2.3.

[4] Proof-of-Control Initiative. *Appendix D: Open Working-Group Issues*. In [1], `0.1/en/0x93-Appendix-D_Open-Issues.md`. Issue 1, identity and authorization. Issue 2, anonymity and pseudonymity. Issue 4, the contribution reproduced as the source of issues 1 and 2. Issue 6, the binary threshold.

[5] Proof-of-Control Initiative. *C7 Evidence Generation and Properties*. In [1], `0.1/en/0x10-C07-Evidence-Generation-and-Properties.md`. Requirements C7.1.1, C7.1.4, C7.1.5, C7.5.1, C7.5.2.

[6] Proof-of-Control Initiative. *C8 Verifiability Tiers and the Binary Threshold*. In [1], `0.1/en/0x10-C08-Verifiability-Tiers.md`. Includes the open item on human authorization and the Tier 4 root, and the statement that Tier 3's name is Trust-minimized.

[7] Proof-of-Control research programme. *P01 trust-calculus tiers* and the programme index. In [1], `docs/proposals/P01-trust-calculus-tiers.md` and `docs/proposals/README.md`. Cited for the correction that Tier 3 does not mean the trusted party has been removed. The programme states that this correction rests on self-authored deployment descriptions.

[8] Proof-of-Control Initiative. *C2 Privacy*. In [1], `0.1/en/0x10-C02-Privacy.md`. Requirements C2.1.2 and C2.4.1.

[9] Proof-of-Control Initiative. *C6 Security*. In [1], `0.1/en/0x10-C06-Security.md`. Requirements C6.1.3 and C6.3.1 through C6.3.5.

[10] Proof-of-Control Initiative. *Threat vocabulary for use-case submissions*. In [1], `docs/use-cases/THREATS.md`. Rows cited: `identity-abuse`, `prompt-injection`, `excessive-agency`, `autonomy-creep`, `approval-fatigue`, `insecure-inter-agent-comms`, `cascading-failure`. A tag records exposure, not a defense.

[11] Proof-of-Control Initiative. *Appendix B: Proof-Mechanism and Controls Inventory*. In [1], `0.1/en/0x91-Appendix-B_Proof-Mechanism-Inventory.md`.

[12] Proof-of-Control Initiative. Evidence claim schema and canonicalization. In [1], `schema/poc-evidence.schema.json`, `schema/poc-evidence.cddl`, and `schema/canonicalization.md`.

[13] Proof-of-Control research programme. *Proposal: normative changes to C5 Identity for accountable unlinkability (P05)*. In [1], `docs/proposals/P05-unlinkable-identity.md`. Status: proposal, not adopted text. Cited for the finding that a persistent principal is mandatory in the current schema, and for the proposed suspension of that requirement.

[14] Proof-of-Control research programme. *Proposal: normative changes for message-to-effect binding (P02)*. In [1], `docs/proposals/P02-effect-binding.md`. Status: proposal, not adopted text.

[15] H. Birkholz, D. Thaler, M. Richardson, N. Smith, and W. Pan. *Remote ATtestation procedureS (RATS) Architecture*. RFC 9334, Internet Engineering Task Force, 2023. https://datatracker.ietf.org/doc/html/rfc9334.

[16] Proof-of-Control Initiative. *C10 Conformance and Disclosure*. In [1], `0.1/en/0x10-C10-Conformance-and-Disclosure.md`. Cited for trust-assumption disclosure as the place residual parties are named. The disclosure format itself is open as Appendix D issue 7 [4].

[17] Proof-of-Control Initiative. *Introduction*. In [1], `docs/introduction.md`. States that the standard answers whose agent ran, what it was allowed to do, whether it stayed inside those controls, and whether it can be attributed when it did not. States the technology-neutral and vendor-neutral principles this paper relies on: the missing check is an evidence shape, not a mandated product.

[18] Ken Huang. *MAESTRO Framework: Navigating Risks in Multi-Agent AI Systems*. Cloud Security Alliance, 6 February 2025. https://cloudsecurityalliance.org/blog/2025/02/06/agentic-ai-threat-modeling-framework-maestro. The draft adopts this stack as C9, `0.1/en/0x10-C09-System-Surface-MAESTRO.md`. Identity and delegation sit on the layer the inventory calls L7 [11].

[19] OWASP Foundation. Material cited by C4 and C6 in [1]: *OWASP Top 10 for Agentic Applications*, https://genai.owasp.org/, and *Artificial Intelligence Security Verification Standard (AISVS)*, https://github.com/OWASP/AISVS. The draft's README describes its AISVS coverage figures as a provisional single-coder coding.

[20] Scott Rose, Oliver Borchert, Stu Mitchell, and Sean Connelly. *Zero Trust Architecture*. NIST Special Publication 800-207, 2020. https://csrc.nist.gov/pubs/sp/800/207/final. Cited because presented credentials checked at request time are the family C5's examples belong to, and because that family is the root of Hole A.

[21] Proof-of-Control Initiative. *Appendix C: Threat Model*. In [1], `0.1/en/0x92-Appendix-C_Threat-Model.md`. The draft's boundary between covered threats and out-of-scope conditions. This paper's claim is that bearer-credential presentation sits inside identity, not in the out-of-scope cell of `identity-abuse` [10].

[22] Proof-of-Control Initiative. Research-basis note for the composition requirements. In [1], `docs/research-basis.md`, as referenced from C4 and Appendix D issue 12. The draft attributes C4.1.7 and C4.1.8 to composition findings reported as SCR-Bench. This paper uses the requirement text, not a re-derivation of that benchmark.
