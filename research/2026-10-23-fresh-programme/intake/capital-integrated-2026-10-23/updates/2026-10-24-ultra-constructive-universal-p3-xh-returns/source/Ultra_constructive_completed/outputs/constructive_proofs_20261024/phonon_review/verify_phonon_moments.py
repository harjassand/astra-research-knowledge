#!/usr/bin/env python3
"""Independent challenge of the full-band moments and the declared optimum.

This checks arbitrary connected non-star cells as well as exact rational
hyperbolic endpoint premises. It does not replace the spectral/dual proof.
Only NumPy and the Python standard library are used. No owner files written.
"""
from fractions import Fraction as R
import json
import math
from pathlib import Path

import numpy as np


def rational_endpoint_premises():
    # 1+1/2!+1/4! < cosh(1) < that sum + (1/6!)/(1-1/56).
    c_lo = R(37, 24)
    c_hi = c_lo + R(7, 4950)
    t_lo, t_hi = c_lo**2, c_hi**2
    assert t_lo > R(86, 37) and t_hi < R(13, 5)
    assert t_lo > R(16, 7)
    # For t=cosh(1)^2, h2/h1=2/t. These two rational inequalities give
    # b3<0<b4 in the owner's entire-function proof.
    assert R(2) / t_hi > R(10, 13)
    assert R(2) / t_lo < R(37, 43)
    # t F(4)/h1 = v(t), strictly increasing on this interval.
    vv = lambda t: 4*t - 10 + 4/(2*t - 1)**2
    assert 4 - 16/(2*t_lo - 1)**3 > 0
    assert vv(t_hi) < 0
    # F(5)/h1 =125/(16t^2-12t+1)^2 +7-16/t >0.
    assert 7 - 16/t_lo > 0
    return {"cosh1_lower": str(c_lo), "cosh1_upper": str(c_hi),
            "F4_scaled_rational_upper": str(vv(t_hi)),
            "status": "exact rational coefficient and F4/F5 sign premises passed"}


def weight(w):
    ww = np.asarray(w, dtype=float)
    out = np.ones_like(ww)
    mask = ww > 0
    out[mask] = (2*ww[mask]*np.exp(-ww[mask])/(-np.expm1(-2*ww[mask])))**2
    return out


def dual(x):
    h1 = 1/math.sinh(1)**2
    h2 = 8/math.sinh(2)**2
    mu = (h1-h2)/6
    lam = -(4*h1-h2)/3
    return x**3/math.sinh(x)**2 + lam + 2*mu*x*x


def third_root():
    lo, hi = 4., 5.
    for _ in range(60):
        mid = (lo+hi)/2
        if dual(mid) < 0:
            lo = mid
        else:
            hi = mid
    return (lo+hi)/2


GX, GW = np.polynomial.legendre.leggauss(160)


def integrate_band(a, b):
    return float((b-a)/2*np.dot(GW, weight((a+b)/2+(b-a)*GX/2)))


def cell(masses, edges, kk):
    masses = np.asarray(masses, dtype=float)
    nn = len(masses)
    lap = np.zeros((nn, nn))
    for i, j, stiffness in edges:
        lap[i, i] += stiffness
        lap[j, j] += stiffness
        lap[i, j] -= stiffness
        lap[j, i] -= stiffness
    invroot = np.diag(1/np.sqrt(masses))
    dd0 = invroot @ lap @ invroot
    vv = np.zeros(nn)
    vv[0] = 1/math.sqrt(masses[0])
    dd1 = dd0 + 4*kk*np.outer(vv, vv)
    aa, bb = np.linalg.eigvalsh(dd0), np.linalg.eigvalsh(dd1)
    assert abs(aa[0]) < 1e-8 and np.all(bb > 0)
    assert nn == 1 or np.all(aa[1:] > 0)
    spectral_scale = 1+np.linalg.norm(dd1, 2)
    assert np.min(bb-aa) > -1e-10*spectral_scale
    assert nn == 1 or np.max(bb[:-1]-aa[1:]) < 1e-10*spectral_scale
    trace = float(np.sum(bb-aa))
    trace_target = 4*kk/masses[0]
    log_ratio = float(np.sum(np.log(bb))-np.sum(np.log(aa[1:])))
    log_target = math.log(4*kk/sum(masses))
    widths = np.sqrt(bb)-np.sqrt(np.maximum(aa, 0))
    aa[0] = 0.
    score = sum(integrate_band(math.sqrt(a), math.sqrt(b)) for a, b in zip(aa, bb))
    return dict(trace_relative_error=abs(trace-trace_target)/(1+trace_target),
                log_error=abs(log_ratio-log_target), score=score,
                width=float(sum(widths)), rigid_width=2*math.sqrt(kk/sum(masses)),
                alpha=aa.tolist(), beta=bb.tolist())


def main():
    exact = rational_endpoint_premises()
    cc = third_root()
    kk = (cc*cc-3)/4
    mt = 4-12/(cc*cc)
    ms = mt-1
    kin = 4*ms/mt
    optimum = cell([1, ms], [(0, 1, kin)], kk)
    target_score = integrate_band(0, 1)+integrate_band(2, cc)
    rigid = cell([mt], [], kk)
    assert np.max(np.abs(np.array(optimum["alpha"])-[0, 4])) < 1e-12
    assert np.max(np.abs(np.array(optimum["beta"])-[1, cc*cc])) < 1e-12
    assert abs(optimum["score"]-target_score) < 1e-12

    # Different connected topologies, broad positive spring scales, varied
    # admissible backbone mass, with ALL optical bands retained.
    rng = np.random.default_rng(20261024)
    tests = []
    for nn in range(2, 11):
        for trial in range(20):
            backbone = rng.uniform(1, .95*mt)
            rest = rng.dirichlet(np.ones(nn-1))*(mt-backbone)
            masses = [backbone]+rest.tolist()
            edges = [(j, j+1, float(np.exp(rng.uniform(-3, 3)))) for j in range(nn-1)]
            for i in range(nn):
                for j in range(i+2, nn):
                    if rng.random() < .4:
                        edges.append((i, j, float(np.exp(rng.uniform(-3, 3)))))
            out = cell(masses, edges, kk)
            assert out["trace_relative_error"] < 1e-10
            assert out["log_error"] < 1e-8
            assert out["width"] >= out["rigid_width"]-1e-6
            assert out["score"] >= target_score-1e-7
            tests.append(out)

    # Repeated/dark internal eigenmodes: symmetric equal side masses.
    dark = cell([1, ms/2, ms/2], [(0, 1, kin/2), (0, 2, kin/2)], kk)
    assert min(abs(b-a) for a, b in zip(dark["alpha"], dark["beta"])) < 1e-12
    assert abs(dark["score"]-optimum["score"]) < 1e-12

    # Actual passive two-mass countercontrol violating only m>=1.
    tiny_backbone = 1e-5
    outside = cell([tiny_backbone, mt-tiny_backbone], [(0, 1, .01)], kk)
    assert outside["score"] < .1*target_score

    mu = (1/math.sinh(1)**2-8/math.sinh(2)**2)/6
    strict_analytic_margin = mu*4*kk*(1-1/mt)
    assert strict_analytic_margin > 0
    output = dict(exact_endpoint_premises=exact, c=cc,
                  optimum=optimum, rigid=rigid,
                  actual_score_reduction_fraction=1-optimum["score"]/rigid["score"],
                  dual_strict_rigid_margin=strict_analytic_margin,
                  connected_random_cells=len(tests),
                  maximum_trace_error=max(t["trace_relative_error"] for t in tests),
                  maximum_log_error=max(t["log_error"] for t in tests),
                  smallest_admissible_score_minus_optimum=min(t["score"]-target_score for t in tests),
                  exact_dark_mode_case=dark,
                  excluded_mass_floor_countercontrol=outside,
                  scope="finite checks and exact endpoint premises; analytic dual proof still required")
    destination = Path(__file__).with_name("replay.json")
    destination.write_text(json.dumps(output, indent=2)+"\n")
    print(json.dumps({k:v for k,v in output.items() if k not in ("optimum", "rigid", "exact_dark_mode_case", "excluded_mass_floor_countercontrol")}, indent=2))


if __name__ == "__main__":
    main()
