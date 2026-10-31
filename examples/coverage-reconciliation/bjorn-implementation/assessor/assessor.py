'''Entry point of the bjorn-implementation assessor, revision I1.

Public-package source derivative; this copy has not been executed.

Launch (inside the container, code read-only at /app): the bootstrap
runs as python3 -I -B -S, adds only /app to sys.path and calls
runpy.run_module('assessor', run_name='__main__', alter_sys=True) with
sys.argv = ['assessor', '--input', '/input/assessor-input.json']. The
__main__ guard below then calls main(sys.argv[1:]).

Reads exactly the one input path. Uses no environment variable, clock,
network, subprocess or other file, and writes no file. Writes exactly one
JSON object to stdout; diagnostics go to stderr.

Exit codes: 0 outcome emitted; 2 input rejected (a rejection object is still
written to stdout); 1 internal error (stdout may be empty).

Numbers: the constants NaN, Infinity and -Infinity, a finite-looking number
that overflows to a non-finite float (for example 1e400), and an integer
beyond the interpreter's digit limit are all rejected as input_rejected.

Outcomes are derived only from evidence fields of the input. case_id is
echoed, never branched on. family only selects which evidence blocks are
required and must agree with claim.kind.
'''
import json
import sys

import assessor_common as common
import assessor_b1
import assessor_b2


def _reject_constant(name):
    raise common.InputRejected(['non-finite JSON number ' + name + ' is not allowed'])


def _finite_float(text):
    value = float(text)
    if value != value or value in (float('inf'), float('-inf')):
        raise common.InputRejected(['JSON number ' + text[:40] + ' is not finite as a float'])
    return value


def _unique_pairs(pairs):
    seen = {}
    for key, value in pairs:
        if key in seen:
            raise common.InputRejected(['duplicate JSON key ' + key])
        seen[key] = value
    return seen


def parse_args(argv):
    if len(argv) != 2 or argv[0] != '--input' or not argv[1]:
        raise common.InputRejected(['usage: assessor --input /input/assessor-input.json'])
    return argv[1]


def load(path):
    with open(path, 'rb') as handle:
        raw = handle.read()
    try:
        text = raw.decode('utf-8')
    except UnicodeDecodeError:
        raise common.InputRejected(['input is not valid UTF-8'])
    try:
        return json.loads(text, object_pairs_hook=_unique_pairs, parse_constant=_reject_constant,
                          parse_float=_finite_float)
    except RecursionError:
        raise common.InputRejected(['input nesting is too deep'])
    except ValueError as exc:
        raise common.InputRejected(['input is not valid JSON: ' + str(exc)])


def assess(doc):
    declared = common.validate_common(doc)
    if doc['family'] == 'B1':
        body = assessor_b1.assess(doc, declared)
    else:
        body = assessor_b2.assess(doc, declared)
    outcome = {
        'schema': common.OUTPUT_SCHEMA,
        'result': 'assessed',
        'case_id': doc['case_id'],
        'family': doc['family'],
    }
    for key, value in body.items():
        if key in outcome:
            raise RuntimeError('family module returned a reserved key: ' + key)
        outcome[key] = value
    return outcome


def main(argv):
    try:
        path = parse_args(argv)
        doc = load(path)
        outcome = assess(doc)
    except common.InputRejected as exc:
        print(json.dumps({'schema': common.OUTPUT_SCHEMA, 'result': 'input_rejected',
                          'errors': exc.errors}, sort_keys=True))
        return 2
    except OSError as exc:
        sys.stderr.write('cannot read input: ' + exc.__class__.__name__ + chr(10))
        return 1
    except Exception as exc:
        sys.stderr.write('internal error: ' + exc.__class__.__name__ + ': ' + str(exc) + chr(10))
        return 1
    print(json.dumps(outcome, sort_keys=True))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
