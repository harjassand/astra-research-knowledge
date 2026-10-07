"""Exact finite controls for the discovery-foundations report.

These checks do not implement or validate the full release-103 estimator.
They check only the independent deductions and legal-action boundaries.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
from random import Random
import hashlib
import json
import time
import tracemalloc


def mul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]


def charpoly(a):
    n = len(a)
    b = [[F(i == j) for j in range(n)] for i in range(n)]
    cs = [F(1)]
    for k in range(1, n + 1):
        b = mul(a, b)
        c = -sum(b[i][i] for i in range(n)) / k
        cs.append(c)
        for i in range(n):
            b[i][i] += c
    return cs


def integer_roots(cs, lo, hi):
    cs = list(cs)
    roots = []
    for r in range(lo, hi + 1):
        while len(cs) > 1:
            out = [cs[0]]
            for c in cs[1:]:
                out.append(c + out[-1] * r)
            if out[-1]:
                break
            roots.append(r)
            cs = out[:-1]
    return roots, cs


def affine_torus_fixture():
    states = list(product(range(2), repeat=3))
    index = {s: i for i, s in enumerate(states)}
    # K=(9I+sum of nine permutation matrices)/18.  The signed
    # elementary/translation generators coincide in pairs modulo 2.
    b = [[9 * int(i == j) for j in range(8)] for i in range(8)]
    for s in states:
        moves = []
        for i in range(3):
            z = list(s)
            z[i] ^= 1
            moves.append(tuple(z))
            for j in range(3):
                if i != j:
                    z = list(s)
                    z[i] ^= s[j]
                    moves.append(tuple(z))
        for z in moves:
            b[index[s]][index[z]] += 1
    assert all(sum(r) == 18 for r in b)
    assert all(b[i][j] == b[j][i] for i in range(8) for j in range(8))
    cs = charpoly(b)
    roots, remainder = integer_roots(cs, 0, 18)
    assert roots.count(18) == 1
    k = [[F(x, 18) for x in row] for row in b]
    cube = mul(mul(k, k), k)
    alpha = sum(min(row[j] for row in cube) for j in range(8))
    assert alpha > 0
    # Dobrushin contraction of K^3 bounds lambda_2^3 <= 1-alpha.
    # Bernoulli's inequality then gives gap(K) >= alpha/3.
    gap_lower = alpha / 3
    return {"states": 8, "numerator_matrix": b,
            "charpoly_numerator": [str(c) for c in cs],
            "integer_numerator_eigenvalues": roots,
            "rejected_integer_spectrum_assumption": {
                "reason": "Only the stationary root is an integer.",
                "remaining_polynomial": list(map(str, remainder))},
            "exact_three_step_dobrushin_alpha": str(alpha),
            "rigorous_gap_lower_bound": str(gap_lower)}


def product_state_step(state, action):
    bits, flags = state
    nxt = (bits[0] | action, bits[1] ^ action, 0)
    pairs = [(0, 1), (0, 2), (1, 2)]
    flags = tuple(old or nxt[i] != nxt[j]
                  for old, (i, j) in zip(flags, pairs))
    return nxt, flags


def acceptance(state, remaining):
    if not remaining:
        return F(all(state[1]))
    return sum(acceptance(product_state_step(state, a), remaining - 1)
               for a in (0, 1)) / 2


def accepting_path_fixture():
    initial = ((0, 0, 0), (False, False, False))
    valid = []
    for w in product((0, 1), repeat=2):
        state = initial
        for a in w:
            state = product_state_step(state, a)
        if all(state[1]):
            valid.append(w)
    state = initial
    chosen = []
    values = [acceptance(initial, 2)]
    for remaining in (2, 1):
        action = max((0, 1), key=lambda a:
                     acceptance(product_state_step(state, a), remaining - 1))
        chosen.append(action)
        state = product_state_step(state, action)
        values.append(acceptance(state, remaining - 1))
    assert tuple(chosen) in valid
    return {"models": ["Boolean OR", "Boolean XOR", "constant zero"],
            "valid_action_words": valid,
            "random_search_success": str(acceptance(initial, 2)),
            "greedy_word": chosen, "continuation_values": list(map(str, values)),
            "scope": "Exact finite continuation control; full 103 compiler not implemented."}


def mdp_values(kernels, horizon, policy=None):
    n = len(kernels)
    values = [[F(s == n - 1) for s in range(n)]]
    qvals = []
    for t in range(horizon):
        prev = values[-1]
        qs = [[sum(p * prev[z] for z, p in enumerate(row))
               for row in kernels[s]] for s in range(n)]
        qvals.append(qs)
        if policy is None:
            values.append([sum(q) / len(q) for q in qs])
        else:
            values.append([qs[s][policy[t][s]] for s in range(n)])
    return values, qvals


def rollout_controls():
    rng = Random(20261007)
    horizon, delta, epsilon = 4, F(1, 128), F(1, 16)
    count = 0
    min_surplus = None
    model_min_surplus = None
    for _ in range(200):
        kernels = []
        for s in range(4):
            acts = []
            for a in range(2):
                cuts = sorted([0, 8] + [rng.randrange(9) for _ in range(3)])
                acts.append([F(cuts[z + 1] - cuts[z], 8) for z in range(4)])
            kernels.append(acts)
        base, qs = mdp_values(kernels, horizon)
        policy = [[max(range(2), key=lambda a:
                       qs[t][s][a] + rng.choice((-delta, F(0), delta)))
                   for s in range(4)] for t in range(horizon)]
        improved, _ = mdp_values(kernels, horizon, policy)
        # Each action was selected from deterministic bounded-error scores.
        surplus = improved[-1][0] - base[-1][0] + 2 * horizon * delta
        assert surplus >= 0
        min_surplus = surplus if min_surplus is None else min(min_surplus, surplus)
        true_kernels = [[[((1 - epsilon) * p + epsilon * int(z == 0))
                          for z, p in enumerate(row)] for row in acts]
                        for acts in kernels]
        for s in range(4):
            for a in range(2):
                tv = sum(abs(p - q) for p, q in
                         zip(kernels[s][a], true_kernels[s][a])) / 2
                assert tv <= epsilon
        true, _ = mdp_values(true_kernels, horizon, policy)
        surplus2 = (true[-1][0] - base[-1][0]
                    + 2 * horizon * delta + horizon * epsilon)
        assert surplus2 >= 0
        model_min_surplus = (surplus2 if model_min_surplus is None
                             else min(model_min_surplus, surplus2))
        count += 1
    return {"rational_mdp_fixtures": count, "states": 4, "actions": 2,
            "horizon": horizon, "score_error": str(delta),
            "row_model_tv_error": str(epsilon),
            "minimum_rollout_bound_surplus": str(min_surplus),
            "minimum_model_bound_surplus": str(model_min_surplus)}


def commuting_projection_fixture():
    checks = 0
    for h in range(3, 15):
        pairs = [(i, i + 1) for i in range(0, h - 1, 2)]
        if h % 2:
            pairs.append((0, h - 1))
        assert len(pairs) == (h + 1) // 2
        for pattern in product((0, 1), repeat=h):
            bad = [int(not (pattern[i] and pattern[j])) for i, j in pairs]
            assert int(not all(pattern)) <= sum(bad)
            checks += 1
    return {"exact_joint_eigenspace_checks": checks,
            "dimensions": [3, 14],
            "scope": "Finite scalar controls for the proved commuting-projection inequality."}


def main():
    start = time.perf_counter()
    tracemalloc.start()
    results = {"affine_torus": affine_torus_fixture(),
               "accepting_path": accepting_path_fixture(),
               "rollout": rollout_controls(),
               "projections": commuting_projection_fixture(),
               "environmental_coin_counterexample": {
                   "actions": 1, "true_success_probability": "1/2",
                   "favorable_accepted_path_value": 1,
                   "error": "The uncontrolled coin outcome cannot be chosen as an action."}}
    sources = Path(__file__).parent / "sources"
    results["source_sha256"] = {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                                for p in sources.glob("*.pdf")}
    results["elapsed_seconds"] = time.perf_counter() - start
    results["peak_traced_python_bytes"] = tracemalloc.get_traced_memory()[1]
    results["status"] = "PASS: finite deduction controls only"
    out = Path(__file__).parent / "checks.json"
    out.write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps({"status": results["status"],
                      "affine_gap_lower_bound": results["affine_torus"]["rigorous_gap_lower_bound"],
                      "projection_checks": results["projections"]["exact_joint_eigenspace_checks"],
                      "mdp_fixtures": results["rollout"]["rational_mdp_fixtures"],
                      "elapsed_seconds": results["elapsed_seconds"],
                      "peak_traced_python_bytes": results["peak_traced_python_bytes"]}, indent=2))


if __name__ == "__main__":
    main()
