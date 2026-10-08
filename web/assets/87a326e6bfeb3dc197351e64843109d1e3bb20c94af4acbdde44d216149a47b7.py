#!/usr/bin/env python3
"""Finite-state design audit for the Kocka et al. protein-automata model.

Only Python's standard library is required.  The generator is enumerated exactly
from the stated channels, while its linear systems are solved in binary64.
For a rational-rate exact-arithmetic fixture see ``exact_rate_audit.py``.
States are N-bit rings. Rule number
uses the standard Wolfram convention f_r(p)=(r>>p)&1, p=4*left+2*center+right.
For every motif p with f_r(p) != center(p), one enzyme catalyses p -> p^flip
at kcat*exp(A)/(1+exp(A)); the same enzyme catalyses the reverse with rate
kcat/(1+exp(A)). Independent spontaneous flips occur at k_spo per site.

The program computes (i) exact one-error repair-vs-new-error races and (ii)
exact mean first-passage time from the all-zero codeword to a majority-one
readout. It also charges gross ATP hydrolysis and net chemical work using the
enzyme-resolved reaction channels; spontaneous transitions consume no ATP.
"""

from __future__ import annotations

import argparse
import json
import math
from typing import Dict, Iterable, List, Sequence, Tuple


def bit(state: int, site: int) -> int:
    return (state >> site) & 1


def motif(state: int, site: int, n: int) -> int:
    left = bit(state, (site - 1) % n)
    center = bit(state, site)
    right = bit(state, (site + 1) % n)
    return 4 * left + 2 * center + right


def rule_output(rule: int, p: int) -> int:
    return (rule >> p) & 1


def enzymes(rule: int) -> Tuple[int, ...]:
    return tuple(p for p in range(8) if rule_output(rule, p) != ((p >> 1) & 1))


def flip_center(p: int) -> int:
    return p ^ 2


def outgoing(state: int, n: int, rule: int, kcat: float, affinity: float,
             k_spo: float) -> List[Tuple[int, float, float, float]]:
    """Return (next_state, total_rate, gross_hydrolysis_rate, reverse_rate).

    Gross hydrolysis includes only forward enzymatic channel flux. Reverse
    events are reported separately because they return one fuel molecule in
    the idealized LDB reaction. Parallel spontaneous/enzyme channels are
    aggregated only after their energy labels have been recorded.
    """
    e = set(enzymes(rule))
    fwd = kcat * math.exp(affinity) / (1.0 + math.exp(affinity))
    rev = kcat / (1.0 + math.exp(affinity))
    out: Dict[int, List[float]] = {}
    for site in range(n):
        p = motif(state, site, n)
        q = flip_center(p)
        nxt = state ^ (1 << site)
        # Enzyme p drives p -> q; enzyme q catalyses its own reverse q -> p.
        h = fwd if p in e else 0.0
        r = rev if q in e else 0.0
        total = k_spo + h + r
        if total == 0.0:
            continue
        slot = out.setdefault(nxt, [0.0, 0.0, 0.0])
        slot[0] += total
        slot[1] += h
        slot[2] += r
    return [(t, v[0], v[1], v[2]) for t, v in out.items()]


def solve_linear(a: List[List[float]], b: List[float]) -> List[float]:
    """Partial-pivot Gaussian elimination for the small transient systems."""
    n = len(b)
    m = [row[:] + [b[i]] for i, row in enumerate(a)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda row: abs(m[row][col]))
        if abs(m[pivot][col]) < 1e-14:
            raise ArithmeticError("singular transient generator; check reachability")
        if pivot != col:
            m[col], m[pivot] = m[pivot], m[col]
        scale = m[col][col]
        for j in range(col, n + 1):
            m[col][j] /= scale
        for row in range(n):
            if row == col:
                continue
            factor = m[row][col]
            if factor != 0.0:
                for j in range(col, n + 1):
                    m[row][j] -= factor * m[col][j]
    return [m[i][n] for i in range(n)]


def scaled_residual(a: List[List[float]], x: Sequence[float],
                    b: Sequence[float]) -> float:
    """Return a diagnostic scaled infinity residual (not an interval proof)."""
    worst = 0.0
    for row, target in zip(a, b):
        value = sum(coef * xi for coef, xi in zip(row, x))
        scale = max(1.0, abs(target) + sum(abs(coef * xi)
                                          for coef, xi in zip(row, x)))
        worst = max(worst, abs(value - target) / scale)
    return worst


def first_passage_and_fuel(n: int, rule: int, kcat: float, affinity: float,
                           k_spo: float) -> dict:
    """Exact CTMC mean time/work to first wrong majority readout (odd N)."""
    if n % 2 != 1:
        raise ValueError("majority decoder fixture requires odd N")
    cutoff = n // 2
    safe = [s for s in range(1 << n) if s.bit_count() <= cutoff]
    ix = {s: i for i, s in enumerate(safe)}
    m = len(safe)
    minus_q = [[0.0] * m for _ in range(m)]
    gross_h = [0.0] * m
    reverse = [0.0] * m
    for state in safe:
        i = ix[state]
        for target, rate, hyd, rev in outgoing(state, n, rule, kcat, affinity, k_spo):
            minus_q[i][i] += rate
            if target in ix:
                minus_q[i][ix[target]] -= rate
            gross_h[i] += hyd
            reverse[i] += rev
    mean_t_vec = solve_linear(minus_q, [1.0] * m)
    hydrolysis_vec = solve_linear(minus_q, gross_h)
    reverse_vec = solve_linear(minus_q, reverse)
    mean_t = mean_t_vec[ix[0]]
    expected_hydrolysis = hydrolysis_vec[ix[0]]
    expected_reverse = reverse_vec[ix[0]]
    return {
        "mean_first_passage_to_wrong_majority": mean_t,
        "expected_ATP_hydrolyses_before_wrong_majority": expected_hydrolysis,
        "expected_reverse_fuel_returns_before_wrong_majority": expected_reverse,
        "expected_net_ATP_consumed": expected_hydrolysis - expected_reverse,
        "scaled_linear_residuals_binary64": {
            "mean_time": scaled_residual(minus_q, mean_t_vec, [1.0] * m),
            "gross_fuel": scaled_residual(minus_q, hydrolysis_vec, gross_h),
            "reverse_fuel": scaled_residual(minus_q, reverse_vec, reverse),
        },
        "numerical_note": "finite generator solved in binary64; residuals are diagnostics, not interval certificates",
        "transient_states": m,
        "enzyme_motifs": list(enzymes(rule)),
        "enzyme_species_count": len(enzymes(rule)),
        "per_species_kcat": kcat,
        "beta_delta_mu": affinity,
        "spontaneous_flip_rate_per_site": k_spo,
    }


def one_error_race(n: int, rule: int, kcat: float, affinity: float,
                   k_spo: float) -> dict:
    """Exact next-jump probability of clean correction from a one-bit error."""
    if n < 4:
        raise ValueError("use N>=4 so the two neighbours are distinct")
    state = 1  # one 1-bit on an otherwise all-zero ring
    rates = {"repair_to_codeword": 0.0, "additional_error": 0.0,
             "other": 0.0, "repair_hydrolysis": 0.0,
             "repair_reverse": 0.0}
    for target, total, hyd, rev in outgoing(state, n, rule, kcat, affinity, k_spo):
        weight = target.bit_count()
        if target == 0:
            rates["repair_to_codeword"] += total
            rates["repair_hydrolysis"] += hyd
            rates["repair_reverse"] += rev
        elif weight > 1:
            rates["additional_error"] += total
        else:
            rates["other"] += total
    total = rates["repair_to_codeword"] + rates["additional_error"] + rates["other"]
    rates["total_outgoing_rate"] = total
    rates["clean_repair_probability_next_jump"] = rates["repair_to_codeword"] / total
    return rates


def symmetric_code_rules() -> List[int]:
    """Rules whose 0^N/1^N are both fixed and which are bit-flip symmetric."""
    answer = []
    for r in range(256):
        f = [rule_output(r, p) for p in range(8)]
        if f[0] == 0 and f[7] == 1 and all(f[p] == 1 - f[7 - p] for p in range(8)):
            answer.append(r)
    return answer


def run(args: argparse.Namespace) -> dict:
    selected_rules = args.rules if args.rules else symmetric_code_rules()
    reports = []
    total_enzyme_capacity = args.total_enzyme_capacity
    for rule in selected_rules:
        m = len(enzymes(rule))
        if m == 0:
            continue
        kcat = args.kcat if not total_enzyme_capacity else total_enzyme_capacity / m
        reports.append({
            "rule": rule,
            "one_error_race": one_error_race(args.n, rule, kcat, args.affinity, args.k_spo),
            "majority_decoder": first_passage_and_fuel(args.n, rule, kcat, args.affinity, args.k_spo),
        })
    return {
        "model": "binary N-ring; standard Wolfram local rule; local detailed balance; symmetric spontaneous flips",
        "N": args.n,
        "affinity_parameter": "A=beta*Delta_mu",
        "dimensionless_affinity": args.affinity,
        "spontaneous_flip_rate_per_site": args.k_spo,
        "rate_normalization": "fixed per-enzyme kcat" if not total_enzyme_capacity else "fixed sum of enzyme kcat capacities",
        "common_kcat_or_total_capacity": args.kcat if not total_enzyme_capacity else total_enzyme_capacity,
        "solver": "partial-pivot Gaussian elimination in binary64",
        "rules": reports,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=7)
    parser.add_argument("--affinity", type=float, default=5.0,
                        help="dimensionless beta*Delta_mu")
    parser.add_argument("--k-spo", type=float, default=0.001,
                        help="spontaneous rate per site, relative to kcat units")
    parser.add_argument("--kcat", type=float, default=1.0,
                        help="per-species catalytic capacity unless total capacity set")
    parser.add_argument("--total-enzyme-capacity", type=float, default=0.0,
                        help="if positive, set per-species kcat = this value / enzyme count")
    parser.add_argument("--rules", type=int, nargs="*", default=None,
                        help="rule codes; default enumerates bit-symmetric 0/1 memory rules")
    args = parser.parse_args()
    print(json.dumps(run(args), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
