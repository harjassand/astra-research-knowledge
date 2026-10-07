"""Scoped numerical diagnostics for the postselection stability report.

No counting algorithm or quantum circuit is executed here. The analytic proofs
are in postselection_stability.txt. NumPy is used for bounded random fixtures;
mpmath is used for exponentially rare counterexamples without float underflow.
"""

import itertools
import json
import math

import mpmath as mp
import numpy as np


def psd_power(a, power):
    vals, vecs = np.linalg.eigh(a)
    return (vecs * vals**power) @ vecs.conj().T


def hilbert(a, b):
    w = psd_power(a, -0.5)
    vals = np.linalg.eigvalsh(w @ b @ w)
    return float(np.log(vals[-1] / vals[0]))


def normalized(a):
    return a / np.trace(a)


def trace_distance(a, b):
    return float(np.abs(np.linalg.eigvalsh(normalized(a) - normalized(b))).sum() / 2)


def random_pd(rng, m):
    x = rng.normal(size=(m, m)) + 1j * rng.normal(size=(m, m))
    return x @ x.conj().T + np.eye(m)


def exterior(a, k):
    sets = list(itertools.combinations(range(a.shape[0]), k))
    if k == 0:
        return np.ones((1, 1), dtype=complex)
    return np.array([[np.linalg.det(a[np.ix_(s, t)]) for t in sets] for s in sets])


def run():
    rng = np.random.default_rng(731952)
    random_filter_cases = 0
    maximum_bound_violation = -math.inf
    maximum_hilbert_expansion = -math.inf
    maximum_ext_identity_error = 0.0
    maximum_sharp_filter_error = 0.0
    for _ in range(80):
        m = 5
        a = random_pd(rng, m)
        b = random_pd(rng, m)
        hin = hilbert(a, b)
        kraus = [rng.normal(size=(3, m)) + 1j * rng.normal(size=(3, m)) for _ in range(3)]
        # A common scale could make this trace nonincreasing. Normalized outputs
        # and Hilbert distances are unaffected by that common scale.
        fa = sum(k @ a @ k.conj().T for k in kraus)
        fb = sum(k @ b @ k.conj().T for k in kraus)
        hout = hilbert(fa, fb)
        maximum_bound_violation = max(maximum_bound_violation, trace_distance(fa, fb) - math.tanh(hin / 4))
        maximum_hilbert_expansion = max(maximum_hilbert_expansion, hout - hin)
        random_filter_cases += 1

        whitening = psd_power(a, -0.5)
        c = whitening @ b @ whitening
        vals, vecs = np.linalg.eigh(c)
        low, high = float(vals[0]), float(vals[-1])
        weights = np.array([math.sqrt(high), math.sqrt(low)]) / (math.sqrt(low) + math.sqrt(high))
        pick = np.vstack([vecs[:, 0].conj(), vecs[:, -1].conj()])
        sharp_k = np.diag(np.sqrt(weights)) @ pick @ whitening
        sa = sharp_k @ a @ sharp_k.conj().T
        sb = sharp_k @ b @ sharp_k.conj().T
        maximum_sharp_filter_error = max(maximum_sharp_filter_error, abs(trace_distance(sa, sb) - math.tanh(hin / 4)))

        logs = np.log(vals)
        for k in range(m + 1):
            direct = hilbert(exterior(a, k), exterior(b, k))
            formula = float(sum(logs[m-k:]) - sum(logs[:k])) if k else 0.0
            maximum_ext_identity_error = max(maximum_ext_identity_error, abs(direct - formula))

    mp.mp.dps = 180
    counterexample_rows = []
    for n in (1, 2, 4, 8, 16, 32, 64):
        gap = mp.mpf(4 * n)
        perturbation = mp.power(2, -n)
        s = gap / 2
        radius = mp.sqrt(s*s + perturbation*perturbation)
        radius_difference = perturbation*perturbation / (radius + s)
        one_minus_ratio = perturbation*perturbation / (radius*(radius+s))
        qrare = one_minus_ratio * mp.exp(radius_difference) / 2 + (1+s/radius) * mp.exp(-radius-s) / 2
        qref = mp.exp(-gap)
        posterior_t = (qrare-qref) / (2*(qrare+qref))
        denom = (1+mp.exp(radius_difference))*(1+mp.exp(-radius-s))*(1+qref)
        success_ref = qref / (1+qref)**2
        success_new = (qrare+qref) / denom
        counterexample_rows.append({
            "n": n, "gap": int(gap), "norm_E": mp.nstr(perturbation, 12),
            "rare_diagonal_ratio": mp.nstr(qrare/qref, 12),
            "posterior_T": mp.nstr(posterior_t, 12),
            "reference_success": mp.nstr(success_ref, 12),
            "perturbed_success": mp.nstr(success_new, 12),
        })

    local_conditioning = []
    t = mp.mpf('1e-10')
    for s in (mp.mpf('0.1'), mp.mpf(1), mp.mpf(3), mp.mpf(6), mp.mpf(10)):
        r = mp.sqrt(s*s+t*t)
        c = mp.cosh(t*t/(r+s)) + t*t/(r*(r+s))*mp.sinh(s)*mp.sinh(r)
        h = mp.acosh(c)
        predicted = mp.sinh(s)/s
        local_conditioning.append({"spectral_width": str(2*s), "measured_h_over_t": mp.nstr(h/t, 14), "sharp_local_constant": mp.nstr(predicted, 14)})

    polynomial_rows = []
    for radius in (mp.mpf('0.5'), mp.mpf(2), mp.mpf(10)):
        for p in (8, 20):
            N = 12*int(mp.ceil(radius))+p+2
            largest_relative = mp.mpf(0)
            for j in range(121):
                x = -radius + 2*radius*j/120
                q = mp.fsum(x**k/mp.factorial(k) for k in range(N))
                largest_relative = max(largest_relative, abs(q/mp.exp(x)-1))
            polynomial_rows.append({"R": str(radius), "p": p, "degree": N-1, "max_grid_relative_error": mp.nstr(largest_relative, 10), "allowed": mp.nstr(mp.power(2, -p), 10)})
            assert largest_relative <= mp.power(2, -p)

    assert maximum_bound_violation < 1e-10
    assert maximum_hilbert_expansion < 1e-10
    assert maximum_ext_identity_error < 1e-9
    assert maximum_sharp_filter_error < 1e-10
    print(json.dumps({
        "random_CP_filter_cases": random_filter_cases,
        "maximum_bound_violation": maximum_bound_violation,
        "maximum_hilbert_expansion": maximum_hilbert_expansion,
        "maximum_sharp_filter_error": maximum_sharp_filter_error,
        "maximum_exterior_identity_error": maximum_ext_identity_error,
        "finite_bit_counterexample": counterexample_rows,
        "noncommuting_local_conditioning": local_conditioning,
        "commuting_polynomial_grid_checks": polynomial_rows,
        "scope": "finite numerical diagnostics; no FPRAS, quantum compiler, theorem prover, or physical experiment executed"
    }, indent=2))


if __name__ == '__main__':
    run()
