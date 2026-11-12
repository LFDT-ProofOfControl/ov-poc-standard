# Gap: C6.3 fits an evidence-signing key and will be mis-applied to a witness

**Status:** proposal. Issue text for the Security and Privacy groups.
**Targets:** C6.3, C6.3.5, C2.1.2, C2.4.1, issue 7.
**Pattern:** split the witness from the evidence-signing key. **Instance:** ENI6MA PassPlus.

## The problem the draft allows

C6.3.1 requires evidence-signing and attestation keys to be generated in and non-exportable from hardware-backed key management. C6.3.2 requires a rotation schedule and a signed link from old key to new key. C6.3.3 requires a compromise procedure that can find every record by key identifier. C6.3.5 requires a post-quantum or hybrid signature, or a re-sign, when retention outlives the classical scheme.

Those sentences are the right sentences for the key that signs the log. They are the wrong sentences for a possession witness. A witness that lives as a human-recalled or device-held secret is not an HSM object. Rotation-on-a-calendar is the wrong recovery action. The right recovery action is revocation of the commitment and re-enrollment.

If the chapter is applied as written to every secret in the system, two bad outcomes are both available.

- The assessor fails the deployment because the witness is not an HSM key. The pattern becomes uncertifiable.
- The assessor accepts the witness as the evidence-signing key. The log is then signed by an object that was never managed as a signing key, and C6.3 has been met on paper by the wrong object.

C2.4.1 asks that retained evidence contain only minimized forms of protected data, enforced by the schema. Nothing tells the assessor that the witness is protected data and that the response bearings are a different field. A pipeline that stores the secret configuration "because the checker needed it" creates a second copy, which is the failure C2 states in its control objective. The chapter does not name this input, so the scan in C2.1.2 has no field list to scan for.

C6.3.5 has a sibling confusion. A hybrid encapsulation used to seal enrollment is a confidentiality margin. An evidence signature is an unforgeability margin at the time of examination. A deployment can satisfy the seal and still carry records under a classical signature that a later examiner cannot trust. The draft does not require the two margins to be disclosed as separate claims, so one measurement will be pasted into both cells.

## The pattern that closes it

Glossary: evidence-signing key, possession witness, enrollment seal. Definitions are in [DEFINITIONS.md](DEFINITIONS.md).

- C6.3 applies to the evidence-signing key only.
- The witness is forbidden in evidence records (profile rule in gap 02). Compromise revokes the commitment and requires re-enrollment, recorded under the evidence-signing key.
- The seal names its recipient, its encapsulation algorithms, and the margin being claimed. That margin is not copied into the C6.3.5 cell.
- C6.3.5 continues to point at the signature scheme on the evidence record. FIPS 204 remains the draft's example. The possession check's resistance to guessing the witness is an Identity disclosure, not a substitute signature.

## What PassPlus runs

- The witness is enrollment secret material. It stays on the device until seal.
- The seal is E6PS v2: X25519 plus ML-KEM-768, BLAKE3 key derivation, XChaCha20-Poly1305. The architecture note states the scoped claim: under the ML-KEM-768 assumption the encapsulation resists a future quantum reader, and if that assumption fails the seal keeps X25519 security.
- The factory opens the seal with a recipient private key. That recipient is a disclosed party, not a removed party.
- The Authority does not store plaintext Encoding A or `secret_units`.
- The checker is a wasm guest. It is not the evidence-signing key. It is not a TEE quote.

This split is already how the system is built. The draft cannot see it, so an assessor using only C6.3 will ask for the witness to be an HSM key or will treat the seal algorithm as the log's signature algorithm.

## What PassPlus does not run

PassPlus does not, on the architecture page, sign Proof-of-Control evidence records with an HSM-held key under a published rotation schedule. C6.3 remains unmet for a log the clients do not yet produce. The pattern's demand is that when that log exists, its signing key is a new object, not the witness and not the seal.

## Requirement sketch

**6.3.6, Level 2.** Verify that the key inventory lists evidence-signing keys and possession witnesses as separate classes, that C6.3.1 through C6.3.5 are assessed against the signing-key class, and that the witness class has a documented revocation and re-enrollment procedure that has been exercised in test.

**6.3.7, Level 2.** Verify that any quantum or hybrid margin claimed for an enrollment seal is recorded in a different disclosure cell from the C6.3.5 signature margin, and that each cell names its scheme.

**Auditor evidence.** The inventory with two classes. One test re-enrollment that leaves old possession records verifiable under the old commitment and rejects new responses under it. The seal's algorithm list and the evidence signature's algorithm list, side by side, not equal unless they are in fact the same scheme.
