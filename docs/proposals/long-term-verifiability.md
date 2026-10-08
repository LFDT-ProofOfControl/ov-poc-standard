# Proposal: evidence that still verifies at the end of its retention period

*Date:* 2026-10-08 · *Status:* proposal only. No normative file is edited by this proposal.

*Submitted by:* Abdel (@AbdelStark), founding contributor, in a personal capacity

*Targets:* C6.3.5, C7.6, C7.2.4 (auditor evidence), C10.2, Appendix C, Appendix D issue 6

*Executable evidence:* attacks A12 and A13 and fourteen regression tests in the reference
implementation, [`impl/poc/renewal.py`](../../impl/poc/renewal.py)

---

## The central finding

Tier 3 evidence is verified "After the fact, but by anyone" (C8). For audit, insurance and
litigation the fact is far behind: the paper sizes storage for evidence kept "for the seven years
a regulator might ask about", and the reference implementation's README says examination "may be
a decade after the fact". Over that period the evidence does not change, and three things
underneath it do:

1. **Algorithms break.** Once an algorithm a signature rests on is broken, that signature is
   something anyone can produce, dated whenever they like. That includes the signatures that date
   evidence (a timestamp token, a log's signed tree head), which post-quantum record signatures do
   not replace. A rewritten history then verifies exactly as the genuine one does.
2. **Verification material changes.** A hardware quote is appraised against collateral the vendor
   revises. Intel's attestation service documents a platform's TCB status as "relative to the
   latest TCB level info obtained from the PCS", and each TCB recovery publishes a new level. The
   same quote can be appraised differently in a later year, and without the collateral used the
   first time, nobody can reproduce the original appraisal.
3. **Mechanisms turn out to have failed silently.** A forged quote made with an extracted
   attestation key, or a proof accepted by an under-constrained circuit, is indistinguishable from
   a genuine one. When such a failure is disclosed, every piece of evidence produced during the
   exposure window loses its standing, back to the start of the window and not just to the
   disclosure.

The standard addresses a slice of this. C6.3.5 handles the record signature's horizon, C3.2.1
keeps keys and tooling published across a migration, and C6.3.3 re-grades evidence after an
evidence-key compromise. It has no requirement that retained evidence stays verifiable, and the
two answers C6.3.5 gives are each defeated by a concrete attack (A12, A13). The fix is not new
cryptography: RFC 4998 (Evidence Record Syntax) standardized it in 2007, and long-term
preservation services already deploy it.

## Summary of proposed changes

| # | Where | Kind | Confidence |
| :--: | --- | --- | --- |
| L1 | C6.3.5 | Correct a requirement that admits two attacks, and extend it past record signatures | Defect settled by construction (A12, A13); wording is drafting |
| L2 | New C7.6.7 | Add: retained evidence verifiable offline from what was retained | Judgement; Level `[WG-INPUT NEEDED]` |
| L3 | C7.2.4, auditor evidence | Verify the quote's signature chain before reading REPORTDATA | Defect settled by reading; wording is drafting |
| L4 | New C10.2 row | Disclose the events that invalidate issued evidence, and how far back re-grading reaches | Judgement; extends P01's proposed 10.2.3 |
| L5 | Appendix C | Qualify the Full rating of "Evidence repudiation" and "Audit tampering"; add a row for appraisal drift | `[WG-INPUT NEEDED]`, normative appendix |
| L6 | Appendix D, issue 6 | Add a third question: does a Tier hold at issuance or for the retention period? | Editor |

**What this rests on.** Primary sources, read for this proposal, and two attacks that run in the
reference implementation: each succeeds against the requirement as written and is detected under
the requirement as proposed. A break is modelled by handing the adversary the broken algorithm's
private keys, which is what "forgeable" means to a verifier; no algorithm was broken and no real
collateral was re-appraised. The scenarios treat break dates as known; L1 says which date a real
verifier should use. Renewal intervals, an evidence-record format and the Levels are left to the
working group.

---

# L1: C6.3.5, renewal

**Where:** `0x10-C06-Security.md`, requirement **6.3.5**.

**Current text**

> `| **6.3.5** | **Verify that** where the declared evidence retention period ([C7.6.5](0x10-C07-Evidence-Generation-and-Properties.md)) extends beyond the period for which the signature scheme is projected to remain unforgeable, the implementation uses a post-quantum or hybrid signature scheme (e.g., FIPS 204 ML-DSA), or re-anchors and re-signs retained evidence under a current scheme before the projection lapses. Evidence is only worth what its signature is worth at the moment it is examined. | 3 |`

**Proposed text**

> `| **6.3.5** | **Verify that** where the declared evidence retention period (C7.6.5) extends beyond the period for which any algorithm the evidence rests on is projected to remain secure (record and capability signatures, timestamp tokens, signed log roots, hardware attestation signatures and their certificate chains, and the assumptions of any proof system), retained evidence is kept exactly as signed and is renewed, ahead of that projection, by a timestamp on an algorithm projected to outlast it that covers the previous timestamp (RFC 4998 timestamp renewal; hash-tree renewal where the hash function is the algorithm retiring); that the renewal timestamp comes from an anchor meeting 8.1.7 (a public transparency log with independent monitors, a public ledger, or a quorum of separately operated authorities), named in the trust-assumption disclosure; that no renewal re-signs, replaces or re-serializes archived evidence; and that the published verification procedure accepts retained evidence only through a timestamp chain whose first timestamp falls within the anchoring interval declared under 7.6.6. Post-quantum or hybrid signing of new evidence does not discharge this requirement. | 3 |`

**Why: post-quantum record signatures leave the dating classical.** The first option protects
the records, and only the signatures the operator controls. What dates the evidence stays
classical, and so does every signature in the bundle the operator cannot migrate. A TDX quote is
a DCAP quote, which Intel's quoting code signs with an ECDSA-P256 attestation key certified
through Intel's PCK chain. RFC 6962 requires a log to sign its tree heads with ECDSA on P-256 or
RSA, and RFC 9162, which obsoletes it, allows ECDSA on P-256 or Ed25519. An RFC 3161 token carries
the authority's signature. Anchoring is what stops an operator who holds the evidence key from
rewriting history (A9, C7.3.5). **A12** keeps the records on a sound algorithm, as a deployment
hybrid from day one would, and breaks only the timestamp's algorithm. The operator rebuilds year-0
history with one read that never happened and forges a year-1 timestamp over it. The rewrite
verifies on every point the genuine history does: record signatures, chain, inclusion proof,
timestamp. A verifier is left with a choice it cannot win: accept both histories, or refuse the
broken algorithm and lose the genuine one. Where the records are classical too, the adversary need
not be the operator. An anchor dated by hashes rather than signatures, such as a proof-of-work
chain, is not exposed in this way.

**Why: re-signing replaces evidence rather than carrying it across.** The key that re-signs did
not observe the events; it signs whatever the renewal job hands it. A re-signing step that does
not verify the originals, which C6.3.5 permits, is a statement by whoever ran it, the case C8
describes: "The system operator produces logs or records, then signs them. [...] Trust required:
that the operator produced the log faithfully." **A13** runs a renewal job that alters one record
on the way through. The result verifies under the renewal key, inside an archive timestamped on a
sound algorithm, and by the time the classical algorithm is broken the original signatures cannot
contradict it, because any of them could be a forgery. Re-anchoring the re-signed set does not
help: it anchors the altered set. Nor can a verifier catch it by enforcing the anchoring interval
of 7.6.6, because honestly re-signed evidence fails that rule too: the re-sign route requires the
verifier to accept a re-anchor years after the fact. Re-signing inside an attested environment
that verifies the originals first is better, and it still moves the evidence onto that
environment's attestation, which is itself a classical signature.

**What works, and why.** RFC 4998 keeps the evidence and extends what dates it. Its renewal rule
(section 5.2): "In the case of Timestamp Renewal, the content of the timeStamp field of the old
Archive Timestamp has to be hashed and timestamped by a new Archive Timestamp." Its verification
rule (section 5.3): "Each Archive Timestamp MUST be valid relative to the time of the following
Archive Timestamp", and "the last Archive Timestamp has to be valid at the time the verification
is performed." The argument is an induction from the newest timestamp, which is sound today. A
sound timestamp issued in year 5 shows the year-1 timestamp existed in year 5, when the year-1
timestamp's algorithm could not yet be forged; so the year-1 timestamp is genuine, and the root
it covers, with every record and original signature under it, existed in year 1. The original
signature then means what it meant on the day it was made. The construction goes back to Bayer,
Haber and Stornetta (1993), and long-term preservation deploys it today: BSI TR-03125 (TR-ESOR)
profiles RFC 4998 and RFC 6283. `impl/poc/renewal.py` implements the subset this needs, and A12
and A13 are detected with it.

Three conditions make it hold. **The renewal anchor must be open.** A single timestamp authority
is a designated party that could backdate, which 8.1.2 caps at Tier 2, so L1 requires the anchor
to meet 8.1.7 and to appear in the disclosure. **Renewal runs ahead of the projection, not at the
break.** A break is known only once disclosed, so a verifier applies the earliest credible date at
which an algorithm, or a particular authority's key, became forgeable (the look-back of L4), and
renewal margins are set against that. **Renewal cannot repair a defect exploitable from the
start.** Evidence produced under a mechanism that was already broken (L4's two cases) is not saved
by covering it; that is what the disclosure and re-grading of L4 are for.

**Why proof systems are in the list.** A proof system that becomes unsound once discrete
logarithms in its group can be computed accepts proofs of false statements from then on, past
statements included: pairing-based SNARKs, whose setup trapdoor becomes recoverable, and
inner-product arguments such as Bulletproofs and Halo 2, whose commitments stop binding. Renewing proofs by re-proving is not available, because the witness is not retained:
C2.4.1 keeps retained evidence to derived or minimized forms of protected data, and a witness is
usually the protected data itself. What remains is to show that the proof existed while its
assumptions held, which is the same renewal.

**Confidence:** the defect is **settled by construction**: both attacks run against the
requirement as written. The algorithm list, the anchor options and the reference to RFC 4998 are
drafting; the working group may prefer a CBOR rendering that matches the claim set (C7.7). Two
choices are the working group's: whether one authority may serve as the renewal anchor below Tier
3, and whether the interval rule binds every verifier or only the published procedure. The Level
stays 3.

---

# L2: new C7.6.7, retained evidence verifies offline

**Where:** `0x10-C07-Evidence-Generation-and-Properties.md`, C7.6 table, after 7.6.6.

**Current text:** none; this is an addition. It extends **3.2.1**, whose current text is:

> `| **3.2.1** | **Verify that** evidence generated before a cross-cloud or cross-vendor migration remains validatable after it: keys, reference values, and verification tooling for the old environment stay published for the retention period. | 2 |`

**Proposed text** (new row)

> `| **7.6.7** | **Verify that** retained evidence is stored with everything needed to verify it at the end of the retention period without any online service of the operator or a vendor: the certificate chains and revocation status used, the attestation collateral as signed by its issuer (for an Intel TDX quote, the PCK certificate chain, TCB Info, QE Identity and revocation lists), the inclusion and consistency proofs with the anchored roots and the timestamps over them, the verification keys and program or circuit identifiers of any proof, and the version of the verification procedure used. | 3 |`

**Auditor evidence:** 7.6.7: take the oldest retained evidence and verify it on a machine with no
network access, using only what was retained with it; then compare the platform status the
retained collateral gives against the status the original verification recorded.

**Why:** C8.1.5 and C8.1.8 require that anyone can complete verification of a Tier 3 claim using
only published materials, and C3.2.1 keeps the operator's keys and tooling published across a
migration. Neither reaches material the operator does not publish. Collateral belongs to the
vendor, and the vendor decides how long it serves older versions: Intel's certification service
lists the "currently supported TCB Evaluation Data Numbers and associated TCB-R event dates".
Re-appraising a quote years later against current collateral can legitimately give a different
status, after later TCB recoveries, and reproducing the original appraisal depends on the vendor
still serving the collateral it used. RFC 9334
separates Evidence, Endorsements, Reference Values and the Attestation Result a Verifier produces;
retained evidence needs all of them, or the appraisal cannot be repeated. Collateral is signed by
its issuer, so retaining it asks the verifier to trust no one new.

**Confidence:** **judgement call.** The defect, that the standard has no requirement that retained
evidence stays verifiable, is settled by reading. Level 3 is proposed because this is what keeps Tier 3's
verification by anyone, after the fact, possible for the declared retention period; `[WG-INPUT NEEDED]` on the
Level, and on whether the row belongs in C7.6 or in C8.1 beside 8.1.5.

---

# L3: C7.2.4, verify the quote before reading it

**Where:** `0x10-C07-Evidence-Generation-and-Properties.md`, C7.2 auditor evidence, the 7.2.4 clause.

**Current text**

> 7.2.4 — take one quote and recompute the expected report-data value from the published evidence key; a quote that does not commit to the key does not attest the key.

**Proposed text**

> 7.2.4: take one quote, verify its signature chain to the vendor's root against the collateral retained with it (7.6.7) and record the platform status that collateral gives, then recompute the expected report-data value from the published evidence key. A quote whose signature chain does not verify attests nothing, and a quote that does not commit to the key does not attest the key.

**Why:** REPORTDATA read from a quote whose signature has not been verified is bytes anyone can
write. An auditor following the current clause literally compares 64 bytes at an offset. The
reference implementation does the same: `TDXQuote.binds_key` in `impl/poc/tdx.py` compares
REPORTDATA in the raw quote, and no signature, certificate-chain or TCB verification is performed
anywhere in the module. This does not touch what the TDX run measured; the generation side is
right, and the hardware did write the key's digest. It means `binding_sound: true` in
`impl/results/tdx.json` records what the hardware produced, not what a verifier can establish.

**Confidence:** **settled by reading** that the clause omits the signature chain. The wording is
drafting. The reference-implementation gap is listed under knock-on edits.

---

# L4: new C10.2 row, invalidation events and re-grading

**Where:** `0x10-C10-Conformance-and-Disclosure.md`, C10.2 table, after the rows P01 proposes
(10.2.3 detection latency, 10.2.4 shared dependencies). Numbered here as **10.2.5** on that basis.

**Current text:** none; this is an addition.

**Proposed text** (new row)

> `| **10.2.5** | **Verify that** for each disclosed assumption, the disclosure names the events that would invalidate evidence already issued (compromise of an attestation or platform key, a TCB recovery, a soundness defect in a proof system or circuit, retirement of an algorithm), the public source monitored for each, and the re-grading applied to affected evidence; and that for an assumption whose failure leaves no trace in the evidence, re-grading reaches back to the earliest point the failure could have been exploited, not to its disclosure. | 2 |`

**Why:** C6.3.3 already requires this for one party: after an evidence-key compromise,
"identification of all evidence signed by the affected key [...] re-grading of affected claims".
Nothing requires it for the parties a Tier 3 claim rests on that are not the operator. Two recent
cases show the failure is silent and the window is years long:

* **TEE.fail** (Intel security announcement 2025-10-28-001) extracted Intel's provisioning
  certification key, the per-CPU key in the signature chain that ends at Intel's root. In the
  authors' words, "properly forged SGX and TDX attestation quotes are cryptographically
  indistinguishable from legitimate ones", and a forged TDX quote verified with Intel's DCAP Quote
  Verification Library at status UpToDate, so the TCB status does not tell it apart. Intel
  considers interposer attacks out of the threat model for SGX and TDX, with no mitigation beyond
  physical security. A deployment that re-grades only on TCB recoveries never re-grades.
* **The Zcash Orchard counterfeiting vulnerability** (disclosed June 2026) was "an
  under-constrained element of the Orchard circuit", present from Orchard's activation in May 2022
  until the June 2026 fix. Shielded Labs: "there is no way to cryptographically prove whether the
  vulnerability was exploited before it was remediated."

In both, evidence produced inside the window cannot be told apart from forgery once the failure
is known, so re-grading from the disclosure date understates the exposure by years.

**Relation to P01.** P01's proposed 10.2.3 discloses detection latency: how long between a breach
and visible evidence of it. This row discloses what happens to evidence issued before the breach
was detected. The two compose. Latency bounds when a relying party learns; the look-back says how
far back the damage reaches.

**Confidence:** **judgement call.** That the events exist and are silent is settled by the two
cases. Level 2 matches C6.3.3, the same obligation for the operator's own key.

---

# L5: Appendix C, repudiation and appraisal drift

**Where:** `0x92-Appendix-C_Threat-Model.md`, the coverage table. Appendix C is normative, so the
wording is the working group's; what follows is the input.

**Current row**

> `| Evidence repudiation | Full | Cryptographic evidence is openly verifiable and non-repudiable; the operator cannot deny an action occurred | Disputes about the meaning or significance of an action, only whether it occurred |`

**Proposed row**

> `| Evidence repudiation | Full, while every algorithm the evidence rests on holds or the evidence has been renewed (C6.3.5) | Cryptographic evidence is openly verifiable and non-repudiable; the operator cannot deny an action occurred | Disputes about the meaning or significance of an action, only whether it occurred; retained evidence that was not renewed before an algorithm it rests on was broken |`

**Current row**

> `| Audit tampering | Full | Records are tamper-evident, generated by the mechanism at execution, not operator-narrated | Insider compromise at the silicon layer, disclosed via trust assumptions |`

**Proposed row**

> `| Audit tampering | Full, including through renewal (C6.3.5) | Records are tamper-evident, generated by the mechanism at execution, not operator-narrated; renewal covers them without re-signing | Insider compromise at the silicon layer, disclosed via trust assumptions |`

**Proposed new row**

> `| Appraisal drift | Strong, with C7.6.7 | Retained evidence carries the collateral, proofs and verifier version it was verified with, so the original appraisal can be repeated offline | A failure the vendor never discloses, and one it declares out of scope |`

**Why:** A12 is a repudiation attack, and A13 is tampering performed by renewal itself. Once an algorithm the evidence rests on is broken, the
operator can deny an action by producing a contradictory history that verifies as well as the
genuine one, years after the fact, which is when evidence is most often examined. A renewal job
that re-signs can alter what it renews. "Full" holds for both rows only with renewal as proposed.
A new row also changes the threat count the README states.

**Confidence:** the qualification is settled by A12; the wording and the coverage grade of the
new row are `[WG-INPUT NEEDED]`.

---

# L6: Appendix D issue 6, a third question

**Proposed addition** to the two questions under issue 6:

> 3. Does a Tier placement attach to evidence at issuance, or must it be maintained for the
>    retention period? Evidence is placed when it is produced and relied on years later, after
>    algorithms, collateral or mechanisms may have failed. C6.3.5 as proposed and the new C7.6.7
>    assume the second reading; the cryptography review should confirm it.

**Confidence:** editor's change; it records a question and settles nothing.

---

# What I do not propose, and why

1. **No fifth evidence property.** Durability could be read as one (Appendix D issue 5). It is the
   condition under which the existing four keep holding, and a separate property would restate
   them.
2. **No retreat from post-quantum signing.** Hybrid signing of new evidence stays the right
   default, and the FAQ's cost analysis stands. It is necessary for the records and not sufficient
   for the evidence.
3. **No format.** RFC 4998 is ASN.1, and RFC 6283 renders it in XML. A rendering consistent with
   the claim set's CBOR and JSON profiles (C7.7) is the working group's choice, and it should come
   with test vectors under `schema/vectors/` like every other part of the claim set.
4. **No renewal interval or algorithm lifetime.** Lifetimes are a policy input. The requirement
   refers to the declared projection, as C6.3.5 already does.
5. **No change to the Tier definitions.** L6 asks the question; the answer belongs with the
   cryptography review under issue 6.

# Knock-on edits implied but not drafted here

* **`docs/faq.md`, question 11** answers "Is the evidence post-quantum safe?" with "Yes." The
  record signatures can be; the evidence as a whole needs L1's renewal, because the quote, the
  timestamp and evidence signed before the switch stay classical.
* **`paper/main.tex`, the post-quantum section** says "The hash chain, the sequence numbers, and
  the anchoring are already post-quantum", then lists "published roots" among the signatures that
  must migrate, which is the half A12 depends on; it also describes C6.3.5 as "re-signs and
  re-anchors". Both inherit L1. The `impl/README.md` sentence, which kept only the first half, is
  corrected in the same pull request as this proposal, because it describes the implementation
  that pull request changes.
* **`impl/poc/tdx.py`** should verify the quote against retained collateral (the equivalent of
  Intel's Quote Verification Library) and store the collateral with the evidence, so that L3's
  auditor step is runnable on the reference implementation. A separate pull request.
* **C3.2.1 auditor evidence** says "validate one pre-migration evidence artifact today, using only
  published materials". With L2 it should read "using only what was retained with it (7.6.7)".
* **Appendix B, remote attestation:** "A remote verifier compares this measurement against an
  authorized golden value without needing to trust the operator." True at issuance; with L2 and L4
  the row should say the comparison is repeatable later only from retained collateral.

# Sources

* [RFC 4998](https://www.rfc-editor.org/rfc/rfc4998): Evidence Record Syntax, sections 5.2 (renewal) and 5.3 (verification)
* Bayer, Haber and Stornetta, "Improving the Efficiency and Reliability of Digital Time-Stamping", Sequences II, 1993 · [BSI TR-03125 (TR-ESOR)](https://www.bsi.bund.de/EN/Themen/Unternehmen-und-Organisationen/Standards-und-Zertifizierung/Technische-Richtlinien/TR-nach-Thema-sortiert/tr03125/BSITR03125.html), Annex ERS: evidence record profiling of RFC 4998 and RFC 6283
* [RFC 3161](https://www.rfc-editor.org/rfc/rfc3161): Time-Stamp Protocol · [RFC 6962](https://www.rfc-editor.org/rfc/rfc6962), section 2.1.4, and [RFC 9162](https://www.rfc-editor.org/rfc/rfc9162): log signature algorithms · [RFC 9334](https://www.rfc-editor.org/rfc/rfc9334): RATS architecture
* Intel, [PCS v3 to v4 migration guide](https://api.trustedservices.intel.com/documents/PCS_V3-V4_migration_guide.pdf): the TCB evaluation data numbers endpoint
* Intel, [`ecdsa_quote.h` and `sgx_ql_ecdsa_quote.h`](https://github.com/intel/SGXDataCenterAttestationPrimitives/tree/main/QuoteGeneration/quote_wrapper/common/inc): the ECDSA-P256 quoting interface and attestation key
* Intel Trust Authority, [Platform TCB](https://docs.trustauthority.intel.com/main/articles/concept-platform-tcb.html): TCB recovery and status "relative to the latest TCB level info obtained from the PCS"
* [TEE.fail](https://tee.fail/): DDR5 interposition against Intel SGX and TDX and AMD SEV-SNP
* Shielded Labs, [The Orchard Counterfeiting Vulnerability](https://shieldedlabs.net/the-orchard-counterfeiting-vulnerability/), 4 June 2026
