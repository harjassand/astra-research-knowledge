"""Floating small-state check of adaptive sparse Poisson-sensor filtering.

The 2^3-state uniformization used for marked first-click CDFs is a diagnostic
substitute for the proposed acquired boundary-resolvent/CDF primitive.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "controlled_product"))
from demo import (N, age_bins, age_kernel, flip_rates, mixture_vector,
                  product_vector, uniformized)


P = (0.5, 0.5, 0.5)
LAM = (0.3, 0.3, 0.3)
INITIAL = (0.5, 0.5, 0.5)
T = 0.7
TARGET_BIT = 0
MENU = {
    "A": {1: 2.2, 3: 2.2, 5: 2.2, 7: 2.2},
    "B": {0: 2.0, 2: 2.0, 4: 2.0, 6: 2.0},
    "C": {0: 5.0, 7: 5.0},
}


def free_evolve(vec, p=P, lam=LAM, t=T):
    d = 1 << N
    out = [0.0] * d
    decay = [math.exp(-li * t) for li in lam]
    for x, vx in enumerate(vec):
        q = [p[i] + (((x >> i) & 1) - p[i]) * decay[i] for i in range(N)]
        px = product_vector(q)
        for y in range(d):
            out[y] += vx * px[y]
    return out


def soft_no_click(vec, hazard, p=P, lam=LAM, t=T):
    d = 1 << N
    rate = sum(lam) + max(hazard.values())

    def step(v):
        out = [0.0] * d
        for x, vx in enumerate(v):
            rates = tuple(flip_rates(x, p, lam))
            out[x] += vx * (1.0 - (sum(r for _, r in rates) +
                                    hazard.get(x, 0.0)) / rate)
            for y, r in rates:
                out[y] += vx * r / rate
        return out

    return uniformized(vec, step, rate * t)


def first_click_cdf(vec, hazard, t, p=P, lam=LAM):
    targets = tuple(sorted(hazard))
    pos = {b: (1 << N) + j for j, b in enumerate(targets)}
    rate = sum(lam) + max(hazard.values())
    init = list(vec) + [0.0] * len(targets)

    def step(v):
        out = [0.0] * len(v)
        for x in range(1 << N):
            vx = v[x]
            rates = tuple(flip_rates(x, p, lam))
            out[x] += vx * (1.0 - (sum(r for _, r in rates) +
                                    hazard.get(x, 0.0)) / rate)
            for y, r in rates:
                out[y] += vx * r / rate
            if x in pos:
                out[pos[x]] += vx * hazard[x] / rate
        for j in range(len(targets)):
            out[(1 << N) + j] += v[(1 << N) + j]
        return out

    return dict(zip(targets, uniformized(init, step, rate * t)[1 << N:]))


def exact_branches(vec, hazard):
    no = soft_no_click(vec, hazard)
    free = free_evolve(vec)
    click = [f - z for f, z in zip(free, no)]
    return no, click


def solve(matrix, rhs):
    """Tiny dense pivoted solve, used only for the n=3 transform check."""
    d = len(rhs)
    a = [list(row) + [rhs[i]] for i, row in enumerate(matrix)]
    for j in range(d):
        pivot = max(range(j, d), key=lambda i: abs(a[i][j]))
        a[j], a[pivot] = a[pivot], a[j]
        div = a[j][j]
        if abs(div) < 1e-14:
            raise ArithmeticError("singular diagnostic matrix")
        for k in range(j, d + 1):
            a[j][k] /= div
        for i in range(d):
            if i == j:
                continue
            factor = a[i][j]
            for k in range(j, d + 1):
                a[i][k] -= factor * a[j][k]
    return [a[i][d] for i in range(d)]


def boundary_transform_error(hazard, s=0.71):
    """Compare the small Woodbury solve with the full soft-killed resolvent."""
    d = 1 << N
    targets = tuple(sorted(hazard))
    mu = product_vector(INITIAL)
    qgen = [[0.0] * d for _ in range(d)]
    for x in range(d):
        for y, rate in flip_rates(x, P, LAM):
            qgen[x][y] += rate
            qgen[x][x] -= rate
    free_matrix = [
        [(s if i == j else 0.0) - qgen[i][j] for j in range(d)]
        for i in range(d)
    ]
    free_columns = []
    direct = []
    for b in targets:
        rhs = [1.0 if x == b else 0.0 for x in range(d)]
        free_columns.append(solve(free_matrix, rhs))
        soft_matrix = [list(row) for row in free_matrix]
        for x, gain in hazard.items():
            soft_matrix[x][x] += gain
        col = solve(soft_matrix, rhs)
        direct.append(hazard[b] * sum(mu[x] * col[x] for x in range(d)))
    w = [sum(mu[x] * col[x] for x in range(d)) for col in free_columns]
    h = [[free_columns[j][b] for j in range(len(targets))]
         for b in targets]
    mat = [[(1.0 if i == j else 0.0) + hazard[targets[i]] * h[i][j]
            for j in range(len(targets))] for i in range(len(targets))]
    # A row solve y M=w is the column solve M^T y=w.
    y = solve([[mat[j][i] for j in range(len(targets))]
               for i in range(len(targets))], w)
    boundary = [y[j] * hazard[b] for j, b in enumerate(targets)]
    return max(abs(a - b) for a, b in zip(boundary, direct))


def compile_branches(components, hazard, small, ratio, large):
    signed_vec = mixture_vector(components)
    targets = tuple(sorted(hazard))
    bins = age_bins(T, small, ratio, large)
    free = [
        (c, tuple(P[i] + (q[i] - P[i]) * math.exp(-LAM[i] * T)
                  for i in range(N)))
        for c, q in components
    ]
    cache = {}

    def G(t):
        t = max(t, 0.0)
        if t not in cache:
            cache[t] = first_click_cdf(signed_vec, hazard, t)
        return cache[t]

    click = []
    for a, b, rep in bins:
        end = G(T - a)
        begin = {target: 0.0 for target in targets} if b == T else G(T - b)
        for target in targets:
            weight = end[target] - begin[target]
            q = P if rep is None else age_kernel(target, rep, P, LAM)
            click.append((weight, q))
    no = free + [(-c, q) for c, q in click]
    return no, click


def mixture_bit_accuracy(no, click, bit=TARGET_BIT):
    score = 0.0
    for components in (no, click):
        one = sum(c * q[bit] for c, q in components)
        zero = sum(c * (1.0 - q[bit]) for c, q in components)
        score += max(zero, one)
    return score


def vector_bit_accuracy(no, click, bit=TARGET_BIT):
    score = 0.0
    for vec in (no, click):
        one = sum(vec[x] for x in range(1 << N) if (x >> bit) & 1)
        zero = sum(vec[x] for x in range(1 << N) if not ((x >> bit) & 1))
        score += max(zero, one)
    return score


def choose(components, true_vec, small, ratio, large):
    rows = {}
    for name, hazard in MENU.items():
        approx = compile_branches(components, hazard, small, ratio, large)
        exact = exact_branches(true_vec, hazard)
        rows[name] = {
            "approx_utility": mixture_bit_accuracy(*approx),
            "exact_utility": vector_bit_accuracy(*exact),
            "approx_branches": approx,
            "exact_branches": exact,
        }
    selected = max(rows, key=lambda name: rows[name]["approx_utility"])
    best = max(rows, key=lambda name: rows[name]["exact_utility"])
    result = {
        "selected": selected,
        "exact_optimal": best,
        "regret": rows[best]["exact_utility"] - rows[selected]["exact_utility"],
        "utilities": {name: {
            "approx": round(row["approx_utility"], 10),
            "exact": round(row["exact_utility"], 10),
        } for name, row in rows.items()},
    }
    return result, rows[selected]


def run(small, ratio, large):
    components = [(1.0, INITIAL)]
    true_vec = product_vector(INITIAL)
    first, chosen_row = choose(components, true_vec, small, ratio, large)
    continuations = {}
    for y, name in enumerate(("no_click", "click")):
        approx_state = chosen_row["approx_branches"][y]
        exact_state = chosen_row["exact_branches"][y]
        second, _ = choose(approx_state, exact_state, small, ratio, large)
        continuations[name] = {
            "branch_probability": round(sum(exact_state), 10),
            "branch_terms": len(approx_state),
            "branch_l1_error": round(sum(abs(a - b) for a, b in
                                         zip(mixture_vector(approx_state), exact_state)), 10),
            "second_choice": second,
        }
    return {"first_choice": first, "adaptive_continuations": continuations}


if __name__ == "__main__":
    print(json.dumps({
        "boundary_transform_max_error": boundary_transform_error(MENU["A"]),
        "coarse": run(0.04, 1.5, 1.5),
        "fine": run(0.01, 1.2, 1.5),
    }, indent=2))
