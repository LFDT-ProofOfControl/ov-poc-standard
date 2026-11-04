# Reproduction recipe

This recipe uses only the exported bundle and released dependencies. It has not been executed. The recorded 13 matches precede export and do not validate this wrapper or a new environment. A reproduction produces a new record; it must not overwrite or be represented as the historical captures.

Use macOS 15.7.9 arm64 with Python 3.14.6 and `/usr/bin/sandbox-exec`. The wrapper requires the recorded Python executable hash and all recorded dependency-file hashes. A different environment stops before an assessor attempt; there is no fallback or relaxed pin. Use the Homebrew Python build identified in `RUNTIME.json` if available. Availability elsewhere is not established.

From this bundle directory, create a new environment outside the bundle and any future output directory, then fetch the three exact wheels and install offline:

```sh
python3.14 -m venv ../composed-reproduction-venv
mkdir ../composed-reproduction-wheels
../composed-reproduction-venv/bin/python -m pip download --only-binary=:all: --require-hashes --no-deps -r requirements.lock -d ../composed-reproduction-wheels
../composed-reproduction-venv/bin/python -m pip install --no-index --find-links ../composed-reproduction-wheels --require-hashes --no-deps -r requirements.lock
../composed-reproduction-venv/bin/python -B reproduce.py --venv ../composed-reproduction-venv --output ../composed-reproduction-output --review-token reviewed-export-reproduction
```

Do not reuse a previous output directory. The wrapper first rejects equality or either containment direction among resolved bundle, environment and output paths, including symlink aliases; output must be new. Bundle/output must also be outside all sandbox-readable runtime roots. It verifies its manifest, platform, executable and the exact installed dependency-file set and hashes before creating output. Only the original __pycache__ and .pyc exclusions apply; symlinks, extra, missing and changed site files are rejected without deletion or reinstallation. It then records an intent before each send to a restricted assessor process, grades each complete capture once, and records the result. Case order is P0, T2-A, T2-B, T2-C, T3-U, T3-R, T3-N, T5-M, T5-S, N2, N3, N4, N5. There is one concurrent assessor, one attempt per case, a 20-second child timeout and no retry/resume. A capture or grading exception halts; remaining cases are NOT_RUN. A semantic mismatch is preserved and does not cause tuning or replay.

The review-token string is an operator assertion, not authentication or permission. Before any full appraisal, the prepared prerequisite harness launches one separately retained sandbox component control: published Ed25519 positive/invalid-signature controls, fixed Merkle positive/invalid-node controls, one Q2 component, denied reads of the actual oracle and public case-label/generator-knowledge canaries (including a symlink escape), denied write/network/fork and absence of inherited API-key environment names. It uses the same launcher/profile as appraisals. Canary contents are synthetic public strings; no generator keys, actual credentials or frozen fixture regeneration are needed. Only permission-denied errno values satisfy denial controls; a missing file or refused connection is not treated as a sandbox denial.

The prepared control has not run. All 19 named outcomes must pass freshly before the first appraisal; any failure preserves capture, marks prerequisites NOT_READY and leaves every case NOT_RUN. The runner records the prerequisite intent/result separately from the thirteen cases. Historical prerequisite PASS records cannot satisfy this gate. See RUN-PLAN.json and PREREQUISITES.md. The permitted Q2 control uses an unchanged copy of P0 supplied material but never calls the full assessor or grader. P0 remains in the later thirteen-case order; its control use is disclosed, not a hidden full attempt.

Inspect the new `attempt-ledger.jsonl`, `RESULT.json` and per-run `capture/` files. UUIDs, monotonic timestamps, acquisition bindings and absolute runtime paths will differ. Compare semantic expectations and recorded attempt/outcome distinctions, not hashes of a new trace against a historical trace. The supplied bytes and exported source/oracle pins remain fixed. The original and exported oracle hashes differ only because of the declared metadata removal; no expectation is changed.

The scorer reports agreement with expectations, not accuracy on a population, hardware attestation or deployment conformance. The complete fixture set includes deliberate failures and uncertainty. No signing-key generation, external model/API call or network operation is part of an assessor attempt.
