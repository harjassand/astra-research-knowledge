"""Conditional, rational certificate processor for a maximal-start hitting law.

It DOES NOT acquire a microscopic capacity, residence bound, or mean.
Its inputs are already certified Q=N/C, normalized-capacity upper U,
core mean deficit D0, exterior residence fraction eta, and source rate kappa.
See RESEARCH_REPORT.txt for assumptions, proof, and complete cost contract.
Only Python's standard library is required.
"""

from fractions import Fraction as F
from math import isqrt


def sqrt_upper(x, bits=80):
    """Return a dyadic upper enclosure of sqrt(x), with error <= 2^-bits."""
    x = F(x)
    if x < 0 or bits < 1:
        raise ValueError("nonnegative input and positive precision required")
    a = x.numerator << (2 * bits)
    d = x.denominator
    k = isqrt(a // d)
    if k * k * d < a:
        k += 1
    return F(k, 1 << bits)


def exp_minus_interval(x, bits=80):
    """Rational interval for exp(-x), width <= 2^-bits, for rational x>=0.

    Large arguments are discarded only using e>2. For the remaining bounded
    arguments, the signed Taylor remainder is enclosed exactly. No external
    floating point library and no physical waiting time is used.
    """
    x = F(x)
    if x < 0 or bits < 1:
        raise ValueError("nonnegative input and positive precision required")
    tol = F(1, 1 << bits)
    if not x:
        return F(1), F(1)
    if x >= bits + 1:
        return F(0), tol
    partial, term, k = F(1), F(1), 0
    while True:
        nxt = term * x / (k + 1)
        if nxt <= tol:
            if k % 2 == 0:
                return max(F(0), partial - nxt), min(F(1), partial)
            return max(F(0), partial), min(F(1), partial + nxt)
        k += 1
        term = nxt
        partial += term if k % 2 == 0 else -term


def make_record(q_lower, q_upper, d0, capacity_upper, kappa, eta, bits=80):
    """Process valid prior certificates, without verifying their acquisition.

    q_lower <= Q=N/C <= q_upper;
    T - E_{pi(.|A)} m <= d0;
    C/Z_A <= capacity_upper < kappa;
    sum over D outside A of w v, divided by N, is at most eta.
    Ordered dynamics and an upward target ensure the least initial state is
    stochastically maximal for the hitting time.
    """
    qlo, qhi, d0, u, k, eta = map(F, (
        q_lower, q_upper, d0, capacity_upper, kappa, eta))
    if not (0 < qlo <= qhi and d0 >= 0 and 0 < u < k and 0 <= eta <= 1):
        raise ValueError("invalid scalar certificate ranges")
    tlo = max(qlo, 1 / u - 1 / k)
    thi = (1 + k * d0) * qhi + d0
    if tlo > thi:
        raise ValueError("the supplied bounds are inconsistent")
    s = u / k
    d_coarse = eta + k * d0 + u * d0 * (2 - s) / (1 - s) ** 2
    d_direct = 1 - qlo / thi + eta + d0 / ((1 - s) * tlo)
    defect = min(F(1), d_coarse, d_direct)
    if defect < 0:
        raise ValueError("inconsistent negative defect certificate")
    delta = min(F(1), 2 * sqrt_upper(defect, bits + 2))
    return {
        "q_lower": qlo, "q_upper": qhi, "d0": d0,
        "capacity_upper": u, "kappa": k, "eta": eta,
        "mean_lower": tlo, "mean_upper": thi,
        "defect_upper": defect, "kolmogorov_upper": delta,
        "wasserstein_upper": 2 * defect,
        "scope": "conditional on the supplied physical certificates",
    }


def cdf_interval(record, time, bits=80):
    """Enclose P(tau<=time) under a valid record, at every rational time."""
    t = F(time)
    if t < 0:
        return F(0), F(0)
    if t == 0:
        return F(0), F(0)
    d = record["kolmogorov_upper"]
    _, upper_slow = exp_minus_interval(t / record["mean_upper"], bits)
    lower_fast, _ = exp_minus_interval(t / record["mean_lower"], bits)
    return max(F(0), 1 - upper_slow - d), min(F(1), 1 - lower_fast + d)


def jsonable(x):
    if isinstance(x, F):
        return {"rational": str(x), "approx": float(x)}
    if isinstance(x, dict):
        return {k: jsonable(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [jsonable(v) for v in x]
    return x
