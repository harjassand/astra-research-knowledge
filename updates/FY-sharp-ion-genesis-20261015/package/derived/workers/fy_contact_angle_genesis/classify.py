#!/usr/bin/env python3
"""Exact rational finite-H projection for the generic-angle stratum.

Input: {"t": "1", "k": "2", "ell": "-1", "m": "3/4",
        "reserve": "1", "alpha": "0"}.
All coefficients are in the adapted normal form of REPORT.md. `alpha` is
used only to instantiate a forbidden-boundary witness. No floats are admitted.
"""

from __future__ import annotations

import argparse
from decimal import Decimal
from fractions import Fraction
from itertools import combinations
import json
from pathlib import Path

import sympy as sp


COORDS = sp.symbols("a b c d", real=True)
a, b, c, d = COORDS
v = b**2 + d**2
w = a*b + c*d
j = a*d - b*c
H = ((a-d)**2 + (b+c)**2)**2
IDENTITY = sp.Matrix([1, 0, 0, 1])


def rational(value):
    if isinstance(value, bool) or isinstance(value, float):
        raise ValueError("Boolean and pre-parsed float inputs are not exact rationals")
    if not isinstance(value, (str, int, Decimal, Fraction, sp.Rational)):
        raise ValueError("Expected an integer, exact decimal token, or rational string")
    if isinstance(value, sp.Rational):
        return value
    if isinstance(value, Decimal) and not value.is_finite():
        raise ValueError("Nonfinite decimal input")
    f = Fraction(value)
    return sp.Rational(f.numerator, f.denominator)


def load_exact_json(text):
    def reject_constant(value):
        raise ValueError("Nonfinite JSON token: " + value)
    return json.loads(text, parse_float=Decimal, parse_constant=reject_constant)


def encode(value):
    if isinstance(value, sp.Rational):
        return str(value)
    if isinstance(value, sp.MatrixBase):
        return [[encode(value[i, jj]) for jj in range(value.cols)]
                for i in range(value.rows)]
    if isinstance(value, dict):
        return {key: encode(val) for key, val in value.items()}
    if isinstance(value, (tuple, list)):
        return [encode(val) for val in value]
    return value


def form(t, k, ell, m):
    n = 1+t*t
    L = t*w-j+v
    G = sp.expand(k*L**2 + ell*v*(j-2*L/n) + m*v**2)
    A0, B0 = 2*m-ell, 2*m+ell
    C = sp.Matrix([[k, ell*t/n, -3*ell/n],
                   [ell*t/n, A0, 0], [-3*ell/n, 0, 3*B0]])
    J = sp.Matrix([[-1, t, t, 1], [0, 1, 0, 0], [0, 0, 0, 1]])
    Delta = sp.factor(k*n*n*A0*B0-ell**2*(t*t*B0+3*A0))
    return G, C, J.T*C*J, A0, B0, Delta


def elementary(matrix, degree):
    return sp.factor(sum(matrix.extract(indices, indices).det()
                         for indices in combinations(range(matrix.rows), degree)))


def acoustic_at(poly, background, direction):
    zz = sp.Matrix(direction)
    acoustic = (zz.T*sp.hessian(poly, COORDS)*zz)[0]/2
    return sp.factor(acoustic.subs(dict(zip(COORDS, background)), simultaneous=True))


def forbidden_boundary_witness(t, k, ell, m, alpha):
    G, _, _, A0, B0, _ = form(t, k, ell, m)
    n = 1+t*t
    if ell:
        Z = sp.Matrix([-(B0*t*t+A0)/(2*A0*n), -ell*t/(A0*n),
                       (B0*t*t+A0)/(2*t*B0*n), ell/(B0*n)])
        P = m*B0*B0*t*t+A0*A0*(2*ell+m)
        S = B0**3*t**4+2*(4*m-3*ell)*A0*B0*t*t+3*A0**3
        g = (ell**3*t/(A0**3*B0**2*n**3))*sp.Matrix([-4*t*P, S, S, 4*t*P])
    else:
        Z = sp.Matrix([0, 1, 0, -t])
        g = 2*k*n*sp.Matrix([-1, t, t, 1])
    assert sp.factor(Z[0]*Z[3]-Z[1]*Z[2]) == 0
    norm2 = sp.factor((g.T*g)[0])
    assert norm2 > 0
    E = -g
    T_alpha = acoustic_at(G+alpha*H, E, Z)
    epsilon = min(sp.Rational(1, 2), norm2/(2*(abs(T_alpha)+1)))
    background = IDENTITY+epsilon*E
    value = sp.factor(-norm2*epsilon+T_alpha*epsilon**2)
    assert value < 0
    return {"tested_alpha": alpha, "rank_one_direction": Z.reshape(2, 2),
            "background_gradient": g.reshape(2, 2),
            "background_direction": E.reshape(2, 2), "epsilon": epsilon,
            "background": background.reshape(2, 2), "half_acoustic_value": value,
            "scope": "For every finite alpha, the same formula gives a negative acoustic value."}


def classify(data):
    required = ("t", "k", "ell", "m")
    if not isinstance(data, dict) or any(key not in data for key in required):
        raise ValueError("Input must contain t, k, ell, and m")
    t, k, ell, m = [rational(data[key]) for key in required]
    reserve = rational(data.get("reserve", "1"))
    alpha = rational(data.get("alpha", "0"))
    if reserve < 0:
        raise ValueError("Reserve must be nonnegative")
    base = {"input": dict(zip(required, [t, k, ell, m])),
            "contract": "Adapted contact R=(t,1) tensor e1; all real backgrounds and W_0^(1,4) gradient tests",
            "external_correctness": "UNKNOWN", "historical_originality": "UNKNOWN"}
    if t == 0:
        return encode(base | {"status": "OUT_OF_SCOPE_TRACE_FREE",
                              "reason": "The generic-angle theorem excludes t=0; inherited sharp shear boundaries can be QC."})
    G, C, Q4, A0, B0, Delta = form(t, k, ell, m)
    base |= {"forced_lambda": 3*ell, "A0": A0, "B0": B0, "Delta": Delta}
    admitted = False
    boundary = False
    if ell == 0:
        if k < 0 or m < 0:
            reason = "The necessary conformal quadratic support is not PSD."
        elif k == 0:
            return encode(base | {"status": "ADMITTED_QC_COMPLETION", "branch": "CONVEX_EXCEPTION",
                                  "sufficient_total_alpha": reserve,
                                  "reserve": reserve, "L4_margin": 4*reserve/1875,
                                  "completion_cost": "The completion m v^2+reserve H is convex; no lambda search or eigenvalue oracle."})
        elif m > 0:
            admitted = True
        else:
            boundary = True
            reason = "Square-only singular support has an additional nonstationary rank-one contact."
    elif A0 <= 0 or B0 <= 0 or Delta < 0:
        reason = "The necessary conformal quadratic support is not PSD."
    elif Delta == 0:
        boundary = True
        reason = "The second rank-one line in the kernel plane has nonzero background acoustic derivative."
    else:
        admitted = True
    if admitted:
        e2, e3 = elementary(Q4, 2), elementary(Q4, 3)
        assert e2 > 0 and e3 > 0 and sp.factor(e3-3*Delta/(1+t*t)) == 0
        kappa = e3/e2
        tensor_bound = sum(abs(coefficient) for coefficient in sp.Poly(G, COORDS).coeffs())
        alpha_star = 401296*tensor_bound**2/kappa+sp.Rational(9391, 4)*tensor_bound
        return encode(base | {"status": "ADMITTED_QC_COMPLETION", "branch": "STRICT_TRANSVERSE_SUPPORT",
                              "quadratic_support_matrix": Q4, "kernel_generator": [[t, 0], [1, 0]],
                              "e2": e2, "e3": e3, "kappa": kappa,
                              "tensor_bound_M": tensor_bound, "alpha_star": alpha_star,
                              "reserve": reserve, "sufficient_total_alpha": alpha_star+reserve,
                              "L4_margin": 4*reserve/1875,
                              "completion_cost": "Fixed-dimensional rational arithmetic; supplied rational t and coefficients are charged; lambda is forced."})
    result = base | {"status": "NO_FINITE_ROC_OR_QC_COMPLETION", "reason": reason}
    if boundary:
        result["witness"] = forbidden_boundary_witness(t, k, ell, m, alpha)
    return encode(result)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = classify(load_exact_json(args.input.read_text()))
    text = json.dumps(result, indent=2)+"\n"
    if args.output:
        args.output.write_text(text)
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
