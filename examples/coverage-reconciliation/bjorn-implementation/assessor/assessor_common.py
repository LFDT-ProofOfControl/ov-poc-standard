'''Shared helpers for the bjorn-implementation assessor, revision I1.

Public-package source derivative; this copy has not been executed.

Standard library only. Nothing in this module touches files, the network, the
environment, the clock or subprocesses. Every input problem is raised as
InputRejected; ambiguity is rejected rather than resolved.
'''
import datetime

INPUT_SCHEMA = 'bjorn-vectors/assessor-input/v0'
INPUT_STATUS = 'DESIGN CANDIDATE / PROPOSED, NOT EXECUTED'
OUTPUT_SCHEMA = 'bjorn-implementation/assessor-output/v0'
FAMILY_KIND = {'B1': 'coverage_complete', 'B2': 'no_bypass'}
# Fixed vocabulary in package bjorn-vectors/rules.json (claim_polarity); not taken
# from any expected-outcome file.
POLARITY = {
    'no_bypass': 'every effect on a required surface in the scope took a mediated route',
    'bypass_occurred': 'at least one effect on a required surface in the scope took a non-mediated route',
}
# Deliberately narrow frozen-format compatibility rule; see package bjorn-vectors/rules.json.
# A binding is exhaustive only if its statement is
# exactly one of these documented v0 vocabulary values and its surface and
# mediated_routes agree. This is not a natural-language policy evaluator.
EXHAUSTIVE_V0_STATEMENTS = (
    {
        'surface': 'alt-db',
        'mediated_routes': ['svc-rp-db'],
        'statement': ('an effect on alt-db whose route is svc-rp-db was executed by rp-db only '
                      'after a capability bound to exactly one gateway record was verified; '
                      'any other route value is not a mediated route'),
    },
)
TOP_LEVEL_KEYS = {
    'B1': {'schema', 'status', 'case_id', 'family', 'claim', 'integrity_inputs', 'records',
           'assumptions', 'source_instances', 'population_evidence'},
    'B2': {'schema', 'status', 'case_id', 'family', 'claim', 'integrity_inputs', 'records',
           'assumptions', 'observations', 'mediation_evidence'},
}
TIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'


class InputRejected(Exception):
    def __init__(self, errors):
        Exception.__init__(self, '; '.join(errors))
        self.errors = list(errors)


class Errors:
    def __init__(self):
        self.items = []

    def add(self, message):
        self.items.append(message)

    def check(self):
        if self.items:
            raise InputRejected(self.items)


def is_int(value):
    return isinstance(value, int) and not isinstance(value, bool)


def is_text(value):
    return isinstance(value, str) and value != ''


def duplicates(values):
    seen, repeated = set(), set()
    for value in values:
        if value in seen:
            repeated.add(value)
        seen.add(value)
    return sorted(repeated)


def ts(value, where='time'):
    if not isinstance(value, str) or len(value) != 20 or value[10] != 'T' or not value.endswith('Z'):
        raise InputRejected([where + ': timestamp must have the form YYYY-MM-DDTHH:MM:SSZ'])
    try:
        return datetime.datetime.strptime(value, TIME_FORMAT)
    except ValueError:
        raise InputRejected([where + ': invalid timestamp ' + value])


def interval(obj, where):
    if not isinstance(obj, dict) or set(obj) != {'start', 'end'}:
        raise InputRejected([where + ': an interval must have exactly start and end'])
    if ts(obj['start'], where + '.start') >= ts(obj['end'], where + '.end'):
        raise InputRejected([where + ': start must be before end'])
    return {'start': obj['start'], 'end': obj['end']}


def within(inner, outer):
    return ts(outer['start']) <= ts(inner['start']) and ts(inner['end']) <= ts(outer['end'])


def overlaps(a, b):
    return ts(a['start']) < ts(b['end']) and ts(b['start']) < ts(a['end'])


def contains(span, moment):
    return ts(span['start']) <= ts(moment) < ts(span['end'])


def field(obj, key, kind, where):
    if not isinstance(obj, dict) or key not in obj:
        raise InputRejected([where + ': missing ' + key])
    value = obj[key]
    if kind == 'int':
        ok = is_int(value)
    elif kind == 'text':
        ok = is_text(value)
    else:
        ok = isinstance(value, kind)
    if not ok:
        raise InputRejected([where + '.' + key + ': wrong type'])
    return value


def check_refs(ids, declared, where, errs):
    if not isinstance(ids, list) or not all(isinstance(item, str) for item in ids):
        errs.add(where + ': assumption references must be a list of ids')
        return
    for item in ids:
        if item not in declared:
            errs.add(where + ': undeclared assumption ' + item)
    for item in duplicates(ids):
        errs.add(where + ': assumption ' + item + ' referenced twice')


def ordered(ids, declared):
    '''Return the given assumption ids in declaration order, without repeats.'''
    wanted = set(ids)
    return [item for item in declared if item in wanted]


def binding_exhaustive(binding, where):
    '''Apply the v0 exhaustiveness compatibility rule to one validated binding.

    Exact whole-string equality only. A matching statement with a contradictory
    surface or route list is rejected; any other statement is non-exhaustive.
    '''
    statement = binding.get('statement')
    for entry in EXHAUSTIVE_V0_STATEMENTS:
        if statement == entry['statement']:
            if binding.get('surface') != entry['surface'] or binding.get('mediated_routes') != entry['mediated_routes']:
                raise InputRejected([where + ': allowlisted exhaustive statement contradicts the binding surface or routes'])
            return True
    return False


def validate_common(doc):
    '''Validate fields shared by both families; return declared assumption ids in order.'''
    if not isinstance(doc, dict):
        raise InputRejected(['input must be a JSON object'])
    errs = Errors()
    if doc.get('schema') != INPUT_SCHEMA:
        errs.add('schema: unexpected value')
    if doc.get('status') != INPUT_STATUS:
        errs.add('status: unexpected value')
    if not is_text(doc.get('case_id')):
        errs.add('case_id: must be a non-empty string')
    family = doc.get('family')
    # Type guard before membership: a list or
    # object family must yield input_rejected, not a TypeError.
    if not isinstance(family, str) or family not in FAMILY_KIND:
        errs.add('family: must be the string B1 or B2')
    errs.check()
    for key in sorted(set(doc) - TOP_LEVEL_KEYS[family]):
        errs.add('unexpected top-level field ' + key)
    for key in sorted(TOP_LEVEL_KEYS[family] - set(doc)):
        errs.add('missing top-level field ' + key)
    errs.check()
    claim = field(doc, 'claim', dict, 'input')
    if set(claim) != {'kind', 'polarity', 'scope', 'cutoff'}:
        errs.add('claim: must have exactly kind, polarity, scope and cutoff')
    if claim.get('kind') != FAMILY_KIND[family]:
        errs.add('claim.kind does not agree with family')
    if not is_text(claim.get('polarity')):
        errs.add('claim.polarity: must be a non-empty string')
    scope = field(claim, 'scope', dict, 'claim')
    interval(scope.get('interval'), 'claim.scope.interval')
    ts(claim.get('cutoff'), 'claim.cutoff')
    records = field(doc, 'records', list, 'input')
    if not records:
        errs.add('records: must not be empty')
    for index, record in enumerate(records):
        where = 'records[' + str(index) + ']'
        field(record, 'record_id', 'text', where)
        field(record, 'seq', 'int', where)
        ts(record.get('time'), where + '.time')
    for item in duplicates(r['record_id'] for r in records):
        errs.add('duplicate record_id ' + item)
    assumptions = field(doc, 'assumptions', list, 'input')
    for index, item in enumerate(assumptions):
        where = 'assumptions[' + str(index) + ']'
        if not isinstance(item, dict) or set(item) != {'id', 'text', 'status'}:
            raise InputRejected([where + ': must have exactly id, text and status'])
        field(item, 'id', 'text', where)
        field(item, 'text', 'text', where)
        if item['status'] != 'declared_not_verified':
            errs.add(where + ': status must be declared_not_verified')
    declared = [item['id'] for item in assumptions]
    for item in duplicates(declared):
        errs.add('duplicate assumption id ' + item)
    integrity = field(doc, 'integrity_inputs', dict, 'input')
    field(integrity, 'provenance', 'text', 'integrity_inputs')
    errs.check()
    return declared


def result(claim, polarity, scope, status, rules, evidence, conditional_on):
    return {
        'claim': claim,
        'polarity': polarity,
        'scope': scope,
        'status': status,
        'rules': list(rules),
        'evidence': list(evidence),
        'conditional_on': list(conditional_on) if status != 'not_established' else [],
    }
