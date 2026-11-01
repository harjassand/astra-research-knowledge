"""A fully acquired finite-box dual backend for Funaki--Gu--Wang (2026).

Infinite one-dimensional speed-change exclusion at rho=1/2, with
c_(i,i+1)=1+alpha*eta_(i-1)*eta_(i+2).  For Lambda={0,...,L-1}, the
dual optimizer is found separately at fixed outside occupations and at fixed
particle count on Lambda+={0,...,L}.  Every block is an explicitly constructed
finite graph Laplacian.  A floating pinned solve proposes its potential.

The bound reported below is rigorous rational arithmetic: the residual after
dyadic quantization is bounded using the elementary connected-S-vertex-graph
gap >=1/S^2.  This is only a numerical-error bound on a finite block, not a
spectral-gap hypothesis on the infinite conserved process.  The finite-box
dual convergence theorem supplies the spatial-limit guarantee.
"""
import os
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
from fractions import Fraction as F
import json
from pathlib import Path
import time
import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import splu


def exact_pinned_response(edges, source, size):
    """Ordinary rational Gaussian elimination: a terminating fallback backend.

    This is deliberately not a large-box performance claim.  It makes arbitrary
    requested arithmetic accuracy available without an unimplemented solver.
    """
    m = size-1
    a = [[F(0) for _ in range(m+1)] for _ in range(m)]
    for i, j, c in edges:
        if i:
            a[i-1][i-1] += c
        if j:
            a[j-1][j-1] += c
        if i and j:
            a[i-1][j-1] -= c; a[j-1][i-1] -= c
    for i in range(m):
        a[i][-1] = F(int(source[i+1]))
    for k in range(m):
        assert a[k][k] > 0
        for i in range(k+1, m):
            if not a[i][k]:
                continue
            ratio = a[i][k]/a[k][k]
            for j in range(k+1, m+1):
                a[i][j] -= ratio*a[k][j]
            a[i][k] = F(0)
    x = [F(0)]*m
    for i in range(m-1, -1, -1):
        x[i] = (a[i][-1]-sum(a[i][j]*x[j] for j in range(i+1, m)))/a[i][i]
    return sum(F(int(source[i+1]))*x[i] for i in range(m))


def solve(L, alpha=1, bits=80, exact=False):
    start = time.perf_counter()
    N = L + 1
    Q = 1 << bits
    sectors = [[] for _ in range(N + 1)]
    for z in range(1 << N):
        sectors[z.bit_count()].append(z)
    total_upper_num = 0
    total_trial_num = 0
    total_error_num = 0
    max_sector = 0
    total_nonzeros = 0
    exact_total = F(0)
    for outside in range(4):
        left, right = outside & 1, outside >> 1
        for states in sectors:
            S = len(states)
            max_sector = max(max_sector, S)
            if S <= 1:
                continue
            index = {z: i for i, z in enumerate(states)}
            edges = []
            for i, z in enumerate(states):
                for b in range(L):
                    if ((z >> b) ^ (z >> (b+1))) & 1 == 0:
                        continue
                    zz = z ^ (3 << b)
                    j = index[zz]
                    if i >= j:
                        continue
                    l = left if b == 0 else (z >> (b-1)) & 1
                    r = right if b == L-1 else (z >> (b+2)) & 1
                    c = 1 + alpha*l*r
                    edges.append((i, j, c))
            rows, cols, vals = [], [], []
            diag = [0] * S
            for i, j, c in edges:
                rows.extend((i, j)); cols.extend((j, i)); vals.extend((-c, -c))
                diag[i] += c; diag[j] += c
            rows.extend(range(S)); cols.extend(range(S)); vals.extend(diag)
            K = sp.csc_matrix((np.array(vals, dtype=np.int64), (rows, cols)), shape=(S, S))
            total_nonzeros += K.nnz
            source = np.array([((z >> L) & 1) - (z & 1) for z in states], dtype=np.int64)
            assert int(source.sum()) == 0
            if exact:
                exact_total += exact_pinned_response(edges, source, S)
                continue
            proposal = np.zeros(S)
            proposal[1:] = splu(K[1:, 1:].astype(float)).solve(source[1:].astype(float))
            xn = [round(float(x)*Q) for x in proposal]
            residual = [Q*int(f) for f in source]
            energy = 0
            for i, j, c in edges:
                delta = xn[i] - xn[j]
                energy += c*delta*delta
                residual[i] -= c*delta
                residual[j] += c*delta
            assert sum(residual) == 0
            trial = 2*Q*sum(int(f)*x for f, x in zip(source, xn)) - energy
            error = S*S*sum(r*r for r in residual)
            total_trial_num += trial
            total_error_num += error
            total_upper_num += trial + error
    # R = E[f K_box^+ f]; D_star = chi*L/R, chi=1/4.
    # The expectation has 4*2^N equally likely outside/inside states.
    R_upper = exact_total/(4*(1 << N)) if exact else F(total_upper_num, Q*Q*4*(1 << N))
    R_trial = R_upper if exact else F(total_trial_num, Q*Q*4*(1 << N))
    lower = max(F(1), F(L, 4) / R_upper)
    assert 1 <= lower <= F(4+alpha, 4)
    return {"L": L, "alpha": alpha, "density": "1/2",
            "finite_box_sites": N, "external_configurations": 4,
            "states_enumerated": 4*(1 << N), "max_particle_sector": max_sector,
            "total_laplacian_nonzeros": total_nonzeros,
            "lower": float(lower),
            "lower_fraction": [str(lower.numerator), str(lower.denominator)],
            "dual_response_trial": float(R_trial),
            "dual_response_error_bound": float(R_upper-R_trial),
            "arithmetic_backend": "exact rational Gaussian elimination" if exact else "dyadic trial with exact residual bound",
            "seconds": time.perf_counter()-start,
            "status": "Exact rational infinite-volume lower from FGW dual finite box and explicit residual bound"}


if __name__ == "__main__":
    results = []
    for alpha in [0, 1, 9]:
        for L in [1, 2, 4, 6, 8, 10]:
            result = solve(L, alpha)
            results.append(result)
            print(json.dumps(result), flush=True)
            Path(__file__).with_name("exclusion_finite_box_results.json").write_text(json.dumps(results, indent=2)+"\n")
