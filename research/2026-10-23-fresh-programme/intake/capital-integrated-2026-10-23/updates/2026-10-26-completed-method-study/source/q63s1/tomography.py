#!/usr/local/bin/python3
"""Single-port shunt tomography and an independent constrained-fit comparator.

All data in this file are synthetic. The inverse routine receives only the
declared scalar measurements. No true matrix enters reconstruction or fit
selection. See PROOF.md for the exact measurement model and hypotheses.
"""
from __future__ import annotations

import csv
import json
import math
import time
from fractions import Fraction as F
from pathlib import Path

import numpy as np
from scipy.optimize import least_squares

HERE = Path(__file__).resolve().parent


def design(n: int, t: float = 1.0):
    """Port is node 0. Ordered baseline, singles t/2t, then pairs t/t."""
    ds = [np.zeros(n)]
    labels = ["baseline"]
    for i in range(1, n):
        for mult in (1, 2):
            v = np.zeros(n)
            v[i] = mult * t
            ds.append(v)
            labels.append(f"single_{i}_{mult}")
    for i in range(1, n):
        for j in range(i + 1, n):
            v = np.zeros(n)
            v[i] = v[j] = t
            ds.append(v)
            labels.append(f"pair_{i}_{j}")
    assert len(ds) == n * (n + 1) // 2
    return np.asarray(ds), labels


def response(k, ds):
    mats = k[None, :, :] + np.array([np.diag(d) for d in ds])
    rhs = np.zeros((len(ds), len(k)))
    rhs[:, 0] = 1.0
    return np.linalg.solve(mats, rhs)[:, 0]


def reconstruct(y, n, t=1.0):
    """Exact-data formula, with explicit failure on inconsistent noisy data.

    A quadratic small root is evaluated through a cancellation-resistant
    expression where possible. No projection onto physical matrices is hidden.
    """
    r = np.zeros((n, n))
    r[0, 0] = y[0]
    if r[0, 0] <= 0:
        raise ValueError("nonpositive baseline")
    cursor = 1
    for i in range(1, n):
        l1, l2 = y[0] - y[cursor], y[0] - y[cursor + 1]
        cursor += 2
        if not (0 < l1 < l2 < 2 * l1):
            raise ValueError("single-load losses inconsistent with exact model")
        ratio = l2 / l1
        p = (2 - ratio) / (2 * t * (ratio - 1))
        a2 = l1 * (1 + t * p) / t
        r[i, i] = p
        r[0, i] = r[i, 0] = math.sqrt(a2)
    for i in range(1, n):
        for j in range(i + 1, n):
            a, c = r[0, i], r[0, j]
            p, q = r[i, i], r[j, j]
            loss = y[0] - y[cursor]
            cursor += 1
            A, B = 1 + t * p, 1 + t * q
            const = (a*a*B + c*c*A) / t - loss * A * B / (t*t)
            discr = (a*c)**2 - loss * const
            if not (loss > 0 and discr >= 0):
                raise ValueError("pair loss has no real admissible root")
            root = const / (a*c + math.sqrt(discr))
            upper = min(a*q/c, c*p/a)
            # Tolerance only handles roundoff near an exact boundary; it is not
            # a noisy-data projection or a route to assert physical feasibility.
            if root < -1e-10 or root > upper + 1e-9:
                raise ValueError("pair root violates inverse-M inequality")
            r[i, j] = r[j, i] = root
    if np.linalg.eigvalsh(r)[0] <= 0:
        raise ValueError("recovered inverse is not positive definite")
    return np.linalg.inv(r)


def edge_list(n):
    return [(i, j) for i in range(n) for j in range(i + 1, n)]


def matrix_from_parameters(theta, n):
    """All edge conductances and all leaks are independently nonnegative."""
    k = np.diag(np.asarray(theta[:n]).copy())
    for w, (i, j) in zip(theta[n:], edge_list(n)):
        k[i, i] += w
        k[j, j] += w
        k[i, j] -= w
        k[j, i] -= w
    return k


def parameters_from_matrix(k):
    n = len(k)
    return np.r_[k.sum(axis=1), [-k[i, j] for i, j in edge_list(n)]]


def ordinary_fit(y, ds, n, seed=0, starts=8):
    """Ordinary multistart physical nonlinear least squares, analytic Jacobian.

    Every start uses the same observations and no true topology. Selection uses
    training residual only. The full complete graph is permitted, including
    sparse boundary solutions. This code does not call reconstruct().
    """
    rng = np.random.default_rng(seed)
    d = n * (n + 1) // 2
    scale = abs(y[0])
    diag_ds = np.array([np.diag(v) for v in ds])
    rhs = np.zeros((len(ds), n))
    rhs[:, 0] = 1
    edges = edge_list(n)

    class Eval:
        last = None
        value = None
        jacobian = None

        def evaluate(self, theta):
            if self.last is not None and np.array_equal(theta, self.last):
                return
            k = matrix_from_parameters(theta, n)
            v = np.linalg.solve(k[None, :, :] + diag_ds, rhs)
            self.value = (v[:, 0] - y) / scale
            self.jacobian = np.empty((len(ds), d))
            self.jacobian[:, :n] = -v * v / scale
            for h, (i, j) in enumerate(edges, n):
                self.jacobian[:, h] = -(v[:, i] - v[:, j])**2 / scale
            self.last = theta.copy()

        def fun(self, theta):
            self.evaluate(theta)
            return self.value

        def jac(self, theta):
            self.evaluate(theta)
            return self.jacobian

    best = None
    total_evaluations = 0
    begin = time.perf_counter()
    for _ in range(starts):
        ev = Eval()
        initial = np.exp(rng.uniform(-1.0, 1.0, d))
        fit = least_squares(ev.fun, initial, jac=ev.jac, bounds=(1e-12, np.inf),
                            x_scale="jac", max_nfev=3000,
                            ftol=1e-13, xtol=1e-13, gtol=1e-13)
        total_evaluations += fit.nfev
        objective = float(np.dot(fit.fun, fit.fun))
        if best is None or objective < best[0]:
            best = (objective, fit.x.copy(), fit.optimality, fit.status)
    return matrix_from_parameters(best[1], n), {
        "scaled_train_sse": best[0], "starts": starts,
        "total_nfev": total_evaluations,
        "seconds": time.perf_counter() - begin,
        "selected_status": int(best[3]),
    }


def random_network(n, rng, kind="dense"):
    theta = np.r_[rng.uniform(.5, 1.5, n), np.zeros(n*(n-1)//2)]
    for h, (i, j) in enumerate(edge_list(n), n):
        allowed = (kind == "dense" or (kind == "path" and j == i+1)
                   or (kind == "star" and i == 0)
                   or (kind == "sparse" and (j == i+1 or rng.random() < .25)))
        if allowed:
            theta[h] = rng.uniform(.5, 2.0)
    return matrix_from_parameters(theta, n)


def fraction_inverse(a):
    n = len(a)
    m = [list(row) + [F(i == j) for j in range(n)] for i, row in enumerate(a)]
    for j in range(n):
        if not m[j][j]:
            h = next(h for h in range(j+1, n) if m[h][j])
            m[j], m[h] = m[h], m[j]
        pivot = m[j][j]
        m[j] = [x/pivot for x in m[j]]
        for i in range(n):
            if i != j:
                v = m[i][j]
                m[i] = [x-v*z for x, z in zip(m[i], m[j])]
    return [row[n:] for row in m]


def rational_sqrt(x):
    p, q = math.isqrt(x.numerator), math.isqrt(x.denominator)
    assert p*p == x.numerator and q*q == x.denominator
    return F(p, q)


def exact_reconstruct(y, n, t=F(1)):
    r = [[F(0) for _ in range(n)] for _ in range(n)]
    r[0][0] = y[0]
    cursor = 1
    for i in range(1, n):
        l1, l2 = y[0]-y[cursor], y[0]-y[cursor+1]
        cursor += 2
        ratio = l2/l1
        p = (2-ratio)/(2*t*(ratio-1))
        r[i][i] = p
        r[0][i] = r[i][0] = rational_sqrt(l1*(1+t*p)/t)
    for i in range(1, n):
        for j in range(i+1, n):
            a, c, p, q = r[0][i], r[0][j], r[i][i], r[j][j]
            loss = y[0]-y[cursor]
            cursor += 1
            A, B = 1+t*p, 1+t*q
            const = (a*a*B+c*c*A)/t-loss*A*B/(t*t)
            disc = a*a*c*c-loss*const
            x = (a*c-rational_sqrt(disc))/loss
            assert 0 < x <= min(a*q/c, c*p/a)
            r[i][j] = r[j][i] = x
    return fraction_inverse(r)


def exact_checks():
    rng = np.random.default_rng(763)
    rows = []
    for n in range(2, 8):
        for kind in ("dense", "path", "star", "sparse"):
            k = random_network(n, rng, kind)
            # Integer weights/leaks, without rounding matrix diagonals
            # independently (which could break the physical parameterization).
            theta = np.ceil(parameters_from_matrix(k) * 2).astype(int)
            k = matrix_from_parameters(theta, n).astype(int)
            a = [[F(int(v)) for v in row] for row in k]
            ds, _ = design(n)
            y = []
            for load in ds:
                loaded = [[a[i][j] + (F(int(load[i])) if i == j else 0)
                           for j in range(n)] for i in range(n)]
                y.append(fraction_inverse(loaded)[0][0])
            rebuilt = exact_reconstruct(y, n)
            assert rebuilt == a
            rows.append({"n": n, "kind": kind, "measurements": len(y),
                         "exact_fraction_equality": True})
    return rows


def float_checks():
    rng = np.random.default_rng(764)
    rows = []
    for n in range(2, 13):
        for kind in ("dense", "path", "star", "sparse"):
            k = random_network(n, rng, kind)
            ds, _ = design(n)
            y = response(k, ds)
            try:
                kh = reconstruct(y, n)
                error = float(np.linalg.norm(kh-k)/np.linalg.norm(k))
                residual = float(np.linalg.norm(response(kh, ds)-y)/np.linalg.norm(y))
                failure = ""
            except (ValueError, np.linalg.LinAlgError) as exc:
                error, residual, failure = None, None, str(exc)
            rows.append({"n": n, "kind": kind, "relative_matrix_error": error,
                         "relative_train_residual": residual, "failure": failure})
    return rows


def comparison():
    rng = np.random.default_rng(765)
    rows, raw = [], []
    for fixture, (n, kind) in enumerate(((4,"dense"), (5,"dense"),
                                       (5,"path"), (5,"star"))):
        k = random_network(n, rng, kind)
        ds, labels = design(n)
        noiseless = response(k, ds)
        heldout_ds = rng.uniform(0, 3, (32, n))
        heldout_true = response(k, heldout_ds)
        for noise_rel in (0, 1e-7, 1e-4):
            sigma = noise_rel * noiseless[0]
            observed = noiseless + rng.normal(0, sigma, len(noiseless))
            started = time.perf_counter()
            try:
                direct = reconstruct(observed, n)
                direct_time = time.perf_counter()-started
                direct_err = float(np.linalg.norm(direct-k)/np.linalg.norm(k))
                direct_pred = response(direct, heldout_ds)
                direct_rmse = float(np.linalg.norm(direct_pred-heldout_true)
                                    /np.linalg.norm(heldout_true))
                direct_min_eig = float(np.linalg.eigvalsh(direct)[0])
                direct_max_offdiag = float(np.max(direct-np.diag(np.diag(direct))))
                direct_min_leak = float(np.min(direct.sum(axis=1)))
                failure = ""
            except (ValueError, np.linalg.LinAlgError) as exc:
                direct_time = time.perf_counter()-started
                direct_err = direct_rmse = direct_min_eig = None
                direct_max_offdiag = direct_min_leak = None
                direct = None
                failure = str(exc)
            fitted, info = ordinary_fit(observed, ds, n, 1765+fixture, starts=8)
            fitted_pred = response(fitted, heldout_ds)
            rows.append({"fixture":fixture, "n":n, "kind":kind,
                         "noise_sigma_relative_to_baseline":noise_rel,
                         "scalar_measurements_per_method":len(observed),
                         "direct_matrix_relative_error":direct_err,
                         "ordinary_matrix_relative_error":float(np.linalg.norm(fitted-k)
                                                                  /np.linalg.norm(k)),
                         "direct_heldout_relative_rmse":direct_rmse,
                         "ordinary_heldout_relative_rmse":float(np.linalg.norm(fitted_pred-heldout_true)
                                                                /np.linalg.norm(heldout_true)),
                         "direct_seconds":direct_time, "direct_failure":failure,
                         "direct_min_eig":direct_min_eig,
                         "direct_max_offdiag":direct_max_offdiag,
                         "direct_min_leak":direct_min_leak, **info})
            raw.append({"fixture":fixture,"kind":kind,"n":n,"noise_rel":noise_rel,
                        "true_k":k.tolist(),"load_labels":labels,"loads":ds.tolist(),
                        "observations":observed.tolist(),"noise_free":noiseless.tolist(),
                        "direct_k":None if direct is None else direct.tolist(),
                        "ordinary_k":fitted.tolist(),"heldout_loads":heldout_ds.tolist(),
                        "heldout_true":heldout_true.tolist()})
    return rows, raw


def depth_barrier():
    """Exact rational signal, avoiding subtracting two nearly equal floats."""
    rows = []
    for depth in (1, 2, 4, 6, 8, 10, 12, 16, 20, 30):
        n = depth+1
        k = [[F(int(i == j)) for j in range(n)] for i in range(n)]
        for i in range(n-1):
            k[i][i] += 1
            k[i+1][i+1] += 1
            k[i][i+1] = k[i+1][i] = F(-1)
        r = fraction_inverse(k)
        delta_f = r[0][-1]**2/(1+r[-1][-1])
        bound = F(2,3)**(2*depth)
        assert delta_f <= bound
        sigma = 1e-6
        # Necessary budget for error <= 1/4 from KL + Pinsker using either
        # the general uniform bound or the largest exact unperturbed signal.
        rows.append({"depth":depth,"n":n,"exact_signal_numerator":delta_f.numerator,
                     "exact_signal_denominator":delta_f.denominator,
                     "baseline_deep_leak_signal":float(delta_f),
                     "uniform_signal_upper_bound":float(bound),
                     "necessary_unit_current_budget_from_uniform_bound_sigma_1e-6":sigma**2/float(bound)**2,
                     "baseline_pair_kl_half_budget_sigma_1e-6":sigma**2/float(delta_f)**2})
    # Uniform-load bound is independent of where the estimator tries to act.
    rng = np.random.default_rng(766)
    worst_ratio = 0
    checks = 0
    for depth in (2,4,6,8,10):
        n = depth+1
        k = np.eye(n)
        for i in range(n-1):
            k[i,i] += 1; k[i+1,i+1] += 1
            k[i,i+1] = k[i+1,i] = -1
        r0 = np.linalg.inv(k)
        for _ in range(100):
            load = rng.exponential(3, n)
            r = np.linalg.inv(k+np.diag(load))
            # Numerator and denominator are the exact rank-one resolvent law;
            # this is a separate validation of inverse monotonicity.
            diff = r[0,-1]**2/(1+r[-1,-1])
            max_signal_bound = r0[0,-1]**2
            assert diff <= max_signal_bound*(1+1e-12)
            worst_ratio = max(worst_ratio, float(diff/max_signal_bound))
            checks += 1
    return rows, {"random_load_checks":checks,"largest_ratio_to_unloaded_squared_green_bound":worst_ratio}


def write_csv(name, rows):
    with (HERE/name).open("w", newline="") as out:
        writer = csv.DictWriter(out, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main():
    started = time.perf_counter()
    exact = exact_checks()
    floats = float_checks()
    comparisons, raw = comparison()
    depths, bound_checks = depth_barrier()
    write_csv("exact_checks.csv", exact)
    write_csv("float_checks.csv", floats)
    write_csv("comparison.csv", comparisons)
    write_csv("depth_barrier.csv", depths)
    (HERE/"comparison_data.json").write_text(json.dumps(raw, indent=2)+"\n")
    summary = {"exact_fraction_checks":len(exact),
               "exact_fraction_checks_passed":sum(r["exact_fraction_equality"] for r in exact),
               "float_checks":len(floats),
               "float_failures":[r for r in floats if r["failure"]],
               "worst_finite_float_matrix_error":max(r["relative_matrix_error"] for r in floats
                                                      if r["relative_matrix_error"] is not None),
               "comparison_cases":len(comparisons),"bound_checks":bound_checks,
               "elapsed_seconds":time.perf_counter()-started,
               "numpy":np.__version__}
    (HERE/"run_summary.json").write_text(json.dumps(summary, indent=2)+"\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
