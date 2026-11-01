'''B2 family logic of the bjorn-implementation assessor, revision I1.

Public-package source derivative; this copy has not been executed.

Implements rules R1 and R7-R13 in package bjorn-vectors/rules.json. Standard library only; no file, network, environment, clock or
subprocess access. Results are derived only from evidence fields of the
input; case_id and evidence identifiers are only echoed. Every inconsistency
in the input raises InputRejected.
'''
import assessor_common as common

SEGMENT_STATUS = ('available', 'available_incomplete', 'unavailable')
COMPLETENESS_KINDS = ('sequenced_feed', 'sequenced_ledger')
OBSERVATION_KEYS = {'surface', 'evidence_id', 'observer', 'mechanism', 'segments', 'observed_effects', 'assumptions'}
BINDING_KEYS = {'evidence_id', 'surface', 'route_field', 'mediated_routes', 'statement', 'assumptions'}
EFFECT_KEYS = {'effect_id', 'time', 'effect_ref', 'feed_seq', 'route'}
COMPLETENESS_KEYS = {'kind', 'first_seq', 'last_seq', 'heartbeat_interval_s', 'gaps'}


def _span(item):
    return {'start': item['start'], 'end': item['end']}


def _completeness(value, where):
    if value is None:
        return None
    if not isinstance(value, dict) or not set(value) <= COMPLETENESS_KEYS:
        raise common.InputRejected([where + ': completeness must be null or a completeness object'])
    if value.get('kind') not in COMPLETENESS_KINDS:
        raise common.InputRejected([where + ': unknown completeness kind'])
    first = common.field(value, 'first_seq', 'int', where)
    last = common.field(value, 'last_seq', 'int', where)
    common.field(value, 'gaps', list, where)
    if 'heartbeat_interval_s' in value:
        common.field(value, 'heartbeat_interval_s', 'int', where)
    if first > last:
        raise common.InputRejected([where + ': first_seq is above last_seq'])
    return value


def _observations(doc, required, claim_iv, declared):
    observations = common.field(doc, 'observations', list, 'input')
    errs = common.Errors()
    by_surface = {}
    for index, obs in enumerate(observations):
        where = 'observations[' + str(index) + ']'
        if not isinstance(obs, dict) or set(obs) != OBSERVATION_KEYS:
            raise common.InputRejected([where + ': unexpected or missing fields'])
        surface = common.field(obs, 'surface', 'text', where)
        for key in ('evidence_id', 'observer', 'mechanism'):
            common.field(obs, key, 'text', where)
        if surface in by_surface:
            errs.add(where + ': second observation of surface ' + surface)
        if surface not in required:
            errs.add(where + ': surface ' + surface + ' is not required by the claim')
        by_surface[surface] = obs
        common.check_refs(obs['assumptions'], declared, where + '.assumptions', errs)
        segments = common.field(obs, 'segments', list, where)
        if not segments:
            errs.add(where + ': no segments')
        for pos, segment in enumerate(segments):
            place = where + '.segments[' + str(pos) + ']'
            if not isinstance(segment, dict) or not {'start', 'end', 'status', 'completeness'} <= set(segment):
                raise common.InputRejected([place + ': missing fields'])
            common.interval(_span(segment), place)
            if segment['status'] not in SEGMENT_STATUS:
                errs.add(place + ': unknown status')
            _completeness(segment['completeness'], place + '.completeness')
        if segments and (segments[0]['start'] != claim_iv['start'] or segments[-1]['end'] != claim_iv['end']
                         or any(a['end'] != b['start'] for a, b in zip(segments, segments[1:]))):
            errs.add(where + ': segments do not tile the claim interval')
        effects = common.field(obs, 'observed_effects', list, where)
        for pos, effect in enumerate(effects):
            place = where + '.observed_effects[' + str(pos) + ']'
            if not isinstance(effect, dict) or not set(effect) <= EFFECT_KEYS:
                raise common.InputRejected([place + ': unexpected fields'])
            common.field(effect, 'effect_id', 'text', place)
            common.field(effect, 'effect_ref', 'text', place)
            common.ts(effect.get('time'), place + '.time')
            if 'feed_seq' in effect:
                common.field(effect, 'feed_seq', 'int', place)
            if 'route' in effect:
                common.field(effect, 'route', 'text', place)
            if not common.contains(claim_iv, effect['time']):
                errs.add(place + ': effect outside the claim interval')
        for item in common.duplicates(e['feed_seq'] for e in effects if 'feed_seq' in e):
            errs.add(where + ': duplicate feed_seq ' + str(item))
    for surface in required:
        if surface not in by_surface:
            errs.add('required surface ' + surface + ' has no observation')
    all_effects = [e for o in observations for e in o['observed_effects']]
    for item in common.duplicates(e['effect_id'] for e in all_effects):
        errs.add('duplicate effect_id ' + item)
    errs.check()
    return by_surface


def _adequacy(obs):
    '''Return [(segment, adequate, reason)] for one validated observation.'''
    rows = []
    for segment in obs['segments']:
        comp = segment['completeness']
        inside = [e for e in obs['observed_effects'] if common.contains(_span(segment), e['time'])]
        if segment['status'] != 'available':
            rows.append((segment, False, segment['status']))
        elif comp is None:
            rows.append((segment, False, 'no_completeness_mechanism'))
        elif comp['gaps']:
            rows.append((segment, False, 'declared_gaps'))
        elif any(not common.is_int(e.get('feed_seq')) or not comp['first_seq'] <= e['feed_seq'] <= comp['last_seq'] for e in inside):
            rows.append((segment, False, 'effect_outside_range'))
        else:
            rows.append((segment, True, None))
    return rows


def _bindings(doc, required, declared):
    bindings = common.field(doc, 'mediation_evidence', list, 'input')
    errs = common.Errors()
    by_surface = {}
    exhaustive = {}
    for index, binding in enumerate(bindings):
        where = 'mediation_evidence[' + str(index) + ']'
        if not isinstance(binding, dict) or set(binding) != BINDING_KEYS:
            raise common.InputRejected([where + ': unexpected or missing fields'])
        surface = common.field(binding, 'surface', 'text', where)
        common.field(binding, 'evidence_id', 'text', where)
        common.field(binding, 'statement', 'text', where)
        if binding['route_field'] != 'route':
            errs.add(where + ': route_field must be route')
        routes = common.field(binding, 'mediated_routes', list, where)
        if not routes or not all(common.is_text(r) for r in routes) or common.duplicates(routes):
            errs.add(where + ': mediated_routes must be unique non-empty strings')
        if surface in by_surface:
            errs.add(where + ': second binding for surface ' + surface)
        if surface not in required:
            errs.add(where + ': surface ' + surface + ' is not required by the claim')
        common.check_refs(binding['assumptions'], declared, where + '.assumptions', errs)
        errs.check()
        by_surface[surface] = binding
        exhaustive[surface] = common.binding_exhaustive(binding, where)
    return by_surface, exhaustive


def assess(doc, declared):
    claim = doc['claim']
    scope = claim['scope']
    if set(scope) != {'surfaces', 'interval'}:
        raise common.InputRejected(['claim.scope: B2 scope must have exactly surfaces and interval'])
    required = common.field(scope, 'surfaces', list, 'claim.scope')
    if not required or not all(common.is_text(s) for s in required) or common.duplicates(required):
        raise common.InputRejected(['claim.scope.surfaces: must be unique non-empty strings'])
    claim_iv = common.interval(scope['interval'], 'claim.scope.interval')
    records = doc['records']
    for index, record in enumerate(records):
        common.field(record, 'effect_ref', 'text', 'records[' + str(index) + ']')
    for item in common.duplicates(r['effect_ref'] for r in records):
        raise common.InputRejected(['effect_ref carried by more than one record: ' + item])
    chain = common.field(doc['integrity_inputs'], 'chain', 'text', 'integrity_inputs')
    seqs = sorted(r['seq'] for r in records)
    visible = 'consistent' if seqs == list(range(len(records))) else 'inconsistent'
    observations = _observations(doc, required, claim_iv, declared)
    bindings, exhaustive = _bindings(doc, required, declared)
    adequacy = {s: _adequacy(observations[s]) for s in required}
    refs = {r['effect_ref'] for r in records}
    effects = [(s, e) for s in required for e in observations[s]['observed_effects']]

    def route_state(surface, effect):
        binding = bindings.get(surface)
        if binding is None or 'route' not in effect:
            return 'undetermined'
        if effect['route'] in binding['mediated_routes']:
            return 'mediated'
        return 'non_mediated' if exhaustive[surface] else 'undetermined'

    def deps(surfaces):
        ids = []
        for surface in surfaces:
            ids.extend(observations[surface]['assumptions'])
            if surface in bindings:
                ids.extend(bindings[surface]['assumptions'])
        return common.ordered(ids, declared)

    def classify(span):
        inside = [(s, e) for s, e in effects if common.contains(span, e['time'])]
        witnessed = [(s, e) for s, e in inside if route_state(s, e) == 'non_mediated']
        if witnessed:
            return 'bypass', deps(sorted({s for s, _ in witnessed}, key=required.index)), witnessed
        adequate = all(ok for s in required for seg, ok, _ in adequacy[s] if common.overlaps(_span(seg), span))
        bound = all(s in bindings for s in required)
        mediated = all(route_state(s, e) == 'mediated' for s, e in inside)
        if adequate and bound and mediated:
            return 'positive', deps(required), []
        return 'undecided', [], []

    kind, used, witnessed = classify(claim_iv)
    whole = {'surfaces': list(required), 'interval': claim_iv}
    if kind == 'bypass':
        names = ', '.join(e['effect_id'] + ' route ' + e['route'] for _, e in witnessed)
        no_bypass = common.result('no_bypass', common.POLARITY['no_bypass'], whole, 'not_supported', ['R11'],
                                  ['witnessed non-mediated route: ' + names], used)
        bypass = common.result('bypass_occurred', common.POLARITY['bypass_occurred'], whole, 'supported', ['R11', 'R12'],
                               ['witnessed non-mediated route: ' + names], used)
    elif kind == 'positive':
        text = ['every required surface adequately observed and bound; every observed effect took a mediated route']
        no_bypass = common.result('no_bypass', common.POLARITY['no_bypass'], whole, 'supported', ['R8', 'R12'], text, used)
        bypass = common.result('bypass_occurred', common.POLARITY['bypass_occurred'], whole, 'not_supported', ['R8'], text, used)
    else:
        text = ['observation, binding or route evidence is insufficient and no non-mediated route was witnessed']
        no_bypass = common.result('no_bypass', common.POLARITY['no_bypass'], whole, 'not_established', ['R9', 'R13'], text, [])
        bypass = common.result('bypass_occurred', common.POLARITY['bypass_occurred'], whole, 'not_established', ['R9', 'R11'], text, [])

    scoped = []
    unestablished = []
    if kind == 'undecided':
        points = sorted({p for s in required for seg, _, _ in adequacy[s] for p in (seg['start'], seg['end'])}, key=common.ts)
        runs = []
        for start, end in zip(points, points[1:]):
            piece = {'start': start, 'end': end}
            if classify(piece)[0] == 'positive':
                if runs and runs[-1]['end'] == start:
                    runs[-1]['end'] = end
                else:
                    runs.append(dict(piece))
        for run in runs:
            if run != claim_iv:
                scoped.append(common.result('no_bypass', common.POLARITY['no_bypass'], {'surfaces': list(required), 'interval': run},
                                            'supported', ['R7', 'R8', 'R12'],
                                            ['every required surface adequately observed and bound in this sub-interval'], deps(required)))
        gaps = {}
        for surface in required:
            undetermined = any(route_state(surface, e) == 'undetermined' for s, e in effects if s == surface)
            if surface not in bindings or undetermined:
                spans = [claim_iv]
            else:
                spans = [_span(seg) for seg, ok, _ in adequacy[surface] if not ok]
            for span in spans:
                gaps.setdefault((span['start'], span['end']), []).append(surface)
        for (start, end), surfaces in sorted(gaps.items(), key=lambda item: common.ts(item[0][0])):
            unestablished.append({'scope': {'surfaces': surfaces, 'interval': {'start': start, 'end': end}},
                                  'affected_claims': ['no_bypass', 'bypass_occurred']})

    findings = []
    for surface, effect in effects:
        if effect['effect_ref'] not in refs:
            findings.append({'type': 'unrecorded_effect', 'effect_id': effect['effect_id'], 'surface': surface,
                             'time': effect['time'], 'rules': ['R10'],
                             'evidence': 'observed effect_ref matches no record'})
    for surface, effect in effects:
        if route_state(surface, effect) == 'non_mediated':
            findings.append({'type': 'non_mediated_route', 'effect_id': effect['effect_id'], 'surface': surface,
                             'time': effect['time'], 'rules': ['R11'],
                             'evidence': 'route is not a mediated route under an exhaustive binding'})

    observation_assessment = []
    mediation_assessment = []
    for surface in required:
        observation_assessment.append({
            'surface': surface,
            'adequate': [_span(seg) for seg, ok, _ in adequacy[surface] if ok],
            'inadequate': [dict(_span(seg), reason=reason) for seg, ok, reason in adequacy[surface] if not ok],
        })
        if surface in bindings:
            mediation_assessment.append({'surface': surface, 'evidence_id': bindings[surface]['evidence_id'], 'status': 'bound',
                                         'exhaustive': exhaustive[surface], 'rules': ['R8']})
        else:
            mediation_assessment.append({'surface': surface, 'status': 'absent', 'exhaustive': None, 'rules': ['R13']})

    return {
        'integrity': {'source': 'declared_input', 'status': chain, 'visible_log': visible},
        'observation_assessment': observation_assessment,
        'mediation_assessment': mediation_assessment,
        'findings': findings,
        'claim_results': [no_bypass, bypass],
        'scoped_results': scoped,
        'unestablished': unestablished,
        'notes': ['integrity status is the declared stage-1 input, echoed; visible_log is computed from the presented records',
                  'record correspondence (unrecorded_effect) is reported separately from mediation',
                  'supported and not_supported results hold only under the listed declared assumptions'],
    }
