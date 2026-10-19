"""Standalone exact checks reconstructed for this review.

Only Python's standard library is used. No source-audit modules are imported.
The rational nonclock point tests spectral algebra; no claim is made that this
particular perturbation lies inside the unspecified IFT neighborhood.
"""

from fractions import Fraction as F
import hashlib
import json
from pathlib import Path


def eye(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]


def mul(a, b):
    return [[sum((x * y for x, y in zip(row, col)), F(0))
             for col in zip(*b)] for row in a]


def diag(xs):
    return [[F(x) if i == j else F(0) for j in range(len(xs))]
            for i, x in enumerate(xs)]


def inverse(a):
    n = len(a)
    m = [list(row) + unit for row, unit in zip(a, eye(n))]
    for j in range(n):
        p = next(p for p in range(j, n) if m[p][j])
        m[j], m[p] = m[p], m[j]
        pivot = m[j][j]
        m[j] = [x / pivot for x in m[j]]
        for i in range(n):
            if i != j:
                scale = m[i][j]
                m[i] = [x - scale * y for x, y in zip(m[i], m[j])]
    return [row[n:] for row in m]


def rank_and_pivots(a):
    m = [list(row) for row in a]
    r = 0
    pivots = []
    for j in range(len(m[0])):
        p = next((p for p in range(r, len(m)) if m[p][j]), None)
        if p is None:
            continue
        m[r], m[p] = m[p], m[r]
        pivot = m[r][j]
        m[r] = [x / pivot for x in m[r]]
        for i in range(r + 1, len(m)):
            scale = m[i][j]
            if scale:
                m[i] = [x - scale * y for x, y in zip(m[i], m[r])]
        pivots.append(j)
        r += 1
        if r == len(m):
            break
    return r, pivots


def determinant(a):
    m = [list(row) for row in a]
    d = F(1)
    for j in range(len(m)):
        p = next((p for p in range(j, len(m)) if m[p][j]), None)
        if p is None:
            return F(0)
        if p != j:
            m[j], m[p] = m[p], m[j]
            d = -d
        pivot = m[j][j]
        d *= pivot
        for i in range(j + 1, len(m)):
            scale = m[i][j] / pivot
            for q in range(j + 1, len(m)):
                m[i][q] -= scale * m[j][q]
            m[i][j] = F(0)
    return d


def generator(k):
    n = len(k)
    a = [[F(0) for _ in range(n)] for _ in range(n)]
    for i, rate in enumerate(k):
        a[i][i] = -rate
        if i + 1 < n:
            a[i + 1][i] = rate
    return a


def eigenbasis(k):
    n = len(k)
    v = eye(n)
    for q in range(n):
        for p in range(q + 1, n):
            v[p][q] = k[p - 1] * v[p - 1][q] / (k[p] - k[q])
    assert mul(generator(k), v) == mul(v, diag([-x for x in k]))
    return v


def label_basis(k, order):
    v = eigenbasis([k[i] for i in order])
    return [[row[order.index(label)] for label in range(4)] for row in v]


def row_output(v):
    return [sum(col) for col in zip(*v)]


def input_coeff(v):
    return [row[0] for row in inverse(v)]


def coefficient(left_v, right_v):
    return [a * b for a, b in zip(row_output(left_v), input_coeff(right_v))]


def equal(a, b):
    assert a == b
    return True


def exact_rank(k, multipliers):
    # Each physical baseline interval has length log(2). For N=6k+1,
    # total baseline L=N log(2); controls are indexed in reverse time u.
    # Right-trivialized off-diagonal derivative integrals are rational:
    # H_i,pq (2**(D gap)-1)/gap * 2**(D gap*j).
    v = eigenbasis(k)
    vi = inverse(v)
    controls = []
    for i in range(4):
        unit_rate = [F(j == i) for j in range(4)]
        controls.append(mul(mul(vi, generator(unit_rate)), v))
    roots = [(p, q) for p in range(4) for q in range(p)]
    gaps = [k[q] - k[p] for p, q in roots]
    frequencies = [D * gap for D in multipliers for gap in gaps]
    assert len(set(frequencies)) == len(frequencies)
    for p, q in roots:
        assert controls[p][p][q] == -v[p][q] != 0
    n = len(frequencies) + 1
    rows = []
    # Integrated hazards divided by log(2), removing the common irrational.
    for i in range(4):
        rows.append([F(stage == i) for stage in range(4) for j in range(n)])
    for D in multipliers:
        for p, q in roots:
            gap = k[q] - k[p]
            node = F(2) ** int(D * gap)
            rows.append([controls[i][p][q] * (node - 1) / gap * node ** j
                         for i in range(4) for j in range(n)])
    rank, pivots = rank_and_pivots(rows)
    expected = 4 + 6 * len(multipliers)
    assert rank == expected
    minor = [[row[j] for j in pivots] for row in rows]
    det = determinant(minor)
    assert det
    return {
        "order_rates": [str(x) for x in k],
        "duration_multipliers": multipliers,
        "physical_baseline_intervals": n,
        "baseline_duration": f"{n} log(2)",
        "rank": rank,
        "expected_rank": expected,
        "frequencies_in_log2_units": [str(x) for x in frequencies],
        "independent_parameter_columns": pivots,
        "nonzero_minor_numerator_digits": len(str(abs(det.numerator))),
        "nonzero_minor_denominator_digits": len(str(det.denominator)),
        "nonzero_minor_sha256": hashlib.sha256(str(det).encode()).hexdigest(),
    }


def run():
    lam = list(map(F, [1, 3, 8, 10]))
    # Independently parameterize the conic 12X^2-5Y^2=847 through (9,5).
    # The rational line Y=5+(13/3)(X-9) has the second point below.
    slope = F(13, 3)
    w = (50 * slope - 216) / (12 - 5 * slope ** 2)
    mu = [1 - w / 2, 3 - slope * w / 2,
          8 + slope * w / 2, 10 + w / 2]
    t = mu[0] * mu[3] / (lam[0] * lam[3])
    assert t != 1 and t > 0
    assert mu[1] * mu[2] / (lam[1] * lam[2]) == t
    assert mu[0] + mu[3] == mu[1] + mu[2] == 11
    assert min(mu) > 0 and len(set(mu)) == 4
    ratios = [x / y for x, y in zip(mu, lam)]
    assert len(set(ratios)) == 4
    orders = [(0, 3, 1, 2), (1, 2, 0, 3)]
    wa = [label_basis(lam, order) for order in orders]
    wb = [label_basis(mu, order) for order in orders]
    c_forward = [coefficient(b, a) for a, b in zip(wa, wb)]
    c_reverse = [coefficient(a, b) for a, b in zip(wa, wb)]
    equal(c_forward[0], c_forward[1])
    equal(c_reverse[0], c_reverse[1])
    equal(coefficient(wa[0], wa[0]), coefficient(wa[1], wa[1]))
    equal(coefficient(wb[0], wb[0]), coefficient(wb[1], wb[1]))
    scale_a = [y / x for x, y in zip(input_coeff(wa[0]), input_coeff(wa[1]))]
    scale_b = [y / x for x, y in zip(input_coeff(wb[0]), input_coeff(wb[1]))]
    equal(scale_a, scale_b)
    ta = mul(mul(wa[1], diag(scale_a)), inverse(wa[0]))
    tb = mul(mul(wb[1], diag(scale_b)), inverse(wb[0]))
    e1 = [[F(i == 0)] for i in range(4)]
    c = [[F(1)] * 4]
    equal(mul(ta, e1), e1)
    equal(mul(tb, e1), e1)
    equal(mul(c, ta), c)
    equal(mul(c, tb), c)
    qa = [generator([lam[i] for i in order]) for order in orders]
    qb = [generator([mu[i] for i in order]) for order in orders]
    equal(mul(ta, qa[0]), mul(qa[1], ta))
    equal(mul(tb, qb[0]), mul(qb[1], tb))
    # E is arbitrary diagonal in the proof; use one exact rational instance.
    e = diag([F(2) ** -int(x) for x in lam])
    f = [mul(mul(b, e), inverse(a)) for a, b in zip(wa, wb)]
    g = [mul(mul(a, e), inverse(b)) for a, b in zip(wa, wb)]
    equal(mul(tb, f[0]), mul(f[1], ta))
    equal(mul(ta, g[0]), mul(g[1], tb))
    checks = {
        "arithmetic": "fractions.Fraction; independent implementation; no source imports",
        "algebra_point": {
            "lambda": [str(x) for x in lam],
            "mu": [str(x) for x in mu],
            "t": str(t),
            "response_ratios": [str(x) for x in ratios],
            "forward_C": [str(x) for x in c_forward[0]],
            "reverse_C": [str(x) for x in c_reverse[0]],
            "scope": "spectral algebra only; no local-realization radius claimed",
        },
        "residue_equalities": True,
        "preparation_readout_preserving_gauges": True,
        "hold_and_bidirectional_ramp_intertwining": True,
        "rank_checks": [exact_rank([lam[i] for i in order], [1, 2])
                        for order in orders],
        "status": "PASS",
    }
    output = Path(__file__).with_name("independent_exact_check.json")
    output.write_text(json.dumps(checks, indent=2) + "\n")
    print(json.dumps(checks, indent=2))


if __name__ == "__main__":
    run()
