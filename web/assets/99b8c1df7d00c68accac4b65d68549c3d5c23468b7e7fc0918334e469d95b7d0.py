"""Scoped checks of two computational adapters, not a run of family 139.

The exact covariance arithmetic uses Fraction. Floating integration below is
only a diagnostic for the proved strong-convexity tilt inequality.
"""
from fractions import Fraction as F
import json
import math
from pathlib import Path
import random
import time
import tracemalloc

ROOT = Path(__file__).resolve().parent


def rank_one_seed_transform(seeds, shift, D_s):
    """Apply (I-vv^T/(4D_s^2))^(1/2) tensor I_d in O(md)."""
    m = len(seeds)
    d = len(seeds[0])
    norm2 = sum(v*v for v in shift)
    c = norm2 / (4*D_s*D_s)
    if not 0 <= c <= 0.25 + 1e-14:
        raise ValueError("Translation budget is not certified")
    scalar = 1 / (4*D_s*D_s*(1 + math.sqrt(1-c)))
    shared = [sum(shift[j]*seeds[j][k] for j in range(m))
              for k in range(d)]
    scaled_shift = [scalar*v for v in shift]
    out = [[seeds[j][k] - scaled_shift[j]*shared[k]
            for k in range(d)] for j in range(m)]
    # Conservative count, excluding the input and random-seed acquisition.
    return out, {"multiplications_upper_bound": 2*m*d + 2*m + 20,
                 "additions": (2*m-1)*d + m + 3,
                 "square_roots": 1,
                 "stored_output_reals": m*d}


def exact_absorption_check():
    # sqrt(1-c)=12/13 makes the covariance identity rational and exact.
    # m=4, v=(-1,...,-1), D_s=13/5 >= ||v||=2, n=5/26.
    m = 4
    shift = [-F(1) for _ in range(m)]
    D_s = F(13, 5)
    n = F(1)/(2*D_s)
    alpha = F(1)/(4*D_s*D_s*(1+F(12,13)))
    P = [[F(i == j)-alpha*shift[i]*shift[j]
          for j in range(m)] for i in range(m)]
    assertions = 0
    for i in range(m):
        for j in range(m):
            covariance = sum(P[i][k]*P[j][k] for k in range(m))
            covariance += n*n*shift[i]*shift[j]
            assert covariance == F(i == j)
            assertions += 1
    # Unmodified fresh seeds would increase diagonal and off-diagonal terms.
    assert F(1)+n*n > 1
    assert n*n > 0
    assertions += 2
    # A variance-matched Rademacher center is not Gaussian: its contribution
    # has fourth cumulant -2 n^4, so covariance matching is insufficient.
    non_gaussian_fourth_cumulant = -2*n**4
    assert non_gaussian_fourth_cumulant != 0
    assertions += 1
    return {"assertions": assertions,
            "covariance_identity": "exact Fraction arithmetic",
            "uncorrected_seed_variance_excess": str(n*n),
            "Rademacher_center_fourth_cumulant": str(non_gaussian_fourth_cumulant),
            "scope": "adapter identity only; no family 139 sampler executed"}


def query_preserving_check():
    rng = random.Random(970139)
    m, d, r = 7, 5, 0.3
    x = [rng.uniform(-1,1) for _ in range(d)]
    displacement = [rng.uniform(-1,1) for _ in range(d)]
    seeds = [[rng.gauss(0,1) for _ in range(d)] for _ in range(m)]
    shift = [-1.0]*m
    points_a = [[x[k]+r*seeds[j][k] for k in range(d)] for j in range(m)]
    points_b = [[x[k]+displacement[k]
                 +r*(seeds[j][k]+shift[j]*displacement[k]/r)
                 for k in range(d)] for j in range(m)]
    error = max(abs(a-b) for row_a,row_b in zip(points_a,points_b)
                for a,b in zip(row_a,row_b))
    assert error < 1e-14
    return {"physical_query_max_error": error, "queries_per_call": m,
            "scope": "pathwise query cancellation for an explicit multiquery routine"}


def integration_probe():
    # V(x)=x^2/2+log cosh(x-3), with 1<=V''<=2.
    def logcosh(x):
        return abs(x)+math.log1p(math.exp(-2*abs(x)))-math.log(2)
    def V(x):
        return x*x/2+logcosh(x-3)
    def gradient(x):
        return x+math.tanh(x-3)
    B = abs(gradient(0))
    results = []
    for residual_goal in [0.05,0.1,0.2]:
        steps = math.ceil(math.log2(4*B/residual_goal))
        center = 0.0
        for _ in range(steps):
            center -= gradient(center)/2
        residual = gradient(center)
        assert abs(residual) <= residual_goal
        # Composite Simpson quadrature, no outward-rounded certification.
        n, left, right = 20000,-12.0,12.0
        dx = (right-left)/n
        grid = [left+i*dx for i in range(n+1)]
        w = [1 if i in (0,n) else 4 if i%2 else 2 for i in range(n+1)]
        base = [math.exp(-V(x)) for x in grid]
        tilt = [math.exp(-V(x)+residual*x) for x in grid]
        Zp = dx/3*sum(a*b for a,b in zip(w,base))
        Zq = dx/3*sum(a*b for a,b in zip(w,tilt))
        p = [v/Zp for v in base]
        q = [v/Zq for v in tilt]
        tv = dx/6*sum(wi*abs(pi-qi) for wi,pi,qi in zip(w,p,q))
        kl = dx/3*sum(wi*pi*math.log(pi/qi) for wi,pi,qi in zip(w,p,q))
        assert tv <= abs(residual)/2+1e-10
        assert kl <= residual*residual/2+1e-10
        results.append({"requested_gradient_residual": residual_goal,
                        "optimization_gradient_calls": steps+2,
                        "acquired_center": center,
                        "true_gradient_residual": residual,
                        "diagnostic_TV": tv,
                        "proved_TV_upper_bound": abs(residual)/2,
                        "diagnostic_KL": kl,
                        "proved_KL_upper_bound": residual*residual/2})
    return {"potential": "x^2/2 + log cosh(x-3)",
            "scope": "floating quadrature probe, not a certificate or runtime comparison",
            "cases": results}


def resource_probe():
    rng = random.Random(139)
    rows = []
    for m,d in [(32,64),(64,64),(128,64),(256,64),(128,128)]:
        seeds = [[rng.gauss(0,1) for _ in range(d)] for _ in range(m)]
        shift = [(-1.0 if j%2 else 1.0)/math.sqrt(m) for j in range(m)]
        tracemalloc.start()
        start = time.perf_counter()
        _, ledger = rank_one_seed_transform(seeds,shift,1.0)
        elapsed = time.perf_counter()-start
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        rows.append({"seed_slots":m,"dimension":d,"elapsed_seconds":elapsed,
                     "additional_peak_traced_bytes":peak,"operation_ledger":ledger})
    return {"scope":"one rank-one adapter, excluding seed acquisition; timings are diagnostics",
            "cases":rows}


if __name__ == "__main__":
    result = {"exact_absorption":exact_absorption_check(),
              "query_preservation":query_preserving_check(),
              "centering_tilt_probe":integration_probe(),
              "resource_probe":resource_probe()}
    (ROOT/"adapter_checks.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"exact_assertions":result["exact_absorption"]["assertions"],
                      "centering_cases":len(result["centering_tilt_probe"]["cases"]),
                      "resource_cases":len(result["resource_probe"]["cases"]),
                      "scope":"Scoped adapters passed; full source sampler not implemented"}))
