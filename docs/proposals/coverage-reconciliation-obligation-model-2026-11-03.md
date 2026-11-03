# Declared obligations and record identities: executable example

Informative supplement, 3 November 2026.

The [example package](../../examples/obligation-reconciliation/README.md)
classifies a supplied population of obligations against supplied logical records.
It distinguishes a literally absent record from a supplied record whose identity
conflicts, retains unmatched variants, counts duplicate admitted identities,
and leaves unknown triggers and unresolved outcomes visible.

For a triggered obligation with conflicting supplied records, `missing` is
empty while `no_admissible_record` identifies the obligation. If no record was
supplied at all, both fields identify it. This overlap is intentional: they are
not independent defect counts to add together. A separate valid record does
not erase a conflict.

A linked A0/A1 example retains the original missing-record finding at the
first cutoff. A newly supplied late receipt changes the later assessment,
which records the earlier assessment ID and serialized digest. The declared
outcome remains unresolved in both. A copied value and digest link do not
implement durable append-only storage or authenticate the receipt.

The [contract](../../examples/obligation-reconciliation/CONTRACT.md),
[fixtures](../../examples/obligation-reconciliation/controls.json) and
[recorded results](../../examples/obligation-reconciliation/results.json)
make the calculations inspectable. Seventeen direct cases plus one linked
assessment case compare actual findings with contributor-authored expectations.
The [execution record](../../examples/obligation-reconciliation/EXECUTIONS.json)
distinguishes two earlier executions of that same suite from a later export
smoke execution. These are not three independently designed suites or a
third-party reproduction.

This develops the explicit-obligation distinction in
[Christopher Filkins's comment on #173](https://github.com/LFDT-ProofOfControl/ov-poc-standard/issues/173#issuecomment-6509031753).
The rules and identity policy are candidate semantics, not adopted requirements.
Inputs, trigger evidence, clocks, premise references and population boundaries
remain synthetic declarations. The example does not establish population
completeness, authenticated triggering, real-time evidence, operational
completeness, full C1/C2/C3 coverage, conformance or production assurance.

This example is separate from the [31 October finite-model campaign](coverage-reconciliation-evidence-2026-10-31.md)
and [Bjørn Vidar Hauge's 13-case reproduction report](https://github.com/LFDT-ProofOfControl/ov-poc-standard/pull/182#issuecomment-6558321737).
Those dated records and the [original proposal](coverage-reconciliation.md)
retain their historical claims. No new result here is attributed to that
external reproduction. This informative addition makes no claim of meeting
the elapsed public-comment deadline or of working-group acceptance.
