#!/usr/bin/env python3
"""Bounded exact actual-model first-slab audit; no propagation or solver.

NPZ containers are inspected before np.load(..., allow_pickle=False). Exact
dyadic endpoint coefficients and literal core support determine success.
All probabilistic comparisons use Fraction; floats are display only.
"""
import hashlib
import json
import math
import os
from pathlib import Path
import resource
import sys
import time
import zipfile
from fractions import Fraction as F

os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
os.environ.setdefault('OMP_NUM_THREADS', '1')
import numpy as np
if hasattr(sys,'set_int_max_str_digits'):
    sys.set_int_max_str_digits(100000)

BASE = Path(__file__).resolve().parents[2]
PACKET = BASE / 'originals/kinetic/schlogl_first_slab_packet'
OUT = Path(__file__).resolve().parent
sys.path.insert(0,str(PACKET/'verification'))
import verify_slab as v
H = F(1, 10000)
DIFF = F('8.2207')
EDGES = [(0,1),(1,2),(2,3),(4,5),(5,6),(6,7),(0,4),(1,5),(2,6),(3,7)]

def birth(n):
    return F('2.676')*n*(n-1)+F('108.102')

def death(n):
    return F('0.040')*n*(n-1)*(n-2)+F('37.881')*n

def jfrac(x):
    return {'exact': str(x), 'approximate': float(x)}

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

# exp(1) < sum_{j=0}^{20}1/j! + (1/21!)/(1-1/22).
# Each subsequent factorial denominator ratio is at most 1/22.
E_UPPER = sum((F(1, math.factorial(j)) for j in range(21)), F(0)) + F(22,21*math.factorial(21))
assert F(2) < E_UPPER < F('2.718281828459046')

def poisson_chernoff_upper(mu, k):
    assert 0 < mu < k
    # Markov applied to (k/mu)^N: exp(k-mu)*(mu/k)^k.
    # k-floor(mu) is the ceiling of k-mu, so e_upper to this integer
    # power is a rational upper bound for the exponential factor.
    return E_UPPER**(k-(mu.numerator//mu.denominator)) * (mu/F(k))**k

def stopped_target_upper(U):
    assert 50 <= U <= 161
    deg = max(sum(i in edge for edge in EDGES) for i in range(8))
    assert deg == 3
    up = (birth(U) + deg*DIFF*U)*H
    deaths = 8*death(U)*H
    return {
        'U': U, 'up_jumps_required': U-49, 'death_jumps_required': 280,
        'up_mean': jfrac(up), 'death_mean': jfrac(deaths),
        'target_upper': jfrac(8*poisson_chernoff_upper(up,U-49)+poisson_chernoff_upper(deaths,280)),
    }

def inspect_candidate(relative, initial_basis, has_product):
    path = PACKET / relative
    manifest_path = path.with_suffix('.json')
    manifest = json.loads(manifest_path.read_text())
    assert manifest['h'] == '0.0001' and F(manifest['t_start']) == 0
    assert manifest['cap'] == 162 and manifest['target_max'] == 15
    assert manifest['semantics'] == 'frozen_target_grid_plus_overflow'
    assert manifest['anchored_chebyshev']
    assert sorted(manifest['order']) == list(range(8))
    assert set(map(tuple, manifest['physical_edges'])) == set(EDGES)
    with zipfile.ZipFile(path) as container:
        infos = container.infolist()
        assert len({x.filename for x in infos}) == len(infos)
        assert all(x.filename.endswith('.npy') and '/' not in x.filename for x in infos)
        assert sum(x.file_size for x in infos) < 70*1024**2
        assert max(x.file_size for x in infos) < 2*1024**2
        npz_size = sum(x.file_size for x in infos)
    with np.load(path, allow_pickle=False) as z:
        coeff = z['time_coefficients']
        initial = z['initial_coefficients']
        overflow = z['overflow_coefficients']
        assert coeff.dtype == np.float64 and coeff.shape[1] == 33
        assert np.isfinite(coeff).all() and np.all(coeff[:,0] == 0)
        assert np.array_equal(initial, np.eye(len(initial))[initial_basis])
        assert float(z['initial_overflow']) == 0 and overflow[0] == 0
        product_mass = F(1) if has_product else F(0)
        product_total = F(1) if has_product else F(0)
        product_inside = F(1) if has_product else F(0)
        mass = v.RI.exact(0)
        contractor = v.DecimalContractor(80)
        support_min, support_max = 163, -1
        target_zero_bases = 0
        for j in range(len(initial)):
            last = 1
            cores = []
            for i in range(8):
                core = z[f'basis_{j}_core_{i}']
                cores.append(core)
                assert core.dtype == np.float64 and np.isfinite(core).all()
                assert core.shape[:2] == (last, 163)
                last = core.shape[2]
                if j == initial_basis:
                    assert core.shape == (1,163,1)
                    assert np.array_equal(core[0,:,0],np.eye(163)[50])
                if has_product and j == 0:
                    assert core.shape == (1,163,1)
                    product_mass *= sum((F.from_float(float(x)) for x in core[0,:16,0]), F(0))
                    product_total *= sum((F.from_float(float(x)) for x in core[0,:,0]), F(0))
                    product_inside *= sum((F.from_float(float(x)) for x in core[0,38:63,0]), F(0))
                else:
                    assert not np.any(core[:,:39,:]) and not np.any(core[:,62:,:])
                    nz = np.flatnonzero(np.any(core != 0,axis=(0,2)))
                    if len(nz):
                        support_min = min(support_min,int(nz[0]))
                        support_max = max(support_max,int(nz[-1]))
            assert last == 1
            endpoint_j = F.from_float(float(initial[j])) + 2*sum((F.from_float(float(coeff[j,k])) for k in range(1,33,2)), F(0))
            mass = mass + contractor.functional(cores)*endpoint_j
            if not has_product or j != 0:
                target_zero_bases += 1
        if has_product:
            # Anchoring: T_k(1)-(-1)^k is two for odd k and zero otherwise.
            endpoint_coefficient = F.from_float(float(initial[0])) + 2*sum((F.from_float(float(coeff[0,k])) for k in range(1,33,2)), F(0))
            success = endpoint_coefficient * product_mass
        else:
            success = F(0)
            assert not np.any(overflow)
        endpoint_overflow = 2*sum((F.from_float(float(overflow[k])) for k in range(1,33,2)), F(0))
        mass = mass + endpoint_overflow
        outside = endpoint_coefficient*(product_total-product_inside)+endpoint_overflow if has_product else F(0)
        mup = (birth(62)+3*DIFF*62)*H
        mum = (death(62)+3*DIFF*62)*H
        tail = lambda mu: mu**13/F(math.factorial(13))/(1-mu/14)
        true_outside = 8*(tail(mup)+tail(mum))
        mass_defect = (mass-v.RI.exact(1)).abs_upper()
        state_error = max(F(0),2*(outside-true_outside)-mass_defect)
    return {
        'path': relative, 'npz_sha256': digest(path),
        'uncompressed_bytes': npz_size,
        'literal_nonproduct_core_support': [support_min,support_max],
        'target_zero_bases': target_zero_bases,
        'target_endpoint': jfrac(success),
        'outside_localization_box_plus_overflow_endpoint':jfrac(outside),
        'true_outside_localization_box_upper':jfrac(true_outside),
        'outward_augmented_mass_interval':{'lower':jfrac(mass.lo),'upper':jfrac(mass.hi)},
        'mass_defect_absolute_upper':jfrac(mass_defect),
        'balanced_witness_actual_state_error_lower':jfrac(state_error),
        'target_identically_zero_for_entire_polynomial': not has_product,
        'initial_augmented_state_exact_delta': True,
        'npz_pickle_allowed': False,
        'mass_contraction_helper':'Read-only packet verification/verify_slab.py DecimalContractor, directed 80-digit arithmetic; no candidate solver imported',
    }

def main():
    t0 = time.monotonic()
    try:
        resource.setrlimit(resource.RLIMIT_AS,(512*1024**2,512*1024**2))
        as_limit = '512 MiB hard RLIMIT_AS installed'
    except (ValueError,OSError) as exc:
        as_limit = 'Host rejected RLIMIT_AS: '+str(exc)+'; bounded inspected NPZ sizes and sequential loads used instead'
    resource.setrlimit(resource.RLIMIT_CPU,(120,121))
    records = [stopped_target_upper(u) for u in range(128,138)]
    best = min(records,key=lambda x:F(x['target_upper']['exact']))
    bound = F(best['target_upper']['exact'])
    assert bound < F(1,10**67)
    candidates = [
        inspect_candidate('experiments/candidate.npz',1,True),
        inspect_candidate('experiments/weighted_repair/candidate.npz',1,True),
        inspect_candidate('experiments/constrained_test/candidate.npz',0,False),
    ]
    for candidate, saved in zip(candidates[:2],['verification/tail_rejection.json','verification/weighted_rejection.json']):
        old = json.loads((PACKET/saved).read_text())['endpoint_success']
        assert F(old['lower']['exact']) <= F(candidate['target_endpoint']['exact']) <= F(old['upper']['exact'])
    for candidate, saved in zip(candidates[:2],['verification/original_balanced_rejection.json','verification/weighted_rejection.json']):
        old=json.loads((PACKET/saved).read_text())
        assert candidate['true_outside_localization_box_upper']['exact'] == old['true_probability_outside_box_or_overflow_upper']['exact']
        assert candidate['mass_defect_absolute_upper']['exact'] == old['mass_defect_absolute_upper']['exact']
        assert candidate['balanced_witness_actual_state_error_lower']['exact'] == old['actual_augmented_state_l1_error_lower_balanced_witness']['exact']
    original_error = F(candidates[0]['target_endpoint']['exact']) - bound
    assert original_error > F('5.5537378340734e-10')
    assert original_error < F('1e-9')
    assert original_error > F('2.43093157255213e-10')
    # Actual same-total states near the target distinguish the backward goal.
    # b=(15,...,15) is frozen; c=(16,15,...,15,14) is continuing, both S=120.
    c = (16,15,15,15,15,15,15,14)
    assert sum(c) == 120 and max(c) == 16
    exit_c = sum((birth(n)+death(n) for n in c),F(0)) + DIFF*sum(c[i]+c[j] for i,j in EDGES)
    delta = F('0.000001')
    # No jump has probability e^(-lambda*delta) >= 1-lambda*delta.
    contrast = 1-exit_c*delta
    assert contrast > F('0.98')
    # Both continuation states have S=120, so separate target overwriting
    # does not rescue a total-count-only approximate backward weight.
    far = (120,0,0,0,0,0,0,0)
    assert sum(far) == sum(c) and max(far) > 15
    c_success_lower = death(16)*H/E_UPPER**math.ceil(exit_c*H)
    far_down_mean = (death(162)+3*DIFF*162)*H
    far_success_upper = poisson_chernoff_upper(far_down_mean,105)
    continuation_contrast = c_success_lower-far_success_upper
    assert continuation_contrast > F('0.01')
    result = {
        'status': 'PASS_BOUNDED_EXACT_ACTUAL_TARGET_AND_SUPPORT_AUDIT',
        'scope': 'Original exact eight-site first-hit model, first slab h=1e-4 only; no endpoint-T1 propagation or full solver.',
        'pin': '9dbe934e5475f415c2d160a6c0715534aafa546b',
        'e_upper': jfrac(E_UPPER), 'tested_scalar_U_values': records,
        'best_stopped_target_upper': best,
        'unbounded_and_cap162_target_probability_both_bounded': True,
        'candidates': candidates,
        'original_actual_first_slab_target_error_lower': jfrac(original_error),
        'original_error_exceeds_generous_1e9_budget': False,
        'original_error_exceeds_cap_subtracted_2431e10_budget': True,
        'weighted_nonzero_target_error_magnitude_not_established': True,
        'constrained_true_target_probability_strictly_positive': 'A finite death-only path from all50 to all15 has positive probability before h; no numerical lower bound acquired.',
        'actual_same_total_adjoint_contrast': {
            'target_state':[15]*8, 'continuing_state':list(c), 'total':120,
            'remaining_time':str(delta), 'continuing_state_exit_rate':jfrac(exit_c),
            'backward_weight_target_minus_continuing_lower':jfrac(contrast),
            'proof':'The target weight is one; no jump from the continuing state precludes success, so its success weight is at most lambda*delta.'
        },
        'actual_same_total_continuation_adjoint_contrast': {
            'near_state':list(c), 'far_state':list(far), 'total':120,
            'remaining_time':str(H), 'model':'Exact cap162 augmented first-hit chain',
            'near_success_lower':jfrac(c_success_lower),
            'far_coordinate_down_jumps_required':105,
            'far_coordinate_down_count_mean_upper':jfrac(far_down_mean),
            'far_success_upper':jfrac(far_success_upper),
            'backward_weight_near_minus_far_lower':jfrac(continuation_contrast),
            'total_count_only_uniform_backward_error_lower':jfrac(continuation_contrast/2),
            'target_overwrite_does_not_distinguish_these_states':True,
        },
        'candidate_solvers_executed':False, 'SSA_events':0,
        'memory_limit_status':as_limit,
        'cpu_limit_seconds':120,
        'elapsed_seconds':time.monotonic()-t0,
        'peak_rss_raw':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
    }
    (OUT/'actual_target_checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({
        'status':result['status'], 'best_U':best['U'], 'target_upper':float(bound),
        'candidate_targets':[x['target_endpoint']['approximate'] for x in candidates],
        'original_target_error_lower':float(original_error),
        'same_total_backward_contrast_lower':float(contrast),
        'elapsed_seconds':result['elapsed_seconds'],
    },indent=2))

if __name__ == '__main__':
    main()
