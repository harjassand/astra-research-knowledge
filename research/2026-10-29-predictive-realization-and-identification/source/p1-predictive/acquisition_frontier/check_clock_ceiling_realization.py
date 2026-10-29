"""Independent exact controls for the clock-ceiling completion theorem.

No producer imports, no LP output trusted, no source draws. All mathematical
checks use Fraction; floating values are display only. Writes a local JSON
certificate after all assertions pass.
"""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import json
import time


HERE = Path(__file__).resolve().parent


def floor(x):
    return x.numerator // x.denominator


def psi(x, f, rate):
    x, f, rate = F(x), F(f), F(rate)
    assert x >= 0 and f >= 0 and rate > 0
    if f == 0:
        assert x == 0
        return F(0)
    u = rate * x / f
    n = floor(u)
    return f * (n + 1) * (2 * u - n) / rate**2


def off_counts(x, f, z, rate):
    """N in {0,k,k+1} with weighted mean x, second moment z."""
    x, f, z, rate = map(F, (x, f, z, rate))
    assert x > 0 and f > 0 and z >= psi(x, f, rate)
    u, v = rate * x / f, rate**2 * z / f
    k = floor(v / u) - 1
    assert k >= 1
    pk = ((k + 2) * u - v) / k
    pn = (v - (k + 1) * u) / (k + 1)
    p0 = 1 - pk - pn
    assert min(pk, pn, p0) >= 0
    assert p0 + pk + pn == 1
    assert k * pk + (k + 1) * pn == u
    assert k * (k + 1) * pk + (k + 1) * (k + 2) * pn == v
    return k, p0, pk, pn


def diag_flow(x, a, z, rate):
    """Root's formula, checked against the adjacent interval at every tie."""
    x, a, z, rate = map(F, (x, a, z, rate))
    assert x > 0 and a > 0 and z >= psi(x, a, rate)
    r = rate * z / x
    n = floor(r - 1)
    assert n >= 1
    f = rate * x * (2 * (n + 1) - r) / (n * (n + 1))
    assert rate * x / (n + 1) < f <= rate * x / n
    assert 0 < f <= min(a, rate * x)
    assert psi(x, f, rate) == z
    return f


def solve(a, rhs):
    """Fraction Gaussian elimination, with a vector or rectangular RHS."""
    n = len(a)
    if n == 0:
        return []
    vector = not isinstance(rhs[0], list)
    b = [[F(x)] for x in rhs] if vector else [[F(x) for x in r] for r in rhs]
    w = len(b[0])
    t = [[F(x) for x in a[i]] + b[i] for i in range(n)]
    for j in range(n):
        p = next(i for i in range(j, n) if t[i][j])
        t[j], t[p] = t[p], t[j]
        v = t[j][j]
        t[j] = [x / v for x in t[j]]
        for i in range(n):
            if i != j and t[i][j]:
                v = t[i][j]
                t[i] = [t[i][k] - v * t[j][k] for k in range(n + w)]
    out = [r[n:] for r in t]
    return [r[0] for r in out] if vector else out


def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), F(0))


def matmul(a, b):
    return [[dot(row, col) for col in zip(*b)] for row in a]


def to_json(x):
    if isinstance(x, F):
        return str(x)
    if isinstance(x, dict):
        return {str(k): to_json(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [to_json(v) for v in x]
    return x


def compile_record(mass, off, weights, ceilings, rate, c):
    """Construct all-rate-Lambda channels, independently eliminate full L."""
    mass = [[F(x) for x in r] for r in mass]
    off = [[F(x) for x in r] for r in off]
    weights = list(map(F, weights))
    ceilings = list(map(F, ceilings))
    rate, c = F(rate), F(c)
    m = len(weights)
    assert all(weights[i] > 0 for i in range(m))
    budgets = [weights[i] * ceilings[i] - sum(off[i]) for i in range(m)]
    assert min(budgets) >= 0
    for i in range(m):
        assert off[i][i] == 0
        assert sum(off[i]) == sum(off[j][i] for j in range(m))
    flows = [r[:] for r in off]
    z = [[F(0) for _ in range(m)] for _ in range(m)]
    for i in range(m):
        if mass[i][i]:
            assert budgets[i] > 0
            flows[i][i] = min(budgets[i], rate * mass[i][i])
        for j in range(m):
            assert mass[i][j] >= 0
            if mass[i][j]:
                assert flows[i][j] > 0
                z[i][j] = psi(mass[i][j], flows[i][j], rate)
    minimum = sum(map(sum, z), F(0))
    assert 2 * c >= minimum
    positive = [(i, j) for i in range(m) for j in range(m) if mass[i][j] > 0]
    if positive:
        i, j = next(((i, j) for i, j in positive if i != j), positive[0])
        z[i][j] += 2 * c - minimum
        if i == j:
            flows[i][i] = diag_flow(mass[i][i], budgets[i], z[i][i], rate)
    else:
        assert c == 0

    state_weights = weights[:]
    edges = {}

    def edge(i, j, f):
        if not f:
            return
        assert i != j and f > 0
        edges[i, j] = edges.get((i, j), F(0)) + f

    def phase(flow):
        assert flow > 0
        k = len(state_weights)
        state_weights.append(flow / rate)
        return k

    channels = []
    for i in range(m):
        for j in range(m):
            f, x, second = flows[i][j], mass[i][j], z[i][j]
            if not f:
                assert x == 0
                continue
            if x == 0:
                assert i != j
                edge(i, j, f)
                channels.append({"from": i, "to": j, "flow": f, "mass": x,
                                 "second": second, "counts": [0]})
                continue
            k, p0, pk, pn = off_counts(x, f, second, rate)
            if i == j:
                assert p0 == 0
            edge(i, j, f * p0)
            prefix_flow = f * (pk + pn)
            prev = i
            for _ in range(k):
                h = phase(prefix_flow)
                edge(prev, h, prefix_flow)
                prev = h
            edge(prev, j, f * pk)
            if pn:
                h = phase(f * pn)
                edge(prev, h, f * pn)
                edge(h, j, f * pn)
            channels.append({"from": i, "to": j, "flow": f, "mass": x,
                             "second": second, "counts": [0, k, k + 1],
                             "probabilities": [p0, pk, pn]})

    size = len(state_weights)
    lap = [[F(0) for _ in range(size)] for _ in range(size)]
    for (i, j), f in edges.items():
        lap[i][i] += f
        lap[i][j] -= f
    assert all(sum(r) == 0 for r in lap)
    assert all(sum(lap[i][j] for i in range(size)) == 0 for j in range(size))
    assert all(lap[i][j] <= 0 for i in range(size) for j in range(size) if i != j)
    port_rates = [lap[i][i] / state_weights[i] for i in range(m)]
    hidden_rates = [lap[i][i] / state_weights[i] for i in range(m, size)]
    assert all(port_rates[i] <= ceilings[i] for i in range(m))
    assert all(r == rate for r in hidden_rates)
    assert all(w > 0 for w in state_weights)

    # Schur record, independently from generator blocks.
    hidden = list(range(m, size))
    hweights = state_weights[m:]
    C = [[lap[i][j] for j in hidden] for i in hidden]
    BI = [[lap[i][j] for j in hidden] for i in range(m)]
    IB = [[lap[i][j] for j in range(m)] for i in hidden]
    X = solve(C, IB)
    t = solve(C, hweights)
    bR = [weights[i] - dot(BI[i], t) for i in range(m)]
    bL = [weights[j] - sum(hweights[k] * X[k][j] for k in range(len(hidden)))
          for j in range(m)]
    S = [[lap[i][j] - dot(BI[i], [r[j] for r in X]) for j in range(m)]
         for i in range(m)]
    Y = solve(C, [[hweights[k] * X[k][j] for j in range(m)]
                  for k in range(len(hidden))])
    recovered_mass = matmul(BI, Y)
    recovered_c = dot(hweights, t)
    expected_S = [[-off[i][j] if i != j else sum(off[i]) for j in range(m)]
                  for i in range(m)]
    assert S == expected_S
    assert bR == [weights[i] + sum(mass[i]) for i in range(m)]
    assert bL == [weights[j] + sum(mass[i][j] for i in range(m)) for j in range(m)]
    assert recovered_mass == mass
    assert recovered_c == c
    assert sum(state_weights) == sum(bR) == sum(bL)

    means = []
    W = sum(state_weights)
    for n in range(1, m + 1):
        for A in combinations(range(m), n):
            live = [i for i in range(size) if i not in A]
            R = [i for i in range(m) if i not in A]
            killed = [[lap[i][j] for j in live] for i in live]
            h = solve(killed, [state_weights[i] for i in live])
            denom = W - sum(weights[i] for i in A)
            full = dot([state_weights[i] for i in live], h) / denom
            if R:
                hR = solve([[S[i][j] for j in R] for i in R], [bR[i] for i in R])
                compressed = (c + dot([bL[i] for i in R], hR)) / denom
            else:
                compressed = c / denom
            assert full == compressed
            means.append({"target": A, "mean": full})
    return {"status": "PASS", "states": size, "hidden_states": len(hidden),
            "S": S, "bR": bR, "bL": bL, "c": c, "M": recovered_mass,
            "minimum_weighted_second_moment": minimum,
            "port_rates": port_rates, "hidden_rates": hidden_rates,
            "state_weights": state_weights, "laplacian": lap,
            "channels": channels, "means": means}


def main():
    start = time.perf_counter()
    scalar = {"off_diagonal": 0, "diagonal": 0}
    for rate in [F(1), F(3, 2), F(2)]:
        for x in [F(1, 4), F(3, 2), F(7, 3)]:
            for f in [F(1, 10), F(1), F(5)]:
                for extra in [F(0), F(1, 7), F(1), F(10)]:
                    z = psi(x, f, rate) + extra
                    off_counts(x, f, z, rate)
                    scalar["off_diagonal"] += 1
                    nf = diag_flow(x, f, z, rate)
                    _, p0, _, _ = off_counts(x, nf, z, rate)
                    assert p0 == 0
                    scalar["diagonal"] += 1

    # A full, independently certified nontrivial transportation optimum.
    rate, budget = F(1), F(1, 4)
    M = [[F(1, 4), F(7, 4)], [F(3, 4), F(1, 4)]]
    flux = [[F(0), F(1)], [F(1), F(0)]]
    r, s = [F(2), F(1)], [F(1), F(2)]
    assert [sum(row) for row in M] == r
    assert [sum(M[i][j] for i in range(2)) for j in range(2)] == s
    cost = sum(psi(M[i][j], budget if i == j else 1, rate)
               for i in range(2) for j in range(2))
    assert cost == F(15, 2)
    grad = [[F(3), F(4)], [F(2), F(3)]]
    alpha, beta = [F(3), F(2)], [F(0), F(1)]
    for i in range(2):
        for j in range(2):
            f = budget if i == j else F(1)
            x = M[i][j]
            u = rate * x / f
            n = floor(u)
            left = 2 * n / rate if u == n and n else 2 * (n + 1) / rate
            right = 2 * (n + 1) / rate
            assert left <= grad[i][j] <= right
            assert grad[i][j] == alpha[i] + beta[j]
    # Each supporting subgradient sums to the same affine function over the
    # transport polytope. This is a global optimality proof, not a grid test.
    affine_intercept = cost - sum(grad[i][j] * M[i][j] for i in range(2) for j in range(2))
    dual_value = dot(alpha, r) + dot(beta, s) + affine_intercept
    assert dual_value == cost
    piecewise = []
    for y in [F(0), F(1, 4), F(1, 2), F(3, 4), F(1)]:
        value = 2 * psi(1 - y, budget, rate) + psi(1 + y, 1, rate) + psi(y, 1, rate)
        piecewise.append({"y": y, "objective": value})
    assert [p["objective"] for p in piecewise] == [F(12), F(19, 2), F(8), F(15, 2), F(8)]

    controls = []
    for c in [F(15, 4), F(4), F(10)]:
        controls.append(compile_record(M, flux, [1, 1], [F(5, 4)] * 2, rate, c))
    assert controls[0]["states"] == 7
    assert [m["mean"] for m in controls[0]["means"]] == [F(39, 16), F(39, 16), F(5, 4)]

    # Zero spare departure budget does not require zero hidden residence:
    # off-diagonal residence can reuse existing trace channels.
    balanced = [[F(0), F(1)], [F(1), F(0)]]
    controls.append(compile_record(balanced, flux, [1, 1], [1, 1], 1, 2))
    assert controls[-1]["states"] == 4
    assert controls[-1]["minimum_weighted_second_moment"] == 4

    # Diagonal-only residence: exercise equality, integer ties and large excess.
    diagonal = [[F(1, 3), F(0)], [F(0), F(2, 3)]]
    diagonal_min = psi(F(1, 3), F(1, 5), F(3, 2)) + psi(F(2, 3), F(1, 5), F(3, 2))
    for extra in [F(0), F(1, 7), F(4)]:
        controls.append(compile_record(diagonal, flux, [1, 1], [F(6, 5)] * 2,
                                       F(3, 2), diagonal_min / 2 + extra))

    # Exact support obstruction: row0 has positive mass but can only feed col1,
    # whose required margin is zero when all diagonal budgets vanish.
    failures = [
        {"kind": "support", "row_mass": [1, 0], "column_mass": [1, 0],
         "zero_diagonal_budgets": [0, 0], "row_subset": [0],
         "allowed_neighbor_columns": [1], "demand": 1, "available": 0},
        {"kind": "port_budget", "w": 1, "ceiling": F(3, 4),
         "trace_outflow": 1, "budget": F(-1, 4)},
    ]
    out = {"status": "PASS", "scope": "supplied rational records, no observations",
           "scalar_moment_checks": scalar,
           "transport_certificate": {"M": M, "Jcap": cost,
                                     "subgradient": grad, "row_potentials": alpha,
                                     "column_potentials": beta, "affine_intercept": affine_intercept,
                                     "dual_value": dual_value, "objective_controls": piecewise},
           "full_generator_controls": controls, "exact_failures": failures,
           "total_full_target_means": sum(len(c["means"]) for c in controls),
           "elapsed_seconds": time.perf_counter() - start}
    path = HERE / "CLOCK_CEILING_REALIZATION_CHECKS.json"
    path.write_text(json.dumps(to_json(out), indent=2) + "\n")
    print(json.dumps({"status": out["status"], "scalar_moment_checks": scalar,
                      "generator_count": len(controls),
                      "state_counts": [x["states"] for x in controls],
                      "full_target_mean_count": out["total_full_target_means"],
                      "Jcap": str(cost), "seconds": out["elapsed_seconds"],
                      "file": str(path)}, indent=2))


if __name__ == "__main__":
    main()
