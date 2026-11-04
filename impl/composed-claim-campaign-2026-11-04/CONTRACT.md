# Frozen implementation contract v1

Exported operative contract. Historical design/campaign coordination paragraphs are omitted. The contract below is byte-identical to the operative source paragraphs; the original record remains retained.

Canonical bytes are Python JSON encoding with sorted keys, separators (comma,colon), ensure_ascii=True, no whitespace/newline, ASCII text only, exact key sets below, no duplicate keys, floats, booleans, NaN or null. Integers are nonnegative and at most 2^53-1. Hash/public key/challenge fields are 64 lowercase hex characters; signatures are 128. Limits: supplied file <=1MiB, objects <=17, proof nodes <=64, authority entries <=16, revoked IDs <=16, tree sizes 1..1024 for this slice. Arrays preserve order. Unknown fields or malformed/noncanonical encodings invalidate capture rather than count as an intended cryptographic negative.

Each signed envelope has exactly kind,key_id,payload,signature. Signed bytes: ASCII "AARM-COMPOSED-v1:" + kind + NUL + canonical(payload). Pure Ed25519, not Ed25519ctx. Expected signer identity comes from the role's pinned trust key; the untrusted key_id must equal that identity. No supplied key substitutes for trust configuration.
- report: report_id,claim,measurement,challenge,signer_id. A signs; signer_id=A.
- certificate: subject_id,public_key,not_before,not_after. V signs; subject_id=A and public_key equals pinned A.
- collateral: subject_id,not_before,not_after,revoked (list of IDs). V signs; subject_id=A.
- publication: claim,measurement. RVP signs.
- directory: policy_version,entries. AR signs. Each entry has key_id,claim,not_before,not_after,disposition (allow or deny).
- head: log_id,size,root,timestamp,key_id. LO signs; payload key_id=LO. Logical timestamps are assertions.
- delivery: source_id,challenge,log_id,head_digest. W1/W2 respectively sign.
- time_receipt: log_id,report_digest,logical_time. LO signs.

Object roles: R, certificate, collateral, M, publication, directory, S1, S2, inclusion, direct, W1_head, W1_delivery, W2_head, W2_delivery, edge_3_5, edge_5_7, time_receipt. M has measurement only. inclusion has index,size,nodes. direct/edges have from_size,to_size,nodes. Omitted roles are absent keys, never null. R is required; other missing inputs are reported by component gates. No artifact F, leaf population, private keys, expected labels or case_id in the supplied file.

Trust config fields: keys (exact V,A,RVP,AR,LO,W1,W2 -> public key), claim,log_id,challenge,report_id,appraisal_time,policy_version. Pinned policy: half-open validity [not_before,not_after), exact claim/key scope, no applicable entry -> unevaluable; multiple applicable entries, including duplicate identical entries, -> unevaluable (duplicate/contradictory material retained); one allow -> verified, one deny -> failed/policy_rejected. Zero-length/reversed intervals invalidate schema. This resolves duplicate handling without changing any of the 13 expectations.

Plan fields: operations (unique ordered subset of Q1a,Q1b,Q1c,Q2,Q3_direct,Q4,Q5), derivation ("after_verified_Q4"). Frozen ordinary order is that list; T5-S omits Q3_direct/Q4 only. Q6 is always explicitly not_requested/not assessed. No result labels or case identifier occur in plan. Q3_from_Q4 executes generically after verified Q4, with exact authenticated endpoint/edge/equality/context trace references. It must not use a Q4 summary alone.

Supervisor creates an opaque run_id, invokes simulated W adapters by reading each provided delivery/head pair, captures receipt order and monotonic_ns timestamps, then cutoff after all receipts. This is trusted local acquisition evidence, not a remote event/time guarantee. It stages only canonical objects/trust/plan plus acquisition metadata and copied assessor-side modules in a new directory. Sandbox denies reads outside system/runtime, selected dependency environment and that staging directory; all network/write/process-fork operations denied. Root directory enumeration and global file metadata are permitted for runtime startup; this does not permit file contents. Supervisor/grader remain trusted and unsandboxed. No malicious-harness resistance or side-channel/confidentiality proof is claimed.
