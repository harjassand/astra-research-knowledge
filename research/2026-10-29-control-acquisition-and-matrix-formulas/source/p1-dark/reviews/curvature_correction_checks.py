"""Focused correction checks; never reruns the five main acquisition cases.

Exercises corrected code, exact constant-source certificates, and the actual
runner on a disposable synthetic interval record. Historical probes remain
separate and explicitly load the historical implementation.
"""
from contextlib import redirect_stdout
from fractions import Fraction as F
from hashlib import sha256
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from unittest.mock import patch
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'code'))
import numpy as np
import simplex_law as sl
import hypograph_control as hc
import polynomial_curvature as pc
import run_curvature_refinement as runner


def encoded(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {k: encoded(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [encoded(v) for v in value]
    return value


def assert_pd_certificate(curve):
    assert curve.mu >= 0 and len(curve.pivots) == len(curve.hess)
    for H, recorded in zip(curve.hess, curve.pivots):
        matrix = [[(curve.mu if i == j else F(0)) - H[i][j]
                   for j in range(curve.law.n)] for i in range(curve.law.n)]
        independently_repeated = pc.positive_definite(matrix)
        assert independently_repeated == recorded and all(x > 0 for x in recorded)


def positive_curvature_law():
    law = sl.SimplexLaw(2, 2)
    return law.ingest([(1 + u[0] ** 2, 1 + u[0] ** 2) for u in law.nodes]).transform()


def noisy_constant_law(zero_value=False):
    law = sl.SimplexLaw(1, 4)
    x = [F(1, 64)]  # An exact DAC20 command.
    weights = sl.lagrange_weights(law.alphas, sl.barycentric(x, law.delta), law.k)
    Lambda = sum(abs(w) for w in weights)
    eta = 1 / Lambda if zero_value else F(49, 100)
    centers = [1 - eta * (1 if w >= 0 else -1) for w in weights]
    intervals = [(y - eta, y + eta) for y in centers]
    assert all(0 < lo <= 1 <= hi for lo, hi in intervals)
    law.ingest(intervals).transform()
    return law, x, eta


def assert_retained(proposal, initial, expected_message=None):
    assert proposal['command'] == hc.finite_command(initial, 20)
    assert not proposal['optimizer_success_not_certificate']
    assert proposal['source_readings'] == 0
    if expected_message:
        assert expected_message in proposal['optimizer_message']


def check_runner_preservation(law, optimizer_patch, expected_reason):
    """Exercise the actual runner against a tiny disposable source record."""
    baseline = F(1, 2)
    tasks = []
    for utility in ('conductance', 'compliance'):
        for task, price in enumerate((F(7, 10), F(-7, 10), F(0))):
            old = hc.certify_task(law, [price], baseline, utility=utility)
            tasks.append({'utility': utility, 'task': task, 'prices': [price], 'certificate': old})
    previous = {'n': 1, 'degree': 4, 'J_bernstein_coefficients': law.bernstein_coefficients,
                'calibrated_c0_lower': baseline, 'tasks': tasks,
                'predictions': [{'u': [u], 'checker_J': F(1)}
                                for u in (F(0), F(1, 64), F(1, 5))],
                'baseline_dark_controls': [0]}
    raw = {'warrants': {'G': F(1), 'kappa': F(1)},
           'J_intervals': law.intervals,
           'source_vectors_checker_only': [[F(0), F(0)]],
           'scope': 'Disposable constant-source review interval record; no main experiment.'}
    label = 'review_constant_source'
    with TemporaryDirectory(prefix='curvature_correction_') as directory:
        temporary_root = Path(directory)
        (temporary_root / 'results').mkdir()
        raw_path = temporary_root / 'results' / (label + '_raw.json')
        raw_path.write_text(json.dumps(encoded(raw)))
        (temporary_root / 'results' / (label + '_results.json')).write_text(json.dumps(encoded(previous)))
        raw_before = raw_path.read_bytes()
        with patch.object(runner, 'ROOT', temporary_root), \
             patch.object(pc.np.linalg, 'eigvalsh', return_value=np.array([np.nan])), \
             patch.object(pc, 'minimize', **optimizer_patch), redirect_stdout(StringIO()):
            runner.run_case(label)
        detail = runner.decoded(json.loads((temporary_root / 'results' / (label + '_curvature.json')).read_text()))
        assert raw_path.read_bytes() == raw_before
        assert detail['extra_source_readings'] == 0
        assert detail['source_gradients_acquired'] == 0
        assert 'Nonfinite numerical eigenvalue' in detail['eigen_proposal_failure']
        checked = []
        for old, row in zip(tasks, detail['tasks']):
            price = row['prices'][0]
            x = row['candidate']['command'][0]
            phi = F(1) if row['utility'] == 'conductance' else F(-1)
            exact_maximum = phi + max(F(0), -price * law.delta)
            exact_candidate = phi - price * x
            lower = row['candidate']['objective_lower_without_baseline']
            upper = row['global_objective_upper_without_baseline']
            assert lower <= exact_candidate <= exact_maximum <= upper
            assert exact_maximum - exact_candidate <= row['continuous_simplex_regret']
            assert row['continuous_simplex_regret'] <= old['certificate']['continuous_simplex_regret']
            assert (x * (1 << 20)).denominator == 1 and F(0) <= x <= law.delta
            if expected_reason:
                assert_retained(row['proposal'], old['certificate']['candidate']['command'], expected_reason)
            else:
                assert not row['proposal']['optimizer_success_not_certificate']
            checked.append({'utility': row['utility'], 'price': price,
                            'exact_global_optimum': exact_maximum,
                            'global_upper': upper, 'certified_regret': row['continuous_simplex_regret'],
                            'previous_regret': old['certificate']['continuous_simplex_regret']})
        return {'task_checks': len(checked), 'raw_unchanged': True,
                'eigen_failure_logged': detail['eigen_proposal_failure'],
                'cases': checked}


def main():
    paths = {name: ROOT / 'code' / name for name in
             ('polynomial_curvature.py', 'run_curvature_refinement.py',
              'simplex_law.py', 'hypograph_control.py')}
    hashes = {name: sha256(path.read_bytes()).hexdigest() for name, path in paths.items()}
    historical_paths = sorted((ROOT / 'reviews' / 'historical').glob('*'))
    historical_hashes = {p.name: sha256(p.read_bytes()).hexdigest() for p in historical_paths if p.is_file()}
    records = {}

    for label, kwargs in (
        ('eigen_LinAlgError', {'side_effect': np.linalg.LinAlgError('review-injected eigen failure')}),
        ('eigen_NaN', {'return_value': np.array([np.nan, np.nan])}),
        ('inaccurate_finite_eigenvalue', {'return_value': np.zeros(2)}),
    ):
        with patch.object(pc.np.linalg, 'eigvalsh', **kwargs):
            curve = pc.CurvatureLaw(positive_curvature_law())
        assert_pd_certificate(curve)
        assert curve.mu > 2
        if label == 'inaccurate_finite_eigenvalue':
            assert curve.verification_attempts == 2 and curve.eigen_proposal_failure is None
        else:
            assert curve.verification_attempts == 1 and curve.eigen_proposal_failure
        records[label] = {'mu': curve.mu, 'attempts': curve.verification_attempts,
                          'failure_log': curve.eigen_proposal_failure,
                          'all_exact_pivots_positive': True}

    huge = sl.SimplexLaw(1, 2)
    huge_value = F(10 ** 400)
    huge.ingest([(huge_value, huge_value) for _ in huge.nodes]).transform()
    huge_curve = pc.CurvatureLaw(huge)
    assert_pd_certificate(huge_curve)
    assert huge_curve.float_proposal_failure
    initial = [F(1, 8)]
    proposal = huge_curve.propose([F(0)], initial, 'compliance')
    assert_retained(proposal, initial, 'OverflowError')
    records['floating_coefficient_overflow'] = {
        'failure_log': huge_curve.float_proposal_failure, 'initial_preserved': True,
        'mu_exactly_verified': True}

    law, x, eta = noisy_constant_law()
    curve = pc.CurvatureLaw(law)
    assert_pd_certificate(curve)
    p, _ = curve.exact_value_gradient(x)
    assert p < 0
    candidate_cases = []
    for zero in (False, True):
        case_law, command, case_eta = noisy_constant_law(zero)
        case_curve = pc.CurvatureLaw(case_law)
        value, _ = case_curve.exact_value_gradient(command)
        assert value == 0 if zero else value < 0
        for utility in ('conductance', 'compliance'):
            for price in (F(7, 10), F(-7, 10), F(0)):
                cert = case_curve.certificate(command, [price], F(1, 2), utility)
                phi = F(1) if utility == 'conductance' else F(-1)
                exact_maximum = phi + max(F(0), -price * case_law.delta)
                exact_candidate = phi - price * command[0]
                assert cert['objective_lower_without_baseline'] <= exact_candidate
                assert exact_maximum <= cert['global_objective_upper_without_baseline']
                assert exact_maximum - exact_candidate <= cert['continuous_simplex_regret']
                if utility == 'compliance':
                    assert cert['positive_utility_tangent_point'] == F(1, 2)
                candidate_cases.append({'zero_polynomial': zero, 'utility': utility,
                                       'price': price, 'polynomial_value': value,
                                       'exact_maximum': exact_maximum,
                                       'certified_upper': cert['global_objective_upper_without_baseline']})
    records['nonpositive_polynomial_exact_certificates'] = {'cases': candidate_cases,
                                                            'case_count': len(candidate_cases)}

    def call_objective(fun, x0, **kwargs):
        fun(x0)
        raise AssertionError('Expected checked compliance proposal rejection')

    with patch.object(pc, 'minimize', side_effect=call_objective):
        proposal = curve.propose([F(0)], x, 'compliance')
    assert_retained(proposal, x, 'Nonpositive polynomial')
    records['nonpositive_compliance_proposal'] = {'initial_preserved': True,
                                                 'failure_log': proposal['optimizer_message']}
    with patch.object(pc, 'minimize', side_effect=call_objective), \
         patch.object(curve, 'float_value_gradient', return_value=(0.0, np.zeros(1))):
        proposal = curve.propose([F(0)], x, 'compliance')
    assert_retained(proposal, x, 'Nonpositive polynomial')
    records['zero_compliance_proposal'] = {'initial_preserved': True}

    for label, kwargs in (
        ('optimizer_LinAlgError', {'side_effect': np.linalg.LinAlgError('review-injected optimizer failure')}),
        ('optimizer_NaN_command', {'return_value': SimpleNamespace(x=np.array([np.nan]), success=True, message='nan', nit=1)}),
    ):
        with patch.object(pc, 'minimize', **kwargs):
            proposal = curve.propose([F(0)], x, 'conductance')
        assert_retained(proposal, x)
        records[label] = {'initial_preserved': True, 'failure_log': proposal['optimizer_message']}

    records['runner_exception_preserves_old_candidate'] = check_runner_preservation(
        law, {'side_effect': np.linalg.LinAlgError('review-injected optimizer failure')}, 'LinAlgError')
    records['runner_unsuccessful_finite_proposal_is_only_a_candidate'] = check_runner_preservation(
        law, {'return_value': SimpleNamespace(x=np.array([0.2]), success=False,
                                             message='review unconverged finite proposal', nit=100)}, None)

    for name, digest in hashes.items():
        assert sha256(paths[name].read_bytes()).hexdigest() == digest
    for name, digest in historical_hashes.items():
        assert sha256((ROOT / 'reviews' / 'historical' / name).read_bytes()).hexdigest() == digest
    output = {'scope': 'Focused correction verification; no rerun or modification of the five main acquisition cases.',
              'all_focused_checks_passed': True, 'reviewed_sha256': hashes,
              'historical_byte_originals_unchanged': historical_hashes,
              'records': records,
              'new_invalid_certificate_found': False}
    (ROOT / 'reviews' / 'CURVATURE_CORRECTION_CHECKS.json').write_text(json.dumps(encoded(output), indent=2) + '\n')
    print(json.dumps({'all_passed': True, 'checks': list(records), 'reviewed_sha256': hashes}, indent=2))


if __name__ == '__main__':
    main()
