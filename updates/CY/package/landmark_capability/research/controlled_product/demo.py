"""Small independent check of the piecewise killed-state product compiler.

The marked CDF in this demonstration is computed by explicit-state
uniformization.  The proposed large-n compiler substitutes the finite-bit
marked CDF routine in work/target_set_resolvent/MARKED_EVENTS.txt.
"""

from __future__ import annotations

import json
import math


N = 3
TARGETS = (1, 6)
STAGES = (
    ((0.21, 0.64, 0.37), (1.1, 0.4, 2.3), 0.8),
    ((0.73, 0.26, 0.58), (0.5, 1.4, 0.8), 1.0),
    ((0.43, 0.76, 0.19), (1.3, 0.7, 1.2), 0.9),
)
INITIAL = (0.8, 0.2, 0.7)


def product_vector(q):
    out = []
    for x in range(1 << N):
        v = 1.0
        for i, qi in enumerate(q):
            v *= qi if ((x >> i) & 1) else 1.0 - qi
        out.append(v)
    return out


def mixture_vector(components):
    out = [0.0] * (1 << N)
    for c, q in components:
        p = product_vector(q)
        for x in range(1 << N):
            out[x] += c * p[x]
    return out


def uniformized(initial, step, theta):
    """Uniformization; theta is Lambda*t and is <10 in this experiment."""
    weight = math.exp(-theta)
    subtotal = weight
    current = list(initial)
    out = [weight * x for x in current]
    j = 0
    while 1.0 - subtotal > 2e-15:
        j += 1
        current = step(current)
        weight *= theta / j
        subtotal += weight
        for a in range(len(out)):
            out[a] += weight * current[a]
        if j > 300:
            raise ArithmeticError("uniformization failed to converge")
    return out


def flip_rates(x, p, lam):
    for i in range(N):
        bit = (x >> i) & 1
        yield x ^ (1 << i), lam[i] * (1.0 - p[i] if bit else p[i])


def killed_evolve(vec, p, lam, t):
    L = sum(lam)
    init = [0.0 if x in TARGETS else vec[x] for x in range(1 << N)]

    def step(v):
        out = [0.0] * (1 << N)
        for x, vx in enumerate(v):
            if x in TARGETS:
                continue
            rates = tuple(flip_rates(x, p, lam))
            out[x] += vx * (1.0 - sum(r for _, r in rates) / L)
            for y, r in rates:
                if y not in TARGETS:
                    out[y] += vx * r / L
        return out

    return uniformized(init, step, L * t)


def marked_cdf(vec, p, lam, t):
    """F_b(t), including each atom at t=0, for a signed input vector."""
    d = 1 << N
    L = sum(lam)
    pos = {b: d + j for j, b in enumerate(TARGETS)}
    init = [0.0] * (d + len(TARGETS))
    for x, vx in enumerate(vec):
        init[pos[x] if x in pos else x] += vx

    def step(v):
        out = [0.0] * len(v)
        for x in range(d):
            if x in pos:
                continue
            vx = v[x]
            rates = tuple(flip_rates(x, p, lam))
            out[x] += vx * (1.0 - sum(r for _, r in rates) / L)
            for y, r in rates:
                out[pos[y] if y in pos else y] += vx * r / L
        for j in range(len(TARGETS)):
            out[d + j] += v[d + j]
        return out

    return uniformized(init, step, L * t)[d:]


def age_kernel(b, age, p, lam):
    return tuple(p[i] + (((b >> i) & 1) - p[i]) * math.exp(-lam[i] * age)
                 for i in range(N))


def age_bins(T, small, ratio, large):
    """(young age, old age, representative age or stationary marker)."""
    if T <= small:
        return [(0.0, T, 0.0)]
    out = [(0.0, small, 0.0)]
    a = small
    while a < min(T, large) * (1.0 - 1e-13):
        b = min(a * ratio, T, large)
        if b <= a:
            raise ArithmeticError("age grid stalled")
        out.append((a, b, a))
        a = b
    if a < T * (1.0 - 1e-13):
        out.append((a, T, None))
    return out


def compile_stage(components, p, lam, T, small, ratio, large):
    incoming = mixture_vector(components)
    bins = age_bins(T, small, ratio, large)
    cache = {}

    def F(t):
        t = max(0.0, t)
        if t not in cache:
            cache[t] = marked_cdf(incoming, p, lam, t)
        return cache[t]

    propagated = [
        (c, tuple(p[i] + (q[i] - p[i]) * math.exp(-lam[i] * T)
                  for i in range(N)))
        for c, q in components
    ]
    exit_abs = 0.0
    for a, b, rep in bins:
        Fb = F(T - a)
        # The oldest bin includes the first-hit atom at physical time zero.
        Fa = [0.0] * len(TARGETS) if b == T else F(T - b)
        for j, target in enumerate(TARGETS):
            mass = Fb[j] - Fa[j]
            exit_abs += abs(mass)
            q = p if rep is None else age_kernel(target, rep, p, lam)
            propagated.append((-mass, q))
    return propagated, len(bins), exit_abs


def run(small, ratio, large):
    true = product_vector(INITIAL)
    components = [(1.0, INITIAL)]
    records = []
    componentwise_terms = 1
    for k, (p, lam, T) in enumerate(STAGES, start=1):
        true = killed_evolve(true, p, lam, T)
        components, bins, exit_abs = compile_stage(
            components, p, lam, T, small, ratio, large
        )
        componentwise_terms *= 1 + len(TARGETS) * bins
        compiled = mixture_vector(components)
        records.append({
            "stage": k,
            "age_bins": bins,
            "terms": len(components),
            "componentwise_terms_if_not_aggregated": componentwise_terms,
            "coefficient_l1": round(sum(abs(c) for c, _ in components), 12),
            "marked_bin_weight_l1": round(exit_abs, 12),
            "survival_mass": round(sum(true), 12),
            "state_l1_error": round(sum(abs(a - b) for a, b in zip(compiled, true)), 12),
            "state_l1_norm": round(sum(abs(x) for x in compiled), 12),
        })
    return records


if __name__ == "__main__":
    print(json.dumps({
        "coarse": run(small=0.04, ratio=1.5, large=2.0),
        "fine": run(small=0.01, ratio=1.2, large=2.0),
    }, indent=2))
