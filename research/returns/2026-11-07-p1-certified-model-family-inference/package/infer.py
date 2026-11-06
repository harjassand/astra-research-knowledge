"""Command-line inference and exact certificate replay for the model family.

  python3 infer.py solve INPUT.json OUTPUT.json
  python3 infer.py verify INPUT.json OUTPUT.json

The supplied slope bounds and stationary-law model are scientific premises.
The checker verifies a consequence of those premises, not their physical truth.
"""
from fractions import Fraction as Q
from pathlib import Path
import argparse
import json

from network import (Envelope, Network, InconsistentData, require,
                     certified_trajectory, verify_trajectory,
                     certified_equilibrium, verify_equilibrium,
                     contraction_scaling)


def build_models(spec):
    sources_lower, sources_upper = [], []
    for law in spec['laws']:
        m, upper = map(Q, law['slopes'])
        sources_lower.append(Envelope(m, upper, law['samples'], 'lower'))
        sources_upper.append(Envelope(m, upper, law['samples'], 'upper'))
    # The lower state uses the upper constitutive force.
    return (Network(spec['rows'], sources_upper, spec['forcing']),
            Network(spec['rows'], sources_lower, spec['forcing']))


def prepare(spec):
    models = build_models(spec)
    n = models[0].n
    mode = spec['mode']
    require(mode in ('transient', 'equilibrium'), 'Unknown inference mode')
    tolerance = Q(spec['endpoint_error'])
    require(tolerance > 0, 'The requested numerical error must be positive')
    readout = list(map(Q, spec.get('nonnegative_readout', [str(Q(1, n))]*n)))
    require(len(readout) == n and min(readout) >= 0, 'Readout must be nonnegative')
    if mode == 'transient':
        box = [tuple(map(Q, row)) for row in spec['initial_box']]
        require(len(box) == n and all(len(row) == 2 and row[0] <= row[1] for row in box),
                'Invalid initial box')
        require(Q(spec['horizon']) >= 0, 'Negative horizon')
        weights = [Q(1)]*n
        initials = [[row[j] for row in box] for j in range(2)]
        return models, models, weights, initials, readout, tolerance
    first = contraction_scaling(models[0])
    second = contraction_scaling(models[1])
    require(first is not None and second is not None,
            'This equilibrium operation requires a certified contracting comparison matrix')
    weights, lower = first
    other_weights, upper = second
    require(weights == other_weights)
    return models, (lower, upper), weights, None, readout, tolerance


def bounds_from_certificates(certificates, weights, readout):
    c0, c1 = certificates
    lower = [w*(Q(x)-Q(c0['radius'])) for x, w in zip(c0['state'], weights)]
    upper = [w*(Q(x)+Q(c1['radius'])) for x, w in zip(c1['state'], weights)]
    require(all(a <= b for a, b in zip(lower, upper)), 'Reversed enclosure')
    return {'coordinate_intervals': [[str(a), str(b)] for a, b in zip(lower, upper)],
            'readout_interval': [str(sum((a*w for a, w in zip(lower, readout)), Q(0))),
                                 str(sum((a*w for a, w in zip(upper, readout)), Q(0)))]}


def solve(spec):
    try:
        original, models, weights, initials, readout, tolerance = prepare(spec)
    except InconsistentData as error:
        return {'status': 'inconsistent_data', 'input': spec, 'reason': str(error)}
    error_scale = max(max(weights), sum((a*b for a, b in zip(weights, readout)), Q(0)))
    numerical_tolerance = tolerance/(2*error_scale)
    certificates = []
    for j, model in enumerate(models):
        if spec['mode'] == 'transient':
            cert = certified_trajectory(model, initials[j], Q(spec['horizon']), numerical_tolerance)
            verify_trajectory(model, cert)
        else:
            cert = certified_equilibrium(model, numerical_tolerance)
            verify_equilibrium(model, cert)
        certificates.append(cert)
    result = {'status': 'certified', 'input': spec,
              'original_endpoint_models': [m.document() for m in original],
              'evaluation_models': [m.document() for m in models],
              'coordinate_scaling': list(map(str, weights)),
              'certificates': certificates,
              'endpoint_interpretation':
              'Two admissible stationary source models attain the true lower and upper bounds; '
              'reported bounds include the displayed numerical error certificates.'}
    result.update(bounds_from_certificates(certificates, weights, readout))
    return result


def verify(spec, result):
    require(result['input'] == spec, 'The certificate is for a different input')
    if result['status'] == 'inconsistent_data':
        try:
            prepare(spec)
        except InconsistentData:
            return True
        raise ValueError('The claimed data inconsistency was not reproduced')
    require(result['status'] == 'certified')
    original, models, weights, initials, readout, tolerance = prepare(spec)
    require(result['original_endpoint_models'] == [m.document() for m in original])
    require(result['evaluation_models'] == [m.document() for m in models])
    require(result['coordinate_scaling'] == list(map(str, weights)))
    require(len(result['certificates']) == 2)
    error_scale = max(max(weights), sum((a*b for a, b in zip(weights, readout)), Q(0)))
    for j, (model, cert) in enumerate(zip(models, result['certificates'])):
        if spec['mode'] == 'transient':
            require(list(map(Q, cert['initial'])) == initials[j])
            require(Q(cert['horizon']) == Q(spec['horizon']))
            verify_trajectory(model, cert)
        else:
            verify_equilibrium(model, cert)
        require(2*Q(cert['radius'])*error_scale <= tolerance, 'Endpoint tolerance not met')
    for key, value in bounds_from_certificates(result['certificates'], weights, readout).items():
        require(result[key] == value, 'Incorrect reported task interval')
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation', choices=['solve', 'verify'])
    parser.add_argument('input')
    parser.add_argument('output')
    args = parser.parse_args()
    spec = json.loads(Path(args.input).read_text())
    if args.operation == 'solve':
        result = solve(spec)
        Path(args.output).write_text(json.dumps(result, separators=(',', ':'))+'\n')
        print(json.dumps({'status': result['status'], 'readout_interval': result.get('readout_interval')}))
    else:
        result = json.loads(Path(args.output).read_text())
        verify(spec, result)
        print('PASS: exact rational inference certificate')


if __name__ == '__main__':
    main()
