# The durable token is the fatal error

**Frank Dylan Rosario**  
**Dr. Lin Wang**  
**Dr. Octavia Sulea**

6 November 2026

Working paper for the Proof-of-Control working groups. Informative. The published draft remains the normative text under `0.1/en/`. The standard remains technology-neutral. The repair below is generic to declare. It holds when each act carries a fresh proof of the kind an ENI6MA / PassPlus checker produces [1] [3] [5].

## Abstract

The Proof-of-Control architecture authorizes an act with a durable token. A durable token is issued once and remains valid for a later act. Identity, authorization, the gateway, and agent-to-agent acceptance all read that token. The agent holds it, because the architecture gave it to the agent in order to act. A second agent and an outside holder present the same token. Tier 3 and Tier 4 then grade the token [11] [12].

That is the fatal error in the whole architecture. Section 2 walks each step where the agent can access a token or another secret, in the words the Standard uses for that surface and that vector. The gaps that follow are that error under different names. The repair is a per-act proof. One-shot places the proof on each interactive step and burns it before the checker accepts, so the next step receives a new proof. Oscillation places that same proof on each direction between two service processes, and the reply receives a new proof.

## 1. The fatal error, in plain English

**Durable token.** An artifact the Standard accepts as authority, which remains valid after the moment it was created and authorizes a later act. The later act can be a different command, a repeated command, or a message to another process.

The draft builds control out of durable tokens [1]:

- Identity accepts a certificate, a key, a DID, an OAuth token, a JWT, a verifiable credential, a capability URL, or a key inside an attested environment [8] [10].
- Authorization accepts that object when the signature, the expiry, the audience, and the scope match, and it accepts a session that covers later tasks [6].
- The gateway accepts a capability bound to a snapshot and releases the tool [7].
- A second agent accepts a signature under the sender's key [8].

Each of those checks can be marked pass while the token is in the holder's hands. The record then contains the token. The introduction asks whose agent ran, what it was allowed to do, and whether it stayed inside that allowance [12]. The allowance the architecture records is possession of the durable token. The agent has that possession by being the agent.

Proof-of-Control, in the draft's own terms, is Tier 3 or Tier 4 [11]. Tier 3 grades a record an outsider can check. Tier 4 grades a release that follows the check. Both tiers grade the artifact they are given. When that artifact is a durable token, the outsider checks the token and the gateway enforces the token. Provenance of a model hash, a minimized privacy log, and a hash chain still record what they record. The control path records the durable token as the act.

A sentence that says "single-use," "per-task," or "bound to a snapshot" still describes a durable token when the object remains presentable for a later act. The word changes. The architecture stays.

## 2. Broken surfaces and vectors the Standard states

The vocabulary in `docs/use-cases/THREATS.md` states, for each slug, what the threat is, what a Proof-of-Control claim addresses, and what it leaves out of scope [9]. C5, C4, C6, and C7 state where a token or a key sits [6] [7] [8] [16]. This section reads those statements in the order an agent walks them. Every step uses the same four lines.

**Surface.** The requirement or threat row the Standard states.

**Vector.** The threat the vocabulary states, the claim it states, and the out-of-scope line it states.

**Secret.** The token or other secret the agent can access at this step.

**Break.** The secret remains valid after this step and authorizes a later act. The record stores the presentation.

### 2.1 The principal's delegation enters the agent

**Surface.** C5 states the identity chain as a signed, short-lived, scoped delegation token issued to the agent. C5.1.3 requires each tool call to carry an OAuth token, a JWT, a verifiable credential, or a capability URL issued for the principal [8].

**Vector.** `identity-abuse`: an agent claims authority it was not granted. The claim the Standard states is a cryptographic identity, a principal on every action, and a delegation chain. The out-of-scope line the Standard states is credential theft and social engineering of the human [9].

**Secret.** The agent can access the delegation token and the grant it names, because the Standard assigns that token to the agent.

**Break.** The token remains valid until expiry and authorizes a later tool call. The record stores the token's issuer, audience, expiry, and principal.

### 2.2 The agent's own credential

**Surface.** C5.1.2 requires the agent to authenticate with a certificate, a key pair, or a DID, and requires the validation to be logged [8].

**Vector.** `identity-abuse`, same row. The claim is the credential check. The out-of-scope line is credential theft [9].

**Secret.** The agent can access the private key, the certificate, or the DID material in its credential inventory.

**Break.** The credential remains valid for a later authentication. The record stores a successful validation and the principal name already inside the credential.

### 2.3 The key inside the attested environment

**Surface.** C5.1.4 requires the identity credential to be held in an attested enclave or TPM [8]. Attestation records platform state [10].

**Vector.** `identity-abuse`. The claim is that a machine whose measurement misses the reference stays outside the credential. The out-of-scope line remains credential theft [9].

**Secret.** The agent process inside a matching measurement can access the key and present it.

**Break.** The key remains in that environment for a later act. The record stores the measurement and the presentation.

### 2.4 The task token in the running agent

**Surface.** C4.1.5 requires credentials issued per task, with scope and expiry bound to that task, and requires that a standing broad-scope credential stay unavailable to the agent at runtime [6].

**Vector.** `excessive-agency`: the agent can do more than its task needs. The claim the Standard states is a record of the authority exercised and a gate on over-scope calls. The out-of-scope line the Standard states is whether the grant was too broad [9].

**Secret.** The agent can access the per-task token at runtime. That is the object C4.1.5 places in the agent's hands for the task.

**Break.** Inside the task window the token authorizes a later command, including `pay invoice 1042 for 20 units` and a later amount. A PassPlus test wrote a local session of 900 seconds after `validated` became true [3]. That session is this token.

### 2.5 The token on the tool call

**Surface.** C5.1.3 puts the delegation token on the tool call. C4.2.1 validates signature, expiry, audience, and scope before execution [6] [8]. C4.1.4 stores the validated parameter digest [6].

**Vector.** `prompt-injection`: crafted input redirects the agent's objective. The claim the Standard states is a gate and a record of the out-of-bounds action. The out-of-scope line the Standard states is the injection itself, and an in-bounds harmful action [9]. `tool-misuse`: a legitimate tool used for an unintended purpose. The claim is a record of the call and its arguments. The out-of-scope line is a valid in-scope call [9].

**Secret.** The agent can access the token it places on the call, and the tool arguments beside it.

**Break.** The redirected objective presents the same token. The validation record stores a pass. The 20-unit payment and a later payment share that token while it remains inside expiry.

### 2.6 Instructions, memory, and tool secrets

**Surface.** `system-prompt-leakage`: the agent discloses its own instructions. The Standard states this row as not addressed, and states that a record of an output can still be written [9]. `memory-poisoning`: contaminated memory steers later decisions. The claim is provenance of memory writes. The out-of-scope line is a validly sourced but misleading note [9]. `supply-chain-poisoning`: compromised tools or MCP servers. The claim is an attestation of which artifact loaded. The out-of-scope line is whether an attested artifact is trustworthy [9].

**Vector.** Those three rows, as stated.

**Secret.** The agent can access its system prompt, the context and memory that hold the task token, and secrets that sit in a loaded tool or MCP configuration.

**Break.** A later act reads the same memory. The prompt and the tool secret remain available to the agent after the step that loaded them. The record can show that an output occurred.

### 2.7 The approval surface

**Surface.** C4.1.6 requires a record of the approver, the exact content presented, the decision, and the timestamp [6].

**Vector.** `approval-fatigue`: the agent games human oversight. The claim the Standard states is evidence of the raw intent presented and of the decision. The out-of-scope line the Standard states is human fatigue and social engineering [9]. `prompt-injection` remains in force on the same step [9].

**Secret.** The agent can access the content it presents, the decision it stores, and any approver session the interface holds.

**Break.** The slip remains in the record as authority for the command that follows. The slip can name 20 units while the tool bytes name another amount. The four stored fields describe the slip.

### 2.8 The gateway and the effect credential

**Surface.** C7.1.1 requires every tool invocation through an Action Interception Gateway, and states that the agent has a credential path to its tools only through that gateway [7]. C7.1.4 states three places the effect credential can sit: inside the attesting environment that emits the request, in a single-use capability bound to the snapshot digest and the target, or at an attested egress point [7].

**Vector.** `excessive-agency` and `tool-misuse`, as in steps 2.4 and 2.5. `unsafe-actuation`: the agent drives an action outside its envelope. The claim is a gate inside a signed envelope. The out-of-scope line is whether a within-envelope action is sound, and whether the envelope was set correctly [9].

**Secret.** The agent can access the delegation token it sends into the gateway. Where the agent runs inside the attesting environment of option (a), the agent can access the effect credential. Where option (b) applies, the agent can access the snapshot it submitted and the capability released for that snapshot.

**Break.** The capability remains a token until it is spent, and it authorizes the snapshot the agent composed. The gateway record stores that snapshot and the release.

### 2.9 The signing key on a message to another agent

**Surface.** C5.2.1 requires agent-to-agent messages signed by the sending agent's credential. C5.2.2 requires the receiver to validate the sender from published key material [8].

**Vector.** `insecure-inter-agent-comms`: forged, unauthenticated, or unsanctioned agent-to-agent messages. The claim the Standard states is authenticity, integrity, a signed identity, and a delegation chain. The out-of-scope line the Standard states is the latency of evidence at the boundary [9].

**Secret.** The sending agent can access the private signing key. The published key is the public half. The message body can carry the delegation token from step 2.1.

**Break.** The signing key remains the sender's for a later message. The second agent accepts the signature and the token. The record stores the sender key identifier and the signature result.

### 2.10 The next agent receives the token

**Surface.** C4.2.2 walks the delegation chain to the principal. C4.2.3 intersects scope on issuance. C4.1.7 includes upstream parameters in the next evaluation. C4.1.8 says a diagnostic output stays off the approval threshold [6].

**Vector.** `excessive-agency` and `insecure-inter-agent-comms` [9]. `context-blind-authorization`: an in-scope call in the wrong context. The claim is that the boundary held. The out-of-scope line is whether the boundary was correctly defined [9].

**Secret.** The second agent can access the signed message, the delegation token, and the upstream parameters the first agent placed on the path.

**Break.** The second agent presents that durable token for its own later act. The path record stores the schema check.

### 2.11 The file the agent can read back

**Surface.** C5.1.1 requires the execution record to carry the agent identifier and the principal identifier [8]. C2.4.1 requires minimized forms of protected data [16]. `data-exfiltration`: protected data leaves its boundary. The claim the Standard states is evidence of access and a gate on unauthorized egress. The out-of-scope line the Standard states is a covert side channel, and whether the privacy policy is adequate [9].

**Vector.** `data-exfiltration`, as stated. `audit-tampering`: a compromised host, or the agent itself, rewrites the record. The claim is a tamper-evident record generated by the mechanism. The out-of-scope line is insider compromise at the silicon level [9].

**Secret.** The agent can access whatever credential material, tool arguments, and token fields the evidence row stored, when that row is in the agent's context. The agent can place those bytes on a later in-scope call.

**Break.** An in-scope call is authorized egress under the vocabulary's own line. The stored secret remains valid for a later reader of the file.

### 2.12 The one key the Standard assigns to the gateway

**Surface.** C7.3.2 requires evidence records signed by keys the generating mechanism holds, and states that operator and agent identities stay off those keys [7]. C6.3 requires those evidence-signing keys in hardware-backed storage, with rotation and compromise lookup [16].

**Vector.** `audit-tampering` and `evidence-repudiation`. The claim is an openly checkable signature. The out-of-scope line for repudiation is a dispute about the meaning of the action [9].

**Secret.** C7.3.2 assigns the evidence-signing key to the gateway. The agent can still access every secret in steps 2.1 through 2.11. Where the witness is filed in the C6.3 inventory, the agent-side holder of that witness can access it as a durable signing secret [16].

**Break.** The log signature can be checked and still describe a durable token the agent presented. The tier grades that token.

### 2.13 The caller bit and the unexpired copy

**Surface.** C7.1.5 grades evaluation evidence when the effect channel is a separate claim [7]. `cascading-failure`: one failure propagates, or the system defaults to allow. The claim the Standard states is a record of failure and deny events, and a fail-closed top tier. The out-of-scope line the Standard states is propagation across a multi-agent system [9].

**Vector.** `cascading-failure`, as stated. `identity-abuse`'s out-of-scope line, credential theft, is the outside holder's copy of a token from the steps above [9].

**Secret.** The agent can access the decision bit it sends. On the PassPlus Authority path, consume stores `proof_ok` from the caller, and stores true when the caller sends the nonce alone [3]. An outside holder can access a copied token, session, or transcript while expiry still covers it.

**Break.** The bit and the copy remain authority for a later act. The record stores the bit or the token's signature, audience, scope, and expiry.

### 2.14 The path, in one table

| Step | Surface the Standard states | Vector the Standard states | Secret the agent can access |
| --- | --- | --- | --- |
| 2.1 Delegation in | C5.1.3 token on the agent | `identity-abuse`; credential theft stated as out of scope | Delegation token and named grant |
| 2.2 Agent credential | C5.1.2 certificate, key pair, or DID | `identity-abuse`; credential theft stated as out of scope | Private key or DID material |
| 2.3 Attested key | C5.1.4 key in enclave or TPM | `identity-abuse`; measurement of the platform | Key inside the agent's matching environment |
| 2.4 Task token | C4.1.5 per-task credential at runtime | `excessive-agency`; breadth of the grant stated as out of scope | Per-task token, including a 900-second session |
| 2.5 Tool call | C5.1.3 and C4.2.1 | `prompt-injection` and `tool-misuse`; the injection and the in-scope call stated as out of scope | Token and arguments on the call |
| 2.6 Other secrets | Prompt, memory, MCP | `system-prompt-leakage` stated as not addressed; `memory-poisoning`; `supply-chain-poisoning` | System prompt, memory copy of the token, tool or MCP secret |
| 2.7 Approval | C4.1.6 | `approval-fatigue`; social engineering stated as out of scope | Presented content, decision, approver session |
| 2.8 Gateway | C7.1.1, C7.1.4 | `excessive-agency`, `tool-misuse`, `unsafe-actuation` | Token sent in; effect credential or snapshot capability |
| 2.9 Message signature | C5.2.1, C5.2.2 | `insecure-inter-agent-comms` | Private signing key and any token in the body |
| 2.10 Next agent | C4.2.2, C4.1.7 | `excessive-agency`, `context-blind-authorization` | Signed message, delegation token, upstream parameters |
| 2.11 Evidence row | C5.1.1, C2.4.1 | `data-exfiltration`; in-scope egress stated as the gated case | Credential material stored where the agent can read it |
| 2.12 Log key | C7.3.2, C6.3 | `audit-tampering` | Evidence-signing key assigned to the gateway; witness if filed as that key |
| 2.13 Bit and copy | C7.1.5, consume path | `cascading-failure`; credential theft stated as out of scope | Caller `proof_ok`; copied token inside expiry |

## 3. The major gaps are that one error

Every gap uses the same problem statement. The name of the durable token changes. The later act in the examples is the command `pay invoice 1042 for 20 units from account A to account B`, and any command after it.

**Problem.** The Standard accepts this artifact as a durable token. The token remains valid after it is created and authorizes a later act. The holder presents the token, and the record stores the fields named here.

### 3.1 Presented credential

**Targets.** C5.1.2, C5.1.3, C5.1.4, C4.2.1 [6] [8] [10].

**Problem.** The Standard accepts a presented credential as a durable token. The token remains valid after it is created and authorizes a later act. The holder presents the token, and the record stores the credential identifier, the signature result, the expiry, the audience, the scope, the principal name inside the credential, and any platform measurement.

The credential is a certificate, a key pair, a DID, an OAuth token, a JWT, a verifiable credential, a capability URL, or the same key presented from inside an attested environment. Audience and expiry set the window. Inside the window the agent presents the token for the 20-unit payment and for a later payment. The measurement records platform state [10]. The record stores a valid credential and a named principal [8].

### 3.2 Approval slip

**Targets.** C4.1.6. Threats `approval-fatigue`, `prompt-injection` [6] [9].

**Problem.** The Standard accepts an approval record as a durable token. The token remains valid after it is created and authorizes a later act. The holder presents the token, and the record stores the approver, the content presented, the decision, and the timestamp.

The agent holds the screen and the tool bytes. The slip can name 20 units while the command names another amount. The four stored fields describe the slip. The command that runs is the later act.

### 3.3 Session after one check

**Targets.** C4.1.5 [6].

**Problem.** The Standard accepts a session credential as a durable token. The token remains valid after it is created and authorizes a later act. The holder presents the token, and the record stores the session identifier, the expiry, and the scope.

One check opens the session. The agent spends it on later tool calls. A PassPlus test wrote a local session of 900 seconds after `validated` became true [3]. That session is a durable token for every command inside the window. The first check's bytes stay on the first command.

### 3.4 Gateway capability

**Targets.** C7.1.1, C7.1.4, C7.1.5, C4.1.3 [6] [7].

**Problem.** The Standard accepts a capability bound to a snapshot as a durable token. The token remains valid after it is created and authorizes a later act. The holder presents the token, and the record stores the snapshot digest, the target resource, and the gateway release.

The capability can be single-use and still be a token the agent composed. The gateway checks the snapshot. The tool runs. The record stores the snapshot the holder presented.

### 3.5 Caller yes-bit

**Targets.** C7.1.5, C7.5, C8 [3] [7] [11].

**Problem.** The Standard accepts a caller decision bit as a durable token. The token remains valid after it is created and authorizes a later act. The holder presents the token, and the record stores the bit.

On the PassPlus Authority path, consume stores `proof_ok` from the caller. When the caller sends the nonce alone, the stored value is true [3]. The agent is a sufficient caller. The record stores a pass. An outsider who reads the bit learns that the caller emitted it [7] [11].

### 3.6 Unexpired replay

**Targets.** C4.1.5, C7.1.4(b) [6] [7].

**Problem.** The Standard accepts a prior envelope inside its expiry as a durable token. The token remains valid after it is created and authorizes a later act. The holder presents the token, and the record stores the signature result, the audience, the scope, and the expiry.

The second submission of the 20-unit payment matches the same checks as the first. Expiry is the lifetime of the durable token.

### 3.7 Next call in the chain

**Targets.** C4.1.7 [6].

**Problem.** The Standard accepts upstream tool-schema parameters as a durable token. The token remains valid after it is created and authorizes a later act. The holder presents the token, and the record stores the path parameters and the schema check.

The first command is the 20-unit payment. The agent composes a wider second command. The path check records the schemas. The second command proceeds on the first permission.

### 3.8 Secret written into the file

**Targets.** C2.4.1, C5.1.1 [8] [16].

**Problem.** The Standard accepts stored credential material as a durable token. The token remains valid after it is created and authorizes a later act. The holder presents the token, and the record stores the credential material the checker used.

The evidence row keeps the material that was validated. A later reader of the file holds what the row stored. Bearings, which are the response, and the witness, which is the secret, share the file when the pipeline stores the secret configuration.

### 3.9 Local checker bit

**Targets.** C5, C8 [8] [11].

**Problem.** The Standard accepts a local checker result as a durable token. The token remains valid after it is created and authorizes a later act. The holder presents the token, and the record stores the operator's `validated` bit.

The checker image is the one the operator ran. The bit remains in the record as authority for the act. The anchored fingerprint of the checker is a separate field from that bit.

### 3.10 One key for the log and the witness

**Targets.** C6.3, C6.3.5, C2.1.2 [16].

**Problem.** The Standard accepts one key inventory as a durable token. The token remains valid after it is created and authorizes a later act. The holder presents the token, and the record stores one class covering the log-signing key, the possession witness, and one disclosure cell for the signature margin and the enrollment-seal margin.

C6.3 states hardware generation, rotation, compromise lookup, and a long-retention signature margin for the key that signs the log [16]. Applied to the witness, that inventory makes the witness a durable signing secret, or it grades the witness as if it were that secret. The seal's confidentiality margin and the log's signature margin then share one cell [3].

### 3.11 The tier grades the token

**Targets.** C8 [11] [12].

**Problem.** The Standard accepts the artifact in sections 3.1 through 3.10 as a durable token. The token remains valid after it is created and authorizes a later act. The holder presents the token, and the record stores that artifact at the tier the deployment claims.

Tier 3 checks the token. Tier 4 releases on the token. The grade follows the artifact the architecture defined as authority.

### 3.12 A second agent

**Targets.** C5.2.1, C5.2.2, C4.2.2 [6] [8].

**Problem.** The Standard accepts an agent-key signature as a durable token. The token remains valid after it is created and authorizes a later act. The holder presents the token, and the record stores the sender key identifier, the signature result, and any onward delegation.

The signing key remains the sender's across messages. The second agent validates the key and runs the command, or delegates onward [6]. This is the smaller case. The second agent receives a durable token the first agent already held.

### 3.13 An outside holder

**Targets.** C5.1.3, C8 [3] [8] [11].

**Problem.** The Standard accepts a copied presentation as a durable token. The token remains valid after it is created and authorizes a later act. The holder presents the token, and the record stores the copied credential, the copied session, the copied transcript, the substituted checker bit, or the stored success bit.

The outside holder succeeds by presenting an artifact the architecture already treats as authority. A copied token passes the identity check inside its expiry [8]. A consume call that sends the nonce alone stores `proof_ok` as true [3].

### 3.14 Three companion records

These three sit beside the durable-token error. Each uses the same problem statement. Each keeps a second record in the repair.

**Endpoint effect. Targets: P02 [14] [15].** The Standard accepts a checked request as a durable token. The token remains valid after it is created and authorizes a later act. The holder presents the token, and the record stores the request digest. The endpoint may apply a default, an alias, or unsigned state to that request. The applied effect is a further record.

**Profile token. Targets: P05, C5.1.1, Appendix D issue 2 [13].** The Standard accepts a session pseudonym as a durable token. The token remains valid after it is created and authorizes a later act. The holder presents the token, and the record stores the pseudonym. The profile names a stand-in for the principal. The act still proceeds on a presentation the holder carries.

**Inventory row. Targets: Appendix B [1].** The Standard accepts the nearest listed mechanism as a durable token. The token remains valid after it is created and authorizes a later act. The holder presents the token, and the record stores that row: a signature, a formal proof, a zero-knowledge proof, a remote attestation, a hash chain, a multiparty computation, a supply-chain attestation, a commitment, a verifiable computation, or a verifiable credential. A verifiable credential is a durable token. A commitment row stores a hidden value and leaves the fresh step, the response, and the burn for the repair to add.

## 4. The repair, in plain English

**Per-act proof.** Authority for this act is a proof of this act's exact bytes. The proof binds those bytes, a fresh nonce, and the fingerprint of the anchored checker. The ledger burns the nonce before the checker accepts. The checker returns one terminal decision. The witness remains inside the protected boundary. The released record holds the challenge digest, the masked-response digest, the checker digest, and the nonce identifier. The durable token is a presentation beside that record. The next act receives a new proof.

The shared proof is a private-reference check [2]. Setup places the enrolled credential and the private naming map inside a protected boundary. The act selects a challenge. The prover locates the secret symbol. A private dictionary turns that region into a response label. A fresh mask is applied before release. The checker returns one decision. The released view is the challenge, the masked response, and the decision. A legal name, a hardware measurement, and the endpoint's applied effect are further contracts on that decision [2] [10] [14].

PassPlus runs the human-facing check on device. A pinned `wasm32-wasip1` guest issues a challenge and returns one decision on the bearings. A local grant is written when the decision is accept. Enrollment plaintext is sealed. Authority rows store hashes and sealed bytes. Web, extension, and iOS run that on-device path [3].

**One-shot (interactive step rounds).** Each interactive step is one act under the per-act proof. The allocator reserves the step. The proof binds that step's bytes. The ledger burns the nonce before the checker accepts. The next interactive step is a new reservation, a new binding, and a new burn. A retry may resend the ciphertext already bound to the spent step. A changed amount, a changed destination, or a new command is a new step [4] [5].

The API protocol uses this shape for a tool call, a payment, a webhook, and a scheduled pull [5]. The child circuit is minted for one endpoint and one policy, and its hash is the anchored fingerprint. The caller binds the request hash and the policy hash. The server burns the nonce, checks the proof, applies the policy, executes, and writes a result hash. The protocol implements challenge, respond, validate, and ledger nonce burn. Future-time reservation and the service check of `request_hash` are in formalization [5].

**Oscillation (the same proof between two service processes).** Each direction between the two processes is one one-shot act. Process A binds the bytes of its message. Process B burns the nonce before the checker accepts. Process B's reply is the next act, with a new reservation, a new binding, and a new burn. The two directions share the ceremony time and the geometry. Each direction has its own allocation [4]. A new exchange opens with the witness. The protocol marks the continuous form of this exchange as proposed and partial [5]. A party that already sits inside a running endpoint while that endpoint holds an ignited circuit shares the current allocation until that allocation ends [5].

**Worked payment.** The command is `pay invoice 1042 for 20 units from account A to account B`. Under the draft, a session token from an earlier check authorizes this payment and a later payment of 20,000 units. Under one-shot, interactive step 1 binds the 20-unit bytes, the ledger burns that nonce, and the checker decides before any transfer. Interactive step 2, the 20,000-unit command, is a new proof and a new burn. Under oscillation, the billing service sends the 20-unit command to the payment service as one direction, burned before the payment service accepts it. The payment service's reply is a new act. A later amount is a new direction between the two processes.

**Why the declaration needs this construction.** C4.1.5, C7.1.3, C7.1.4(b), C4.2.1, and a hash chain can be written as requirements today [6] [7]. They hold as a repair of the durable token when the authority input is the per-act proof: a witness inside a protected boundary, a checker whose fingerprint is anchored, and a burn completed before the decision. PassPlus is the on-device checker [3]. One-shot is that checker on each interactive step [5]. Oscillation is that same checker on each direction between two service processes [4] [5]. A ledger that burns a caller-supplied bit records a durable yes. The burn that repairs the architecture is the burn of this act's proof.

## 5. The same repair on each gap

Every row uses the same solution statement.

**Solution.** This act carries a per-act proof of its own bytes. One-shot burns that proof on this interactive step, and the next step receives a new proof. Oscillation burns that same proof on this direction between the two service processes, and the reply receives a new proof.

| Gap | Durable token the Standard accepts | Solution |
| --- | --- | --- |
| 3.1 Presented credential | Certificate, key, DID, OAuth token, JWT, verifiable credential, capability URL, or attested-environment presentation | This act carries a per-act proof of its own bytes. One-shot burns that proof on this interactive step, and the next step receives a new proof. Oscillation burns that same proof on this direction between the two service processes, and the reply receives a new proof. |
| 3.2 Approval slip | Approver, presented content, decision, timestamp | This act carries a per-act proof of its own bytes. One-shot burns that proof on this interactive step, and the next step receives a new proof. Oscillation burns that same proof on this direction between the two service processes, and the reply receives a new proof. |
| 3.3 Session | Session identifier, expiry, scope, including a 900-second local session | This act carries a per-act proof of its own bytes. One-shot burns that proof on this interactive step, and the next step receives a new proof. Oscillation burns that same proof on this direction between the two service processes, and the reply receives a new proof. |
| 3.4 Gateway capability | Snapshot digest, target resource, release decision | This act carries a per-act proof of its own bytes. One-shot burns that proof on this interactive step, and the next step receives a new proof. Oscillation burns that same proof on this direction between the two service processes, and the reply receives a new proof. |
| 3.5 Caller yes-bit | `validated` or `proof_ok`, stored true when the caller sends the nonce alone | This act carries a per-act proof of its own bytes. One-shot burns that proof on this interactive step, and the next step receives a new proof. Oscillation burns that same proof on this direction between the two service processes, and the reply receives a new proof. |
| 3.6 Replay | Prior envelope inside its expiry | This act carries a per-act proof of its own bytes. One-shot burns that proof on this interactive step, and the next step receives a new proof. Oscillation burns that same proof on this direction between the two service processes, and the reply receives a new proof. |
| 3.7 Next call | Upstream tool-schema parameters | This act carries a per-act proof of its own bytes. One-shot burns that proof on this interactive step, and the next step receives a new proof. Oscillation burns that same proof on this direction between the two service processes, and the reply receives a new proof. |
| 3.8 Secret in the file | Credential material stored in the evidence row | This act carries a per-act proof of its own bytes. One-shot burns that proof on this interactive step, and the next step receives a new proof. Oscillation burns that same proof on this direction between the two service processes, and the reply receives a new proof. |
| 3.9 Local checker | Operator `validated` bit | This act carries a per-act proof of its own bytes. One-shot burns that proof on this interactive step, and the next step receives a new proof. Oscillation burns that same proof on this direction between the two service processes, and the reply receives a new proof. |
| 3.10 One key class | Log key, witness, and seal margin in one inventory | This act carries a per-act proof of its own bytes. One-shot burns that proof on this interactive step, and the next step receives a new proof. Oscillation burns that same proof on this direction between the two service processes, and the reply receives a new proof. |
| 3.11 Tier grade | Whichever token sections 3.1–3.10 stored | This act carries a per-act proof of its own bytes. One-shot burns that proof on this interactive step, and the next step receives a new proof. Oscillation burns that same proof on this direction between the two service processes, and the reply receives a new proof. |
| 3.12 Second agent | Agent-key signature and onward delegation | This act carries a per-act proof of its own bytes. One-shot burns that proof on this interactive step, and the next step receives a new proof. Oscillation burns that same proof on this direction between the two service processes, and the reply receives a new proof. |
| 3.13 Outside holder | Copied credential, session, transcript, checker bit, or stored success bit | This act carries a per-act proof of its own bytes. One-shot burns that proof on this interactive step, and the next step receives a new proof. Oscillation burns that same proof on this direction between the two service processes, and the reply receives a new proof. |

Companion records, in the same plain English:

| Gap | Companion record beside the per-act proof |
| --- | --- |
| 3.2 Approval slip | Where the shown sentence and the command bytes differ, the record contains a published function from the sentence to the bytes, and an auditor recomputes it. |
| 3.8 and 3.10 | The released row holds the four digests. The witness remains inside the protected boundary. The evidence-signing key is its own class under C6.3. The enrollment seal records its recipient, its encapsulation, and its confidentiality margin in its own cell. Re-enrollment is the witness procedure [3] [16]. |
| 3.12 and 3.13 | Two processes that share a current ignited allocation record that allocation as the live act. A new direction records a new per-act proof. A new exchange opens with the witness [5]. |
| 3.14 Endpoint | The endpoint record contains a published mapping from the proved bytes to the applied effect. Exactly-once execution at that endpoint is a separate record [14] [15]. |
| 3.14 Profile | A signed profile token names the profile. The possession-bound value records the principal reference. The unlinkable value records a session pseudonym and an opening policy. A Level 1 opening records a declared policy and grades that action class at Tier 2 [13]. |
| 3.14 Inventory | Appendix B records an interactive per-act proof row. The one-shot cell is interactive step rounds. The oscillation cell is the same proof between two service processes. The device-local cell records the PassPlus checker at Tier 2. The Tier 3 cell records outsider recomputation from the published commitment, the challenge, the masked response, and the checker digest [3] [11]. |

## 6. What the groups would write

1. A controlled command and a controlled agent message each carry a per-act proof of their own bytes.
2. The ledger burns that nonce before the checker accepts. The burned nonce remains the spent record of that act.
3. One-shot applies the proof to each interactive step. The next step receives a new proof.
4. Oscillation applies the same proof to each direction between two service processes. The reply receives a new proof.
5. The witness remains inside the protected boundary. The evidence-signing key remains its own inventory class.
6. A conformance claim records Proof-of-Control on each path whose messages and commands carry this proof [11].

Items 1, 2, 3, and 5 match the implemented one-shot path: challenge, respond, validate, and ledger nonce burn, with the PassPlus checker as the on-device decision [3] [5]. Item 4 matches the specified oscillation between two service processes. The continuous exchange remains proposed and partial [5].

## 7. Conclusion

The architecture's fatal error is the durable token. The Standard issues a credential, a session, an approval slip, a snapshot capability, a caller bit, an unexpired envelope, a path permission, a stored secret, a local yes, a signing key, or an agent signature, and that object authorizes a later act. The agent holds the object. A second agent and an outside holder present it. The tiers grade it.

The repair is one per-act proof in two placements. One-shot burns the proof on each interactive step, and the next step receives a new proof. Oscillation burns that same proof on each direction between two service processes, and the reply receives a new proof. The construction that produces the proof is an ENI6MA / PassPlus checker: the witness stays inside the protected boundary, the checker fingerprint is anchored, and the burn completes before the decision [2] [3] [5]. A control record that still contains a durable token as its authority is a record of the error.

## References

[1] Advanced AI Society and the Proof-of-Control Initiative. *Open Verification: the Proof-of-Control Standard for Agents*. Working Draft v0.1. https://github.com/LFDT-ProofOfControl/ov-poc-standard. Normative files under `0.1/en/`.

[2] Frank Dylan Rosario and Dr. Lin Grant Wang. *Perfect Geometric Proof of Identity*. Formal evidence preprint, 18 September 2026. Local copy: `LEAN4-PUBLISH/01-CORE-FORMAL/CORE-02-comprehensive-native-evidence/source/PERFECT_GEOMETRIC_PROOF_OF_IDENTITY.md`. The declared channel is the challenge, the masked response, and one terminal decision. The witness remains inside the protected boundary.

[3] ENI6MA. *Pass+ and ENI6MA Sequoia architecture*, 2 October 2026, `PASS PLUS/Docs/SYSTEM/ARCHITECTURE.md`, and *Login ceremony*, `PASS PLUS/Docs/SYSTEM/lifecycles/login-ceremony.md`. On-device guest. Local grant when `validated` is true. Authority rows store hashes and sealed bytes. Web, extension, and iOS run the on-device challenge and validate path. Authority consume stores the caller's `proof_ok`, and stores true when the caller sends the nonce alone.

[4] Frank Dylan Rosario. *Geometric One-Time Pads*, section "Paired-clone oscillation and durable consumption." Review manuscript, 5 November 2026. Local copy: `BOOK-PUBLISH/_ZENODO-WHITE-PAPERS-2026-11-05-r4/papers/geometric-one-time-pads/source/manuscript.md`. Ordered alternation. Separate allocation per direction. Consumption before the check.

[5] ENI6MA. *API authentication protocol V3*. Local copy: `LEAN4-PUBLISH/03-TECHNICAL-SYSTEMS/TECH-06-api-auth-pii/source/ENI6MA_API_AUTH_PROTOCOL_V3.md`. One-shot path: challenge, respond, validate, ledger nonce burn. Oscillation between two processes: proposed and partial. A party inside a running endpoint that holds an ignited circuit shares the current allocation.

[6] Proof-of-Control Initiative. *C4 Authorization*. In [1], `0.1/en/0x10-C04-Authorization.md`. C4.1.3, C4.1.5, C4.1.6, C4.1.7, C4.2.1, C4.2.2.

[7] Proof-of-Control Initiative. *C7 Evidence Generation and Properties*. In [1], `0.1/en/0x10-C07-Evidence-Generation-and-Properties.md`. C7.1.1, C7.1.3, C7.1.4, C7.1.5, C7.3.2, C7.5.

[8] Proof-of-Control Initiative. *C5 Identity*. In [1], `0.1/en/0x10-C05-Identity.md`. C5.1.1 through C5.1.4, C5.2.1, C5.2.2.

[9] Proof-of-Control Initiative. *Threat vocabulary*. In [1], `docs/use-cases/THREATS.md`. Each row states the threat, what a Proof-of-Control claim addresses, and what it leaves out of scope. Rows used here: `prompt-injection`, `system-prompt-leakage`, `memory-poisoning`, `supply-chain-poisoning`, `identity-abuse`, `context-blind-authorization`, `excessive-agency`, `insecure-inter-agent-comms`, `tool-misuse`, `unsafe-actuation`, `data-exfiltration`, `audit-tampering`, `cascading-failure`, `evidence-repudiation`, `approval-fatigue`.

[10] H. Birkholz, D. Thaler, M. Richardson, N. Smith, and W. Pan. *Remote ATtestation procedureS (RATS) Architecture*. RFC 9334, 2023. https://datatracker.ietf.org/doc/html/rfc9334. Attestation records platform state.

[11] Proof-of-Control Initiative. *C8 Verifiability Tiers*. In [1], `0.1/en/0x10-C08-Verifiability-Tiers.md`. Proof-of-Control is Tier 3 or Tier 4.

[12] Proof-of-Control Initiative. *Introduction*. In [1], `docs/introduction.md`. The standard records whose agent ran, what it was allowed to do, and whether it stayed inside that allowance.

[13] Proof-of-Control research programme. *P05 unlinkable identity*. In [1], `docs/proposals/P05-unlinkable-identity.md`. The unlinkable profile records a session pseudonym and an opening policy. A summary is `SUMMARY/2026-11-06-p05-unlinkable-identity.md`.

[14] Proof-of-Control research programme. *P02 effect binding*. In [1], `docs/proposals/P02-effect-binding.md`. The endpoint record contains a published mapping from the proved bytes to the applied effect.

[15] Frank Dylan Rosario, Dr. Lin Wang, Dr. Francisco Perez, and Dr. Octavia Sulea. *Authorization Beyond Consensus*. Review manuscript, 5 November 2026. Local copy: `BOOK-PUBLISH/_ZENODO-WHITE-PAPERS-2026-11-05-r4/papers/authorization-beyond-consensus/source/manuscript.md`. Spent-event handling and exactly-once execution at the far system are separate records.

[16] Proof-of-Control Initiative. *C2 Privacy* and *C6 Security*. In [1], `0.1/en/0x10-C02-Privacy.md` (C2.4.1) and `0.1/en/0x10-C06-Security.md` (C6.3). Minimized evidence. Evidence-signing keys form their own inventory class.
