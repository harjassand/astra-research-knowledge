#!/usr/bin/env python3
"""Exact discriminants for the equality-rigidity theorem in RIGIDITY.md.

Reads only the supplied angular case. New output is written next to this file.
Uses SymPy for exact polynomial remainder computations. The source receiver is
replayed, unchanged, as an internal premise check, not as independent review.
"""
from fractions import Fraction
from pathlib import Path
import json
import os
import subprocess
import sys

import sympy as s

HERE = Path(__file__).resolve().parent
CASE = HERE.parents[1] / "cases" / "angular"
b, d, t, h, u = s.symbols("b d t h u", real=True)


def literal(rows):
    return s.expand(sum(s.Rational(n, m) * b**i * d**j
                        for i, j, n, m in rows))


def seed_geometry(filename, kappa, sigma):
    data = json.loads((CASE / filename).read_text())
    w, g = literal(data["w"]), literal(data["g"])
    ideal = s.groebner([w, g], b, d)
    kernel = [literal(row) for row in data["kernel"]]
    C = s.Matrix([[literal(row) for row in entry]
                  for entry in data["matrices"]["C"]["entries"]])
    rem = lambda polynomial: s.factor(ideal.reduce(s.expand(polynomial))[1])

    # The literal Hessian null vector is an actual acoustic, rank-one tensor:
    # v=(1,k3), xi=(1,k1), h_ij^a=v_a xi_i xi_j modulo the zero ideal.
    acoustic = [kernel[2] - kernel[1]**2,
                kernel[4] - kernel[1]*kernel[3],
                kernel[5] - kernel[2]*kernel[3]]
    assert all(rem(x) == 0 for x in acoustic)
    assert all(rem(x) == 0 for x in C * s.Matrix(kernel))

    T, X, Y, Z = 1 + b*b + d*d, 1 - b*b - d*d, 2*b, 2*d
    assert rem(X - kappa*Z) == 0
    assert rem(Z*Z - sigma*T*T) == 0
    eta2 = s.factor(1 - (1+kappa*kappa)*sigma)
    assert eta2 > 0 and sigma > 0
    assert 1 - kappa*kappa*sigma > 0
    assert s.discriminant(g, d) > 0
    assert s.resultant(g, 1-d*d-2*kappa*d, d) != 0

    # A Hopf fibre is z2=rho*z1. Its real-linear parametrisation has
    # determinant Im(rho)*(x*x+y*y), hence contains no nonzero rank-one A.
    x, y, p, q = s.symbols("x y p q", real=True)
    fibre = s.Matrix([[x, p*x-q*y], [y, q*x+p*y]])
    assert s.expand(fibre.det()-q*(x*x+y*y)) == 0

    # Replay the unchanged acquired primitive, full factorisation, orientation
    # identities, finite cover and Bernstein positivity. Explicit seed argument
    # prevents the receiver from writing its default output into the case.
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    replay = subprocess.run(
        [sys.executable, str(CASE / "receive_boundary.py"),
         str(CASE / filename)], check=True, capture_output=True, text=True,
        cwd=HERE, env=env)
    replay_data = json.loads(replay.stdout)
    assert replay_data["all_signs_exact"]
    return {
        "beta": data["beta"], "r": data["r"],
        "kappa": str(kappa), "sigma": str(sigma),
        "nY_squared": str(eta2),
        "determinant_to_norm_squared_squared": str(sigma/4),
        "literal_C_kernel_remainders": ["0"]*6,
        "rank_one_Hessian_remainders": ["0"]*3,
        "zero_ideal_Hopf_remainders": ["0"]*2,
        "g_discriminant": str(s.discriminant(g, d)),
        "nonzero_b_square_resultant": str(s.resultant(g, 1-d*d-2*kappa*d, d)),
        "internal_source_replay": replay_data,
    }


def quartic_wave():
    # This integer-scaled K is the governing arc construction at tau=1/30.
    # Scaling K does not change an acoustic zero. The positive small root t of
    # m gives a real nonzero gradient K with rank-one direction R=(1,t;0,0).
    m = 2710*t**4 - 83981*t*t + 2710
    K = s.Matrix([
        -299*(10+291*t*t)*(1+t*t),
        299*t*(291+10*t*t)*(1+t*t),
        89401*t*(1-t*t) - 3010*t*(1+t*t)**2,
        89401*t*t*(1-t*t) + 3010*(1+t*t)**2,
    ])
    R = s.Matrix([1, t, 0, 0])
    beta, r = s.Rational(299, 301), s.Rational(1084, 301)

    def energy(A):
        a, bb, c, dd = A
        T = a*a+bb*bb+c*c+dd*dd
        q = a*dd-bb*c
        X = a*a+c*c-bb*bb-dd*dd
        return T*T + 4*(r-1)*q*q + 4*beta*q*X

    line = s.Poly(s.expand(energy(K+h*R)), h)
    rem = lambda p: s.factor(s.rem(s.Poly(p, t), s.Poly(m, t)).as_expr())
    c2, c3 = [rem(line.coeff_monomial(h**j)) for j in [2, 3]]
    c4 = s.factor(line.coeff_monomial(h**4))
    assert c2 == c3 == 0
    assert s.expand(c4-(1+t*t)**2) == 0
    T = sum(z*z for z in K)
    X, Z = K[0]**2+K[2]**2-K[1]**2-K[3]**2, 2*(K[0]*K[3]-K[1]*K[2])
    assert rem(X-s.Rational(20, 299)*Z) == 0
    assert rem(Z*Z-s.Rational(78561, 78961)*T*T) == 0
    Delta = 83981**2 - 4*2710**2
    t_small = s.sqrt((83981-s.sqrt(Delta))/5420)
    assert Delta > 0 and s.Rational(83981) > s.sqrt(Delta)
    return {
        "acoustic_polynomial": str(m),
        "positive_small_root": str(t_small),
        "positive_small_root_decimal": str(s.N(t_small, 18)),
        "gradient_K_integer_polynomials": [str(s.expand(z)) for z in K],
        "rank_one_direction": [["1", "t"], ["0", "0"]],
        "squared_amplitude_coefficient_mod_m": str(c2),
        "cubed_amplitude_coefficient_mod_m": str(c3),
        "fourth_amplitude_coefficient": str(c4),
        "mean_cosine_fourth_power": "3/8",
        "exact_normalized_periodic_gap": "(3/8)*epsilon^4*(1+t^2)^2",
        "consequence": "No positive quadratic strong-QC bound at this base; strict quartic-order gap for this wave.",
    }


def arc_geometry():
    B, H = 1-3*u*u, 1+3*u*u
    kappa = 2*u/B
    mu = (1-4*u+3*u*u)/H
    sigma = s.factor(4*mu/(1+mu)**2)
    eta2 = s.factor(1-(1+kappa*kappa)*sigma)
    expected = 16*u**3*(3*u*u-3*u+1)/((3*u*u-1)**2*(3*u*u-2*u+1)**2)
    assert s.factor(eta2-expected) == 0
    # 3u^2-3u+1=3(u-1/2)^2+1/4 > 0.
    assert s.expand(3*(u-s.Rational(1,2))**2+s.Rational(1,4)) == 3*u*u-3*u+1
    assert s.factor(sigma.subs(u, s.Rational(1,30))) == s.Rational(78561,78961)
    assert s.factor(eta2.subs(u, s.Rational(1,30))) == s.Rational(4336000,7059192361)
    assert s.factor(sigma.subs(u, s.Rational(1,6))) == s.Rational(65,81)
    # The accepted radius is contained in (0,1/3), so these exact positivity
    # formulas apply throughout that already-certified arc.
    radius = Fraction(1, 2**206)
    assert Fraction(1,30)-radius > 0
    assert Fraction(1,30)+radius < Fraction(1,3)
    return {
        "sigma": str(sigma), "nY_squared": str(eta2),
        "four_real_rank_one_free_Hopf_planes_for": "0 < tau < 1/3",
        "quasiconvex_arc_inherited_scope": "abs(tau-1/30) < 2^(-206)",
        "scope": "The geometric formula alone does not establish quasiconvexity outside the accepted arc and seeds.",
    }


def main():
    output = {
        "theorem": "Finite rank-one-free singular planes imply strict quasiconvexity of a heat/exact-form-certified quartic.",
        "seed_B0": seed_geometry("seed_11_13.json", s.Rational(4,11), s.Rational(65,81)),
        "seed_B1": seed_geometry("seed_299_301.json", s.Rational(20,299), s.Rational(78561,78961)),
        "quartic_order_acoustic_wave": quartic_wave(),
        "arc_geometry": arc_geometry(),
        "proof_obligation_outside_executable_scope": "The real-analytic heat-flow and Fourier-rigidity proof is in RIGIDITY.md. No uniform L4 modulus or gradient-Young-measure rigidity is inferred.",
    }
    path = HERE / "rigidity_results.json"
    path.write_text(json.dumps(output, indent=2)+"\n")
    print(json.dumps({"output": str(path), "all_exact_assertions_passed": True,
                      "source_coefficient_matrices_replayed":
                      output["seed_B0"]["internal_source_replay"]["positive_coefficient_matrices"]
                      + output["seed_B1"]["internal_source_replay"]["positive_coefficient_matrices"]}, indent=2))


if __name__ == "__main__":
    main()
