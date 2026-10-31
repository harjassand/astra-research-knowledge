#!/usr/bin/env python3
"""Exact power comparison on the same one-trajectory acquisition contract."""
from fractions import Fraction
from pathlib import Path
import json
import math
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "outputs/reversible_currents"))
from currents import (binomial_power, critical_score, fraction_json, log_bounds,
                      lower_rate_interval, q_bound)


def martingale_critical(n, alpha):
    # 2 exp(-(s-1)^2/(2n)) <= alpha, decided using an exact log enclosure.
    loglo, loghi = log_bounds(2/alpha)
    for s in range(n % 2, n+1, 2):
        exponent = Fraction(max(s-1, 0)**2, 2*n)
        if exponent >= loghi:
            return s
        assert not loglo <= exponent < loghi, "increase log precision"
    return None


def search():
    alpha = beta = Fraction(1, 40)
    first = {}
    rows = []
    for n in range(1, 1001):
        c = critical_score(n, alpha)
        m = martingale_critical(n, alpha)
        p = binomial_power(n, c)
        pm = binomial_power(n, m)
        if p >= 1-beta and "cover_chernoff" not in first:
            first["cover_chernoff"] = {"n": n, "critical": c,
                "power": fraction_json(p), "power_decimal": float(p)}
        if pm >= 1-beta and "forward_backward" not in first:
            first["forward_backward"] = {"n": n, "critical": m,
                "power": fraction_json(pm), "power_decimal": float(pm)}
        if n in (20, 50, 100, 150, 200, 500, 1000) or (
                first.get("cover_chernoff", {}).get("n") == n) or (
                first.get("forward_backward", {}).get("n") == n):
            rows.append({"n": n, "chernoff_critical": c, "power": float(p),
                "martingale_critical": m, "martingale_power": float(pm)})
        if len(first) == 2 and n >= 1000:
            break
    n = first["cover_chernoff"]["n"]
    s = first["cover_chernoff"]["critical"]
    # Aperiodic model: no-hold histories alone give this exact power lower bound.
    # Pick n at 99% power to leave space for the explicitly charged laziness.
    for lazy_n in range(1, 1001):
        lazy_s = critical_score(lazy_n, alpha)
        base_power = binomial_power(lazy_n, lazy_s)
        hold = Fraction(1, 100000)
        lazy_power = (1-hold)**lazy_n * base_power
        if lazy_power >= 1-beta:
            break
    sample_endpoints = []
    for n0, s0 in ((n, s), (n, n), (1000, 500), (1000, 1000)):
        lo, hi = lower_rate_interval(n0, s0, alpha)
        sample_endpoints.append({"n": n0, "absolute_score": s0,
            "null_bound": fraction_json(q_bound(n0, s0)),
            "rate_enclosure": [fraction_json(lo), fraction_json(hi)],
            "rate_preview": float(lo), "enclosure_width": float(hi-lo)})
    result = {
        "contract": "one stationary source trajectory; fixed n; no resets or mixing bound",
        "alpha": fraction_json(alpha), "beta": fraction_json(beta),
        "source_b": "1/2", "source_sign_probability": "3/4",
        "source_entropy_rate": "log(3)/2 nats/step",
        "first_horizons_up_to_search_limit": first,
        "comparisons": rows,
        "aperiodic_source": {"hold_probability": fraction_json(hold),
            "n": lazy_n, "observations": lazy_n+1,
            "critical": lazy_s, "power_lower": fraction_json(lazy_power),
            "power_lower_decimal": float(lazy_power)},
        "sample_endpoints": sample_endpoints,
        "scope": "exact finite-source power calculation, not physical data or a general power theorem",
    }
    target = ROOT / "work/reversible_current_power.json"
    target.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({"first": first, "aperiodic_n": lazy_n,
        "aperiodic_power_lower": float(lazy_power),
        "sample_endpoints": [{k:v for k,v in r.items() if k not in
             ("null_bound", "rate_enclosure")} for r in sample_endpoints]}, indent=2))


if __name__ == "__main__":
    search()
