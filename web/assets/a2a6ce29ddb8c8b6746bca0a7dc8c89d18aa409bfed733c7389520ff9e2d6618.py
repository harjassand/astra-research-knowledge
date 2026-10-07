"""Finite diagnostics for the analytic scout proof; not theorem validation."""
import json
import math


def bin_prob(n, k, q):
    if q == 0:
        return float(k == 0)
    return math.exp(
        math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)
        + k * math.log(q) + (n - k) * math.log1p(-q)
    )


def schur_prob(n, k, lam):
    if lam == 0:
        return float(k == 0)
    q, p = lam / n, 1 - lam / n
    r = q / p
    t = n - 2 * k
    mult = math.comb(n, k) - (math.comb(n, k - 1) if k else 0)
    return math.exp(math.log(mult) + (n - k) * math.log(p) + k * math.log(q)) * (
        (1 - r ** (t + 1)) / (1 - r)
    )


def pure_spin_distance(n, k, a):
    t = n - 2 * k
    if a == 0:
        return 0.0
    local_prob = a / (n + a)
    inner = sum(
        math.sqrt(bin_prob(t, ell, local_prob))
        * math.exp((-a + ell * math.log(a) - math.lgamma(ell + 1)) / 2)
        for ell in range(t + 1)
    )
    return math.sqrt(max(0.0, 1 - inner * inner))


coupling_max = 0.0
normalizer_max = 0.0
spin_rows = []
for n in [8, 16, 32, 64, 128]:
    for lam in [0.0, 0.25, 1.0, 2.0]:
        if n < 4 * lam:
            continue
        p, q = 1 - lam / n, lam / n
        r = q / p
        weights = [schur_prob(n, k, lam) for k in range(n // 2 + 1)]
        normalizer_max = max(normalizer_max, abs(sum(weights) - 1))
        occupation = [0.0] * (n + 1)
        for k, wk in enumerate(weights):
            t = n - 2 * k
            for ell in range(t + 1):
                conditional = (1 - r) * r ** ell / (1 - r ** (t + 1))
                occupation[k + ell] += wk * conditional
        residual = sum(abs(occupation[k] - bin_prob(n, k, q)) for k in range(n + 1))
        coupling_max = max(coupling_max, residual)
        tv = 0.5 * sum(
            abs((weights[k] if k < len(weights) else 0.0) - bin_prob(n, k, q))
            for k in range(n + 1)
        )
        assert tv <= r + 1e-11, (n, lam, tv, r)
        assert sum(k * wk for k, wk in enumerate(weights)) <= lam + 1e-11
    for k in [0, 1, 2]:
        if k <= n // 4:
            a = 1.0
            dist = pure_spin_distance(n, k, a)
            spin_rows.append({"n": n, "k": k, "distance": dist, "n_distance_over_1k": n * dist / (1 + k)})

assert coupling_max < 1e-10
assert normalizer_max < 1e-10
print(json.dumps({
    "scope": "finite algebraic diagnostics only",
    "schur_normalizer_max_abs_error": normalizer_max,
    "occupation_binomial_max_L1_error": coupling_max,
    "spin_coherent_distances": spin_rows,
}, indent=2))
