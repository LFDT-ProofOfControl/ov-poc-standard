#!/usr/bin/env python3
'''Host-side comparator for the bjorn-implementation candidate, revision I1.

Public-package source derivative; this copy has not been executed.

Usage:
    python3 compare.py --input FILE --expected FILE --outcome FILE
        [--measured FILE] [--receipt FILE]
        [--binding-spec FILE --orchestration-manifest FILE --checker FILE]

Host only. Reads only the named files and its own source (for its code pin)
and writes one JSON report to stdout. See package REPRODUCE.md:
- the input is validated before it bounds dependencies: types, unique ids
  and surfaces, declared references, route_field 'route' only, and real UTC
  instants (impossible values such as minute 99 are rejected);
- expected <= actual <= relevant, with relevant derived from the input only;
- --receipt is the immutable isolated-assessor receipt (input and stdout);
- orchestration links are not re-implemented here. The frozen artifact-
  link checker, accepted only at its exact pinned bytes, recomputes the
  manifest from the binding spec (plan, producer and assessor receipts,
  artifacts and actual code paths). The supplied manifest must equal that
  recomputation exactly, and its digests must name the files this
  comparator received, including this comparator's own version and code;
- an executed comparison is PASS only with verified links, a verified
  receipt and matching outcome and measurements; fixture_only is never PASS.
The host records are trusted local harness records, not cryptographic proof.

Exit codes: 0 for PASS or OUTCOME_PASS_FIXTURE_ONLY; 1 for FAIL or
NOT_PASS_UNBOUND_EXECUTED_RUN; 2 for usage, parse or malformed documents.
'''
import datetime
import hashlib
import json
import os
import re
import sys
import types

COMPARATOR_VERSION = 'bjorn-compare/I1'
REPORT_SCHEMA = 'bjorn-implementation/compare-report/v0'
OUTPUT_SCHEMA = 'bjorn-implementation/assessor-output/v0'
MEASURED_SCHEMA = 'bjorn-implementation/measured/v0'
RECEIPT_CONSTANTS = {'schema_version': 1, 'profile': 's3-bjorn-isolated-python-v1', 'module': 'assessor',
                     'status': 'completed', 'attach_exit_code': 0}
# Artifact-link checker, accepted only at the exact pinned source bytes.
CHECKER_PIN = {'bytes': 12511, 'sha256': 'c445c11409c7137d05f82bbb46540ecc870b22a5fcb1efc65a20bfd625d67d30'}
RULE_IDS = {'R' + str(n) for n in range(1, 15)}
JSON_OPTIONS = ('--input', '--expected', '--outcome', '--measured', '--receipt', '--binding-spec',
                '--orchestration-manifest')
OPTIONS = JSON_OPTIONS + ('--checker',)
REQUIRED = ('--input', '--expected', '--outcome')
LINK_OPTIONS = ('--binding-spec', '--orchestration-manifest', '--checker')
HEX_RE = re.compile('[0-9a-f]{64}')
INSTANT_RE = re.compile(r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})Z')
# Same documented v0 vocabulary value as assessor_common.EXHAUSTIVE_V0_STATEMENTS
# Repeated here so that the host comparator imports no
# assessor code. Exact whole-string equality only.
EXHAUSTIVE_V0 = (
    {
        'surface': 'alt-db',
        'mediated_routes': ['svc-rp-db'],
        'statement': ('an effect on alt-db whose route is svc-rp-db was executed by rp-db only '
                      'after a capability bound to exactly one gateway record was verified; '
                      'any other route value is not a mediated route'),
    },
)
POSITIVE = {('no_bypass', 'supported'), ('bypass_occurred', 'not_supported')}
WITNESSED = {('no_bypass', 'not_supported'), ('bypass_occurred', 'supported')}


class UsageError(Exception):
    pass


class DocumentError(Exception):
    '''A supplied document is malformed for comparison.'''


def _unique_pairs(pairs):
    seen = {}
    for key, value in pairs:
        if key in seen:
            raise ValueError('duplicate JSON key ' + key)
        seen[key] = value
    return seen


def _reject_constant(name):
    raise ValueError('non-finite JSON number ' + name)


def _finite_float(text):
    value = float(text)
    if value != value or value in (float('inf'), float('-inf')):
        raise ValueError('JSON number ' + text[:40] + ' is not finite as a float')
    return value


def digest_of(raw):
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def load(path):
    with open(path, 'rb') as handle:
        raw = handle.read()
    doc = json.loads(raw.decode('utf-8'), object_pairs_hook=_unique_pairs, parse_constant=_reject_constant,
                     parse_float=_finite_float)
    return doc, digest_of(raw)


def own_digest():
    with open(os.path.abspath(__file__), 'rb') as handle:
        return digest_of(handle.read())


def parse_args(argv):
    if len(argv) % 2:
        raise UsageError('options must come in --name value pairs')
    args = {}
    for name, value in zip(argv[0::2], argv[1::2]):
        if name not in OPTIONS or name in args or not value:
            raise UsageError('unknown, repeated or empty option ' + name)
        args[name] = value
    for name in REQUIRED:
        if name not in args:
            raise UsageError('missing required option ' + name)
    return args


def _obj(value):
    return value if isinstance(value, dict) else {}


def _list(value):
    return value if isinstance(value, list) else []


def _second(value):
    '''The assessor-input form: exactly YYYY-MM-DDTHH:MM:SSZ and a real UTC instant.'''
    match = INSTANT_RE.fullmatch(value) if isinstance(value, str) else None
    if match is None:
        return None
    try:
        return datetime.datetime.strptime(match.group(1), '%Y-%m-%dT%H:%M:%S')
    except ValueError:
        return None


def _in(moment, iv):
    iv = _obj(iv)
    m, s, e = _second(moment), _second(iv.get('start')), _second(iv.get('end'))
    return None not in (m, s, e) and s <= m < e


def _is_digest(block):
    return (isinstance(block, dict) and type(block.get('bytes')) is int and block['bytes'] >= 0
            and isinstance(block.get('sha256'), str) and HEX_RE.fullmatch(block['sha256']) is not None)


def _same(block, digest):
    return (digest is not None and _is_digest(block) and block['bytes'] == digest['bytes']
            and block['sha256'] == digest['sha256'])


def _ids(value, where):
    if (not isinstance(value, list) or not all(isinstance(v, str) and v for v in value)
            or len(set(value)) != len(value)):
        raise DocumentError(where + ': must be a list of unique non-empty string ids')
    return list(value)


def _by_surface(items, where):
    if not isinstance(items, list):
        raise DocumentError(where + ': must be a list')
    out = {}
    for index, item in enumerate(items):
        place = where + '[' + str(index) + ']'
        if not isinstance(item, dict) or not isinstance(item.get('surface'), str) or not item['surface']:
            raise DocumentError(place + ': must be an object with a non-empty string surface')
        if item['surface'] in out:
            raise DocumentError(place + ': surface ' + item['surface'] + ' appears twice')
        out[item['surface']] = item
    return out


class Source:
    '''The assessor input, validated as the only authority for dependency bounds.'''

    def __init__(self, inp):
        if not isinstance(inp, dict):
            raise DocumentError('input: must be a JSON object')
        for name in ('case_id', 'family'):
            if not isinstance(inp.get(name), str) or not inp[name]:
                raise DocumentError('input.' + name + ': must be a non-empty string')
        if inp['family'] not in ('B1', 'B2'):
            raise DocumentError('input.family: must be B1 or B2')
        self.family = inp['family']
        assumptions = inp.get('assumptions')
        if not isinstance(assumptions, list) or not all(isinstance(a, dict) for a in assumptions):
            raise DocumentError('input.assumptions: must be a list of objects')
        self.declared = _ids([a.get('id') for a in assumptions], 'input.assumptions ids')
        self.population, self.observations, self.bindings = [], {}, {}
        if self.family == 'B1':
            basis = inp.get('population_evidence')
            if not isinstance(basis, dict):
                raise DocumentError('input.population_evidence: must be an object')
            if basis.get('kind') == 'independent_population_evidence':
                self.population = self.refs(basis.get('assumptions'), 'input.population_evidence.assumptions')
            return
        self.observations = _by_surface(inp.get('observations'), 'input.observations')
        self.bindings = _by_surface(inp.get('mediation_evidence'), 'input.mediation_evidence')
        for surface, obs in sorted(self.observations.items()):
            where = 'input.observations[' + surface + ']'
            self.refs(obs.get('assumptions'), where + '.assumptions')
            effects = obs.get('observed_effects')
            if not isinstance(effects, list) or not all(isinstance(e, dict) for e in effects):
                raise DocumentError(where + '.observed_effects: must be a list of objects')
            for effect in effects:
                if _second(effect.get('time')) is None:
                    raise DocumentError(where + '.observed_effects: time must be a real UTC instant YYYY-MM-DDTHH:MM:SSZ')
                if 'route' in effect and (not isinstance(effect['route'], str) or not effect['route']):
                    raise DocumentError(where + '.observed_effects: route must be a non-empty string')
        for surface, binding in sorted(self.bindings.items()):
            where = 'input.mediation_evidence[' + surface + ']'
            self.refs(binding.get('assumptions'), where + '.assumptions')
            _ids(binding.get('mediated_routes'), where + '.mediated_routes')
            if not isinstance(binding.get('statement'), str):
                raise DocumentError(where + '.statement: must be a string')
            # Same supported schema as assessor_b2: witnesses are read only from
            # the effect field named route.
            if binding.get('route_field') != 'route':
                raise DocumentError(where + '.route_field: only route is supported')

    def refs(self, value, where):
        ids = _ids(value, where)
        undeclared = [i for i in ids if i not in self.declared]
        if undeclared:
            raise DocumentError(where + ': undeclared assumption ' + ', '.join(undeclared))
        return ids

    def exhaustive(self, surface):
        binding = self.bindings.get(surface)
        if binding is None:
            return False
        for entry in EXHAUSTIVE_V0:
            if binding['statement'] == entry['statement']:
                return binding['surface'] == entry['surface'] and binding['mediated_routes'] == entry['mediated_routes']
        return False

    def witnesses(self, surfaces, iv):
        '''Surfaces whose observation shows an in-scope effect with an unlisted route
        under a v0-exhaustive binding, taken from the input only.'''
        found = []
        for surface in surfaces:
            if not self.exhaustive(surface):
                continue
            routes = self.bindings[surface]['mediated_routes']
            for effect in self.observations.get(surface, {}).get('observed_effects', []):
                route = effect.get('route')
                if route is not None and route not in routes and _in(effect.get('time'), iv):
                    found.append(surface)
                    break
        return found

    def surface_deps(self, surfaces):
        ids = []
        for surface in surfaces:
            for source in (self.observations.get(surface), self.bindings.get(surface)):
                if source is not None:
                    ids.extend(i for i in source['assumptions'] if i not in ids)
        return ids


class Report:
    def __init__(self):
        self.mismatches = []
        self.additional = []

    def mismatch(self, path, expected, actual):
        self.mismatches.append({'path': path, 'expected': expected, 'actual': actual})


def scope_key(scope):
    scope = _obj(scope)
    iv = _obj(scope.get('interval'))
    if 'surfaces' in scope:
        who = 'surfaces:' + ','.join(sorted(str(s) for s in _list(scope['surfaces'])))
    else:
        who = 'instance:' + str(scope.get('instance_id'))
    return who + '|' + str(iv.get('start')) + '|' + str(iv.get('end'))


def id_list(value):
    return isinstance(value, list) and all(isinstance(v, str) for v in value) and len(set(value)) == len(value)


def valid_rules(rules, allow_empty):
    return (isinstance(rules, list) and (allow_empty or bool(rules))
            and all(isinstance(r, str) and r in RULE_IDS for r in rules))


def check_deps(rep, path, expected, actual, relevant, declared, empty_required):
    if not id_list(expected) or not id_list(actual):
        rep.mismatch(path, expected, actual)
        return
    exp, act, rel = set(expected), set(actual), set(relevant)
    if empty_required:
        if exp or act:
            rep.mismatch(path + ' (not_established requires no dependencies)', expected, actual)
        return
    if exp - act:
        rep.mismatch(path + ' (omitted expected dependency)', sorted(exp - act), actual)
    if act - declared:
        rep.mismatch(path + ' (undeclared dependency)', [], sorted(act - declared))
    if (act & declared) - rel:
        rep.mismatch(path + ' (unrelated dependency)', sorted(rel), sorted((act & declared) - rel))
    extra = sorted((act - exp) & rel)
    if extra:
        rep.additional.append({'path': path, 'ids': extra, 'note': 'permitted conservative dependency, not exact equality'})


def relevant_for(rep, path, src, claim, status, scope):
    if claim == 'coverage_complete':
        return src.population
    scope = _obj(scope)
    surfaces = scope.get('surfaces')
    if not isinstance(surfaces, list) or not all(isinstance(s, str) for s in surfaces):
        return []
    if (claim, status) in POSITIVE:
        return src.surface_deps(surfaces)
    if (claim, status) in WITNESSED:
        witnesses = src.witnesses(surfaces, scope.get('interval'))
        if not witnesses:
            rep.mismatch(path + ' (the input shows no in-scope non-mediated effect for this result)', 'input witness', None)
        return src.surface_deps(witnesses)
    return []


def keyed_results(rep, path, results):
    out = {}
    if not isinstance(results, list):
        rep.mismatch(path, 'list', results)
        return out
    for item in results:
        if not isinstance(item, dict):
            rep.mismatch(path + ' (entry is not an object)', 'object', item)
            continue
        key = str(item.get('claim')) + '@' + scope_key(item.get('scope'))
        if key in out:
            rep.mismatch(path + ' duplicate ' + key, None, item)
        out[key] = item
    return out


def compare_results(rep, src, expected, outcome, field, declared):
    exp = keyed_results(rep, 'expected.' + field, expected.get(field, []))
    act = keyed_results(rep, 'outcome.' + field, outcome.get(field, []))
    for key in sorted(set(exp) | set(act)):
        path = field + '[' + key + ']'
        if key not in act:
            rep.mismatch(path, 'present', 'missing')
            continue
        if key not in exp:
            rep.mismatch(path, 'absent', 'extra result')
            continue
        e, a = exp[key], act[key]
        for name in ('status', 'polarity'):
            if e.get(name) != a.get(name):
                rep.mismatch(path + '.' + name, e.get(name), a.get(name))
        if not valid_rules(a.get('rules'), False):
            rep.mismatch(path + '.rules (invalid citation)', 'R1-R14', a.get('rules'))
        status = e.get('status')
        relevant = relevant_for(rep, path, src, e.get('claim'), status, e.get('scope'))
        check_deps(rep, path + '.conditional_on', e.get('conditional_on'), a.get('conditional_on'),
                   relevant, declared, status == 'not_established')


def finding_key(item):
    item = _obj(item)
    return '|'.join(str(item.get(k, '')) for k in ('type', 'obligation_id', 'effect_id', 'surface', 'time', 'due'))


def unestablished_key(item):
    item = _obj(item)
    claims = sorted(str(c) for c in _list(item.get('affected_claims')))
    return scope_key(item.get('scope')) + '|' + ','.join(claims)


def span_key(item):
    item = _obj(item)
    return str(item.get('start')) + '|' + str(item.get('end'))


def compare_sets(rep, path, expected, actual, key):
    e = sorted(key(x) for x in expected) if isinstance(expected, list) else None
    a = sorted(key(x) for x in actual) if isinstance(actual, list) else None
    if e != a:
        rep.mismatch(path, e, a)


def surface_map(rep, path, items):
    out = {}
    for item in _list(items):
        key = str(_obj(item).get('surface'))
        if key in out:
            rep.mismatch(path + ' duplicate surface ' + key, None, item)
        out[key] = _obj(item)
    return out


def epoch_pairs(integrity):
    return sorted((str(_obj(p).get('epoch_id')), str(_obj(p).get('status'))) for p in _list(_obj(integrity).get('per_epoch')))


def compare_b1(rep, src, expected, outcome, declared):
    e_int, a_int = epoch_pairs(expected.get('integrity')), epoch_pairs(outcome.get('integrity'))
    if e_int != a_int:
        rep.mismatch('integrity.per_epoch', e_int, a_int)
    e_cross, a_cross = _obj(expected.get('cross_epoch')), _obj(outcome.get('cross_epoch'))
    for name in ('discontinuity', 'from_epoch', 'to_epoch', 'link', 'link_record_id'):
        if e_cross.get(name) != a_cross.get(name):
            rep.mismatch('cross_epoch.' + name, e_cross.get(name), a_cross.get(name))
    e_basis, a_basis = _obj(expected.get('basis_assessment')), _obj(outcome.get('basis_assessment'))
    for name in ('kind', 'status', 'evidence_id', 'covers'):
        if e_basis.get(name) != a_basis.get(name):
            rep.mismatch('basis_assessment.' + name, e_basis.get(name), a_basis.get(name))
    if 'conditional_on' in e_basis or 'conditional_on' in a_basis:
        check_deps(rep, 'basis_assessment.conditional_on', e_basis.get('conditional_on', []),
                   a_basis.get('conditional_on', []), src.population, declared, False)
    e_rec, a_rec = expected.get('reconciliation'), outcome.get('reconciliation')
    if (e_rec is None) != (a_rec is None):
        rep.mismatch('reconciliation', e_rec, a_rec)
    elif e_rec is not None:
        e_rec, a_rec = _obj(e_rec), _obj(a_rec)
        if scope_key(e_rec.get('scope')) != scope_key(a_rec.get('scope')):
            rep.mismatch('reconciliation.scope', e_rec.get('scope'), a_rec.get('scope'))
        compare_sets(rep, 'reconciliation.matched', e_rec.get('matched'), a_rec.get('matched'),
                     lambda m: str(_obj(m).get('obligation_id')) + '|' + str(_obj(m).get('record_id')))
        compare_sets(rep, 'reconciliation.missing', e_rec.get('missing'), a_rec.get('missing'), str)


def compare_b2(rep, expected, outcome):
    e_int, a_int = _obj(expected.get('integrity')), _obj(outcome.get('integrity'))
    for name in ('status', 'visible_log'):
        if e_int.get(name) != a_int.get(name):
            rep.mismatch('integrity.' + name, e_int.get(name), a_int.get(name))
    e_obs = surface_map(rep, 'expected.observation_assessment', expected.get('observation_assessment'))
    a_obs = surface_map(rep, 'outcome.observation_assessment', outcome.get('observation_assessment'))
    if sorted(e_obs) != sorted(a_obs):
        rep.mismatch('observation_assessment.surfaces', sorted(e_obs), sorted(a_obs))
    for surface in sorted(set(e_obs) & set(a_obs)):
        compare_sets(rep, 'observation_assessment[' + surface + '].adequate', e_obs[surface].get('adequate'),
                     a_obs[surface].get('adequate'), span_key)
        compare_sets(rep, 'observation_assessment[' + surface + '].inadequate', e_obs[surface].get('inadequate'),
                     a_obs[surface].get('inadequate'), lambda i: span_key(i) + '|' + str(_obj(i).get('reason')))
    e_med = surface_map(rep, 'expected.mediation_assessment', expected.get('mediation_assessment'))
    a_med = surface_map(rep, 'outcome.mediation_assessment', outcome.get('mediation_assessment'))
    if sorted(e_med) != sorted(a_med):
        rep.mismatch('mediation_assessment.surfaces', sorted(e_med), sorted(a_med))
    for surface in sorted(set(e_med) & set(a_med)):
        for name in ('status', 'evidence_id'):
            if e_med[surface].get(name) != a_med[surface].get(name):
                rep.mismatch('mediation_assessment[' + surface + '].' + name, e_med[surface].get(name), a_med[surface].get(name))


def compare_outcome(rep, src, expected, outcome):
    if outcome.get('schema') != OUTPUT_SCHEMA or outcome.get('result') != 'assessed':
        rep.mismatch('result', 'assessed', outcome.get('result'))
        return
    source = _obj(outcome.get('integrity')).get('source')
    if source != 'declared_input':
        rep.mismatch('integrity.source', 'declared_input', source)
    declared = set(src.declared)
    if src.family == 'B1':
        compare_b1(rep, src, expected, outcome, declared)
    else:
        compare_b2(rep, expected, outcome)
    compare_sets(rep, 'findings', expected.get('findings'), outcome.get('findings'), finding_key)
    for item in _list(outcome.get('findings')):
        if not valid_rules(_obj(item).get('rules'), True):
            rep.mismatch('findings.rules (invalid citation)', 'R1-R14', _obj(item).get('rules'))
    compare_results(rep, src, expected, outcome, 'claim_results', declared)
    compare_results(rep, src, expected, outcome, 'scoped_results', declared)
    compare_sets(rep, 'unestablished', expected.get('unestablished'), outcome.get('unestablished'), unestablished_key)


def compare_measured(src, inp, input_digest, measured):
    problems = []
    if measured.get('schema') != MEASURED_SCHEMA:
        problems.append('measured schema is not ' + MEASURED_SCHEMA)
    if measured.get('input_sha256') != input_digest['sha256']:
        problems.append('measured.input_sha256 does not name the supplied assessor input')
    integrity = _obj(inp.get('integrity_inputs'))
    if src.family == 'B1':
        declared = {p['epoch_id']: p.get('chain') for p in _list(integrity.get('per_epoch'))
                    if isinstance(p, dict) and isinstance(p.get('epoch_id'), str)}
        measured_epochs = {p['epoch_id']: p for p in _list(measured.get('per_epoch'))
                           if isinstance(p, dict) and isinstance(p.get('epoch_id'), str)}
        if sorted(declared) != sorted(measured_epochs):
            problems.append('measured epochs differ from declared epochs')
        for epoch_id in sorted(set(declared) & set(measured_epochs)):
            if (declared[epoch_id] == 'verified') != (measured_epochs[epoch_id].get('verified') is True):
                problems.append(epoch_id + ': measured chain result differs from the declaration')
    elif (integrity.get('chain') == 'verified') != (_obj(measured.get('chain')).get('verified') is True):
        problems.append('measured chain result differs from the declaration')
    if measured.get('semantic_diff') != []:
        problems.append('generated input differs semantically from the frozen fixture')
    return problems


def check_receipt(receipt, input_digest, outcome_digest):
    '''The immutable isolated-assessor receipt: constants and exact input/stdout digests.
    Orchestration links, container state, captured stdout bytes, single start and
    cleanup are verified by the pinned checker in check_orchestration.'''
    problems = []
    for name, value in RECEIPT_CONSTANTS.items():
        if receipt.get(name) != value or type(receipt.get(name)) is not type(value):
            problems.append('receipt.' + name + ' is not ' + str(value))
    for name, digest in (('input', input_digest), ('stdout', outcome_digest)):
        if not _same(receipt.get(name), digest):
            problems.append('receipt.' + name + ' digest does not match the supplied file')
    return problems


def load_checker(path):
    '''Load the artifact-link checker from exactly the pinned bytes.'''
    with open(path, 'rb') as handle:
        raw = handle.read()
    if digest_of(raw) != CHECKER_PIN:
        raise DocumentError('checker bytes differ from the frozen S3 checker pin')
    module = types.ModuleType('bjorn_s3_checker')
    module.__file__ = os.path.abspath(path)
    exec(compile(raw, module.__file__, 'exec'), module.__dict__)
    return module


def check_orchestration(mode, spec, manifest, checker_path, digests, own):
    '''Recompute the artifact-link manifest with the pinned checker from the
    binding spec, require the supplied manifest to equal it exactly,
    and bind every digest to the files this comparator received. A status string
    is never sufficient. Trusted local harness records, not cryptographic proof.'''
    try:
        recomputed = load_checker(checker_path).check_orchestration(spec)
    except Exception as exc:  # any checker refusal fails closed as unverified links
        return None, ['artifact links not verified: ' + exc.__class__.__name__ + ': ' + str(exc)]
    problems = []

    def need(ok, message):
        if not ok:
            problems.append(message)

    pins = _obj(recomputed.get('pins'))
    comparator = _obj(pins.get('comparator'))
    need(manifest == recomputed, 'supplied manifest differs from the manifest recomputed from the binding spec')
    need(recomputed.get('checker') == CHECKER_PIN, 'manifest was not produced by the pinned checker bytes')
    need(recomputed.get('mode') == mode, 'planned mode differs from the comparison mode ' + mode)
    need(comparator.get('version') == COMPARATOR_VERSION and _same(comparator, own),
         'planned comparator pin is not this comparator version and code')
    need(_same(pins.get('expected'), digests.get('--expected')), 'planned expected pin differs from the supplied expected file')
    for key, option in (('input', '--input'), ('outcome', '--outcome'), ('assessor_receipt', '--receipt')):
        need(_same(recomputed.get(key), digests.get(option)), 'manifest ' + key + ' differs from the supplied ' + option[2:] + ' file')
    if mode == 'executed':
        need(_same(recomputed.get('measured'), digests.get('--measured')), 'manifest measured differs from the supplied measured file')
        need(recomputed.get('measurement_status') == 'PRODUCER_ARTIFACT_BOUND', 'manifest does not bind a producer artifact')
    else:
        need(recomputed.get('measured') is None and recomputed.get('measurement_status') == 'NOT_RUN',
             'fixture_only manifest must carry no measurement')
    return recomputed.get('comparison_run_id'), problems


def run(argv):
    args = parse_args(argv)
    docs, digests = {}, {}
    for option in JSON_OPTIONS:
        if option in args:
            docs[option], digests[option] = load(args[option])
    inp = docs['--input']
    src = Source(inp)
    for option, doc in docs.items():
        if not isinstance(doc, dict):
            raise DocumentError(option[2:] + ': must be a JSON object')
    expected, outcome = docs['--expected'], docs['--outcome']
    measured, receipt = docs.get('--measured'), docs.get('--receipt')
    own = own_digest()
    rep = Report()
    for name, doc in (('expected', expected), ('outcome', outcome), ('measured', measured)):
        if doc is None:
            continue
        if name == 'outcome' and doc.get('result') == 'input_rejected':
            continue
        for field in ('case_id', 'family'):
            if doc.get(field) != inp.get(field):
                rep.mismatch(name + '.' + field + ' (correspondence)', inp.get(field), doc.get(field))
    if not rep.mismatches:
        compare_outcome(rep, src, expected, outcome)
    outcome_match = not rep.mismatches
    inp_d, out_d = digests['--input'], digests['--outcome']
    binding_problems = check_receipt(receipt, inp_d, out_d) if receipt is not None else []
    binding = 'not_verified' if receipt is None else ('verified' if not binding_problems else 'mismatch')
    mode = 'fixture_only' if measured is None else 'executed'
    if measured is None:
        measurement_match, measurement_problems = None, []
    else:
        measurement_problems = compare_measured(src, inp, inp_d, measured)
        measurement_match = not measurement_problems
    comparison_run_id = None
    supplied = [option for option in LINK_OPTIONS if option in args]
    if not supplied:
        orchestration, orchestration_problems = 'not_supplied', []
    elif len(supplied) != len(LINK_OPTIONS) or receipt is None:
        orchestration = 'mismatch'
        orchestration_problems = ['--binding-spec, --orchestration-manifest, --checker and --receipt must be supplied together']
    else:
        comparison_run_id, orchestration_problems = check_orchestration(
            mode, docs['--binding-spec'], docs['--orchestration-manifest'], args['--checker'], digests, own)
        orchestration = 'mismatch' if orchestration_problems else 'verified'
    if not outcome_match or 'mismatch' in (binding, orchestration) or measurement_match is False:
        overall = 'FAIL'
    elif mode == 'fixture_only':
        overall = 'OUTCOME_PASS_FIXTURE_ONLY'
    elif binding == 'verified' and orchestration == 'verified':
        overall = 'PASS'
    else:
        overall = 'NOT_PASS_UNBOUND_EXECUTED_RUN'
    return {
        'schema': REPORT_SCHEMA,
        'comparator': {'version': COMPARATOR_VERSION, 'code': own},
        'checker_pin': CHECKER_PIN if supplied else None,
        'case_id': inp.get('case_id'),
        'comparison_run_id': comparison_run_id,
        'run_mode': mode,
        'run_binding': binding,
        'run_binding_problems': binding_problems,
        'orchestration': orchestration,
        'orchestration_problems': orchestration_problems,
        'digests': {option[2:]: digest for option, digest in digests.items()},
        'outcome_match': outcome_match,
        'mismatches': rep.mismatches,
        'additional_dependencies': rep.additional,
        'measurement_match': measurement_match,
        'measurement_status': 'NOT_RUN' if measured is None else ('MATCH' if measurement_match else 'MISMATCH'),
        'measurement_problems': measurement_problems,
        'overall': overall,
        'note': ('structural comparison of one assessor outcome; host records are trusted local harness records, '
                 'not cryptographic proof; not independent reproduction'),
    }


def main(argv):
    try:
        report = run(argv)
    except (UsageError, DocumentError, OSError, ValueError, UnicodeDecodeError, AttributeError, TypeError, KeyError,
            RecursionError) as exc:
        print(json.dumps({'schema': REPORT_SCHEMA, 'overall': 'ERROR', 'error': exc.__class__.__name__ + ': ' + str(exc)}, sort_keys=True))
        return 2
    print(json.dumps(report, sort_keys=True, indent=2))
    return 0 if report['overall'] in ('PASS', 'OUTCOME_PASS_FIXTURE_ONLY') else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
