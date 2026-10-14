#!/usr/bin/env python3
"""Exact symbolic certificate for the resonant compatible tangent family."""
from __future__ import annotations

import json
from pathlib import Path
import sympy as sp

from exact_tangent_triad import run


def bernstein_coefficients(poly: sp.Expr, x: sp.Symbol, right: sp.Rational) -> list[sp.Expr]:
    y = sp.symbols("y")
    p = sp.Poly(sp.expand(poly.subs(x, right*y)), y)
    n = p.degree()
    power = [p.nth(i) for i in range(n+1)]
    return [sp.factor(sum(power[i]*sp.binomial(k, i)/sp.binomial(n, i)
                          for i in range(k+1))) for k in range(n+1)]


def Q_basis(A: sp.Matrix) -> sp.Matrix:
    # Exact orthogonal complement of A=I in row-major coordinates.
    return sp.Matrix.hstack(A, sp.Matrix([1,0,0,-1]),
                            sp.Matrix([0,1,0,0]), sp.Matrix([0,0,1,0]))


def schur(H: sp.Matrix, ell: sp.Matrix, A: sp.Matrix) -> tuple[sp.Expr, sp.Expr, sp.Expr]:
    Q = Q_basis(A)
    Hb = Q.T*H*Q
    eb = Q.T*ell
    D = Hb[1:,1:]
    k = Hb[1:,0]
    h = sp.factor(Hb[0,0])
    hs = sp.factor(h-(k.T*D.inv()*k)[0])
    rs = sp.factor(eb[0]-(k.T*D.inv()*eb[1:,0])[0])
    return h, hs, rs


def main() -> None:
    e = sp.symbols("e", positive=True)
    result = run(1/e, 1, -3, (sp.Integer(2), sp.Integer(1), sp.Integer(1)))
    H = sp.Matrix(result["H"])
    C = sp.Matrix(result["covariance"])
    b = sp.Matrix(result["b"])
    ell = sp.Matrix(result["ell"])
    I4 = sp.eye(4)
    J = sp.zeros(4)
    J[0,3] = J[3,0] = sp.Rational(1,2)
    J[1,2] = J[2,1] = -sp.Rational(1,2)
    expected_C = sp.Matrix([
        [7*e**2, 0, -18*e**3, sp.Rational(21,2)*e**2],
        [0, 3, sp.Rational(21,2)*e**2, 0],
        [-18*e**3, sp.Rational(21,2)*e**2, sp.Rational(387,4)*e**4, -27*e**3],
        [sp.Rational(21,2)*e**2, 0, -27*e**3, sp.Rational(63,4)*e**2],
    ])
    assert sp.simplify(C-expected_C) == sp.zeros(4)
    K = sp.simplify(3*I4-C-21*e**2*J)
    assert K[1,:] == sp.zeros(1,4) and K[:,1] == sp.zeros(4,1)
    x = sp.symbols("x", nonnegative=True)
    # The nonzero 3x3 block's principal minors are positive on e^2 in [0,1/16].
    inds = [0,2,3]
    block = K.extract(inds, inds)
    minors=[]
    for size in (1,2,3):
        for subset in __import__('itertools').combinations(range(3),size):
            minor=sp.factor(block.extract(subset,subset).det())
            coeffs=bernstein_coefficients(minor.subs(e**2,x),x,sp.Rational(1,16))
            assert all(sp.simplify(v)>0 for v in coeffs)
            minors.append({"indices":[inds[i] for i in subset],"polynomial":str(minor),
                           "bernstein_coefficients_on_x_in_0_1_over_16":[str(v) for v in coeffs]})
    # Sylvester's criterion on H shows H>0 for every e>0.
    leading=[]
    for size in range(1,5):
        minor=sp.factor(H[:size,:size].det())
        poly=sp.Poly(minor,e)
        assert all(coef>=0 for coef in poly.all_coeffs()) and minor!=0
        leading.append(str(minor))

    A=sp.Matrix([1,0,0,1]); R=sp.Matrix([0,1,0,0])
    h,hs,rs=schur(H,ell,A)
    m2,m3,m4=(result[k] for k in ("m2","m3","m4"))
    d2sq=result["delta2_sq"]
    d4four=result["delta4_4"]
    limits={
        "h_over_e4":sp.limit(h/e**4,e,0),
        "hstar_over_e4":sp.limit(hs/e**4,e,0),
        "rstar_over_e3":sp.limit(rs/e**3,e,0),
        "delta2_sq_over_e2":sp.limit(d2sq/e**2,e,0),
        "delta4_sq_over_e2":sp.limit(sp.sqrt(d4four)/e**2,e,0),
        "normalized_reduced_metric_using_delta2":sp.limit(rs**2/(hs*m4*d2sq),e,0),
        "normalized_reduced_metric_using_delta4":sp.limit(rs**2/(hs*m4*sp.sqrt(d4four)),e,0),
        "full_gap":sp.limit(result["gap"],e,0),
    }
    expected={"h_over_e4":sp.Rational(645,8),
              "hstar_over_e4":sp.Rational(10385,144),
              "rstar_over_e3":-sp.Rational(25,2),
              "delta2_sq_over_e2":sp.Rational(91,12),
              "delta4_sq_over_e2":sp.Rational(91,12),
              "normalized_reduced_metric_using_delta2":sp.Rational(8000,567021),
              "normalized_reduced_metric_using_delta4":sp.Rational(8000,567021),
              "full_gap":sp.Rational(219,4)}
    assert limits==expected
    assert (m2,m3,m4)==(3,3,sp.Rational(81,4))
    Bopt=sp.simplify(-H.inv()*b)
    Bopt_limits={
        "e_times_entry_a":sp.limit(e*Bopt[0],e,0),
        "entry_b":sp.limit(Bopt[1],e,0),
        "entry_c_over_e2":sp.limit(Bopt[2]/e**2,e,0),
        "e_times_entry_d":sp.limit(e*Bopt[3],e,0),
    }
    assert Bopt_limits=={"e_times_entry_a":sp.Rational(360,2077),
                         "entry_b":-sp.Rational(1,3),
                         "entry_c_over_e2":-sp.Rational(72487,18693),
                         "e_times_entry_d":sp.Rational(360,2077)}

    # Rational Pythagorean output rotation: sin(theta)=2e/(1+e^2).
    cth=(1-e**2)/(1+e**2); sth=2*e/(1+e**2)
    T=sp.Matrix([[cth,0,-sth,0],[0,cth,0,-sth],[sth,0,cth,0],[0,sth,0,cth]])
    Hrot=sp.simplify(T*H*T.T)
    ellrot=sp.simplify(T*ell)
    hfix,hsfix,rsfix=schur(Hrot,ellrot,A)
    fixed_limits={
        "h_over_e2":sp.limit(hfix/e**2,e,0),
        "hstar_over_e4":sp.limit(hsfix/e**4,e,0),
        "hstar_over_h_over_e2":sp.limit((hsfix/hfix)/e**2,e,0),
        "rstar_over_e3":sp.limit(rsfix/e**3,e,0),
        "normalized_reduced_metric":sp.limit(rsfix**2/(hsfix*m4*d2sq),e,0),
    }
    assert fixed_limits=={"h_over_e2":sp.Integer(24),
                          "hstar_over_e4":sp.Rational(10385,144),
                          "hstar_over_h_over_e2":sp.Rational(10385,3456),
                          "rstar_over_e3":-sp.Rational(25,2),
                          "normalized_reduced_metric":sp.Rational(8000,567021)}
    # Following both the rank-one covariance line and acoustic direction is an
    # exact orthogonal conjugacy, so every fitted-frame block is unchanged.
    Q=Q_basis(A)
    assert sp.simplify((T*Q).T*Hrot*(T*Q)-Q.T*H*Q)==sp.zeros(4)
    assert sp.simplify((T*Q).T*ellrot-Q.T*ell)==sp.zeros(4,1)

    report={
        "status":"exact symbolic identities and asymptotic limits for one compatible family",
        "field":{"epsilon":"1/N, N integer >=4","slow_frequencies":[[1,1],[-3,1],[-2,2]],
                 "amplitudes_s":[2,1,1],"tangent_residual_r":"0",
                 "phase_relation":"theta_1+theta_2=theta_3","periodic_output_vectors":"(epsilon*s_j/q_j, epsilon*d_j/q_j)"},
        "covariance_fitted_line":"e12 exactly for 0<epsilon<=1/4 by K=3I-C-21 epsilon^2 J >=0",
        "covariance_psd_finsler_minor_certificates":minors,
        "averaged_Hessian_leading_principal_minors":leading,
        "moments":{"m2":str(m2),"m3":str(m3),"m4":str(m4)},
        "moving_contact_asymptotic_limits":{k:str(v) for k,v in limits.items()},
        "full_background_optimizer_scaled_limits":{k:str(v) for k,v in Bopt_limits.items()},
        "rotated_stale_frame_limits":{k:str(v) for k,v in fixed_limits.items()},
        "interpretation":"The compatible resonant family satisfies the requested reduced estimate with a finite sharp-family limit, retains a positive all-background gap, and has an escaping optimizer. It does not prove a uniform estimate over all gradients or integrands.",
    }
    path=Path(__file__).with_name("exact_moving_metric_certificate.json")
    path.write_text(json.dumps(report,indent=2)+"\n")
    print(path)


if __name__=="__main__":main()
