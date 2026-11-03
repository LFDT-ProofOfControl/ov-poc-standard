# Declared obligation model: contract

Informative candidate semantics for this supplied-input example.
See [PROVENANCE.md](PROVENANCE.md) for the retained expectation history
and the distinction between this public editorial export and the original
frozen contract.

## Inputs and identity

Inputs are supplied synthetic declarations, not authenticated observations.
An obligation key denotes operation/attempt/phase and maps to `true`, `false`
or `unknown`. The input population is supplied independently of records.
Each record is `[record_id, obligation_key, content]`, all strings in this slice.
Equal triples are transport redelivery and count once. Different triples with
the same record ID conflict, including a changed binding to an obligation.
All distinct variants are retained; all variants of a conflicted ID are
inadmissible for matching. Sorting is lexicographic for deterministic output.
`unresolved` is a separately supplied list of operation/attempt identifiers.

## Findings, precedence and overlap

| Field | Exact meaning within the supplied snapshot |
| --- | --- |
| `missing` | Trigger `true` and **no supplied variant** bound to that key. Quarantining a supplied variant alone cannot establish absence. This says nothing about records elsewhere or event non-occurrence. |
| `no_admissible_record` | Trigger `true` and no nonconflicting logical record bound to that key. Includes literally missing units, so overlap with `missing` is intentional; conflict-only units appear here but not in `missing`. |
| `conflicts` | One object per conflicted record ID, preserving every variant, all affected declared units (including false/unknown), and unmatched units (undeclared or false). Remains present even if a different unconflicted record exists for the unit. |
| `duplicates` | More than one distinct **admitted** ID bound to a declared true/unknown unit. Quarantined variants do not enter duplicate counts. Unknown applicability remains unknown. |
| `unmatched` | Every distinct supplied variant bound to an undeclared or false unit, with reason and full triple, even if also conflicted. |
| `undetermined` | Every `unknown` trigger, regardless of record presence. |
| `unresolved` | Supplied unresolved outcomes, independent of missing, conflicts, duplicates and trigger states. |

There is no aggregate satisfaction, coverage, conformance or completeness
verdict. In particular, a conflict never supplies an admissible record and
a separate valid record does not erase the conflict finding. False is a
declaration, not proof of a non-event. Empty findings establish no population
completeness. Exact record content is retained here only because fixtures are
synthetic; this is not a sensitive-data ingestion service.

## Assessment envelope and late receipt

The envelope retains the supplied input snapshot and its SHA-256, assessment
ID, model version, declared scope, original cutoff, current availability
cutoff, clock declaration, trigger basis, and exact obligation-rule,
phase-profile and identity-policy references. Referenced premise text is
included in `premises.json`; references use SHA-256 of the corresponding
serialized object. Serialization for this slice is Python JSON with sorted
keys, compact separators, `ensure_ascii=False`, UTF-8 and no trailing newline;
it is not a claim of an external canonical JSON standard.

A0 has a declared triggered before obligation, no matching record at cutoff
T0, and an unresolved outcome. A1 is a separately identified assessment at
T1 linked to A0's ID and the digest of the complete serialized A0 envelope.
A1 keeps A0's original cutoff and the same premises/trigger declarations.
It identifies the added receipt and declared event/availability times. Only
A1's record snapshot changes. A0 remains missing; A1 has a matching record;
the outcome remains unresolved in both. The envelope computes the link but
does not authenticate it. It consumes a declared selected snapshot; it does
not prove selection completeness or automatically interpret timestamps.

This example labels its change `late_receipt`, requiring unchanged premises,
trigger declarations and unresolved outcomes. Changed rule premises require
a separately labelled reassessment outside this example. The historical
unknown-to-true snapshot control is retained separately, with its changed
declarations explicitly supplied; it is not the late-receipt example.

Neither deepcopy, the envelope nor a digest link implements persistent
append-only storage, trusted clocks, actual execution-time ordering, source
authentication or verification of trigger authority/adequacy. These are
inspectable declared inputs, not verified provenance.

## Controls and exclusions

The fixtures supply full explicit inputs and handwritten expected findings
for seventeen direct cases and one linked A0/A1 case. The expectations are
preserved from the retained pre-implementation fixtures; only their top-level
schema label changes for this export. The runner emits all actual outcomes
and exits nonzero on a mismatch.

The two separately supplied snapshot states remain snapshot non-mutation
controls. The A0/A1 case separately exercises the exact prior assessment
ID/digest link, retained original finding and unchanged unresolved outcome.
No historical snapshot control is relabelled as executed late-evidence behavior.

Malformed/adversarial admission, competing trigger authorities, cryptography,
live producers, policy evaluation, complete populations and unrepresentable
phases remain outside this slice. No full C1/C2/C3 or all-proposal-case
coverage is claimed.
