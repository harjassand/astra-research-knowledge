"""Finite checks for the Gaussian PPT cone obstruction.

These checks verify conventions, exact rejected witnesses, and finite channel
certificates. They do not certify a global Schmidt-rank optimization or the
large-dimension existence theorem. The all-dimension argument is in PROOF.md.
Dependencies: numpy, sympy. Run from any directory with Python 3.
"""

from __future__ import annotations

import hashlib
import json
import math
import platform
import sys
from pathlib import Path

import numpy as np
import sympy as sp


def pt(x, d):
    return x.reshape(d, d, d, d).transpose(0, 3, 2, 1).reshape(d*d, d*d)


def partial_a(x, d):
    return np.einsum("iaib->ab", x.reshape(d, d, d, d))


def partial_b(x, d):
    return np.einsum("iaj a->ij".replace(" ", ""), x.reshape(d, d, d, d))


def interaction_projection(x, d):
    ident = np.eye(d)
    return (
        x - np.kron(partial_b(x, d), ident)/d
        - np.kron(ident, partial_a(x, d))/d
        + np.trace(x)*np.eye(d*d)/(d*d)
    )


def gue(dimension, rng):
    # Standard real Gaussian in Hermitian matrices for Tr(XY) inner product.
    raw = rng.normal(size=(dimension, dimension)) + 1j*rng.normal(size=(dimension, dimension))
    return (raw + raw.conj().T)/2


def choi_to_superoperator(x, d):
    return x.reshape(d, d, d, d).transpose(1, 3, 0, 2).reshape(d*d, d*d)


def superoperator_to_choi(x, d):
    return x.reshape(d, d, d, d).transpose(2, 0, 3, 1).reshape(d*d, d*d)


def exact_symplectic_rejection(d=6, k=2):
    half = d//2
    omega = sp.zeros(d)
    for i in range(half):
        omega[i, half+i] = 1
        omega[half+i, i] = -1
    flip = sp.zeros(d*d)
    for i in range(d):
        for j in range(d):
            flip[j*d+i, i*d+j] = 1
    maximally_entangled = sp.zeros(d*d, 1)
    for i in range(d):
        maximally_entangled[i*d+i] = 1
    # dP is the unnormalized maximally entangled projector.
    d_p = maximally_entangled*maximally_entangled.T
    local = sp.kronecker_product(sp.eye(d), omega)
    twisted_flip = local*flip*local.T
    w = k*sp.eye(d*d) - d_p - k*twisted_flip
    w_pt = sp.zeros(d*d)
    for i in range(d):
        for a in range(d):
            for j in range(d):
                for b in range(d):
                    w_pt[i*d+a, j*d+b] = w[i*d+b, j*d+a]
    # A Bell vector on a symplectic pair has Schmidt rank two.
    v = sp.zeros(d*d, 1)
    v[half] = 1/sp.sqrt(2)
    v[half*d] = -1/sp.sqrt(2)
    value = sp.simplify((v.T*w_pt*v)[0])
    original = sp.simplify((v.T*w*v)[0])
    assert value == 1-k
    assert original == 0
    return {"dimension": d, "k": k, "schmidt_rank": 2,
            "original_expectation": str(original), "partial_transpose_expectation": str(value),
            "conclusion": "The k-Breuer-Hall witness fails even 2-copositivity for k>=2."}


def convention_checks(rng):
    d = 3
    x = gue(d*d, rng)
    y = gue(d*d, rng)
    g = interaction_projection(x, d)
    tolerance = 1e-11
    checks = {
        "partial_transpose_involution": np.linalg.norm(pt(pt(x, d), d)-x),
        "partial_transpose_hs_adjoint": abs(np.trace(x@pt(y, d))-np.trace(pt(x, d)@y)),
        "interaction_projection_idempotent": np.linalg.norm(interaction_projection(g, d)-g),
        "projection_hs_orthogonal": abs(np.trace(g@(x-g))),
        "zero_input_partial_trace": np.linalg.norm(partial_b(g, d)),
        "zero_output_partial_trace": np.linalg.norm(partial_a(g, d)),
        "projection_commutes_with_pt": np.linalg.norm(interaction_projection(pt(x, d), d)-pt(g, d)),
        "reshuffle_inverse": np.linalg.norm(superoperator_to_choi(choi_to_superoperator(x,d),d)-x),
        "reshuffle_hs_isometry": abs(np.linalg.norm(choi_to_superoperator(x,d))-np.linalg.norm(x)),
    }
    assert all(value < tolerance for value in checks.values()), checks
    return {key: float(value) for key, value in checks.items()}


def finite_channel_check(d, seed):
    rng = np.random.default_rng(seed)
    g = interaction_projection(gue(d*d, rng), d)
    ident = np.eye(d*d)
    rho = (ident+g/(9*d))/(d*d)
    choi = d*rho
    delta = choi_to_superoperator(ident/d, d)
    e = choi_to_superoperator(g, d)/(9*d*d)
    channel = delta+e
    square = superoperator_to_choi(channel@channel, d)
    square_perturbation = np.linalg.norm(square-ident/d)
    e_operator = np.linalg.norm(e, ord=2)
    e_frobenius = np.linalg.norm(e)
    norm_bound = e_operator*e_frobenius
    diagnostics = {
        "dimension": d,
        "seed": seed,
        "rho_min_eigenvalue": float(np.linalg.eigvalsh(rho).min()),
        "rho_pt_min_eigenvalue": float(np.linalg.eigvalsh(pt(rho, d)).min()),
        "trace_error": float(abs(np.trace(rho)-1)),
        "tp_error": float(np.linalg.norm(partial_b(choi,d)-np.eye(d))),
        "unital_error": float(np.linalg.norm(partial_a(choi,d)-np.eye(d))),
        "delta_e_error": float(np.linalg.norm(delta@e)),
        "e_delta_error": float(np.linalg.norm(e@delta)),
        "square_choi_error": float(np.linalg.norm(square-(ident/d+superoperator_to_choi(e@e,d)))),
        "square_choi_hs_distance": float(square_perturbation),
        "upper_bound_e_operator_times_frobenius": float(norm_bound),
        "separable_ball_radius": 1/d,
        "square_has_separable_ball_certificate": bool(norm_bound < 1/d),
        "gaussian_hs_squared": float(np.linalg.norm(g)**2),
        "gaussian_hs_squared_expectation": (d*d-1)**2,
        "global_low_schmidt_certificate": "NOT COMPUTED",
    }
    assert diagnostics["rho_min_eigenvalue"] > 0
    assert diagnostics["rho_pt_min_eigenvalue"] > 0
    for key in ("trace_error", "tp_error", "unital_error", "delta_e_error", "e_delta_error", "square_choi_error"):
        assert diagnostics[key] < 1e-10, (key, diagnostics)
    assert square_perturbation <= norm_bound + 1e-10
    assert norm_bound < 1/d
    return diagnostics


def constant_checks():
    # Integer arithmetic validates the sufficient dimension fraction.
    lhs = 5*48**2*36**2
    rhs = 2**24
    assert lhs < rhs
    # Chaining coefficients: log7<2, log2<.7, sqrt5<9/4, sqrt3<7/4.
    coefficient = sp.Rational(3) + 6*(sp.Rational(9,4)+2*sp.Rational(7,4))
    tail_coefficient = sp.Rational(3,2)+6
    assert coefficient < 40 and tail_coefficient < 8
    # Lower chi-square tail: log2 >= 2/3 and D>=16.
    lower_exponent = sp.Rational(225,512)*sp.Rational(2,3)-sp.Rational(1,4)
    assert lower_exponent >= sp.Rational(1,32)
    assert sp.Rational(32,81) < 1
    # Quantitative separation from the normalized DSP cone.
    separation = (sp.Rational(1,18)-sp.Rational(1,36))/8/2
    assert separation == sp.Rational(1,576)
    # Finite orbit extension constants.
    orbit_leading = 48*math.sqrt(5/(2**26))+8/math.sqrt(2**20)
    assert orbit_leading < 1/36
    return {
        "dimension_fraction": "2^-24",
        "constant_integer_lhs": lhs,
        "constant_integer_rhs": rhs,
        "chaining_coefficient_upper": str(coefficient),
        "chaining_tail_coefficient_upper": str(tail_coefficient),
        "chi_square_exponent_lower": str(lower_exponent),
        "half_trace_distance_lower": str(separation),
        "square_ball_margin": str(1-sp.Rational(32,81)),
        "finite_orbit_leading_bound": orbit_leading,
    }


def main():
    result = {
        "scope": "Exact algebra and finite numerical convention/channel checks; no finite-sample proof of the all-dimension theorem.",
        "environment": {"python": sys.version, "numpy": np.__version__, "sympy": sp.__version__, "platform": platform.platform()},
        "constants": constant_checks(),
        "exact_rejected_witness": exact_symplectic_rejection(),
        "conventions": convention_checks(np.random.default_rng(197252)),
        "finite_channels": [finite_channel_check(d, 2026100800+d) for d in (2, 3, 4, 8, 12, 16)],
        "unverified": ["Numerical maximization over all Schmidt-rank-k vectors", "Explicit matrix at d>=2^24", "Historical priority", "External specialist review", "Proof assistant formalization"],
    }
    output = Path(__file__).with_name("CHECK_RESULTS.json")
    output.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({"checks": "PASS", "exact_rejected_witness": result["exact_rejected_witness"],
                      "finite_dimensions": [x["dimension"] for x in result["finite_channels"]],
                      "all_finite_square_certificates": all(x["square_has_separable_ball_certificate"] for x in result["finite_channels"]),
                      "results": str(output.resolve()), "scope": result["scope"]}, indent=2))


if __name__ == "__main__":
    main()
