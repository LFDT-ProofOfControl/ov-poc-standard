# Reproducing the bounded coverage-reconciliation example

This supplement exercises a finite, 13-case synthetic model. It does not change the standard or establish deployment coverage. A successful comparison means that the assessor outcome and the measured reference results match the frozen expectations. It does not mean every claim is positive: B1-a1 and B1-b intentionally remain not_established; B1-c is not_supported.

The recorded run used the source interfaces described here. This packaging recipe has been checked against those interfaces, but the selected public export and these shell snippets have not been executed as a new reproduction. There is no tested portable campaign driver in this package. Use the existing stage commands below; keep each attempt's outputs, and stop on the first failure.

## 1. Package layout and integrity

The expected location in the repository is:

~~~
examples/coverage-reconciliation/
  bjorn-implementation/
    adapter/adapter.py
    assessor/{assessor.py,assessor_common.py,assessor_b1.py,assessor_b2.py}
    comparator/compare.py
    runtime/orchestration-controller/controller.py
    runtime/orchestration-launcher/run_isolated.py
    runtime/orchestration-binding/check_orchestration.py
    schema/assessor-output.schema.json
  bjorn-vectors/
    fixtures/assessor/<case>.json
    generator-truth/<case>.json
    expected/<case>.json
~~~

The nine execution modules and all 39 case documents are required for the executed mode. The separately recorded comparator self-test is not part of this minimal export and is not an executed case. Verify the final export's file manifest before calculating local request pins. The controller, launcher and comparator contain linked revision pins; a mismatched checker or launcher must be rejected. Do not refresh those constants to bypass a mismatch.

This guide assumes a SHA256SUMS file at the export root, with paths relative to that root:

~~~sh
set -eu
set -C
BJORN_EXPORT=/absolute/path/to/examples/coverage-reconciliation
export BJORN_EXPORT
cd "$BJORN_EXPORT"
shasum -a 256 -c SHA256SUMS
~~~

Verify the complete final outgoing manifest before deriving request pins; hashing whichever files happen to be present does not establish the export revision.

## 2. Compatibility and preparation

Execute sections 1–5 in the same shell so the exported `BJORN_PY`, `BJORN_REF`, `BJORN_EXPORT` and `BJORN_WORK` values remain available. If a new shell is required, explicitly restore those reviewed values before continuing; do not infer or silently substitute paths.

The unchanged isolated launcher has a deliberately narrow host configuration:

| Setting | Required value |
|---|---|
| Docker executable | /usr/local/bin/docker |
| Docker context | desktop-linux |
| Assessor platform | linux/amd64 |
| Image index | sha256:4766d8b510c428e595d74b9cc5bbb2fae8e26316fffb4adc89908d79aacd58a2 |
| Platform child manifest | sha256:6e13e65c55e33adf203d77ee371cf8bf5d81bd4902ef07565721f46bf44917af |
| Image config digest recorded in the original environment | sha256:64d91f7b885eed272bba87909446b12ff408d4aaa5f1a0e9ca787bbea1a020b9 |

Have the pinned image available before running a case. The launcher uses --pull=never; it does not install Docker or pull an image. It also checks the local platform-filtered Docker inspection representation: both Id and Descriptor.digest must equal the platform child manifest, with architecture amd64 and os linux. A Docker installation that reports different fields is not automatically compatible. There is no CLI flag to substitute another Docker path, context, image or inspection convention. Supporting such a host requires a separately reviewed launcher change and linked-pin update; it is not covered by the recorded result.

The host measurement producer used a regular, copied CPython 3.13.13 executable with:

~~~
cryptography==50.0.2
cffi==2.1.1
pycparser==3.12
~~~

The interpreter and every ancestor of the supplied paths must be non-symlinks. A typical symlink-based virtual environment is rejected. Use a separate copied-interpreter environment with system-site-packages disabled. Do not replace a rejected path with a relaxed guard.

The following dependency lock is equivalent to `requirements.lock` (the displayed line order differs) and reproduces the recorded CPython 3.13 macOS ARM64 wheel selection. It is not a cross-platform lock:

~~~
cryptography==50.0.2 --hash=sha256:fa8f5efb344d6908a1ce62f4a24e2e5780f825d6f53f5f50ec5ffacac72936cb
cffi==2.1.1 --hash=sha256:19ee6127ee34de7d83ce3d371ebc5ed91addbdcc39f9ab15ce4eb35a4e534971
pycparser==3.12 --hash=sha256:a076f3f489b39b43ed13563a1dafe42447445bec2e294154ec5c57fcdda4c85e
~~~

| Wheel | Official distribution URL |
|---|---|
| cryptography-50.0.2-cp311-abi3-macosx_11_0_arm64.whl | https://files.pythonhosted.org/packages/e5/56/d194340cc4a57535e82e1bee9e89667ac4b7c13b5d3f59686deae3094dd5/cryptography-50.0.2-cp311-abi3-macosx_11_0_arm64.whl |
| cffi-2.1.1-cp313-cp313-macosx_11_0_arm64.whl | https://files.pythonhosted.org/packages/55/41/4c7042f317b9217502988f0873af87e16ad606dc20f84e546e3e6ce9764c/cffi-2.1.1-cp313-cp313-macosx_11_0_arm64.whl |
| pycparser-3.12-py3-none-any.whl | https://files.pythonhosted.org/packages/b6/ae/315bbeee126a769cbde43cf4908acb4b40408d8bf8bbf334dd7368d8dadf/pycparser-3.12-py3-none-any.whl |

Prepare these wheels separately, verify their hashes, and retain the downloaded metadata and installation inventory. For a prepared wheel directory and the lock above, an existing installer can target the copied environment without installing pip into it:

~~~sh
# Set these to absolute, physical paths chosen for this reproduction.
# BJORN_BASE_PY must already be the intended CPython 3.13.13 executable.
# BJORN_INSTALL_PY must already provide a pip version supporting --python.
BJORN_BASE_PY=/absolute/physical/path/to/cpython-3.13.13
BJORN_INSTALL_PY=/absolute/physical/path/to/an/existing/python-with-pip
BJORN_VENV=/absolute/physical/path/to/a/new-producer-venv
BJORN_WHEELS=/absolute/physical/path/to/the/verified-wheel-directory
BJORN_REQUIREMENTS_LOCK=/absolute/physical/path/to/the/requirements.lock
"$BJORN_BASE_PY" -I -B -m venv --copies --without-pip "$BJORN_VENV"
BJORN_PY="$BJORN_VENV/bin/python3.13"
export BJORN_PY

"$BJORN_INSTALL_PY" -I -B -m pip --python "$BJORN_PY" install \
  --no-index --find-links "$BJORN_WHEELS" --require-hashes \
  --no-deps --no-compile -r "$BJORN_REQUIREMENTS_LOCK"

"$BJORN_PY" -I -B -c \
  "import cryptography,json,sys; print(json.dumps({'python_version':sys.version.split()[0],'cryptography_version':cryptography.__version__}))"
~~~

The last output must report Python 3.13.13 and cryptography 50.0.2. Keep the executable digest, pyvenv.cfg, exact package inventory and setup logs with the attempt. The fixture-only mode does not invoke the producer and does not require a cryptography import. The executed mode verifies the version/import result again inside the producer stage. A missing or incompatible environment is a prerequisite failure, not permission to substitute fixture measurements.

## 3. Reference source

Prepare a separate upstream checkout, without modifying the export:

~~~sh
BJORN_REFERENCE_CHECKOUT=/absolute/physical/path/to/a/new-reference-checkout
git clone https://github.com/LFDT-ProofOfControl/ov-poc-standard.git "$BJORN_REFERENCE_CHECKOUT"
git -C "$BJORN_REFERENCE_CHECKOUT" checkout --detach \
  93d0e282fc177d5df741de4cdd6a0d0dacf1955a
BJORN_REF="$BJORN_REFERENCE_CHECKOUT/impl"
export BJORN_REF
~~~

The controller verifies these four exact files before any reference import and again around the producer invocation:

| Reference path | Bytes | SHA-256 |
|---|---:|---|
| impl/poc/__init__.py | 709 | d8ea20ed3b3ad06a44516140ca1e43f2f396c0c2d9426d822d914b6079ca37e9 |
| impl/poc/core.py | 30825 | 0a093e348e94bb2709b654f07e773964c98536c18e902aaa57082d26a39ce1da |
| impl/poc/merkle.py | 8698 | 22497d3605b47875802e08f7c2c0eb4f9c9a68da46f57d08eac198081a13c2a0 |
| impl/attacks/run_attacks.py | 16739 | 3603a34c15f74f798789f3685b86af1b9a6ae48c9c839bc6124229cc2e8a6601 |

Do not invoke the adapter directly as a substitute for the controller: its own two-file guard does not replace this four-file pre-import closure or the original producer receipt.

## 4. Select one case and prepare its request

Use absolute physical paths without symlink ancestors. Keep the source checkout, reference checkout, environment and fresh result directory separate. Do not use a path through a symlink such as a platform's temporary-directory alias.

~~~sh
set -eu
set -C  # refuse to overwrite redirected logs

BJORN_EXPORT=/absolute/path/to/examples/coverage-reconciliation
BJORN_WORK=/absolute/path/to/a/new-results-directory
BJORN_MODE=executed
BJORN_CASE=B1-a1
export BJORN_EXPORT BJORN_WORK BJORN_MODE BJORN_CASE

mkdir "$BJORN_WORK"
BJORN_IMPL="$BJORN_EXPORT/bjorn-implementation"
BJORN_VECTORS="$BJORN_EXPORT/bjorn-vectors"
BJORN_CONTROLLER="$BJORN_IMPL/runtime/orchestration-controller/controller.py"
BJORN_LAUNCHER="$BJORN_IMPL/runtime/orchestration-launcher/run_isolated.py"
BJORN_CHECKER="$BJORN_IMPL/runtime/orchestration-binding/check_orchestration.py"
BJORN_COMPARE="$BJORN_IMPL/comparator/compare.py"
BJORN_RUN="$BJORN_WORK/$BJORN_MODE-$BJORN_CASE"
BJORN_REQUEST="$BJORN_WORK/$BJORN_MODE-$BJORN_CASE-request.json"
export BJORN_RUN BJORN_REQUEST
~~~

The next recipe writes metadata only. It does not import the implementation, assign run IDs, run a case or claim that the local files are trusted; first verify the export manifest. The controller assigns fresh IDs when issuing the plan. Technical schema identifiers are retained exactly for wire compatibility.

~~~sh
"$BJORN_PY" -I -B - <<'PY'
import hashlib, json, os
from pathlib import Path

cases = ('B1-a1','B1-a2','B1-b','B1-c','B1-d','B2-a','B2-b','B2-c',
         'B2-d1','B2-d2','B2-e','B2-f','B2-g')
case, mode = os.environ['BJORN_CASE'], os.environ['BJORN_MODE']
if case not in cases or mode not in ('executed', 'fixture_only'):
    raise ValueError('unsupported case or mode')

def physical(value):
    p = Path(value)
    if not p.is_absolute() or '..' in p.parts:
        raise ValueError('absolute physical path required')
    for ancestor in (p, *p.parents):
        if ancestor.is_symlink():
            raise ValueError('symlink path rejected: ' + str(ancestor))
    return p

def pin(path):
    path = physical(path)
    if not path.is_file():
        raise ValueError('regular source file required')
    raw = path.read_bytes()
    return {'path':str(path), 'bytes':len(raw),
            'sha256':hashlib.sha256(raw).hexdigest()}

export = physical(os.environ['BJORN_EXPORT'])
impl, vectors = export/'bjorn-implementation', export/'bjorn-vectors'
python = pin(os.environ['BJORN_PY'])
assessor_names = ('assessor.py','assessor_common.py','assessor_b1.py','assessor_b2.py')
reference = None
if mode == 'executed':
    root = physical(os.environ['BJORN_REF'])
    reference_names = ('impl/poc/__init__.py','impl/poc/core.py',
                       'impl/poc/merkle.py','impl/attacks/run_attacks.py')
    reference = {
        'root':str(root),
        'revision':'93d0e282fc177d5df741de4cdd6a0d0dacf1955a',
        'files':[{'logical_path':name, **pin(root/name.removeprefix('impl/'))}
                 for name in reference_names],
    }
request = {
    'schema':'s3-bjorn-controller-request/v1',
    'mode':mode, 'case_id':case,
    'inputs':{
        'fixture':pin(vectors/'fixtures/assessor'/(case+'.json')),
        'truth':pin(vectors/'generator-truth'/(case+'.json')) if mode=='executed' else None,
        'expected':pin(vectors/'expected'/(case+'.json')),
    },
    'code':{
        'adapter':pin(impl/'adapter/adapter.py') if mode=='executed' else None,
        'reference':reference,
        'assessor':[{'logical_path':name, **pin(impl/'assessor'/name)}
                    for name in assessor_names],
        'launcher':pin(impl/'runtime/orchestration-launcher/run_isolated.py'),
        'comparator':{'version':'bjorn-compare/I1', **pin(impl/'comparator/compare.py')},
        'checker':pin(impl/'runtime/orchestration-binding/check_orchestration.py'),
    },
    'python':{**python, 'expected_python_version':'3.13.13',
              'expected_cryptography_version':'50.0.2'},
}
destination = physical(os.environ['BJORN_REQUEST'])
with destination.open('x', encoding='utf-8') as handle:
    json.dump(request, handle, indent=2, sort_keys=True, allow_nan=False)
    handle.write('\n')
destination.chmod(0o444)
PY
~~~

## 5. Executed mode: existing stage commands

Run these stages sequentially. The shell stops on a nonzero exit and refuses to replace a log. Inspect the captured error and preserve the whole attempt; do not restart a failed stage in the same run directory or silently choose another mode.

~~~sh
"$BJORN_PY" -I -B "$BJORN_CONTROLLER" issue \
  --request "$BJORN_REQUEST" --run-dir "$BJORN_RUN" \
  >"$BJORN_WORK/$BJORN_CASE-issue.stdout" 2>"$BJORN_WORK/$BJORN_CASE-issue.stderr"

"$BJORN_PY" -I -B "$BJORN_CONTROLLER" produce --run-dir "$BJORN_RUN" \
  >"$BJORN_WORK/$BJORN_CASE-produce.stdout" 2>"$BJORN_WORK/$BJORN_CASE-produce.stderr"

"$BJORN_PY" -I -B "$BJORN_CONTROLLER" assessor-spec --run-dir "$BJORN_RUN" \
  >"$BJORN_WORK/$BJORN_CASE-assessor-spec.stdout" 2>"$BJORN_WORK/$BJORN_CASE-assessor-spec.stderr"

"$BJORN_PY" -I -B "$BJORN_LAUNCHER" \
  --spec "$BJORN_RUN/assessor-spec.json" --output "$BJORN_RUN/assessor-receipt.json" \
  >"$BJORN_WORK/$BJORN_CASE-launch.stdout" 2>"$BJORN_WORK/$BJORN_CASE-launch.stderr"

chmod 444 "$BJORN_RUN/assessor-receipt.json"
BJORN_RECEIPT_SHA="$("$BJORN_PY" -I -B -c \
  'import hashlib,sys; print(hashlib.sha256(open(sys.argv[1],"rb").read()).hexdigest())' \
  "$BJORN_RUN/assessor-receipt.json")"

"$BJORN_PY" -I -B "$BJORN_CONTROLLER" binding-spec --run-dir "$BJORN_RUN" \
  --assessor-receipt "$BJORN_RUN/assessor-receipt.json" \
  --assessor-receipt-sha256 "$BJORN_RECEIPT_SHA" \
  >"$BJORN_WORK/$BJORN_CASE-binding.stdout" 2>"$BJORN_WORK/$BJORN_CASE-binding.stderr"

"$BJORN_PY" -I -B "$BJORN_CHECKER" \
  --spec "$BJORN_RUN/binding-spec.json" --output "$BJORN_RUN/orchestration-manifest.json" \
  >"$BJORN_WORK/$BJORN_CASE-check-links.stdout" 2>"$BJORN_WORK/$BJORN_CASE-check-links.stderr"

chmod 444 "$BJORN_RUN/orchestration-manifest.json"

"$BJORN_PY" -I -B "$BJORN_COMPARE" \
  --input "$BJORN_RUN/producer-out/assessor-input.json" \
  --expected "$BJORN_VECTORS/expected/$BJORN_CASE.json" \
  --outcome "$BJORN_RUN/outcome.json" \
  --measured "$BJORN_RUN/producer-out/measured.json" \
  --receipt "$BJORN_RUN/assessor-receipt.json" \
  --binding-spec "$BJORN_RUN/binding-spec.json" \
  --orchestration-manifest "$BJORN_RUN/orchestration-manifest.json" \
  --checker "$BJORN_CHECKER" \
  >"$BJORN_WORK/$BJORN_CASE-report.json" 2>"$BJORN_WORK/$BJORN_CASE-compare.stderr"
~~~

Do not parse and rewrite assessor stdout to create outcome.json. The binding stage extracts the original captured bytes from the original receipt and pins those bytes. Keep the plan, original receipts and generated artifacts from this same attempt together.

Check the report and receipts, not only process exit 0:

| Artifact | Required recorded result |
|---|---|
| Controller issue | PLAN_ISSUED_NO_EXECUTION; four distinct preassigned IDs in plan.json |
| Producer receipt | completed, exit_code 0; input_frozen_before_assessment true; original input and measured hashes |
| Assessor receipt | completed, attach_exit_code 0, start_attempts 1, cleanup.exit_code 0 |
| Orchestration manifest | ARTIFACT_LINKS_VERIFIED, mode executed, measurement_status PRODUCER_ARTIFACT_BOUND |
| Comparator report | overall PASS, run_mode executed, outcome_match true, measurement_match true, measurement_status MATCH |
| Comparator bindings | run_binding and orchestration both verified; comparison_run_id equals the plan's comparator ID |
| Problem arrays | mismatches, measurement_problems, run_binding_problems and orchestration_problems all empty |

The plan's orchestration, producer, assessor and comparator IDs must match their corresponding records. The manifest must retain the plan's exact component_run_ids. Additional dependencies are separate from mismatches: the frozen B2-d1 expectation permits the conservative A5 addition for each of the two complementary claims.

The assessor receives only its four program files and the selected input in read-only mounts. Generator truth, expected outcomes, measurements and host comparison remain outside the assessor container. Its container has no network, a read-only root, UID/GID 65532, dropped capabilities and bounded resources. Those controls and local receipts are not evidence against a malicious host.

## 6. Fixture-only mode

To assess the frozen fixture without the producer, start a separate fresh workspace, set BJORN_MODE=fixture_only, and generate the request above. The recipe then supplies null truth, adapter and reference fields.

Run issue, omit produce entirely, and continue with assessor-spec, launcher, binding-spec and the checker. Change the final comparator call to:

~~~sh
"$BJORN_PY" -I -B "$BJORN_COMPARE" \
  --input "$BJORN_RUN/fixture-assessor-input.json" \
  --expected "$BJORN_VECTORS/expected/$BJORN_CASE.json" \
  --outcome "$BJORN_RUN/outcome.json" \
  --receipt "$BJORN_RUN/assessor-receipt.json" \
  --binding-spec "$BJORN_RUN/binding-spec.json" \
  --orchestration-manifest "$BJORN_RUN/orchestration-manifest.json" \
  --checker "$BJORN_CHECKER" \
  >"$BJORN_WORK/$BJORN_CASE-report.json" 2>"$BJORN_WORK/$BJORN_CASE-compare.stderr"
~~~

The producer ID and producer receipt are null. The manifest and report must describe fixture_only mode. Expected overall is OUTCOME_PASS_FIXTURE_ONLY, outcome_match true, measurement_match null and measurement_status NOT_RUN, with both run bindings verified. Do not attach an old measured.json or describe this mode as a reference measurement.

## 7. Complete case selection

Use this fixed order, with one fresh request and run directory per case:

~~~
B1-a1 B1-a2 B1-b B1-c B1-d B2-a B2-b B2-c B2-d1 B2-d2 B2-e B2-f B2-g
~~~

For each identifier, the three case paths are fixtures/assessor/ID.json, generator-truth/ID.json and expected/ID.json under bjorn-vectors. For another case in the same mode, retain the workspace, set BJORN_CASE to the next identifier, recompute BJORN_RUN and BJORN_REQUEST from the variable assignments in section 4, and repeat only the metadata recipe and stage commands. Do not repeat environment creation or mkdir for the existing workspace. A loop may select these identifiers, but this guide does not supply a newly tested campaign driver. Do not let a loop continue after a failure. Label unattempted cases NOT_RUN and retain the failure rather than replacing it with a fresh successful record.

The separately recorded comparator self-test covered 20 synthetic in-memory examples with a controlled checker stub. It did not exercise the real artifact-link checker, Docker isolation, reference producer or these 13 cases. It is not included in this minimal export, and its success cannot replace the stage checks above.

## 8. Interpretation and retained evidence

Keep each attempt's request, pre-execution plan, issuance, producer receipt and pin, produced input/measured files, assessor spec and original receipt, exact outcome, binding spec, orchestration manifest, comparator report, stdout/stderr and environment/source hashes. Do not normalize or retrofit original receipts. If a public summary removes machine-specific paths, label it a derived view rather than byte-identical raw evidence.

The adapter measures a narrow reference-chain/signature-verification and generated-record/epoch-mapping path. It mirrors the reference attack builder's setup to permit the restart-link grant; it does not call that builder as an unchanged black box. Withheld events are not submitted. Population evidence, observations, alternate routes and mediation bindings remain simulated or declared under explicit assumptions.

The B1 cases construct epoch-separated evidence; they do not crash or restart a live process in real time. Neither family measures endpoint effects, and this supplement does not implement the full obligation-trigger procedure discussed in #173.

No RelyingParty is instantiated. Gateway executed=True is a release indication, not measured endpoint capability verification, dispatch or an effect. Matching these 13 expectations does not establish real-world completeness, general operational validation, minimal-premise dependency sets, independent reproduction or standards adoption.
