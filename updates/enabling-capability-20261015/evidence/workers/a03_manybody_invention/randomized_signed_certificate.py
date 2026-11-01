"""Gap-free signed polynomial certificate, as an established-method control.

Target is the exact real matrix of the saved binary64 H entries. Confidence
requires independent unbiased random bits; arithmetic bounds require IEEE
round-to-nearest and the stated dot-product error model. No FCIDUMP bridge.
This is NOT claimed novel: probabilistic Lanczos/Chebyshev spectrum bounds
were already developed by van Dorsselaer, Hochstenbach and van der Vorst.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import math
import os
import time

import numpy as np
from scipy import sparse

BASE = Path(__file__).resolve().parent
SOURCE = BASE.parent / 'computation_search'
UNIT = F(1, 2**53)


def up(value):
    return float(np.nextafter(float(value), np.inf))


def down(value):
    return float(np.nextafter(float(value), -np.inf))


def gamma(k):
    return up(k*UNIT/(1-k*UNIT))


def fup(value):
    """Convert exact Fraction to an outward upper binary64 number."""
    return up(value)


def fnorm_upper(x):
    squared = float(np.sum(x*x))
    squared_upper = up((F(squared)+F(1,10**300))/(1-F(gamma(2*x.size+3))))
    return up(math.sqrt(squared_upper))


def row_sum_upper(x):
    # fsum rounds an exact sum to nearest; a nextafter gives an upper bound.
    return up(math.fsum(abs(float(v)) for v in x))


def chebyshev_u_upper(k, alpha):
    """Exact rational upper bound for U_k(alpha), alpha>=1.

    U_k(1+x)=sum_j binom(k+j+1,2j+1) 2^j x^j. Once term
    ratios decrease below 1/2, bound the uncomputed tail geometrically.
    """
    if k < 0:
        return F(0)
    x = F(alpha)-1
    assert x >= 0
    term = F(k+1)
    total = term
    for j in range(k):
        ratio = 2*x*F((k+j+2)*(k-j), (2*j+3)*(2*j+2))
        if j >= 24 and ratio < F(1, 2):
            return total + term*ratio/(1-ratio)
        term *= ratio
        total += term
    return total


def root_offset_upper(degree, target):
    """Find rational x>=0 with T_degree(1+x)>=target, no transcendentals.

    A positive 12-term Taylor truncation is a lower bound for T. Bisection
    gives an upper endpoint for the truncation's root, hence a valid x.
    """
    target = max(F(1), F(target))
    coeff = [F(1)]
    for j in range(min(12, degree)):
        coeff.append(coeff[-1]*F(degree*degree-j*j, (j+1)*(2*j+1)))
    def poly(x):
        value = F(0)
        for c in reversed(coeff):
            value = value*x+c
        return value
    lo, hi = F(0), F(1)
    while poly(hi) < target:
        hi *= 2
    for _ in range(56):
        mid = (lo+hi)/2
        if poly(mid) >= target:
            hi = mid
        else:
            lo = mid
    assert poly(hi) >= target
    return hi


def main():
    start = time.perf_counter()
    source_file = SOURCE/'hamiltonian.npz'
    H = np.load(source_file)['H']
    common = json.loads((SOURCE/'MATCHED_TARGET.json').read_text())
    benchmark = json.loads((SOURCE/'BENCHMARK.json').read_text())
    upper = float(common['shared_rayleigh_upper'])
    n = len(H)
    off = H.copy(); np.fill_diagonal(off, 0)
    off_rows = np.array([row_sum_upper(row) for row in off])
    diag = np.diag(H)
    lower = min(down(F(float(a))-F(float(b))) for a,b in zip(diag,off_rows))
    ceiling = max(up(F(float(a))+F(float(b))) for a,b in zip(diag,off_rows))
    hnorm = max(row_sum_upper(row) for row in H)
    initial_lower = lower
    c, s = (ceiling+upper)/2, (ceiling-upper)/2
    C = H/s
    C[np.diag_indices(n)] -= c/s
    # Relation H=s*C+c*I+R, with the division/subtraction errors included.
    bridge = up(F(gamma(4))*(F(hnorm)+abs(F(c)))+F(1,10**300))
    assert np.array_equal(C, C.T)
    csr = sparse.csr_matrix(C)
    cnorm = max(row_sum_upper(row) for row in C)
    max_nnz = int(np.diff(csr.indptr).max())
    probes, q = 48, F(1,4)
    random_path = BASE/'random_probe_bits.bin'
    if random_path.exists():
        raw = random_path.read_bytes()
    else:
        raw = os.urandom((n*probes+7)//8)
        random_path.write_bytes(raw)
    assert len(raw) == (n*probes+7)//8
    bits = np.unpackbits(np.frombuffer(raw, dtype=np.uint8))[:n*probes]
    G = (2*bits.astype(float)-1).reshape(n,probes)
    setup_seconds = time.perf_counter()-start
    assert np.all((G == 1) | (G == -1))
    # Paley-Zygmund: P(|u^T r|>=1/4)>=75/256 for any fixed unit u.
    # Thus the Frobenius-projection event fails with at most (181/256)^r.
    failure = F(181,256)**probes
    dot_gamma = gamma(2*max_nnz+2)
    def dot_error(x):
        return up(F(dot_gamma)*F(cnorm)*F(fnorm_upper(x))+F(1,10**300))
    prev = G
    current = csr @ G
    initial_error = dot_error(G)
    max_local_error = 0.
    rows = []
    recurrence_start = time.perf_counter()
    checkpoints = {8,16,32,64,128,256,512,1024}
    certification_seconds = 0.
    for degree in range(1,1025):
        if degree in checkpoints:
            tc = time.perf_counter()
            lo_c = (F(lower)-F(c)-F(bridge))/F(s)
            hi_c = (F(ceiling)-F(c)+F(bridge))/F(s)
            alpha = up(max(F(1),abs(lo_c),abs(hi_c)))
            error = F(initial_error)*chebyshev_u_upper(degree-1, alpha)
            if degree >= 2:
                error += F(max_local_error)*(degree-1)*chebyshev_u_upper(degree-2, alpha)
            error_upper = fup(error)
            measured_upper = fnorm_upper(current)
            norm_upper = up(F(measured_upper)+F(error_upper))
            offset = root_offset_upper(degree, F(norm_upper)/q)
            new_lower = down(F(c)-F(s)*(1+offset)-F(bridge))
            lower = max(lower,new_lower)
            certification_seconds += time.perf_counter()-tc
            rows.append({
                'degree':degree, 'matrix_vector_equivalent_calls':degree*probes,
                'lower':lower,'upper':upper,'interval_width':up(F(upper)-F(lower)),
                'recurrence_error_frobenius_upper':error_upper,
                'observed_norm_upper':measured_upper,'alpha_norm_bound':alpha,
                'elapsed_recurrence_and_certification_seconds':time.perf_counter()-recurrence_start,
                'certification_seconds_cumulative':certification_seconds,
            })
            print(json.dumps(rows[-1]),flush=True)
        if degree == 1024:
            break
        z = csr @ current
        new = 2*z-prev
        local = up(2*F(dot_error(current)) + UNIT/(1-UNIT)*(2*F(fnorm_upper(z))+F(fnorm_upper(prev)))+F(1,10**300))
        max_local_error = max(max_local_error,local)
        prev,current = current,new
    output = {
        'status':'conditional_probabilistic_binary64_H_certificate; established method control; no enabling advantage',
        'target':'same finite-basis N2 Ag determinant compression as computation_search',
        'source_matrix_sha256':hashlib.sha256(source_file.read_bytes()).hexdigest(),
        'source_matched_target_sha256':hashlib.sha256((SOURCE/'MATCHED_TARGET.json').read_bytes()).hexdigest(),
        'source_benchmark_sha256':hashlib.sha256((SOURCE/'BENCHMARK.json').read_bytes()).hexdigest(),
        'random_bits_sha256':hashlib.sha256(raw).hexdigest(),
        'random_source':'os.urandom; confidence assumes independent unbiased bits, not established by their hash',
        'random_bits_reused_on_replay':True,
        'probes':probes,'projection_threshold_exact':str(q),
        'failure_probability_exact':str(failure), 'failure_probability_upper':up(failure),
        'confidence_not_union_bounded':'same fixed ground-vector projection event covers all degrees and adaptive prior lower bounds',
        'arithmetic_assumptions':['IEEE binary64 round-to-nearest with gradual underflow','CSR dot products obey gamma_(2 max_nnz+2)','no overflow; explicit 1e-300 allowances dominate aggregate underflow for these array dimensions','fsum faithfully rounded and sqrt correctly rounded'],
        'matrix_dimension':n,'matrix_nonzeros':int(csr.nnz),'maximum_row_nonzeros':max_nnz,
        'initial_Gershgorin_lower':initial_lower,'Gershgorin_upper':ceiling,
        'matrix_scaling_bridge_norm_upper':bridge,
        'setup_seconds':setup_seconds,
        'rows':rows,
        'shared_costs':{
            'source_full_matrix_acquisition_seconds':benchmark['full_matrix_acquisition']['wall_seconds'],
            'literal_source_reference_vector_producer_seconds':benchmark['incumbent_fci'][0]['wall_seconds'],
            'fastest_FCI_run_seconds':benchmark['incumbent_fci'][1]['wall_seconds'],
            'cost_provenance_note':'At time of audit reference_vector.npy came from pspace400, not the faster pspace0 run. Charge literal producer unless computation_search saves a new matched fast vector.',
            'source_rigorous_upper_check_seconds':common['shared_rayleigh_upper_seconds'],
            'exact_FCIDUMP_to_H_bridge':'not included here; s05 provides it separately',
        },
        'equally_informed_incumbent':{
            'kind':'retained FCI vector plus one-shot signed Schur256',
            'certificate_seconds':common['rows'][1]['wall_seconds'],
            'width':common['rows'][1]['width'],
            'note':'source timing measured by computation_search; shared acquisition/upper costs additionally charged to both'
        },
        'elapsed_code_seconds':time.perf_counter()-start,
        'memory_scope':'full H and dense C plus 48 determinant-length probes; not a compressed many-body representation',
        'inference_tokens_cost_energy':'UNKNOWN; code elapsed is separate',
        'novelty':'Known randomized polynomial spectral certification; no novelty claimed',
    }
    (BASE/'RANDOMIZED_SIGNED_CERTIFICATE.json').write_text(json.dumps(output,indent=2)+'\n')


if __name__ == '__main__':
    main()
