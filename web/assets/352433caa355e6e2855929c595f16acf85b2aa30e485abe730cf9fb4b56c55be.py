#!/usr/bin/env python3
"""Exact-rational checks for the coupled-flux two-species witness.

No third-party packages are required. Decimal exponentiation is used only to
print approximate horizon/cost/risk diagnostics; every certificate inequality
and the independent-box counterexample is checked with fractions.
"""

from decimal import Decimal, localcontext
from fractions import Fraction as F
from math import factorial


def exp_pos_half_upper(n: int = 5) -> F:
    """Rational upper bound on exp(1/2), with a geometric tail majorant."""
    partial = sum((F(1, 2) ** j) / factorial(j) for j in range(n + 1))
    first_tail = (F(1, 2) ** (n + 1)) / factorial(n + 1)
    largest_tail_ratio = F(1, 2 * (n + 2))
    return partial + first_tail / (1 - largest_tail_ratio)


def exp_neg_half_partial(n: int) -> F:
    return sum(((-F(1, 2)) ** j) / factorial(j) for j in range(n + 1))


def exp_pos_partial(x: F, n: int) -> F:
    """Lower bound on exp(x) for x>0 from its positive Taylor partial sum."""
    return sum((x**j) / factorial(j) for j in range(n + 1))


def ceil_fraction(x: F) -> int:
    return (x.numerator + x.denominator - 1) // x.denominator


def dec(x: F) -> Decimal:
    return Decimal(x.numerator) / Decimal(x.denominator)


def main() -> None:
    # Certified elementary exponential enclosures from Taylor remainders.
    exp_plus_upper = exp_pos_half_upper()
    exp_minus_lower = exp_neg_half_partial(7)  # odd alternating partial sum
    exp_minus_upper = exp_neg_half_partial(8)  # even alternating partial sum
    assert exp_plus_upper < F(1649, 1000)
    assert F(606, 1000) < exp_minus_lower < exp_minus_upper < F(607, 1000)

    a_lower = exp_pos_partial(F(1, 2), 5) - 1
    a_upper = F(649, 1000)  # exp(1/2)-1
    b_lower = exp_minus_lower - 1
    b_for_upper_h = -F(393, 1000)  # exp(-1/2)-1 < -393/1000
    b_abs_upper = F(394, 1000)  # 1-exp(-1/2) < 394/1000

    # Stoichiometry: 2A -> A+B and 2B -> A+B; x=A/V, A+B=V.
    # Coupled K={(q,q):1<=q<=16}; the drift is q(1-2x).
    left_outer = F(1, 4)
    left_collar_end = F(9, 32)
    coupled_inward_margin = 1 - 2 * left_collar_end
    assert coupled_inward_margin == F(7, 16)
    assert a_lower > 0 and 1 - exp_minus_upper > 0

    # For theta=1/2 the left-facet H is q*h(x), with h increasing on [1/4,9/32].
    x = left_collar_end
    h_collar_upper = x**2 * a_upper + (1 - x) ** 2 * b_for_upper_h
    assert h_collar_upper == -F(2427, 16000)
    assert h_collar_upper < -F(3, 20)
    x = left_outer
    h_at_left_endpoint_upper = x**2 * a_upper + (1 - x) ** 2 * b_for_upper_h
    assert h_at_left_endpoint_upper < 0
    # Thus max over q in [1,16] is q=1 on the collar, yielding eta=3/20.
    eta = F(3, 20)

    # h is convex on Q, so its maximum is at an endpoint. Symmetry plus the
    # rational endpoint enclosure gives the all-Q positive-part constant C.
    x = F(3, 4)
    sixteen_h_endpoint_upper = 16 * (
        x**2 * a_upper + (1 - x) ** 2 * b_for_upper_h
    )
    assert sixteen_h_endpoint_upper == F(681, 125)  # 5.448
    C = F(109, 20)
    assert sixteen_h_endpoint_upper < C

    # Both reactants have degree 2 and U_A=U_B=1, hence E_2(U)=1.
    D = 16 * (F(649, 1000) + F(394, 1000))
    assert D == F(2086, 125)
    assert ceil_fraction(2 * D / eta) == 223
    V0 = 223
    theta = F(1, 2)
    ell = F(1, 32)
    c = theta * ell
    assert c == F(1, 64)

    # Independent-box attack: at x=1/4 and (k_A,k_B)=(16,1),
    # dot{x}=k_B(1-x)^2-k_A*x^2=-7/16, outward through the left facet.
    x = F(1, 4)
    independent_box_drift = F(1) * (1 - x) ** 2 - F(16) * x**2
    assert independent_box_drift == -F(7, 16)
    independent_box_H_lower = 16 * x**2 * a_lower + (1 - x) ** 2 * b_lower
    assert independent_box_H_lower > 0

    # The total activity envelope is 16*max_Q[x^2+(1-x)^2]=10 exactly.
    activity_at_endpoint = F(1, 4) ** 2 + F(3, 4) ** 2
    Lambda_Q = 16 * activity_at_endpoint
    assert Lambda_Q == 10

    # V=3000 with A=B=1500 has both initial facet gaps 1/4.  The theorem's
    # bound at T=exp(cV/2) is 2 exp(-375)+2(VC+D)exp(-cV/2).
    V = 3000
    assert V % 2 == 0 and V >= V0
    T_exponent = c * V / 2
    assert T_exponent == F(375, 16)  # 23.4375
    exact_risk_upper = (
        2 / exp_pos_partial(F(375), 10)
        + 2 * (V * C + D) / exp_pos_partial(F(375, 16), 42)
    )
    assert exact_risk_upper < F(217, 100_000_000)  # 2.17e-6
    risk_bound_form = (
        "2*exp(-375) + 2*(V*C + D)*exp(-23.4375)"
    )

    with localcontext() as ctx:
        ctx.prec = 60
        T = dec(T_exponent).exp()
        risk = (
            Decimal(2) * Decimal(-375).exp()
            + Decimal(2) * (Decimal(V) * dec(C) + dec(D)) * (-dec(T_exponent)).exp()
        )
        candidates = Decimal(V) * dec(Lambda_Q) * T
        assert risk < Decimal("2.17e-6")

    print("PASS exact rational coupled-margin, correction, constants, and box-witness checks")
    print(f"theta={theta}; eta={eta}; ell={ell}; c={c}; V0={V0}; C={C}; D={D}")
    print(
        f"Lambda_Q={Lambda_Q}; independent_box_drift={independent_box_drift}; "
        f"independent_box_H_lower={independent_box_H_lower} > 0"
    )
    print(f"risk_bound_at_T=e^(cV/2): {risk_bound_form}")
    print("exact rational exponential-series enclosure proves risk < 217/100000000")
    print(f"T=e^({T_exponent}) ~= {T}")
    print(f"risk upper bound ~= {risk}")
    print(f"V*Lambda_Q*T ~= {candidates} expected thinning candidates; no simulation run")


if __name__ == "__main__":
    main()
