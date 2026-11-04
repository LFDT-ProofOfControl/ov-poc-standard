# Composed-claim campaign: 4 November 2026

One frozen, same-operator synthetic campaign produced 13 expected-outcome matches in 13 sequential attempts. The recorded operations comprise 382 verified and eight deliberately failed operations. MATCH means agreement with the frozen expectations, including failure and uncertainty; it does not mean that every component verified.

This dated supplement to the [worked record](composed-claim-worked-record-2026-10-31.md) implements bounded T2, T3 and T5 variants with positive and negative controls. The earlier record remains a historical proposal. This result does not complete all its T1–T5, establish a composite Tier, or change a normative requirement. It is supporting material for [#174](https://github.com/LFDT-ProofOfControl/ov-poc-standard/issues/174), separate from the obligation model in PR182.

## What ran

The campaign ran on 4 November 2026, 04:38:12.105640–04:38:13.035842 UTC, using Python 3.14.6 on macOS 15.7.9 arm64, cryptography 46.0.3, cffi 2.0.0 and pycparser 2.23. The assessor received frozen signed synthetic artifacts and a fixed operation plan, without generator-only keys, case labels or expected outcomes. A separate grader compared captured outcomes with the precommitted oracle.

There were 13 assessor attempts and 13 grading calls, no retry, no missing run, no overlap, zero stderr, no timeout and exit code 0 for each process. Captures contain 390 entry/completion pairs and 1,276,832 stdout bytes. These are recorded operations, not 390 separate security mechanisms. Their local process, acquisition and timing evidence relies on the operator and host.

## Case matrix

Q1a authenticates the synthetic report and collateral, Q1b compares measurement values, and Q1c appraises the reference publisher under the stated policy. Q2 verifies inclusion; Q3_direct verifies the direct consistency proof. Q4 authenticates and compares the supplied views. Q5 authenticates an asserted time; Q6 is not assessed throughout.

| Case | Intervention and recorded result | Limit |
| --- | --- | --- |
| P0 | Complete material; all requested component operations verified | Positive control for synthetic material; Q6 remains not assessed |
| T2-A | Collateral withheld: Q1a unavailable; raw challenge equality and available log operations retained | Log success supplies no missing appraisal |
| T2-B | Reference value and its publication withheld: Q1b/Q1c unavailable; available authority operations retained | No value inferred from the log |
| T2-C | Authority directory withheld: Q1c unavailable; Q1b equality verified | Equality does not establish authority |
| T3-U | No applicable authority entry: Q1c unevaluable after five available operations; Q1b verified | Unknown authority differs from policy rejection |
| T3-R | Explicit applicable deny: Q1c failed/policy_rejected; equality retained | Policy rejection is not measurement inequality |
| T3-N | Signed report carries a different digest: Q1b failed/observed_inequality; authority retained | No deployed software identity inferred |
| T5-M | S1 and authenticated W1/W2 heads missing: Q2 verified; Q3_direct/Q4 unavailable | PA-obs not established |
| T5-S | Complete material supplied, Q3/Q4 unscheduled: not assessed with zero operations | Distinct from missing material; PA-obs not established |
| N2 | Invalid inclusion node: executed Q2 proof rejection | PA-incl and PA-obs not established |
| N3 | Invalid direct consistency node: Q3_direct failed/proof_rejected; completed Q4 route supports Q3 proposition and bounded PA-obs | Q4-derived support shares Q4 evidence; it is not a separate security route |
| N4 | Requested S2 signature invalid: authentication failed in Q2/Q3_direct/Q4; dependent proofs not entered; W2 authentication retained | Equivalent-payload alternative unevaluated; no negative mathematical inference |
| N5 | Authenticated W2 root conflict: Q4 failed; direct Q3 retained | PA-obs not established |

The [full matrix](../../impl/composed-claim-campaign-2026-11-04/evidence/MATRIX.csv), raw traces and saved outcomes preserve the finer distinctions. The Q3-derived route records the exact log, algorithm, trust configuration, authenticated endpoint digests, sizes, roots, report, appraisal, view set and cutoff. It is not inferred from a Q4 summary alone.

## Evidence and reproduction

The [companion bundle](../../impl/composed-claim-campaign-2026-11-04/README.md) includes assessor sources, supplied fixtures, expectation content, saved captures, provenance and a concrete [reproduction recipe](../../impl/composed-claim-campaign-2026-11-04/REPRODUCE.md). Export preparation used static comparisons and synthetic path/file preflight regressions only. The exported recipe has not been executed, and no public-only or independent reproduction is reported. Some metadata was removed for export; every transformation is identified separately from byte-identical captures.

Ed25519 verification, Merkle proof verification, digest equality and local acquisition/operation instrumentation were real computations. Deployment identities, signer roles, authority policy, remote source independence and logical log times were stipulated. Fixture generation computed a digest of synthetic F; the assessor never observed deployed software. P0/T5-S reuse is disclosed session-binding material, not a freshness demonstration. There is no hardware attestation, controller independence, endpoint/effect result, relying-party coverage, global completeness, truthful-time bound, future detectability or composite Tier result.

Prepared by Mikhail Sergeev with AI assistance. The result develops the reporting distinctions in the worked record and #174, including Bjørn Vidar Hauge's withheld-appraisal proposal and David McKibbin's #162 distinctions. The record credits P01, StevenMih's PR142, Nirinasoa Rajaona's #114 and its later reply by FantasticoFox, and GravitOpenNetwork's #123. Their observations are not claimed as new; this supplement contributes the bounded implementation, frozen variants and recorded execution. Publication is not working-group adoption or evidence of an extended comment deadline.
