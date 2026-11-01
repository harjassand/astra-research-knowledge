"""Ordinary first-moment spectral bounds already earn leading Ising universality.

No Poisson solve, word sum, dynamical trajectory, or tensor approximation is used.
All displayed intervals are computed as exact Fractions. Formula-sized inputs
specify the complete family even when expanded fractions become long.
"""
from fractions import Fraction as F
import json
from pathlib import Path
import time


def solve(n, same=F(1), opposite=F(2)):
    start = time.perf_counter()
    assert n >= 4 and same > 0 and opposite > 0
    t = F(n-1, n+1)
    power = t**n
    gamma = F(n*n-1, n*n+1)
    # Exact periodic Ising magnetization variance and base response.
    variance = n*(1+t)/(1-t)*(1-power)/(1+power)
    chi0 = variance/(1-gamma)
    # Fraction of the base Dirichlet energy carried by equal-neighbor flips.
    p_same = (1-t*t)*(1+t**(n-2))/(2*(1-power))
    mean = opposite+(same-opposite)*p_same
    m, M = min(same, opposite), max(same, opposite)
    lower = chi0/mean
    upper = chi0*(m+M-mean)/(m*M)
    assert lower <= upper
    asymptotic = chi0/opposite
    return {
        "n": n, "same": str(same), "opposite": str(opposite),
        "lower": float(lower), "upper": float(upper),
        "relative_width": float((upper-lower)/lower),
        "midpoint_relative_error_certificate": float((upper-lower)/(lower+upper)),
        "normalized_spectral_mean": float(mean),
        "same_neighbor_dirichlet_fraction": float(p_same),
        "universality_prediction": float(asymptotic),
        "certified_prediction_relative_error_bound": float(max(abs(lower-asymptotic), abs(upper-asymptotic))/lower),
        "exact_recipe": "t=(n-1)/(n+1); gamma=(n^2-1)/(n^2+1); V=n(1+t)/(1-t)*(1-t^n)/(1+t^n); chi0=V/(1-gamma); p=(1-t^2)(1+t^(n-2))/(2(1-t^n)); a=opposite+(same-opposite)*p; [chi0/a, chi0*(min+max-a)/(min*max)]",
        "arithmetic": "exact rational endpoint evaluation; displayed decimal conversions are summaries",
        "seconds": time.perf_counter()-start,
    }


if __name__ == "__main__":
    out = []
    for n in [8, 16, 32, 64, 128, 256, 1024, 4096]:
        row = solve(n); out.append(row)
        print(json.dumps({k:row[k] for k in ["n", "relative_width", "same_neighbor_dirichlet_fraction", "seconds"]}), flush=True)
    # Swap kinetic classes: universality persists when the limiting rate is the
    # other spectral endpoint, showing this is not a faster-hopping-only trick.
    out.append(solve(128, same=F(3), opposite=F(1)))
    Path(__file__).with_name("critical_first_moment_results.json").write_text(json.dumps(out, indent=2)+"\n")
