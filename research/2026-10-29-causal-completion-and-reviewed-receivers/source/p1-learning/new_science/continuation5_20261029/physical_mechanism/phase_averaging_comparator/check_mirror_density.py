"""Population checks of the ordinary phase-averaging comparisons.

The matrices describe exact model generators. Floating-point matrix results
are numerical checks, not rigorous interval certificates or apparatus data.
Independent-spin lower bounds use 70-digit Decimal scalar series.
"""
from pathlib import Path
from decimal import Decimal, localcontext
import json
import math
import numpy as np
from scipy.linalg import eigh, helmert, svdvals


def spectral(a):
    vals, vecs = eigh((a + a.T) / 2)
    assert vals.min() > -1e-11
    return np.maximum(vals, 0), vecs


def semigroup(spec, t):
    vals, vecs = spec
    return (vecs * np.exp(-t * vals)) @ vecs.T


def opnorm(a):
    return float(svdvals(a)[0])


def laplacian(n, rates):
    a = np.zeros((n, n))
    for i, rate in enumerate(rates):
        j = (i + 1) % n
        a[i, i] += rate / 2
        a[j, j] += rate / 2
        a[i, j] -= rate / 2
        a[j, i] -= rate / 2
    return a


def mirror_case(n, h, alpha=0.6):
    rng = np.random.default_rng(17017 + n)
    beta = rng.uniform(-alpha, alpha, n)
    basis = helmert(n, full=False).T
    a = basis.T @ laplacian(n, np.ones(n)) @ basis
    b = basis.T @ laplacian(n, beta) @ basis
    spec_a = spectral(a)
    specs = {sgn: spectral(a + sgn * b) for sgn in [-1, 1]}
    low, high = float(spec_a[0].min()), 2.0
    invsqrt = (spec_a[1] / np.sqrt(spec_a[0])) @ spec_a[1].T
    c = 1 + alpha
    x = 2 * h * c * high
    rem = math.expm1(x) - x - x * x / 2
    eps = rem / (h * high * (2 - math.exp(x)))
    assert x < math.log(2) and eps < 1
    cycle_bound = eps / (2 * math.sqrt(1 - eps))
    alltime_bound = cycle_bound + 2 * alpha**2 * high**2 * h**2
    perkey_bound = cycle_bound + 2 * alpha * high * h
    macro_specs = {}
    relative_errors = []
    for sgn in [-1, 1]:
        half = semigroup(specs[sgn], h / 2)
        tmat = half @ semigroup(specs[-sgn], h) @ half
        vals, vecs = eigh((tmat + tmat.T) / 2)
        assert vals.min() > 0 and vals.max() < 1 + 1e-11
        ah = (vecs * (-np.log(vals) / (2 * h))) @ vecs.T
        # The mean-zero sector excludes the exact common kernel.
        macro_specs[sgn] = spectral(ah)
        rel = invsqrt @ (ah - a) @ invsqrt
        rerr = opnorm(rel)
        assert rerr <= eps + 2e-9
        relative_errors.append(rerr)

    def partial(sgn, u):
        if u <= h / 2:
            return semigroup(specs[sgn], u)
        half = semigroup(specs[sgn], h / 2)
        if u <= 3 * h / 2:
            return semigroup(specs[-sgn], u - h / 2) @ half
        return semigroup(specs[sgn], u - 3 * h / 2) @ semigroup(specs[-sgn], h) @ half

    times = [h / 4, h, 2 * h, 1 + h / 4,
             n**2 * 0.01 + h / 4, n**2 * 0.1 + h / 4, n**2 + h / 4]
    rows = []
    for t in times:
        cycles = int(math.floor(t / (2 * h) + 1e-12))
        u = max(0.0, t - 2 * h * cycles)
        reference = semigroup(spec_a, t)
        us = [partial(sgn, u) @ semigroup(macro_specs[sgn], 2 * h * cycles)
              for sgn in [-1, 1]]
        avg = (us[0] + us[1]) / 2
        err = opnorm(avg - reference)
        individual = max(opnorm(z - reference) for z in us)
        assert err <= alltime_bound + 2e-9
        assert individual <= perkey_bound + 2e-9
        rows.append({"physical_time": t, "cycles": cycles, "within_cycle_time": u,
                     "phase_averaged_error": err, "exposed_orientation_max_error": individual})
    return {"sites": n, "h": h, "mean_gap": low, "mean_norm_upper": high,
            "alpha": alpha, "relative_log_error": max(relative_errors),
            "relative_log_bound": eps, "alltime_average_bound": alltime_bound,
            "cycle_bound": cycle_bound, "alltime_perkey_bound": perkey_bound,
            "largest_sampled_error": max(r["phase_averaged_error"] for r in rows),
            "sampled_times": rows,
            "maximum_global_pi_pulses": 2 * max(r["cycles"] for r in rows)}


def i0_decimal(x):
    term = Decimal(1)
    ans = term
    q = x * x / 4
    for k in range(1, 1000):
        term *= q / (k * k)
        ans += term
        if abs(term) < Decimal('1e-65'):
            return ans
    raise AssertionError("I0 series did not converge")


def manybody_floor():
    rows = []
    with localcontext() as ctx:
        ctx.prec = 70
        alpha = Decimal('0.6')
        pie = Decimal(str(math.pi))
        eminus = Decimal(-1).exp()
        mirror_limit = alpha * alpha * eminus / 8
        rotation_limit = alpha * alpha * eminus / pie
        for n in [16, 64, 256, 1024, 4096]:
            nd = Decimal(n)
            h = 2 / nd
            z = alpha / nd
            err = eminus * ((nd * i0_decimal(z).ln()).exp() - 1)
            omega = pie * nd
            zrot = 2 * alpha / omega
            errot = eminus * ((nd * i0_decimal(zrot).ln()).exp() - 1)
            rows.append({"spins": n, "h": float(h), "time": float(1 / nd),
                         "mirror_error": float(err), "mirror_error_over_h": float(err / h),
                         "rotation_omega": float(omega), "rotation_error": float(errot),
                         "rotation_error_times_omega": float(errot * omega)})
        common_bit_floor = eminus * ((alpha.exp() + (-alpha).exp()) / 2 - 1)
        assert abs(rows[-1]["mirror_error_over_h"] - float(mirror_limit)) < 1e-6
        assert abs(rows[-1]["rotation_error_times_omega"] - float(rotation_limit)) < 1e-6
        return {"iid_phase_mirror_limit_error_over_h": float(mirror_limit),
                "iid_phase_rotation_limit_error_times_omega": float(rotation_limit),
                "single_global_bit_constant_error": float(common_bit_floor), "rows": rows}


def telegraph_case():
    nvis, nsign = 4, 4
    # State order is sign block, then visible configuration.
    a = np.zeros((16, 16))
    gamma, alpha = 10.0, 0.6
    smax = 1.2
    for sign in range(nsign):
        for y in range(nvis):
            row = sign * nvis + y
            for i in range(2):
                outside = 1 if y & (1 << (1 - i)) else -1
                sigma = 1 if sign & (1 << i) else -1
                si = 1 + 0.2 * outside
                beta = alpha * (0.4 + 0.6 * outside)
                rate = si * (1 + beta * sigma) / 2
                col = sign * nvis + (y ^ (1 << i))
                a[row, row] += rate
                a[row, col] -= rate
                col = (sign ^ (1 << i)) * nvis + y
                a[row, row] += gamma
                a[row, col] -= gamma
    assert np.max(np.abs(a - a.T)) < 1e-14
    p = np.vstack([np.eye(4) / 2] * 4)
    av = p.T @ a @ p
    b = (np.eye(16) - p @ p.T) @ a @ p
    vals, vecs = eigh(av)
    pos = vals > 1e-10
    w = vecs[:, pos] / np.sqrt(vals[pos])
    actual_m = float(eigh(w.T @ b.T @ b @ w, eigvals_only=True).max())
    m = smax * alpha * alpha
    assert actual_m <= m + 1e-12
    r = m / (2 * gamma)
    bound = r / (2 * math.sqrt(1 - r))
    sp, sr = spectral(a), spectral(av)
    times = [0.0001, 0.001, 0.01, 0.1, 1, 10, 100]
    errors = [opnorm(p.T @ semigroup(sp, t) @ p - semigroup(sr, t)) for t in times]
    assert max(errors) < bound + 1e-12
    # Fixed initial orientation: exact one-spin character response, no P initial state.
    small_alpha, gam, t = 0.1, 10.0, 0.1
    d = math.sqrt(gam * gam + small_alpha * small_alpha)
    retained_key_response = math.exp(-(1 + gam) * t) * (
        math.cosh(d * t) + (gam - small_alpha) / d * math.sinh(d * t))
    key_error = abs(retained_key_response - math.exp(-t))
    rr = small_alpha**2 / (2 * gam)
    wrong_bound = rr / (2 * math.sqrt(1 - rr))
    assert key_error > wrong_bound
    return {"sites": 2, "gamma": gamma, "actual_relative_variance": actual_m,
            "variance_upper": m, "bound": bound, "times": times, "errors": errors,
            "retained_initial_key_counterexample": {"alpha": small_alpha, "gamma": gam,
                "time": t, "conditional_error": key_error, "inapplicable_P_bound": wrong_bound}}


def main():
    cases = [mirror_case(16, 0.01), mirror_case(64, 0.02), mirror_case(64, 0.01),
             mirror_case(64, 0.005), mirror_case(128, 0.01)]
    results = {"status": "PASS", "scope": "population numerical checks, not interval certificates or physical runs",
               "density_mirror_cases": cases, "manybody_short_time_floor": manybody_floor(),
               "telegraph_supplier": telegraph_case()}
    out = Path(__file__).with_name("PHASE_COMPARATOR_CHECKS.json")
    out.write_text(json.dumps(results, indent=2) + '\n')
    print(json.dumps({"status": "PASS", "density_cases": len(cases),
                      "largest_density_error": max(x['largest_sampled_error'] for x in cases),
                      "smallest_visible_gap": min(x['mean_gap'] for x in cases),
                      "output": str(out)}, indent=2))


if __name__ == '__main__':
    main()
