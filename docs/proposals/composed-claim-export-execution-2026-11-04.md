# Composed-claim export execution: 4 November 2026

One same-operator execution of the outgoing-only pinned bundle completed at **08:37:29.173463–08:37:30.340587 UTC**. Nineteen fresh prerequisite outcomes passed before thirteen sequential full attempts and thirteen grades; all grades matched the frozen expectations. There was one wrapper invocation, no retry, no timeout, zero stderr and no halted or missing case. MATCH includes deliberately failed and uncertain component outcomes.

This is a separate result from the [04:38 UTC campaign](composed-claim-campaign-2026-11-04.md). It verifies the observed wrapper/control path on a reused pinned runtime: Python 3.14.6, macOS 15.7.9 arm64, cryptography 46.0.3, cffi 2.0.0 and pycparser 2.23. The recorded executable digest and exact 633-file dependency inventory matched their pins before launch. No environment installation was repeated. This is not fresh-install validation or independent reproduction.

## Prerequisites and attempts

The [control capture](../../impl/composed-claim-campaign-2026-11-04/evidence/export-execution-2026-11-04/output/prerequisites/capture/stdout.jsonl) records all 19 named outcomes: Ed25519 positive and invalid signature; Merkle inclusion positive and invalid node; consistency 3→5, 3→7 and 5→7 positive and invalid node; permitted Q2 component; denied oracle, case-label, generator-knowledge and symlink-escape reads; denied write, local-loopback network and fork; absence of inherited API-key environment names. The control made one Q2 component invocation with two verified entry/completion pairs, zero full appraisals and zero grades. Its P0 material reuse is disclosed, not another full-case attempt or a freshness demonstration. The canaries are public synthetic strings.

The [43-record attempt ledger](../../impl/composed-claim-campaign-2026-11-04/evidence/export-execution-2026-11-04/output/attempt-ledger.jsonl) retains start, prerequisite intent/finish, thirteen ordered attempt-intent/grade-intent/finish triples and end. Every capture and grade is retained, including all failures and uncertainty. The thirteen full cases contain 390 paired operations: 382 verified and eight deliberately failed; the separate Q2 control is excluded.

| Case | Attempts / grades | Grade | Q2 | Q3 direct | Q3 proposition | Q4 | PA-obs |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P0 | 1 / 1 | MATCH | verified | verified | supported | verified | supported |
| T2-A | 1 / 1 | MATCH | verified | verified | supported | verified | supported |
| T2-B | 1 / 1 | MATCH | verified | verified | supported | verified | supported |
| T2-C | 1 / 1 | MATCH | verified | verified | supported | verified | supported |
| T3-U | 1 / 1 | MATCH | verified | verified | supported | verified | supported |
| T3-R | 1 / 1 | MATCH | verified | verified | supported | verified | supported |
| T3-N | 1 / 1 | MATCH | verified | verified | supported | verified | supported |
| T5-M | 1 / 1 | MATCH | verified | unavailable | not established | unavailable | not established |
| T5-S | 1 / 1 | MATCH | verified | not assessed | not established | not assessed | not established |
| N2 | 1 / 1 | MATCH | failed | verified | supported | verified | not established |
| N3 | 1 / 1 | MATCH | verified | failed | supported | verified | supported |
| N4 | 1 / 1 | MATCH | failed | failed | not established | failed | not established |
| N5 | 1 / 1 | MATCH | verified | verified | supported | failed | not established |

The [full matrix](../../impl/composed-claim-campaign-2026-11-04/evidence/export-execution-2026-11-04/MATRIX.csv) and [run index](../../impl/composed-claim-campaign-2026-11-04/evidence/export-execution-2026-11-04/RUN-INDEX.json) retain Q1 appraisal/equality/authority, Q5, Q6, operation counts and derivation provenance. T2 missing appraisal is not filled in by log success. T3 observed equality, unknown authority and policy rejection remain distinct. T5 missing evidence differs from supplied but unscheduled operations. N3 rejects the direct proof while completed, bound Q4 operations support the Q3 proposition and bounded PA-obs; this shares Q4 evidence, not another independent security route. N4 requested endpoint authentication fails; an alternative equivalent endpoint route is not assessed. N5 preserves authenticated view conflict.

## Exact tested material and later publication documents

The execution used a 134-file, 2,445,524-byte snapshot. The [snapshot inventory](../../impl/composed-claim-campaign-2026-11-04/evidence/export-execution-2026-11-04/snapshot-inventory.json) SHA256 is `45e6360f8b09f8c70d60e137fc0251bd04be828e1fc6040c06df3091830c44c4`; the tested bundle inventory SHA256 is `7be60ddcbadca83a4fcc7f2b75cd12f3c10745bdcadd4bcebde8ac98c28da464`; RUN-PLAN SHA256 is `bf24c077e5115dd21cc5a7d8ef3d678b4d063abfacd5d8fc9121151d19ee77e4`. The source/input export is reused. Frozen oracle and plan wording remains historical. The later README/reproduction status, this note, evidence and publication inventory are documentation changes, not the exact complete snapshot executed earlier. No executable, expectation, fixture or claim-strength change accompanies them, and no new run or regrade was performed to prepare them.

The [transformation map](../../impl/composed-claim-campaign-2026-11-04/evidence/export-execution-2026-11-04/TRANSFORM-MAP.json) identifies byte-identical captures and every process/path/provenance projection by original/output digests. Original private records are retained; public projections alone do not establish an independent chain of custody. Hashes embedded inside a capture continue to name original bytes, even where the accompanying process/profile file is a labelled projection. Runtime path placeholders preserve the disclosed structure; they are not executable commands or profiles. Run IDs, operation IDs and measured timestamps remain unchanged.

Ed25519/Merkle verification and local operation/acquisition instrumentation were actual computations. Signer roles, authority policy, log times and the synthetic deployment/measurement model were stipulated; no deployed software was observed. The operator, host, supervisor and grader remain trusted. This result establishes no hardware attestation, controller independence, remote witness independence, endpoint/effect assurance, population accuracy, global completeness, composite Tier or blanket completion of T1–T5. Future execution still requires fresh prerequisites; historical PASS records do not admit it.

Prepared by Mikhail Sergeev with AI assistance. The earlier note's attribution to the worked record, #174, Bjørn Vidar Hauge, David McKibbin, P01, StevenMih, Nirinasoa Rajaona, FantasticoFox and GravitOpenNetwork is preserved. Existing vector-source attribution and third-party notices remain unchanged. This is informative supporting evidence, not working-group adoption or evidence of an extended comment deadline.
