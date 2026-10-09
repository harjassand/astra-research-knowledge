#!/usr/bin/env python3
"""Exact low-dimensional checks for signed amplifier EPnI identities.

The checks use rational arithmetic and symbolic geometric-number-basis weights.
The only finite matrix example is a deliberately complex off-diagonal observable
used to distinguish adjoint from plain Fock transpose.
"""

from fractions import Fraction as Q
import sympy as sp


def check_scalar_thermal_balance():
    G, rA, rB, u = Q(3, 2), Q(1, 3), Q(2, 5), Q(1, 4)
    rstar = G * rA + (G - 1) * (rB + 1)
    assert rstar == Q(6, 5)
    assert rstar + 1 == G * (rA + 1) + (G - 1) * rB

    # The tempting passive sign convention is false at this explicit point.
    wrong_companion = G * (rA + 1) + (G - 1) * (rB + 1)
    assert wrong_companion == Q(27, 10)
    assert wrong_companion != rstar + 1

    lamA, lamB, lamD = (1 - u) * G, (1 - u) * (G - 1), u
    rD = rstar
    r0 = lamA * rA + lamB * (rB + 1) + lamD * rD
    assert r0 == rstar
    assert lamA - lamB + lamD == 1
    assert r0 + 1 == lamA * (rA + 1) + lamB * rB + lamD * (rD + 1)

    x1 = lamA * rA + lamB * (rB + 1)
    x2 = lamA * (rA + 1) + lamB * rB
    slack1, slack2 = r0 - x1, r0 + 1 - x2
    assert slack1 == u * rD == Q(3, 10)
    assert slack2 == u * (rD + 1) == Q(11, 20)
    eps = Q(1, 4)
    assert (1 + eps) * x1 < r0
    assert (1 + eps) * x2 < r0 + 1

    # The OU Gaussian-noise coefficient has the same signed normalization.
    noise = lamA * (rA + Q(1, 2)) + lamB * (rB + Q(1, 2)) + lamD * (rD + Q(1, 2))
    assert noise == r0 + Q(1, 2)
    print("scalar thermal balance: PASS (exact fractions)")
    print(f"  G={G}, rA={rA}, rB={rB}, r*={rstar}, lambdas=({lamA},{lamB},{lamD})")
    print(f"  slacks={slack1},{slack2}; epsilon={eps} satisfies both")
    print(f"  false passive companion={wrong_companion} versus r*+1={rstar + 1}")
    print(f"  OU noise coefficient={noise}=r0+1/2")


def check_thermal_defects_in_number_basis():
    q = sp.symbols("q", positive=True)
    r = q / (1 - q)
    p = lambda n: (1 - q) * q**n
    checked = 0
    # Z=|u><v|. These are the exact infinite-oscillator traces; each is a
    # single geometric-weight term because Z has finite number-basis support.
    for u in range(9):
        for v in range(9):
            down_left = sp.sqrt(v) * p(v) if v == u + 1 else 0
            down_right = sp.sqrt(u + 1) * p(u) if v == u + 1 else 0
            q_down = sp.simplify((r + 1) * down_left - r * down_right)

            up_left = sp.sqrt(u) * p(v) if u == v + 1 else 0
            up_right = sp.sqrt(u) * p(u) if u == v + 1 else 0
            q_up = sp.simplify(r * up_left - (r + 1) * up_right)
            assert q_down == 0, (u, v, q_down)
            assert q_up == 0, (u, v, q_up)
            checked += 1
    print(f"thermal number-basis defects: PASS ({checked} matrix units, symbolic q)")


def check_adjoint_vs_transpose():
    # |psi>=(|0>+|1>)/sqrt(2); its oscillator mean is exactly 1/2.
    a = sp.Matrix([[0, 1, 0], [0, 0, sp.sqrt(2)], [0, 0, 0]])
    rho = sp.zeros(3)
    rho[:2, :2] = sp.Matrix([[sp.Rational(1, 2), sp.Rational(1, 2)],
                              [sp.Rational(1, 2), sp.Rational(1, 2)]])
    mu = sp.trace(rho * a)
    assert mu == sp.Rational(1, 2)
    d = a - mu * sp.eye(3)
    r = sp.Integer(1)
    Z = sp.zeros(3)
    Z[0, 1] = sp.I

    def q_down(X):
        return sp.simplify((r + 1) * sp.trace(rho * d.conjugate().T * X)
                           - r * sp.trace(rho * X * d.conjugate().T))

    def q_up(X):
        return sp.simplify(r * sp.trace(rho * d * X)
                           - (r + 1) * sp.trace(rho * X * d))

    rhs_adjoint = sp.simplify(-sp.conjugate(q_down(Z.conjugate().T)))
    rhs_transpose = sp.simplify(-sp.conjugate(q_down(Z.T)))
    assert q_up(Z) == sp.I / 4
    assert rhs_adjoint == q_up(Z)
    assert rhs_transpose == -sp.I / 4
    assert rhs_transpose != q_up(Z)
    print("adjoint/transpose orientation: PASS")
    print(f"  q_up(i|0><1|)={q_up(Z)}")
    print(f"  -conj q_down(Z†)={rhs_adjoint}")
    print(f"  -conj q_down(Z^T)={rhs_transpose}  [wrong sign]")


def check_convolution_sign_symbolically():
    G, rA, rB = sp.symbols("G rA rB")
    K = G - 1
    rstar = G * rA + K * (rB + 1)
    commutator_coefficient = sp.simplify(G * (rstar - rA) - K * (rstar + rB + 1))
    assert commutator_coefficient == 0

    # If +q_B^up is mistakenly used, the two B-order coefficients no longer
    # form a commutator; their sum is exactly 2, so CCR cancellation fails.
    plus_x = rstar + 1 - rB
    plus_y = -rstar + rB + 1
    assert sp.simplify(plus_x + plus_y) == 2
    print("raw defect convolution sign: PASS symbolically")
    print("  candidate minus sign leaves zero commutator coefficient")
    print("  mistaken plus sign leaves nonzero symmetric component 2")


if __name__ == "__main__":
    check_scalar_thermal_balance()
    check_thermal_defects_in_number_basis()
    check_adjoint_vs_transpose()
    check_convolution_sign_symbolically()
