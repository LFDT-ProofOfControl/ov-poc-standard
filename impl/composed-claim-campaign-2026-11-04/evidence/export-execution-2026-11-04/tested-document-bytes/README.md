# Frozen composed-claim campaign bundle

This bundle accompanies the [dated result](../../docs/proposals/composed-claim-campaign-2026-11-04.md). It supplies inspectable inputs, sources and historical captures for one synthetic 13-case campaign.

- `fixtures/*/supplied.json`: the 13 original canonical supplied inputs, byte-identical. They contain public verification keys and signed synthetic objects; generator-only signing keys and generator knowledge are excluded.
- `common.py`, `merkle.py`, `assessor.py`, `entrypoint.py`, `admission.py`: byte-identical source. Only four assessor-side modules and the supplied/acquisition files enter the restricted directory.
- `supervisor.py`: one operator-facing error string changed for export; behavior preserved. The nonempty review token remains a trusted-operator assertion, not a security boundary.
- `grader.py`: only the pinned oracle hash changes to the exported metadata-redacted oracle. The comparison logic is unchanged.
- `oracle/EXPECTED-OUTCOMES.json`: original frozen case order, interventions, expectations and route contract. Coordination metadata is omitted. Historical wording such as “proposed, not executed” describes the time of expectation freeze, not the later campaign.
- `evidence/`: saved raw stdout/stderr, acquisition, assessor outcomes, original grades, stage inventories, run index and CSV. Historical grades name the original oracle hash. Process projections are explicitly transformed; they are not original process captures.
- `PROVENANCE.json`, `EXPORT-MAP.json`, `INVENTORY.json`: original/output hashes, transformation descriptions and exact outgoing inventory. INVENTORY excludes itself.
- `reproduce.py`, `runtime_preflight.py` and [REPRODUCE.md](REPRODUCE.md): export orchestration with corrected resolved disjoint placement and exact dependency inventory. Only synthetic path/file preflight regressions have run.
- `prerequisites.py`, `control_probe.py`, fixed vector files and [PREREQUISITES.md](PREREQUISITES.md): prepared fresh primitive/isolation gate and exact next-run plan; not executed.

Expected outcomes and generator-only material never enter assessor staging. The host, unsandboxed supervisor and grader remain trusted. Acquisition timestamps describe local ingestion of supplied views, not remote witness independence or truthful log time. The macOS sandbox permits system/runtime/dependency/staging reads and metadata reads; it is not a malicious-host or side-channel defense. The output limit is a post-capture bound, not disk containment.

No dependency code or wheels are redistributed. Pinned released distributions are fetched separately for a future reproduction. The historical runtime and all 633 installed dependency-file hashes are provided without the original local directory. No cross-platform execution claim is made.
