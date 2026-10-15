#!/usr/bin/env python3
"""Exact countermodels and invariance checks; small fixtures, not benchmarks.

Writes only alongside this script. Fractions establish the stated finite models.
The deadline check additionally compares a closed form with scipy.linalg.expm.
An unmodified, pinned PyGT.GT is an optional independently implemented comparator.
"""
from __future__ import annotations

from fractions import Fraction as F
from decimal import Decimal, localcontext, ROUND_FLOOR, ROUND_CEILING
from itertools import combinations
from pathlib import Path
import hashlib
import importlib.util
import json
import math
import random
import sys
import time
import urllib.request

ROOT = Path(__file__).resolve().parent
PYGT_PIN = "fa0e106958d9948209daff04360290d50de82572"


def scale10(e):
    return F(10**e) if e >= 0 else F(1, 10**(-e))


def solve(A, b):
    """Exact Gauss-Jordan, solely an oracle for small rational checks."""
    n = len(b)
    a = [list(row) + [rhs] for row, rhs in zip(A, b)]
    for k in range(n):
        pivot = next(i for i in range(k, n) if a[i][k])
        a[k], a[pivot] = a[pivot], a[k]
        z = a[k][k]
        a[k] = [x/z for x in a[k]]
        for i in range(n):
            if i != k:
                z = a[i][k]
                a[i] = [x-z*y for x, y in zip(a[i], a[k])]
    return [row[-1] for row in a]


def lap(nodes, edges):
    ix = {x: i for i, x in enumerate(nodes)}
    L = [[F(0) for _ in nodes] for _ in nodes]
    for (a, b), c in edges.items():
        i, j = ix[a], ix[b]
        L[i][i] += c
        L[j][j] += c
        L[i][j] -= c
        L[j][i] -= c
    return L, ix


def values(w, edges, s=0, t=1):
    nodes = sorted(w)
    L, ix = lap(nodes, edges)
    interior = [i for i in nodes if i not in (s, t)]
    A = [[L[ix[i]][ix[j]] for j in interior] for i in interior]
    b = [-L[ix[i]][ix[s]] for i in interior]
    hi = solve(A, b) if interior else []
    h = dict(zip(interior, hi)) | {s: F(1), t: F(0)}
    C = sum(c*(h[a]-h[b])**2 for (a,b), c in edges.items())
    N = sum(w[i]*h[i] for i in w)
    nt = [i for i in nodes if i != t]
    u = solve([[L[ix[i]][ix[j]] for j in nt] for i in nt], [w[i] for i in nt])
    mfpt = dict(zip(nt, u)) | {t: F(0)}
    assert N/C == mfpt[s]
    return C, N, h, mfpt


def eliminate(w, edges, keep):
    """Classical positive star-mesh plus load (mass) elimination."""
    w, edges = dict(w), dict(edges)
    peak = len(edges)
    work = 0
    for k in sorted(set(w)-set(keep)):
        nei = {}
        for (a,b), c in edges.items():
            if k == a:
                nei[b] = c
            elif k == b:
                nei[a] = c
        d = sum(nei.values())
        assert d > 0
        for j, c in nei.items():
            w[j] += c*w[k]/d
        for a,b in combinations(sorted(nei), 2):
            key = (a,b)
            edges[key] = edges.get(key, F(0)) + nei[a]*nei[b]/d
        edges = {e:c for e,c in edges.items() if k not in e}
        del w[k]
        peak = max(peak, len(edges))
        work += len(nei)*(len(nei)-1)//2
    return w, edges, {"pair_updates": work, "peak_edges": peak}


def components(vertices, edges):
    rem = set(vertices)
    out = []
    while rem:
        stack = [rem.pop()]
        cc = set(stack)
        while stack:
            x = stack.pop()
            ns = {b if a == x else a for a,b in edges if a == x or b == x}
            for y in ns & rem:
                rem.remove(y)
                cc.add(y)
                stack.append(y)
        out.append(cc)
    return out


def mass_envelope(w, edges, keep, h):
    rem = set(w)-set(keep)
    base = sum(w[i]*h[i] for i in keep)
    lo, hi = base, base
    for cc in components(rem, {e:c for e,c in edges.items() if set(e) <= rem}):
        bd = set()
        for a,b in edges:
            if a in cc and b in keep:
                bd.add(b)
            if b in cc and a in keep:
                bd.add(a)
        W = sum(w[i] for i in cc)
        assert bd
        lo += W*min(h[i] for i in bd)
        hi += W*max(h[i] for i in bd)
    return lo, hi


def path_lower(nodes, edges, s, t):
    parent = {s: None}
    queue = [s]
    for x in queue:
        for a,b in edges:
            if a == x or b == x:
                y = b if a == x else a
                if y not in parent:
                    parent[y] = x
                    queue.append(y)
    x, resistance = t, F(0)
    while x != s:
        y = parent[x]
        resistance += 1/edges[tuple(sorted((x,y)))]
        x = y
    return 1/resistance


def transport_flow_energy(w, edges, q, root):
    parent = {root: None}
    queue = [root]
    for x in queue:
        for a,b in edges:
            if a == x or b == x:
                y = b if a == x else a
                if y not in parent:
                    parent[y] = x
                    queue.append(y)
    mass = {x:q.get(x, F(0)) for x in w}
    energy = F(0)
    for x in queue[:0:-1]:
        p = parent[x]
        energy += mass[x]**2/edges[tuple(sorted((x,p)))]
        mass[p] += mass[x]
    return energy


def goal_certificate(w, edges, C, N, rng, s=0, t=1):
    nodes = sorted(w)
    interior = [i for i in nodes if i not in (s,t)]
    L, ix = lap(nodes, edges)
    g = {i:F(rng.randrange(11),10) for i in interior} | {s:F(1),t:F(0)}
    v = {i:F(rng.randrange(11),5) for i in interior}
    r = {i:sum(L[ix[i]][ix[j]]*g[j] for j in nodes) for i in interior}
    q = {i:w[i]-sum(L[ix[i]][ix[j]]*v[j] for j in interior) for i in interior}
    estimate = sum(w[i]*g[i] for i in nodes)-sum(v[i]*r[i] for i in interior)
    Eg = sum(c*(g[a]-g[b])**2 for (a,b),c in edges.items())
    CL = path_lower(nodes, edges, s, t)
    Dq = transport_flow_energy(w, edges, q, t)
    assert CL <= C <= Eg
    assert (N-estimate)**2 <= Dq*(Eg-CL)


def forest_ratio(w, edges, s=0, t=1):
    nodes = sorted(w)
    es = list(edges)
    n = len(nodes)
    def partition(selected):
        parent = {i:i for i in nodes}
        def root(x):
            while parent[x] != x:
                x = parent[x]
            return x
        prod = F(1)
        for a,b in selected:
            x,y = root(a),root(b)
            if x == y:
                return None, F(0)
            parent[x] = y
            prod *= edges[(a,b)]
        return {i:root(i) for i in nodes},prod
    tree = F(0)
    forest = F(0)
    for selected in combinations(es, n-1):
        p, z = partition(selected)
        if p is not None:
            tree += z
    for selected in combinations(es, n-2):
        p,z = partition(selected)
        if p is not None and p[s] != p[t]:
            forest += z*sum(w[i] for i in nodes if p[i] == p[s])
    return forest/tree


def random_checks():
    rng = random.Random(20261015)
    counts = {"positive_elimination":0,"boundary_envelope":0,"goal_certificate":0,"forest_identity":0,"coefficient_precision":0}
    eta = F(1,100000)
    zeta = F(1,200000)
    for case in range(100):
        n = rng.randrange(3,9)
        w = {i:F(rng.randrange(1,12))*scale10(rng.randrange(-5,6)) for i in range(n)}
        edges = {}
        for i in range(1,n):
            edges[tuple(sorted((i,rng.randrange(i))))] = F(rng.randrange(1,12))*scale10(rng.randrange(-8,9))
        for a,b in combinations(range(n),2):
            if rng.random() < .25:
                edges[(a,b)] = F(rng.randrange(1,12))*scale10(rng.randrange(-8,9))
        C,N,h,u = values(w,edges)
        keep = {0,1,2}
        rw,re,stats = eliminate(w,edges,keep)
        RC,RN,Rh,Ru = values(rw,re)
        assert C == RC and N == RN and sum(w.values()) == sum(rw.values())
        for source,target in [(0,1),(1,0),(2,1),(1,2),(0,2),(2,0)]:
            fu = values(w,edges,source,target)[3]
            ru = values(rw,re,source,target)[3]
            assert all(fu[i] == ru[i] for i in keep)
        counts["positive_elimination"] += 1
        lo,hi = mass_envelope(w,edges,keep,h)
        assert lo <= N <= hi
        counts["boundary_envelope"] += 1
        goal_certificate(w,edges,C,N,rng)
        counts["goal_certificate"] += 1
        pw = {i:x*(1+zeta*rng.choice((-1,1))) for i,x in w.items()}
        pe = {e:c*(1+eta*rng.choice((-1,1))) for e,c in edges.items()}
        newtau = values(pw,pe)[3][0]
        tau = N/C
        l = (1-zeta)*(1-eta)**(n-2)/(1+eta)**(n-1)
        ubd = (1+zeta)*(1+eta)**(n-2)/(1-eta)**(n-1)
        assert l <= newtau/tau <= ubd
        counts["coefficient_precision"] += 1
        if n <= 6 and len(edges) <= 10:
            assert forest_ratio(w,edges) == tau
            counts["forest_identity"] += 1
    return counts


def countermodels():
    M = F(10**12)
    delta = F(1,10**12)
    p = F(1,10**12)
    w = {0:F(1),1:F(1),2:M}
    pair = []
    for a in [p,1-p]:
        edges = {(0,1):F(1),(0,2):delta*a,(1,2):delta*(1-a)}
        C,N,h,u = values(w,edges)
        rw,re,stats = eliminate(w,edges,{0,1})
        assert C == 1+delta*p*(1-p)
        assert N == 1+M*a
        assert rw[0] == N
        pair.append({"p":str(a),"C":str(C),"Z":str(sum(w.values())),"N":str(N),"MFPT":str(u[0]),"deleted_conductance_budget":str(delta),"transported_source_mass":str(rw[0]),"transported_target_mass":str(rw[1])})
    return {"unequal_hitting_weak_pair":pair,"directional_mean_ratio":str(F(pair[1]["MFPT"])/F(pair[0]["MFPT"]))}


def rational_negative_exp_bounds(x, degree):
    """Exact rational Taylor/geometric bounds on exp(-x), x >= 0."""
    x=F(x)
    term=total=F(1)
    for k in range(1,degree+1):
        term *= x/k
        total += term
    rho=x/(degree+2)
    assert 0 <= rho < 1
    remainder=(term*x/(degree+1))/(1-rho)
    return 1/(total+remainder),1/total


def outward_decimal(x, rounding):
    with localcontext() as ctx:
        ctx.prec=60
        ctx.rounding=rounding
        return str(Decimal(x.numerator)/Decimal(x.denominator))


def hybrid_rational_certificate():
    delta=F(1,10**12)
    rows=[]
    for T,degree in [(20,128),(100,256)]:
        core_lo,core_hi=rational_negative_exp_bounds(F(T),degree)
        entry_exp_lo,entry_exp_hi=rational_negative_exp_bounds((1+delta)*T,degree)
        entry_hi=delta/(1+delta)*(1-entry_exp_lo)
        upper=core_hi+entry_hi
        lower_text=outward_decimal(core_lo,ROUND_FLOOR)
        upper_text=outward_decimal(upper,ROUND_CEILING)
        ratio=F(upper_text)/F(lower_text)
        if T == 20:
            assert ratio < F(1000486,1000000)
        rows.append({"deadline":T,"exact_mean":"1000001","survival_lower":lower_text,"survival_upper":upper_text,"ratio_upper":outward_decimal(ratio,ROUND_CEILING),"negative_exp_Taylor_degree":degree,"rounding":"Exact rational Taylor/geometric proof; final 60-digit decimal division rounded outward; ratio bounds encoded decimal endpoints","relative_ratio_less_than_1_000486":T == 20})
    return rows


def deadline_check():
    import numpy as np
    import scipy
    from scipy.linalg import expm
    M,delta,T = 1e6,1e-12,100.
    alpha,beta = 1+delta+delta/M,delta/M
    disc = math.sqrt(alpha*alpha-4*beta)
    slow = 2*beta/(alpha+disc)
    fast = alpha-slow
    A = (delta*(1+1/M)-slow)/(fast-slow)
    B = (1-slow)/(fast-slow)
    survival = A*math.exp(-slow*T)+B*math.exp(-fast*T)
    Q = np.array([[-(1+delta),delta],[delta/M,-delta/M]])
    direct = float((np.array([1.,0.])@expm(Q*T)).sum())
    reduced = math.exp(-T/(M+1))
    assert abs(direct/survival-1)<1e-10
    assert reduced/survival > 1e11
    hybrid=[]
    for deadline in [20.,100.]:
        core=math.exp(-deadline)
        entry=delta/(1+delta)*(-math.expm1(-(1+delta)*deadline))
        exact=A*math.exp(-slow*deadline)+B*math.exp(-fast*deadline)
        assert core <= exact <= core+entry+1e-25
        hybrid.append({"deadline":deadline,"exact_mean_returned_separately":M+1,"core_survival_lower":core,"branch_entry_error_upper":entry,"survival_upper":core+entry,"original_survival_closed_form":exact,"relative_interval_width":entry/core,"arithmetic_scope":"float evaluations of a proved analytic envelope, not directed-rounding endpoint certification"})
    return {"M":M,"delta":delta,"deadline":T,"capacity":1,"total_mass":M+2,"exact_mean":M+1,"mean_preserving_two_state_survival":reduced,"exact_three_state_survival_closed_form":survival,"scipy_expm_survival":direct,"survival_ratio":reduced/survival,"variance":(M+1)**2+2*M*M/delta,"slow_rate":slow,"fast_rate":fast,"slow_survival_weight":A,"hybrid_float_evaluations":hybrid,"hybrid_rational_arithmetic_certificate":hybrid_rational_certificate(),"numpy":np.__version__,"scipy":scipy.__version__}


def fetch_pygt():
    ledger = {"repository":"https://github.com/tomswinburne/PyGT","commit":PYGT_PIN,"files":[]}
    for source,target in [("PyGT/GT.py","GT.py"),("LICENSE","LICENSE")]:
        url = f"https://raw.githubusercontent.com/tomswinburne/PyGT/{PYGT_PIN}/{source}"
        raw = urllib.request.urlopen(url,timeout=30).read()
        path = ROOT/"vendor"/target
        path.parent.mkdir(exist_ok=True)
        path.write_bytes(raw)
        ledger["files"].append({"url":url,"target":str(path.relative_to(ROOT)),"bytes":len(raw),"sha256":hashlib.sha256(raw).hexdigest()})
    (ROOT/"vendor"/"SOURCE.json").write_text(json.dumps(ledger,indent=2)+"\n")
    return ledger


def pygt_checks():
    import numpy as np
    path = ROOT/"vendor"/"GT.py"
    if not path.exists():
        return {"status":"NOT_EXECUTED","reason":"Run --fetch-pygt first"}
    spec = importlib.util.spec_from_file_location("pinned_pygt_GT",path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    records=[]
    models=[]
    for p in [F(1,10**12),1-F(1,10**12)]:
        delta=F(1,10**12)
        models.append(({0:F(1),1:F(1),2:F(10**12)}, {(0,1):F(1),(0,2):delta*p,(1,2):delta*(1-p)},f"weak_two_boundary_p={p}"))
    for delta in [F(1,10**12),F(1),F(10**12)]:
        models.append(({0:F(1),1:F(1),2:F(10**6)}, {(0,1):F(1),(0,2):delta},f"one_boundary_delta={delta}"))
    for w,edges,label in models:
        n=len(w)
        deg=np.zeros(n)
        for (a,b),c in edges.items():
            deg[a]+=float(c)
            deg[b]+=float(c)
        tau=np.array([float(w[j])/deg[j] for j in range(n)])
        B=np.zeros((n,n))
        for (a,b),c in edges.items():
            B[b,a]=float(c)/deg[a]
            B[a,b]=float(c)/deg[b]
        rm=np.array([False,False,True])
        start=time.perf_counter()
        rb,rt=mod.blockGT(rm.copy(),B.copy(),tau.copy(),block=1,screen=False)
        # Exit probability is summed off-diagonal, avoiding cancellation in 1-Bss.
        got=float(rt[0]/np.asarray(rb)[1,0])
        exact=float(values(w,edges)[3][0])
        elapsed=time.perf_counter()-start
        error=got/exact-1
        assert abs(error)<1e-10
        records.append({"model":label,"pygt_MFPT":got,"exact_MFPT":exact,"relative_error":error,"single_run_seconds_including_small_oracle":elapsed})
    return {"status":"EXECUTED_SMALL_FIXTURES","commit":PYGT_PIN,"source_sha256":hashlib.sha256(path.read_bytes()).hexdigest(),"records":records,"timing_scope":"Import excluded. Recorded fixture time includes exact rational oracle and is not a performance comparison."}


def main():
    if "--fetch-pygt" in sys.argv:
        fetch_pygt()
    start=time.perf_counter()
    results={"scope":"small exact models and adversarial fixtures; no molecular benchmark, physical validation or speed advantage","capital_pin":"a6190a1083f688a7e4bf64adbc5244ef150ff2c4","python":sys.version,"checks":random_checks(),"countermodels":countermodels(),"deadline":deadline_check(),"pygt":pygt_checks()}
    results["elapsed_seconds_including_imports"] = time.perf_counter()-start
    (ROOT/"results.json").write_text(json.dumps(results,indent=2)+"\n")
    print(json.dumps(results,indent=2))


if __name__ == "__main__":
    main()
