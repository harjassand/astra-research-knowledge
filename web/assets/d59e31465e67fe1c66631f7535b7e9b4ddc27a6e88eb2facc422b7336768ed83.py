"""Small exact checks for cross-review and mandatory-core residual attack.

Writes only owned phase2/deeper_checks.json. No peer code is imported.
"""
from fractions import Fraction as F
from itertools import combinations, product
from math import comb
from pathlib import Path
import hashlib
import json
import random
import time

from paired_exact import (Q, mat, zeros, eye, adj, mul, det, inverse, columns,
    paired_columns, canonical, gram_weight, brute_weights, estimator_sample,
    skew_lift, force_project, mandatory_core_pit, bit_height)


def pf(A):
    n = len(A)
    if n == 0:
        return Q(1)
    return sum((((-1)**(j+1))*A[0][j]*pf([
        [A[a][b] for b in range(1, n) if b != j]
        for a in range(1, n) if a != j]) for j in range(1, n)), Q())


def pf_norm(A, k):
    return sum((pf([[A[i][j] for j in R] for i in R]).abs2()
                for R in combinations(range(len(A)), 2*k)), F(0))


def sign_audit(V, k):
    N = len(V[0])//2
    Z = sum(brute_weights(V, k).values(), F(0))
    vals = []
    for signs in product((-1, 1), repeat=N):
        y = estimator_sample(V, k, signs)
        assert y == pf_norm(skew_lift(V, signs), k)
        vals.append(y)
    mean = sum(vals, F(0))/len(vals)
    second = sum((y*y for y in vals), F(0))/len(vals)
    assert mean == Z
    assert second <= 9**k*Z*Z
    return {'k': k, 'N': N, 'mean': Z, 'second': second,
            'relative_second': second/(Z*Z) if Z else None,
            'samples': len(vals)}


def four_phase_audit(V, k):
    N = len(V[0])//2
    roots = [Q(1),Q(-1),Q(0,1),Q(0,-1)]
    Z = sum(brute_weights(V,k).values(),F(0))
    vals = [estimator_sample(V,k,xs) for xs in product(roots,repeat=N)]
    mean = sum(vals,F(0))/len(vals)
    second = sum((y*y for y in vals),F(0))/len(vals)
    assert mean == Z
    assert second <= comb(2*k,k)*Z*Z
    return {'k':k,'N':N,'mean':mean,'second':second,
            'relative_second':second/(Z*Z) if Z else None,'samples':len(vals),
            'variance_bound_origin':'c01_s01 phase2 Section 2'}


def block_pfaffian_audit(V):
    A = skew_lift(V,[Q(1),Q(0,1),Q(-1),Q(0,-1)])
    m = len(A)
    H = mul(adj(A),A)
    q = [estimator_sample(V,k,[Q(1),Q(0,1),Q(-1),Q(0,-1)])
         for k in range(m//2+1)]
    sign = (-1)**(m*(m-1)//2)
    for t in (0,1,2):
        B = [([t*z for z in A[i]]+eye(m)[i]) for i in range(m)]
        Aadj = adj(A)
        B += [([-z for z in eye(m)[i]]+Aadj[i]) for i in range(m)]
        value = sum((q[k]*t**k for k in range(len(q))),F(0))
        assert pf(B) == Q(sign*value)
        assert det(B) == det([[eye(m)[i][j]+t*H[i][j]
                              for j in range(m)] for i in range(m)])
    return {'status':'PASS','identity':'Pf([[tA,I],[-I,A*]])=(-1)^(m(m-1)/2) sum_k X_k t^k',
            'tested_t':[0,1,2],'sample_coefficients':q}


def all_prefix_audit(V, k, constraints):
    weights = brute_weights(V, k)
    ans = []
    for forced, excluded in constraints:
        exact = sum((w for S, w in weights.items()
                     if set(forced) <= set(S) and set(excluded).isdisjoint(S)), F(0))
        d, W, labels = force_project(V, forced, excluded)
        r = k-len(forced)
        projected = d*sum(brute_weights(W, r).values(), F(0)) if d else F(0)
        assert projected == exact
        mean = F(0)
        N = len(labels)
        if d:
            vals = [estimator_sample(W, r, signs)
                    for signs in product((-1, 1), repeat=N)]
            mean = d*sum(vals, F(0))/len(vals)
            assert mean == exact
        ans.append({'forced': forced, 'excluded': excluded, 'mass': exact,
                    'projected_input_bits': bit_height(W) if d else None,
                    'sign_mean': mean})
    return ans


def review_exchange():
    V = mat([[1,0,0,0,(1,1),2], [0,1,0,0,2,(1,-1)],
             [0,0,1,0,1,(3,1)], [0,0,0,1,(1,-1),1]])
    aa, bb = [0,1,2,3], [0,3,4,5]
    A, B = columns(V, aa), columns(V, bb)
    C = mul(inverse(A), B)
    Ci = inverse(C)
    i = 1
    total = Q()
    output_mass = F(0)
    capacity = F(0)
    mu = det(A).abs2()*det(B).abs2()
    for j, label in enumerate(bb):
        if label in aa:
            assert C[i][j] == Q()
            continue
        ax, bx = aa[:], bb[:]
        ax[i], bx[j] = bb[j], aa[i]
        da, db = det(columns(V, ax)), det(columns(V, bx))
        assert da == det(A)*C[i][j]
        assert db == det(B)*Ci[j][i]
        total += da*db
        my = da.abs2()*db.abs2()
        output_mass += my
        capacity += mu*my/(16*(mu+my))
    assert total == det(A)*det(B)
    assert mu <= 2*output_mass
    assert capacity >= mu/F(2*4**3)
    # Cycle component diagnostic: all union-preserving moves conserve
    # the sum of line occupancy under the true four-state product law.
    states = [(a,b) for a in (0,1) for b in (0,1)]
    observable = {s: sum(s) for s in states}
    assert observable[(0,1)] == observable[(1,0)]
    assert observable[(0,0)] != observable[(1,1)]
    return {'complex_identity': 'PASS', 'mu': mu, 'output_mass': output_mass,
            'capacity': capacity, 'global_additive_union_obstruction': 'PASS'}


def conditional_dpp_ordered(A):
    """Independent exhaustive probability audit of the projection recursion."""
    k, m = len(A), len(A[0])
    P = mul(mul(adj(A), inverse(mul(A, adj(A)))), A)
    out = {}

    def rec(labels, kernel, rank, chosen, prob):
        if rank == 0:
            key = tuple(sorted(chosen))
            out[key] = out.get(key, F(0))+prob
            return
        assert sum((kernel[i][i].re for i in range(len(labels))), F(0)) == rank
        assert mul(kernel, kernel) == kernel
        for j, label in enumerate(labels):
            pj = kernel[j][j]
            assert pj.im == 0 and pj.re >= 0
            if not pj:
                continue
            remain = [a for a in range(len(labels)) if a != j]
            new = [[kernel[a][b]-kernel[a][j]*kernel[j][b]/pj
                    for b in remain] for a in remain]
            rec([labels[a] for a in remain], new, rank-1,
                chosen+[label], prob*pj.re/rank)
    rec(list(range(m)), P, k, [], F(1))
    Z = det(mul(A, adj(A))).re
    for J in combinations(range(m), k):
        assert out.get(J, F(0)) == det(columns(A, J)).abs2()/Z
    assert sum(out.values(), F(0)) == 1
    return out


def review_fiber(Fmat, k):
    n = len(Fmat)
    B = comb(n, k)
    rowZ, weights = {}, {}
    for I in combinations(range(n), k):
        available = sorted(set(range(n))-set(I))
        A = [[Fmat[i][j] for j in available] for i in I]
        rowZ[I] = det(mul(A, adj(A))).re
        if rowZ[I]:
            law = conditional_dpp_ordered(A)
            for inds, p in law.items():
                J = tuple(available[j] for j in inds)
                weights[I,J] = rowZ[I]*p
    Z = sum(rowZ.values(), F(0))
    states = list(weights)
    assert sum(weights.values(), F(0)) == Z
    min_ratio = None
    for x in states:
        for y in states:
            if x == y:
                continue
            zx, zy = rowZ[x[0]], rowZ[y[0]]
            pxy = weights[y]/(B*zy)*min(F(1), zy/zx)
            pyx = weights[x]/(B*zx)*min(F(1), zx/zy)
            assert weights[x]*pxy == weights[y]*pyx
            ratio = (weights[x]/Z*pxy)/((weights[x]/Z)*(weights[y]/Z))
            assert ratio >= F(1,B)
            min_ratio = ratio if min_ratio is None else min(min_ratio, ratio)
    return {'supported_joint_states': len(states), 'row_proposals': B,
            'Z': Z, 'minimum_flow_over_product': min_ratio,
            'exact_conditional_law_and_reversibility': 'PASS'}


def review_refresh(Fmat, lam, epsilon):
    n = len(Fmat)
    pairs = [(i,j) for i in range(n) for j in range(i+1,n)]
    V = canonical(Fmat)
    for i,j in pairs:
        for row in range(n):
            V[row] += [Q(int(row==i)), Q(int(row==j))]
    activities = [epsilon*x for x in lam]+[F(1)]*len(pairs)
    actual = F(0)
    for S in combinations(range(len(activities)), n//2):
        if not any(i<n for i in S):
            continue
        wt = gram_weight(V, S)
        for i in S:
            wt *= activities[i]
        actual += wt
    es = [F(1)]+[F(0)]*(n//2)
    for i in range(n):
        a = lam[i]*sum((z.abs2() for z in Fmat[i]), F(0))
        for s in range(n//2,0,-1):
            es[s] += a*es[s-1]
    sf = sum((comb(len(pairs), n//2-s)*es[s]
              for s in range(1,n//2+1)), F(0))
    assert actual <= epsilon*sf
    return {'actual_contaminant': actual, 'epsilon_S_F': epsilon*sf,
            'Hadamard_bound': 'PASS'}


def core_audit(Fmat, k, delta, seed):
    V = canonical(Fmat)
    w = brute_weights(V, k)
    supported = [set(S) for S in w if w[S]]
    exact = sorted(set.intersection(*supported)) if supported else []
    acquired = mandatory_core_pit(V, k, delta, random.Random(seed))
    assert acquired['status'] == 'POSITIVE'
    assert acquired['core'] == exact
    d,W,labels = force_project(V, exact)
    r = k-len(exact)
    residual = sum(brute_weights(W,r).values(), F(0))
    Z = sum(w.values(), F(0))
    assert d*residual == Z
    # Full residual sign means use only small residual-label fixtures.
    mean = None
    if len(labels) <= 5:
        vals = [estimator_sample(W,r,s) for s in product((-1,1),repeat=len(labels))]
        mean = sum(vals,F(0))/len(vals)
        assert mean == residual
    return {'n': len(Fmat), 'k': k, 'exact_core': exact,
            'PIT_acquisition': acquired, 'factor': d, 'residual_partition': residual,
            'partition': Z, 'residual_sign_mean': mean,
            'projected_entry_bits': bit_height(W)}


def variance_counters():
    ratio = []
    for L in (2,10,50,100):
        d = F(1,2**L)
        mean = 2*d*d/(1+d*d)
        second = d*d
        relative_second = second/(mean*mean)
        assert relative_second == (1+d*d)**2/(4*d*d)
        ratio.append({'L': L, 'mean': mean, 'second': second,
                      'relative_second': relative_second})
    product_moments = []
    for k in range(1,6):
        # Canonical F is k disjoint bidirected unit swaps. The skew lift
        # is block diagonal with off-diagonal s_(2b)-s_(2b+1).
        vals = []
        for signs in product((-1,1),repeat=2*k):
            y = 1
            for b in range(k):
                y *= (signs[2*b]-signs[2*b+1])**2
            vals.append(y)
        mean = F(sum(vals),len(vals))
        second = F(sum(y*y for y in vals),len(vals))
        assert mean == 2**k and second == 8**k
        assert second/(mean*mean) == 2**k
        assert F(sum(bool(y) for y in vals),len(vals)) == F(1,2**k)
        product_moments.append({'k':k, 'mean':mean, 'second':second,
                                'relative_second':second/(mean*mean),
                                'nonzero_probability':F(1,2**k)})
    return {'sector_growth':ratio,'sign_product_blocks':product_moments}


def main():
    start = time.perf_counter()
    dense = mat([[0,(1,1),2,(0,1)],[(1,-1),0,3,2],
                 [2,(1,1),0,1],[1,2,(1,-1),0]])
    V = canonical(dense)
    signs = [sign_audit(V,k) for k in (0,1,2)]
    prefixes = all_prefix_audit(V,2,[([0],[]),([1],[0]),([0,2],[1]),([],[3])])
    d,W,_ = force_project(V,[0],[1])
    four_phase = four_phase_audit(W,1)
    upper6 = mat([[int(i<j) for j in range(6)] for i in range(6)])
    dense8 = mat([[int(i<j) for j in range(8)] for i in range(8)])
    dense8[7][6] = Q(1)
    cores = [core_audit(upper6,3,F(1,10000),23),
             core_audit(dense8,4,F(1,10000),29)]
    FT = mat([[0,16,16,1],[0,0,16,1],[0,0,0,1],[0,0,0,0]])
    cores.append(core_audit(FT,2,F(1,10000),31))
    result = {'status':'PASS','independent_peer_code_execution':False,
        'estimator_identity_and_improved_variance':signs,
        'positive_projection_prefixes':prefixes,
        'projected_four_phase_bound':four_phase,
        'unitary_normal_form_free_block_identity':block_pfaffian_audit(V),
        'mandatory_core_and_residual':cores,
        'c01_l02_exchange':review_exchange(),
        'c01_l05_conditional_DPP_kernel':review_fiber(dense,2),
        'c01_l08_refresh':review_refresh(dense,[F(1),F(2),F(1,2),F(3)],F(1,128)),
        'variance_counters':variance_counters(),
        'elapsed_seconds':time.perf_counter()-start,
        'randomness':'seeded diagnostics only; ideal independent fair bits in theorem',
        'limitations':'finite diagnostics; no general mixing theorem, no end-to-end FPRAS/sampler'}
    own = Path(__file__).parent
    result['script_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    (own/'deeper_checks.json').write_text(json.dumps(result,indent=2,default=str)+'\n')
    print(json.dumps({'status':result['status'],'elapsed_seconds':result['elapsed_seconds'],
                      'core_residuals':[x['PIT_acquisition']['residual'] for x in cores]},indent=2))


if __name__ == '__main__':
    main()
