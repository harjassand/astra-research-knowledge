"""Independent dense checks of mismatch transfer and driven hypercontractivity.

This checks direct killed-generator solutions against derived bounds. It is
not a proof, an observed physical dataset, or an asymptotic complexity test.
Run with python research_work/passive/computation/verify_mismatch.py.
"""
from pathlib import Path
import json
import math
import numpy as np
from scipy.linalg import expm, null_space

OUT = Path(__file__).resolve().parent
rng = np.random.default_rng(734198)


def reference(n, variant):
    size = 2 ** n
    q = np.zeros((size, size))
    alpha = rng.uniform(0.5, 1.0, n - 1)
    for x in range(size):
        for i in range(n):
            q[x, x ^ (1 << i)] += 0.5
        for i in range(n - 1):
            code = (x >> i) & 3
            forward = ((i + variant) % 2 == 0)
            newcode = ([1, 3, 2, 0] if forward else [3, 0, 2, 1])[code]
            if newcode != code:
                q[x, x ^ ((code ^ newcode) << i)] += alpha[i]
    q -= np.diag(q.sum(axis=1))
    assert np.max(np.abs(q.sum(axis=0))) < 1e-12
    return q


def mismatch(q0, n, eta, variant):
    """Local contexts modulate aggregated observed rates; not balanced flows."""
    q = np.zeros_like(q0)
    for x in range(len(q0)):
        for y in range(len(q0)):
            if x == y or q0[x, y] == 0:
                continue
            mask = x ^ y
            i = (mask & -mask).bit_length() - 1
            lo, hi = max(0, i - 1), min(n, i + (3 if mask.bit_count() == 2 else 2))
            parity = sum((x >> j) & 1 for j in range(lo, hi))
            sign = 1 if (parity + i + variant) % 2 == 0 else -1
            q[x, y] = q0[x, y] * (1 + eta * sign)
    q -= np.diag(q.sum(axis=1))
    return q


def stationary(q):
    a = q.T.copy()
    rhs = np.zeros(len(q))
    a[-1, :] = 1
    rhs[-1] = 1
    pi = np.linalg.solve(a, rhs)
    assert pi.min() > 0
    assert np.max(np.abs(pi @ q)) < 1e-12
    return pi


def mean(q, pi, mask):
    bidx = np.array([x for x in range(len(q)) if not ((mask >> x) & 1)])
    killed = -q[np.ix_(bidx, bidx)]
    t = np.linalg.solve(killed, np.ones(len(bidx)))
    return pi[bidx] @ t / pi[bidx].sum()


def invsqrt(a):
    lam, vec = np.linalg.eigh(a)
    assert lam.min() > 0
    return (vec * lam ** (-0.5)) @ vec.T


records = []
target_checks = 0
sharpened_checks = 0
max_hyper_2_inf = 0.0
max_hyper_1_2 = 0.0
max_form_fraction = 0.0
for n in range(2, 7):
    for variant in range(3):
        q0 = reference(n, variant)
        size = len(q0)
        pi0 = np.full(size, 1 / size)
        eta, beta = 0.001, 0.002
        q = mismatch(q0, n, eta, variant)
        pi = stationary(q)
        cap = float((-np.diag(q0)).max())
        g, c = 1.0, 0.5

        # Endpoint hypercontractive estimates and signed relative kernel.
        t0 = math.log(n - 1) / (4 * c)
        p_at_t0 = expm(t0 * q0)
        norm_2_inf = math.sqrt(size * np.max(np.sum(p_at_t0 ** 2, axis=1)))
        norm_1_2 = math.sqrt(size * np.max(np.sum(p_at_t0 ** 2, axis=0)))
        assert norm_2_inf <= 2 + 1e-11
        assert norm_1_2 <= 2 + 1e-11
        max_hyper_2_inf = max(max_hyper_2_inf, norm_2_inf)
        max_hyper_1_2 = max(max_hyper_1_2, norm_1_2)
        r_beta = math.log(4 * (n - 1) / beta) / (2 * c)
        rel_kernel_error = np.max(np.abs(size * expm(r_beta * q0) - 1))
        assert rel_kernel_error <= beta + 1e-11

        u = 2 * eta * cap * r_beta / (1 - eta) - math.log(1 - beta)
        v = u - math.log(1 - eta)
        log_f = 2 * math.asinh(math.sqrt(2 * cap / g) * math.sinh(v / 2))
        stationary_log_error = float(np.max(np.abs(np.log(pi / pi0))))
        assert stationary_log_error <= u + 1e-12
        d0, d = -pi0[:, None] * q0, -pi[:, None] * q

        # Check mixed-energy operator norm against the stronger exact-flow v.
        edges = (q0 > 0)
        v_exact = float(np.max(np.abs(np.log((-d[edges]) / (-d0[edges])))))
        basis = null_space(np.ones((1, size)))
        e0 = basis.T @ ((d0 + d0.T) / 2) @ basis
        e1 = basis.T @ ((d + d.T) / 2) @ basis
        delta = basis.T @ (d - d0) @ basis
        op = invsqrt(e0) @ delta @ invsqrt(e1)
        opnorm = float(np.linalg.norm(op, 2))
        kappa_exact = 2 * math.sqrt(2 * cap / g) * math.sinh(v_exact / 2)
        assert opnorm <= kappa_exact + 1e-11
        max_form_fraction = max(max_form_fraction, opnorm / kappa_exact)

        # True gap is computed under its actual, generally nonuniform law.
        s = -(np.sqrt(pi)[:, None] * q / np.sqrt(pi)[None, :])
        gap_actual = float(np.linalg.eigvalsh((s + s.T) / 2)[1])
        gap_lower = (1 - eta) * math.exp(-2 * u) * g
        assert gap_actual >= gap_lower - 1e-11

        # Explicit target sweep for small systems; random masks above that.
        if n <= 3:
            targets = range(1, 2 ** size - 1)
        elif n <= 4:
            targets = set(int(z) for z in rng.integers(1, 2 ** size - 1, 80))
        else:
            # Singleton, coordinate half-space and several specified cylinders.
            targets = [1, 1 << (size - 1)]
            for k in range(1, n):
                targets.append(sum(1 << x for x in range(size) if x & (2 ** k - 1) == 0))
        worst_log_ratio = 0.0
        for target in targets:
            m0, m = mean(q0, pi0, target), mean(q, pi, target)
            lr = math.log(m / m0)
            worst_log_ratio = max(worst_log_ratio, abs(lr))
            assert abs(lr) <= 3 * u + log_f + 1e-10
            p0 = target.bit_count() / size
            if math.exp(u) * p0 < 1:
                b0 = 1 - p0
                b_min = 1 - math.exp(u) * p0
                b_max = 1 - math.exp(-u) * p0
                lower = -2 * u + math.log(b0 / b_max) - log_f
                upper = 2 * u + math.log(b0 / b_min) + log_f
                assert lower - 1e-10 <= lr <= upper + 1e-10
                sharpened_checks += 1
            target_checks += 1
        records.append({
            'n': n, 'variant': variant, 'eta': eta, 'beta': beta,
            'reference_exit_cap': cap,
            'stationary_log_error': stationary_log_error,
            'stationary_log_bound': u,
            'relative_kernel_error': float(rel_kernel_error),
            'actual_gap': gap_actual, 'actual_gap_lower_bound': gap_lower,
            'worst_target_log_mean_ratio': worst_log_ratio,
            'uniform_log_mean_bound': 3 * u + log_f,
            'exact_flow_mixed_norm': opnorm,
            'exact_flow_mixed_norm_bound': kappa_exact,
        })

result = {
    'seed': 734198, 'models': len(records), 'target_checks': target_checks,
    'rare_sharpened_checks': sharpened_checks,
    'max_endpoint_2_inf_norm': max_hyper_2_inf,
    'max_endpoint_1_2_norm': max_hyper_1_2,
    'max_mixed_form_fraction_of_bound': max_form_fraction,
    'all_assertions_passed': True,
    'scope': 'Dense floating-point verification, not a proof or physical dataset.',
    'records': records,
}
(OUT / 'mismatch_checks.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({k: v for k, v in result.items() if k != 'records'}))
