"""Evaluate the exact Gaussian-tail remainder bound from v7 at its finite diagnostic point."""
from __future__ import annotations
import json
import math


def tails(t: float) -> tuple[float, float, float]:
    r = math.sqrt(t)
    phi = math.exp(-t / 2) / math.sqrt(2 * math.pi)
    bar = 0.5 * math.erfc(r / math.sqrt(2))
    return (
        2 * bar,
        2 * (r * phi + bar),
        2 * ((t ** 1.5 + 3 * r) * phi + 3 * bar),
    )


def run(q: float = 1.0, sigma: float = 100.0, d: int = 3) -> dict:
    kappa = 1 / (8 * math.pi)
    s = sigma / q**2
    L = kappa * sigma**2 / q**2
    b = sigma**2 / (2 * L)
    p = sigma**2 / (4 * L**2 + sigma**2)
    t, tc = L / q**2, (L - b) / q**2
    t0, t2, _ = tails(t)
    c0, c2, c4 = tails(tc)
    remainder = (
        3 * p * q**2
        + 2 * p * L * (t2 + (d - 1) * t0)
        + q**2 * (c4 + (d - 1) * c2)
        + b * (c2 + (d - 1) * c0)
    )
    leading_gap = 2 * p * L / math.pi - 2 * q**2
    return {
        "q": q, "sigma": sigma, "d": d, "s": s, "kappa": kappa,
        "L": L, "b": b, "p": p, "t": t, "t_c": tc,
        "remainder_bound": remainder,
        "leading_e2_e3_gap": leading_gap,
        "certified_gap_after_two_remainders": leading_gap - 2 * remainder,
        "assumptions": {"b_le_L": b <= L, "t_c_nonnegative": tc >= 0},
        "scope": "Numerical evaluation of the exact v7 bound; no sampling or empirical fitting.",
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
