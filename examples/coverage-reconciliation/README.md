# Coverage and mediation: a finite-model supplement

This informative example supports the [coverage-reconciliation proposal](../../docs/proposals/coverage-reconciliation.md) and [discussion #173](https://github.com/LFDT-ProofOfControl/ov-poc-standard/issues/173). It provides 13 synthetic cases separating evidence-chain integrity, population coverage and mediation claims. It does not implement the proposal's complete obligation/identity procedure or change a normative requirement.

The recorded 30 October 2026 campaign matched the frozen expected outcomes and measured-reference expectations in all 13 cases. A comparison match can correctly return `not_established` or `not_supported`. Read [RESULTS.md](RESULTS.md) before interpreting PASS.

- [REPRODUCE.md](REPRODUCE.md): exact prerequisites, compatibility limits and staged commands.
- [Case catalogue](bjorn-vectors/cases.json), [derivation rules](bjorn-vectors/rules.json), input schemas and per-case fixtures, generator truth and expectations.
- `bjorn-implementation/`: assessor, producer adapter, comparator and selected current runtime components.
- [Recorded result view](results/recorded-results.json): derived selected claims, scoped conclusions, measurements and original artifact digests. It is not the original receipts or a new execution.
- [REFERENCE.json](REFERENCE.json), [dependencies.json](dependencies.json), [requirements.lock](requirements.lock): exact public reference and recorded producer wheel pins.
- [PROVENANCE.json](PROVENANCE.json) and `SHA256SUMS`: export contents and transformations. Verify the export before producing fresh run-specific pins.
- [NOTICE.md](NOTICE.md) and [LICENSE](LICENSE): attribution and intended contribution terms.

The 39 fixture, generator-truth and expected-result files retain their recorded bytes. Case/rule catalogue metadata and source comments/docstrings were prepared for publication, with explicitly listed digest-constant updates. The cleanup and staged reproduction recipe have been checked statically; this exported package has not been run as another campaign. Recorded results refer to the original execution and source digests, not to an execution of the cleaned export.

Technical `s3-bjorn` schema/profile/container names, the `bjorn_s3_checker` module name and one checker-pin diagnostic retain their original compatibility strings. They do not identify a published workflow role or record. Renaming executable strings would be a separate source change; this export preserves them. In fixture inputs, `DESIGN CANDIDATE / PROPOSED, NOT EXECUTED` is a required frozen validation value. In the case/rule catalogues the same text is retained historical metadata. Neither use replaces the dated execution record above.

The measured work is reference chain/signature verification and generated record/epoch mapping. Populations, observations, routes, mediation bindings, completeness bases and copied times are synthetic or declared. The adapter does not instantiate a RelyingParty; gateway release is not endpoint capability enforcement, dispatch or an external effect. Trusted local host records do not prove integrity against a malicious host. These results do not establish independent reproduction, real-source crash recovery, operational completeness, certification or working-group adoption.

The intended reproduction path is the recorded macOS arm64 producer environment plus the pinned linux/amd64 container under the specified Docker Desktop configuration. The launcher is not a general portable Docker frontend. No dependencies, reference implementation, container image or raw private archive are vendored.
