#!/usr/bin/env python3
"""Jointly screen d/slack and replay the selected r=2 finite gate.

The d/r screen is a scalar parameter search, not a proof of source transfer.
The selected (r,d,s) point is replayed with Decimal arithmetic, including the
integer even-p threshold and all numerical source hypotheses used here.
"""

from decimal import Decimal as D, getcontext
from math import ceil, log, log1p, sqrt

getcontext().prec = 70
LN2 = D(2).ln()


def decimal_point(r: int, d: int, slack: D):
    k = 2 * r * d
    c2 = 16 * r * r - 7 * r
    c = D(c2).sqrt()
    b1 = 1 + k
    h = (
        D(2) * D(k).ln()
        - D(k).ln() / D(k)
        - D(r - 1) / D(r) * LN2
    )
    gap = (
        D(2) * (-((D(k) + (c + slack) ** 2) / D(k) ** 2).ln())
        - h
    )

    eta = slack / (D(2) * D(k))
    e = slack / (D(6) * D(b1 + 1) * c)
    net_log = D(k * k - 1) * (D(1) + D(2) / eta).ln()
    conc_n = D(2) + D(96 * d * r) * (net_log + D(3).ln()) / (e / 2) ** 2

    p_power = 12 * d + 56
    n0 = 16 * (2 * d) ** 14
    n0d = D(n0)
    a = D(r * (r + 1)) / 2
    budget = (D(1) + e / 2).ln() / 2
    known_coeff = D(r + 1) * D(4 * b1).ln() + a * n0d.ln()
    p_coeff = D(3) * a + a * D(p_power)

    def known_log(p_int: int) -> D:
        p = D(p_int)
        return (known_coeff + p_coeff * p.ln()) / p

    # Find the least even p satisfying the decreasing-tail expectation gate.
    lo, hi = 2, 4
    while known_log(hi) > budget:
        lo, hi = hi, 2 * hi
    while hi - lo > 2:
        mid = ((lo + hi) // 4) * 2
        if mid <= lo:
            mid = lo + 2
        if known_log(mid) <= budget:
            hi = mid
        else:
            lo = mid
    p = hi
    if p % 2:
        p += 1
    while known_log(p) > budget:
        p += 2
    while p > 2 and known_log(p - 2) <= budget:
        p -= 2

    log2n = (n0d.ln() + D(p_power) * D(p).ln()) / LN2
    ln_n = n0d.ln() + D(p_power) * D(p).ln()
    hidden_log_upper = D(1560).ln() - ln_n / 2
    conc_log2 = conc_n.ln() / LN2

    # Source gates: ell_0 is tight at N=N0 p^(12d+56); its displayed
    # d^4 p^(4d+16)<=sqrt(N) consequence is checked independently.
    second_lhs_log = D(d**4).ln() + D(4 * d + 16) * D(p).ln()
    second_rhs_log = ln_n / 2
    weingarten_gate_log_lhs = D(2).ln() + D("3.5") * D(p).ln()
    weingarten_gate_log_rhs = D(2) * ln_n

    return {
        "r": r,
        "d": d,
        "K": k,
        "C2": c2,
        "slack": slack,
        "gap": gap,
        "eta": eta,
        "e": e,
        "net_log": net_log,
        "conc_log2N": conc_log2,
        "p_power": p_power,
        "N0": n0,
        "p": p,
        "log2p": D(p).ln() / LN2,
        "log2N": log2n,
        "per_use_qubits": D(r) * log2n,
        "two_use_qubits": D(2 * r) * log2n,
        "known_log": known_log(p),
        "known_budget": budget,
        "hidden_log_upper": hidden_log_upper,
        "source_second_moment_margin_log": second_rhs_log - second_lhs_log,
        "weingarten_margin_log": weingarten_gate_log_rhs - weingarten_gate_log_lhs,
        "N_ge_d70_margin_log": ln_n - D(70) * D(d).ln(),
    }


def float_screen(r: int, d: int, target_gap: float):
    k = 2 * r * d
    c = sqrt(16 * r * r - 7 * r)
    b1 = 1 + k

    def gap(s):
        return ((r - 1) / r) * log(2) + log(k) / k - 2 * log1p((c + s) ** 2 / k)

    if gap(0.0) <= target_gap:
        return None
    lo, hi = 0.0, 2 * c + 1
    for _ in range(70):
        mid = (lo + hi) / 2
        if gap(mid) >= target_gap:
            lo = mid
        else:
            hi = mid

    slack = lo
    e = slack / (6 * (b1 + 1) * c)
    p_power = 12 * d + 56
    ln_n0 = log(16 * (2 * d) ** 14)
    a = r * (r + 1) / 2
    budget = log1p(e / 2) / 2
    aa = (r + 1) * log(4 * b1) + a * ln_n0
    bb = 3 * a + a * p_power

    def known_log(p):
        return (aa + bb * log(p)) / p

    left, right = 2.0, 1e35
    for _ in range(100):
        mid = (left + right) / 2
        if known_log(mid) > budget:
            left = mid
        else:
            right = mid
    p = ceil(right / 2) * 2
    log2n = (ln_n0 + p_power * log(p)) / log(2)
    return {
        "r": r,
        "d": d,
        "gap0": gap(0.0),
        "slack_at_target": slack,
        "gap_at_target": gap(slack),
        "p_approx": p,
        "log2N_approx": log2n,
        "per_use_approx": r * log2n,
    }


if __name__ == "__main__":
    target = 0.001
    r2 = [float_screen(2, d, target) for d in range(62, 151)]
    r2 = [x for x in r2 if x is not None]
    print("R=2 screen, d=62..150, target gap=0.001 nats")
    for x in sorted(r2, key=lambda row: row["per_use_approx"])[:5]:
        print(x)

    print("R=3..10 screen, d=2..400, target gap=0.001 nats")
    for r in range(3, 11):
        rows = [float_screen(r, d, target) for d in range(2, 401)]
        rows = [x for x in rows if x is not None]
        print(None if not rows else min(rows, key=lambda row: row["per_use_approx"]))

    chosen = decimal_point(2, 65, D("0.165"))
    print("Selected exact Decimal replay: r=2,d=65,s=0.165")
    for key, value in chosen.items():
        print(f"{key}={value}")
    assert chosen["gap"] > D("0.001")
    assert chosen["known_log"] <= chosen["known_budget"]
    assert chosen["hidden_log_upper"] <= chosen["known_budget"].ln()
    assert chosen["conc_log2N"] < chosen["log2N"]
    assert chosen["source_second_moment_margin_log"] > 0
    assert chosen["weingarten_margin_log"] > 0
    assert chosen["N_ge_d70_margin_log"] > 0
