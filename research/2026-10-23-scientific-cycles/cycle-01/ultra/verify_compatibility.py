"""Small actual-state replay and exact GF(2) Hall certificates; not a proof by search.
Run on a COPY: the script writes FINITE_CHECKS.json next to itself.
"""
import os
for key in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ[key] = "1"
import itertools
import json
import math
from pathlib import Path
import resource
import sys
import time
import numpy as np

START_WALL, START_CPU = time.perf_counter(), time.process_time()

def rank2(a):
    a = np.array(a, dtype=np.uint8, copy=True)
    if a.ndim != 2:
        raise ValueError("matrix required")
    r = 0
    for j in range(a.shape[1]):
        nz = np.flatnonzero(a[r:, j])
        if len(nz) == 0:
            continue
        k = r + int(nz[0])
        a[[r, k]] = a[[k, r]]
        for i in range(a.shape[0]):
            if i != r and a[i, j]:
                a[i] ^= a[r]
        r += 1
        if r == a.shape[0]:
            break
    return r

def one_gate(n, site, g):
    out = np.array([[1.0 + 0j]])
    for j in range(n):
        out = np.kron(out, g if j == site else np.eye(2))
    return out

def clifford_fixture(n, seed):
    rng = np.random.default_rng(seed)
    g = np.concatenate((np.zeros((n, n), dtype=np.uint8), np.eye(n, dtype=np.uint8)), axis=1)
    u = np.eye(2**n, dtype=complex)
    h = np.array([[1, 1], [1, -1]], complex) / np.sqrt(2)
    s = np.diag([1, 1j])
    gates = []
    # Includes nonlocal task connections; eigenbasis need not be a task product.
    for k in range(5*n + 3):
        kind = k % 3
        site = int(rng.integers(n))
        if kind == 0:
            u = one_gate(n, site, h) @ u
            g[:, [site, n+site]] = g[:, [n+site, site]]
            gates.append(["H", site])
        elif kind == 1:
            u = one_gate(n, site, s) @ u
            g[:, n+site] ^= g[:, site]
            gates.append(["S", site])
        else:
            target = (site + int(rng.integers(1, n))) % n
            perm = np.arange(2**n)
            for x in range(2**n):
                if (x >> (n-1-site)) & 1:
                    perm[x] ^= 1 << (n-1-target)
            v = np.zeros_like(u)
            v[perm] = u
            u = v
            g[:, target] ^= g[:, site]
            g[:, n+site] ^= g[:, n+target]
            gates.append(["CNOT", site, target])
    assert rank2(g) == n
    assert not np.any((g[:, :n] @ g[:, n:].T + g[:, n:] @ g[:, :n].T) % 2)
    assert np.linalg.norm(u.conj().T @ u - np.eye(2**n)) < 1e-10
    return g, u, gates

def prefix_lists(g, r, nper):
    n = r*nper
    lists = []
    for a in range(r):
        for i in range(1, nper+1):
            sites = list(range(a*nper, a*nper+i))
            cols = sites + [n+x for x in sites]
            candidates = []
            for j in cols:
                v = g[:, j].copy()
                if np.any(v) and not any(np.array_equal(v, w) for w in candidates):
                    candidates.append(v)
            lists.append(candidates)
    return lists

def hall_certificate(lists):
    # ALL subsets, exact arithmetic. Exponential fixture check, not scalability claim.
    n = len(lists)
    min_slack = n
    for mask in range(1, 1 << n):
        selected = [j for j in range(n) if mask >> j & 1]
        cols = [v for j in selected for v in lists[j]]
        dim = rank2(np.array(cols).T) if cols else 0
        slack = dim-len(selected)
        assert slack >= 0
        min_slack = min(min_slack, slack)
    order = sorted(range(n), key=lambda j: len(lists[j]))
    result = [None]*n
    calls = 0
    def choose(k, chosen):
        nonlocal calls
        calls += 1
        if k == n:
            return True
        j = order[k]
        for v in lists[j]:
            trial = chosen + [v]
            if rank2(np.array(trial).T) != len(trial):
                continue
            result[j] = v
            if choose(k+1, trial):
                return True
        result[j] = None
        return False
    assert choose(0, [])
    basis = np.array(result).T
    assert rank2(basis) == n
    return basis, min_slack, calls

def partial_trace(a, traced, n):
    dims = [2]*n
    t = a.reshape(dims+dims)
    left = n
    for site in sorted(traced, reverse=True):
        t = np.trace(t, axis1=site, axis2=site+left)
        left -= 1
    return t.reshape(2**left, 2**left)

def score_matrix(sqrt_rho, traced, n):
    reduced = partial_trace(sqrt_rho, traced, n)
    return float(np.vdot(reduced, reduced).real / (2**len(traced)))

def score_coordinates(c, traced, n):
    # Uniform rank-one projection of the indicated amplitude coordinates.
    t = c.reshape([2]*n)
    other = [i for i in range(n) if i not in traced]
    a = np.transpose(t, traced+other).reshape(2**len(traced), -1)
    return float(np.sum(np.abs(a.sum(axis=0))**2) / 2**len(traced))

def stopping_checks():
    rows=[]
    for d, horizon, copies in [(2, 2, 2), (2, 4, 3), (3, 3, 2)]:
        # Physical product A:B computational vector: each prefix tail is D^-i.
        p=np.array([(d-1)/d**(k+1) for k in range(horizon)] + [d**(-horizon)])
        for trunc in (0.0, 2.0, 8.0):
            g=np.array([math.exp(-trunc)]+[d**k for k in range(1,horizon+1)])
            actual=float(np.dot(p,g))**copies
            z=1+(horizon-1+math.exp(-trunc))*(1-1/d)
            assert abs(actual-z**copies) < 1e-10
            rows.append({"D":d,"N":horizon,"t":copies,"L":trunc,"partition_error":abs(actual-z**copies)})
    return rows

def run():
    rng=np.random.default_rng(20261021)
    cases=[]
    max_dom=0.0
    for r, nper, seed in [(2,1,7),(2,2,11),(2,3,19),(3,2,23)]:
        n=r*nper; q=2**n
        g,u,gates=clifford_fixture(n,seed)
        lists=prefix_lists(g,r,nper)
        basis,slack,calls=hall_certificate(lists)
        bits=np.array(list(itertools.product((0,1),repeat=n)),dtype=np.uint8)
        labels=(bits @ basis.T)%2
        powers=2**np.arange(n-1,-1,-1)
        permutation=labels @ powers
        assert len(np.unique(permutation))==q
        spectra=[]
        v=rng.random(q)**3; spectra.append(v/v.sum())
        v=np.zeros(q); v[::3]=1; spectra.append(v/v.sum())
        v=np.zeros(q); v[0]=1; spectra.append(v)
        spectra.append(np.ones(q)/q)
        for index,lam in enumerate(spectra):
            c=np.sqrt(lam[permutation])
            sqrt_rho=(u*np.sqrt(lam)) @ u.conj().T
            actual=[]; coordinate=[]
            for a in range(r):
                for i in range(1,nper+1):
                    traced=list(range(a*nper,a*nper+i))
                    actual.append(score_matrix(sqrt_rho,traced,n))
                    coordinate.append(score_coordinates(c,traced,n))
            violation=max(np.array(actual)-coordinate)
            assert violation < 2e-12
            max_dom=max(max_dom,violation)
            entropy=float(-sum(x*math.log(x) for x in lam if x>0))
            defect=math.log(2)*sum(actual)-entropy
            coorddef=math.log(2)*sum(coordinate)-entropy
            constant=2-math.log(2)
            assert coorddef <= r*constant+1e-11
            cases.append({"r":r,"N":nper,"seed":seed,"spectrum_case":index,
                          "generator_xz":g.tolist(),"selected_label_basis_columns":basis.tolist(),
                          "gates":gates,"lambda":lam.tolist(),"all_subset_Hall_min_slack":slack,
                          "transversal_search_nodes":calls,"actual_prefix_scores":actual,
                          "coordinate_upper_scores":coordinate,"entropy":entropy,
                          "defect_per_task":defect/r,"coordinate_defect_per_task":coorddef/r})
    stopping=stopping_checks()
    rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    result={"status":"PASS","scope":"finite_actual_quantum_states_and_exact_GF2_certificates;not_a_universal_numerical_proof",
            "actual_state_cases":len(cases),"all_subset_Hall_cases":4,
            "max_positive_componentwise_domination_residual":max_dom,
            "cases":cases,"stopping_partition_checks":stopping,
            "implementation":"complete finite backtracking; exponential worstcase; no efficiency claim",
            "cost":{"wall_s":time.perf_counter()-START_WALL,"CPU_s":time.process_time()-START_CPU,
                    "peak_RSS_bytes":rss if sys.platform=="darwin" else 1024*rss,
                    "matrix_max_dimension":64,"BLAS_threads":1,
                    "total_research_or_retrieval_cost":"UNKNOWN"}}
    Path(__file__).with_name("FINITE_CHECKS.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({k:v for k,v in result.items() if k not in ("cases","stopping_partition_checks")},indent=2))

if __name__=="__main__":
    run()
