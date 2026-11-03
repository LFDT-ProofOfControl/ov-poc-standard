'''B1 family logic of the bjorn-implementation assessor, revision I1.

Public-package source derivative; this copy has not been executed.

Implements rules R1-R7 and R14 in package bjorn-vectors/rules.json.
Standard library only; no file, network, environment, clock or
subprocess access. All results are derived from evidence fields of the input;
case_id and evidence identifiers are only echoed. Every inconsistency in the
input raises InputRejected.

Validation and reconciliation details:
- type guards come before set membership on record kind and population
  evidence kind;
- epoch_link_evidence with other than two epochs is rejected before any
  one-epoch shortcut, so an unresolved link reference is never accepted
 ;
- when population evidence covers a span wider than the claim interval,
  reconciliation is projected to the claim interval: only obligations due
  inside it and only business records timed inside it count (R4).
'''
import assessor_common as common

KINDS = {'business', 'epoch_link'}
BASIS_KINDS = ('none', 'epoch_link_evidence', 'independent_population_evidence')


def _kind(record):
    return record.get('kind', 'business')


def _minus(outer, inner):
    pieces = []
    if common.ts(outer['start']) < common.ts(inner['start']):
        pieces.append({'start': outer['start'], 'end': inner['start']})
    if common.ts(inner['end']) < common.ts(outer['end']):
        pieces.append({'start': inner['end'], 'end': outer['end']})
    return pieces


def _instance_and_epochs(doc, instance_id):
    instances = common.field(doc, 'source_instances', list, 'input')
    if len(instances) != 1:
        raise common.InputRejected(['source_instances: this implementation supports exactly one source instance'])
    instance = instances[0]
    if common.field(instance, 'instance_id', 'text', 'source_instances[0]') != instance_id:
        raise common.InputRejected(['source_instances[0]: instance_id differs from the claim scope'])
    epochs = common.field(instance, 'epochs', list, 'source_instances[0]')
    if not epochs or len(epochs) > 2:
        raise common.InputRejected(['epochs: this implementation supports one or two epochs'])
    for index, epoch in enumerate(epochs):
        where = 'epochs[' + str(index) + ']'
        common.field(epoch, 'epoch_id', 'text', where)
        common.field(epoch, 'counter_start', 'int', where)
        common.ts(epoch.get('declared_start'), where + '.declared_start')
    for item in common.duplicates(e['epoch_id'] for e in epochs):
        raise common.InputRejected(['duplicate epoch_id ' + item])
    return epochs


def _chains(doc, epochs):
    records = doc['records']
    ids = [e['epoch_id'] for e in epochs]
    errs = common.Errors()
    for index, record in enumerate(records):
        where = 'records[' + str(index) + ']'
        if record.get('epoch_id') not in ids:
            errs.add(where + ': unknown epoch_id')
        kind = _kind(record)
        # Type guard before set membership.
        if not isinstance(kind, str) or kind not in KINDS:
            errs.add(where + ': unknown record kind')
        elif kind == 'business':
            if not common.is_text(record.get('obligation_id')):
                errs.add(where + ': business record without obligation_id')
        elif 'obligation_id' in record:
            errs.add(where + ': control record carries an obligation (R14)')
    errs.check()
    declared = common.field(doc['integrity_inputs'], 'per_epoch', list, 'integrity_inputs')
    for index, item in enumerate(declared):
        where = 'integrity_inputs.per_epoch[' + str(index) + ']'
        common.field(item, 'epoch_id', 'text', where)
        common.field(item, 'chain', 'text', where)
        common.field(item, 'records', 'int', where)
    for item in common.duplicates(d['epoch_id'] for d in declared):
        errs.add('duplicate integrity declaration for ' + item)
    if sorted(d['epoch_id'] for d in declared) != sorted(ids):
        errs.add('integrity_inputs.per_epoch must declare exactly the declared epochs')
    errs.check()
    by_epoch = {d['epoch_id']: d for d in declared}
    chains = {}
    for epoch in epochs:
        chain = sorted((r for r in records if r['epoch_id'] == epoch['epoch_id']), key=lambda r: r['seq'])
        start = epoch['counter_start']
        if [r['seq'] for r in chain] != list(range(start, start + len(chain))):
            errs.add(epoch['epoch_id'] + ': chain sequence is not contiguous from counter_start')
        if by_epoch[epoch['epoch_id']]['records'] != len(chain):
            errs.add(epoch['epoch_id'] + ': declared record count differs from the presented chain')
        chains[epoch['epoch_id']] = chain
    errs.check()
    integrity = {
        'source': 'declared_input',
        'per_epoch': [{'epoch_id': e['epoch_id'], 'status': by_epoch[e['epoch_id']]['chain']} for e in epochs],
    }
    return chains, by_epoch, integrity


def _cross_epoch(doc, epochs, chains, by_epoch):
    if len(epochs) != 2:
        return None
    first, second = epochs
    reason = second.get('start_reason')
    if not common.is_text(reason):
        raise common.InputRejected(['epochs[1].start_reason: required for a second epoch'])
    out = {'discontinuity': reason, 'from_epoch': first['epoch_id'], 'to_epoch': second['epoch_id'],
           'link': 'absent', 'note': 'cross-epoch completeness is assessed only from population evidence (R3)'}
    basis = doc['population_evidence']
    if isinstance(basis, dict) and basis.get('kind') == 'epoch_link_evidence':
        link_id = common.field(basis, 'link_record_id', 'text', 'population_evidence')
        links = [r for r in doc['records'] if r['record_id'] == link_id]
        if len(links) != 1 or _kind(links[0]) != 'epoch_link':
            raise common.InputRejected(['population_evidence.link_record_id must name exactly one epoch_link record'])
        link = links[0]
        previous = chains[first['epoch_id']]
        if (link['epoch_id'] != second['epoch_id'] or link.get('previous_epoch_id') != first['epoch_id']
                or not previous or link.get('previous_last_seq') != previous[-1]['seq']):
            raise common.InputRejected(['epoch link record contradicts the declared epochs or chains'])
        if by_epoch[second['epoch_id']]['chain'] == 'verified':
            out['link'] = 'verified'
            out['link_record_id'] = link_id
    return out


def _population(basis, instance_id, declared):
    where = 'population_evidence'
    errs = common.Errors()
    common.field(basis, 'evidence_id', 'text', where)
    scope = common.field(basis, 'scope', dict, where)
    if scope.get('instance_id') != instance_id:
        errs.add(where + '.scope: instance differs from the claim scope')
    span = common.interval(scope.get('interval'), where + '.scope.interval')
    checkpoints = common.field(basis, 'checkpoints', list, where)
    entries = common.field(basis, 'entries', list, where)
    if len(checkpoints) < 2:
        errs.add(where + ': at least two checkpoints are required')
    errs.check()
    for index, item in enumerate(checkpoints):
        common.field(item, 'ledger_seq', 'int', where + '.checkpoints[' + str(index) + ']')
        common.ts(item.get('time'), where + '.checkpoints[' + str(index) + '].time')
    for index, item in enumerate(entries):
        place = where + '.entries[' + str(index) + ']'
        common.field(item, 'ledger_seq', 'int', place)
        common.field(item, 'obligation_id', 'text', place)
        common.ts(item.get('due'), place + '.due')
    first, last = checkpoints[0], checkpoints[-1]
    if first['time'] != span['start'] or last['time'] != span['end']:
        errs.add(where + ': checkpoint times do not equal the scope bounds')
    for item in common.duplicates(e['ledger_seq'] for e in entries):
        errs.add(where + ': duplicate ledger_seq ' + str(item))
    for item in common.duplicates(e['obligation_id'] for e in entries):
        errs.add(where + ': obligation listed twice: ' + item)
    if sorted(e['ledger_seq'] for e in entries) != list(range(first['ledger_seq'] + 1, last['ledger_seq'] + 1)):
        errs.add(where + ': entries do not fill the checkpoint range exactly (R4)')
    for item in entries:
        if not common.contains(span, item['due']):
            errs.add(where + ': ' + item['obligation_id'] + ' is due outside the evidence scope')
    common.check_refs(basis.get('assumptions'), declared, where + '.assumptions', errs)
    errs.check()
    return span, entries, common.ordered(basis['assumptions'], declared)


def assess(doc, declared):
    claim = doc['claim']
    scope = claim['scope']
    if set(scope) != {'instance_id', 'interval'}:
        raise common.InputRejected(['claim.scope: B1 scope must have exactly instance_id and interval'])
    instance_id = common.field(scope, 'instance_id', 'text', 'claim.scope')
    claim_iv = common.interval(scope['interval'], 'claim.scope.interval')
    epochs = _instance_and_epochs(doc, instance_id)
    chains, by_epoch, integrity = _chains(doc, epochs)
    basis = common.field(doc, 'population_evidence', dict, 'input')
    kind = basis.get('kind')
    # Type guard before membership.
    if not isinstance(kind, str) or kind not in BASIS_KINDS:
        raise common.InputRejected(['population_evidence.kind: unknown value'])
    if kind == 'none' and set(basis) != {'kind'}:
        raise common.InputRejected(['population_evidence: kind none carries no other fields'])
    # Link evidence is validated before any one-epoch shortcut: with
    # one epoch there is nothing to link, so the evidence shape is incompatible.
    if kind == 'epoch_link_evidence' and len(epochs) != 2:
        raise common.InputRejected(['population_evidence: epoch_link_evidence requires exactly two epochs'])
    cross = _cross_epoch(doc, epochs, chains, by_epoch)
    polarity = claim['polarity']
    whole = {'instance_id': instance_id, 'interval': claim_iv}
    business = [r for r in doc['records'] if _kind(r) == 'business']
    out = {'integrity': integrity, 'findings': [], 'scoped_results': [], 'unestablished': [],
           'notes': ['integrity is the declared stage-1 input, echoed; this assessor measures nothing',
                     'supported results hold only under the listed declared assumptions']}
    if cross is not None:
        out['cross_epoch'] = cross
    if kind != 'independent_population_evidence':
        if kind == 'none':
            out['basis_assessment'] = {'kind': 'none', 'status': 'absent', 'rules': ['R6']}
            rules, evidence = ['R2', 'R6'], ['no population evidence supplied']
        else:
            out['basis_assessment'] = {'kind': kind, 'evidence_id': common.field(basis, 'evidence_id', 'text', 'population_evidence'),
                                       'status': 'not_population_evidence', 'rules': ['R3']}
            rules, evidence = ['R3', 'R6'], ['an epoch link is not population evidence']
        out['reconciliation'] = None
        out['claim_results'] = [common.result('coverage_complete', polarity, whole, 'not_established', rules, evidence, [])]
        out['unestablished'] = [{'scope': whole, 'affected_claims': ['coverage_complete']}]
        return out
    span, entries, deps = _population(basis, instance_id, declared)
    covers = common.within(claim_iv, span)
    if not covers and not common.within(span, claim_iv):
        raise common.InputRejected(['population_evidence.scope must contain or lie within the claim interval'])
    # Reconciliation region: the claim interval when the evidence covers
    # it, otherwise the evidence span. Obligations due and records timed outside
    # the region do not count, so a record outside the claim scope can never
    # satisfy an obligation inside it (R4).
    region = claim_iv if covers else span
    listed = {e['obligation_id'] for e in entries}
    in_region = [e for e in entries if common.contains(region, e['due'])]
    counts = {e['obligation_id']: [] for e in in_region}
    due = {e['obligation_id']: e['due'] for e in in_region}
    for record in business:
        if common.contains(span, record['time']) and record['obligation_id'] not in listed:
            raise common.InputRejected(['record ' + record['record_id'] + ' carries an obligation absent from the population evidence'])
        if common.contains(region, record['time']) and record['obligation_id'] in counts:
            counts[record['obligation_id']].append(record['record_id'])
    findings = []
    matched = []
    for obligation in sorted(counts):
        carried = counts[obligation]
        if not carried:
            findings.append({'type': 'missing_record', 'obligation_id': obligation, 'due': due[obligation], 'rules': ['R5'],
                             'evidence': 'listed in the population evidence; no business record in scope carries it'})
        elif len(carried) > 1:
            findings.append({'type': 'duplicate_record', 'obligation_id': obligation, 'due': due[obligation], 'rules': ['R5'],
                             'evidence': 'carried by ' + str(len(carried)) + ' business records'})
        else:
            matched.append({'obligation_id': obligation, 'record_id': carried[0]})
    span_scope = {'instance_id': instance_id, 'interval': span}
    region_scope = {'instance_id': instance_id, 'interval': region}
    out['basis_assessment'] = {'kind': kind, 'evidence_id': basis['evidence_id'],
                               'status': 'covers_claim_scope' if covers else 'partial_scope', 'covers': span,
                               'internal_check': str(len(entries)) + ' entries fill the checkpoint range',
                               'conditional_on': deps, 'rules': ['R4'] if covers else ['R4', 'R7']}
    out['reconciliation'] = {'scope': region_scope, 'matched': matched,
                             'missing': [f['obligation_id'] for f in findings if f['type'] == 'missing_record']}
    out['findings'] = findings
    status = 'not_supported' if findings else 'supported'
    if covers:
        out['claim_results'] = [common.result('coverage_complete', polarity, whole, status, ['R4', 'R5'] if findings else ['R4', 'R12'],
                                              ['population evidence covers the claim scope and its internal check holds'], deps)]
        return out
    out['claim_results'] = [common.result('coverage_complete', polarity, whole, 'not_established', ['R6', 'R7'],
                                          ['population evidence covers only part of the claim interval'], [])]
    out['scoped_results'] = [common.result('coverage_complete', polarity, span_scope, status, ['R4', 'R7', 'R12'],
                                           ['population evidence covers this sub-interval'], deps)]
    out['unestablished'] = [{'scope': {'instance_id': instance_id, 'interval': piece}, 'affected_claims': ['coverage_complete']}
                            for piece in _minus(claim_iv, span)]
    return out
