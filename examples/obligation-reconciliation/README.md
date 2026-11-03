# Reconcile declared obligations with supplied records

This executable example distinguishes missing records, conflicting identities,
duplicate admitted records and unresolved declarations within a supplied
snapshot. It also links a later assessment to an unchanged earlier assessment
when a late receipt becomes available.

Run from this directory with Python 3 and its standard library:

```sh
python3 -B -W error run_controls.py
```

No package installation, network service, API key or other repository is needed.
The runner reads the adjacent `controls.json` and `premises.json`, prints JSON
containing every actual and expected finding, and exits nonzero if any comparison
fails. It does not write these files. Earlier executions used Python 3.14.6 and
3.12.14; the export smoke environment is recorded in [EXECUTIONS.json](EXECUTIONS.json).
The retained [results.json](results.json) is the export smoke output, not a
replacement for an earlier raw execution record.

## Read a result

| Finding | Interpretation within the supplied snapshot |
| --- | --- |
| `missing` | A declared triggered obligation has no supplied variant. |
| `no_admissible_record` | It has no nonconflicting matching record. This includes `missing`; do not sum the two as independent defects. |
| `conflicts` | One identity has different triples; all variants and affected bindings remain visible. |
| `duplicates` | Multiple distinct admitted identities match the same applicable or unknown obligation. |
| `unmatched` | A supplied variant binds to an undeclared or declared-false obligation. |
| `undetermined` | Applicability is declared unknown, whether or not a record exists. |
| `unresolved` | The separately supplied outcome remains unresolved. |

Seventeen direct cases exercise these distinctions. The eighteenth compares
linked assessments A0 and A1. A0 retains its original missing finding; A1
includes a late receipt and the exact ID/digest link to A0. Their outcome
remains unresolved. Two other fixture states exercise snapshot non-mutation;
they are not the linked late-receipt case.

The [contract](CONTRACT.md) defines precedence and overlap. [PROVENANCE.md](PROVENANCE.md)
identifies the original expectations, export transformations and limits of the
historical execution reports. [NOTICE.md](NOTICE.md) gives attribution and
license provenance. The source and result hashes are in [SHA256SUMS](SHA256SUMS).

## Boundaries

These are contributor-authored synthetic controls. A comparison PASS means
that actual findings match the stated expectations, including negative or
uncertain findings. It does not make every underlying claim positive.
A separate execution of the same suite is not independent suite design or
third-party reproduction.

The model consumes supplied population, rule, identity, trigger and time
declarations. It does not authenticate them or establish that the supplied
population is complete. It does not implement trusted time, persistent
append-only storage, competing trigger authorities, adversarial input
admission, cryptographic verification, full C1/C2/C3 coverage or production
assurance. No Tier is assigned.

This package is a separate informative example from the existing 13-case
coverage campaign and its external reproduction. See the
[dated supplement](../../docs/proposals/coverage-reconciliation-obligation-model-2026-11-03.md)
for the relationship to the proposal.
