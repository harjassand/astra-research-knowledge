#!/usr/bin/env python3
"""Bounded exact certificates for the complete flagged-stock formation frontier.

SciPy proposes rational LP certificates. Fraction arithmetic checks every
inequality and primal/dual equality; floating status is never the certificate.
This is a classical model check, not quantum acquisition or an E_F optimizer.
"""
from fractions import Fraction as F
from collections import Counter
from pathlib import Path
import json, time


def inventory(L, r):
    counts = Counter({0: 1})
    for _ in range(r):
        nxt = Counter()
        for s, n in counts.items():
            for k in range(1, L + 1):
                nxt[s + k] += n
        counts = nxt
    return [(s, F(n, L**r)) for s, n in sorted(counts.items())]


def deterministic(D, L, r, M):
    budget, overlap = F(1), F(0)
    weights = []
    for s, p in inventory(L, r):
        f = min(F(1), F(M, D**s))
        credit = min(p, budget * f)
        q = credit / f
        budget -= q
        overlap += credit
        weights.append((s, p, f, credit, q))
    assert budget >= 0
    return 1 - overlap, weights


def compact(D, L, r, epsilon):
    import numpy as np
    from scipy.optimize import linprog
    ip = inventory(L, r)
    n = len(ip)
    c = [F(s) for s, _ in ip] + [F(0)] * n
    A, b = [], []
    for i, (_, p) in enumerate(ip):
        row = [F(0)] * (2*n)
        row[i], row[n+i] = F(1), F(-1)
        A.append(row); b.append(F(0))
        row = [F(0)] * (2*n)
        row[n+i] = F(1)
        A.append(row); b.append(p)
    A.append([F(0)]*n + [F(-1)]*n)
    b.append(-(1-epsilon))
    A.append([F(-(D**s-1)) for s, _ in ip] + [F(D**s) for s, _ in ip])
    b.append(F(1))
    ans = linprog(np.array(c, float), A_ub=np.array(A, float),
                  b_ub=np.array(b, float), bounds=(0, None), method="highs")
    assert ans.success, ans.message
    rational = lambda x: F(float(x)).limit_denominator(10**12)
    x = list(map(rational, ans.x))
    z = list(map(rational, ans.ineqlin.marginals))
    dot = lambda a, q: sum((u*v for u, v in zip(a, q)), F(0))
    assert all(v >= 0 for v in x)
    assert all(dot(row, x) <= rhs for row, rhs in zip(A, b))
    assert all(v <= 0 for v in z)
    slack = [c[j]-sum((A[i][j]*z[i] for i in range(len(A))), F(0))
             for j in range(2*n)]
    assert all(v >= 0 for v in slack)
    primal, dual = dot(c, x), dot(b, z)
    assert primal == dual, (primal, dual)
    if epsilon == 0:
        assert primal == F(r*(L+1), 2)
    if D == 2 and L == 2 and r == 1:
        assert primal == max(F(0), F(3,2)-3*epsilon)
    return dict(D=D, L=L, r=r, epsilon=str(epsilon),
                inventory=[(s, str(p)) for s, p in ip],
                cost_units_lnD=str(primal), primal=list(map(str,x)),
                dual=list(map(str,z)), reduced_costs=list(map(str,slack)),
                exact_primal_dual="PASS")


def main():
    wall, cpu = time.perf_counter(), time.process_time()
    specs = [(2,2,1,F(0)), (2,2,1,F(1,8)), (2,2,1,F(1,4)),
             (2,2,1,F(1,2)), (2,2,1,F(3,4)),
             (2,3,2,F(0)), (2,3,2,F(1,4)), (3,2,2,F(1,5))]
    cases = [compact(*spec) for spec in specs]
    ds = []
    for M, expected in [(1,F(1,2)),(2,F(1,4)),(3,F(1,8)),(4,F(0))]:
        error, weights = deterministic(2,2,1,M)
        assert error == expected
        ds.append(dict(D=2,L=2,r=1,M=M,error=str(error),
                       greedy=[list(map(str,w)) for w in weights]))
    stable = dict(status="PASS", lp_cases=cases, deterministic_cases=ds,
                  scope="Exact rational finite classical preparation certificates; no physical experiment, EF optimization or advantage claim.")
    Path(__file__).with_name("RESULT.json").write_text(json.dumps(stable,indent=2)+"\n")
    timing = dict(wall_seconds=time.perf_counter()-wall,
                  process_cpu_seconds=time.process_time()-cpu,
                  jobs=1, cases=len(cases)+len(ds))
    Path(__file__).with_name("TIMING.json").write_text(json.dumps(timing,indent=2)+"\n")
    print(json.dumps(dict(status="PASS", **timing)))


if __name__ == "__main__":
    main()
