#!/usr/bin/env python3
"""Bounded exact Fourier experiment for the G contact and arbitrary backgrounds.

The script builds compatible gradients from three integer Fourier modes,
integrates all polynomial moments exactly by Laurent convolution, and reports
the full optimized Jensen gap and the contact-direction Schur complement.
It is evidence for this finite family only, not a proof of quasiconvexity.
"""
from __future__ import annotations

import json
from pathlib import Path

import sympy as s


Poly = dict[tuple[int, int], s.Expr]


def add(*items: Poly) -> Poly:
    out: Poly = {}
    for p in items:
        for k, v in p.items():
            out[k] = out.get(k, s.S.Zero) + v
    return {k: s.expand(v) for k, v in out.items() if v != 0}


def scale(p: Poly, c: s.Expr) -> Poly:
    return {k: s.expand(c * v) for k, v in p.items() if c * v != 0}


def mul(p: Poly, q: Poly) -> Poly:
    out: Poly = {}
    for (i, j), x in p.items():
        for (k, ell), y in q.items():
            key = (i + k, j + ell)
            out[key] = out.get(key, s.S.Zero) + x * y
    return {k: s.expand(v) for k, v in out.items() if v != 0}


def cosine(k: tuple[int, int]) -> Poly:
    return {k: s.Rational(1, 2), (-k[0], -k[1]): s.Rational(1, 2)}


def mean(p: Poly) -> s.Expr:
    return s.factor(p.get((0, 0), 0))


def substitute(poly: s.Expr, entries: list[Poly], variables: tuple[s.Symbol, ...]) -> Poly:
    """Evaluate a scalar polynomial on four exact Laurent polynomials."""
    out: Poly = {}
    expanded = s.Poly(s.expand(poly), *variables)
    for powers, coeff in expanded.terms():
        term: Poly = {(0, 0): coeff}
        for p, power in zip(entries, powers):
            for _ in range(power):
                term = mul(term, p)
        out = add(out, term)
    return out


a, b, c, d, eps = s.symbols("a b c d eps", real=True)
u, v, w, q = a*a + c*c, b*b + d*d, a*b + c*d, a*d - b*c
G = 3*(u + v - 2*q)**2 + s.Rational(35, 24)*u**2 + q**2 - s.Rational(5, 2)*q*u
variables = (a, b, c, d)
gradients = [s.diff(G, z) for z in variables]
Hessian = s.hessian(G, variables)


def run_family(modes: list[tuple[tuple[int, int], tuple[int, int, int, int], s.Expr]]) -> dict:
    entries: list[Poly] = [{} for _ in range(4)]
    for frequency, matrix, amplitude in modes:
        c_mode = scale(cosine(frequency), amplitude)
        for index, value in enumerate(matrix):
            entries[index] = add(entries[index], scale(c_mode, s.sympify(value)))
    bvec = [mean(substitute(g, entries, variables)) for g in gradients]
    hmat = s.Matrix([
        [mean(substitute(Hessian[i, j], entries, variables)) for j in range(4)]
        for i in range(4)
    ])
    cval = mean(substitute(G, entries, variables))
    # Background basis: A=I first, then its Euclidean orthogonal complement.
    A = s.Matrix([1, 0, 0, 1])
    W = [s.Matrix([0, 1, 0, 0]), s.Matrix([0, 0, 1, 0]), s.Matrix([1, 0, 0, -1])]
    basis = [A, *W]
    change = s.Matrix.hstack(*basis)
    hb = change.T * hmat * change
    bb = change.T * s.Matrix(bvec)
    D = hb[1:, 1:]
    k = hb[1:, 0]
    h = hb[0, 0]
    bA = bb[0]
    bW = bb[1:, 0]
    if s.det(D) == 0:
        raise AssertionError("transverse block unexpectedly singular")
    z = D.inv() * k
    ht = s.factor(h - (k.T * D.inv() * k)[0])
    bt = s.factor(bA - (k.T * D.inv() * bW)[0])
    reduced = s.factor(cval - (bW.T * D.inv() * bW)[0] / 2)
    bfull = s.Matrix(bvec)
    if s.factor(hmat.det()) != 0:
        quadratic = (bfull.T * hmat.inv() * bfull)[0]
    else:
        # Solve H z=b; the quadratic b.z is invariant across solutions because
        # nullspace closure puts b in range(H).
        solution, _parameters = hmat.gauss_jordan_solve(bfull)
        quadratic = (bfull.T * solution)[0]
    full_gap = s.factor(cval - quadratic / 2)
    fourth = mean(substitute((a*a+b*b+c*c+d*d)**2, entries, variables))
    out = {
        "covariance_rank": s.Matrix([
            [mean(mul(entries[i], entries[j])) for j in range(4)] for i in range(4)
        ]).rank(),
        "fourth_moment": s.factor(fourth),
        "c": s.factor(cval),
        "b": [s.factor(x) for x in bvec],
        "H": [[s.factor(hmat[i, j]) for j in range(4)] for i in range(4)],
        "H_principal_minors": [s.factor(hmat[:j, :j].det()) for j in range(1, 5)],
        "H_contact": s.factor(h),
        "H_cross": [s.factor(x) for x in k],
        "H_transverse_det": s.factor(s.det(D)),
        "H_schur_contact": ht,
        "b_contact": s.factor(bA),
        "b_transverse": [s.factor(x) for x in bW],
        "b_schur_contact": bt,
        "background_transverse_shift": [s.factor(x) for x in z],
        "gap_before_contact_elimination": reduced,
        "full_optimized_gap": full_gap,
        "negative_on_eps_positive": bool(s.factor(full_gap).is_negative),
    }
    return out


families = {
    "two_modes_independent": [
        ((0, 1), (0, 1, 0, 0), s.Integer(1)),  # e12 cos(y)
        ((1, 0), (1, 0, 0, 0), eps),            # e11 cos(x)
    ],
    "three_mode_resonant": [
        ((0, 1), (0, 1, 0, 0), s.Integer(1)),  # e12 cos(y)
        ((1, 0), (1, 0, 0, 0), eps),            # e11 cos(x)
        ((1, 1), (0, 0, 1, 1), eps),            # (e21+e22) cos(x+y)
    ],
    "rotating_one_frequency": [
        ((0, 1), (0, 1, 0, 0), s.Integer(1)),
        ((0, 1), (0, 0, 0, 1), eps),            # same wave, changed output vector
    ],
    "rotated_line_plus_tiny_independent_mode": [
        ((0, 1), (0, 1, 0, eps), s.Integer(1)), # rank-one line rotated by eps
        ((1, 0), (eps**2, 0, 0, 0), s.Integer(1)), # smaller independent mode
    ],
    "tangent_resonant_flatness": [
        # In physical coordinates these are frequencies (1,N), (2,N), (3,2N),
        # with eps=1/N. Their exact relation k1+k2=k3 gives a genuine cubic
        # resonance while all three rank-one matrices approach e12.
        ((1, 0), (eps, 1, s.Rational(3, 2)*eps**2, s.Rational(3, 2)*eps), s.Integer(1)),
        ((0, 1), (2*eps, 1, 6*eps**2, 3*eps), s.Integer(1)),
        ((1, 1), (s.Rational(3, 2)*eps, 1, s.Rational(27, 8)*eps**2, s.Rational(9, 4)*eps), s.Integer(1)),
    ],
}

for n in (2, 4, 8, 16):
    families[f"anisotropic_resonance_N{n}"] = [
        ((1, n), (s.Rational(1, n), 1, s.Rational(1, n*n), s.Rational(1, n)), s.Integer(1)),
        ((-1, n), (s.Rational(-1, n), 1, s.Rational(1, n*n), s.Rational(-1, n)), s.Integer(1)),
        ((0, 2*n), (0, 1, 0, 0), s.Integer(1)),
    ]

if __name__ == "__main__":
    results = {name: run_family(modes) for name, modes in families.items()}
    tangent = results["tangent_resonant_flatness"]
    eps4 = eps**4
    assert tangent["covariance_rank"] == 3
    assert s.factor(tangent["H_schur_contact"]).as_leading_term(eps) == s.Rational(74285, 4608)*eps4
    assert s.factor(tangent["b_contact"]).as_leading_term(eps) == -s.Rational(15, 8)*eps**3
    assert s.factor(tangent["b_schur_contact"]).as_leading_term(eps) == s.Rational(25, 64)*eps**3
    resonant_loss = s.factor(tangent["b_schur_contact"]**2/(2*tangent["H_schur_contact"]))
    assert resonant_loss.as_leading_term(eps) == s.Rational(1125, 237712)*eps**2
    assert s.limit(tangent["full_optimized_gap"], eps, 0) == s.Rational(111, 8)
    for minor in tangent["H_principal_minors"]:
        assert all(coefficient > 0 for coefficient in s.Poly(minor, eps).all_coeffs() if coefficient != 0)
    for polynomial in s.fraction(tangent["full_optimized_gap"]):
        assert all(coefficient > 0 for coefficient in s.Poly(polynomial, eps).all_coeffs() if coefficient != 0)

    rotated = results["rotated_line_plus_tiny_independent_mode"]
    assert s.limit(rotated["H_schur_contact"]/eps**4, eps, 0) == s.Rational(9, 4)
    assert s.limit(rotated["H_schur_contact"]/rotated["H_contact"], eps, 0) == 0
    assert s.limit(rotated["full_optimized_gap"], eps, 0) == s.Rational(9, 8)
    for minor in rotated["H_principal_minors"]:
        assert all(coefficient > 0 for coefficient in s.Poly(minor, eps).all_coeffs() if coefficient != 0)

    single_rotation = results["rotating_one_frequency"]
    assert single_rotation["H_schur_contact"] == 0
    assert single_rotation["full_optimized_gap"] == 9*(eps**2 + 1)**2/8
    for name, item in results.items():
        print(name)
        for key in ("covariance_rank", "fourth_moment", "H_contact", "H_cross",
                    "H_schur_contact", "b_contact", "b_schur_contact",
                    "gap_before_contact_elimination", "full_optimized_gap"):
            print(f"  {key}: {item[key]}")

    Path(__file__).with_name("near_contact_modes.json").write_text(
        json.dumps(results, indent=2, default=str) + "\n"
    )
    checks = {
        "exact_tangent_resonance": {
            "covariance_rank": tangent["covariance_rank"],
            "H_principal_minor_coefficients_positive": True,
            "h_star_over_eps4": "74285/4608",
            "beta_star_over_eps3": "25/64",
            "reduced_loss_over_eps2": "1125/237712",
            "optimized_gap_limit": "111/8",
        },
        "rotated_line_plus_small_independent_mode": {
            "h_star_over_eps4": "9/4",
            "h_star_over_h_limit": "0",
            "optimized_gap_limit": "9/8",
        },
        "single_rotated_rank_one_mode": {
            "h_star": "0",
            "optimized_gap": str(single_rotation["full_optimized_gap"]),
        },
    }
    Path(__file__).with_name("near_contact_checks.json").write_text(
        json.dumps(checks, indent=2) + "\n"
    )
