#!/usr/bin/env python3
"""Exact local verification for the output-matrix heat obstruction.

The polynomial maps used below encode local jets. They are not integrated over
R^2. The compact cutoff, semigroup, and integration arguments are proved in
ANALYTIC_PROOF.md, and are deliberately not labelled mechanically formalized.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
from datetime import datetime, timezone
from pathlib import Path

import sympy as sp


def zero(expression: sp.Expr) -> bool:
    return sp.expand(expression) == 0


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("VERIFICATION.json"))
    args = parser.parse_args()
    x, y, tau, eps, s = sp.symbols("x y tau eps s", real=True)
    coordinates = (x, y)
    origin = {x: 0, y: 0}
    spatial_pairs = ((0, 0), (0, 1), (1, 1))
    C = {
        pair: sp.Matrix(2, 2, lambda alpha, beta: sp.Symbol(
            f"C{pair[0]+1}{pair[1]+1}_{alpha+1}{beta+1}", real=True
        ))
        for pair in spatial_pairs
    }
    coefficient_symbols = [entry for pair in spatial_pairs for entry in C[pair]]

    def coefficient(i: int, j: int) -> sp.Matrix:
        return C[tuple(sorted((i, j)))]

    def generator(u: sp.Matrix) -> sp.Matrix:
        return sp.Matrix([
            sp.expand(sum(
                coefficient(i, j)[alpha, beta] * sp.diff(u[beta], coordinates[i], coordinates[j])
                for beta in range(2) for i in range(2) for j in range(2)
            ))
            for alpha in range(2)
        ])

    def jacobian(u: sp.Matrix) -> sp.Matrix:
        return u.jacobian(coordinates)

    def determinant_velocity(u: sp.Matrix) -> sp.Expr:
        return sp.expand(sp.diff(jacobian(u + tau * generator(u)).det(), tau).subs(tau, 0))

    checks: dict[str, bool] = {}
    f_abstract = sp.Function("f")(x, y)
    checks["rank_one_initial_map_for_arbitrary_f"] = zero(jacobian(sp.Matrix([f_abstract, f_abstract**2])).det())

    f = x + x*y
    u = sp.Matrix([f, f**2])
    A = jacobian(u)
    w = generator(u)
    W = jacobian(w)
    J_velocity = determinant_velocity(u)
    point_velocity = sp.expand(J_velocity.subs(origin))
    checks["constant_output_matrix_velocity"] = zero(point_velocity - 4*C[(0, 0)][1, 1])
    checks["all_other_constant_coefficients_cancel"] = all(
        zero(sp.diff(point_velocity, c))
        for c in coefficient_symbols if c != C[(0, 0)][1, 1]
    )
    checks["mixed_spatial_term_counted_twice"] = generator(sp.Matrix([x*y, 0])) == 2*C[(0, 1)][:, 0]
    initial_jacobian = A.subs(origin)
    expected_jacobian = sp.Matrix([[1, 0], [0, 0]])
    checks["initial_jacobian_at_origin"] = initial_jacobian == expected_jacobian

    # Strong parabolicity is an analytic inequality. This verifies exactly the
    # rank-one symbol evaluation to which that inequality is applied.
    output_test = sp.Matrix([0, 1])
    input_test = sp.Matrix([1, 0])
    symbol_value = sum(
        output_test[alpha]*coefficient(i, j)[alpha, beta]*output_test[beta]*input_test[i]*input_test[j]
        for alpha in range(2) for beta in range(2) for i in range(2) for j in range(2)
    )
    checks["coercivity_test_is_C11_22"] = zero(symbol_value-C[(0, 0)][1, 1])

    # The local second time-energy derivative is 2 J_velocity^2 when J_0=0.
    second_velocity = generator(w)
    jet_path = u + tau*w + tau**2*second_velocity/2
    F_jet_path = sp.expand(jacobian(jet_path).det()**2)
    checks["pointwise_energy_first_time_derivative_zero"] = zero(sp.diff(F_jet_path, tau).subs(tau, 0))
    checks["pointwise_energy_second_time_derivative"] = zero(
        sp.diff(F_jet_path, tau, 2).subs(tau, 0)-2*J_velocity**2
    )

    # Purely compact-test argument: v_s=u+sLu. Its instantaneous energy
    # derivative under L has derivative 2 J_velocity^2 at s=0, pointwise.
    v_s = u+s*w
    B_s = jacobian(v_s)
    B_s_velocity = jacobian(generator(v_s))
    instantaneous_density = sp.expand(2*B_s.det()*sum(
        B_s.cofactor_matrix()[alpha, k]*B_s_velocity[alpha, k]
        for alpha in range(2) for k in range(2)
    ))
    checks["compact_test_density_zero_at_s_zero"] = zero(instantaneous_density.subs(s, 0))
    checks["compact_test_density_linear_coefficient"] = zero(
        sp.diff(instantaneous_density, s).subs(s, 0)-2*J_velocity**2
    )

    # Independently regenerate the generalized Hessian dissipation and its
    # integration-by-parts identity for the polynomial family v_s.
    a_entries = sp.symbols("A11 A12 A21 A22", real=True)
    a_matrix = sp.Matrix(2, 2, a_entries)
    energy = a_matrix.det()**2
    gradient = [sp.diff(energy, entry) for entry in a_entries]
    hessian = sp.hessian(energy, a_entries)
    substitution = {a_entries[2*alpha+k]: B_s[alpha, k] for alpha in range(2) for k in range(2)}
    Q = sum(
        hessian[2*alpha+k, 2*gamma+ell].subs(substitution)
        *coefficient(i, j)[alpha, beta]
        *sp.diff(B_s[gamma, ell], coordinates[i])
        *sp.diff(B_s[beta, k], coordinates[j])
        for alpha in range(2) for beta in range(2)
        for gamma in range(2) for k in range(2) for ell in range(2)
        for i in range(2) for j in range(2)
    )
    flux_divergence = sum(
        sp.diff(sum(
            gradient[2*alpha+k].subs(substitution)*coefficient(i, j)[alpha, beta]
            *sp.diff(B_s[beta, k], coordinates[j])
            for alpha in range(2) for beta in range(2) for k in range(2) for j in range(2)
        ), coordinates[i])
        for i in range(2)
    )
    checks["generalized_dissipation_divergence_identity"] = zero(instantaneous_density+Q-flux_divergence)

    # Three curve-image jets isolate all 12 effective constant coefficients.
    a1, a2, b1, b2 = sp.symbols("a1 a2 b1 b2", real=True)
    tangent = sp.Matrix([a1, a2])
    curvature = sp.Matrix([b1, b2])
    scalar_jets = {
        "C11": (x+x*y, C[(0, 0)], 2),
        "C12": (x+y**2/2, C[(0, 1)], 2),
        "C22": (y+x*y, C[(1, 1)], -2),
    }
    classification_equations = []
    classification_formulas = {}
    for label, (scalar_jet, matrix, factor) in scalar_jets.items():
        curve_map = tangent*scalar_jet+curvature*scalar_jet**2/2
        velocity = sp.expand(determinant_velocity(curve_map).subs(origin))
        expected = factor*sp.Matrix.hstack(tangent, matrix*curvature).det()
        checks[f"classification_jet_{label}"] = zero(velocity-expected)
        checks[f"classification_initial_rank_one_{label}"] = zero(jacobian(curve_map).det())
        classification_formulas[label] = sp.sstr(expected)
        classification_equations.extend(sp.Poly(velocity, a1, a2, b1, b2).coeffs())
    classification_matrix, classification_rhs = sp.linear_eq_to_matrix(classification_equations, coefficient_symbols)
    classification_rank = classification_matrix.rank()
    solution = sp.linsolve((classification_matrix, classification_rhs), coefficient_symbols)
    checks["classification_linear_system_full_rank"] = classification_rank == 12
    checks["classification_only_zero_coefficients"] = solution == sp.FiniteSet(sp.Tuple(*([0]*12)))

    # General C1 adaptive coefficients are determined here by their exact
    # value and first derivative at A_eps. An affine expression represents
    # that arbitrary first jet; no affine restriction is made in the theorem.
    u_eps = eps*u
    A_eps_field = jacobian(u_eps)
    A_eps_point = A_eps_field.subs(origin)
    adaptive = {}
    DC = {}
    for pair in spatial_pairs:
        for alpha in range(2):
            for beta in range(2):
                key = (pair, alpha, beta)
                derivatives = [sp.Symbol(
                    f"DC{pair[0]+1}{pair[1]+1}_{alpha+1}{beta+1}_A{k//2+1}{k%2+1}", real=True
                ) for k in range(4)]
                DC[key] = derivatives
                adaptive[key] = C[pair][alpha, beta] + sum(
                    derivatives[2*gamma+k]*(A_eps_field[gamma, k]-A_eps_point[gamma, k])
                    for gamma in range(2) for k in range(2)
                )
    adaptive_generator = sp.Matrix([
        sum(
            adaptive[(tuple(sorted((i, j))), alpha, beta)]
            *sp.diff(u_eps[beta], coordinates[i], coordinates[j])
            for beta in range(2) for i in range(2) for j in range(2)
        )
        for alpha in range(2)
    ])
    adaptive_velocity = sp.expand(sp.diff(
        jacobian(u_eps+tau*adaptive_generator).det(), tau
    ).subs(tau, 0).subs(origin))
    adaptive_expected = (
        4*eps**2*C[(0, 0)][1, 1]
        +2*eps**3*(DC[((0, 1), 1, 0)][0]+DC[((0, 0), 1, 1)][0])
    )
    checks["adaptive_exact_first_jet_formula"] = zero(adaptive_velocity-adaptive_expected)
    checks["adaptive_transverse_gradient_jet"] = A_eps_field.diff(y).subs(origin) == sp.Matrix([[eps, 0], [0, 0]])
    checks["adaptive_transverse_state_jet_zero"] = u_eps.diff(y).subs(origin) == sp.zeros(2, 1)

    # Finite-dimensional consistency checks for the all-square-dimensions
    # corollary. The proof for every n>=2 is the cofactor calculation in the
    # report; these finite checks do not replace that proof.
    dimensional_velocities = {}
    for n in (2, 3, 4):
        z = sp.symbols(f"z1:{n+1}", real=True)
        local_f = z[0]+z[0]*z[1]
        local_u = sp.Matrix([local_f, local_f**2, *z[2:]])
        jac = local_u.jacobian(z)
        evaluation = dict.fromkeys(z, 0)
        cof = jac.subs(evaluation).cofactor_matrix()
        directional_velocity = 0
        for alpha in range(n):
            for k in range(n):
                if cof[alpha, k] == 0:
                    continue
                term = 0
                for beta in range(n):
                    for i in range(n):
                        for j in range(n):
                            third_jet = sp.diff(local_u[beta], z[i], z[j], z[k]).subs(evaluation)
                            if third_jet != 0:
                                lo, hi = sorted((i+1, j+1))
                                c = sp.Symbol(f"N{n}C{lo}{hi}_{alpha+1}{beta+1}", real=True)
                                term += c*third_jet
                directional_velocity += cof[alpha, k]*term
        target = 4*sp.Symbol(f"N{n}C11_22", real=True)
        checks[f"dimension_{n}_determinant_velocity"] = zero(directional_velocity-target)
        checks[f"dimension_{n}_initial_determinant_zero"] = zero(jac.det())
        dimensional_velocities[str(n)] = sp.sstr(directional_velocity)

    report = {
        "schema": "astra-output-matrix-heat-exact-verification-v1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "python": platform.python_version(),
        "sympy": sp.__version__,
        "verifier_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "number_of_checks": len(checks),
        "constant_coefficient_velocity_at_origin": sp.sstr(point_velocity),
        "adaptive_exact_velocity_at_origin": sp.sstr(adaptive_velocity),
        "adaptive_coefficient_convention": "C values and DC derivatives are evaluated at A_eps=eps E11",
        "classification_formulas": classification_formulas,
        "classification_coefficient_system_rank": classification_rank,
        "classification_number_of_effective_coefficients": len(coefficient_symbols),
        "dimensional_cross_checks": dimensional_velocities,
        "analytic_obligations_not_mechanically_formalized": [
            "existence of a smooth compact cutoff equal to one near the origin",
            "constant strongly parabolic Fourier semigroup and smooth time differentiability",
            "differentiation and integration by parts for compact or Schwartz maps",
            "strict integral positivity from a continuous nonzero determinant velocity",
            "small-amplitude asymptotics for arbitrary C1 adaptive coefficients",
            "general all-dimensions cofactor proof",
            "historical novelty and independent external correctness review"
        ],
        "scope": "Exact symbolic jet and polynomial identities; not formal proof verification or novelty clearance."
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True)+"\n")
    print(json.dumps({"status": report["status"], "checks": len(checks), "output": str(args.output)}, sort_keys=True))
    if not all(checks.values()):
        failed = [name for name, passed in checks.items() if not passed]
        raise SystemExit("Failed checks: "+", ".join(failed))


if __name__ == "__main__":
    main()
