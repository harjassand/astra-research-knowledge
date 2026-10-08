"""Exact finite checks for the strongly-endotactic explosion witness.

The infinite-product and explosion proof is in FINAL_REPORT.md. This script
checks its finite algebra over exact rationals; it does not numerically
simulate an explosive process.
"""

from fractions import Fraction
from functools import cmp_to_key
from math import gcd
from pathlib import Path
import json


# Coordinates are (A, B). Reactions are listed as source, target, name.
REACTIONS = [
    ((0, 0), (2, 0), "r0"),       # 0 -> 2A
    ((2, 0), (4, 1), "r1"),       # 2A -> 4A+B
    ((4, 1), (6, 4), "r2"),       # 4A+B -> 6A+4B
    ((6, 4), (3, 0), "r3"),       # 6A+4B -> 3A
]
SOURCES = [source for source, _, _ in REACTIONS]
STOICH = [(target[0] - source[0], target[1] - source[1])
          for source, target, _ in REACTIONS]


def falling(n: int, k: int) -> int:
    if n < k:
        return 0
    out = 1
    for j in range(k):
        out *= n - j
    return out


def scaled_rates(n: int, V=Fraction(1), rates=None):
    """Three desired/total rates along one pump cycle at level n.

    Standard volume scaling is lambda_r^V(z) = k_r V^(1-|y|)
    product_i (z_i)_(y_i). Rate order is (r0,r1,r2,r3).
    """
    if rates is None:
        rates = (Fraction(1),) * 4
    k0, k1, k2, k3 = map(Fraction, rates)
    V = Fraction(V)

    # State (n,0): r1 is the desired next reaction; r0 competes.
    q0 = k0 * V
    q1 = k1 * falling(n, 2) / V
    stage1 = (q1, q0 + q1)

    # State (n+2,1): r2 is desired; r0 and r1 compete.
    a = n + 2
    q0 = k0 * V
    q1 = k1 * falling(a, 2) / V
    q2 = k2 * falling(a, 4) / V**4
    stage2 = (q2, q0 + q1 + q2)

    # State (n+4,4): r3 is desired; all earlier sources compete.
    a = n + 4
    q0 = k0 * V
    q1 = k1 * falling(a, 2) / V
    q2 = k2 * falling(a, 4) * falling(4, 1) / V**4
    q3 = k3 * falling(a, 6) * falling(4, 4) / V**9
    stage3 = (q3, q0 + q1 + q2 + q3)
    return stage1, stage2, stage3


def cycle_success(n: int, V=Fraction(1), rates=None) -> Fraction:
    return Fraction(1) * __import__("functools").reduce(
        lambda x, pair: x * pair[0] / pair[1], scaled_rates(n, V, rates), Fraction(1)
    )


def exact_prefix_probability(N: int, V=Fraction(1), rates=None) -> Fraction:
    """Probability of following all prescribed cycles n=3,...,N-1."""
    p = Fraction(1)
    for n in range(3, N):
        p *= cycle_success(n, V, rates)
    return p


def unit_rate_tail_competition_bound(N: int) -> Fraction:
    """Exact sum of competitor/desired ratios for all n >= N, V=k=1."""
    # q1_n = 1/(n)_2.
    q1 = Fraction(1, N - 1)

    # q2_n = 1/(n)_2 + 1/(n+2)_4.
    q2 = Fraction(1, N - 1) + Fraction(1, 3 * (N + 1) * N * (N - 1))

    # q3_n = 1/[6(n+4)_2] + 1/[24(n+4)_4] + 1/[24(n+4)_6].
    q3 = (
        Fraction(1, 6 * (N + 3))
        + Fraction(1, 72 * (N + 3) * (N + 2) * (N + 1))
        + Fraction(1, 120 * (N + 3) * (N + 2) * (N + 1) * N * (N - 1))
    )
    return q1 + q2 + q3


def normalize_ray(v):
    x, y = v
    g = gcd(abs(x), abs(y))
    assert g > 0
    x, y = x // g, y // g
    # Keep oriented rays; do not identify v and -v.
    return (x, y)


def half(v):
    x, y = v
    return 0 if (y > 0 or (y == 0 and x > 0)) else 1


def compare_angle(a, b):
    ha, hb = half(a), half(b)
    if ha != hb:
        return -1 if ha < hb else 1
    cross = a[0] * b[1] - a[1] * b[0]
    if cross:
        return -1 if cross > 0 else 1
    return 0


def exact_sweep_directions():
    """All ray boundaries where source maxima or reaction signs can change."""
    rays = set()

    def add_line_normal(v):
        x, y = v
        normal = normalize_ray((y, -x))
        rays.add(normal)
        rays.add((-normal[0], -normal[1]))

    for i, y in enumerate(SOURCES):
        for z in SOURCES[i + 1 :]:
            add_line_normal((z[0] - y[0], z[1] - y[1]))
    for v in STOICH:
        add_line_normal(v)

    ordered = sorted(rays, key=cmp_to_key(compare_angle))
    return ordered


def strong_endotactic_sweep():
    """Check the strong-endotactic sign conditions on all cells and rays.

    Source order and reaction-dot signs can change only at the enumerated
    exact rational directions. Rank(S)=2, so every nonzero w is admissible.
    """
    directions = exact_sweep_directions()
    candidates = list(directions)
    for i, a in enumerate(directions):
        b = directions[(i + 1) % len(directions)]
        # The arrangement has nonparallel lines, so each open angular gap is
        # strictly less than pi; a+b is an exact rational interior direction.
        assert a[0] * b[1] - a[1] * b[0] > 0
        w = (a[0] + b[0], a[1] + b[1])
        assert w != (0, 0)
        candidates.append(w)

    for w in candidates:
        dots = [w[0] * v[0] + w[1] * v[1] for v in STOICH]
        values = [w[0] * y[0] + w[1] * y[1] for y in SOURCES]
        top = max(values)
        active = [i for i, value in enumerate(values) if value == top]
        active_edges = [i for i, (source, _, _) in enumerate(REACTIONS)
                        if source in [SOURCES[j] for j in active]]
        assert active_edges
        assert all(dots[i] <= 0 for i in active_edges), (w, active, dots)
        assert any(dots[i] < 0 for i in active_edges), (w, active, dots)
    return len(candidates)


def class_macro_checks():
    v0, v1, v2, v3 = STOICH
    # Net pump r1,r2,r3 raises A by one and preserves B.
    assert tuple(sum(v[i] for v in (v1, v2, v3)) for i in range(2)) == (1, 0)
    # Exact decrement macro: r1 + 9 r2 + 7 r3 lowers A by one, preserves B.
    assert tuple(v1[i] + 9 * v2[i] + 7 * v3[i] for i in range(2)) == (-1, 0)
    # All products have A-count >= 2; on A>=3 no reaction can leave A>=3.
    assert min(target[0] for _, target, _ in REACTIONS) == 2
    assert all(target[0] >= 3 for _, target, _ in REACTIONS[1:])


def conditional_time_bound(V=Fraction(1), rates=None) -> Fraction:
    """Upper bound on route time conditional on following every chosen jump."""
    if rates is None:
        rates = (Fraction(1),) * 4
    _, k1, k2, k3 = map(Fraction, rates)
    V = Fraction(V)
    # Exact telescoping sums for n >= 3 under standard volume scaling.
    return V / (2 * k1) + V**4 / (72 * k2) + V**9 / (86400 * k3)


def main():
    class_macro_checks()
    sweep_cells = strong_endotactic_sweep()
    N = 100
    prefix = exact_prefix_probability(N)
    tail = unit_rate_tail_competition_bound(N)
    assert 0 < tail < 1
    # For p=1/(1+q), log p >= -q, so the infinite product tail is >= e^-Q
    # and e^-Q >= 1-Q for 0<=Q<=1. This is an exact rational lower bound.
    lower = prefix * (1 - tail)
    time_bound = conditional_time_bound()
    assert time_bound == Fraction(44401, 86400)

    # Standard volume scaling keeps the finite-level path probabilities
    # positive at arbitrary fixed integer volume. Check a rational example.
    V = Fraction(7, 3)
    assert all(0 < p < 1 for p in (
        stage[0] / stage[1] for stage in scaled_rates(3, V)
    ))

    T = 2 * time_bound
    capped_hit_lb = lower / 2
    # For count cap M>=107, choose N=M-7. All route states through (N,0)
    # have A+B<=M, so blocking outward reactions preserves this route.
    assert N + 7 == 107
    assert T == Fraction(44401, 43200)

    payload = {
        "schema_version": 1,
        "scope": "exact finite checks; infinite-product proof is in FINAL_REPORT.md",
        "strong_endotactic_sweep_candidates": sweep_cells,
        "volume_one_unit_rate_route": {
            "start": [3, 0],
            "level_N": N,
            "prefix_probability_exact": f"{prefix.numerator}/{prefix.denominator}",
            "tail_competitor_sum_exact": f"{tail.numerator}/{tail.denominator}",
            "infinite_success_probability_lower_exact": f"{lower.numerator}/{lower.denominator}",
            "infinite_success_probability_lower_decimal": float(lower),
            "conditional_time_mean_upper_exact": f"{time_bound.numerator}/{time_bound.denominator}",
            "time_horizon_2S_exact": f"{T.numerator}/{T.denominator}",
            "hard_total_count_cap_for_N": N + 7,
            "capped_chain_hit_by_2S_probability_lower_exact": f"{capped_hit_lb.numerator}/{capped_hit_lb.denominator}",
            "capped_chain_hit_by_2S_probability_lower_decimal": float(capped_hit_lb),
        },
        "volume_scaled_rational_fixture": {
            "V": "7/3",
            "level_n": 3,
            "rates": ["1", "1", "1", "1"],
            "stage_probabilities_exact": [
                f"{prob.numerator}/{prob.denominator}"
                for stage in scaled_rates(3, Fraction(7, 3))
                for prob in [stage[0] / stage[1]]
            ],
            "note": "all propensities and transition probabilities are positive rationals",
        },
    }
    out_path = Path(__file__).with_name("CHECK_OUTPUT.json")
    out_path.write_text(json.dumps(payload, indent=2) + "\n")

    print(f"exact strong-endotactic sweep candidates checked: {sweep_cells}")
    print(f"exact prefix probability through level {N}: {float(prefix):.12f}")
    print(f"exact tail sum bound from level {N}: {float(tail):.12g}")
    print(f"certified rational lower bound on infinite success probability: {float(lower):.12f}")
    print(f"conditional explosion-time expectation upper bound: {time_bound} = {float(time_bound):.12f}")
    print(f"hard-cap hit-by-2S probability lower bound: {float(capped_hit_lb):.12f}")
    print("rational volume-scaled stage propensities checked at V=7/3, level n=3")
    print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
