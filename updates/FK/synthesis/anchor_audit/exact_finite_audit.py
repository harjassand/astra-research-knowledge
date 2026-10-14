#!/usr/bin/env python3
"""Independent exact rational checks for the finite-anchor proof spine."""
from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


def cycle_laplacian(n: int) -> sp.Matrix:
    out = sp.zeros(n)
    for i in range(n):
        out[i, i] = 2
        out[i, (i - 1) % n] -= 1
        out[i, (i + 1) % n] -= 1
    return out


def product_green_and_lyapunov():
    nt, nx = 4, 3
    dim = nt * nx
    alpha, kt, kx = sp.Rational(2, 3), sp.Rational(5, 4), sp.Rational(7, 6)
    it, ix = sp.eye(nt), sp.eye(nx)
    lt, lx = cycle_laplacian(nt), cycle_laplacian(nx)
    K = alpha * sp.eye(dim) + kt * sp.kronecker_product(lt, ix) + kx * sp.kronecker_product(it, lx)
    C = K.inv()
    assert all(C[i, j] >= 0 for i in range(dim) for j in range(dim))

    green_errors = []
    for x in range(nx):
        for anchor_t in range(nt):
            value = sum(C[t * nx + x, anchor_t * nx + y]
                        for t in range(nt) for y in range(nx))
            green_errors.append(sp.simplify(value - 1 / alpha))
    assert all(err == 0 for err in green_errors)

    anchor_times = (0, 2)
    p = sp.zeros(dim, 1)
    for anchor_t in anchor_times:
        for y in range(nx):
            p[anchor_t * nx + y] = 1
    Q = sp.diag(*[1 - p[i] for i in range(dim)])
    c = C[0, 0]
    rhs = -c * (Q * C + C * Q) / 2

    # Solve (I kron K + K kron I) vec(C1)=vec(rhs) over Q exactly.
    lyap = sp.kronecker_product(sp.eye(dim), K) + sp.kronecker_product(K, sp.eye(dim))
    c1_vec = lyap.inv() * rhs.vec()
    C1 = sp.Matrix(dim, dim,
                   lambda i, j: c1_vec[i + j * dim])
    assert K * C1 + C1 * K == rhs
    assert C1 == C1.T

    # Exact algebraic DFT projections check every Fourier diagonal.
    modes = []
    for rt in range(nt):
        for rx in range(nx):
            z = sp.Matrix([
                sp.exp(2 * sp.pi * sp.I * (sp.Rational(rt * t, nt)
                                             + sp.Rational(rx * x, nx)))
                / sp.sqrt(dim)
                for t in range(nt) for x in range(nx)
            ])
            projected = sp.simplify(sp.expand_complex((sp.conjugate(z).T * C1 * z)[0]))
            eigenvalue = sp.simplify(
                alpha + 4 * kt * sp.sin(sp.pi * rt / nt) ** 2
                + 4 * kx * sp.sin(sp.pi * rx / nx) ** 2
            )
            expected = sp.simplify(-sp.Rational(1, 2) * c / eigenvalue**2)
            expected *= sp.Rational(nt - len(anchor_times), nt)
            error = sp.simplify(sp.expand_complex(projected - expected))
            assert error == 0, (rt, rx, error)
            modes.append({"time_mode": rt, "space_mode": rx,
                          "eigenvalue": str(eigenvalue),
                          "derivative_diagonal": str(projected)})

    # The same Green identity makes the deterministic positive-force bound sharp
    # for the zero-frequency Fourier amplitude in this linear resolvent case.
    b = sp.Rational(3, 5)
    anchor_force = sp.zeros(dim, 1)
    for i in range(dim):
        anchor_force[i] = -b * p[i]
    zmean = K.inv() * anchor_force
    target_x = 1
    fourier_amplitude = sp.simplify(
        sum(zmean[t * nx + target_x] for t in range(nt)) / sp.sqrt(nt)
    )
    claimed_bound = sp.simplify(b * len(anchor_times) / (alpha * sp.sqrt(nt)))
    assert abs(fourier_amplitude) == claimed_bound

    return {
        "grid": [nt, nx], "alpha": str(alpha), "anchor_times": anchor_times,
        "green_identity_checks": len(green_errors), "green_error": "0",
        "inverse_entries_nonnegative": True,
        "lyapunov_residual": "0", "fourier_modes_checked": len(modes),
        "modes": modes,
        "linear_resolvent_amplitude": str(fourier_amplitude),
        "linear_resolvent_bound": str(claimed_bound),
        "bound_is_sharp": True,
    }


def correlated_source_derivative():
    # Exact scalar OU family: X and Y have identical N(0, 1/k) marginals,
    # while Corr(X,Y)=rho. Different source correlations change the lambda
    # derivative of the anchored target variance.
    k = sp.Rational(3, 2)
    rows = []
    for rho in (sp.Rational(0), sp.Rational(1, 2), sp.Rational(1)):
        variance = 1 / k
        covariance = rho / k
        mixed_wick = 3 * variance * covariance  # E[Y^3 X]
        derivative = -mixed_wick / (6 * k)
        expected = -rho / (2 * k**3)
        assert sp.simplify(derivative - expected) == 0
        rows.append({"rho": str(rho), "target_variance_at_zero": str(variance),
                     "source_variance": str(variance),
                     "E_Y3X": str(mixed_wick),
                     "anchored_variance_derivative": str(derivative)})
    return rows


def continuum_scaling():
    # For a=beta/N and K=a*m^2 I + a^-1 L_cycle, bound the diagonal Green
    # function by the exact mode sum; this is the scale needed for coordinate
    # moments, unlike the crude operator bound alpha^-1.
    beta, mass = sp.Rational(2), sp.Rational(1)
    rows = []
    for n in (8, 16, 32, 64):
        a = beta / n
        lap = cycle_laplacian(n)
        K = a * mass**2 * sp.eye(n) + (1 / a) * lap
        c = sp.simplify(K.inv()[0, 0])
        assert c > 0
        rows.append({"N": n, "a": str(a), "alpha": str(a * mass**2),
                     "diagonal_green": str(c),
                     "scaled_physical_susceptibility_factor_a_over_alpha": str(a / (a * mass**2))})
    # Moment-only source counterexample to an unqualified continuum claim.
    # A stationary OU source with mean 1 and variance 1 has E[Y^3]=4. At
    # g=0, d E[F_0]/dg = -4/(alpha*sqrt(N)); this diverges when g is fixed.
    source_third_moment = sp.Integer(4)
    source_rows = []
    for n in (8, 16, 32, 64):
        a = beta / n
        K = a * mass**2 * sp.eye(n) + (1 / a) * cycle_laplacian(n)
        p = sp.zeros(n, 1)
        p[0] = 1
        derivative_mean = -source_third_moment * K.inv() * p
        fourier_derivative = sp.simplify(sum(derivative_mean) / sp.sqrt(n))
        expected_fixed_g = -source_third_moment * sp.sqrt(n) / beta
        expected_physical_g = -source_third_moment / (6 * mass**2 * sp.sqrt(n))
        assert sp.simplify(fourier_derivative - expected_fixed_g) == 0
        source_rows.append({"N": n, "d_EF_dg_fixed_g_parameter": str(fourier_derivative),
                            "d_EF_dlambda_for_g=a_lambda_over_6": str(
                                sp.simplify(a * fourier_derivative / 6)),
                            "fixed_g_growth_magnitude": str(source_third_moment * sp.sqrt(n) / beta),
                            "physical_g_vanishes": str(expected_physical_g)})
    # For standard action scaling g_N=a lambda/6 and uniformly bounded source/
    # target sixth moments, B_N=O(a), D_N=O(N^-1/2), while a times the raw
    # second-moment discrepancy bound is O(N^-1).
    return {"beta": str(beta), "mass": str(mass), "finite_values": rows,
            "analytic_diagonal_bound": "1/(beta*m^2) + 2*sum_{l>=1} 1/(beta*m^2+16*l^2/beta)",
            "stationary_source_counterexample": {
                "source": "stationary OU Y with mean 1 and variance 1, independent of target noise; E[Y^3]=4 and its sixth moment is finite",
                "finite_exact_derivatives": source_rows,
                "scope": "failure of an unqualified continuum extension when g is held fixed; not a failure of the fixed-alpha theorem"},
            "conditional_scaling": {
                "assumptions": ["g_N=O(a)", "uniform coordinate sixth moments for source and reference",
                                "fixed physical beta>0 and mass m>0"],
                "B_N": "O(a)", "D_N": "O(N^-1/2)",
                "raw_E_abs_F2_difference_bound": "O(1)",
                "physical_a_times_E_abs_F2_difference_bound": "O(N^-1)"}}


def main():
    result = {"scope": "independent exact rational/algebraic finite checks plus a conditional continuum scaling audit",
              "product_green_and_lyapunov": product_green_and_lyapunov(),
              "correlated_source_derivatives": correlated_source_derivative(),
              "continuum_scaling": continuum_scaling()}
    out = Path(__file__).parent / "exact_finite_audit.json"
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(out)
    print(json.dumps({"green_identity_checks": result["product_green_and_lyapunov"]["green_identity_checks"],
                      "fourier_modes_checked": result["product_green_and_lyapunov"]["fourier_modes_checked"],
                      "bound_is_sharp": result["product_green_and_lyapunov"]["bound_is_sharp"],
                      "correlated_source_derivatives": result["correlated_source_derivatives"],
                      "continuum_scaling": result["continuum_scaling"]["conditional_scaling"]}, indent=2))


if __name__ == "__main__":
    main()
