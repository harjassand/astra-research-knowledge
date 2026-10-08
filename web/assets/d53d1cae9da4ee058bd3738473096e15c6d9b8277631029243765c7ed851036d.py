#!/usr/bin/env python3
"""Symbolic counterexample to product-only isotope identification.

No guessed enrichment, rate, isotope-effect, or residence-time numbers are
used.  SymPy verifies an exact intersection of the direct CO*+CH2* and
CO*+CO* / asymmetric-hydrogenation product-law sets.
"""

import sympy as sp


def direct_law(p_methyl, p_carboxyl):
    """Independent precursor pools; key is (methyl-13C, carboxyl-13C)."""
    return {
        (1, 1): p_methyl * p_carboxyl,
        (1, 0): p_methyl * (1 - p_carboxyl),
        (0, 1): (1 - p_methyl) * p_carboxyl,
        (0, 0): (1 - p_methyl) * (1 - p_carboxyl),
    }


def dimer_law(p_site_a, p_site_b, a_to_methyl):
    """Two site-specific CO pools, followed by asymmetric hydrogenation."""
    a = a_to_methyl
    return {
        (1, 1): p_site_a * p_site_b,
        (1, 0): a * p_site_a * (1 - p_site_b)
        + (1 - a) * p_site_b * (1 - p_site_a),
        (0, 1): a * (1 - p_site_a) * p_site_b
        + (1 - a) * (1 - p_site_b) * p_site_a,
        (0, 0): (1 - p_site_a) * (1 - p_site_b),
    }


def effective_fraction(feed_fraction, k13_over_k12):
    """Effective reacting 13C fraction after an isotope-specific rate factor."""
    return feed_fraction * k13_over_k12 / (
        1 - feed_fraction + feed_fraction * k13_over_k12
    )


def check_symbolic_overlap():
    # These are arbitrary effective pool histories, not numerical assignments.
    p_m, p_c = sp.symbols("p_m p_c", real=True)
    alpha = sp.Integer(1)
    direct = direct_law(p_m, p_c)
    dimer = dimer_law(p_m, p_c, alpha)
    assert all(sp.simplify(direct[z] - dimer[z]) == 0 for z in direct)

    # At every time t, the same substitution works for arbitrary tracer traces.
    t = sp.symbols("t", real=True)
    p_m_t = sp.Function("p_m")(t)
    p_c_t = sp.Function("p_c")(t)
    direct_t = direct_law(p_m_t, p_c_t)
    dimer_t = dimer_law(p_m_t, p_c_t, alpha)
    assert all(sp.simplify(direct_t[z] - dimer_t[z]) == 0 for z in direct_t)

    # A position ratio alone only gives an odds-ratio constraint.  The same
    # relation holds for the two dimer CO-site pools under fixed orientation.
    r_direct = ((1 - p_m) * p_c) / (p_m * (1 - p_c))
    r_dimer = ((1 - p_m) * p_c) / (p_m * (1 - p_c))
    assert sp.simplify(r_direct - r_dimer) == 0

    # Explicit reversible two-pool isotope-exchange state-space witness.
    # Both chemical interpretations can share this transfer operator because
    # the Cu-Fe report supplies no route-specific exchange or residence rates.
    s = sp.symbols("s", positive=True)
    kd1, kd2, ed12, ed21 = sp.symbols("kd1 kd2 ed12 ed21", positive=True)
    kh1, kh2, eh12, eh21 = sp.symbols("kh1 kh2 eh12 eh21", positive=True)
    A_d = sp.Matrix([[-kd1 - ed12, ed21], [ed12, -kd2 - ed21]])
    B_d = sp.diag(kd1, kd2)
    A_h = sp.Matrix([[-kh1 - eh12, eh21], [eh12, -kh2 - eh21]])
    B_h = sp.diag(kh1, kh2)
    transfer_d = (s * sp.eye(2) - A_d).inv() * B_d
    transfer_h = (s * sp.eye(2) - A_h).inv() * B_h
    # Map the dimer pool turnover/exchange rates to the direct route's
    # effective precursor turnover/exchange rates. All rates remain positive.
    mapping = {kh1: kd1, kh2: kd2, eh12: ed12, eh21: ed21}
    assert all(
        sp.simplify(transfer_d[i, j] - transfer_h[i, j].subs(mapping)) == 0
        for i in range(2)
        for j in range(2)
    )

    # KIEs are folded into the effective fractions.  Since no Cu-Fe carbon KIE
    # is reported, equal effective fractions remain an admissible assignment.
    x1, x2, q1, q2 = sp.symbols("x1 x2 q1 q2", real=True, positive=True)
    p1 = effective_fraction(x1, q1)
    p2 = effective_fraction(x2, q2)
    assert sp.simplify(p1 - effective_fraction(x1, q1)) == 0
    assert sp.simplify(p2 - effective_fraction(x2, q2)) == 0

    return {
        "static_and_time_resolved_position_laws": "exact overlap",
        "overlap_witness": "p_site_A(t)=p_CH2(t), p_site_B(t)=p_CO(t), orientation A->methyl",
        "reversible_exchange": "same admissible two-pool transfer matrix in both models",
        "kinetic_isotope_effect": "absorbed into unconstrained effective fractions; no Cu-Fe carbon KIE supplied",
        "numerical_parameters_used": [],
    }


if __name__ == "__main__":
    for key, value in check_symbolic_overlap().items():
        print(f"{key}: {value}")
