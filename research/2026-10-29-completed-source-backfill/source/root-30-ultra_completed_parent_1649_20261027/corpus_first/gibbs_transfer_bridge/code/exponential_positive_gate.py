"""Distinct exact-exponential positive factor and closed-loop orientation checks.

The 25-term matrix-unit factorization is not the nine-term quadratic gate.
Floating checks replay the analytic nonnegative factor and network identity;
they are not directed interval bounds for the cold Gibbs partition function.
"""
import sys
sys.dont_write_bytecode = True
import json, time
import numpy as np
from scipy.linalg import expm
from positive_gate import BASE, spin
from positive_transfer import physical_trace


def exponential_factors(delta):
    h = np.array(spin()[-1], dtype=float)
    # 4I-h is entrywise nonnegative, so its exponential is nonnegative.
    G = np.exp(-4*delta)*expm(delta*(4*np.eye(25)-h))
    L, R = [], []
    tensor = G.reshape(5, 5, 5, 5)
    for ap in range(5):
        for a in range(5):
            left = np.zeros((5, 5)); left[ap, a] = 1
            L.append(left); R.append(tensor[ap, :, a, :])
    L, R = np.array(L), np.array(R)
    recovered = np.einsum('rij,rkl->ikjl', L, R).reshape(25, 25)
    assert np.max(np.abs(recovered-G)) < 1e-14
    assert np.min(G) >= 0 and np.min(R) >= 0
    return L, R, G


def kernel(a, N):
    p = len(a); local = np.einsum('aij,bjk->abik', a, a)
    if N == 1:
        return np.trace(local, axis1=2, axis2=3).T
    if N == 2:
        return np.einsum('axij,byji->xyab', local, local,
                         optimize=True).reshape(p*p, p*p)
    raise ValueError(N)


def run():
    start = time.monotonic(); rows = []
    for delta in (.001, 64/589043):
        L, R, G = exponential_factors(delta)
        for N in (1, 2):
            KL, KR = kernel(L, N), kernel(R, N)
            T = KL@KR.T
            assert np.min(T) >= 0
            loop = float(np.trace(T@T))
            physical = physical_trace(G, 4, N)
            rel = abs(loop-physical)/physical
            assert rel < 1e-12
            rows.append(dict(delta=delta, time_slices=N, beta=N*delta,
                             factor_terms=25, history_dimension=25**N,
                             four_site_Z=loop,
                             direct_closed_relative_difference=rel,
                             minimum_transfer_entry=float(T.min())))
    result = dict(
        status='EXACT_EXPONENTIAL_POSITIVE_FACTOR_AND_PERIODIC_NETWORK_IDENTITY',
        analytic_factor='L_(a_prime,a)=E_(a_prime,a); R=G[a_prime,:,a,:]',
        positivity_proof='G=exp(-4 delta) exp(delta(4I-h_M)); 4I-h_M>=0 entrywise',
        exact_operator_schmidt_rank_for_delta_positive=25,
        rank_reason='The CP exponential has positive coefficients for every generator word; irreducible spin generators generate the full matrix algebra, so its Choi Gram matrix is positive definite.',
        distinct_quadratic_terms=9,
        exact_exponential_slices_from_peer_not_rederived=589043,
        rows=rows, elapsed_seconds=time.monotonic()-start,
        scope='All-size algebraic trace identity; finite numeric orientation replays only. No long-ring compression, cold trace, or purity certificate.')
    (BASE/'results/EXPONENTIAL_POSITIVE_GATE.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    run()
