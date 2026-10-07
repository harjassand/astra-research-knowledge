"""Finite exact diagnostics for result 279's deferred dyadic completion.

These check finite instances, not the underlying order-trial theorem.
Python standard library only; all probabilities are fractions.Fraction.
"""

from fractions import Fraction as F
import json


def completion(s, W, t, z):
    delta = F(1, 2**t)
    A = (1 - delta) * s
    assert 0 < z <= A
    E = W + t + 2
    scaled = z / A * 2**E
    C = F(scaled.numerator // scaled.denominator, 2**E)
    R = z - C * A
    q = R * 2**W / delta
    assert 0 <= C <= 1
    assert 0 <= R < A / 2**E
    assert 0 <= q < F(1, 4)
    assert A * C + delta * F(1, 2**W) * q == z
    assert C.denominator & (C.denominator - 1) == 0
    assert q.denominator & (q.denominator - 1) == 0
    return C, q


count = 0
for W in range(6):
    for t in range(1, 7):
        for numerator in range(1, 33):
            s = F(numerator, 32)
            A = (1 - F(1, 2**t)) * s
            for z_numerator in range(1, 65):
                z = F(z_numerator, 64)
                if z <= A:
                    completion(s, W, t, z)
                    count += 1
            # A dyadic endpoint gives C=1 and residual=0.
            C, q = completion(s, W, t, A)
            assert C == 1 and q == 0
            count += 1

# An adaptive controller with mixed bad branches, valid completed bad
# histories, aborted histories, invalid-data histories, and early padding.
W, t, z, L = 2, 2, F(1, 4), 3
delta = F(1, 2**t)
specs = {
    "start": ([F(1, 8), F(1, 2), F(1, 4), F(1, 8)], {1, 2}, 1),
    "a": ([F(1, 2), F(1, 4), F(1, 8), F(1, 8)], {0, 1}, 0),
    "b": ([F(1, 8), F(1, 8), F(1, 2), F(1, 4)], {2}, 2),
    "dummy": ([F(1), F(0), F(0), F(0)], {0}, 0),
}


def next_state(state, y):
    if state == "start":
        return ["abort", "a", "b", "dummy"][y]
    if state == "a":
        return ["dummy", "dummy", "abort", "dummy"][y]
    if state == "b":
        return ["dummy", "invalid", "dummy", "abort"][y]
    if state == "dummy":
        return "dummy" if y == 0 else "abort"
    raise AssertionError(state)


def retention(state, branch, y):
    distribution, good, y0 = specs[state]
    s = sum(distribution[y] for y in good)
    C, q = completion(s, W, t, z)
    if branch == "ordinary":
        return C if y in good else F(0)
    return q if y == y0 else F(0)


runs = []


def enumerate_runs(state, slot, probability, history):
    if state in {"abort", "invalid"} or slot == L:
        runs.append((state, probability, history))
        return
    distribution = specs[state][0]
    for branch in ("ordinary", "guess"):
        for y in range(2**W):
            p = (1 - delta) * distribution[y] if branch == "ordinary" else delta / 2**W
            if p:
                enumerate_runs(next_state(state, y), slot + 1, probability * p,
                               history + [(state, branch, y)])


enumerate_runs("start", 0, F(1), [])
assert sum(p for _, p, _ in runs) == 1
deferred = F(0)
analytical = F(0)
for state, p, history in runs:
    q = F(1)
    for pre_state, branch, y in history:
        q *= retention(pre_state, branch, y)
    if len(history) != L:
        assert q == 0
    analytical += p * q
    if state == "dummy" and len(history) == L:
        deferred += p * q
assert analytical == deferred == z**L

# Quarter correction: test general dyadic p > 1/2 and guess widths.
quarter_count = 0
for J in range(9):
    for numerator in range(33, 65):
        p = F(numerator, 64)
        scaled = F(2**(J + 2), 1) / (2 * p)
        c = F(scaled.numerator // scaled.denominator, 2**(J + 2))
        e = F(1, 4) - p * c / 2
        q = 2**(J + 1) * e
        assert 0 <= c <= 1 and 0 <= q < F(1, 4)
        assert p * c / 2 + F(1, 2) * F(1, 2**J) * q == F(1, 4)
        quarter_count += 1

print(json.dumps({
    "completion_parameter_cases": count,
    "adaptive_recorded_runs": len(runs),
    "adaptive_deferred_success": str(deferred),
    "adaptive_analytical_success": str(analytical),
    "adaptive_target_z_power_L": str(z**L),
    "quarter_parameter_cases": quarter_count,
    "arithmetic": "exact fractions, no floating point",
    "status": "all finite diagnostics passed; not a general proof certificate",
}, indent=2))
