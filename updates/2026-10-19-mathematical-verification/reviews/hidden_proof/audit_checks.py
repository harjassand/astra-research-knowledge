"""Independent float sanity checks, not proof certificates or original-source execution."""
from __future__ import annotations

import hashlib
import json
import math
from decimal import Decimal, getcontext
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
SOURCE = HERE.parents[1] / "sources/pro/hidden_state/proof.tex"
RNG = np.random.default_rng(20261019)


def op(a):
    return float(np.linalg.norm(a, 2))


def psd_power(a, alpha):
    w, u = np.linalg.eigh((a + a.T) / 2)
    assert min(w) > 0
    return (u * w**alpha) @ u.T


def matrix_exp(a):
    """Small dense real matrices; convergent Taylor series with scaling/squaring."""
    size = float(np.linalg.norm(a, 1))
    scale = max(0, int(math.ceil(math.log2(size / 0.5)))) if size else 0
    b = a / 2**scale
    out = np.eye(len(a))
    term = out.copy()
    for k in range(1, 100):
        term = term @ b / k
        out += term
        if np.linalg.norm(term, 1) < 2e-17 * np.linalg.norm(out, 1):
            break
    else:
        raise AssertionError("Taylor series did not converge")
    for _ in range(scale):
        out = out @ out
    return out


def observation(mu, labels):
    count = max(labels) + 1
    p = np.bincount(labels, weights=mu, minlength=count)
    v = np.zeros((len(mu), count))
    v[np.arange(len(mu)), labels] = np.sqrt(mu / p[labels])
    assert op(v.T @ v - np.eye(count)) < 1e-13
    return p, v


def h1_checks():
    worst_gap_ratio = 0.0
    worst_entry_ratio = 0.0
    least_gap_eigenvalue = 0.0
    least_delta_eigenvalue = 0.0
    count = 0
    for n in range(3, 13):
        for _ in range(8):
            mu = np.exp(RNG.normal(0, 1.2, n))
            mu /= sum(mu)
            raw = np.exp(RNG.normal(0, 1.0, (n, n)))
            flux = (raw + raw.T) / 2
            np.fill_diagonal(flux, 0)
            h = flux / np.sqrt(mu[:, None] * mu[None, :])
            np.fill_diagonal(h, -flux.sum(axis=1) / mu)
            evals, evecs = np.linalg.eigh(h)
            h /= abs(min(evals))
            evals /= abs(min(evals))
            tau = 10 ** RNG.uniform(-2, 1)
            tmat = (evecs * np.exp(tau * evals)) @ evecs.T
            nobs = int(RNG.integers(2, min(5, n - 1) + 1))
            labels = np.arange(n) % nobs
            RNG.shuffle(labels)
            _, v = observation(mu, labels)
            s = v.T @ tmat @ v
            u = v.T @ tmat @ tmat @ v
            delta = u - s @ s
            a0 = min(np.linalg.eigvalsh(s))
            dnorm = op(delta)
            least_delta_eigenvalue = min(least_delta_eigenvalue, min(np.linalg.eigvalsh(delta)))
            for alpha in [1 / 64, 0.1, 0.5, 0.9]:
                tp = (evecs * np.exp(tau * alpha * evals)) @ evecs.T
                sp = psd_power(s, alpha)
                gap = sp - v.T @ tp @ v
                bound = (1 - alpha) * a0 ** (alpha - 2) * dnorm
                ratio = op(gap) / bound if bound else 0
                least_gap_eigenvalue = min(least_gap_eigenvalue, min(np.linalg.eigvalsh(gap)))
                offdiag = sp.copy()
                np.fill_diagonal(offdiag, 0)
                m = max(0.0, -float(offdiag.min()))
                worst_gap_ratio = max(worst_gap_ratio, ratio)
                worst_entry_ratio = max(worst_entry_ratio, m / bound if bound else 0)
                assert min(np.linalg.eigvalsh(delta)) >= -5e-12
                assert min(np.linalg.eigvalsh(gap)) >= -5e-12
                assert op(gap) <= bound + 5e-12
                count += 1
    return dict(cases=count, hidden_dimension=[3, 12], observed_classes=[2, 5],
                worst_gap_to_bound_ratio=worst_gap_ratio,
                worst_negative_entry_to_bound_ratio=worst_entry_ratio,
                min_gap_eigenvalue=least_gap_eigenvalue,
                min_delta_eigenvalue=least_delta_eigenvalue)


def power_lipschitz_checks():
    worst_ratio = 0.0
    count = 0
    for n in range(2, 9):
        for _ in range(12):
            floor = 10 ** RNG.uniform(-4, -0.1)
            radius = floor * 10 ** RNG.uniform(-6, 1)
            raw1 = RNG.normal(size=(n, n))
            raw2 = RNG.normal(size=(n, n))
            x, y = raw1 @ raw1.T, raw2 @ raw2.T
            a = floor * np.eye(n) + radius * x / op(x)
            b = floor * np.eye(n) + radius * y / op(y)
            for alpha in [1 / 64, 0.1, 0.5, 0.9]:
                actual = op(psd_power(a, alpha) - psd_power(b, alpha))
                bound = alpha * floor ** (alpha - 1) * op(a - b)
                worst_ratio = max(worst_ratio, actual / bound)
                assert actual <= bound * (1 + 1e-7) + 2e-13
                count += 1
    return dict(cases=count, dimensions=[2, 8], worst_actual_to_bound_ratio=worst_ratio)


def negative_fractional_witness_checks():
    # A reversible four-state line, observing its two middle states as one class.
    # The observed one-lag kernel need not itself embed as a three-state CTMC.
    q = np.array([[-1, 1, 0, 0], [1, -2, 1, 0],
                  [0, 1, -2, 1], [0, 0, 1, -1]], dtype=float)
    mu = np.ones(4) / 4
    p, v = observation(mu, np.array([0, 1, 1, 2]))
    w, evecs = np.linalg.eigh(q)
    rows = []
    for tau in [0.001, 0.01, 0.1, 1, 5]:
        tmat = (evecs * np.exp(tau * w)) @ evecs.T
        s = v.T @ tmat @ v
        u = v.T @ tmat @ tmat @ v
        delta = u - s @ s
        a0 = min(np.linalg.eigvalsh(s))
        for alpha in [1 / 64, 0.1, 0.5, 0.9]:
            sp = psd_power(s, alpha)
            negative_entry = max(0.0, -float(sp[0, 2]))
            bound = (1 - alpha) * a0 ** (alpha - 2) * op(delta)
            assert negative_entry <= bound + 3e-13
            rows.append(dict(tau=tau, alpha=alpha, S_power_0_2=float(sp[0, 2]),
                             H1_bound=bound, negative_entry_to_bound_ratio=negative_entry / bound))
    return dict(hidden_dimension=4, observed_classes=3, stationary_observed_law=list(p),
                negative_entry_cases=sum(r["S_power_0_2"] < 0 for r in rows), cases=rows)


def ep(q, mu):
    out = 0.0
    for i in range(len(q)):
        for j in range(i + 1, len(q)):
            a, b = mu[i] * q[i, j], mu[j] * q[j, i]
            out += (a - b) * math.log(a / b)
    return out


def adjoint(q, mu):
    return q.T * mu[None, :] / mu[:, None]


def endpoint_checks():
    worst_ratio = 0.0
    worst_kernel_ratio = 0.0
    worst_escape_error = 0.0
    count = 0
    for n in range(3, 8):
        for strength in [1e-3, 1e-2, 0.1, 0.6]:
            mu = np.exp(RNG.normal(0, 1, n))
            mu /= sum(mu)
            raw = RNG.uniform(0.2, 1, size=(n, n))
            flux = (raw + raw.T) / 2
            np.fill_diagonal(flux, 0)
            current = strength * min(flux[0, 1], flux[1, 2], flux[2, 0])
            for i, j in [(0, 1), (1, 2), (2, 0)]:
                flux[i, j] += current
                flux[j, i] -= current
            q = flux / mu[:, None]
            np.fill_diagonal(q, -q.sum(axis=1))
            q /= max(-q.diagonal())
            qs = adjoint(q, mu)
            r = (q + qs) / 2
            exit_error = max(abs(qs.sum(axis=1)))
            worst_escape_error = max(worst_escape_error, float(exit_error))
            assert op(mu @ q) < 1e-13
            assert exit_error < 1e-13
            sigma = ep(q, mu)
            for t in [0.05, 0.5, 2]:
                p, pr = matrix_exp(t * q), matrix_exp(t * r)
                j = mu[:, None] * p
                jr = mu[:, None] * pr
                sym_j = (j + j.T) / 2
                tv = float(np.abs(sym_j - jr).sum() / 2)
                bound = -math.expm1(-t * sigma / 2)
                worst_ratio = max(worst_ratio, tv / bound)
                assert tv <= bound + 3e-14
                labels = np.arange(n) % min(n - 1, 3)
                po, v = observation(mu, labels)
                dmu = np.sqrt(mu)
                sq = dmu[:, None] * p / dmu[None, :]
                sr = dmu[:, None] * pr / dmu[None, :]
                observed_difference = v.T @ ((sq + sq.T) / 2 - sr) @ v
                kernel_bound = t * sigma / min(po)
                worst_kernel_ratio = max(worst_kernel_ratio, op(observed_difference) / kernel_bound)
                assert op(observed_difference) <= kernel_bound + 3e-13
                count += 1
    return dict(cases=count, dimensions=[3, 7],
                worst_endpoint_TV_to_affinity_bound_ratio=worst_ratio,
                worst_normalized_kernel_to_t_sigma_over_pmin_ratio=worst_kernel_ratio,
                max_adjoint_escape_rate_row_error=worst_escape_error)


def cycle_path_checks():
    rows = []
    t = 0.2
    kmax = 10
    for delta in [1e-3, 1e-2, 0.1, 0.6]:
        a, b = (1 + delta) / 2, (1 - delta) / 2
        q = np.array([[-1, a, b], [b, -1, a], [a, b, -1]], dtype=float)
        mu = np.ones(3) / 3
        qs, r = q.T, (q + q.T) / 2
        rate = 1.1
        p, ps, pr = np.eye(3) + q / rate, np.eye(3) + qs / rate, np.eye(3) + r / rate
        f, g, h = mu.copy(), mu.copy(), mu.copy()
        last = np.arange(3)
        pois = math.exp(-rate * t)
        tvmix = tvdirect = 0.0
        least_geometric_density_slack = 0.0
        for k in range(kmax + 1):
            tvmix += pois * np.abs((f + g) / 2 - h).sum() / 2
            tvdirect += pois * np.abs(f - h).sum() / 2
            least_geometric_density_slack = min(least_geometric_density_slack,
                float(np.min(h - np.sqrt(f * g))))
            if k == kmax:
                break
            f = (f[:, None] * p[last, :]).ravel()
            g = (g[:, None] * ps[last, :]).ravel()
            h = (h[:, None] * pr[last, :]).ravel()
            last = np.tile(np.arange(3), len(last))
            pois *= rate * t / (k + 1)
        next_pois = pois * rate * t / (kmax + 1)
        tail_upper = next_pois / (1 - rate * t / (kmax + 2))
        sigma = ep(q, mu)
        linear_bound = t * sigma / 2
        # Exact affinity on this balanced three-cycle: killed-generator row sum.
        affinity_bound = -math.expm1(t * (math.sqrt(1 - delta**2) - 1))
        exp_exact = np.ones((3, 3)) / 3
        theta = math.sqrt(3) * delta * t / 2
        exp_exact += math.exp(-1.5 * t) * math.cos(theta) * (np.eye(3) - np.ones((3, 3)) / 3)
        exp_sym = (matrix_exp(t * q) + matrix_exp(t * qs)) / 2
        assert op(exp_exact - exp_sym) < 1e-14
        assert tvmix + tail_upper <= affinity_bound + 3e-14
        assert affinity_bound <= linear_bound + 3e-14
        assert least_geometric_density_slack >= -3e-16
        rows.append(dict(delta=delta, sigma=sigma, path_TV_mixture_truncated=float(tvmix),
                         path_TV_direct_truncated=float(tvdirect),
                         omitted_TV_upper_bound=tail_upper,
                         affinity_defect=affinity_bound,
                         linear_entropy_bound=linear_bound,
                         min_density_geometric_slack=least_geometric_density_slack))
    return dict(dimensions=3, time=t, max_uniformization_events=kmax, cases=rows)


def constants():
    getcontext().prec = 90
    two = Decimal(2)
    alpha = Decimal(1) / 64
    a = two**(-18)
    b = a / 2
    m = (2 * two**(-Decimal(1) / 8) - 1 - two**(-Decimal(9) / 32)) / 4
    c = alpha * b**(alpha - 1) + 4 * (1 - alpha) * b**(alpha - 2)
    return dict(decimal_precision=90, alpha=str(alpha), a0=str(a), p_min="0.25", tau="1",
                m=str(m), C_alpha=str(c), H1_defect=str(m * a**(2 - alpha) / (1 - alpha)),
                H2_zeta=str(min(b, m / c)), H2_floor=str(min(b, m / c) / 4),
                scope="High precision evaluation, not an exact rational certificate")


if __name__ == "__main__":
    results = dict(source=str(SOURCE), source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
                   seed=20261019, numpy_version=np.__version__,
                   h1=h1_checks(), operator_lipschitz=power_lipschitz_checks(),
                   negative_fractional_witness=negative_fractional_witness_checks(),
                   endpoint_comparison=endpoint_checks(), symmetrized_path_comparison=cycle_path_checks(),
                   example_constants=constants(), status="ALL_SANITY_CHECKS_PASSED",
                   limitations="Finite floating-point checks do not prove the theorem or establish physical validation or priority.")
    (HERE / "numerical_checks.json").write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps(results, indent=2))
