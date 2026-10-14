#!/usr/bin/env python3
"""Independent exact audit of normalized source-box closure.

This file uses only the Python standard library. The mathematical oracle is
direct rational vertex evaluation, separately checked against Edmonds-Karp.
It does not import the producer or root worker's scientific implementation.
"""
from collections import deque
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from pathlib import Path
import json
import platform
import random
import sys
import time

BASE = Path(__file__).resolve().parent
SOURCE = BASE.parent / "FG-sources" / "compact"
COUNTS = {"instances": 0, "vertices": 0, "thresholds": 0,
          "cut_identity_vertex_checks": 0, "flow_equalities": 0,
          "lower_vertex_checks": 0, "nested_checks": 0,
          "dinkelbach_cut_calls": 0, "interior_convexity_checks": 0}


def dot(x, y):
    return sum((a * b for a, b in zip(x, y)), F(0))


def mv(A, x):
    return [dot(row, x) for row in A]


def quad(A, x):
    return dot(x, mv(A, x))


def invert(A):
    n = len(A)
    M = [list(row) + [F(int(i == j)) for j in range(n)]
         for i, row in enumerate(A)]
    for k in range(n):
        pivot = next(i for i in range(k, n) if M[i][k])
        M[k], M[pivot] = M[pivot], M[k]
        a = M[k][k]
        M[k] = [v / a for v in M[k]]
        for i in range(n):
            if i != k:
                a = M[i][k]
                if a:
                    M[i] = [x - a * y for x, y in zip(M[i], M[k])]
    return [row[n:] for row in M]


def check_spd(A):
    """Exact LDL^T diagonal pivots; no eigenvalue tolerance."""
    n = len(A)
    assert all(A[i][j] == A[j][i] for i in range(n) for j in range(n))
    M = [list(row) for row in A]
    for k in range(n):
        assert M[k][k] > 0
        for i in range(k + 1, n):
            for j in range(i, n):
                M[i][j] -= M[i][k] * M[k][j] / M[k][k]
                M[j][i] = M[i][j]


def profile(ell, u, active, bits):
    s = list(ell)
    for i, z in zip(active, bits):
        if z:
            s[i] = u[i]
    return s


def coefficients(G, ell, u):
    n = len(ell)
    assert all(0 < ell[i] <= u[i] for i in range(n))
    check_spd(G)
    assert all(x >= 0 for row in G for x in row)
    active = [i for i in range(n) if ell[i] < u[i]]
    d = [u[i] - ell[i] for i in active]
    gell = mv(G, ell)
    a = [2 * di * gell[i] + di * di * G[i][i]
         for i, di in zip(active, d)]
    b = [[d[j] * d[k] * G[active[j]][active[k]]
          if j != k else F(0) for k in range(len(active))]
         for j in range(len(active))]
    alpha = [a[j] + sum(b[j], F(0)) for j in range(len(active))]
    assert all(x > 0 for x in alpha)
    return active, d, a, b, alpha, quad(G, ell), sum(ell, F(0))


def graph_cut(alpha, b, d, t, bits, pair_factor=F(1)):
    """z=1 on source side; monotone source-alpha, sink-t*d network."""
    return (sum((a * (1 - z) + t * di * z
                 for a, di, z in zip(alpha, d, bits)), F(0))
            + sum((pair_factor * b[i][j] * abs(bits[i] - bits[j])
                   for i in range(len(bits)) for j in range(i + 1, len(bits))), F(0)))


def mincut(alpha, b, d, t):
    """Exact Edmonds-Karp plus maximal source-side minimum-cut recovery."""
    assert t >= 0
    m = len(d)
    ss, tt = m, m + 1
    N = m + 2
    residual = [[F(0) for _ in range(N)] for _ in range(N)]
    for i in range(m):
        residual[ss][i] = alpha[i]
        residual[i][tt] = t * d[i]
        for j in range(i + 1, m):
            residual[i][j] = residual[j][i] = b[i][j]
    flow, augmentations = F(0), 0
    while True:
        parent = [-1] * N
        parent[ss] = ss
        Q = deque([ss])
        while Q and parent[tt] == -1:
            v = Q.popleft()
            for w in range(N):
                if parent[w] == -1 and residual[v][w] > 0:
                    parent[w] = v
                    Q.append(w)
        if parent[tt] == -1:
            break
        w = tt
        path = []
        while w != ss:
            v = parent[w]
            path.append((v, w))
            w = v
        delta = min(residual[v][w] for v, w in path)
        for v, w in path:
            residual[v][w] -= delta
            residual[w][v] += delta
        flow += delta
        augmentations += 1
    # Every minimum-cut source side excludes any node that can reach tt.
    reaches_sink = {tt}
    Q = deque([tt])
    while Q:
        w = Q.popleft()
        for v in range(N):
            if v not in reaches_sink and residual[v][w] > 0:
                reaches_sink.add(v)
                Q.append(v)
    assert ss not in reaches_sink
    bits = tuple(int(i not in reaches_sink) for i in range(m))
    assert graph_cut(alpha, b, d, t, bits) == flow
    return flow, bits, augmentations


def dinkelbach(G, ell, u, initialize="zero"):
    active, d, a, b, alpha, q0, Z0 = coefficients(G, ell, u)
    t = F(0) if initialize == "zero" else q0 / Z0
    steps = []
    prev_bits = None
    for _ in range(len(active) + 3):
        flow, bits, aug = mincut(alpha, b, d, t)
        s = profile(ell, u, active, bits)
        q, Z = quad(G, s), sum(s, F(0))
        H = q0 - t * Z0 + sum(alpha, F(0)) - flow
        assert H == q - t * Z
        assert H >= 0
        if prev_bits is not None:
            assert all(x <= y for x, y in zip(bits, prev_bits))
            COUNTS["nested_checks"] += 1
        steps.append({"threshold": str(t), "bits": list(bits), "excess": str(H),
                      "q": str(q), "mass": str(Z), "ratio": str(q / Z),
                      "cut": str(flow), "augmentations": aug})
        COUNTS["dinkelbach_cut_calls"] += 1
        if H == 0:
            assert len(steps) <= len(active) + (2 if initialize == "zero" else 1)
            return t, s, steps
        new_t = q / Z
        assert new_t > t
        t, prev_bits = new_t, bits
    raise AssertionError("finite Dinkelbach bound violated")


def lower_scan(ell, u, v, c):
    r = [2 * x for x in v]
    order = sorted(range(len(ell)), key=lambda i: (r[i], i))
    s = list(ell)
    numerator, mass = dot(r, s) - c, sum(s, F(0))
    candidates = [(numerator / mass, tuple(s), 0)]
    for k, i in enumerate(order, 1):
        numerator += r[i] * (u[i] - ell[i])
        mass += u[i] - ell[i]
        s[i] = u[i]
        candidates.append((numerator / mass, tuple(s), k))
    L, s, k = min(candidates, key=lambda x: x[0])
    psi = -c + sum((min((ri - L) * lo, (ri - L) * hi)
                    for ri, lo, hi in zip(r, ell, u)), F(0))
    assert psi == 0
    return L, list(s), k


def audit_instance(G, ell, u, Gplus=None, name="random"):
    active, d, a, b, alpha, q0, Z0 = coefficients(G, ell, u)
    vertices = list(product((0, 1), repeat=len(active)))
    data = [(bits, profile(ell, u, active, bits)) for bits in vertices]
    qz = [(bits, s, quad(G, s), sum(s, F(0))) for bits, s in data]
    U = max(q / Z for _, _, q, Z in qz)
    old_U = quad(G, u) / Z0
    assert U <= old_U
    COUNTS["instances"] += 1
    COUNTS["vertices"] += len(vertices)
    thresholds = sorted(set((F(0), q0 / Z0, U, U + F(1), U / 2)))
    prev_bits = None
    for t in thresholds:
        direct = max(q - t * Z for _, _, q, Z in qz)
        cuts = [(graph_cut(alpha, b, d, t, bits), bits) for bits in vertices]
        C = min(x[0] for x in cuts)
        for bits, _, q, Z in qz:
            assert q - t * Z == q0 - t * Z0 + sum(alpha, F(0)) - graph_cut(alpha, b, d, t, bits)
            COUNTS["cut_identity_vertex_checks"] += 1
        flow, bits, aug = mincut(alpha, b, d, t)
        assert flow == C
        assert direct == q0 - t * Z0 + sum(alpha, F(0)) - flow
        all_min_bits = [zs for val, zs in cuts if val == C]
        maximal_bits = tuple(max(zs[i] for zs in all_min_bits) for i in range(len(active)))
        assert bits == maximal_bits
        if prev_bits is not None:
            assert all(x <= y for x, y in zip(bits, prev_bits))
            COUNTS["nested_checks"] += 1
        prev_bits = bits
        COUNTS["thresholds"] += 1
        COUNTS["flow_equalities"] += 1
    Ucut, witness, steps0 = dinkelbach(G, ell, u)
    Ucut1, _, steps1 = dinkelbach(G, ell, u, "ell")
    assert Ucut == Ucut1 == U
    # A rational interior mixture is bounded by the vertex maximum.
    s_mid = [(lo + hi) / 2 for lo, hi in zip(ell, u)]
    assert quad(G, s_mid) / sum(s_mid, F(0)) <= U
    COUNTS["interior_convexity_checks"] += 1
    Gplus = G if Gplus is None else Gplus
    v = mv(Gplus, ell)
    assert all(x >= 0 for x in v)
    c = dot(ell, v)
    L, lwitness, prefix = lower_scan(ell, u, v, c)
    assert c / sum(u, F(0)) <= L <= c / sum(ell, F(0))
    direct_L = min((2 * dot(s, v) - c) / Z for _, s, _, Z in qz)
    assert L == direct_L
    COUNTS["lower_vertex_checks"] += len(vertices)
    return {"name": name, "n": len(ell), "m": len(active),
            "old_upper": str(old_U), "upper": str(U), "upper_decimal": float(U),
            "upper_witness": list(map(str, witness)),
            "old_lower": str(c / sum(u, F(0))), "fixed_trial_lower": str(L),
            "lower_decimal": float(L), "lower_witness": list(map(str, lwitness)),
            "lower_prefix_length": prefix,
            "calls_zero": len(steps0), "calls_ell": len(steps1),
            "trace_zero": steps0, "trace_ell": steps1}


def random_instances():
    rng = random.Random(20261014)
    records = []
    for case in range(168):
        n = 1 + case % 7
        B = [[F(rng.randrange(5), rng.randrange(1, 5)) for _ in range(n)] for _ in range(n)]
        G = [[sum((B[i][k] * B[j][k] for k in range(n)), F(0))
              + (F(rng.randrange(1, 6), rng.randrange(1, 5)) if i == j else F(0))
              for j in range(n)] for i in range(n)]
        ell = [F(rng.randrange(1, 8), rng.randrange(1, 7)) for _ in range(n)]
        u = [lo + F(rng.randrange(5), rng.randrange(1, 6)) for lo in ell]
        records.append(audit_instance(G, ell, u, name=f"seeded-{case}"))
    return records


def source_cases():
    n, N = 4, 16
    q, eps = F(1, 26), F(1, 10000)
    mass = [q ** g.bit_count() * (1 - q) ** (n - g.bit_count()) for g in range(N)]
    def form(weight):
        A = [[F(0) for _ in range(N)] for _ in range(N)]
        for g in range(N):
            A[g][g] += mass[g] * weight[g] * q * (1 if g & 8 else eps)
            for i in range(n):
                if g & (1 << i):
                    continue
                h = g | (1 << i)
                gate = F(1) if i == 0 or g & (1 << (i - 1)) else eps
                c = mass[g] * q * gate * min(weight[g], weight[h])
                A[g][g] += c
                A[h][h] += c
                A[g][h] -= c
                A[h][g] -= c
        return A
    G = invert(form([F(1)] * N))
    records = []
    producer = {(x["feature"], x["R"]): x for x in json.loads((SOURCE / "conditional_envelope_results.json").read_text())}
    for feature in ("all_open", "first_open", "all_closed"):
        for R in (3, 100):
            indicator = lambda g: int(g == 15) if feature == "all_open" else (g & 1) if feature == "first_open" else int(g == 0)
            weight = [F(1 + (R - 1) * indicator(g)) for g in range(N)]
            u = [m * w for m, w in zip(mass, weight)]
            Gplus = invert(form(weight))
            record = audit_instance(G, mass, u, Gplus, f"source-{feature}-R{R}")
            assert record["old_upper"] == str(F(producer[feature, R]["upper_exact"]))
            assert record["old_lower"] == str(F(producer[feature, R]["lower_exact"]))
            record["feature"], record["R"] = feature, R
            records.append(record)
    return records


def controls():
    controls = {}
    G = [[F(100), F(0)], [F(0), F(1)]]
    ell, u = [F(1), F(1)], [F(1), F(2)]
    r = audit_instance(G, ell, u, name="all-upper-is-suboptimal")
    assert r["upper"] == "101/2"
    assert quad(G, u) / sum(u) == F(104, 3)
    controls["all_upper_is_suboptimal"] = r
    scalar = audit_instance([[F(1)]], [F(1)], [F(2)], name="normalization-gap")
    assert scalar["old_upper"] == "4" and scalar["upper"] == "2"
    controls["normalization_gap"] = scalar
    Gbad = [[F(1), F(-9, 10)], [F(-9, 10), F(1)]]
    check_spd(Gbad)
    x, hi = [F(1), F(1, 10)], [F(1), F(1)]
    assert quad(Gbad, x) == F(83, 100) > quad(Gbad, hi) == F(1, 5)
    rejected = False
    try:
        coefficients(Gbad, [F(1, 10)] * 2, hi)
    except AssertionError:
        rejected = True
    assert rejected, "sign control did not reject negative G entries"
    controls["spd_without_entrywise_positivity"] = {
        "G": [[str(x) for x in row] for row in Gbad],
        "source_x": list(map(str, x)), "source_u": list(map(str, hi)),
        "q_x": str(quad(Gbad, x)), "q_u": str(quad(Gbad, hi)),
        "meaning": "PSD alone does not permit q(w)<=q(u), nonnegative pair capacities, or attractive nesting."}
    # Factor mutation: there exists a split-cut where 2*b is incorrect.
    G = [[F(2), F(1)], [F(1), F(2)]]
    ell, u = [F(1)] * 2, [F(2)] * 2
    active, d, a, b, alpha, q0, Z0 = coefficients(G, ell, u)
    bits, t = (1, 0), F(4)
    s = profile(ell, u, active, bits)
    excess = quad(G, s) - t * sum(s)
    mutated = q0 - t * Z0 + sum(alpha) - graph_cut(alpha, b, d, t, bits, F(2))
    assert excess != mutated
    controls["double_pair_capacity_mutation"] = {"bits": list(bits), "threshold": str(t),
        "true_excess": str(excess), "mutated_excess": str(mutated), "detected": True}
    # In an equal-mass source mixture, averaging ratios without mass weights is invalid.
    G = [[F(1)]]
    x, y, p = [F(1)], [F(3)], F(1, 2)
    mixture = (p * quad(G, x) + (1 - p) * quad(G, y)) / (p * sum(x) + (1 - p) * sum(y))
    naive = p * quad(G, x) / sum(x) + (1 - p) * quad(G, y) / sum(y)
    assert mixture == F(5, 2) != naive == F(2)
    controls["mixture_requires_mass_weighting"] = {"mixture_ratio": str(mixture),
        "naive_average_of_ratios": str(naive), "correct_weight_on_y": "3/4"}
    # Positivity of total mass is load-bearing even for G=I.
    eps = F(1, 1000)
    s = [F(-1) + eps, F(1)]
    ratio = dot(s, s) / sum(s)
    assert ratio > 1000
    controls["mass_boundary"] = {"s": list(map(str, s)), "G": "I_2", "ratio": str(ratio),
        "meaning": "A box touching mass zero admits divergence as epsilon decreases; ell_i>0 excludes it."}
    # Fixed-trial lower optimization does not equal reoptimized lower envelope.
    lo, hi, v = [F(1), F(1)], [F(1), F(20)], [F(100), F(1)]
    L, _, _ = lower_scan(lo, hi, v, F(101))
    assert L == F(139, 21)
    controls["fixed_trial_lower_scope"] = {"fixed_trial_lower": str(L),
        "reoptimized_minimizer_second_coordinate": "sqrt(101)-1",
        "reoptimized_minimum": "2*(sqrt(101)-1)",
        "meaning": "Exact fixed-trial lower is generally weaker than optimizing the retained trial field for mean source."}
    # A rationalized near-optimal field gives an exact lower certificate.
    y = F(72399, 8000)
    v_rational = [F(100), y]
    c_rational = F(100) + y * y
    Lr, witness, prefix = lower_scan(lo, hi, v_rational, c_rational)
    Ur = (F(100) + y * y) / (1 + y)
    assert 0 < Ur - Lr < F(1, 100000)
    assert (Lr / 2 + 1) ** 2 <= 101 <= (Ur / 2 + 1) ** 2
    for bits in product((0, 1), repeat=2):
        s = [hi[i] if bits[i] else lo[i] for i in range(2)]
        assert (2 * dot(s, v_rational) - c_rational) / sum(s) >= Lr
    controls["rational_field_certificate_for_irrational_lower"] = {
        "v": list(map(str, v_rational)), "energy": str(c_rational),
        "certified_lower": str(Lr), "rational_primal_upper_on_lower_optimum": str(Ur),
        "interval_width": str(Ur - Lr), "lower_witness": list(map(str, witness)),
        "lower_prefix_length": prefix, "exact_algebraic_optimum": "2*(sqrt(101)-1)",
        "meaning": "Optimization approximation affects tightness; all reported certificate arithmetic is rational."}
    # Sharpness over physical completions can fail even in one state:
    # if weighted form A_s=s, actual q_s(s)/mass is always 1.
    controls["physical_sharpness_failure"] = {"ell": "1", "u": "2", "A_minus": "1", "A_plus": "2",
        "admissible_physical_form": "A_s=s", "physical_tau_all_s": "1",
        "source_only_upper": "2", "meaning": "Source and form extrema cannot be combined independently in this physical class."}
    return controls


def main():
    started = time.time()
    random_results = random_instances()
    source_results = source_cases()
    countercontrols = controls()
    elapsed = time.time() - started
    payload = {"status": "PASS", "scope": "finite represented rational retained sources only; internally reconstructed audit",
        "python": sys.version, "platform": platform.platform(),
        "elapsed_seconds": elapsed, "counts": COUNTS,
        "random_seed": 20261014, "random_instances": len(random_results),
        "maximum_calls_zero": max(x["calls_zero"] for x in random_results),
        "maximum_calls_ell": max(x["calls_ell"] for x in random_results),
        "random_summary": [{k: x[k] for k in ("name", "n", "m", "upper", "fixed_trial_lower", "calls_zero", "calls_ell")}
                           for x in random_results],
        "source_cases": source_results, "countercontrols": countercontrols,
        "source_hashes": {f: sha256((SOURCE / f).read_bytes()).hexdigest()
                          for f in ("RESEARCH_NOTE.md", "conditional_envelope.py", "conditional_envelope_results.json")}}
    path = BASE / "independent_results.json"
    path.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps({"status": payload["status"], "elapsed_seconds": elapsed, "counts": COUNTS,
        "maximum_calls_zero": payload["maximum_calls_zero"], "maximum_calls_ell": payload["maximum_calls_ell"],
        "source_summary": [{k: x[k] for k in ("feature", "R", "m", "upper_decimal", "lower_decimal", "calls_zero", "calls_ell")}
                           for x in source_results], "output": str(path)}, indent=2))


if __name__ == "__main__":
    main()
