"""Passive heat-pulse delay: independent matrix moments and candidate extremizer.

Run using /usr/local/bin/python3. No external data, NumPy/SciPy only.
All curves are local linear-lumped simulations, not source measurements.
"""
from pathlib import Path
import json
import time
import numpy as np
from scipy.optimize import minimize

OUT = Path(__file__).resolve().parent


def moments(capacity, edges, sink, source=0):
    """All initial energy at source; sink edge flux is the release density.

    edges entries (i,j,conductance); sink entries (i,conductance).
    Backwards absorption generator is -diag(C)^-1 L.
    """
    c = np.asarray(capacity, dtype=float)
    n = len(c)
    lap = np.zeros((n, n))
    for i, j, g in edges:
        lap[i, i] += g
        lap[j, j] += g
        lap[i, j] -= g
        lap[j, i] -= g
    for i, g in sink:
        lap[i, i] += g
    mean_nodes = np.linalg.solve(lap, c)
    second_nodes = 2 * np.linalg.solve(lap, c * mean_nodes)
    mean = mean_nodes[source]
    variance = second_nodes[source] - mean**2
    return float(mean), float(variance), float(variance / mean**2)


def ladder_moments(c, r):
    n = len(c)
    return moments(c, [(i, i + 1, 1 / r[i]) for i in range(n - 1)], [(n - 1, 1 / r[-1])])


def capacity_kernel(c):
    s = np.cumsum(c)
    return np.minimum.outer(s, s) / np.maximum.outer(s, s)


def optimum(n, ratio, mean=1.0):
    if n == 1:
        assert ratio == 1
        return np.ones(1), np.asarray([mean]), 1.0
    log_s = np.linspace(0, np.log(ratio), n)
    s = np.exp(log_s)
    c = np.diff(np.concatenate(([0], s)))
    k = np.exp(-np.abs(log_s[:, None] - log_s[None, :]))
    w = np.linalg.solve(k, np.ones(n))
    a = mean * w / np.sum(w)
    r = a / s
    bound = 1 / (1 + (n - 1) * np.tanh(np.log(ratio) / (2 * (n - 1))))
    return c, r, float(bound)


def ordinary_ladder_optimization(n, ratio, rng, starts=8):
    """Competent ordinary same-information RC design by multistart SLSQP.

    Uses independent numerical moments, not the analytic optimum. Designs all
    positive capacities summing to ratio, C_source=1, all positive resistances.
    Resistance overall scale is irrelevant to CV; mean is normalized afterward.
    """
    def unpack(z):
        w = np.exp(z[:n-1] - np.max(z[:n-1]))
        c = np.concatenate(([1.], (ratio - 1) * w / w.sum()))
        r = np.exp(z[n-1:])
        return c, r
    def fun(z):
        c, r = unpack(z)
        try:
            return ladder_moments(c, r)[2]
        except np.linalg.LinAlgError:
            return 1e10
    best = None
    records = []
    for j in range(starts):
        z = rng.normal(0, 1.5, 2*n - 1)
        res = minimize(fun, z, method='SLSQP', bounds=[(-10, 10)] * len(z),
                       options={'ftol': 1e-12, 'maxiter': 400})
        rec = dict(start=j, cv2=float(res.fun), success=bool(res.success),
                   iterations=int(res.nit), message=res.message)
        records.append(rec)
        if best is None or res.fun < best.fun:
            best = res
    c, r = unpack(best.x)
    m = ladder_moments(c, r)[0]
    return c, r / m, records


def random_tree(n, ratio, rng):
    # Rooted at sink node n. Source 0 is a leaf or interior node as sampled.
    # Connecting each i to an earlier node after random relabeling makes a tree.
    order = [n] + list(rng.permutation(n))
    edges, sink = [], []
    for k in range(1, n + 1):
        i = int(order[k])
        j = int(order[rng.integers(k)])
        g = float(np.exp(rng.uniform(-3, 3)))
        if j == n:
            sink.append((i, g))
        else:
            edges.append((i, j, g))
    w = np.exp(rng.uniform(-2, 2, n - 1))
    c = np.concatenate(([1.], (ratio - 1) * w / w.sum()))
    return c, edges, sink


def run():
    start = time.perf_counter()
    rng = np.random.default_rng(17026)
    rows = []
    for n in [2, 3, 4, 8, 16, 32]:
        for ratio in [2., 10., 100., 10000.]:
            c, r, b = optimum(n, ratio)
            m, v, cv = ladder_moments(c, r)
            k = capacity_kernel(c)
            a = r * np.cumsum(c)
            # Explicit elementwise contraction avoids spurious matmul floating-
            # point status warnings observed with this bundled BLAS on small arrays.
            cv_kernel = float(np.sum(a[:, None] * k * a[None, :]) / a.sum()**2)
            rows.append(dict(n=n, capacity_ratio=ratio, theorem_cv2=b,
                             matrix_cv2=cv, kernel_cv2=cv_kernel, mean=m,
                             chiclana_ctmc_lower_cv2=float(1/(1+0.5*np.log(np.sum(r)/r[-1]))),
                             cv=float(np.sqrt(cv)), capacities=c.tolist(),
                             resistances=r.tolist()))
    # Explicitly independent optimization comparator.
    comparators = []
    for n, ratio in [(3, 10.), (4, 100.), (8, 100.)]:
        c, r, runs = ordinary_ladder_optimization(n, ratio, rng)
        comparators.append(dict(n=n, capacity_ratio=ratio,
                               capacities=c.tolist(), resistances=r.tolist(),
                               matrix_moments=ladder_moments(c, r), runs=runs))
    # Stress trees without using a ladder formula to evaluate moments.
    stresses = []
    for n in [3, 4, 8, 16]:
        for ratio in [2., 10., 100.]:
            bound = optimum(n, ratio)[2]
            gaps = []
            worst = None
            for _ in range(200):
                c, edges, sink = random_tree(n, ratio, rng)
                m, v, cv = moments(c, edges, sink)
                gaps.append(cv - bound)
                if worst is None or cv < worst['cv2']:
                    worst = dict(cv2=cv, capacities=c.tolist(), edges=edges, sink=sink)
            stresses.append(dict(n=n, capacity_ratio=ratio, samples=len(gaps),
                                 minimum_gap=float(min(gaps)), best=worst))
    # Arbitrary ladders verify the moment identity away from the extremizer.
    ladder_identity_errors = []
    for _ in range(200):
        n=int(rng.integers(2,20))
        c=np.exp(rng.uniform(-3,3,n))
        r=np.exp(rng.uniform(-3,3,n))
        a=r*np.cumsum(c)
        k=capacity_kernel(c)
        m,v,cv=ladder_moments(c,r)
        v_formula=float(np.sum(a[:,None]*k*a[None,:]))
        ladder_identity_errors.append(abs(v-v_formula)/max(v,v_formula))
    branch_full=moments([1,1,1,1],[(0,1,5),(1,2,10),(1,3,2.5)],[(2,1/.3)])
    branch_collapsed=ladder_moments([1,2,1],[.2,.1,.3])
    branch_check=dict(full_moments=branch_full,collapsed_moments=branch_collapsed,
                      variance_difference=branch_full[1]-branch_collapsed[1],
                      predicted_difference=2*(.1+.3)*1**2*.4)
    result = dict(seed=17026, analytic_designs=rows, ordinary_comparators=comparators,
                  random_tree_stress=stresses, wall_seconds=time.perf_counter()-start,
                  arbitrary_ladder_identity_max_relative_error=max(ladder_identity_errors),
                  branch_collapse_check=branch_check,
                  scope='linear reciprocal lumped heat model; simulation only')
    (OUT / 'numerical_results.json').write_text(json.dumps(result, indent=2, allow_nan=False) + '\n')
    print(json.dumps(dict(analytic_max_abs_error=max(abs(x['matrix_cv2']-x['theorem_cv2']) for x in rows),
                          random_tree_min_gap=min(x['minimum_gap'] for x in stresses),
                          arbitrary_ladder_max_relative_error=max(ladder_identity_errors),
                          branch_check=branch_check,
                          comparator_best=[dict(n=x['n'], ratio=x['capacity_ratio'],
                                                cv2=x['matrix_moments'][2]) for x in comparators],
                          wall_seconds=result['wall_seconds']), indent=2))


if __name__ == '__main__':
    run()
