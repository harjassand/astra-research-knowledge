#!/usr/bin/env python3
"""Small scalar checks for the N46 depth bound and N61 cover stress test.

This does not construct the quantum channels, moment designs, or codes.
"""
import math


def depth_bound(m: int, b: float):
    alpha = math.log(2.0) / 2.0
    log_a = 0.5 * (math.log(m) + math.log(math.log(m)) - math.log(2.0))
    a = math.exp(log_a)
    l_star = math.log(alpha) + log_a - math.log(b)
    l_star /= alpha
    if l_star <= 0:
        candidates = (0, 1)
        continuous = a
    else:
        lo = math.floor(l_star)
        hi = math.ceil(l_star)
        candidates = (lo, hi)
        continuous = b * l_star + b / alpha
    f = lambda depth: depth * b + a * math.exp(-alpha * depth)
    best_l = min(candidates, key=f)
    return l_star, continuous, best_l, f(best_l)


def log_binomial(n: int, k: int) -> float:
    return math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)


def ladder_row(ell: int):
    m = 1 << (ell - 1)
    d = ell * m
    t = m + 1
    eta = ell ** -3

    f_upper = (m + 1) / (m + d)
    eb_lower = 1.0 - f_upper - 2.0 * eta
    b_upper = 1.0 / ell + eta

    # A maximal code with squared overlap <= 1/4 has at least this many
    # points. The log avoids materializing that exponentially large integer.
    log_pack = (d - 1) * math.log(4.0 / 3.0)
    # Caratheodory gives at most D_t^2 states for the exact moment witness.
    log_design_upper = 2.0 * log_binomial(d + t - 1, t)
    log_total_upper = max(log_pack, log_design_upper) + math.log(2.0)

    # ln N(a) is between these bounds for a < sqrt(3)/4, up to rounding.
    log_cover_lower = log_pack
    log_cover_upper = log_total_upper
    loglog_lower = math.log(log_cover_lower)
    loglog_upper = math.log(log_cover_upper)
    return {
        "ell": ell,
        "m": m,
        "d": d,
        "eb_lower": eb_lower,
        "b_upper": b_upper,
        "log_cover_lower": log_cover_lower,
        "log_cover_upper": log_cover_upper,
        "loglog_lower": loglog_lower,
        "loglog_upper": loglog_upper,
        "b_sqrt_loglog_range": (
            b_upper * math.sqrt(loglog_lower),
            b_upper * math.sqrt(loglog_upper),
        ),
        "b_logcover_lower": b_upper * log_cover_lower,
        "log_design_upper": log_design_upper,
    }


def main():
    print("N46 finite-tree bound (continuous and adjacent integer depths)")
    for ell in (4, 8, 12, 16, 20):
        m = 1 << (ell - 1)
        b = 1.0 / ell
        l_star, f_cont, l_int, f_int = depth_bound(m, b)
        print(
            f"ell={ell:2d} m={m:8d} L*={l_star:9.3f} "
            f"F_cont={f_cont:.6g} integer_L={l_int:9d} F_int={f_int:.6g}"
        )

    print("\nN61 finite-cover scalar scaling; fixed a < sqrt(3)/4")
    for ell in (4, 8, 12, 16, 20, 24):
        row = ladder_row(ell)
        low, high = row["b_sqrt_loglog_range"]
        print(
            f"ell={ell:2d} d={row['d']:12d} "
            f"e_EB_lower={row['eb_lower']:.8f} "
            f"b_upper={row['b_upper']:.8f} "
            f"lnlnN=[{row['loglog_lower']:.6f},{row['loglog_upper']:.6f}] "
            f"b*sqrt(lnlnN)=[{low:.6f},{high:.6f}] "
            f"b*lnN_lower={row['b_logcover_lower']:.6g}"
        )
        assert row["eb_lower"] > 0.5
        assert high < 2.0


if __name__ == "__main__":
    main()
