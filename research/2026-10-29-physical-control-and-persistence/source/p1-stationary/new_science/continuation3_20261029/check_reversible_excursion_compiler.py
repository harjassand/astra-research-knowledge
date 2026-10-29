#!/usr/bin/env python3
"""Exact population-model checks of the physical excursion protocol.

No data here are apparatus measurements. Fraction arithmetic compares a
literal endpoint-observation controller with the independently derived block
formula, including hidden endpoints and native-time occupation.
"""
from fractions import Fraction as F
from functools import reduce
from math import comb
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent


def zeros(n, m=None):
    return [[F(0) for _ in range(n if m is None else m)] for _ in range(n)]


def eye(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]


def mul(a, b):
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), F(0))
             for j in range(len(b[0]))] for i in range(len(a))]


def add(a, b):
    return [[x + y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def scale(c, a):
    return [[c * x for x in row] for row in a]


def power(a, n):
    r = eye(len(a))
    for _ in range(n):
        r = mul(r, a)
    return r


def block(a, rows, cols):
    return [[a[i][j] for j in cols] for i in rows]


def row_times(v, a):
    return [sum((v[i] * a[i][j] for i in range(len(v))), F(0))
            for j in range(len(a[0]))]


def normalize(v):
    z = sum(v, F(0))
    return [x / z for x in v]


def reversible(p, mu):
    assert all(sum(row) == 1 and min(row) >= 0 for row in p)
    assert row_times(mu, p) == mu
    assert all(mu[i] * p[i][j] == mu[j] * p[j][i]
               for i in range(len(p)) for j in range(len(p)))


def formula(p, a, horizon):
    """Block proof, with arbitrary finite rational horizon law."""
    n = len(p)
    b = [i for i in range(n) if i not in a]
    cap = max(horizon)
    r = sum((F(h) * w for h, w in horizon.items()), F(0))
    tail = [sum((w for h, w in horizon.items() if h > j), F(0))
            for j in range(cap)]
    aa, ab, ba, bb = (block(p, a, a), block(p, a, b),
                      block(p, b, a), block(p, b, b))
    s = zeros(len(a))
    kaa = zeros(len(a))
    v = zeros(len(a))
    for j in range(cap):
        s = add(s, scale(tail[j], power(aa, j)))
        if j < cap - 1:
            v = add(v, scale(sum(tail[j + 1:]), power(aa, j)))
    for h, w in horizon.items():
        kaa = add(kaa, scale(w, power(aa, h)))
    kab = mul(s, ab)
    kba = scale(1 / r, mul(ba, s))
    kbb = add(bb, scale(1 / r, mul(mul(ba, v), ab)))
    k = zeros(n)
    for rows, cols, val in [(a, a, kaa), (a, b, kab),
                             (b, a, kba), (b, b, kbb)]:
        for ii, i in enumerate(rows):
            for jj, j in enumerate(cols):
                k[i][j] = val[ii][jj]
    return k, r


def hit(p, start, target, cap):
    """Actual repeated calls: stop on target readout or budget exhaustion."""
    n = len(p)
    end = [F(0)] * n
    occ = [F(0)] * n
    joint = [[F(0)] * n for _ in range(cap + 1)]
    if cap == 0:
        end[start] = joint[0][start] = F(1)
        return end, occ, joint
    active = [F(i == start) for i in range(n)]
    for call in range(1, cap + 1):
        occ = [x + y for x, y in zip(occ, active)]
        nxt = row_times(active, p)
        active = [F(0)] * n
        for y, mass in enumerate(nxt):
            if y in target or call == cap:
                end[y] += mass
                joint[call][y] += mass
            else:
                active[y] = mass
    assert sum(end) == 1
    return end, occ, joint


def controller(p, a, horizon):
    """Literal observation/stop policy; never examines a microscopic state.

    The evaluator sums microscopic transition possibilities to verify it.
    Policy decisions only use A/B, counters, and the supplied selector law.
    """
    n = len(p)
    b = set(range(n)) - set(a)
    cap = max(horizon)
    r = sum((h * w for h, w in horizon.items()), F(0))
    residual = {j: sum((w for h, w in horizon.items() if h > j), F(0)) / r
                for j in range(cap)}
    k, occ = zeros(n), zeros(n)
    joint = [[[F(0)] * n for _ in range(cap + 1)] for _ in range(n)]
    for x in range(n):
        if x in a:
            for h, wh in horizon.items():
                end, oc, jj = hit(p, x, b, h)
                for y in range(n):
                    k[x][y] += wh * end[y]
                    occ[x][y] += wh * oc[y]
                for call in range(h + 1):
                    for y in range(n):
                        joint[x][call][y] += wh * jj[call][y]
        else:
            occ[x][x] += 1  # mandatory first actual call
            for y, py in enumerate(p[x]):
                if y in b:
                    k[x][y] += py
                    joint[x][1][y] += py
                else:
                    for ell, well in residual.items():
                        end, oc, jj = hit(p, y, b, ell)
                        for z in range(n):
                            k[x][z] += py * well * end[z]
                            occ[x][z] += py * well * oc[z]
                        for call in range(ell + 1):
                            for z in range(n):
                                joint[x][call + 1][z] += py * well * jj[call][z]
    for x in range(n):
        assert sum(k[x]) == 1
        assert sum(occ[x]) == sum(call * sum(joint[x][call])
                                   for call in range(cap + 1))
        assert sum(joint[x][0]) == 0
    return k, occ, joint


def make_reversible(weights, seed):
    n = len(weights)
    p = zeros(n)
    for i in range(n):
        for j in range(i + 1, n):
            conductance = F(1 + ((i + 2) * (j + 3) + seed) % 11, 256)
            p[i][j] = conductance / weights[i]
            p[j][i] = conductance / weights[j]
    for i in range(n):
        p[i][i] = 1 - sum(p[i])
    mu = normalize([F(w) for w in weights])
    reversible(p, mu)
    return p, mu


def jsonable(obj):
    if isinstance(obj, F):
        return str(obj)
    if isinstance(obj, dict):
        return {str(k): jsonable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [jsonable(x) for x in obj]
    return obj


def hidden_checks():
    cases = []
    for weights, seed in [([1, 2, 3, 3, 2, 1], 7),
                           ([1, 2, 3, 4, 5, 6], 13)]:
        p, mu = make_reversible(weights, seed)
        a = [0, 1, 2]
        b = [3, 4, 5]
        ma = sum(mu[i] for i in a)
        for horizon in [{1: F(1)}, {2: F(1)}, {4: F(1)}, {8: F(1)},
                        {2: F(1, 2), 5: F(1, 2)},
                        {1: F(1, 3), 4: F(2, 3)}]:
            k, r = formula(p, a, horizon)
            actual, occ, joint = controller(p, a, horizon)
            assert k == actual
            z = ma + r * (1 - ma)
            nu = [mu[i] * (1 if i in a else r) / z for i in range(6)]
            reversible(k, nu)
            native_occupation = row_times(nu, occ)
            assert native_occupation == [r * m / z for m in mu]
            cost = sum(native_occupation)
            assert cost == r / z
            # The reversed paired trajectories retain their native call count.
            assert all(nu[x] * joint[x][ell][y] == nu[y] * joint[y][ell][x]
                       for x in range(6) for y in range(6)
                       for ell in range(max(horizon) + 1))
            cases.append({"baseline_weights": weights, "horizon": horizon,
                          "ratio": r, "target": nu,
                          "equilibrium_mean_calls": cost,
                          "pointwise_mean_call_range": [min(map(sum, occ)),
                                                         max(map(sum, occ))],
                          "full_hidden_pair_checks": 36,
                          "joint_call_count_pair_checks": 36 * (max(horizon) + 1)})
    # Exhibit memory: current A by itself and a previous A->A history differ.
    p, mu = make_reversible([1, 2, 3, 3, 2, 1], 7)
    a, b = [0, 1, 2], [3, 4, 5]
    base_exit = sum(mu[x] * p[x][y] for x in a for y in b) / sum(mu[x] for x in a)
    history_mass = sum(mu[x] * p[x][y] for x in a for y in a)
    history_exit = sum(mu[x] * p[x][y] * p[y][z]
                       for x in a for y in a for z in b) / history_mass
    assert base_exit != history_exit
    return {"cases": cases,
            "visible_nonmarkov_witness": {
                "Pr_next_B_given_A": base_exit,
                "Pr_next_B_given_A_A": history_exit},
            "P": p, "mu": mu}


def binary_checks():
    cases = []
    for pflip in [F(1, 20), F(1, 4), F(7, 20), F(9, 20), F(3, 4)]:
        p = [[1 - pflip, pflip], [pflip, 1 - pflip]]
        for cap in [1, 2, 4, 8, 16]:
            k, occ, _ = controller(p, [0], {cap: F(1)})
            amp = 1 - (1 - pflip) ** cap
            assert k[0][1] == amp and k[1][0] == amp / cap
            assert sum(occ[0]) == amp / pflip
            assert sum(occ[1]) == 2 - amp / (cap * pflip)
            cases.append({"p": pflip, "cap": cap, "down_flip": k[0][1],
                          "up_flip": k[1][0],
                          "mean_calls_A": sum(occ[0]),
                          "mean_calls_B": sum(occ[1])})
    p, n = F(1, 4), 4
    fast = 1 - (1 - p) ** n
    naive = p * (1 - p) ** (n - 1)
    slow_high = n * naive
    assert fast / naive != n and slow_high / naive == n
    return {"cases": cases,
            "failed_deterministic_return_horizon": {
                "p": p, "cap": n, "fast_down": fast,
                "naive_up": naive, "actual_stationary_B": fast / (fast + naive),
                "intended_stationary_B": F(n, n + 1)},
            "discarded_slow_pair": {"down_flip": slow_high,
                                     "up_flip": naive,
                                     "fast_down_gain": fast / slow_high}}


def local_shared_hidden_check():
    # Two visible bits plus one evolving, shared hidden bit; this challenges
    # the supplier interface, rather than scaling the completed easy ring.
    states = [(x, y, h) for x in range(2) for y in range(2) for h in range(2)]
    index = {s: i for i, s in enumerate(states)}
    native, compiled = [], []
    mu = [F(1, 8)] * 8
    weights = [F(2) if x == y else F(1, 2) for x, y, h in states]
    target = normalize([mu[i] * weights[i] for i in range(8)])
    for site in range(2):
        p = zeros(8)
        k = zeros(8)
        for other in range(2):
            ids = [i for i, s in enumerate(states) if s[1 - site] == other]
            local, _ = make_reversible([1, 1, 1, 1], 17 + 3 * site + other)
            for ii, i in enumerate(ids):
                for jj, j in enumerate(ids):
                    p[i][j] = local[ii][jj]
            lower = [ii for ii, i in enumerate(ids) if states[i][site] != other]
            local_compiled, _, _ = controller(local, lower, {4: F(1)})
            for ii, i in enumerate(ids):
                for jj, j in enumerate(ids):
                    k[i][j] = local_compiled[ii][jj]
        reversible(p, mu)
        reversible(k, target)
        assert all(p[i][j] == 0 for i in range(8) for j in range(8)
                   if states[i][1 - site] != states[j][1 - site])
        assert any(p[i][j] > 0 for i in range(8) for j in range(8)
                   if states[i][2] != states[j][2])
        native.append(p)
        compiled.append(k)
    scan = mul(compiled[0], compiled[1])
    assert row_times(target, scan) == target
    # The compiled visible kernel itself still depends on the unobserved bit.
    probs = []
    for h in range(2):
        x = index[(0, 0, h)]
        probs.append(sum(compiled[0][x][j] for j, s in enumerate(states) if s[0] == 1))
    assert probs[0] != probs[1]
    return {"state_count": 8, "visible_states": 4,
            "evolving_shared_hidden_states": 2, "target_microscopic_law": target,
            "target_visible_law": [F(2, 5), F(1, 10), F(1, 10), F(2, 5)],
            "compiled_flip_given_same_visible_different_hidden": probs,
            "local_reversibility_pairs": 128,
            "prescribed_scan_stationarity_exact": True}


def pmul(a, b):
    c = [F(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i + j] += x * y
    return c


def infinite_rank_moment_check():
    cap = 4
    poly = [F(1 + F(1, cap)) * comb(cap, j) * (-1) ** j for j in range(cap + 1)]
    poly[0] -= F(1, cap)
    lo, hi = F(1, 4), F(9, 20)
    moments = []
    power_poly = [F(1)]
    for _ in range(7):
        moments.append(sum(c * (hi ** (j + 1) - lo ** (j + 1)) / (j + 1)
                           for j, c in enumerate(power_poly)) / (hi - lo))
        power_poly = pmul(power_poly, poly)
    h = [[moments[i + j] for j in range(4)] for i in range(4)]
    pivots = []
    for k in range(4):
        pivot = h[k][k]
        assert pivot > 0
        pivots.append(pivot)
        for i in range(k + 1, 4):
            for j in range(k + 1, 4):
                h[i][j] -= h[i][k] * h[k][j] / pivot
    return {"cap": cap, "p_interval": [lo, hi], "moments": moments,
            "exact_positive_LDL_pivots": pivots,
            "all_orders_claim": "proved by polynomial-square integral, not inferred from finite checks"}


def main():
    result = {"scope": "Exact finite population-model verification; no apparatus data",
              "general_hidden_kernels": hidden_checks(),
              "iid_binary_specialization": binary_checks(),
              "local_composition_with_evolving_shared_memory": local_shared_hidden_check(),
              "infinite_rank_symbolic_moment_sanity": infinite_rank_moment_check(),
              "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    target = HERE / "REVERSIBLE_EXCURSION_CHECKS.json"
    target.write_text(json.dumps(jsonable(result), indent=2) + "\n")
    print(json.dumps({"output": str(target), "general_cases": 12,
                      "binary_cases": 25, "status": "all exact assertions passed"}))


if __name__ == "__main__":
    main()
