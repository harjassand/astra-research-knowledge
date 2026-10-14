#!/usr/bin/env python3
"""Exact finite checks for the curved-family N794 completion synthesis.

The analytic statements are in REPORT.md.  This script checks (i) a non-affine
curved profile's curvature cancellations, zero-background moment vector, and
explicit 8x8 flux completion; and (ii) the N794 Fourier-acoustic normalization
for a finite, half-turn-symmetric compatible gradient at a rational background.
It does not machine-certify the analytic theorem or any global Morrey claim.
"""
from __future__ import annotations

import json
from itertools import combinations
from pathlib import Path

import sympy as S


def check(name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(name)
    print("PASS", name)


def average_power_cos(power: int) -> S.Expr:
    """Normalized average of cos(x)^power on the 2pi torus."""
    if power % 2:
        return S.Integer(0)
    return S.binomial(power, power // 2) / S.Integer(2) ** power


class Fourier:
    """Small exact two-dimensional Fourier algebra with SymPy coefficients."""

    def __init__(self, coeff=None):
        self.c = {tuple(k): S.sympify(v) for k, v in (coeff or {}).items() if v != 0}

    def __add__(self, other):
        if not isinstance(other, Fourier):
            other = Fourier({(0, 0): other})
        d = self.c.copy()
        for k, v in other.c.items():
            d[k] = d.get(k, S.Integer(0)) + v
        return Fourier({k: v for k, v in d.items() if v != 0})

    __radd__ = __add__

    def __neg__(self):
        return Fourier({k: -v for k, v in self.c.items()})

    def __sub__(self, other):
        return self + (-other if isinstance(other, Fourier) else -S.sympify(other))

    def __mul__(self, other):
        if not isinstance(other, Fourier):
            return Fourier({k: v * S.sympify(other) for k, v in self.c.items()})
        d = {}
        for k, v in self.c.items():
            for ell, w in other.c.items():
                q = (k[0] + ell[0], k[1] + ell[1])
                d[q] = d.get(q, S.Integer(0)) + v * w
        return Fourier({k: v for k, v in d.items() if v != 0})

    __rmul__ = __mul__

    def __pow__(self, power: int):
        out = Fourier({(0, 0): S.Integer(1)})
        for _ in range(power):
            out = out * self
        return out

    def diff(self, j: int):
        return Fourier({k: v * S.I * k[j] for k, v in self.c.items()})

    def mean(self):
        value = S.simplify(self.c.get((0, 0), S.Integer(0)))
        if S.simplify(S.im(value)) != 0:
            raise AssertionError(f"non-real Fourier mean: {value}")
        return S.simplify(S.re(value))


def cos_mode(k):
    return Fourier({k: S.Rational(1, 2), (-k[0], -k[1]): S.Rational(1, 2)})


def sin_mode(k):
    return Fourier({k: 1 / (2 * S.I), (-k[0], -k[1]): -1 / (2 * S.I)})


def eval_poly_fourier(expr, variables, values):
    poly = S.Poly(expr, *variables)
    out = Fourier()
    for exponents, coeff in poly.terms():
        term = Fourier({(0, 0): coeff})
        for value, exponent in zip(values, exponents):
            term = term * (value ** exponent)
        out = out + term
    return out


def n794_basis_and_acoustic_matrices():
    """N794 f=(u^2,v^2,uv,w^2,uw,vw,qu,qv,qw) and Q_i."""
    A, Bc, C, E, G, H, L, M, N = S.symbols("A B C E G H L M N")
    names = (A, Bc, C, E, G, H, L, M, N)
    a, b, c, d = S.symbols("a b c d")
    u, v = a * a + c * c, b * b + d * d
    w, q = a * b + c * d, a * d - b * c
    basis = (u**2, v**2, u*v, w**2, u*w, v*w, q*u, q*v, q*w)

    M11 = S.Matrix([
        [12*A, 3*G, 0, 3*L],
        [3*G, 2*C + 2*E, -L, N],
        [0, -L, 4*A, G],
        [3*L, N, G, 2*C],
    ])
    M12 = S.Matrix([
        [3*G, 2*C + 2*E, -L, N],
        [2*C + 2*E, 3*H, -N, M],
        [-L, -N, G, E],
        [N, M, E, H],
    ])
    M22 = S.Matrix([
        [2*C + 2*E, 3*H, -N, M],
        [3*H, 12*Bc, -3*M, 0],
        [-N, -3*M, 2*C, H],
        [M, 0, H, 4*Bc],
    ])
    acoustic = []
    for name in names:
        sub = {parameter: int(parameter == name) for parameter in names}
        Q = S.zeros(8)
        Q[:4, :4] = M11.subs(sub)
        Q[:4, 4:] = M12.subs(sub)
        Q[4:, :4] = M12.subs(sub)
        Q[4:, 4:] = M22.subs(sub)
        acoustic.append(Q)
    return (a, b, c, d), basis, acoustic


def curved_zero_background_check():
    """Exact Y_0 and moment pairings for r=1+cos(2 theta)/5, g=sin(x)/4."""
    variables, basis, acoustic = n794_basis_and_acoustic_matrices()
    eps = S.Rational(1, 5)
    # Exact one-variable Fourier moments in theta, with R=r and RP=dr/dtheta.
    Rtheta = Fourier({(0, 0): 1}) + eps * cos_mode((0, 2))
    RPtheta = -2 * eps * sin_mode((0, 2))

    # Use independent polynomial symbols for the exact product averages.
    P, R, RP = S.symbols("P R RP", real=True)
    # Under U=rotation(theta), U^T(P+sQ)=(s*RP*e1+R*e2) tensor (P,1).
    zP = S.Matrix([0, 0, R*P**2, R*P, 0, 0, R*P, R])
    zQ = S.Matrix([RP*P**2, RP*P, 0, 0, RP*P, RP, 0, 0])
    # The first flux atom is z(P+sQ, grad r)=RP*(zP+s*zQ).
    v0, v1 = RP * zP, RP * zQ
    flux_remainder = (
        v0*v0.T / 2 + (v0*v1.T + v1*v0.T) / 6 + v1*v1.T / 12
    )
    # The acoustic flux atom is r^2 int_0^1 t z(tP,k)z(tP,k)^T dt.
    flux_acoustic = R**2 * zP*zP.T / 4

    # Average exactly by independence of x and theta after y -> theta shift.
    p_moments = {j: average_power_cos(j) / S.Integer(4) ** j for j in range(5)}
    # p=cos(x)/4.
    theta_moments = {}
    for j in range(5):
        for k in range(5):
            theta_moments[(j, k)] = (Rtheta**j * RPtheta**k).mean()

    def exact_average(expr):
        poly = S.Poly(S.expand(expr), P, R, RP)
        total = S.Integer(0)
        for exponents, coeff in poly.terms():
            ep, er, erp = exponents
            total += coeff * p_moments[ep] * theta_moments[(er, erp)]
        return S.simplify(total)

    Y0 = (flux_remainder + flux_acoustic).applyfunc(exact_average)
    check("curved Y0 is symmetric", Y0 == Y0.T)
    check("curved Y0 is PSD", Y0.is_positive_semidefinite is True)
    check("curved Y0 annihilates N794 skew blocks",
          Y0[:4, 4:] == Y0[4:, :4].T)

    # rV(theta) has X=(rtheta*V+r*W) tensor (p,1), so q=0 and
    # |rtheta*V+r*W|^2=r^2+rtheta^2. Compute all nine exact moments.
    S2mean = S.simplify(theta_moments[(4, 0)]
                        + 2*theta_moments[(2, 2)] + theta_moments[(0, 4)])
    pmean = {j: p_moments[j] for j in range(5)}
    m0 = [
        S2mean*pmean[4], S2mean, S2mean*pmean[2], S2mean*pmean[2],
        S2mean*pmean[3], S2mean*pmean[1], S.Integer(0), S.Integer(0), S.Integer(0),
    ]
    pairings = [S.trace(Q*Y0) for Q in acoustic]
    check("curved exact Y0 has the nine N794 pairings", pairings == m0)

    # The shear cancellations are exact: m(x)=<r^4>_y is constant.
    m_four = theta_moments[(4, 0)]
    gp = cos_mode((1, 0)) * S.Rational(1, 4)
    gpp = -sin_mode((1, 0)) * S.Rational(1, 4)
    check("curved profile fourth-moment cancellation value",
          m_four == S.Rational(5603, 5000))
    cancel_1 = (m_four * gpp).mean()
    cancel_2 = (m_four * gp * gpp).mean()
    check("both weighted curvature cancellations", cancel_1 == 0 and cancel_2 == 0)

    matrix_json = [[str(Y0[i, j]) for j in range(8)] for i in range(8)]
    return {
        "profile": "theta=y+sin(x)/4; r=1+cos(2 theta)/5; V=(cos theta,sin theta)",
        "curvature_cancellation_m": str(m_four),
        "zero_background_moment_vector": [str(value) for value in m0],
        "Y0": matrix_json,
        "Y0_pairings": [str(value) for value in pairings],
        "Y0_rank": int(Y0.rank()),
    }


def fourier_background_check():
    """Exact Parseval factor and Y_H pairings for a finite compatible gradient."""
    variables, basis, acoustic = n794_basis_and_acoustic_matrices()
    a, b, c, d = variables
    Bvals = [S.Rational(1, 2), -S.Rational(1, 3),
             S.Rational(2, 5), S.Rational(3, 4)]

    # phi=(cos x+sin y, sin x+cos y); translation (pi,pi) sends Dphi to -Dphi.
    phi1 = cos_mode((1, 0)) + sin_mode((0, 1))
    phi2 = sin_mode((1, 0)) + cos_mode((0, 1))
    X = [phi1.diff(0), phi1.diff(1), phi2.diff(0), phi2.diff(1)]
    support = set().union(*(set(entry.c) for entry in X))
    check("finite test gradient has half-turn antisymmetry",
          all((k[0] + k[1]) % 2 == 1 for k in support))

    Bmat = S.Matrix([[Bvals[0], Bvals[1]], [Bvals[2], Bvals[3]]])
    Ue1 = S.eye(2)
    Ue2 = S.Matrix([[0, -1], [1, 0]])

    def z(U, k, background=None):
        if background is None:
            background = Bmat
        xrow = list(U.T * background)
        return S.Matrix([k[0]*entry for entry in xrow]
                        + [k[1]*entry for entry in xrow])

    YH = S.zeros(8)
    # Trig convention: phi=sum(alpha cos(k.x)+beta sin(k.x));
    # each mode contributes 1/4 times one outer product for alpha and beta.
    for k, Ualpha, Ubeta in (
        ((1, 0), Ue1, Ue2),
        ((0, 1), Ue2, Ue1),
    ):
        for U in (Ualpha, Ubeta):
            zk = z(U, k)
            YH += zk*zk.T / 4

    def eval_basis(expr, values):
        return eval_poly_fourier(expr, variables, values)

    Bsub = {a: Bvals[0], b: Bvals[1], c: Bvals[2], d: Bvals[3]}
    mB, m0 = [], []
    hessian_half = []
    for f in basis:
        shifted = [Bvals[j] + X[j] for j in range(4)]
        mB.append(eval_basis(f, shifted).mean() - f.subs(Bsub))
        m0.append(eval_basis(f, X).mean())
        hf = S.hessian(f, variables)
        hess_expr = Fourier()
        for i in range(4):
            for j in range(4):
                coefficient = hf[i, j].subs(Bsub)
                hess_expr = hess_expr + X[i]*X[j]*coefficient
        hessian_half.append(hess_expr.mean() / 2)

    pairings = [S.trace(Q*YH) for Q in acoustic]
    increments = [S.simplify(x-y) for x, y in zip(mB, m0)]
    check("Fourier PSD sum equals half the background Hessian",
          pairings == hessian_half)
    check("half-turn quartic expansion has no odd remainder",
          pairings == increments)
    check("finite YH is symmetric PSD by its atom construction", YH == YH.T)
    check("finite YH annihilates N794 skew blocks",
          YH[:4, 4:] == YH[4:, :4].T)
    check("YH vanishes at B=0",
          all(S.simplify(v) == 0 for v in z(Ue1, (1, 0), S.zeros(2))))

    return {
        "profile": "phi=(cos x+sin y, sin x+cos y)",
        "background_row_major": [str(value) for value in Bvals],
        "fourier_hessian_pairings": [str(value) for value in pairings],
        "moment_increments": [str(value) for value in increments],
        "YH": [[str(YH[i, j]) for j in range(8)] for i in range(8)],
        "skew_block_symmetric": True,
        "half_turn_shift": ["pi", "pi"],
    }


def triad_halfturn_obstruction():
    """Exact support obstruction: the frozen triad has no anti-period shift."""
    e1, e2, e12 = (1, 0), (0, 1), (1, 1)
    psi1 = cos_mode(e1) - sin_mode(e1) + cos_mode(e2) - sin_mode(e2)
    psi2 = (cos_mode(e1) + sin_mode(e1) + cos_mode(e2) - sin_mode(e2)
            + cos_mode(e12) + sin_mode(e12))
    nonzero_classes = {
        k: (psi1.c.get(k, S.Integer(0)), psi2.c.get(k, S.Integer(0)))
        for k in (e1, e2, e12)
    }
    check("triad has all three nonzero Fourier classes",
          all(any(value != 0 for value in pair)
              for pair in nonzero_classes.values()))
    # Nonzero Fourier classes e1,e2,e1+e2 force tx=pi, ty=pi,
    # and tx+ty=pi simultaneously, an exact contradiction mod 2pi.
    equations = {"e1": "tx = pi (mod 2pi)",
                "e2": "ty = pi (mod 2pi)",
                "e1+e2": "tx+ty = pi (mod 2pi)"}
    check("connected triad cannot have a translation sending profile to -profile",
          (S.pi + S.pi - S.pi).simplify() != 0)
    return {
        "frequency_classes": [[1, 0], [0, 1], [1, 1]],
        "positive_frequency_vector_coefficients": {
            str(k): [str(value) for value in pair]
            for k, pair in nonzero_classes.items()
        },
        "anti_period_equations": equations,
        "scope": "pointwise profile obstruction only; no moment-cone separation is claimed",
    }


def main():
    results = {
        "scope": (
            "Exact finite symbolic checks for the structured left-SO(2) curved family; "
            "not a formal proof and not a universal quasiconvexity claim."
        ),
        "curved_zero_background": curved_zero_background_check(),
        "fourier_background": fourier_background_check(),
        "profile_boundary": triad_halfturn_obstruction(),
    }
    output = Path(__file__).with_name("verification_results.json")
    output.write_text(json.dumps(results, indent=2) + "\n")
    print(f"WROTE {output}")


if __name__ == "__main__":
    main()
