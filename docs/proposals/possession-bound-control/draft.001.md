# Review of delegation credentials and authorization for individual agent actions

**Frank Dylan Rosario**  
**Dr. Lin Wang**  
**Dr. Octavia Sulea**

6 November 2026  
Normalized descriptive version 2

Informative review of Working Draft v0.1 of *Open Verification: the Proof-of-Control Standard for Agents*. The byline is retained from the supplied review. This revision does not record a new approval by the named authors. The standard's requirements remain in `0.1/en/`; this paper proposes clarifications and additional evidence requirements.

The review uses the local standard repository at commit `54a7bc67140b39c9107216cd390dd47c1d42946d`. References to the standard below identify that revision. The ENI6MA references are local manuscripts and architecture documents. Their implementation statements are attributed to those documents. This editorial review includes no new deployment test, cryptographic proof, or performance benchmark.

## Abstract

The standard requires an agent's tool requests to include evidence of delegated authority. It also specifies permission checks, approval records, protection of selected keys, mediation of execution, and signed evidence. These controls establish different facts. A credential may identify the principal that granted authority. A permission check determines whether a request is allowed. An approval record describes what an authenticated approver accepted. None of these facts, considered alone, establishes that a particular person approved every parameter of the current request.

This review examines where a deployment may expose a reusable credential and where the evidence for a particular action may be incomplete. The analysis distinguishes an exportable bearer token from a protected private key, an approval record, a single-use capability, and an evidence signature. The standard already requires several controls that can reject modified or repeated requests. Consequently, the existence of a delegation token does not establish that every conforming deployment permits the same misuse.

The proposed addition is a defined profile for authorization of individual actions using evidence from a protected witness. A witness is secret information used by a proof protocol. The profile would specify the exact request, the authorized principal, the verifier, a unique event identifier, the permitted use of the response, and the condition for execution. Its security would depend on the complete protocol and implementation. The ENI6MA documents provide relevant design material, with explicit limits concerning request authentication, human attribution, independent verification, and execution. The recommended contribution is a precise specification and corresponding tests for those properties.

## 1. What the standard's delegation requirements establish

### 1.1 Actors, data, and operations

In this review, a **principal** is the person or organization on whose behalf an agent is authorized to act. An **agent runtime** is the software that receives model output, prepares requests, and invokes tools. The **model context** is the text or other input sent to the language model for an inference. The runtime and the model context are separate locations. A runtime can attach a credential to a request without including that credential in the model's input.

A **delegation credential** records authority granted by a principal or by a service acting for that principal. A **bearer token** is a credential whose possession is sufficient for its use, subject to the receiving service's checks. A copied bearer token can therefore be usable by another holder while the token remains valid. This is the bearer property described in RFC 6750. It does not describe every credential format or authentication protocol. [14]

A **private key** is secret cryptographic data used to perform operations such as signing. A certificate associates a public key with information certified by its issuer. A decentralized identifier identifies a subject under its associated identification method. A certificate or identifier is not itself the private key. A service may permit an agent to request a signing operation while preventing the agent from reading the key.

A **verifier** is the component that checks supplied evidence. A **gateway** is a component through which requests must pass before a tool executes them. An **endpoint** is the receiving service that performs the requested operation. These components may have different permissions, storage, and responsibilities. The analysis must identify which component possesses each credential and which component decides whether execution is allowed.

### 1.2 Delegation and approval of a particular request

The identity figure in [C5 Identity][c5] depicts a principal issuing a signed delegation token with an expiration time and a limited scope. C5.1.1 requires an execution record to identify the agent and principal. C5.1.2 requires credential validation. C5.1.3 requires a delegation token on each tool call and links that token to the principal's grant. These requirements support attribution to an identity and to a grant of authority. [8]

The introductory text of C5.1 uses the phrase "explicitly bind agent tool calls back to human intent." The evidence described in C5 must be interpreted with the authorization requirements in [C4][c4]. A principal may intentionally approve a task that permits several later actions. A valid task credential can establish that delegation. It does not, without additional evidence, establish a new human approval of each later action.

The distinction matters when a deployment claims that a particular person approved the exact amount, recipient, and operation in a request. That claim requires evidence connecting the approval to those values. C4.1.6 requires a record of the authenticated approver, the displayed content, the decision, and its time. Its auditor guidance also requires checking that the displayed content matches the executed action. The review therefore cannot correctly describe the draft as omitting that comparison altogether. The remaining specification question is how the deployment authenticates and verifies that correspondence. [6]

### 1.3 Example: two payment requests under one delegation

**Definition and context.** A payment service transfers accounting units between accounts. An accounting unit is the integer unit used by this example; no currency or exchange rate is implied. Invoice 1042 is the identifier in the payment record. Account A is the payer and account B is the recipient. Request A specifies a payment of 20 units. Request B specifies a payment of 20,000 units. All other request fields are equal.

**Inputs and assumptions.** The principal grants the agent permission to submit payments to that service from 10:00 until 10:15 on the same day. The example assumes the grant allows both amounts, does not require a separate human approval for each payment, and does not impose a lower amount limit. It also assumes no invoice-duplication rule prevents the second request. The credential is a reusable bearer token. These are example assumptions, not requirements imposed by the standard.

**Action and check.** At 10:01 the agent submits request A. At 10:04 it submits request B. For each request, the service validates the credential and evaluates the request against the grant. The signature, receiving service, expiration time, and permissions satisfy the assumed policy for both requests. The service records the principal associated with the grant.

**Result.** Both requests can be accepted under this policy. The resulting records establish that the requests used the principal's delegated authority. The records do not establish that the principal separately approved each amount.

**Limit.** A policy restricting payments to 20 units, requiring a new approval, or rejecting duplicate invoice payments changes the outcome. C4.1.2 requires evaluation against the grant, and C4.1.3 requires blocking requests outside its scope at the specified level. An approval mismatch also conflicts with the C4.1.6 auditor check. This example demonstrates the consequence of the assumed grant and policy. It does not demonstrate unavoidable acceptance of request B under full conformance. [6]

### 1.4 Credential exposure and model access

If a runtime can read an exportable bearer token, code with equivalent access may be able to copy the token into another buffer, file, or request. Whether the language model can cause that operation depends on the available tools, permissions, and filtering. Whether a later recipient can use the copy depends on the credential and service controls.

C5.1.3 specifies that a tool call carries a delegation token. That requirement does not specify that the model generates the token, sees the token, or stores the token in its context. A transport component could attach the credential after the model has generated the tool arguments. The security assessment must inspect the actual data transfer between components before describing model exposure as an observed fact.

Similarly, C5.1.4 requires the identity credential to be associated with an attested execution environment, with the key held in an enclave or a trusted platform module. Attestation is evidence about an execution environment according to the selected mechanism. Key custody determines whether the private key can be read. Permission to invoke a protected operation determines which requests the agent can cause that mechanism to process. Key extraction and misuse of permitted operations are separate failure conditions. [8]

### 1.5 What the threat vocabulary covers

The [threat vocabulary][threats] separates a threat, the evidence or enforcement addressed by the standard, and matters outside its stated scope. For `prompt-injection`, the standard addresses the attempted action and enforcement of its authorization limits. It does not claim to prevent the injected instruction itself. For `excessive-agency`, it addresses the authority exercised and actions exceeding that authority. It does not decide whether the original grant was too broad. [9]

These scope limits leave application owners responsible for choosing suitable permissions. A harmful request can satisfy an incorrectly chosen permission set. Conversely, an injected instruction does not establish that the agent can bypass a correctly enforced permission check. The credential, policy, and execution mechanism must be examined together.

The vocabulary's `system-prompt-leakage` entry does not claim prevention of instruction disclosure. That omission supplies no evidence that a credential is stored with those instructions. Credential disclosure requires a separate description of the storage location, reader, and permitted output operation.

### 1.6 Processing cost and evidence required for a performance claim

The standard specifies work associated with each action. C4 includes permission evaluation, parameter validation, and applicable delegation checks. C7.1.2 requires signed evidence at request receipt, effect performance, and result return. C7.1.3 requires durable storage of the record created before execution as a condition of forwarding the request. A durable record is one retained according to the storage system's persistence guarantees. [6] [7]

The following distinctions determine what can be concluded about cost:

| Requirement or operation | Work the source describes | Measurement or deployment fact still needed |
| --- | --- | --- |
| Credential and permission checks | Validate credentials and evaluate each request | Algorithms, reuse of prior verified results where permitted, and processing time |
| C4.1.7 execution context | Include relevant parameters and state from previous invocations in authorization evaluation | Representation, size limits, and whether any of this data enters model input |
| C7.1.1 separate process or service | Mediate tool requests outside the agent process | Same-host communication or remote deployment, and communication delay |
| C7.1.2 three signed records | Record three stages of an action | Signing cost and which work occurs before or after the effect |
| C7.1.3 durable record before forwarding | Wait for the required storage operation before forwarding | Storage configuration, contention, and delay under failure |
| Hardware attestation | Obtain and refresh evidence about the environment | Refresh interval and cost of the selected implementation |

An authorization context is data used by the policy evaluator. It is not necessarily the model context. A separate process need not reside on another computer. The requirement for three records also does not mean all three records are stored before execution; the second and third describe later events.

C7 includes reported implementation timings and a discussion of attestation refresh intervals. Those reports are source claims, not benchmarks reproduced in this review. C8's statement about five deployment descriptions appears in its discussion of a proposed trust classification. It should not be expanded into a claim that the repository contains no implementation measurements. [7] [10]

A performance comparison with authorization using a separate proof for each action must measure equivalent work. Relevant quantities include proof generation, request encoding, verification, durable event consumption, communication, evidence storage, and endpoint execution. The ENI6MA formal manuscript also states that abstract check counts do not establish constant processing cost or a latency advantage. [2] The available review evidence does not support declaring either architecture incapable of production use or universally faster than the other.

## 2. Credential access and misuse conditions at each stage

Each stage below identifies the specified operation, the data involved, the condition for exposure or misuse, and the resulting question for a deployment review. A possible access route is not described as a confirmed disclosure.

### 2.1 Issuing a delegation credential

C5.1.3 associates a tool call with a credential issued by or for the principal. In a bearer implementation, the receiving component stores or obtains token bytes that can be presented to the service. If the agent runtime can read those bytes and write unrestricted output, it may disclose them. If a separate component attaches them without exposing them to the agent, that particular disclosure route is absent. The implementation must document the actual holder and readers. [8]

### 2.2 Authenticating the agent

C5.1.2 validates the credential used for authentication. An exportable private key can be copied by a process that can read it. A non-exportable key can instead support operations through a restricted interface. The assessor must determine which condition applies and what the interface allows. A certificate, a public identifier, a signature, and a private key must be recorded as different data types. Storing a validation result does not inherently store the private key. [8]

### 2.3 Using an attested environment

C5.1.4 restricts credential use to an environment satisfying the attestation requirement. That restriction can prevent use from an unacceptable environment. The remaining questions concern the code authorized to invoke the key, the permitted operation parameters, and the information returned by the protected component. A copied output may or may not be reusable, depending on its request and event binding. The environment's measurement alone does not answer those questions. [8]

### 2.4 Retaining authority during a task

C4.1.5 requires credentials scoped to a task and an expiration time, and excludes standing broad credentials at runtime. A task may legitimately contain several operations. If its credential permits repeated requests, the agent can use it until expiration or another restriction applies. The review must state the task's permitted operations and limits before evaluating whether reuse is excessive. The existence of an expiration time reduces the duration of permitted use; it does not by itself limit the use count. [6]

### 2.5 Constructing and transmitting a tool request

C4.2.1 validates the signed authorization token before execution. A component preparing or receiving the request may have access to its credential field. Disclosure requires an additional condition, such as logging that field, retaining it in an accessible retry buffer, or returning it in a tool response. Encrypted transport and credential redaction affect who can recover it. A token carried in an encrypted request must not be described as publicly readable merely because the recipient can decode it. [6] [8]

### 2.6 Obtaining human approval

C4.1.6 records the approver, displayed content, decision, and time, and its audit guidance compares displayed and executed content. A vulnerable implementation could allow an agent to change execution parameters after approval without invalidating the approval. That would indicate a failed correspondence check. The approval interface's ownership, authenticated display data, and relationship to the executed request therefore need explicit evidence. An approval record becomes a reusable authorization artifact only if some component accepts it for that purpose. [6]

### 2.7 Allowing an approved request to execute

C7.1.4 provides three mediation options: the attesting environment sends the request using protected effect credentials; a receiving service checks a single-use capability bound to the evaluated data and target; or an attested enforcement component accepts only requests with matching evidence. The associated test evaluates request A and attempts to execute a different request B, which must be refused. These controls can prevent substitution. [7]

A **single-use capability** is an authorization artifact accepted for one permitted use. Copying its bytes does not establish that the service will accept a second use. A defective implementation might accept concurrent copies or substitute a target. A correct implementation must enforce its declared use count and binding. The test must distinguish these outcomes.

### 2.8 Sending a message to another agent

C5.2.1 requires a sender signature and rejection of invalid messages. C5.2.2 requires validation using published key material. A signature supports verification of the message and the signing credential. A message can still contain data that the sender should not disclose. If the sender includes a reusable credential and the recipient can use it, the disclosure transfers usable authority. If the receiver requires additional evidence or the credential excludes that receiver, copying it is insufficient. [8]

### 2.9 Evaluating a sequence of tool calls

C4.1.7 requires consideration of relevant earlier parameters and state. C4.1.8 prevents diagnostic or advisory results from increasing the authorization allowed by the original grant. A review should therefore test whether later requests remain subject to that grant. It should not assume that adding prior results automatically expands permission. The potential failure is an evaluator that treats earlier tool output as new authority despite those requirements. [6]

### 2.10 Verifying a confidential delegation presentation

C4.2.4 permits a zero-knowledge presentation of policy-compliant delegation. A zero-knowledge protocol is intended to establish a specified statement while limiting disclosure of protected information. The particular protocol determines its freshness and reuse properties. An agent's ability to produce another proof from retained credentials differs from an attack that resubmits an old proof. A review must inspect the verified statement, challenge, recipient, and event rules before claiming that either operation is accepted. [6]

### 2.11 Storing evidence and diagnostic information

C5.1.1 requires agent and principal identifiers in the execution record. C2.1.2 excludes protected content from evidence, and C2.4.1 requires minimized retained data. C7.6.4 controls access to the evidence store and records reads. These requirements do not instruct a logger to retain raw authorization secrets. [8] [13] [7]

If a deployment nevertheless stores a usable secret in a readable log, the log creates an additional source of that secret. Signing the log can make later changes detectable, but it does not provide confidentiality. C7.3.2 separately restricts access to the evidence-signing key. The assessor must examine both the log contents and the permissions governing access to them. [7]

### 2.12 Assigning a verification tier and identifying a mechanism

C8 classifies how evidence is verified and whether execution depends on verification. It explicitly distinguishes verification of control adherence from the adequacy of the controls. A tier designation is an assessment statement, not a credential that an agent necessarily presents to a tool. [10]

Appendix B identifies categories of evidence mechanisms. Classification as a signature, commitment, attestation, or proof does not make those mechanisms equivalent. Each deployment must state the evidence produced, the fact it establishes, and the assumptions required to trust it. The proposed possession protocol needs that same description. [1]

## 3. Separate the security properties of different data objects

The original review grouped private keys, delegation tokens, approval decisions, capabilities, and evidence records into one reusable secret set. An implementation may expose several of these objects, but that exposure must be established for each object. Their security properties differ.

| Object | Function | Condition relevant to misuse |
| --- | --- | --- |
| Bearer delegation token | Allows requests under a grant | Another holder can use a valid copy if the service requires no additional proof |
| Protected private key | Performs an authorized cryptographic operation | Misuse may involve unauthorized operation requests even when extraction is prevented |
| Certificate or public identifier | Supplies public identity or verification information | Public availability does not by itself confer control of a private key |
| Task or session credential | Allows operations during a defined task or session | The permitted operations and duration may exceed what the owner intended |
| Approval record | Records an authenticated decision about displayed content | Misuse depends on acceptance for another request or manipulation of the displayed-to-executed correspondence |
| Single-use capability | Allows one operation for specified data and target | Failure occurs if binding, expiry, or use-count enforcement is missing or incorrect |
| Proof transcript | Records protocol inputs and outputs | Reuse depends on freshness, recipient binding, and event-state enforcement |
| Evidence signature | Allows verification of a record's origin and integrity | Verification does not independently establish the truth of every recorded assertion |
| Tier or conformance statement | Describes an evidence claim | Overstatement occurs when readers infer protection beyond the assessed property |

The useful common question is whether the agent can cause an unauthorized effect using an available object or operation. Answering it requires an inventory of read access, operation access, scope, freshness, and enforcement. Replacing every object name with the word token removes information needed to answer that question.

## 4. Existing controls and the questions that remain

### 4.1 Expiration and scope

Expiration limits the time during which a credential is accepted. Scope limits the requests it can authorize. A use counter limits how many times an authorization can be exercised. These are separate checks and can operate together. For payments, the specification should state whether the grant limits the amount per payment, total amount, recipient, invoice, and number of uses. Any claim about repeated use must identify which checks the deployment performs. [6]

### 4.2 Approval and the executed request

The standard already requires comparison of approval content and execution. A more precise profile could define the machine-readable request from which the approval display is generated, the information shown to the approver, and the authenticated record connecting the decision to that request. The display needs intelligible values for amount, recipient, and operation. Presenting only a cryptographic digest does not explain a payment to a person. A digest is a value calculated from data under a named hash algorithm; its usefulness depends on the approved data being represented and checked correctly.

### 4.3 Gateway mediation and single use

The gateway requirements provide meaningful execution controls. C7.1.1 disallows a direct tool access route that avoids the gateway. C7.1.3 requires the initial durable evidence record before forwarding. C7.1.4 connects evaluation to the dispatched request. These requirements should be preserved in a proposed authorization profile. [7]

Further implementation evidence should address simultaneous submissions, state recovery, and retries. For single use, a service needs a state transition that prevents two submissions from both being accepted. The deployment must also state what happens when an operation executes but its acknowledgment is lost. Consuming an event identifier and completing an external payment are different operations. Their relationship requires an explicit transaction or retry contract.

### 4.4 Hardware protection and request policy

Protected key storage can prevent reading a key. A policy evaluator can restrict requests made with that key. Attestation can provide evidence about the relevant execution environment. These controls have different functions and may be combined. A possession protocol does not remove the need to establish the integrity of its own checker and the policy under which the checker is used. [8] [2]

### 4.5 Public verification and conformance claims

An external verifier needs enough authenticated information to check the claimed fact. A local `true` result alone does not provide that information. Conversely, publishing a transcript does not make it independently verifiable if the verification procedure still requires private state held only by the operator. The profile must specify the verification algorithm and the information available to each verifier. [2] [10]

This requirement applies equally to a delegation system and to the proposed ENI6MA integration. Neither a product name nor the use of cryptography determines a verification tier. The claim must identify the tested mechanism and the assumptions that remain.

## 5. Proposed authorization profile for individual actions

### 5.1 Define the evidence before describing its security

The proposed profile uses a protected witness to produce evidence associated with a particular request. A **witness** is the secret information used by the selected proof procedure. A **nonce** is an event value that must not be accepted again within its defined domain. A **canonical encoding** is a specified method for converting request fields into one unambiguous byte representation. A **verifier identifier** names the approved verification procedure and version.

The profile should authenticate the principal or enrolled account, intended receiving service, operation, complete parameters, policy version, event identifier, expiration time, and verifier identifier. An **authenticated binding** means that the verifier can detect replacement of those values under the selected cryptographic and system assumptions. Merely placing a digest next to a response does not establish that binding.

For a human-approval use case, the profile must additionally define how the displayed request and the person's response are associated. For an autonomous-agent use case, the profile must identify the delegated policy and the agent's enrolled credential. Successful authentication of an agent does not, by itself, identify the human who delegated authority. The formal manuscript states that human attribution requires additional enrollment, origin, and custody premises. [2]

### 5.2 Required operations and acceptance condition

An implementation of the proposed profile would perform the following operations under a published protocol:

1. Prepare the complete request, including fields that the endpoint would otherwise supply from defaults, and identify relevant endpoint state.
2. Assign a fresh event identifier and bind it to the intended request, receiving service, policy, and verifier version.
3. Present the defined challenge to the enrolled participant or protected component. For human approval, display the material request fields in plain language.
4. Obtain a response without exporting the witness through the permitted interface. The implementation must justify this property for the complete observable output.
5. Verify the response, request binding, applicable policy, and event state using the designated verifier.
6. Complete the event-state transition required to prevent another acceptance. Execution and a final acceptance response must remain conditional on both valid verification and successful event consumption.
7. Allow the endpoint operation only through the enforcing component, and record the result without storing the witness or another reusable authorization secret.

The ENI6MA API document describes consuming a nonce before proof validation. In literal operational terms, that sequence marks the event unavailable for another attempt before the checker completes. This review preserves that documented sequence as a protocol characteristic. It does not treat consuming the nonce as evidence that the proof is valid. A complete implementation must define who may consume an event, how concurrent attempts are resolved, and how a rejected or interrupted attempt is recorded. A different sequence would require its own analysis. [5]

The requirement common to the proposed profile is explicit: the system must not report authorization success or execute the protected operation unless verification succeeds and the single-use state transition has been enforced. The sequence of those internal operations, its failure behavior, and its relationship to the endpoint effect must be specified and tested.

### 5.3 Example: binding approval to a payment

**Definition and context.** Use the payment service from section 1.3. In this example, the owner requires a separate approval for every payment. The request contains the operation `pay`, invoice `1042`, payer `A`, recipient `B`, and an integer amount. The event identifier selects one pending approval attempt. It is not a reusable session credential.

**Inputs and assumptions.** The request amount is 20 units. The approved request encoding includes all listed fields, the receiving service, the policy version, the verifier version, and the event identifier. The approval interface accurately displays the amount and accounts from that encoding. The selected protocol authenticates the response's association with those values. The event store reliably enforces single use. These are required assumptions for the example's result.

**Action and check.** The person responds to the challenge for the 20-unit payment. The verifier checks the response and its association with the encoded request. The enforcing component confirms the required event-state transition before allowing the endpoint to execute that payment.

**Result.** Changing the amount to 20,000 changes the encoded request. The previous response fails the request-binding check under the assumed protocol. Resubmitting the original accepted request fails the event-reuse check. A new permitted payment requires a new event and evidence satisfying its own policy.

**Limit.** These results depend on the protocol and enforcement assumptions. They do not follow from the word proof alone. A dishonest display, compromised enrollment, current-event relay, bypass of the enforcing component, or endpoint behavior outside the authenticated request requires separate treatment. The formal ENI6MA manuscript explicitly distinguishes witness secrecy from current-event relay resistance. [2]

### 5.4 Independent calls and messages between services

The ENI6MA API document calls its independent-call mode a one-shot proof envelope. In this review, that term means a request with its own proof-related data and event identifier, with no open caller session required between calls. The document distinguishes reported challenge, response, validation, and nonce-consumption implementation from request-hash and future-reservation work still being formalized. Those status differences remain material to a claim about complete action authorization. [5]

The related manuscripts use oscillation for alternating exchanges between paired service components. In literal terms, the proposed arrangement verifies successive messages using separately allocated state. A message in the reverse direction must meet the requirements for that message. A service reply is not automatically a new authorization to perform another payment. Continuous operation is identified as proposed or partial in the API document. [4] [5]

### 5.5 What the Pass+ documents establish

The Pass+ architecture and login documents dated 2 October 2026 describe an on-device checker that issues a challenge and returns an acceptance decision. They describe a local grant following acceptance and storage of hashes and encrypted enrollment data. They also describe a consume operation that records a caller-supplied `proof_ok` value, with a default acceptance value in the documented path. Those are statements about the reviewed documentation and the source observations it reports. They do not establish current production behavior. [3]

A caller-supplied Boolean value, meaning either `true` or `false`, can record the caller's assertion. An enforcing service needs its own justified basis for relying on that assertion. A requirement for independent verification cannot be satisfied merely by naming the Boolean proof. The same documentation does not establish a complete integration that prevents a payment tool from executing unless the requested payment has passed the proposed proof and consumption checks.

The formal manuscript also states that its mathematical results do not certify an arbitrary compiled binary. Protection of the witness, authentication of the full request, and external effects remain explicit implementation or composition obligations. The proposed contribution must retain those limits. [2]

## 6. Conformance limits, additional examples, and review tests

### 6.1 A supported conformance conclusion

A deployment can satisfy its declared checks and still use a permission set that the owner should have restricted further. C8 expressly allows that distinction between enforcing controls and choosing adequate controls. A review should therefore state the protected property, the policy, and the evidence supporting each conformance claim. [10]

The broader assertion that every conforming implementation necessarily exposes reusable secrets or accepts unauthorized modified payments is not established by the cited requirements. Protected keys, mediated requests, single-use capabilities, approval correspondence, and restricted evidence access can change the result. The proposed action-specific profile should make the required human or enrolled-participant evidence more precise and provide tests for its claimed improvements.

### 6.2 Example: an unchanged request with a changed recipient

**Definition and context.** A payment endpoint accepts the recipient label `primary_supplier`. The endpoint resolves that label by reading a stored mapping from labels to account identifiers. A mapping version identifies the stored mapping used at a particular time. The approved request contains the label but omits the resolved account and mapping version.

**Inputs and assumptions.** At approval time, `primary_supplier` resolves to account B. Before execution, an authorized or compromised administrator changes the mapping so that the same label resolves to account C. The endpoint reads the current mapping during execution. The request bytes remain unchanged.

**Action and check.** The verifier confirms that the request bytes match the approved request. The endpoint then resolves the label using the changed mapping.

**Result.** The byte comparison succeeds, but the payment is directed to C under the stated endpoint behavior. Request integrity alone did not determine the recipient.

**Limit.** A profile that includes the resolved account and relevant state version, and requires the endpoint to enforce them, can reject the changed interpretation. This is the type of request-to-effect issue considered by proposal P02. It applies to both delegation credentials and proofs tied to individual requests. P02 is a proposal, and its reported experiments have not been repeated in this review. [12]

### 6.3 Example: privacy of an identifier and privacy of a witness

**Definition and context.** A service records an account identifier when a user authorizes an operation. The account identifier connects operations to the same enrolled account. A witness is the secret information used during the authorization protocol. The service's policy permits the identifier in evidence and prohibits the witness.

**Inputs and assumptions.** The evidence contains the account identifier and allowed protocol outputs. The witness remains within the protected component. The protocol's disclosed outputs must satisfy its declared secrecy assumptions.

**Action and check.** A reviewer compares two records. The matching account identifiers allow the reviewer to associate both operations with the account. The reviewer does not receive the witness from either record.

**Result.** The records can support account attribution while withholding the witness. They do not provide unlinkability between those operations.

**Limit.** P05 proposes a different identity profile that restricts persistent identifiers and uses session pseudonyms with a defined accountability procedure. A session pseudonym is an identifier used for the specified session. P05 includes proposed mechanisms and implementation limits. Witness protection and unlinkability require separate claims; neither should be inferred from the other. [11]

### 6.4 Tests required for the proposed integration

Each test must name a build, policy, endpoint, input, expected decision, and observable execution result. The following are proposed tests, not results obtained during this editorial revision.

| Test condition | Required observation |
| --- | --- |
| Change a payment amount after approval | The enforcing component refuses the changed request before the payment occurs |
| Change the receiving service or resource | Verification rejects the request under the defined binding rule |
| Submit two copies concurrently | At most one protected execution is permitted, with a documented result for the other submission |
| Restart after event consumption | The same event cannot become available again through recovery |
| Lose the endpoint acknowledgment | The documented retry mechanism avoids an unintended duplicate effect |
| Supply only `proof_ok: true` | The claimed independent check cannot be bypassed by the caller's assertion |
| Replace the verifier or its version | Acceptance follows the declared verifier policy and rejects an unauthorized replacement |
| Attempt direct tool access | The agent cannot execute the protected operation without the required enforcement |
| Inspect model inputs and accessible logs | The claimed secret-exclusion rules hold for the tested execution |
| Use a copied current response | The result matches the protocol's stated relay and concurrent-submission assumptions |
| Change an endpoint default or alias | The operation is rejected or remains within the authenticated effect conditions |
| Measure representative load | Report the measured latency, throughput, failures, and resource use with the tested configuration |

Possession of a running authorized component remains a separate threat condition. If a party controls the permitted endpoint or can invoke its active credential operation, the assessment must identify which policy checks still constrain that party. The API document explicitly limits its claims for parties controlling a running authorized endpoint. Retaining the witness inside that component does not eliminate the need to analyze its permitted uses. [5]

## 7. Conclusion and proposed contribution

The standard defines delegation, authorization evaluation, execution mediation, and evidence verification. A reusable bearer credential introduces a disclosure and reuse risk when another party can obtain and use it under the receiving service's policy. A valid credential also does not establish a separate human approval of every later request. Those findings support precise requirements for credential custody and evidence of approval for individual actions.

The reviewed standard already includes controls relevant to those risks. It requires approval correspondence checks, request-substitution tests, mediation of tool access, selected key protections, and restrictions on evidence contents and access. A complete review must evaluate those controls according to their specified function. It must also distinguish harmful activity permitted by a broad grant from a failure to enforce that grant.

The proposed contribution is a profile defining the protected witness, authenticated request context, participant attribution, verifier, event consumption, endpoint conditions, and verification evidence. The profile should include reproducible positive and negative tests and a clear implementation status. ENI6MA supplies relevant protocol and formal work, while its own documents identify further application and deployment obligations. The contribution should claim the properties demonstrated for a named implementation and retain the assumptions under which those properties hold.

## References

References [1] and [6] through [13] identify files in the reviewed repository revision. Local documents [2] through [5] may change independently; the accompanying source manifest records the inspected file hashes. No DOI or publication status has been added to the supplied citations.

[1] Advanced AI Society and the Proof-of-Control Initiative. *Open Verification: the Proof-of-Control Standard for Agents*. Working Draft v0.1. [Reviewed repository revision](https://github.com/LFDT-ProofOfControl/ov-poc-standard/tree/54a7bc67140b39c9107216cd390dd47c1d42946d). Includes [Appendix B, Proof Mechanism Inventory](https://github.com/LFDT-ProofOfControl/ov-poc-standard/blob/54a7bc67140b39c9107216cd390dd47c1d42946d/0.1/en/0x91-Appendix-B_Proof-Mechanism-Inventory.md).

[2] Frank Dylan Rosario and Dr. Lin Grant Wang. *Perfect Geometric Proof of Identity*. Formal evidence manuscript, date stated in the supplied review: 18 September 2026. [Local source](/Users/rosario/work/LEAN4-PUBLISH/01-CORE-FORMAL/CORE-02-comprehensive-native-evidence/source/PERFECT_GEOMETRIC_PROOF_OF_IDENTITY.md). Relevant sections: 1, 2, 3, 7, 8, and 9. The current local text distinguishes channel secrecy, knowledge, attribution, request authentication, and implementation evidence.

[3] ENI6MA. *Pass+ and ENI6MA Sequoia architecture* and *Login ceremony*. Architecture review dated 2 October 2026. Source locations and hashes are listed in the accompanying manifest. Historical documentation of local verification, grants, enrollment storage, and the consume operation; no fresh product qualification is claimed here.

[4] Frank Dylan Rosario. *Geometric One-Time Pads*. Review manuscript, date stated in the supplied review: 5 November 2026. [Local source](/Users/rosario/work/BOOK-PUBLISH/_ZENODO-WHITE-PAPERS-2026-11-05-r4/papers/geometric-one-time-pads/source/manuscript.md). Relevant discussion: paired components and durable consumption. Used as protocol context, not as a benchmark or deployment certification.

[5] Frank Dylan Rosario and Dr. Lin Grant Wang. *ENI6MA API Authentication and PII Architecture*. API Auth Protocol V3, version `3.2.0-draft`, source metadata dated 25 September 2026. [Local source](/Users/rosario/work/LEAN4-PUBLISH/03-TECHNICAL-SYSTEMS/TECH-06-api-auth-pii/source/ENI6MA_API_AUTH_PROTOCOL_V3.md). Relevant passages: canonical source and mode separation, one-shot request handling, section 8.3, and application-composition limits.

[6] Proof-of-Control Initiative. [C4 Authorization][c4]. Requirements C4.1.1 through C4.1.8, C4.2.1, C4.2.2, and C4.2.4, with auditor evidence.

[7] Proof-of-Control Initiative. [C7 Evidence Generation and Properties][c7]. Requirements C7.1.1 through C7.1.5, C7.2.3, C7.3.2, C7.5, C7.6.4, and C7.7, with auditor evidence and implementation discussion.

[8] Proof-of-Control Initiative. [C5 Identity][c5]. Identity figure, C5.1.1 through C5.1.4, C5.2.1, and C5.2.2.

[9] Proof-of-Control Initiative. [Threat vocabulary][threats]. Entries concerning identity, permission scope, prompt injection, disclosure, messages between agents, and approval.

[10] Proof-of-Control Initiative. [C8 Verifiability Tiers and the Binary Threshold](https://github.com/LFDT-ProofOfControl/ov-poc-standard/blob/54a7bc67140b39c9107216cd390dd47c1d42946d/0.1/en/0x10-C08-Verifiability-Tiers.md). Tier definitions, control-adequacy qualification, and open issues concerning trust classification.

[11] Proof-of-Control research programme. [P05: Unlinkable identity](https://github.com/LFDT-ProofOfControl/ov-poc-standard/blob/54a7bc67140b39c9107216cd390dd47c1d42946d/docs/proposals/P05-unlinkable-identity.md). Proposal status and implementation qualifications apply.

[12] Proof-of-Control research programme. [P02: Normative changes for message-to-effect binding](https://github.com/LFDT-ProofOfControl/ov-poc-standard/blob/54a7bc67140b39c9107216cd390dd47c1d42946d/docs/proposals/P02-effect-binding.md). Proposed endpoint conditions and limits of request-representation evidence.

[13] Proof-of-Control Initiative. [C2 Privacy](https://github.com/LFDT-ProofOfControl/ov-poc-standard/blob/54a7bc67140b39c9107216cd390dd47c1d42946d/0.1/en/0x10-C02-Privacy.md). C2.1.2 and C2.4.1.

[14] M. Jones and D. Hardt. *The OAuth 2.0 Authorization Framework: Bearer Token Usage*. [RFC 6750](https://www.rfc-editor.org/rfc/rfc6750), October 2012. Cited for the bearer-token definition.

[15] D. Fett, B. Campbell, J. Bradley, T. Lodderstedt, M. Jones, and D. Waite. *OAuth 2.0 Demonstrating Proof of Possession (DPoP)*. [RFC 9449](https://www.rfc-editor.org/rfc/rfc9449), September 2023. A standardized example of constraining token use to a presenter proving possession of a private key. It demonstrates why token formats and proof requirements must be identified separately. This citation does not assert that DPoP alone approves a complete application payload or establishes human intent.

[c4]: https://github.com/LFDT-ProofOfControl/ov-poc-standard/blob/54a7bc67140b39c9107216cd390dd47c1d42946d/0.1/en/0x10-C04-Authorization.md
[c5]: https://github.com/LFDT-ProofOfControl/ov-poc-standard/blob/54a7bc67140b39c9107216cd390dd47c1d42946d/0.1/en/0x10-C05-Identity.md
[c7]: https://github.com/LFDT-ProofOfControl/ov-poc-standard/blob/54a7bc67140b39c9107216cd390dd47c1d42946d/0.1/en/0x10-C07-Evidence-Generation-and-Properties.md
[threats]: https://github.com/LFDT-ProofOfControl/ov-poc-standard/blob/54a7bc67140b39c9107216cd390dd47c1d42946d/docs/use-cases/THREATS.md
