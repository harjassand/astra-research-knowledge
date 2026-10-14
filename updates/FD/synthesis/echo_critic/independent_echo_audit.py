"""Independent finite tests and exact conditional echo certificate.

Uses only numpy for finite matrix tests; exact certificate uses Fraction.
Does not import or alter the CRAY source scripts. Finite passes do not prove
the theorem, certify a simulator, establish novelty, or validate hardware.
"""
from __future__ import annotations

from fractions import Fraction as F
import hashlib
import json
import math
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
BASE = HERE.parent.parent
SOURCE = BASE / "work/sources/cray_active_acquisition"


def frac(value: F) -> str:
    return str(value)


def exp_lower(x: F, degree: int = 100) -> F:
    assert x >= 0
    term = F(1)
    total = term
    for k in range(1, degree + 1):
        term *= x / k
        total += term
    return total


def exact_certificate() -> dict:
    record = json.loads((SOURCE / "retained_memory_results.json").read_text())
    n, observed = record["N"], record["failures"]
    assert (n, observed) == (100_000_000, 7)
    assert len(record["event_times"]) == observed
    assert all(1 <= x <= n for x in record["event_times"])
    assert sorted(set(record["event_times"])) == record["event_times"]
    q, alpha = F(161, 10**9), F(1, 100)
    x = n * q
    a = x / (1 - q)
    poly = sum(a**j / math.factorial(j) for j in range(observed + 1))
    tail_upper = poly / exp_lower(x)
    assert tail_upper < alpha

    # Source inputs, not the simulator's exact residual.
    d, t = 8, F(1, 50)
    J, Rcap, w = F(779, 100), F(2), F(1, 5)
    Lambda = 2 * J + Rcap
    assert Lambda == F(879, 50)
    D = t * (1 - Lambda * t / 2)
    coefficient = D**2 / (4 * d)
    assert D == F(4121, 250000)
    assert coefficient == F(16982641, 2000000000000)

    rows = []
    for gamma, radius_bound in [
        (F(0), F(69, 500)),
        (F(1, 10**8), F(71, 500)),
        (F(1, 10**7), F(22, 125)),
    ]:
        radius_square = (q + gamma) / coefficient
        assert radius_square < radius_bound**2
        rows.append({
            "gamma": frac(gamma),
            "exact_squared_radius": frac(radius_square),
            "radius_approximation_only": math.sqrt(radius_square),
            "strict_rational_radius_upper": frac(radius_bound),
            "closed_deltaF_interval": [frac(w - radius_bound), frac(w + radius_bound)],
            "positive_interval_exact": radius_bound < w,
        })
    ceiling = coefficient * w**2 - q
    assert ceiling == F(8932641, 50000000000000)
    assert (q + F(2, 10**7)) / coefficient > w**2

    # Optional tighter endpoint: a small exact margin remains mathematically
    # valid, although the main certificate above uses the wider tail slack.
    q_tight = F(160, 10**9)
    x_tight = n * q_tight
    a_tight = x_tight / (1 - q_tight)
    tail_tight = sum(a_tight**j / math.factorial(j) for j in range(observed + 1)) / exp_lower(x_tight)
    assert tail_tight < alpha
    tight_radius_square = (q_tight + F(1, 10**7)) / coefficient
    assert tight_radius_square < F(7, 40)**2

    return {
        "status": "Exact conditional arithmetic for a supplied simulated count record",
        "source_count_sha256": hashlib.sha256((SOURCE / "retained_memory_results.json").read_bytes()).hexdigest(),
        "N": n,
        "failures": observed,
        "alpha": frac(alpha),
        "q_safe_upper": frac(q),
        "tail_upper_rational": frac(tail_upper),
        "tail_upper_approximation_only": float(tail_upper),
        "tail_upper_strictly_below_alpha_exact": True,
        "dimension": d,
        "time": frac(t),
        "J": frac(J),
        "Rcap": frac(Rcap),
        "Lambda": frac(Lambda),
        "w": frac(w),
        "coefficient_exact": frac(coefficient),
        "positive_sign_gamma_ceiling_strict": frac(ceiling),
        "gamma_rows": rows,
        "optional_tighter_certificate": {
            "q_safe_upper": frac(q_tight),
            "tail_upper_rational": frac(tail_tight),
            "tail_upper_approximation_only": float(tail_tight),
            "gamma": "1/10000000",
            "strict_rational_radius_upper": "7/40",
            "closed_deltaF_interval": ["1/40", "3/8"],
        },
        "extra_product_budget_required": False,
        "unchanged_obligations": [
            "True residual support and collar/outside factorization",
            "Coherent comparison and local maximally mixed reset",
            "State-uniform conditional apparatus-error allowance",
            "Fixed predeclared validation count/time/candidate or proper selection budget",
            "Source model, tails, sector, scalar-reference and physical-unit accounting",
        ],
        "nonclaims": [
            "No laboratory data or verified apparatus allowance",
            "No rigorous floating-point quantum-trajectory simulation certificate",
            "No novelty, generic successful witness, or matched-method advantage",
        ],
    }


def exact_twirl_checks() -> dict:
    """Exact real-rational correlated example; XZ and Y conjugations agree."""
    I = np.array([[F(1), F(0)], [F(0), F(1)]], dtype=object)
    X = np.array([[F(0), F(1)], [F(1), F(0)]], dtype=object)
    Z = np.array([[F(1), F(0)], [F(0), F(-1)]], dtype=object)
    paulis = [I, X, Z, X @ Z]
    # Normalized entangled vector (3|00>+4|11>)/5 has rational amplitudes.
    v = np.array([[F(3, 5)], [F(0)], [F(0)], [F(4, 5)]], dtype=object)
    rho = v @ v.T
    outside = np.array([[F(9, 25), F(0)], [F(0), F(16, 25)]], dtype=object)
    target = np.kron(I / 2, outside)
    twirled = np.zeros((4, 4), dtype=object)
    for P in paulis:
        G = np.kron(P, I)
        term = G @ rho @ G.T
        twirled += term / 4
        # Every conditional state remains pure, entangled, and not product.
        assert np.trace(term @ term) == F(1)
        assert not np.array_equal(term, target)
    assert np.array_equal(twirled, target)
    assert np.trace(target) == F(1)

    # Current-P conditioning counterexample: H=0, rank-one local residual,
    # initial |1>, with echo real part diag(3/5,1). This is the real part of a
    # unitary diag(3/5-4i/5,1), so the following failure probabilities are exact.
    initial = np.array([[F(0), F(0)], [F(0), F(1)]], dtype=object)
    echo_real = np.array([[F(3, 5), F(0)], [F(0), F(1)]], dtype=object)
    failures = []
    for P in paulis:
        current = P @ initial @ P.T
        p = (1 - np.trace(current @ echo_real)) / 2
        failures.append(p)
    assert failures == [F(0), F(1, 5), F(0), F(1, 5)]
    pooled = sum(failures) / 4
    assert pooled == F(1, 10)
    return {
        "status": "Exact Fraction identities for declared two-qubit example and count-selection counterexample",
        "correlated_input": "Pure (3|00>+4|11>)/5",
        "Pauli_conjugations": ["I", "X", "Z", "XZ (same conjugation as Y)"],
        "outside_density_diagonal": ["9/25", "16/25"],
        "twirled_density_diagonal": [frac(target[i, i]) for i in range(4)],
        "twirl_equals_product_exact": True,
        "each_current_P_conditioned_state_remains_entangled": True,
        "selection_counterexample_failure_probabilities": [frac(p) for p in failures],
        "selection_counterexample_pooled_failure": frac(pooled),
        "selection_counterexample_I_Z_conditioned_failure": "0",
        "fresh_label_preparation_still_required": True,
        "not_hardware_validation": True,
    }


def opnorm(x: np.ndarray) -> float:
    return float(np.linalg.svd(x, compute_uv=False)[0])


def hermitian(rng, dim: int, norm: float = 1.) -> np.ndarray:
    x = rng.normal(size=(dim, dim)) + 1j * rng.normal(size=(dim, dim))
    h = (x + x.conj().T) / 2
    return h * (norm / opnorm(h))


def unitary_exp(h: np.ndarray, t: float) -> np.ndarray:
    # Spectral construction is independent of the source's scipy expm route.
    eigenvalues, eigenvectors = np.linalg.eigh(h)
    return (eigenvectors * np.exp(1j * t * eigenvalues)) @ eigenvectors.conj().T


def density(rng, dim: int, pure: bool = False) -> np.ndarray:
    width = 1 if pure else dim
    x = rng.normal(size=(dim, width)) + 1j * rng.normal(size=(dim, width))
    rho = x @ x.conj().T
    return rho / np.trace(rho)


def module_norm(o: np.ndarray, d: int, b: int) -> float:
    blocks = (o.conj().T @ o).reshape(d, b, d, b)
    reduced = np.einsum("aiaj->ij", blocks) / d
    return math.sqrt(max(0., float(np.linalg.eigvalsh(reduced)[-1])))


def matrix_tests() -> dict:
    rng = np.random.default_rng(20261014_721)
    counts = {"generic_models": 0, "product_models": 0, "pointwise_bounds": 0,
              "product_multiplier_checks": 0, "extremal_vector_checks": 0}
    ratios = {"largest_source_remainder_fraction": 0.,
              "largest_module_remainder_fraction": 0.,
              "largest_product_multiplier_fraction": 0.,
              "minimum_new_probability_to_bound": 1e300,
              "minimum_module_probability_to_bound": 1e300,
              "maximum_unitary_identity_error": 0.}

    # Arbitrary finite interaction matrices; no product-budget input.
    for index in range(100):
        d = [2, 3, 4, 8, 12][index % 5]
        b = [2, 3, 5][index % 3]
        touching = hermitian(rng, d * b, rng.uniform(.3, 3.))
        bath = hermitian(rng, b, rng.uniform(0., 2000.))
        H = touching + np.kron(np.eye(d), bath)
        if index % 2:
            v = density(rng, d, pure=True)
            r = v * rng.uniform(.02, .7)
        else:
            r = hermitian(rng, d, rng.uniform(.02, .7))
        R = np.kron(r, np.eye(b))
        rnorm = opnorm(r)
        Rcap = rnorm * rng.uniform(1., 5.)
        lam = 2 * opnorm(touching) + Rcap
        rvals, rvecs = np.linalg.eigh(r)
        vstar = rvecs[:, np.argmax(np.abs(rvals))]
        for time_ratio in [.2, .7, 1., 1.5, 1.9]:
            t = time_ratio / lam
            E = unitary_exp(H, t) @ unitary_exp(H + R, -t)
            L = E - np.eye(d * b)
            D = L + 1j * t * R
            cap = lam * t * t * rnorm / 2
            assert opnorm(D) <= cap + 5e-10
            ratios["largest_source_remainder_fraction"] = max(
                ratios["largest_source_remainder_fraction"], opnorm(D) / cap)
            c = t * t * (1 - lam * t / 2)**2 / (4 * d)
            for pure in [False, True]:
                tau = density(rng, b, pure=pure)
                rho = np.kron(np.eye(d) / d, tau)
                p = float(np.trace(rho @ (L.conj().T @ L)).real / 4)
                p_via_echo = (1 - float(np.trace(rho @ E).real)) / 2
                error = abs(p - p_via_echo)
                assert error < 5e-10
                ratios["maximum_unitary_identity_error"] = max(
                    ratios["maximum_unitary_identity_error"], error)
                assert p + 5e-11 >= c * rnorm**2
                ratios["minimum_new_probability_to_bound"] = min(
                    ratios["minimum_new_probability_to_bound"], p / (c * rnorm**2))
                counts["pointwise_bounds"] += 1
            x = rng.normal(size=b) + 1j * rng.normal(size=b)
            x /= np.linalg.norm(x)
            signal = np.linalg.norm(L @ np.kron(vstar, x))
            lower = t * (1 - lam * t / 2) * rnorm
            assert signal + 5e-10 >= lower
            counts["extremal_vector_checks"] += 1
        counts["generic_models"] += 1

    # Independently inspect the superseded draft's actual product-norm claim.
    for index in range(80):
        d = [2, 3, 4, 8][index % 4]
        b = [2, 3, 5][index % 3]
        hs = hermitian(rng, d, rng.uniform(.1, 2.))
        he = hermitian(rng, b, rng.uniform(0., 1000.))
        V = np.zeros((d * b, d * b), dtype=complex)
        kappa = 0.
        for _ in range(3):
            A = hermitian(rng, d, rng.uniform(.1, 1.5))
            B = hermitian(rng, b, rng.uniform(.1, 1.5))
            V += np.kron(A, B)
            kappa += opnorm(A) * opnorm(B)
            O = rng.normal(size=(d * b, d * b)) + 1j * rng.normal(size=(d * b, d * b))
            multiplier_fraction = module_norm(O @ np.kron(A, B), d, b) / (
                opnorm(A) * opnorm(B) * module_norm(O, d, b))
            assert multiplier_fraction <= 1. + 1e-11
            ratios["largest_product_multiplier_fraction"] = max(
                ratios["largest_product_multiplier_fraction"], multiplier_fraction)
            counts["product_multiplier_checks"] += 1
        r = hermitian(rng, d, rng.uniform(.02, .8))
        R = np.kron(r, np.eye(b))
        rnorm = opnorm(r)
        lam = 2 * opnorm(hs) + 2 * kappa + 2 * rnorm
        H = np.kron(hs, np.eye(b)) + np.kron(np.eye(d), he) + V
        t = rng.uniform(.1, .9) / lam
        E = unitary_exp(H, t) @ unitary_exp(H + R, -t)
        D = E - np.eye(d * b) + 1j * t * R
        sigma = math.sqrt(float(np.trace(r @ r).real) / d)
        f = (math.expm1(kappa * t) - kappa * t) / kappa**2
        cap = lam * f * sigma
        norm_d = module_norm(D, d, b)
        assert norm_d <= cap + 5e-10
        ratios["largest_module_remainder_fraction"] = max(
            ratios["largest_module_remainder_fraction"], norm_d / cap)
        for pure in [False, True]:
            tau = density(rng, b, pure)
            rho = np.kron(np.eye(d) / d, tau)
            L = E - np.eye(d * b)
            p = float(np.trace(rho @ (L.conj().T @ L)).real / 4)
            lb = (t - lam * f)**2 * rnorm**2 / (4 * d)
            assert p + 5e-11 >= lb
            ratios["minimum_module_probability_to_bound"] = min(
                ratios["minimum_module_probability_to_bound"], p / lb)
        counts["product_models"] += 1

    # Exact structure of the multiplier counterexample, evaluated numerically.
    swap_rows = []
    for d in [2, 4, 8, 16]:
        swap = np.zeros((d * d, d * d))
        for i in range(d):
            for j in range(d):
                swap[j * d + i, i * d + j] = 1.
        P = np.zeros((d, d)); P[0, 0] = 1.
        O = np.kron(P, np.eye(d))
        quotient = module_norm(O @ swap, d, d) / module_norm(O, d, d)
        assert abs(quotient - math.sqrt(d)) < 1e-12
        assert abs(opnorm(swap) - 1.) < 1e-12
        swap_rows.append({"d": d, "operator_norm_V": 1., "module_multiplier_ratio": quotient})

    # Rank-one signal formula: shows the dimension factor of this interface.
    rank_one_rows = []
    theta = .4
    for d in [2, 4, 8, 16, 32]:
        expected = (1 - math.cos(theta)) / (2 * d)
        R = np.zeros((d, d)); R[0, 0] = theta
        E = unitary_exp(R, -1.)
        p = (1 - np.trace(E).real / d) / 2
        assert abs(p - expected) < 1e-14
        rank_one_rows.append({"d": d, "p": p, "d_times_p": d * p})
    return {
        "status": "Finite floating-point diagnostics only; proof is in the accompanying note",
        "seed": 20261014_721,
        "counts": counts,
        "ratios": ratios,
        "SWAP_multiplier_counterexamples": swap_rows,
        "rank_one_signal_dimension_checks": rank_one_rows,
        "numpy_version": np.__version__,
    }


if __name__ == "__main__":
    result = {"exact_conditional_certificate": exact_certificate(),
              "exact_twirl_checks": exact_twirl_checks(),
              "independent_matrix_tests": matrix_tests()}
    (HERE / "INDEPENDENT_ECHO_AUDIT.json").write_text(json.dumps(result, indent=2) + "\n")
    short = dict(result["independent_matrix_tests"])
    short.pop("SWAP_multiplier_counterexamples")
    short.pop("rank_one_signal_dimension_checks")
    print(json.dumps(short, indent=2))
    print("Exact gamma=1e-7 interval:", result["exact_conditional_certificate"]["gamma_rows"][2]["closed_deltaF_interval"])
