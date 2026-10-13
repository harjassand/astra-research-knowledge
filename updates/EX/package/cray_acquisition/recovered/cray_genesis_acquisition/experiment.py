"""Reproducible prototype: dissipation-weighted coefficient acquisition.

All large-network inputs are SYNTHETIC. Expensive-oracle calls are counted,
not actually performed ab initio. Large-network arithmetic is float64 and is
NOT an interval-arithmetic certificate. See exact_checks.py and REPORT.md.

Run: OPENBLAS_NUM_THREADS=1 python experiment.py
"""
from __future__ import annotations
import json
import math
import time
from pathlib import Path
from dataclasses import dataclass
import numpy as np
from scipy import sparse
from scipy.sparse.linalg import spsolve

HERE = Path(__file__).resolve().parent

@dataclass
class Network:
    shape: tuple[int, int, int]
    edges: np.ndarray
    c0: np.ndarray
    reference_h: np.ndarray
    C0: float
    p: np.ndarray
    axial: np.ndarray

def make_network(shape=(256, 256, 1), seed=2601013) -> Network:
    """Parallel heterogeneous axial channels coupled by arbitrary lateral edges.

    Each axial column has its own conductance, constant along that column.
    Hence h=x/(nx-1) is an EXACT mathematical reference solution, despite
    heterogeneous cross-links. Floating arrays approximate this exact formula.
    Coefficients are positive integers divided by 1024.
    """
    rng = np.random.default_rng(seed)
    nx, ny, nz = shape
    ids = np.arange(nx*ny*nz).reshape(shape)
    ex = np.column_stack((ids[:-1].ravel(), ids[1:].ravel()))
    ey = np.column_stack((ids[:, :-1].ravel(), ids[:, 1:].ravel()))
    ez = np.column_stack((ids[:, :, :-1].ravel(), ids[:, :, 1:].ravel()))
    edges = np.concatenate((ex, ey, ez))
    channel = rng.integers(256, 4097, size=ny*nz).astype(float)/1024
    cx = np.tile(channel, nx-1)
    lateral = rng.integers(128, 8193, size=len(ey)+len(ez)).astype(float)/1024
    c0 = np.concatenate((cx, lateral))
    h = np.repeat(np.arange(nx)/(nx-1), ny*nz)
    C0 = float(channel.sum()/(nx-1))
    p = np.zeros(len(edges))
    p[:len(ex)] = cx / ((nx-1)*channel.sum())
    p /= p.sum()
    axial = np.zeros(len(edges), dtype=bool)
    axial[:len(ex)] = True
    return Network(shape, edges, c0, h, C0, p, axial)

def solve_conductance(net: Network, ratios: np.ndarray) -> tuple[float, float, float]:
    start = time.perf_counter()
    u, v = net.edges.T
    c = net.c0 * ratios
    N = int(np.prod(net.shape))
    L = sparse.coo_matrix((np.concatenate((c,c,-c,-c)),
                          (np.concatenate((u,v,u,v)), np.concatenate((u,v,v,u)))),
                         shape=(N,N)).tocsr()
    plane = net.shape[1]*net.shape[2]
    interior = np.arange(plane, N-plane)
    h = np.zeros(N)
    h[-plane:] = 1.0
    h[interior] = spsolve(L[interior][:, interior].tocsc(), -(L @ h)[interior])
    drop = h[u]-h[v]
    value = float(np.dot(c, drop*drop))
    res = float(np.max(np.abs((L @ h)[interior])))
    return value, time.perf_counter()-start, res

def eb_radius(data: np.ndarray, width: float, delta: float) -> float:
    """One-sided Maurer-Pontil sample-variance confidence radius.

    For X in an interval of known width W and n>=2:
    E X <= mean X + sqrt(2 s^2 log(2/delta)/n)
                        + 7 W log(2/delta)/(3(n-1)).
    """
    n = len(data)
    if n < 2:
        return float('inf')
    z = math.log(2.0/delta)
    return math.sqrt(2*float(np.var(data, ddof=1))*z/n) + 7*width*z/(3*(n-1))

def certify(net: Network, ratios: np.ndarray, method: str, seed: int,
            epsilon=.05, alpha=.01, lo=.5, hi=2., max_n=131072) -> dict:
    """Sequential moment certificate with an explicit union bound over stages.

    Only values at sampled edges are used by this procedure. One sample queries
    one coefficient; a cache avoids repeat high-fidelity calls. Stage k gives
    each of its two one-sided bounds error alpha/[2 k(k+1)].
    The sum over all stages and both moments is alpha.
    """
    if not (0 < lo < hi and 0 < epsilon < 1 and 0 < alpha < 1):
        raise ValueError('Invalid bounds or tolerance.')
    start = time.perf_counter()
    rng = np.random.default_rng(seed)
    idx = rng.choice(len(net.p), size=max_n, p=net.p)
    # Sampling all random indices upfront does not read the expensive values.
    stage_rows = []
    lower, upper = lo*net.C0, hi*net.C0
    n = 128
    k = 0
    while n <= max_n:
        k += 1
        vals = ratios[idx[:n]]
        if np.any(vals < lo) or np.any(vals > hi):
            raise ValueError('Sampled coefficient violates asserted bounds.')
        reciprocal = 1/vals
        d = alpha / (2*k*(k+1))
        if method == 'empirical_bernstein':
            arad = eb_radius(vals, hi-lo, d)
            brad = eb_radius(reciprocal, 1/lo-1/hi, d)
        elif method == 'hoeffding':
            arad = (hi-lo)*math.sqrt(math.log(1/d)/(2*n))
            brad = (1/lo-1/hi)*math.sqrt(math.log(1/d)/(2*n))
        else:
            raise ValueError(method)
        au = min(hi, float(vals.mean())+arad)
        bu = min(1/lo, float(reciprocal.mean())+brad)
        lower = max(lower, net.C0/bu)
        upper = min(upper, net.C0*au)
        if lower > upper:
            raise RuntimeError('Empty confidence intersection; audit data/bounds.')
        row = dict(stage=k, samples=n, unique_queries=int(len(np.unique(idx[:n]))),
                   lower=lower, upper=upper, relative_width=upper/lower-1,
                   sample_mean=float(vals.mean()), sample_inverse_mean=float(reciprocal.mean()))
        stage_rows.append(row)
        if upper/lower <= 1+epsilon:
            break
        n *= 2
    last = stage_rows[-1]
    return dict(method=method, seed=seed, epsilon=epsilon, alpha=alpha,
                passed=bool(last['relative_width'] <= epsilon),
                samples=last['samples'], unique_queries=last['unique_queries'],
                lower=lower, upper=upper, midpoint=math.sqrt(lower*upper),
                relative_width=last['relative_width'],
                compute_seconds=time.perf_counter()-start, stages=stage_rows)

def cases(net: Network) -> dict[str, np.ndarray]:
    rng = np.random.default_rng(74192)
    M = len(net.edges)
    axial_n = int(net.axial.sum())
    # Lateral values have no ratio bound in the theorem (p=0). A 10^8 spread
    # stresses that the certificate does not require their acquisition.
    lateral_log = rng.uniform(-4, 4, size=M-axial_n)
    lateral = 10**lateral_log
    case1 = np.concatenate((np.full(axial_n, 1.6), lateral))
    u, v = net.edges[:axial_n].T
    x = (u//(net.shape[1]*net.shape[2]))/(net.shape[0]-1)
    y = (u//net.shape[2]) % net.shape[1]
    z = u % net.shape[2]
    case2ax = np.exp(.08*np.sin(2*np.pi*x + .21*y) + .045*np.cos(.13*z+.3*y))
    case2 = np.concatenate((case2ax, lateral))
    # Strong axial mismatch: the fixed witnesses intentionally do not resolve it.
    case3ax = np.where(rng.random(axial_n)<.5, .5, 2.)
    case3 = np.concatenate((case3ax, lateral))
    return {'common_scale':case1, 'heterogeneous_small_mismatch':case2,
            'strong_mismatch':case3}

def main():
    started = time.perf_counter()
    net = make_network()
    out = dict(status='synthetic float64 diagnostic, not physical validation',
               numpy_version=np.__version__, shape=net.shape,
               vertices=int(np.prod(net.shape)), edges=len(net.edges),
               positive_sampling_support=int(net.axial.sum()), C0=net.C0,
               reference_acquisition_seconds=time.perf_counter()-started,
               cases={})
    allcases = cases(net)
    for name, ratios in allcases.items():
        A = float(np.dot(net.p, ratios))
        B = float(np.dot(net.p, 1/ratios))
        truth, secs, residual = solve_conductance(net, ratios)
        rows = []
        for method in ('empirical_bernstein','hoeffding'):
            result = certify(net, ratios, method, seed=19031)
            result['contains_float64_comparator'] = bool(result['lower'] <= truth <= result['upper'])
            result['midpoint_relative_error'] = result['midpoint']/truth-1
            rows.append(result)
        record = dict(A=A, B=B, intrinsic_gap=A*B-1,
                      full_moment_lower=net.C0/B, full_moment_upper=net.C0*A,
                      target_conductance=truth, target_solve_seconds=secs,
                      target_interior_residual_inf=residual, methods=rows)
        out['cases'][name] = record
        print(name, 'C/C0',truth/net.C0,'gap',A*B-1,'solve_s',secs, flush=True)
        for row in rows:
            print(row['method'],row['passed'],row['samples'],row['unique_queries'],
                  row['relative_width'],row['contains_float64_comparator'], flush=True)
        (HERE/'results.json').write_text(json.dumps(out, indent=2))
    # Monte Carlo diagnostic; not evidence of a 99% coverage guarantee by itself.
    coverage=[]
    ratios=allcases['heterogeneous_small_mismatch']
    truth=out['cases']['heterogeneous_small_mismatch']['target_conductance']
    for seed in range(100,200):
        row=certify(net, ratios, 'empirical_bernstein', seed=seed, max_n=16384)
        coverage.append(dict(seed=seed, passed=row['passed'], samples=row['samples'],
                             queries=row['unique_queries'],
                             covered=bool(row['lower']<=truth<=row['upper'])))
    out['coverage_diagnostic']=coverage
    out['total_seconds']=time.perf_counter()-started
    (HERE/'results.json').write_text(json.dumps(out, indent=2))
    print('Complete:',out['total_seconds'],flush=True)

if __name__=='__main__':
    main()
