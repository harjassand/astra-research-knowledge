"""Exact population checks for the finite-rate transport supplier.

Standard library only. These are model checks, not acquired kinetic data or an
apparatus demonstration. Rational stationary equations, transient fluctuation
symmetry by uniformization, and two substantive scope counterexamples.
"""
from fractions import Fraction as F
from pathlib import Path
import json
import math


def solve(a, b):
    n = len(b)
    z = [list(row) + [b[i]] for i, row in enumerate(a)]
    for k in range(n):
        p = next(i for i in range(k, n) if z[i][k])
        z[k], z[p] = z[p], z[k]
        v = z[k][k]
        z[k] = [x / v for x in z[k]]
        for i in range(n):
            if i != k and z[i][k]:
                v = z[i][k]
                z[i] = [x - v * y for x, y in zip(z[i], z[k])]
    return [row[-1] for row in z]


def generator(n, edges):
    q = [[F(0) for _ in range(n)] for _ in range(n)]
    for i, j, a, b in edges:
        assert i != j and a > 0 and b > 0
        q[i][j] += a
        q[j][i] += b
    for i in range(n):
        q[i][i] = -sum(q[i])
    return q


def stationary(q):
    n = len(q)
    a = [[q[j][i] for j in range(n)] for i in range(n - 1)]
    a.append([F(1)] * n)
    p = solve(a, [F(0)] * (n - 1) + [F(1)])
    assert min(p) > 0 and sum(p) == 1
    assert all(sum(p[j] * q[j][i] for j in range(n)) == 0 for i in range(n))
    return p


def edge_current(p, q, i, j):
    return p[i] * q[i][j] - p[j] * q[j][i]


def entropy(p, q):
    s = 0.0
    for i in range(len(p)):
        for j in range(i + 1, len(p)):
            if q[i][j]:
                a, b = p[i] * q[i][j], p[j] * q[j][i]
                s += float(a - b) * math.log(float(a / b))
    return s


def build_hidden(seed, rs, native_scale=F(1)):
    # Six hidden microstates: visible station i and internal z in {0,1}.
    micros = [(i, z) for i in range(3) for z in range(2)]
    raw = [F(1 + ((7 * a + 3 * seed) % 11)) for a in range(6)]
    mu = [x / sum(raw) for x in raw]
    states = [(a, e) for a, (i, z) in enumerate(micros) for e in ((i - 1) % 3, i)]
    index = {s: k for k, s in enumerate(states)}
    edges = []
    native_pairs = [[] for _ in range(3)]
    gates = [[] for _ in range(3)]
    for e in range(3):
        ids = [a for a, (i, z) in enumerate(micros) if i in (e, (e + 1) % 3)]
        for u, a in enumerate(ids):
            for b in ids[u + 1:]:
                c = native_scale * F(1 + ((13 * a + 17 * b + 5 * e + seed) % 19), 37)
                qa, qb = c / mu[a], c / mu[b]
                assert mu[a] * qa == mu[b] * qb
                ia, ib = index[a, e], index[b, e]
                edges.append((ia, ib, qa, qb))
                ya, yb = micros[a][0], micros[b][0]
                if ya != yb:
                    if ya == e:
                        native_pairs[e].append((ia, ib))
                    else:
                        native_pairs[e].append((ib, ia))
    for a, (i, z) in enumerate(micros):
        u, v = index[a, (i - 1) % 3], index[a, i]
        gamma = F(1 + ((a + seed) % 7), 5)
        edges.append((u, v, gamma * rs[i], gamma))
        gates[i].append((u, v))
    q = generator(len(states), edges)
    m = [mu[a] / 2 for a, e in states]
    return q, m, states, native_pairs, gates


def motor_case(seed, rs, scale=F(1)):
    q, m, states, native, gates = build_hidden(seed, rs, scale)
    p = stationary(q)
    js = [sum(edge_current(p, q, u, v) for u, v in es) for es in native]
    cs = [sum(edge_current(p, q, u, v) for u, v in es) for es in gates]
    assert len(set(js + cs)) == 1
    r = math.prod(rs)
    j = js[0]
    assert (j > 0) == (r > 1) and (j < 0) == (r < 1)
    ep = entropy(p, q)
    target = float(j) * math.log(float(r))
    assert abs(ep - target) <= 1e-12 * max(1.0, ep, target)
    # Multiple hidden states with one visible label need not have equal rates.
    nonlumpable = False
    for u, (a, e) in enumerate(states):
        for v, (b, f) in enumerate(states):
            if a // 2 == b // 2 and e == f and a != b:
                for y in range(3):
                    if y == a // 2:
                        continue
                    pu = sum(q[u][w] for w, (c, g) in enumerate(states) if c // 2 == y)
                    pv = sum(q[v][w] for w, (c, g) in enumerate(states) if c // 2 == y)
                    if pu != pv:
                        nonlumpable = True
    assert nonlumpable
    return {"seed": seed, "gate_ratios": list(map(str, rs)), "native_scale": str(scale),
            "current_exact": str(j), "current": float(j), "entropy_production": ep,
            "affinity_times_current": target, "nonlumpable_visible_mode": nonlumpable}


def transient_check():
    r = F(3)
    q, m, states, native, gates = build_hidden(3, [r, F(1), F(1)])
    n = len(q)
    ceiling = 1 + max(-q[i][i] for i in range(n))
    p = [[(F(1) if i == j else F(0)) + q[i][j] / ceiling for j in range(n)] for i in range(n)]
    assert all(sum(row) == 1 and min(row) >= 0 for row in p)
    increment = {pair: 1 for pair in gates[0]}
    increment.update({(v, u): -1 for u, v in gates[0]})
    law = {(i, 0): m[i] for i in range(n)}
    for depth in range(1, 8):
        nxt = {}
        for (i, count), mass in law.items():
            for j, prob in enumerate(p[i]):
                if prob:
                    key = (j, count + increment.get((i, j), 0))
                    nxt[key] = nxt.get(key, F(0)) + mass * prob
        law = nxt
        counts = {}
        for (i, c), mass in law.items():
            counts[c] = counts.get(c, F(0)) + mass
        assert sum(counts.values()) == 1
        for c, mass in counts.items():
            assert mass == r ** c * counts.get(-c, F(0))
    # A retained initial microstate/mode selection does not supply m conditionally.
    u, v = gates[0][0]
    one_step_negative = p[v][u]
    one_step_positive = sum(p[v][j] for j in range(n) if increment.get((v, j), 0) == 1)
    assert one_step_negative > 0 and one_step_positive == 0
    return {"uniformization_depths_exact": list(range(1, 8)), "gate_ratio": str(r),
            "arbitrary_initial_record_counterexample_negative_probability": str(one_step_negative),
            "arbitrary_initial_record_counterexample_positive_probability": str(one_step_positive)}


def hidden_tree():
    # Four specimen states project to 0,1,2,0; native motion follows a line.
    labels = [0, 1, 2, 0]
    states = [(a, e) for a, y in enumerate(labels) for e in ((y - 1) % 3, y)]
    idx = {s: i for i, s in enumerate(states)}
    edges = []
    for e, a, b in [(0, 0, 1), (1, 1, 2), (2, 2, 3)]:
        edges.append((idx[a, e], idx[b, e], F(1), F(1)))
    for a, y in enumerate(labels):
        edges.append((idx[a, (y - 1) % 3], idx[a, y], F(2 if y == 0 else 1), F(1)))
    assert len(edges) == len(states) - 1
    q = generator(len(states), edges)
    p = stationary(q)
    assert all(edge_current(p, q, u, v) == 0 for u, v, a, b in edges)
    return {"joint_states": len(states), "edges": len(edges), "stationary_law": list(map(str, p)),
            "all_edge_currents_exact": "0", "claimed_phase_affinity": "log(2)"}


def leakage_case(eta, eps):
    r = F(2)
    edges = [(0, 1, r, F(1)), (1, 2, eta, eta), (3, 0, eta, eta),
             (1, 3, eps, eps), (2, 0, eps, eps), (2, 3, F(1), F(1))]
    q = generator(4, edges)
    p = stationary(q)
    g = (2 * eta * eps + eta + eps) / (eta + eps + 2)
    d = (r - 1) / (2 * (r + 1 + 2 * g))
    assert p[1] - p[0] == d
    current = edge_current(p, q, 2, 3)
    assert current == (eta - eps) * d / (eta + eps + 2)
    fuel = edge_current(p, q, 0, 1)
    assert fuel > 0
    ep = entropy(p, q)
    assert abs(ep - float(fuel) * math.log(2)) < 1e-14
    return {"useful_path_rate": str(eta), "leakage_rate": str(eps),
            "target_current_exact": str(current), "target_current": float(current),
            "fuel_current_exact": str(fuel), "entropy_production": ep}


def noncommuting_no_pump():
    p = [[F(3, 4), F(1, 4), F(0)], [F(1, 4), F(3, 4), F(0)], [F(0), F(0), F(1)]]
    q = [[F(1), F(0), F(0)], [F(0), F(3, 4), F(1, 4)], [F(0), F(1, 4), F(3, 4)]]
    pq = [[sum(p[i][k] * q[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
    assert any(pq[i][j] != pq[j][i] for i in range(3) for j in range(3))
    assert all(p[i][j] == p[j][i] and q[i][j] == q[j][i] for i in range(3) for j in range(3))
    assert all(sum(pq[i][j] for i in range(3)) == 1 for j in range(3))
    return {"stroboscopic_product": [[str(x) for x in row] for row in pq],
            "endpoint_reversible": False, "mean_physical_native_edge_currents": "all zero at uniform equilibrium"}


def main():
    cases = []
    for seed in [1, 7, 19]:
        for rs in [[F(2), F(1), F(1)], [F(1, 2), F(1), F(1)], [F(2), F(3), F(1, 6)]]:
            cases.append(motor_case(seed, rs))
    cases.append(motor_case(1, [F(2), F(1), F(1)], F(1, 100000)))
    results = {"status": "PASS", "scope": "exact population models; no acquisition or physical execution",
               "hidden_motor_cases": cases, "transient_record_relation": transient_check(),
               "hidden_tree_obstruction": hidden_tree(),
               "leakage_reversal": [leakage_case(F(1, 1000), F(1, 1000000)),
                                    leakage_case(F(1, 1000000), F(1, 1000)),
                                    leakage_case(F(1, 10**12), F(1, 10**6))],
               "noncommuting_no_pump": noncommuting_no_pump()}
    out = Path(__file__).with_name("TRANSPORT_SUPPLIER_CHECKS.json")
    out.write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps({"status": "PASS", "hidden_motor_cases": len(cases),
                      "transient_depths": 7, "tree_obstruction": True,
                      "leakage_reversal_cases": 3, "output": str(out)}, indent=2))


if __name__ == "__main__":
    main()
