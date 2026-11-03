#!/usr/bin/env python3
"""Controller for one frozen Bjorn case. No automatic next stage."""
import argparse
import base64
import datetime
import hashlib
import json
import math
import os
from pathlib import Path
import re
import selectors
import stat
import subprocess
import sys
import time
import uuid

CASES = {'B1-a1', 'B1-a2', 'B1-b', 'B1-c', 'B1-d', 'B2-a', 'B2-b', 'B2-c',
         'B2-d1', 'B2-d2', 'B2-e', 'B2-f', 'B2-g'}
REVISION = '93d0e282fc177d5df741de4cdd6a0d0dacf1955a'
REFERENCE_FILES = {'impl/poc/__init__.py', 'impl/poc/core.py', 'impl/poc/merkle.py',
                   'impl/attacks/run_attacks.py'}
REFERENCE_PINS = {
    'impl/poc/__init__.py': (709, 'd8ea20ed3b3ad06a44516140ca1e43f2f396c0c2d9426d822d914b6079ca37e9'),
    'impl/poc/core.py': (30825, '0a093e348e94bb2709b654f07e773964c98536c18e902aaa57082d26a39ce1da'),
    'impl/poc/merkle.py': (8698, '22497d3605b47875802e08f7c2c0eb4f9c9a68da46f57d08eac198081a13c2a0'),
    'impl/attacks/run_attacks.py': (16739, '3603a34c15f74f798789f3685b86af1b9a6ae48c9c839bc6124229cc2e8a6601'),
}
ASSESSOR_FILES = {'assessor.py', 'assessor_common.py', 'assessor_b1.py', 'assessor_b2.py'}
CHECKER_SHA = 'c445c11409c7137d05f82bbb46540ecc870b22a5fcb1efc65a20bfd625d67d30'
LAUNCHER_SHA = '240d7f82369a8495d317817c858525130c14e6852a8063e71dc36ee74ea8b803'
MAX_BYTES = 16777216
STREAM_LIMIT = 262144
TIMEOUT = 60
ENV_PROBE = ("import cryptography,json,sys; print(json.dumps({"
             "'python_version':sys.version.split()[0],"
             "'cryptography_version':cryptography.__version__}))")


def need(ok, message):
    if not ok:
        raise ValueError(message)


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='microseconds').replace('+00:00', 'Z')


def digest(raw):
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def strict(raw):
    def pairs(items):
        out = {}
        for key, value in items:
            need(key not in out, 'duplicate JSON key')
            out[key] = value
        return out
    def reject(value):
        raise ValueError('non-finite JSON constant')
    def number(value):
        need(len(value) <= 128, 'JSON float token too long')
        value = float(value); need(math.isfinite(value), 'non-finite JSON float')
        return value
    value = json.loads(raw.decode('utf-8'), object_pairs_hook=pairs,
                       parse_constant=reject, parse_float=number)
    need(isinstance(value, dict), 'JSON object required')
    return value


def safe_path(value):
    path = Path(value)
    need(path.is_absolute() and '..' not in path.parts, 'absolute non-traversing path required')
    for node in [path, *path.parents]:
        need(not node.is_symlink(), 'symlink rejected: ' + str(node))
    return path


def raw_file(value, maximum=MAX_BYTES):
    path = safe_path(value)
    with os.fdopen(os.open(path, os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0)), 'rb') as handle:
        info = os.fstat(handle.fileno())
        need(stat.S_ISREG(info.st_mode) and info.st_size <= maximum, 'invalid file type/size')
        raw = handle.read(maximum + 1)
    need(len(raw) <= maximum, 'file exceeds limit')
    return raw


def check_digest(pin, raw, label):
    need(isinstance(pin, dict) and type(pin.get('bytes')) is int
         and digest(raw) == {'bytes': pin['bytes'], 'sha256': pin.get('sha256')}, label + ' pin mismatch')


def read_pin(pin, label, maximum=MAX_BYTES):
    raw = raw_file(pin['path'], maximum)
    check_digest(pin, raw, label)
    return raw


def pin_only(pin):
    return {'bytes': pin['bytes'], 'sha256': pin['sha256']}


def named_pins(items):
    return [{'path': item['logical_path'], **pin_only(item)} for item in items]


def serialize(doc):
    return (json.dumps(doc, ensure_ascii=False, indent=2, sort_keys=True) + '\n').encode('utf-8')


def publish(path, raw):
    path = safe_path(path)
    need(path.parent.is_dir(), 'output parent missing')
    with os.fdopen(os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL |
                          getattr(os, 'O_NOFOLLOW', 0), 0o600), 'wb') as handle:
        handle.write(raw); handle.flush(); os.fsync(handle.fileno())
        os.fchmod(handle.fileno(), 0o444)
    return {'path': str(path), **digest(raw)}


def verify_request(request):
    need(set(request) == {'schema', 'mode', 'case_id', 'inputs', 'code', 'python'}, 'unexpected request fields')
    need(request['schema'] == 's3-bjorn-controller-request/v1', 'unsupported request')
    need(request['mode'] in {'executed', 'fixture_only'} and request['case_id'] in CASES, 'unsupported mode/case')
    inputs, code = request['inputs'], request['code']
    need(set(inputs) == {'fixture', 'truth', 'expected'}, 'input pins incomplete')
    need(set(code) == {'adapter', 'reference', 'assessor', 'launcher', 'comparator', 'checker'}, 'code pins incomplete')
    fixture = strict(read_pin(inputs['fixture'], 'fixture'))
    expected = strict(read_pin(inputs['expected'], 'expected'))
    need(fixture.get('schema') == 'bjorn-vectors/assessor-input/v0', 'fixture schema mismatch')
    need(fixture.get('case_id') == expected.get('case_id') == request['case_id'], 'case correspondence mismatch')
    need(fixture.get('family') == expected.get('family') == request['case_id'][:2], 'family correspondence mismatch')
    files = code['assessor']
    need(isinstance(files, list) and len(files) == 4
         and {item['logical_path'] for item in files} == ASSESSOR_FILES, 'exact four assessor files required')
    roots = set()
    for item in files:
        read_pin(item, 'assessor')
        path = safe_path(item['path']); need(path.name == item['logical_path'], 'assessor must have flat filenames')
        roots.add(path.parent)
    need(len(roots) == 1, 'assessor files must share one source directory')
    read_pin(code['launcher'], 'launcher'); need(code['launcher']['sha256'] == LAUNCHER_SHA, 'wrong launcher revision')
    read_pin(code['checker'], 'checker'); need(code['checker']['sha256'] == CHECKER_SHA, 'wrong checker revision')
    read_pin(code['comparator'], 'comparator')
    need(isinstance(code['comparator'].get('version'), str) and code['comparator']['version'], 'comparator version required')
    python = request['python']
    read_pin(python, 'interpreter', 134217728)
    need(os.access(python['path'], os.X_OK), 'interpreter not executable')
    need(isinstance(python.get('expected_python_version'), str) and python['expected_python_version'], 'Python version pin required')
    if request['mode'] == 'executed':
        truth = strict(read_pin(inputs['truth'], 'generator truth'))
        need(truth.get('schema') == 'bjorn-vectors/generator-truth/v0', 'truth schema mismatch')
        need(truth.get('case_id') == fixture['case_id'] and truth.get('family') == fixture['family'], 'truth correspondence mismatch')
        read_pin(code['adapter'], 'adapter')
        ref = code['reference']; need(ref['revision'] == REVISION, 'reference revision mismatch')
        root = safe_path(ref['root']); need(root.is_dir(), 'reference impl directory missing')
        need(len(ref['files']) == 4 and {item['logical_path'] for item in ref['files']} == REFERENCE_FILES,
             'all four imported/reference files must be pinned')
        for item in ref['files']:
            need(safe_path(item['path']) == root / item['logical_path'].removeprefix('impl/'), 'reference path/root mismatch')
            size, sha = REFERENCE_PINS[item['logical_path']]
            need(pin_only(item) == {'bytes': size, 'sha256': sha}, 'reference pin differs from verified revision')
            read_pin(item, item['logical_path'])
        need(isinstance(python.get('expected_cryptography_version'), str)
             and python['expected_cryptography_version'], 'expected cryptography version required; not yet verification')
    else:
        need(inputs['truth'] is None and code['adapter'] is None and code['reference'] is None,
             'fixture-only mode must not include a producer')
    return fixture


def plan_pins(request):
    code = request['code']; executed = request['mode'] == 'executed'
    return {'adapter': pin_only(code['adapter']) if executed else None,
            'reference_code': {'revision': REVISION, 'files': named_pins(code['reference']['files'])} if executed else None,
            'assessor_code': named_pins(code['assessor']), 'launcher': pin_only(code['launcher']),
            'expected': pin_only(request['inputs']['expected']),
            'comparator': {'version': code['comparator']['version'], **pin_only(code['comparator'])}}


def build_plan(request):
    # Called only after actual pinned files have been verified by issue().
    executed = request['mode'] == 'executed'
    ids = [uuid.uuid4().hex for _ in range(4)]
    need(len(set(ids)) == 4, 'identifier collision')
    return {'schema': 'bjorn-implementation/orchestration-plan/v1', 'phase': 'pre_execution',
            'run_id': ids[0], 'assigned_at': now(), 'mode': request['mode'],
            'component_run_ids': {'producer': ids[1] if executed else None, 'assessor': ids[2], 'comparator': ids[3]},
            'pins': plan_pins(request)}


def issue(request_path, run_dir):
    request_raw = raw_file(request_path); request = strict(request_raw)
    verify_request(request)
    root = safe_path(run_dir); need(not root.exists() and root.parent.is_dir(), 'fresh run directory required')
    plan_raw = serialize(build_plan(request))
    root.mkdir(mode=0o700)
    req = publish(root / 'request.json', request_raw)
    plan = publish(root / 'plan.json', plan_raw)
    issuance = {'schema': 's3-bjorn-issuance/v1', 'request': digest(request_raw), 'plan': digest(plan_raw),
                'controller': digest(raw_file(__file__)), 'issued_at': now()}
    publish(root / 'issuance.json', serialize(issuance))
    return {'status': 'PLAN_ISSUED_NO_EXECUTION', 'request': req, 'plan': plan}


def load_run(run_dir):
    root = safe_path(run_dir); need(root.is_dir(), 'run directory missing')
    issuance = strict(raw_file(root / 'issuance.json'))
    request_raw, plan_raw = raw_file(root / 'request.json'), raw_file(root / 'plan.json')
    check_digest(issuance['request'], request_raw, 'issued request')
    check_digest(issuance['plan'], plan_raw, 'issued plan')
    check_digest(issuance['controller'], raw_file(__file__), 'issuing controller')
    request, plan = strict(request_raw), strict(plan_raw)
    verify_request(request)
    need(plan.get('schema') == 'bjorn-implementation/orchestration-plan/v1'
         and plan.get('phase') == 'pre_execution' and plan['mode'] == request['mode']
         and plan['pins'] == plan_pins(request), 'plan differs from issued request')
    return root, request, plan, plan_raw


def stream_record(raw):
    return {**digest(raw), 'base64': base64.b64encode(raw).decode('ascii'), 'text': raw.decode('utf-8', 'replace')}


def capture(argv, cwd):
    """One owned child; bounded capture; never retry or interpret success here."""
    result = {'argv': argv, 'attempted_at': now(), 'started': False, 'exit_code': None}
    buffers = {'stdout': bytearray(), 'stderr': bytearray()}
    proc, selector = None, None
    try:
        proc = subprocess.Popen(argv, cwd=str(cwd), stdin=subprocess.DEVNULL,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result.update(started=True, pid=proc.pid, started_at=result['attempted_at'])
        selector = selectors.DefaultSelector()
        for label, stream in [('stdout', proc.stdout), ('stderr', proc.stderr)]:
            os.set_blocking(stream.fileno(), False)
            selector.register(stream, selectors.EVENT_READ, label)
        deadline = time.monotonic() + TIMEOUT
        while selector.get_map():
            need(time.monotonic() < deadline, 'child timeout')
            for key, _ in selector.select(timeout=0.1):
                raw = os.read(key.fileobj.fileno(), 65536)
                if not raw:
                    selector.unregister(key.fileobj); continue
                room = STREAM_LIMIT - len(buffers[key.data])
                buffers[key.data].extend(raw[:room])
                need(len(raw) <= room, key.data + ' capture limit exceeded')
        proc.wait(timeout=3)
    except Exception as exc:
        result['capture_error'] = type(exc).__name__ + ': ' + str(exc)
    finally:
        if proc is not None:
            try:
                if proc.poll() is None:
                    proc.kill(); proc.wait(timeout=3)
            except Exception as exc:
                result['cleanup_error'] = type(exc).__name__ + ': ' + str(exc)
            result['exit_code'] = proc.returncode
            proc.stdout.close(); proc.stderr.close()
        if selector is not None:
            selector.close()
        result['finished_at'] = now()
        result.update({label: stream_record(bytes(raw)) for label, raw in buffers.items()})
    return result


def successful_capture(record):
    need(record.get('started') is True and record.get('exit_code') == 0
         and not record.get('capture_error') and not record.get('cleanup_error'), 'owned child did not complete successfully')
    return strict(base64.b64decode(record['stdout']['base64'], validate=True))


def validate_produced(out, request, plan, summary):
    out = safe_path(out)
    need(out.is_dir() and {p.name for p in out.iterdir()} == {'assessor-input.json', 'measured.json'},
         'producer output inventory differs from the two contracted files')
    inp = raw_file(out / 'assessor-input.json'); meas = raw_file(out / 'measured.json')
    input_doc, measured = strict(inp), strict(meas)
    need(input_doc.get('schema') == 'bjorn-vectors/assessor-input/v0', 'produced input schema mismatch')
    need(stat.S_IMODE((out / 'assessor-input.json').stat().st_mode) & 0o222 == 0,
         'adapter did not freeze its produced input')
    need(input_doc.get('case_id') == measured.get('case_id') == request['case_id']
         and input_doc.get('family') == measured.get('family') == request['case_id'][:2], 'produced identity mismatch')
    need(measured.get('schema') == 'bjorn-implementation/measured/v0'
         and measured.get('orchestration_run_id') == plan['run_id']
         and measured.get('producer_run_id') == plan['component_run_ids']['producer'], 'measured run identity mismatch')
    need(measured.get('input_sha256') == digest(inp)['sha256'] and type(measured.get('input_bytes')) is int
         and measured['input_bytes'] == len(inp), 'measurement input digest mismatch')
    need(measured.get('fixture') == pin_only(request['inputs']['fixture'])
         and measured.get('truth') == pin_only(request['inputs']['truth']), 'measurement source pins mismatch')
    need(summary.get('result') == 'produced' and summary.get('case_id') == request['case_id']
         and summary.get('assessor_input') == digest(inp) and summary.get('measured') == digest(meas),
         'adapter summary does not bind exact produced artifacts')
    return inp, meas


def produce(run_dir):
    root, request, plan, plan_raw = load_run(run_dir)
    need(request['mode'] == 'executed', 'fixture-only has no producer')
    out = root / 'producer-out'
    need(all(not safe_path(root / name).exists() for name in
             ['producer-out', 'producer-attempt.json', 'producer-receipt.json', 'producer-receipt-pin.json']),
         'producer outputs must all be fresh; never adopt previous artifacts')
    attempt = {'run_id': plan['component_run_ids']['producer'], 'orchestration_run_id': plan['run_id'],
               'plan': digest(plan_raw), 'started_at': now()}
    publish(root / 'producer-attempt.json', serialize(attempt))
    receipt = {'schema': 'bjorn-implementation/producer-receipt/v1', 'phase': 'measurement_producer',
        'orchestration': {'run_id': plan['run_id'], 'plan': digest(plan_raw)}, 'run_id': attempt['run_id'],
        'status': 'failed', 'exit_code': None, 'started_at': attempt['started_at'],
        'code': {'adapter': plan['pins']['adapter'], 'reference_code': plan['pins']['reference_code']},
        'input_frozen_before_assessment': False, 'controller': digest(raw_file(__file__))}
    try:
        python = request['python']
        env = capture([python['path'], '-I', '-B', '-c', ENV_PROBE], root)
        receipt['environment_probe'] = env
        verify_request(request)
        observed = successful_capture(env)
        need(observed == {'python_version': python['expected_python_version'],
                          'cryptography_version': python['expected_cryptography_version']}, 'technical environment pin mismatch')
        receipt['environment_observed'] = observed
        # Recheck every local code/source pin and ancestor after the environment import,
        # and again immediately after the adapter. Never use -S: cryptography uses site packages.
        verify_request(request)
        argv = [python['path'], '-I', '-B', request['code']['adapter']['path'],
                '--impl', request['code']['reference']['root'], '--fixture', request['inputs']['fixture']['path'],
                '--truth', request['inputs']['truth']['path'], '--out', str(out),
                '--orchestration-run-id', plan['run_id'], '--producer-run-id', attempt['run_id']]
        child = capture(argv, root); receipt['adapter_invocation'] = child; receipt['exit_code'] = child['exit_code']
        verify_request(request)
        summary = successful_capture(child)
        inp, meas = validate_produced(out, request, plan, summary)
        (out / 'assessor-input.json').chmod(0o444); (out / 'measured.json').chmod(0o444)
        need(raw_file(out / 'assessor-input.json') == inp and raw_file(out / 'measured.json') == meas,
             'producer artifacts changed during freeze')
        receipt.update(status='completed', outputs={'assessor_input': digest(inp), 'measured': digest(meas)},
                       input_frozen_before_assessment=True, artifacts_frozen_at=now())
    except Exception as exc:
        receipt['failure'] = type(exc).__name__ + ': ' + str(exc)
    receipt['finished_at'] = now()  # Component completion includes artifact validation/freezing.
    ref = publish(root / 'producer-receipt.json', serialize(receipt))
    publish(root / 'producer-receipt-pin.json', serialize(ref))
    return {'status': receipt['status'], 'producer_receipt': ref,
            'adapter_process_started': receipt.get('adapter_invocation', {}).get('started', False)}


def produced_input(root, request, plan, plan_raw):
    if request['mode'] == 'fixture_only':
        return request['inputs']['fixture'], None, None
    ref = strict(raw_file(root / 'producer-receipt-pin.json'))
    need(ref['path'] == str(root / 'producer-receipt.json'), 'producer receipt path mismatch')
    receipt_raw = read_pin(ref, 'owned producer receipt'); receipt = strict(receipt_raw)
    need(receipt.get('status') == 'completed' and type(receipt.get('exit_code')) is int and receipt['exit_code'] == 0
         and receipt.get('input_frozen_before_assessment') is True
         and receipt.get('orchestration') == {'run_id': plan['run_id'], 'plan': digest(plan_raw)}
         and receipt.get('run_id') == plan['component_run_ids']['producer'], 'producer receipt does not establish completed owned production')
    inp = root / 'producer-out/assessor-input.json'; meas = root / 'producer-out/measured.json'
    input_ref = {'path': str(inp), **receipt['outputs']['assessor_input']}
    measured_ref = {'path': str(meas), **receipt['outputs']['measured']}
    read_pin(input_ref, 'frozen produced input'); read_pin(measured_ref, 'frozen measurement')
    return input_ref, measured_ref, ref


def assessor_spec(run_dir):
    root, request, plan, plan_raw = load_run(run_dir)
    need(not (root / 'assessor-spec.json').exists(), 'assessor spec already exists')
    inp, _, _ = produced_input(root, request, plan, plan_raw)
    if request['mode'] == 'fixture_only':
        inp = publish(root / 'fixture-assessor-input.json', read_pin(inp, 'fixture input'))
    spec = {'schema_version': 2, 'module': 'assessor',
            'program_root': str(Path(request['code']['assessor'][0]['path']).parent),
            'files': [{'path': item['logical_path'], 'sha256': item['sha256']} for item in request['code']['assessor']],
            'input': {'path': inp['path'], 'sha256': inp['sha256']},
            'orchestration': {'run_id': plan['run_id'], 'component_run_id': plan['component_run_ids']['assessor'],
                              'plan': digest(plan_raw)}}
    return {'status': 'ASSESSOR_SPEC_ONLY_NO_LAUNCH', 'spec': publish(root / 'assessor-spec.json', serialize(spec))}


def assemble_binding(run_dir, assessor_receipt_path, assessor_receipt_sha256):
    root, request, plan, plan_raw = load_run(run_dir)
    need(not (root / 'binding-spec.json').exists() and not (root / 'outcome.json').exists(), 'binding outputs already exist')
    inp, measured, producer = produced_input(root, request, plan, plan_raw)
    if request['mode'] == 'fixture_only':
        inp = {'path': str(root / 'fixture-assessor-input.json'), **digest(read_pin(inp, 'fixture input'))}
        read_pin(inp, 'frozen fixture input')
    raw = raw_file(assessor_receipt_path)
    need(digest(raw)['sha256'] == assessor_receipt_sha256, 'assessor receipt external pin mismatch')
    receipt = strict(raw)
    need(receipt.get('module') == 'assessor' and receipt.get('profile') == 's3-bjorn-isolated-python-v1'
         and receipt.get('status') == 'completed' and type(receipt.get('attach_exit_code')) is int and receipt['attach_exit_code'] == 0
         and receipt.get('orchestration') == {'run_id': plan['run_id'], 'plan': digest(plan_raw)}
         and receipt.get('run_id') == plan['component_run_ids']['assessor'], 'assessor receipt identity/status mismatch')
    check_digest(receipt['spec'], raw_file(root / 'assessor-spec.json'), 'exact assessor spec')
    check_digest(receipt['input'], read_pin(inp, 'consumed input'), 'assessor consumed input')
    outcome = base64.b64decode(receipt['stdout']['base64'], validate=True)
    check_digest(receipt['stdout'], outcome, 'captured stdout'); strict(outcome)
    code = request['code']; executed = request['mode'] == 'executed'
    binding = {'plan': {'path': str(root / 'plan.json'), 'sha256': digest(plan_raw)['sha256']},
        'producer_receipt': {'path': producer['path'], 'sha256': producer['sha256']} if producer else None,
        'assessor_receipt': {'path': str(safe_path(assessor_receipt_path)), 'sha256': assessor_receipt_sha256},
        'input': inp['path'], 'outcome': str(root / 'outcome.json'), 'measured': measured['path'] if measured else None,
        'expected': request['inputs']['expected']['path'],
        'code': {'adapter': code['adapter']['path'] if executed else None,
                 'reference_code': {item['logical_path']: item['path'] for item in code['reference']['files']} if executed else None,
                 'assessor_code': {item['logical_path']: item['path'] for item in code['assessor']},
                 'launcher': code['launcher']['path'], 'comparator': code['comparator']['path']}}
    publish(root / 'outcome.json', outcome)
    ref = publish(root / 'binding-spec.json', serialize(binding))
    return {'status': 'BINDING_SPEC_ASSEMBLED_NOT_VERIFIED', 'binding_spec': ref,
            'checker': code['checker'], 'comparison_executed': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    issue_parser = sub.add_parser('issue'); issue_parser.add_argument('--request', required=True); issue_parser.add_argument('--run-dir', required=True)
    for name in ['produce', 'assessor-spec']:
        item = sub.add_parser(name); item.add_argument('--run-dir', required=True)
    binding = sub.add_parser('binding-spec'); binding.add_argument('--run-dir', required=True)
    binding.add_argument('--assessor-receipt', required=True); binding.add_argument('--assessor-receipt-sha256', required=True)
    args = parser.parse_args()
    try:
        if args.command == 'issue': result = issue(args.request, args.run_dir)
        elif args.command == 'produce': result = produce(args.run_dir)
        elif args.command == 'assessor-spec': result = assessor_spec(args.run_dir)
        else: result = assemble_binding(args.run_dir, args.assessor_receipt, args.assessor_receipt_sha256)
    except (OSError, ValueError, KeyError, TypeError, AttributeError, RecursionError) as exc:
        print(json.dumps({'status': 'ERROR', 'error': type(exc).__name__ + ': ' + str(exc)}), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if result['status'] == 'failed' else 0


if __name__ == '__main__':
    sys.exit(main())
