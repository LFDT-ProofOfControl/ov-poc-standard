#!/usr/bin/env python3
'''Measurement producer (adapter) for the bjorn-implementation candidate, revision I1.

Public-package source derivative; this copy has not been executed.

Usage (as invoked by the producer harness):
    python3 -I -B adapter.py --impl DIR --fixture FILE --truth FILE --out DIR
        --orchestration-run-id ID --producer-run-id ID

--impl is the upstream impl/ directory, checked out at the reference pin.
See package REPRODUCE.md for the runtime steps and NOTICE.md for scope and provenance.

Pins:
- Before anything is imported from --impl, the exact bytes of
  impl/poc/core.py and impl/attacks/run_attacks.py are checked against the
  recorded pins. They are checked again after import, and any mismatch
  refuses.
- core.py imports poc/__init__.py and poc/merkle.py, which carry no pin
  here. This two-file check is not a pre-import closure over the reference
  code. The producer harness verifies all transitive reference pins
  (core.py, run_attacks.py, poc/__init__.py, poc/merkle.py) before and after
  this process, and the reference_code pins of the plan must name them.
- run_attacks.py is pinned because its build() setup is mirrored, not
  called. build() grants no source.restart kind, which the epoch link needs
  for this setup. Nothing from run_attacks.py is imported.

Prerequisites and run IDs:
- The cryptography package must already be importable by the interpreter
  that runs this adapter. It is never installed.
- The orchestration and producer run IDs are preassigned by the producer
  harness from the frozen plan, and this adapter only copies them.
- The producer receipt is issued by that harness, not by this adapter.

Generation:
- Records are generated through the reference Gateway. Each chain has its
  own attesting environment and evidence store.
- All chains share one signing key, so a later epoch is a restart from
  genesis.
- Withheld B1 events and B2 alternate-path effects are never submitted.
- The content of a generated record is read from the submitted action only
  after its snapshot digest has been recomputed and found equal to the signed
  token claim.
- Record times are copied from the fixture record at the same chain
  position. Generated timestamps are not compared.
- Each full chain, control records included, is checked with
  Verifier.verify_chain.

Not measured:
- No RelyingParty is instantiated. Gateway.submit is called without a
  relying party, and on that path the reference gateway returns
  executed=True once the evidence is recorded. The adapter requires that
  value only as the gateway release signal; it is not a measured
  RelyingParty execution result.
- Endpoint capability checks (signature, measurement, resource, nonce
  replay, action binding) and dispatch are therefore not measured. The
  measurement excludes RelyingParty execution; see package NOTICE.md.

Simulated and declared parts:
- Population evidence, observations, routes, bindings, assumptions and the
  integrity declaration are copied from the frozen fixture. They are
  simulated or declared parts, not reference behavior.
- Measured integrity goes only to measured.json, never into the assessor
  input.

Files:
- Bytecode writing is disabled before any further import, so importing the
  reference package or its dependencies writes no __pycache__ directory.
  The harness additionally invokes the adapter with -I -B.
- The fixture and truth files are only read.
- Exactly two files are written, into a --out directory that must not exist
  yet: assessor-input.json, made read-only before any assessment, and
  measured.json.
- After a failure the directory may hold a partial result. It must not be
  used.

Exit codes:
- 0: produced.
- 2: usage, pin, input or I/O refusal.
- 3: missing prerequisite.
- 1: generation or internal error.
'''
import sys

# Suppress bytecode writes before any further import.
# A writable reference checkout must not gain poc/__pycache__ or any other
# file outside --out.
sys.dont_write_bytecode = True

import copy
import hashlib
import importlib
import importlib.util
import json
import os
import re

MEASURED_SCHEMA = 'bjorn-implementation/measured/v0'
INPUT_SCHEMA = 'bjorn-vectors/assessor-input/v0'
TRUTH_SCHEMA = 'bjorn-vectors/generator-truth/v0'
REFERENCE_REVISION = '93d0e282fc177d5df741de4cdd6a0d0dacf1955a'
REFERENCE_PINS = (
    ('poc/core.py', 30825, '0a093e348e94bb2709b654f07e773964c98536c18e902aaa57082d26a39ce1da'),
    ('attacks/run_attacks.py', 16739, '3603a34c15f74f798789f3685b86af1b9a6ae48c9c839bc6124229cc2e8a6601'),
)
OPTIONS = ('--impl', '--fixture', '--truth', '--out', '--orchestration-run-id', '--producer-run-id')
RUN_ID_RE = re.compile('[0-9a-f]{32}')
PRINCIPAL = 'user:alice'
HARNESS_KINDS = frozenset({'obligation.record', 'source.restart', 'effect.record'})
B2_AGENT_ID = 'did:web:example:agents:ref-1'
ABSENT = '<absent>'


class Refused(Exception):
    '''Usage, pin or input refusal (exit 2).'''


class Missing(Exception):
    '''A prerequisite is not present (exit 3).'''


class GenerationError(Exception):
    '''The reference implementation did not behave as the adapter requires (exit 1).'''


def is_int(value):
    return isinstance(value, int) and not isinstance(value, bool)


def is_text(value):
    return isinstance(value, str) and value != ''


def digest_of(raw):
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def _unique_pairs(pairs):
    seen = {}
    for key, value in pairs:
        if key in seen:
            raise Refused('duplicate JSON key ' + key)
        seen[key] = value
    return seen


def _reject_constant(name):
    raise Refused('non-finite JSON number ' + name)


def _finite_float(text):
    value = float(text)
    if value != value or value in (float('inf'), float('-inf')):
        raise Refused('JSON number ' + text[:40] + ' is not finite as a float')
    return value


def load_json(path, where):
    with open(path, 'rb') as handle:
        raw = handle.read()
    try:
        doc = json.loads(raw.decode('utf-8'), object_pairs_hook=_unique_pairs, parse_constant=_reject_constant,
                         parse_float=_finite_float)
    except (UnicodeDecodeError, ValueError, RecursionError) as exc:
        raise Refused(where + ': not strict JSON: ' + str(exc))
    if not isinstance(doc, dict):
        raise Refused(where + ': must be a JSON object')
    return doc, digest_of(raw)


def serialize(doc):
    return (json.dumps(doc, indent=2, ensure_ascii=False) + chr(10)).encode('utf-8')


def parse_args(argv):
    if len(argv) != 2 * len(OPTIONS):
        raise Refused('usage: adapter.py ' + ' '.join(o + ' VALUE' for o in OPTIONS))
    args = {}
    for name, value in zip(argv[0::2], argv[1::2]):
        if name not in OPTIONS or name in args or not value:
            raise Refused('unknown, repeated or empty option ' + name)
        args[name] = value
    ids = (args['--orchestration-run-id'], args['--producer-run-id'])
    if not all(RUN_ID_RE.fullmatch(i) for i in ids) or ids[0] == ids[1]:
        raise Refused('run IDs must be distinct lowercase 32-hex strings preassigned by the harness')
    return args


def check_pins(impl):
    pins = []
    for logical, size, sha in REFERENCE_PINS:
        path = os.path.join(impl, *logical.split('/'))
        if os.path.islink(path) or not os.path.isfile(path):
            raise Refused('impl/' + logical + ': missing, not a regular file, or a symlink')
        with open(path, 'rb') as handle:
            got = digest_of(handle.read())
        if got != {'bytes': size, 'sha256': sha}:
            raise Refused('impl/' + logical + ': bytes differ from the pin at ' + REFERENCE_REVISION)
        pins.append({'path': 'impl/' + logical, 'bytes': got['bytes'], 'sha256': got['sha256']})
    return pins


def load_reference(impl):
    '''Import the pinned reference core; called only after check_pins.'''
    # Bytecode writing stays disabled for every import below (set at module start).
    sys.dont_write_bytecode = True
    if importlib.util.find_spec('cryptography') is None:
        raise Missing('the cryptography package is not importable by this interpreter; this adapter never installs it')
    sys.path.insert(0, impl)
    importlib.import_module('poc')
    core = importlib.import_module('poc.core')
    expected = os.path.realpath(os.path.join(impl, 'poc', 'core.py'))
    if os.path.realpath(getattr(core, '__file__', None) or '') != expected:
        raise Refused('poc.core was not loaded from the pinned impl/poc/core.py')
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    return core, Ed25519PrivateKey


def check_fixture(fixture):
    if fixture.get('schema') != INPUT_SCHEMA:
        raise Refused('fixture: schema is not ' + INPUT_SCHEMA)
    if not is_text(fixture.get('case_id')) or fixture.get('family') not in ('B1', 'B2'):
        raise Refused('fixture: case_id must be a string and family B1 or B2')
    records = fixture.get('records')
    if not isinstance(records, list) or not records or not all(isinstance(r, dict) for r in records):
        raise Refused('fixture: records must be a non-empty list of objects')
    for record in records:
        if not is_text(record.get('record_id')) or not is_int(record.get('seq')) or not is_text(record.get('time')):
            raise Refused('fixture: every record needs a string record_id, an integer seq and a time')
    ids = [r['record_id'] for r in records]
    if len(set(ids)) != len(ids):
        raise Refused('fixture: duplicate record_id')
    return records


def check_truth(truth, fixture):
    if truth.get('schema') != TRUTH_SCHEMA:
        raise Refused('truth: schema is not ' + TRUTH_SCHEMA)
    for name in ('case_id', 'family'):
        if truth.get(name) != fixture.get(name):
            raise Refused('truth.' + name + ' differs from the fixture')
    injected = truth.get('injected', [])
    tokens = truth.get('leak_check_tokens', [])
    if not isinstance(injected, list) or not all(isinstance(i, dict) for i in injected):
        raise Refused('truth: injected must be a list of objects')
    if not isinstance(tokens, list) or not all(is_text(t) for t in tokens):
        raise Refused('truth: leak_check_tokens must be a list of strings')
    return injected, tokens


def check_withheld(records, injected):
    '''A withheld event or alternate-path effect must not be among the records to submit.'''
    carried = {r.get(k) for r in records for k in ('obligation_id', 'effect_ref') if isinstance(r.get(k), str)}
    for item in injected:
        for key in ('obligation_id', 'effect_ref'):
            value = item.get(key)
            if isinstance(value, str) and value in carried:
                raise Refused('truth: injected ' + key + ' ' + value + ' is carried by a fixture record')


def check_leaks(text, tokens):
    found = [t for t in tokens if t in text]
    if found:
        raise Refused('generated assessor input contains leak-check tokens: ' + ', '.join(found))


def identity_entry(fixture_id, claims, chain):
    return {'fixture_record_id': fixture_id, 'chain': chain, 'agent_id': claims['agent_id'],
            'step_index': claims['step_index'], 'snapshot_hash': claims['canonical_snapshot_hash'],
            'chain_head': claims['chain_head']}


class Generator:
    '''Mirrors run_attacks.build(): one grant, a path-aware policy, no anchor.
    One signing key serves every chain of the run. No RelyingParty is created.'''

    def __init__(self, core, key_class, resources):
        self.core = core
        grant = core.Grant(principal=PRINCIPAL, allowed_kinds=HARNESS_KINDS,
                           allowed_resources=frozenset(resources), max_spend=0.0,
                           max_sensitivity_egress='public')
        self.policy = core.PolicyEngine(grant, path_aware=True)
        self.key = key_class.generate()

    def chain(self, agent_id):
        ae = self.core.AttestingEnvironment(self.policy, anchor=None, anchor_interval_s=0.0, signing_key=self.key)
        store = self.core.EvidenceStore()
        return ae, store, self.core.Gateway(ae, store, agent_id=agent_id)

    def submit(self, ae, store, gw, action):
        '''Submit one action; return its token after binding the action content to the signed claim.'''
        step = ae.step_index
        snap = {'agent_id': gw.agent_id, 'action': json.loads(action.canonical_form()),
                'path_summary': ae.phi.digest(), 'step_index': step}
        expected = self.core.sha256(self.core.canonical(snap))
        before = len(store.records)
        # Submitted without a relying party: executed=True here is the gateway
        # release signal after evidence was recorded, not a measured RelyingParty
        # execution or capability check.
        result = gw.submit(action)
        if result.get('verdict') != 'ALLOW' or result.get('executed') is not True or len(store.records) != before + 1:
            raise GenerationError('gateway did not record and release ' + action.kind + ': ' + str(result.get('reason')))
        token = store.records[-1]
        claims = token['poc_claims']
        if (claims['step_index'] != step or claims['agent_id'] != gw.agent_id
                or self.core.untag(claims['canonical_snapshot_hash']) != expected):
            raise GenerationError('signed token does not commit to the submitted action at step ' + str(step))
        return token


def generate_b1(gen, records, fixture):
    instances = fixture.get('source_instances')
    if not isinstance(instances, list) or len(instances) != 1 or not isinstance(instances[0], dict):
        raise Refused('fixture: exactly one source instance is supported')
    instance_id = instances[0].get('instance_id')
    epochs = instances[0].get('epochs')
    if not is_text(instance_id) or not isinstance(epochs, list) or not epochs:
        raise Refused('fixture: the source instance needs an instance_id and epochs')
    table = {}
    for index, epoch in enumerate(epochs):
        if (not isinstance(epoch, dict) or not is_text(epoch.get('epoch_id')) or epoch['epoch_id'] in table
                or not is_int(epoch.get('counter_start'))):
            raise Refused('fixture: epochs need unique epoch_id values and an integer counter_start')
        # Adapter-only epoch identity convention.
        table[epoch['epoch_id']] = 'did:web:example:agents:' + instance_id + '#e' + str(index + 1)
    if len(set(table.values())) != len(table):
        raise Refused('agent_id table is not injective')
    inverse = {agent: epoch_id for epoch_id, agent in table.items()}
    if any(not isinstance(r.get('epoch_id'), str) or r['epoch_id'] not in table for r in records):
        raise Refused('fixture: a record names an unknown epoch')
    explicit_kind = any('kind' in r for r in records)
    generated, identity, per_epoch, projection = [], [], [], []
    previous = None
    for epoch in epochs:
        epoch_id, start = epoch['epoch_id'], epoch['counter_start']
        rows = sorted((r for r in records if r['epoch_id'] == epoch_id), key=lambda r: r['seq'])
        ae, store, gw = gen.chain(table[epoch_id])
        control = 0
        for row in rows:
            kind = row.get('kind', 'business')
            if kind == 'epoch_link' and previous is not None:
                action = gen.core.Action('source.restart', instance_id, {
                    'previous_epoch_id': previous[0], 'previous_last_seq': previous[1],
                    'previous_chain_head': previous[2]})
                control += 1
            elif kind == 'business' and is_text(row.get('obligation_id')):
                action = gen.core.Action('obligation.record', instance_id, {'obligation_id': row['obligation_id']})
            else:
                raise Refused('fixture record ' + row['record_id'] + ': unsupported kind or missing content')
            claims = gen.submit(ae, store, gw, action)['poc_claims']
            record = {'record_id': row['record_id']}
            if explicit_kind:
                record['kind'] = 'epoch_link' if action.kind == 'source.restart' else 'business'
            record['epoch_id'] = inverse[claims['agent_id']]
            record['seq'] = start + claims['step_index']
            record['time'] = row['time']
            if action.kind == 'source.restart':
                record['previous_epoch_id'] = action.params['previous_epoch_id']
                record['previous_last_seq'] = action.params['previous_last_seq']
            else:
                record['obligation_id'] = action.params['obligation_id']
            generated.append(record)
            identity.append(identity_entry(row['record_id'], claims, epoch_id))
        ok, message = gen.core.Verifier(ae.pk, ae.measurement).verify_chain(store.records)
        per_epoch.append({'epoch_id': epoch_id, 'verified': ok is True, 'message': message})
        projection.append({'epoch_id': epoch_id, 'chain_length': len(store.records), 'control_records': control,
                           'business_records': len(store.records) - control})
        if store.records:
            last = store.records[-1]['poc_claims']
            previous = (epoch_id, start + last['step_index'], last['chain_head'])
    return generated, identity, {'per_epoch': per_epoch, 'projection': projection, 'agent_id_table': table}


def generate_b2(gen, records):
    ae, store, gw = gen.chain(B2_AGENT_ID)
    generated, identity = [], []
    for row in sorted(records, key=lambda r: r['seq']):
        if not is_text(row.get('surface')) or not is_text(row.get('effect_ref')):
            raise Refused('fixture record ' + row['record_id'] + ': needs a surface and an effect_ref')
        action = gen.core.Action('effect.record', row['surface'], {'effect_ref': row['effect_ref']})
        claims = gen.submit(ae, store, gw, action)['poc_claims']
        generated.append({'record_id': row['record_id'], 'seq': claims['step_index'], 'time': row['time'],
                          'surface': action.resource, 'effect_ref': action.params['effect_ref']})
        identity.append(identity_entry(row['record_id'], claims, B2_AGENT_ID))
    ok, message = gen.core.Verifier(ae.pk, ae.measurement).verify_chain(store.records)
    return generated, identity, {'chain': {'verified': ok is True, 'message': message, 'chain_length': len(store.records)},
                                 'agent_id_table': {'chain': B2_AGENT_ID}}


def _value(doc, key):
    return doc[key] if key in doc else ABSENT


def semantic_diff(produced, fixture):
    '''Differences between the generated assessor input and the frozen fixture.
    Records are compared field by field per record_id; other fields are copied.'''
    diffs = []
    for key in sorted(set(produced) | set(fixture)):
        if key != 'records' and _value(produced, key) != _value(fixture, key):
            diffs.append({'path': key, 'generated': _value(produced, key), 'fixture': _value(fixture, key)})
    if len(produced['records']) != len(fixture['records']):
        diffs.append({'path': 'records', 'generated': len(produced['records']), 'fixture': len(fixture['records'])})
    ours = {r['record_id']: r for r in produced['records']}
    theirs = {r['record_id']: r for r in fixture['records']}
    for record_id in sorted(set(ours) | set(theirs)):
        mine, frozen = ours.get(record_id), theirs.get(record_id)
        if mine is None or frozen is None:
            diffs.append({'path': 'records[' + record_id + ']', 'generated': mine, 'fixture': frozen})
            continue
        for name in sorted(set(mine) | set(frozen)):
            if _value(mine, name) != _value(frozen, name):
                diffs.append({'path': 'records[' + record_id + '].' + name,
                              'generated': _value(mine, name), 'fixture': _value(frozen, name)})
    return diffs


def write_new(path, raw):
    with open(path, 'xb') as handle:
        handle.write(raw)


def run(args):
    impl = os.path.abspath(args['--impl'])
    out = os.path.abspath(args['--out'])
    if os.path.lexists(out):
        raise Refused('--out must name a directory that does not exist yet')
    if not os.path.isdir(os.path.dirname(out)):
        raise Refused('the parent of --out must be an existing directory')
    fixture, fixture_digest = load_json(args['--fixture'], 'fixture')
    truth, truth_digest = load_json(args['--truth'], 'truth')
    records = check_fixture(fixture)
    injected, tokens = check_truth(truth, fixture)
    check_withheld(records, injected)
    family = fixture['family']
    pins = check_pins(impl)
    core, key_class = load_reference(impl)
    if check_pins(impl) != pins:
        raise Refused('pinned reference files changed during import')
    if family == 'B1':
        resources = {i.get('instance_id') for i in fixture.get('source_instances') or []
                     if isinstance(i, dict) and is_text(i.get('instance_id'))}
        gen = Generator(core, key_class, resources)
        generated, identity, block = generate_b1(gen, records, fixture)
    else:
        resources = {r['surface'] for r in records if is_text(r.get('surface'))}
        gen = Generator(core, key_class, resources)
        generated, identity, block = generate_b2(gen, records)
    if len({(i['chain'], i['step_index']) for i in identity}) != len(identity):
        raise GenerationError('identity map is not injective')
    produced = copy.deepcopy(fixture)
    produced['records'] = generated
    raw_input = serialize(produced)
    check_leaks(raw_input.decode('utf-8'), tokens)
    input_digest = digest_of(raw_input)
    measured = {
        'schema': MEASURED_SCHEMA,
        'case_id': fixture['case_id'],
        'family': family,
        'input_sha256': input_digest['sha256'],
        'input_bytes': input_digest['bytes'],
        'orchestration_run_id': args['--orchestration-run-id'],
        'producer_run_id': args['--producer-run-id'],
        'reference': {'revision': REFERENCE_REVISION, 'files': pins},
        'fixture': fixture_digest,
        'truth': truth_digest,
        'identity_map': identity,
        'semantic_diff': semantic_diff(produced, fixture),
        'parts': {
            'measured': ['verify_chain result of each full generated chain, control records included',
                         'record sequence positions and epoch-link previous_last_seq from the generated chains'],
            'simulated': ['population evidence', 'observations, segments and completeness evidence',
                          'routes and mediation bindings', 'assumptions',
                          'record times, copied from the fixture by chain position'],
            'declared': ['integrity_inputs, copied unchanged; measured integrity appears only in this file'],
            'not_measured': ['RelyingParty capability checks and dispatch: no RelyingParty is instantiated',
                             'gateway executed=True without a relying party is a release signal, '
                             'not an endpoint execution result'],
        },
        'note': ('produced by the adapter with the reference implementation at the pin; the producer receipt is '
                 'issued by the owning harness; not an independent reproduction'),
    }
    measured.update(block)
    raw_measured = serialize(measured)
    os.mkdir(out, 0o755)
    input_path = os.path.join(out, 'assessor-input.json')
    write_new(input_path, raw_input)
    os.chmod(input_path, 0o444)
    write_new(os.path.join(out, 'measured.json'), raw_measured)
    return {'result': 'produced', 'case_id': fixture['case_id'], 'assessor_input': input_digest,
            'measured': digest_of(raw_measured)}


def main(argv):
    try:
        summary = run(parse_args(argv))
    except Missing as exc:
        print(json.dumps({'result': 'prerequisite_missing', 'error': str(exc)}, sort_keys=True))
        return 3
    except (Refused, OSError) as exc:
        print(json.dumps({'result': 'refused', 'error': exc.__class__.__name__ + ': ' + str(exc)}, sort_keys=True))
        return 2
    except Exception as exc:
        sys.stderr.write('generation or internal error: ' + exc.__class__.__name__ + ': ' + str(exc) + chr(10))
        return 1
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
