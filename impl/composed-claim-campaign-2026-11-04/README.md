# Frozen composed-claim campaign bundle

This bundle accompanies the [original dated result](../../docs/proposals/composed-claim-campaign-2026-11-04.md) and the separate [export-execution record](../../docs/proposals/composed-claim-export-execution-2026-11-04.md). It supplies inspectable sources, inputs and two distinct same-operator records. The earlier dated note and root PROVENANCE/EXPORT-MAP retain their original preparation-time statements; current execution status is in the later record.

- `fixtures/*/supplied.json`: the 13 original canonical supplied inputs, byte-identical. They contain public verification keys and signed synthetic objects; generator-only signing keys and generator knowledge are excluded.
- `common.py`, `merkle.py`, `assessor.py`, `entrypoint.py`, `admission.py`: byte-identical source. Only four assessor-side modules and the supplied/acquisition files enter the restricted directory.
- `supervisor.py`: one operator-facing error string changed for export; behavior preserved. The nonempty review token remains a trusted-operator assertion, not a security boundary.
- `grader.py`: only the pinned oracle hash changes to the exported metadata-redacted oracle. The comparison logic is unchanged.
- `oracle/EXPECTED-OUTCOMES.json`: original frozen case order, interventions, expectations and route contract. Coordination metadata is omitted. Historical wording such as “proposed, not executed” describes the time of expectation freeze, not the later campaign.
- `evidence/`: saved raw stdout/stderr, acquisition, assessor outcomes, original grades, stage inventories, run index and CSV. Historical grades name the original oracle hash. Process projections are explicitly transformed; they are not original process captures.
- `PROVENANCE.json`, `EXPORT-MAP.json`, `INVENTORY.json`: original/output hashes, transformation descriptions and exact outgoing inventory. INVENTORY excludes itself.
- `reproduce.py`, `runtime_preflight.py` and [REPRODUCE.md](REPRODUCE.md): export orchestration with corrected resolved disjoint placement and exact dependency inventory. One outgoing-only execution on the reused pinned runtime is now recorded separately. Dependency installation was not repeated or validated anew.
- `prerequisites.py`, `control_probe.py`, fixed vector files and [PREREQUISITES.md](PREREQUISITES.md): frozen prerequisite and run-plan snapshots. Their unexecuted wording records preparation time; the later export-execution evidence records 19 fresh outcomes and 13 attempts. Every future run still requires fresh prerequisites.

Expected outcomes and generator-only material never enter assessor staging. The host, unsandboxed supervisor and grader remain trusted. Acquisition timestamps describe local ingestion of supplied views, not remote witness independence or truthful log time. The macOS sandbox permits system/runtime/dependency/staging reads and metadata reads; it is not a malicious-host or side-channel defense. The output limit is a post-capture bound, not disk containment.

No dependency code or wheels are redistributed. Pinned released distributions are fetched separately for a future reproduction. The historical runtime and all 633 installed dependency-file hashes are provided without the original local directory. No cross-platform execution claim is made.

## Later export execution and publication inventory

`evidence/export-execution-2026-11-04/` contains the 08:37 UTC control capture, thirteen full captures/results/grades, matrix, attempt ledger, process/profile projections, runtime observation and tested-snapshot inventory. The original `evidence/` files retain the separate 04:38 UTC campaign. The two sets are not pooled as independent trials.

`TRANSFORM-MAP.json` in the later evidence directory maps each original digest to its outgoing digest. Path placeholders and the review-token placeholder are projections, not executable profiles or original captures. Embedded capture/profile/source hashes retain their original-byte meaning; consult the map for the corresponding projected hash. Case/run/operation IDs and timestamps are retained. No signing key or generator-only material is included.

The tested snapshot had 134 files and inventory SHA256 `7be60ddcbadca83a4fcc7f2b75cd12f3c10745bdcadd4bcebde8ac98c28da464`. Current README, REPRODUCE and INVENTORY plus the added evidence/note are later documentation. This complete publication inventory has not been executed. All tested executable, oracle, fixture, vector, runtime-pin and plan bytes remain unchanged. The tested document copies and snapshot inventory permit reconstruction without a second source snapshot.

The files under `tested-document-bytes/` are captures, not current navigation documents. Their relative links retain the original bundle-root context; their bytes are not rewritten for the archival location.
