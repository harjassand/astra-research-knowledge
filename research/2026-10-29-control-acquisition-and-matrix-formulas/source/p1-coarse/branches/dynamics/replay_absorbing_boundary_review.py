"""Independent saved-count replay for the no-source-gap boundary compiler.

No trajectory generation, hidden matrix, hidden norm cap or source tail enters
this review. Exact Fraction arithmetic accepts all confidence and matrix claims.
"""
from fractions import Fraction as F
from pathlib import Path
from math import factorial
import hashlib
import importlib.util
import json

from replay_multiboundary_review import (
    decode, eye, tr, mm, scale, sub, vec, determinant, psd3, check_endpoint,
)

ROOT = Path(__file__).resolve().parents[2]
RESULT = ROOT / 'results/ABSORBING_BOUNDARY_RESULTS.json'
CODE = ROOT / 'core/absorbing_boundary_compiler.py'


def endpoint(count, n, p, ell, side):
    assert 0 <= p <= 1
    assert p <= F(count, n) if side == 'lower' else p >= F(count, n)
    check_endpoint(count, n, p, ell, side)


def review_acquisition(data):
    receipts = data['receipts']
    assert len(receipts) == 6
    assert len({(r['mode'], r['start_boundary']) for r in receipts}) == 6
    for r in receipts:
        n, h, j = r['trials'], r['horizon'], r['start_boundary']
        first, final = r['first_step_boundary_counts'], r['terminal_boundary_counts']
        parity = r['excursion_return_counts_even_odd']
        pending, dead = r['pending_alive_at_censor'], r['absorbed_before_boundary_return']
        returned = sum(map(sum, parity))
        assert sum(first) + r['first_step_alive_outside'] + r['first_step_absorbed'] == n
        assert sum(final) + dead + pending == n
        assert all(final[k] == first[k] + parity[0][k] + parity[1][k] for k in range(3))
        assert returned + pending == r['returned_or_pending']
        assert sum(parity[0]) + pending == r['even_returned_or_pending']
        assert r['first_step_absorbed'] <= dead
        assert r['first_step_alive_outside'] == returned + pending + dead-r['first_step_absorbed']
        hist = r['duration_histogram']
        assert len(hist) == h+1 and hist[0] == 0 and sum(hist) == n
        assert hist[1] == sum(first) + r['first_step_absorbed']
        assert hist[h] >= pending
        assert r['primitive_applications'] == sum(k*x for k, x in enumerate(hist))
        assert r['categorical_observations'] == r['primitive_applications']
        last = r['last_terminal_boundary_or_absorbed_or_pending']
        assert last in (-2, -1, 0, 1, 2)
        assert r['preparations_with_known_boundary_reuse'] == n-final[j]+int(last == j)
        assert r['logical_trials'] == r['fresh_reset_execution_upper_bound'] == n
    for key, value in data['costs'].items():
        assert value == sum(r[key] for r in receipts)
    raw = json.loads((ROOT/'results/ABSORBING_BOUNDARY_RAW_RECEIPTS.json').read_text())
    assert raw['receipts'] == receipts
    return len(receipts)


def review_certificate(data):
    cert, ell = data['certificate'], data['confidence_exponent']
    assert cert['global_source_norm_cap_input'] is None
    checked = 0
    for mode, m in enumerate(cert['modes']):
        records = [next(r for r in data['receipts'] if r['mode'] == mode and r['start_boundary'] == j) for j in range(3)]
        n = records[0]['trials']
        assert all(r['trials'] == n for r in records)
        obs = [r['first_step_boundary_counts'] for r in records]
        t, lo, hi, rad = (m[k] for k in ('model', 'kernel_lower', 'kernel_upper', 'entry_radius'))
        assert t == tr(t) and lo == tr(lo) and hi == tr(hi) and rad == tr(rad)
        for j in range(3):
            for k in range(j, 3):
                x = obs[j][j] if j == k else obs[j][k]+obs[k][j]
                total = n if j == k else 2*n
                assert t[j][k] == F(x, total)
                assert rad[j][k] == max(t[j][k]-lo[j][k], hi[j][k]-t[j][k])
                endpoint(x, total, lo[j][k], ell, 'lower')
                endpoint(x, total, hi[j][k], ell, 'upper')
                checked += 2
        rowrad = []
        for j, r in enumerate(records):
            rl, rh = m['row_mass_intervals'][j]
            endpoint(sum(obs[j]), n, rl, ell, 'lower')
            endpoint(sum(obs[j]), n, rh, ell, 'upper')
            rowrad.append(max(abs(rl-sum(t[j])), abs(rh-sum(t[j]))))
            for countkey, boundkey, side in (
                ('returned_or_pending', 'excursion_return_row_upper', 'upper'),
                ('even_returned_or_pending', 'even_excursion_return_row_upper', 'upper'),
                ('absorbed_before_boundary_return', 'observed_absorption_row_lower', 'lower')):
                endpoint(r[countkey], n, m[boundkey][j], ell, side)
            checked += 5
        ru, eu, al = (m[k] for k in ('excursion_return_row_upper', 'even_excursion_return_row_upper', 'observed_absorption_row_lower'))
        kp = max(min(al), min(1-m['row_mass_intervals'][j][1]-ru[j] for j in range(3)))
        km = min(2*lo[j][j]+al[j] for j in range(3))
        assert kp == m['boundary_schur_plus_lower'] and kp > 0
        assert km == m['boundary_schur_minus_lower'] and km > 0
        local = (1/kp+1/km)/2
        assert local == m['local_boundary_inverse_dissipation_upper']
        q = max(eu)+max(ru)**2*local
        assert q == m['true_galerkin_form_operator_upper']
        delta = max(map(sum, rad))
        assert delta == m['operator_error_upper']
        proposed = m['proposed_form_operator_upper']
        difference = proposed-q-delta*delta*local
        # Certify both enclosing square roots without using floating point.
        assert difference >= 0 and difference**2 >= 4*q*delta*delta*local
        budget = sub(eye(3), mm(t, t))
        assert budget == m['budget'] and psd3(budget) and determinant(budget) > 0
        assert psd3(sub(scale(budget, m['theta_squared']), scale(eye(3), proposed)))
        assert psd3(sub(scale(budget, m['correction_noise_zeta']), scale(eye(3), delta)))
        pi = [[rowrad[j]+sum(rad[j][k] for k in range(3) if k != j) if j == k else -rad[j][k]
               for k in range(3)] for j in range(3)]
        assert pi == m['structured_uncertainty_form']
        assert psd3(sub(scale(budget, m['structured_correction_noise_zeta']), pi))
        rho = max(hi for lo, hi in m['row_mass_intervals'])
        assert rho == m['true_kernel_norm_upper'] and rho < 1
        assert m['robust_galerkin_theta_squared'] == q/(1-rho*rho)
    assert checked == 54
    remainder = 2*max(m['theta_squared'] for m in cert['modes'])
    structured = max(m['structured_correction_noise_zeta'] for m in cert['modes'])
    noise = max(m['correction_noise_zeta'] for m in cert['modes'])
    assert cert['uniform_signed_remainder_bound'] == remainder
    assert cert['uniform_structured_all_word_bound'] == remainder+structured
    assert cert['uniform_all_word_bound'] == remainder+noise
    assert cert['robust_galerkin_uniform_dynamical_bound'] == 2*max(m['robust_galerkin_theta_squared'] for m in cert['modes'])
    return checked


def review_positive_propagation(data):
    cert = data['certificate']
    programs = [x['prediction'] for x in data['program_checks']]
    programs += [data['order_comparison']['program_a'], data['order_comparison']['program_b']]
    for p in programs:
        low = high = [F(j == p['start_boundary']) for j in range(3)]
        for mode in p['word']:
            m = cert['modes'][mode]
            low = vec(m['kernel_lower'], low)
            high = vec(m['kernel_upper'], high)
        expected = [max(F(0), low[p['end_boundary']]), min(F(1), high[p['end_boundary']]+cert['robust_galerkin_uniform_dynamical_bound'])]
        assert expected == p['robust_galerkin_source_interval']
    comp = data['order_comparison']
    a, b = (comp[k]['robust_galerkin_source_interval'] for k in ('program_a', 'program_b'))
    assert comp['robust_galerkin_difference_interval'] == [a[0]-b[1], a[1]-b[0]]
    return len(programs)


def review_direct(data):
    direct = data['direct_endpoint_comparator']
    for r in direct['receipts']:
        n, counts = r['trials'], r['endpoint_boundary_or_outside_counts']
        assert sum(counts) == n and len(counts) == 4
        for p, side in zip(r['confidence_interval'], ('lower', 'upper')):
            endpoint(counts[r['end_boundary']], n, p, data['confidence_exponent'], side)
        assert r['primitive_applications'] == n*len(r['word'])
        assert r['categorical_observations'] == n
        base = n-counts[r['start_boundary']]
        # Current direct receipt omits the final report; the extra bit is bounded.
        assert base <= r['preparations_with_known_boundary_reuse'] <= base+1
    for key, value in direct['costs'].items():
        assert value == sum(r[key] for r in direct['receipts'])
    a, b = (r['confidence_interval'] for r in direct['receipts'])
    assert direct['difference_interval'] == [a[0]-b[1], a[1]-b[0]]
    assert direct['difference_interval'][0] > 0
    low = sum(r['trials']-r['endpoint_boundary_or_outside_counts'][r['start_boundary']] for r in direct['receipts'])
    return 4, [low, low+len(direct['receipts'])]


def minimal_input_replay(data):
    """Execute only inference on boundary counts, with source access disabled."""
    spec = importlib.util.spec_from_file_location('reviewed_absorption_compiler', CODE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    def forbidden(*args, **kwargs):
        raise AssertionError('Inference requested hidden source access')
    module.source_fixture = forbidden
    module.InfiniteAbsorbingInstrument = forbidden
    keys = ('mode', 'start_boundary', 'trials', 'first_step_boundary_counts',
            'returned_or_pending', 'even_returned_or_pending', 'absorbed_before_boundary_return')
    stripped = [{k:r[k] for k in keys} for r in data['receipts']]
    inferred = decode(module.dumpable(module.infer(stripped, F(data['confidence_exponent']))))
    assert inferred == data['certificate']
    return list(keys)


def main():
    data = decode(json.loads(RESULT.read_text()))
    receipts = review_acquisition(data)
    endpoints = review_certificate(data)
    programs = review_positive_propagation(data)
    direct_endpoints, direct_reset_interval = review_direct(data)
    assert endpoints+direct_endpoints == data['confidence_tail_count'] == 58
    ell = data['confidence_exponent']
    exp_lower = sum((F(ell**k, factorial(k)) for k in range(60)), F(0))
    assert F(58)/exp_lower < data['joint_failure_probability_upper'] == F(1, 1000)
    fields = minimal_input_replay(data)
    out = dict(result_sha256=hashlib.sha256(RESULT.read_bytes()).hexdigest(),
        code_sha256=hashlib.sha256(CODE.read_bytes()).hexdigest(),
        exact_confidence_endpoints_checked=endpoints+direct_endpoints,
        acquisition_receipts_exactly_replayed=receipts,
        positive_word_interval_propagations_checked=programs,
        hidden_source_access_disabled_in_inference_replay=True,
        minimal_inference_receipt_fields=fields,
        source_norm_gap_or_hidden_tail_input_required=False,
        acquisition_costs=data['costs'],
        direct_receipt_only_preparation_interval=direct_reset_interval,
        direct_execution_reported_preparations=data['direct_endpoint_comparator']['costs']['preparations_with_known_boundary_reuse'],
        new_trajectories_generated=0, all_reviewed_checks_passed=True)
    path = Path(__file__).with_name('ABSORBING_BOUNDARY_REVIEW_RESULTS.json')
    path.write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    main()
