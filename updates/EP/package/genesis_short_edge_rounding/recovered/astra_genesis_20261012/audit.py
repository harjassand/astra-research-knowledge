#!/usr/bin/env python3
"""Internal checks for the short-edge rounding proof, 12 October 2026.

These tests are not a proof checker and do not implement the rounding theorem.
They verify exact scalar certificates and stress-test two analytic identities
used in its proof. NumPy and SciPy are required. Run with one BLAS thread.
"""
from __future__ import annotations

import json
import math
from fractions import Fraction as F
from pathlib import Path

import numpy as np
from scipy.linalg import null_space


def exact_certificates() -> dict:
    terms = {
        "large_rows": F(1, 4),
        "binding_barriers": F(9, 128),
        "normalised_high_spectrum": F(5, 32),
        "positive_curvature": F(3, 8),
        "ridge_allowance": F(5, 256),
    }
    total = sum(terms.values(), F(0))
    e3_lower = sum((F(3**j, math.factorial(j)) for j in range(5)), F(0))
    assert total == F(223, 256) < 1
    assert e3_lower == F(131, 8) > 16
    assert F(1, 2) + F(1, 512) < 1
    return {
        "terms_multiplying_s_over_k": {key: str(value) for key, value in terms.items()},
        "total": str(total),
        "remaining_face_dimension": str(1 - total),
        "exp_3_strict_lower_bound": str(e3_lower),
        "exp_3_exceeds_16": True,
        "sign_cube_error_less_than": "108 k",
        "zero_one_error_less_than": "54 k",
    }


def normalised_resolvent_tests(rng: np.random.Generator, count: int = 160) -> dict:
    max_relative_error = 0.0
    max_eigenvalue_error = 0.0
    max_low_response = 0.0
    for trial in range(count):
        n = (5, 9, 15, 24)[trial % 4]
        C = rng.uniform(0.0, 1.0, size=(n, n + 3)) / n
        B = np.diag(rng.uniform(0.0, 0.5, size=n))
        eta = 1e-5 / n
        # Fix a nondegenerate positive matrix; the identity itself is valid
        # beyond the numerical parameters used in the rounding theorem.
        M = C @ C.T + B + eta * np.ones((n, n))
        eig, vec = np.linalg.eigh(M)
        L, v = eig[-1], vec[:, -1]
        assert np.min(L - np.diag(B)) > 0
        sd = 1.0 / np.sqrt(L - np.diag(B))
        K = sd[:, None] * (C @ C.T + eta * np.ones((n, n))) * sd[None, :]
        keig, kvec = np.linalg.eigh(K)
        max_eigenvalue_error = max(max_eigenvalue_error, abs(keig[-1] - 1.0))
        y = rng.normal(size=n)
        y -= v * (v @ y)
        lhs = float(np.sum((vec[:, :-1].T @ y) ** 2 / (L - eig[:-1])))
        rhs = float(np.sum((kvec[:, :-1].T @ (sd * y)) ** 2 / (1.0 - keig[:-1])))
        relative_error = abs(lhs - rhs) / max(1.0, abs(lhs), abs(rhs))
        max_relative_error = max(max_relative_error, relative_error)
        low = keig < 0.2
        CL = sd[:, None] * C
        factors = (kvec[:, low].T @ CL) / np.sqrt(1.0 - keig[low])[:, None]
        response = factors.T @ factors
        top = float(np.linalg.eigvalsh(response)[-1])
        max_low_response = max(max_low_response, top)
        assert top <= 0.25 + 1e-10
        assert relative_error < 1e-10
    return {
        "cases": count,
        "maximum_relative_quadratic_form_error": max_relative_error,
        "maximum_error_in_top_eigenvalue_of_K": max_eigenvalue_error,
        "maximum_low_response_eigenvalue": max_low_response,
        "low_response_upper_bound": 0.25,
    }


def curvature_tests(rng: np.random.Generator, count: int = 24) -> dict:
    max_diag_ratio = 0.0
    max_Lprime = 0.0
    max_response_violation = -math.inf
    max_fd_error = 0.0
    max_phi_second = -math.inf
    for trial in range(count):
        k = 1 + (trial % 2)
        n = 96 if k == 1 else 160
        m = 12
        R = 2.0 * math.sqrt(k)
        beta = 1.0 / R
        H0 = 11.0 * R * R
        A0 = 4.0 * R * R
        Delta = 1.0 / (16.0 * R * R)
        eta = 1.0 / (1024.0 * k * n)
        z = rng.uniform(0.9, 1.1, size=(m, n))
        z /= z.sum(axis=1)[:, None]
        assert z.max() <= Delta
        q = R * R / 2.0
        r = math.sqrt(q)
        b = np.sqrt(q * z) * rng.choice([-1.0, 1.0], size=(m, n))
        assert np.max(np.sum(b * b, axis=0)) <= 1.0
        x = rng.uniform(-0.7, 0.7, size=n)
        if k == 2:
            x[1::2] = -x[0::2]
        f = lambda y: 2.0 * R * (1.0 - y * y)
        E = q * (z @ f(x))
        Z = np.repeat(z, 2, axis=0)
        signs = np.tile(np.array([1.0, -1.0]), m)
        beta_ridge = eta * np.ones((n, n))

        def state_from_plus_barrier(plus_barrier: float):
            d = H0 + r * plus_barrier - E / r - 6.0 * R * r
            u = ((signs * np.repeat(d, 2) - H0) / r
                 + np.repeat(E, 2) / (r * r) + 6.0 * R)
            a = A0 * np.exp(beta * u)
            mat = (Z.T * a) @ Z + beta_ridge
            return d, a, mat

        lo, hi = -50.0, 0.0
        for _ in range(48):
            mid = (lo + hi) / 2
            _, _, mat = state_from_plus_barrier(mid)
            if np.linalg.eigvalsh(mat)[-1] < 1.06:
                lo = mid
            else:
                hi = mid
        d, a, M = state_from_plus_barrier((lo + hi) / 2)
        eig, vec = np.linalg.eigh(M)
        L, v = eig[-1], vec[:, -1]
        gradients = (signs[:, None] * np.repeat(b, 2, axis=0) / r
                     - 4.0 * R * Z * x[None, :])
        zv = Z @ v
        G = (np.sqrt(a) * beta * zv)[:, None] * gradients
        C = Z.T * np.sqrt(a)
        U = G.T @ G
        Ddiag = 4.0 * R * beta * (Z.T @ (a * zv * zv))
        ratio = np.diag(U) / Ddiag
        max_diag_ratio = max(max_diag_ratio, float(np.max(ratio) * R * R))
        assert np.all(np.diag(U) <= Ddiag / (R * R) + 1e-12)
        # Here B=0, so S is scalar. Tests above separately cover nonconstant B.
        sd = np.ones(n) / math.sqrt(L)
        K = M / L
        keig, kvec = np.linalg.eigh(K)
        high = keig >= 0.2
        constraints = [kvec[:, high].T @ (sd[:, None] * (C @ G))]
        if k == 2:
            pairs = np.zeros((n // 2, n))
            pairs[np.arange(n // 2), 2 * np.arange(n // 2)] = 1.0
            pairs[np.arange(n // 2), 2 * np.arange(n // 2) + 1] = 1.0
            constraints.append(pairs)
        equations = np.vstack(constraints)
        equations /= np.linalg.norm(equations, axis=1)[:, None]
        N = null_space(equations, rcond=1e-11)
        Q = 1.5 * U - np.diag(Ddiag)
        qeig, qvec = np.linalg.eigh(N.T @ Q @ N)
        h = N @ qvec[:, 0]
        h /= np.linalg.norm(h)
        forcing = C @ (G @ h)
        Lprime = float(v @ forcing)
        exact_second = float(h @ (U - np.diag(Ddiag)) @ h
                             + 2 * np.sum((vec[:, :-1].T @ forcing) ** 2 / (L - eig[:-1])))
        upper = float(h @ Q @ h)
        max_Lprime = max(max_Lprime, abs(Lprime))
        max_response_violation = max(max_response_violation, exact_second - upper)
        assert exact_second <= upper + 1e-10
        assert upper < 0
        phi_second = 6 * (L - 1) * Lprime**2 + 3 * (L - 1)**2 * exact_second - 2 * eta
        max_phi_second = max(max_phi_second, phi_second)
        assert phi_second < 0
        offset = d - b @ x

        def actual_L(step: float) -> float:
            y = x + step * h
            dy = offset + b @ y
            Ey = q * (z @ f(y))
            uy = ((signs * np.repeat(dy, 2) - H0) / r
                  + np.repeat(Ey, 2) / (r * r) + 6 * R)
            ay = A0 * np.exp(beta * uy)
            return float(np.linalg.eigvalsh((Z.T * ay) @ Z + beta_ridge)[-1])

        step = 0.002
        fd = (actual_L(step) - 2 * L + actual_L(-step)) / step**2
        max_fd_error = max(max_fd_error, abs(fd - exact_second))
        assert abs(fd - exact_second) < 2e-7
    return {
        "cases": count,
        "partition_face_cases": count // 2,
        "maximum_R_squared_times_diagonal_ratio": max_diag_ratio,
        "diagonal_ratio_upper_bound": 1.0,
        "maximum_absolute_L_prime_on_selected_direction": max_Lprime,
        "maximum_exact_curvature_minus_proved_upper_bound": max_response_violation,
        "maximum_finite_difference_absolute_error": max_fd_error,
        "largest_selected_potential_second_derivative": max_phi_second,
        "warning": "Local analytic stress tests only; no rounding algorithm or theorem-level numerical validation.",
    }


def main() -> None:
    rng = np.random.default_rng(20261012)
    result = {
        "status": "Internal checks only; not independent verification or formal proof.",
        "seed": 20261012,
        "exact_scalar_certificates": exact_certificates(),
        "normalised_resolvent": normalised_resolvent_tests(rng),
        "spectral_curvature": curvature_tests(rng),
    }
    output = Path(__file__).with_name("audit_results.json")
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
