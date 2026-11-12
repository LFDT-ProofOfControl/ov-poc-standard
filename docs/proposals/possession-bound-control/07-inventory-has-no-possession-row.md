# Gap: Appendix B has no row for an interactive possession protocol

**Status:** proposal. Informative addition to Appendix B. Not a new mandatory mechanism.
**Targets:** `0.1/en/0x91-Appendix-B_Proof-Mechanism-Inventory.md`, layers L6 and L7.
**Pattern:** interactive possession protocol. **Instance:** ENI6MA PassPlus.

## The problem the draft allows

Appendix B is the menu assessors use when a control names a mechanism. The menu contains digital signatures, formal verification, zero-knowledge proofs, remote attestation, hash chains, secure multiparty computation, supply-chain attestation, commitments, verifiable computation, and verifiable credentials.

An interactive possession check will be filed under the nearest row.

- Filed as a zero-knowledge proof, the deployment inherits a claim the transcript may not meet. A checker that sees bearings learns the response symbols. Witness-hiding is not the taxonomy's ZKP row.
- Filed as remote attestation, the deployment inherits a hardware quote it may not have. A pinned wasm digest is a checker identity. It is not an Intel TDX report.
- Filed as a verifiable credential, the deployment inherits a bearer object. Gap 01 is the reason that filing fails.
- Filed as a bare commitment, the deployment gets the binding to a hidden value and loses the fresh challenge, the response, and the nonce consumption.

The technology-neutral rule says the standard must not mandate this mechanism. The same rule does not require the inventory to be silent. Silence is how a non-matching row gets selected in an audit.

## The row to add

| Mechanism | What it shows | MAESTRO layers | Maturity |
| --- | --- | --- | --- |
| Interactive possession protocol | A response is consistent with a commitment to a witness for a named challenge. The witness is not an output. A consumed nonce does not accept again. | L7 identity, L6 approval records. L3 only where the agent loop refuses a tool call that lacks a citing capability. | Emerging for a device-local checker that returns a boolean. Research for an outsider-checked transcript in the Proof-of-Control claim schema. |

**Verification requirement.** Recompute acceptance from the published commitment, challenge, and response, or, at the lower maturity, record the checker digest and the boolean and grade that artifact at Tier 2 (gap 05). Confirm the evidence record omits the witness. Confirm a second presentation of the nonce is refused.

**Does not show.** Legal personhood beyond the principal reference. That the human understood a sentence the digest does not cover. That a remote endpoint applied the authorized effect (P02). That the checker measurement is a hardware attestation.

**Feasibility.** The PassPlus clients are the emerging cell: on-device `wasm32-wasip1` guest, challenge then validate, local grant only on acceptance, witness sealed rather than logged. The research cell is the outsider transcript. Label it research until a published verifier recomputes acceptance without the operator boolean. Do not mark the cell Proven.

## What this asks

One informative row, plus a sentence in the taxonomy preamble: an implementation that cites this row states which maturity cell it occupies, and a Tier 3 claim requires the research cell's verifier, not the emerging cell's boolean.

No product name in the row. The PassPlus instance stays in this proposal so reviewers can see the emerging cell is occupied by running clients and the research cell is not.
