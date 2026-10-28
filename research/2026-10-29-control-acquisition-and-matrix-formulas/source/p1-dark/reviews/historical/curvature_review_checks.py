"""Scoped independent review probes; never reruns or changes main results."""
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'code'))
import numpy as np
import simplex_law as sl
import polynomial_curvature as pc


def exact_polynomial(terms, u, derivative=()):
    value = F(0)
    for alpha, coefficient in terms:
        powers = list(alpha)
        multiplier = coefficient
        for i in derivative:
            multiplier *= powers[i]
            powers[i] -= 1
            if not multiplier:
                break
        if multiplier:
            for x, power in zip(u, powers):
                multiplier *= x ** power
            value += multiplier
    return value


def main():
    names = ['polynomial_curvature.py', 'run_curvature_refinement.py',
             'simplex_law.py', 'hypograph_control.py']
    hashes = {name: sha256((ROOT / 'code' / name).read_bytes()).hexdigest() for name in names}
    counts = {'exact_values': 0, 'exact_gradient_entries': 0,
              'exact_hessian_entries': 0, 'positive_curvature_fallback_cases': 0,
              'finite_command_cases': 0}
    for k in range(2, 6):
        terms = [((0, 0), F(10))]
        for degree in range(1, k + 1):
            for i, alpha in enumerate(sl.compositions(degree, 2)):
                terms.append((alpha, F((-1) ** (i + degree) * (i + 1), degree + 3)))
        law = sl.SimplexLaw(2, k)
        law.ingest([(exact_polynomial(terms, u), exact_polynomial(terms, u)) for u in law.nodes]).transform()
        curve = pc.CurvatureLaw(law)
        for u in ([F(0), F(0)], [F(1, 5), F(0)], [F(1, 15), F(1, 15)], [F(1, 30), F(1, 10)]):
            value, gradient = curve.exact_value_gradient(u)
            assert value == exact_polynomial(terms, u)
            counts['exact_values'] += 1
            for i in range(2):
                assert gradient[i] == exact_polynomial(terms, u, (i,))
                counts['exact_gradient_entries'] += 1
            weights = curve.weights(u, curve.hess_alphas)
            for i in range(2):
                for j in range(2):
                    entry = sum(w * h[i][j] for w, h in zip(weights, curve.hess))
                    assert entry == exact_polynomial(terms, u, (i, j))
                    counts['exact_hessian_entries'] += 1

    positive = sl.SimplexLaw(2, 2)
    positive.ingest([(1 + u[0] ** 2, 1 + u[0] ** 2) for u in positive.nodes]).transform()
    with patch.object(pc.np.linalg, 'eigvalsh', return_value=np.zeros(2)):
        forced = pc.CurvatureLaw(positive)
    assert forced.verification_attempts == 2 and forced.mu > 2
    assert all(p > 0 for row in forced.pivots for p in row)
    counts['positive_curvature_fallback_cases'] += 1

    eigen_failure = None
    try:
        with patch.object(pc.np.linalg, 'eigvalsh', side_effect=np.linalg.LinAlgError('review-injected proposal failure')):
            pc.CurvatureLaw(positive)
    except Exception as exc:
        eigen_failure = type(exc).__name__
    assert eigen_failure == 'LinAlgError'

    # Admissible intervals contain the positive constant source J=1. The
    # acquired polynomial can nevertheless be negative between its nodes.
    noisy = sl.SimplexLaw(1, 4)
    x = [F(1, 50)]
    weights = sl.lagrange_weights(noisy.alphas, sl.barycentric(x, noisy.delta), noisy.k)
    eta = F(49, 100)
    centers = [1 - eta * (1 if w >= 0 else -1) for w in weights]
    intervals = [(y - eta, y + eta) for y in centers]
    assert all(0 < lo <= 1 <= hi for lo, hi in intervals)
    noisy.ingest(intervals).transform()
    noisy_curve = pc.CurvatureLaw(noisy)
    value, _ = noisy_curve.exact_value_gradient(x)
    assert value < 0
    negative_polynomial_failure = None
    try:
        noisy_curve.certificate(x, [F(0)], F(1, 2), 'conductance')
    except Exception as exc:
        negative_polynomial_failure = type(exc).__name__
    assert negative_polynomial_failure == 'AssertionError'

    fake = SimpleNamespace(x=np.array([-0.1, 0.5]), success=False,
                           message='review proposal only', nit=1)
    with patch.object(pc, 'minimize', return_value=fake):
        command = forced.propose([F(0), F(0)], [F(0), F(0)], 'conductance')['command']
    assert all(a >= 0 and (a * (1 << 20)).denominator == 1 for a in command)
    assert sum(command) <= F(1, 5)
    counts['finite_command_cases'] += 1

    for name, digest in hashes.items():
        assert sha256((ROOT / 'code' / name).read_bytes()).hexdigest() == digest
    output = {'scope': 'Independent scoped code-review probes; no main experiment rerun.',
              'reviewed_sha256': hashes, 'checks_passed': counts,
              'reproduced_robustness_gaps': {
                  'numerical_eigen_proposal_exception': eigen_failure,
                  'valid_positive_source_intervals_with_negative_acquired_polynomial': {
                      'candidate': [str(a) for a in x], 'polynomial_value': str(value),
                      'all_node_intervals_contain_constant_J_1': True,
                      'conductance_curvature_call': negative_polynomial_failure}},
              'certificate_mathematical_error_found': False}
    destination = ROOT / 'reviews' / 'CURVATURE_REVIEW_CHECKS.json'
    destination.write_text(json.dumps(output, indent=2) + '\n')
    print(json.dumps(output, indent=2))


if __name__ == '__main__':
    main()
