#!/usr/bin/env python3
"""Independent exact checks for the profile-circulation source.

This implementation does not import the supplied profile_algebra helpers. It
uses direct line integration for path moments and a cos(2y) reduction for the
opposite-carrier strip action.
"""
from __future__ import annotations

from fractions import Fraction as Q
from itertools import product
from math import comb
from pathlib import Path
import json
import hashlib

import sympy as sp

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "source-copy"


def square_loop(x=Q(0), y=Q(0), side=Q(1), reverse=False):
    vertices = [
        (x, y),
        (x + side, y),
        (x + side, y + side),
        (x, y + side),
        (x, y),
    ]
    return list(reversed(vertices)) if reverse else vertices


def finite_difference_path(step=Q(2)):
    """Realize Gamma - 3T_v Gamma + 3T_2v Gamma - T_3v Gamma."""
    base = (Q(0), Q(0))
    vertices = [base]
    for j, coefficient in enumerate((1, -3, 3, -1)):
        loop = square_loop(step * j, Q(0), Q(1), reverse=coefficient < 0)
        for _ in range(abs(coefficient)):
            if vertices[-1] != loop[0]:
                vertices.append(loop[0])
            vertices.extend(loop[1:])
            if vertices[-1] != base:
                vertices.append(base)
    return vertices


def linear_monomial_integral(x0, y0, dx, dy, i, j):
    """Integrate (x0+t dx)^i (y0+t dy)^j over t in [0,1]."""
    total = Q(0)
    for a in range(i + 1):
        for b in range(j + 1):
            total += (
                Q(comb(i, a) * comb(j, b), a + b + 1)
                * x0 ** (i - a)
                * dx**a
                * y0 ** (j - b)
                * dy**b
            )
    return total


def loop_one_form_moment(vertices, i, j, component):
    """Return integral x^i y^j dx (component 0) or dy (component 1)."""
    total = Q(0)
    for (x0, y0), (x1, y1) in zip(vertices, vertices[1:]):
        dx, dy = x1 - x0, y1 - y0
        total += (dx if component == 0 else dy) * linear_monomial_integral(
            x0, y0, dx, dy, i, j
        )
    return total


def area_winding_moment(vertices, i, j):
    """Green formula: integral winding*x^i*y^j dA."""
    return loop_one_form_moment(vertices, i + 1, j, 1) / Q(i + 1)


def line_integral_polynomial(vertices, coeffs, component):
    """Integrate a polynomial one-form coefficient against dx or dy."""
    return sum(
        (
            c * loop_one_form_moment(vertices, i, j, component)
            for (i, j), c in coeffs.items()
        ),
        Q(0),
    )


def direct_energy_first_column(vertices, widths):
    """Integral of F(Dphi), F(A)=A_11^4, psi=(cos y,sin y)."""
    total = Q(0)
    for (r0, s0), (r1, s1), tau in zip(vertices, vertices[1:], widths):
        p = (r1 - r0) / tau
        q = (s1 - s0) / tau
        # Exact y-average of (p cos(y) + q sin(y))^4.
        y_average = Q(3, 8) * (p**4 + q**4) + Q(3, 4) * p**2 * q**2
        total += tau * y_average
    return total


def fraction_from_sympy(value):
    value = sp.Rational(value)
    return Q(int(value.p), int(value.q))


def profile_action_polynomials():
    """Build exact y-averages for G and |Dphi|^4 for carriers (1,-1).

    The derivation uses u=u0+u1 cos(2y), v=v0+v1 cos(2y),
    det=d0+d1 cos(2y), then E[(a+b cos(2y))^2]=a^2+b^2/2.
    """
    r, s, p, q = sp.symbols("r s p q")
    u0, u1 = p**2 + q**2, 2 * p * q
    v0, v1 = r**2 + s**2, -2 * r * s
    d0, d1 = p * r - q * s, q * r - p * s
    h0, h1 = u0 + v0 - 2 * d0, u1 + v1 - 2 * d1
    g = (
        3 * (h0**2 + h1**2 / 2)
        + sp.Rational(35, 24) * (u0**2 + u1**2 / 2)
        + (d0**2 + d1**2 / 2)
        - sp.Rational(5, 2) * (d0 * u0 + d1 * u1 / 2)
    )
    n4 = (u0 + v0) ** 2 + (u1 + v1) ** 2 / 2
    variables = (r, s, p, q)

    # Independently compare with direct trigonometric integration at one
    # generic rational point before using these formulas for all graph edges.
    y = sp.symbols("y", real=True)
    rv, sv, pv, qv = map(sp.Rational, (2, 3, 5, 7))
    aa = (pv + qv) * sp.cos(y)
    cc = (pv - qv) * sp.sin(y)
    bb = -(rv + sv) * sp.sin(y)
    dd = (rv - sv) * sp.cos(y)
    uu, vv = aa**2 + cc**2, bb**2 + dd**2
    det = aa * dd - bb * cc
    g_trig = (
        3 * (uu + vv - 2 * det) ** 2
        + sp.Rational(35, 24) * uu**2
        + det**2
        - sp.Rational(5, 2) * det * uu
    )
    n4_trig = (uu + vv) ** 2
    direct_g = sp.integrate(g_trig, (y, 0, 2 * sp.pi)) / (2 * sp.pi)
    direct_n4 = sp.integrate(n4_trig, (y, 0, 2 * sp.pi)) / (2 * sp.pi)
    assert sp.simplify(direct_g - g.subs(dict(zip(variables, (rv, sv, pv, qv))))) == 0
    assert sp.simplify(direct_n4 - n4.subs(dict(zip(variables, (rv, sv, pv, qv))))) == 0

    def terms(poly):
        return [
            (tuple(int(e) for e in exps), fraction_from_sympy(c))
            for exps, c in sp.Poly(sp.expand(poly), *variables).terms()
        ]

    return variables, terms(g), terms(n4)


def exact_edge_integral(terms, start, end, tau):
    """Integrate a polynomial(r,s,r_x,s_x) on one affine strip exactly."""
    r0, s0 = start
    dr, ds = end[0] - r0, end[1] - s0
    total = Q(0)
    for (i, j, k, ell), coefficient in terms:
        velocity = dr**k * ds**ell / tau ** (k + ell)
        path_part = linear_monomial_integral(r0, s0, dr, ds, i, j)
        total += coefficient * velocity * tau * path_part
    return total


def exact_graph_recheck():
    _, g_terms, n4_terms = profile_action_polynomials()
    certificate = json.loads((SOURCE / "profile_graph_certificate.json").read_text())
    vertices = [
        (Q(i, 4), Q(j, 4)) for i in range(9) for j in range(9)
    ]
    widths = [Q(1, 8), Q(1, 4), Q(1, 2), Q(1), Q(2)]
    denominator = int(certificate["common_denominator"])
    potential = [int(v) for v in certificate["potential_numerators"]]
    assert len(vertices) == certificate["vertex_count"] == 81
    assert len(potential) == len(vertices)

    raw_negative = adjusted_negative = tight = edge_count = 0
    minimum_slack = None
    minimum_raw = None
    for i, start in enumerate(vertices):
        for j, end in enumerate(vertices):
            for width_index, tau in enumerate(widths):
                raw = exact_edge_integral(g_terms, start, end, tau)
                norm4 = exact_edge_integral(n4_terms, start, end, tau)
                assert norm4 >= 0
                adjusted = raw - norm4 / 4
                if raw < 0:
                    raw_negative += 1
                if adjusted < 0:
                    adjusted_negative += 1
                if minimum_raw is None or raw < minimum_raw[0]:
                    minimum_raw = (raw, i, j, width_index)
                slack = adjusted + Q(potential[i] - potential[j], denominator)
                assert slack >= 0, (i, j, width_index, slack)
                tight += slack == 0
                minimum_slack = slack if minimum_slack is None else min(minimum_slack, slack)
                edge_count += 1

    return {
        "method": "independent cos(2y) action formula plus rational segment integration",
        "vertices": len(vertices),
        "directed_edge_widths_checked": edge_count,
        "raw_negative_edges": raw_negative,
        "adjusted_negative_edges": adjusted_negative,
        "tight_edge_width_inequalities": tight,
        "minimum_slack": str(minimum_slack),
        "most_negative_raw_edge": {
            "cost": str(minimum_raw[0]),
            "start_index": minimum_raw[1],
            "end_index": minimum_raw[2],
            "width_index": minimum_raw[3],
        },
        "conclusion": "the supplied rational vertex potential certifies every listed closed walk in this finite graph",
    }


def verify_copied_inputs():
    manifest_path = SOURCE / "MANIFEST.json"
    manifest = json.loads(manifest_path.read_text())
    checked = []
    omitted = []
    for item in manifest["files"]:
        rel = item["path"]
        path = SOURCE / rel
        if not path.exists():
            omitted.append(rel)
            continue
        payload = path.read_bytes()
        digest = hashlib.sha256(payload).hexdigest()
        assert len(payload) == item["bytes"], rel
        assert digest == item["sha256"], rel
        checked.append(rel)
    assert len(checked) == 11
    assert omitted == [
        "exploration/graph_discovery.json",
        "exploration/graph_opposite_discovery.json",
        "exploration/profile_graph_explore.py",
        "exploration/profile_graph_opposite.py",
        "exploration/two_envelope_probe.py",
    ]
    return {
        "manifest_entries_verified": len(checked),
        "verified_paths": checked,
        "not_copied_exploration_paths": omitted,
        "source_manifest_sha256": hashlib.sha256(manifest_path.read_bytes()).hexdigest(),
    }


def exact_large_background_circulation():
    y = sp.symbols("y", real=True)
    r, s, B1, B2 = sp.symbols("r s B1 B2", real=True)
    psi1, psi2 = sp.cos(y), sp.sin(y)
    q_profile = r * sp.diff(psi1, y) + s * sp.diff(psi2, y)
    # F(a,b)=1/4(a^2+b^2)^2, so DF(a,b)[(psi,0)]
    # equals (a^2+b^2)*a*psi.
    density = B1**2 + (B2 + q_profile) ** 2
    alpha1 = sp.integrate(B1 * density * psi1, (y, 0, 2 * sp.pi)) / (2 * sp.pi)
    alpha2 = sp.integrate(B1 * density * psi2, (y, 0, 2 * sp.pi)) / (2 * sp.pi)
    assert sp.simplify(alpha1 - B1 * B2 * s) == 0
    assert sp.simplify(alpha2 + B1 * B2 * r) == 0

    side = Q(1, 100)
    square = square_loop(Q(0), Q(0), side)
    alpha_dr = {(0, 1): Q(1)}  # s dr
    alpha_ds = {(1, 0): Q(-1)}  # -r ds
    geometric_integral = (
        line_integral_polynomial(square, alpha_dr, 0)
        + line_integral_polynomial(square, alpha_ds, 1)
    )
    assert geometric_integral == -2 * side**2
    B_value = Q(10**6)
    circulation = B_value**2 * geometric_integral
    assert circulation == Q(-200_000_000)
    return {
        "energy": "F(A)=|A|^4/4, convex and rank-one convex",
        "profiles": "psi1=cos(y), psi2=sin(y)",
        "exact_one_form": "alpha=B1*B2*(s dr-r ds)",
        "square_side": str(side),
        "signed_area_moment_M00": str(side**2),
        "B1_equals_B2": str(B_value),
        "exact_circulation": str(circulation),
        "scope": "a small but nonzero low-order moment gives an unbounded-in-B circulation; this is not a negative Jensen gap because the full energy is convex and the positive Bregman terms compensate",
    }


def exact_nonpreservation_example():
    original = square_loop(Q(0), Q(0), Q(1))
    widths_original = [Q(23, 2)] * 4
    transformed = finite_difference_path(Q(2))
    widths_transformed = [Q(1)] * (len(transformed) - 1)
    assert len(transformed) - 1 == 46
    assert sum(widths_original) == sum(widths_transformed) == 46
    original_integral = direct_energy_first_column(original, widths_original)
    transformed_integral = direct_energy_first_column(transformed, widths_transformed)
    original_average = original_integral / 46
    transformed_average = transformed_integral / 46
    assert original_integral == Q(12, 12167)
    assert transformed_integral == Q(1596)
    assert original_average == Q(6, 23**4)
    assert transformed_average == Q(798, 23)
    return {
        "energy": "F(A)=A_11^4 on 1x2 matrices; convex quartic with mu_F=0",
        "same_x_period": 46,
        "original_loop": "unit square, four equal widths 23/2",
        "finite_difference_loop": "Gamma-3T_(2,0)Gamma+3T_(4,0)Gamma-T_(6,0)Gamma, with unit widths for all 46 segments",
        "original_unnormalized_energy": str(original_integral),
        "transformed_unnormalized_energy": str(transformed_integral),
        "original_optimized_normalized_gap": str(original_average),
        "transformed_optimized_normalized_gap": str(transformed_average),
        "why_optimized_gap_equals_B0_value": "the y-average of phi_x and phi_x^3 is zero, so the affine gap is E(phi_x^4)+6*B11^2*E(phi_x^2)",
        "conclusion": "the operation is not energy-preserving in general; it may still preserve special degenerate energies or loops",
    }


def main():
    copy_integrity = verify_copied_inputs()
    plus = finite_difference_path(Q(2))
    minus = finite_difference_path(Q(-2))
    zero_moments = {}
    for label, path in (("positive_translation", plus), ("negative_translation", minus)):
        assert len(path) - 1 == 46
        moments = {
            f"r^{i}s^{j}d{coord}": loop_one_form_moment(path, i, j, component)
            for i in range(4)
            for j in range(4 - i)
            for coord, component in (("r", 0), ("s", 1))
        }
        assert all(value == 0 for value in moments.values())
        area = {
            f"M{i}{j}": area_winding_moment(path, i, j)
            for i in range(3)
            for j in range(3 - i)
        }
        assert all(value == 0 for value in area.values())
        zero_moments[label] = {key: str(value) for key, value in moments.items()}
        zero_moments[f"{label}_area_moments"] = {key: str(value) for key, value in area.items()}
        zero_moments[f"{label}_higher_current_integral_r4_ds"] = str(
            loop_one_form_moment(path, 4, 0, 1)
        )

    assert loop_one_form_moment(plus, 4, 0, 1) == -192
    assert loop_one_form_moment(minus, 4, 0, 1) == 192
    assert min(r for r, _ in minus) < 0 and max(r for r, _ in minus) > 0

    graph = exact_graph_recheck()
    assert graph["directed_edge_widths_checked"] == 32805
    assert graph["raw_negative_edges"] == 104
    assert graph["adjusted_negative_edges"] == 2046
    assert graph["tight_edge_width_inequalities"] == 93
    assert graph["minimum_slack"] == "0"
    assert graph["most_negative_raw_edge"] == {
        "cost": "-1431/1280",
        "start_index": 53,
        "end_index": 77,
        "width_index": 2,
    }

    # Exact coefficient-level check: G has a negative invariant coefficient,
    # while its rank-one restriction still has mu=3.
    u, v, qdet = sp.symbols("u v qdet", nonnegative=True)
    G_invariants = (
        3 * (u + v - 2 * qdet) ** 2
        + sp.Rational(35, 24) * u**2
        + qdet**2
        - sp.Rational(5, 2) * qdet * u
    )
    rank_one_G = sp.expand(G_invariants.subs(qdet, 0))
    assert sp.simplify(
        rank_one_G - (3 * (u + v) ** 2 + sp.Rational(35, 24) * u**2)
    ) == 0
    a, b, c, d = sp.symbols("a b c d", real=True)
    uu, vv, qq = a**2 + c**2, b**2 + d**2, a * d - b * c
    G_matrix = (
        3 * (uu + vv - 2 * qq) ** 2
        + sp.Rational(35, 24) * uu**2
        + qq**2
        - sp.Rational(5, 2) * qq * uu
    )
    G_identity = G_matrix.subs({a: 1, b: 0, c: 0, d: 1})
    G_reflection = G_matrix.subs({a: 1, b: 0, c: 0, d: -1})
    witness_mean = sp.factor(
        (36**4 * G_identity + 36**2 * G_reflection) / (1 + 36**2)
    )
    assert G_identity == -sp.Rational(1, 24)
    assert G_reflection == sp.Rational(1271, 24)
    assert witness_mean == -sp.Rational(1350, 1297)

    results = {
        "status": "PASS",
        "source_copy_integrity": copy_integrity,
        "independent_moment_checks": zero_moments,
        "large_background_circulation": exact_large_background_circulation(),
        "finite_difference_energy_nonpreservation": exact_nonpreservation_example(),
        "profile_graph": graph,
        "negative_coefficient_integrand": {
            "G_contains_coefficient": "-5/2*q*u",
            "rank_one_restriction": str(rank_one_G),
            "mu_G": "3",
            "meaning": "this coefficient-level check does not by itself prove rank-one convexity; the separate exact acoustic Gram is checked by the supplied verifier and its replay",
            "non_polyconvex_witness": {
                "G(I)": str(G_identity),
                "G(diag(1,-1))": str(G_reflection),
                "determinant_balanced_mean_energy": str(witness_mean),
                "scope": "an exact finite measure obstruction to polyconvexity, not a compatible-gradient counterexample",
            },
        },
    }
    (ROOT / "independent_checks.json").write_text(json.dumps(results, indent=2) + "\n")
    print("PASS: 40 low-order line-integral moments across positive/negative translations")
    print("PASS: exact small-area / large-background circulation stress test")
    print("PASS: same-domain exact energy non-preservation witness")
    print("PASS: independently recomputed all 32,805 profile-graph inequalities")
    print("WROTE independent_checks.json")


if __name__ == "__main__":
    main()
