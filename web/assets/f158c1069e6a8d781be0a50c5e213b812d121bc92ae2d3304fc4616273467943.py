"""Numerical sanity checks of the derived formulas; not a proof certificate.

Uses only Python's standard library and records finite benchmark values.
"""

import json
import math
from pathlib import Path


def crossing(m, n):
    if n == 0:
        return 0
    return math.floor(m * math.log1p(1 / (n + 1)) / -math.log1p(-1 / (n + 1) ** 2))


def nb_cdf(m, n, cutoff, tolerance=1e-15):
    if cutoff < 0:
        return 0.0
    if n == 0:
        return 1.0
    ratio = n / (n + 1)
    mode = math.floor((m - 1) * n)
    center = min(mode, cutoff)
    log_mass = (
        math.lgamma(center + m) - math.lgamma(center + 1)
        - math.lgamma(m) - m * math.log(n + 1)
        + center * math.log(ratio)
    )
    mass = math.exp(log_mass)
    pieces = [mass]
    down = mass
    for k in range(center, 0, -1):
        step = k / (k + m - 1) / ratio
        down *= step
        pieces.append(down)
        # Subsequent ratios decrease, so the rest is bounded by a series.
        if step < 1 and down * step / (1 - step) < tolerance:
            break
    up = mass
    for k in range(center, cutoff):
        up *= (k + m) / (k + 1) * ratio
        pieces.append(up)
    return min(1.0, math.fsum(pieces))


def normal_cdf(x):
    return (1 + math.erf(x / math.sqrt(2))) / 2


def benchmark(m, n):
    cutoff = crossing(m, n)
    return cutoff, nb_cdf(m, n, cutoff) - nb_cdf(m, n + 1, cutoff)


def main():
    # The m=1 exact formula agrees with Guta--Bowles--Adesso IV.2.
    checks = []
    for n in [0, 1, 2, 10, 100]:
        cutoff, error = benchmark(1, n)
        exact = 0.5 if n == 0 else ((n + 1) / (n + 2)) ** (cutoff + 1) - (n / (n + 1)) ** (cutoff + 1)
        assert abs(error - exact) < 1e-12, (n, error, exact)
        checks.append({"m": 1, "N": n, "cutoff": cutoff, "error": error, "one_mode_formula": exact})

    profiles = []
    for c in [0.25, 1.0, 4.0]:
        limit = 2 * normal_cdf(math.sqrt(c) / 2) - 1
        for n in [10, 30, 100]:
            m = round(c * n * n)
            cutoff, error = benchmark(m, n)
            affinity = (math.sqrt(n + 2) + math.sqrt(n)) / (2 * math.sqrt(n + 1))
            lower = -math.expm1(m * math.log(affinity))
            upper = math.sqrt(-math.expm1(2 * m * math.log(affinity)))
            assert lower - 1e-8 <= error <= upper + 1e-8
            profiles.append({"c": c, "m": m, "N": n, "cutoff": cutoff, "error": error,
                             "normal_limit": limit, "absolute_difference": abs(error - limit),
                             "affinity_lower": lower, "affinity_upper": upper})

    result = {"status": "scoped numerical sanity checks passed", "one_mode": checks, "profiles": profiles}
    target = Path(__file__).with_name("negative_binomial_checks.json")
    target.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
