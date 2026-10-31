#!/usr/bin/env python3
"""Read-only numerical checks of OUTPUT_MODE_AUDIT.md.

Uses NumPy and SciPy. No root-file changes, network calls, or file writes.
"""

from __future__ import annotations

import math
import numpy as np
from scipy.integrate import quad, solve_ivp
from scipy.linalg import expm


RNG = np.random.default_rng(161803398)
TOL = 3e-8


def outer(vector):
    return np.outer(vector, vector.conj())


def trace_norm(matrix):
    return float(np.sum(np.linalg.svd(matrix, compute_uv=False)))


def integrate_complex(function, left, right):
    return quad(lambda x: function(x).real, left, right, epsabs=2e-11)[0] + 1j * quad(
        lambda x: function(x).imag, left, right, epsabs=2e-11
    )[0]


def scalar_filter(kappa, duration):
    a = kappa / 2
    z = math.exp(-a * duration)
    V = duration - 2 / a * math.tanh(a * duration / 2)
    w = lambda t: (1 - 2 * np.exp(-a * t) / (1 + z)) / math.sqrt(V)
    k = lambda t: (
        (1 - np.exp(-a * t)) * (1 - np.exp(-a * (duration - t)))
        / (a * (1 + z) * math.sqrt(V))
    )
    return w, k, V


def verify_scalar():
    residual = 0.0
    for duration in (0.3, 2.0, 8.0, 20.0):
        w, k, V = scalar_filter(1.0, duration)
        values = [
            quad(lambda t: w(t) ** 2, 0, duration)[0] - 1,
            quad(lambda t: w(t) * np.exp(-t / 2), 0, duration)[0],
            quad(k, 0, duration)[0] - 2 * math.sqrt(V),
        ]
        residual = max(residual, max(abs(value) for value in values))
        assert max(abs(value) for value in values) < TOL
        assert min(k(t) for t in np.linspace(0, duration, 1001)) >= -TOL
    return {"scalar_identity_residual": residual}


def receiver_filter(A, monitored_row, duration):
    """Real Gram projection for independent real and imaginary startup columns."""
    dimension = A.shape[0]
    nodes, weights = np.polynomial.legendre.leggauss(280)
    times = (nodes + 1) * duration / 2
    weights = weights * duration / 2

    def basis(t):
        row = monitored_row @ expm(A * float(t))
        return np.concatenate([row.real, row.imag])

    samples = np.array([basis(t) for t in times])
    gram = samples.T @ (weights[:, None] * samples)
    rhs = samples.T @ weights
    # Fixed examples below have independent nuisance columns.
    assert np.linalg.eigvalsh(gram)[0] > 1e-12
    coefficients = np.linalg.solve(gram, rhs)
    V = duration - rhs @ coefficients
    assert V > 0

    def w(t):
        return (1 - basis(t) @ coefficients) / math.sqrt(V)

    return w, V, times, weights, float(np.linalg.cond(gram))


def verify_detuned_conjugation():
    kappa, delta, duration = 1.0, 0.3, 12.0
    lam = kappa / 2 + 1j * delta
    A = np.array([[-lam]], dtype=complex)
    row = np.array([math.sqrt(kappa)], dtype=complex)
    w, V, _, _, _ = receiver_filter(A, row, duration)

    def k(t):
        return integrate_complex(
            lambda u: w(u) * np.exp(-lam * (u - t)), t, duration
        )

    def h(t):
        return w(t) - kappa * k(t)

    t = 0.37 * duration
    direct_commutator = -math.sqrt(kappa) * integrate_complex(
        lambda r: np.exp(-lam * (t - r)) * h(r).conjugate(), 0, t
    )
    corrected = math.sqrt(kappa) * k(t).conjugate()
    incorrect = math.sqrt(kappa) * k(t)
    assert abs(direct_commutator - corrected) < TOL
    assert abs(direct_commutator - incorrect) > 1e-3
    return {
        "detuned_correct_conjugation_residual": abs(direct_commutator - corrected),
        "detuned_unconjugated_error": abs(direct_commutator - incorrect),
    }


def verify_multimode():
    H = np.array([[0.3, 0.23], [0.23, -0.6]], dtype=complex)
    C = np.diag([math.sqrt(1.1), math.sqrt(0.7)]).astype(complex)
    A = -1j * H - C.conj().T @ C / 2
    monitored_row = C[0]
    drive = np.array([0.8, 0.4j], dtype=complex)
    assert np.allclose(A + A.conj().T, -C.conj().T @ C)
    assert np.max(np.linalg.eigvals(A).real) < 0
    dc = -drive.conj() @ np.linalg.solve(A.conj().T, monitored_row.conj())
    phase = np.angle(dc)
    chi = float((np.exp(-1j * phase) * dc).real)
    assert chi > 0
    largest_startup = largest_response = largest_canonical = 0.0
    negative_scaled = []
    for duration in (10.0, 20.0, 40.0):
        w, V, times, weights, condition = receiver_filter(A, monitored_row, duration)
        startup = sum(
            weight * w(t) * (monitored_row @ expm(A * t))
            for t, weight in zip(times, weights)
        )
        norm = sum(weight * w(t) ** 2 for t, weight in zip(times, weights))
        assert np.linalg.norm(startup) < TOL
        assert abs(norm - 1) < TOL
        largest_startup = max(largest_startup, float(np.linalg.norm(startup)))

        def derivative(t, value):
            return -np.exp(-1j * phase) * w(t) * monitored_row.conj() - A.conj().T @ value

        solution = solve_ivp(
            derivative, (duration, 0.0), np.zeros(2, dtype=complex),
            rtol=3e-11, atol=3e-12, dense_output=True,
        )
        assert solution.success

        def beta(t):
            return float((drive.conj() @ solution.sol(t)).real)

        integrated = quad(beta, 0, duration, epsabs=2e-9, limit=200)[0]
        response_residual = abs(integrated - chi * math.sqrt(V))
        assert response_residual < TOL
        largest_response = max(largest_response, response_residual)
        negative = quad(lambda t: max(-beta(t), 0.0), 0, duration, epsabs=2e-9, limit=200)[0]
        negative_scaled.append(negative * math.sqrt(V))

        # The bath-only output coefficient over all physical loss/input ports.
        bath_norm = 0.0
        for t, weight in zip(times, weights):
            commutator = solution.sol(t)
            bath_row = (
                np.exp(1j * phase) * w(t) * np.array([1.0, 0.0])
                - commutator.conj() @ C.conj().T
            )
            bath_norm += weight * float(np.vdot(bath_row, bath_row).real)
        canonical_residual = abs(bath_norm - 1)
        assert canonical_residual < TOL
        largest_canonical = max(largest_canonical, canonical_residual)
    return {
        "multimode_startup_residual": largest_startup,
        "multimode_integrated_response_residual": largest_response,
        "multimode_canonical_bath_norm_residual": largest_canonical,
        "multimode_DC_chi": chi,
        "sample_negative_area_times_sqrt_V": negative_scaled,
    }


def random_density(dimension):
    sample = RNG.normal(size=(dimension, dimension)) + 1j * RNG.normal(
        size=(dimension, dimension)
    )
    state = sample @ sample.conj().T
    return state / np.trace(state)


def positive_sqrt(matrix):
    values, vectors = np.linalg.eigh(matrix)
    return (vectors * np.sqrt(np.maximum(values, 0))) @ vectors.conj().T


def verify_two_sided_cp_comparator():
    Ps = [np.diag([1.0, 0.0]), np.diag([0.0, 1.0])]
    p = 0.12
    rotation = np.array([[math.cos(0.4), -math.sin(0.4)], [math.sin(0.4), math.cos(0.4)]])
    errors = [
        np.diag([0.02, p]),
        rotation @ np.diag([0.04, 0.09]) @ rotation.T,
    ]
    operators = {}
    for logical in (0, 1):
        for record in (0, 1):
            effect = errors[logical] if record != logical else np.eye(2) - errors[logical]
            operators[record, logical] = np.kron(Ps[logical], positive_sqrt(effect))
    max_excess = 0.0
    for _ in range(40):
        state = random_density(8)  # Logical 2, source 2, reference 2.
        physical = np.zeros((16, 16), dtype=complex)
        ideal = np.zeros_like(physical)
        wrong = 0.0
        for record in (0, 1):
            physical_kraus = operators[record, 0] + operators[record, 1]
            extended = np.kron(physical_kraus, np.eye(2))
            flag = np.diag([float(record == 0), float(record == 1)])
            physical += np.kron(flag, extended @ state @ extended.conj().T)
            for logical in (0, 1):
                extended = np.kron(operators[record, logical], np.eye(2))
                branch = extended @ state @ extended.conj().T
                correct_flag = np.diag([float(logical == 0), float(logical == 1)])
                ideal += np.kron(correct_flag, branch)
                if record != logical:
                    wrong += float(np.trace(branch).real)
        distance = trace_norm(physical - ideal) / 2
        bound = wrong + math.sqrt(wrong * (1 - wrong))
        max_excess = max(max_excess, distance - bound)
        assert wrong <= p + TOL
        assert distance <= bound + TOL
        assert np.isclose(np.trace(physical), 1)
        assert np.isclose(np.trace(ideal), 1)
    return {"CP_comparator_max_bound_excess": max_excess}


def verify_marginal_only_counterexample():
    mu, v, steepness = 1.5, 1.0, 2.0
    density = lambda y: math.exp(-y * y / (2 * v)) / math.sqrt(2 * math.pi * v)
    conditional_plus = lambda y: (1 + math.tanh(steepness * y)) / 2
    actual = 2 * quad(lambda y: density(y) * conditional_plus(y), mu, np.inf)[0]
    claimed = math.erfc(mu / math.sqrt(2 * v)) / 2
    assert claimed < actual < 2 * claimed
    return {
        "unconditional_Gaussian_one_tail": claimed,
        "correlated_input_actual_wrong": actual,
    }


def verify_coarse_rate_settling():
    rate_low, rate_high = 0.8, 1.3
    gain_low, variance, energy = 0.35, 1.6, 7.0
    epsilon = 1e-5
    receiver_second_moment = 2 * energy + 1 + 2 * math.sqrt(energy * (energy + 1))
    length = max(
        4 / rate_low,
        2 * rate_high * variance / gain_low**2 * math.log(1 / epsilon),
    )
    threshold = gain_low * math.sqrt(length / rate_high)
    settling = max(
        0.0,
        math.log(
            8 * rate_high * receiver_second_moment
            / (rate_low * gain_low**2 * length**2 * epsilon)
        ) / rate_low,
    )
    mu_low = 4 * gain_low * math.sqrt(length / rate_high) * (
        1 - 2 * math.exp(-rate_low * settling / 2) / (rate_low * length)
    )
    residue_upper = 4 * math.exp(-rate_low * settling) / (rate_low * length)
    gaussian = math.erfc((mu_low - threshold) / math.sqrt(2 * variance)) / 2
    receiver = residue_upper * receiver_second_moment / threshold**2
    assert mu_low >= 2 * threshold - TOL
    assert gaussian <= epsilon / 2 + TOL
    assert receiver <= epsilon / 2 + TOL

    # Test formulas at moderate windows where direct integration is informative.
    largest_integral_residual = 0.0
    for settling_test, length_test in ((0.0, 6.0), (1.2, 3.0), (4.0, 8.0)):
        duration = settling_test + length_test
        conservative_shift = 4 * gain_low * math.sqrt(length_test / rate_high) * (
            1 - 2 * math.exp(-rate_low * settling_test / 2) / (rate_low * length_test)
        )
        conservative_residue = (
            4 * math.exp(-rate_low * settling_test) / (rate_low * length_test)
        )
        for rate in np.linspace(rate_low, rate_high, 11):
            residue = (
                2 * math.exp(-rate * settling_test / 2)
                * (-math.expm1(-rate * length_test / 2))
                / math.sqrt(rate * length_test)
            )
            shift = 4 * gain_low * math.sqrt(length_test / rate) * (
                1 - 2 * math.exp(-rate * settling_test / 2)
                * (-math.expm1(-rate * length_test / 2)) / (rate * length_test)
            )

            def kernel(t):
                lower = max(t, settling_test)
                return (
                    2 / math.sqrt(rate * length_test)
                    * (math.exp(-rate * (lower - t) / 2)
                       - math.exp(-rate * (duration - t) / 2))
                )

            integral = 2 * gain_low * quad(
                kernel, 0, duration, points=[settling_test], epsabs=1e-11
            )[0]
            largest_integral_residual = max(largest_integral_residual, abs(integral - shift))
            assert abs(integral - shift) < TOL
            assert residue**2 <= conservative_residue + TOL
            assert residue**2 <= 1 + TOL
            if conservative_shift > 0:
                assert shift >= conservative_shift - TOL
    return {
        "settling_integrated_shift_residual": largest_integral_residual,
        "sizing_boxcar_length": length,
        "sizing_settling_time": settling,
        "sizing_label_bound": gaussian + receiver,
        "sizing_label_target": epsilon,
    }


def main():
    results = {}
    for verification in (
        verify_scalar,
        verify_detuned_conjugation,
        verify_multimode,
        verify_two_sided_cp_comparator,
        verify_marginal_only_counterexample,
        verify_coarse_rate_settling,
    ):
        results.update(verification())
    print("PASS: scalar, conjugation, multimode, CP comparator, freshness audits.")
    for label, value in results.items():
        print(f"{label}: {value}")
    print("Scope: floating-point diagnostics plus proofs; no hardware/domain certificate.")


if __name__ == "__main__":
    main()
