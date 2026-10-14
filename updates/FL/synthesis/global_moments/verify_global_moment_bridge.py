#!/usr/bin/env python3
"""Exact checks for the modulation-to-moment-dual bridge and a profile obstruction.

Uses only SymPy exact Fourier arithmetic.  This is a finite symbolic check of
the displayed examples and coefficient map, not a formal proof of the general
integral identity.
"""
from __future__ import annotations

import json
from pathlib import Path

import sympy as S
from sympy import QQ_I


class Fourier:
    def __init__(self, coeff=None):
        self.c = {tuple(k): QQ_I.convert(v) for k, v in (coeff or {}).items() if v != 0}

    def __add__(self, other):
        if not isinstance(other, Fourier):
            other = Fourier({(0, 0): other})
        d = self.c.copy()
        for k, v in other.c.items():
            d[k] = d.get(k, QQ_I.zero) + v
        return Fourier({k: v for k, v in d.items() if v})

    __radd__ = __add__

    def __neg__(self):
        return Fourier({k: -v for k, v in self.c.items()})

    def __sub__(self, other):
        return self + (-other if isinstance(other, Fourier) else -S.sympify(other))

    def __mul__(self, other):
        if not isinstance(other, Fourier):
            return Fourier({k: v * QQ_I.convert(other) for k, v in self.c.items()})
        d = {}
        for k, v in self.c.items():
            for ell, w in other.c.items():
                m = (k[0] + ell[0], k[1] + ell[1])
                d[m] = d.get(m, QQ_I.zero) + v * w
        return Fourier({k: v for k, v in d.items() if v})

    __rmul__ = __mul__

    def __pow__(self, n):
        out = Fourier({(0, 0): 1})
        for _ in range(n):
            out = out * self
        return out

    def diff(self, j):
        return Fourier({k: v * QQ_I.convert(S.I * k[j]) for k, v in self.c.items()})

    def mean(self):
        z = QQ_I.to_sympy(self.c.get((0, 0), QQ_I.zero))
        assert S.im(z) == 0
        return S.re(z)

    def coefficient(self, k):
        return S.simplify(QQ_I.to_sympy(self.c.get(tuple(k), QQ_I.zero)))


def cos(k):
    return Fourier({k: S.Rational(1, 2), (-k[0], -k[1]): S.Rational(1, 2)})


def sin(k):
    return Fourier({k: 1 / (2 * S.I), (-k[0], -k[1]): -1 / (2 * S.I)})


def coeff_matrices():
    A, B, C, E, G, H, L, M, N = S.symbols("A B C E G H L M N")
    names = (A, B, C, E, G, H, L, M, N)
    M11 = S.Matrix([
        [12*A, 3*G, 0, 3*L],
        [3*G, 2*C+2*E, -L, N],
        [0, -L, 4*A, G],
        [3*L, N, G, 2*C],
    ])
    M12 = S.Matrix([
        [3*G, 2*C+2*E, -L, N],
        [2*C+2*E, 3*H, -N, M],
        [-L, -N, G, E],
        [N, M, E, H],
    ])
    M22 = S.Matrix([
        [2*C+2*E, 3*H, -N, M],
        [3*H, 12*B, -3*M, 0],
        [-N, -3*M, 2*C, H],
        [M, 0, H, 4*B],
    ])
    out = []
    for name in names:
        subs = {z: int(z == name) for z in names}
        Q = S.zeros(8)
        Q[:4, :4] = M11.subs(subs)
        Q[:4, 4:] = M12.subs(subs)
        Q[4:, :4] = M12.subs(subs)
        Q[4:, 4:] = M22.subs(subs)
        out.append(Q)
    return out


def main():
    # Exact rational 8x8 dual completion for r(x)V(y), r=1+cos(x)/2.
    xmode, ymode = (1, 0), (0, 1)
    r = Fourier({(0, 0): 1}) + S.Rational(1, 2) * cos(xmode)
    rx = r.diff(0)
    V1, V2 = cos(ymode), sin(ymode)
    aa, bb, cc, dd = rx*V1, -r*V2, rx*V2, r*V1
    u, v = aa**2 + cc**2, bb**2 + dd**2
    w, q = aa*bb + cc*dd, aa*dd - bb*cc
    basis = (u**2, v**2, u*v, w**2, u*w, v*w, q*u, q*v, q*w)
    m = [z.mean() for z in basis]
    assert m == [S.Rational(3,128), S.Rational(227,128), S.Rational(17,128), 0, 0, 0, 0, 0, 0]

    Y = S.zeros(8)
    Y[0, 0] = S.Rational(1, 512)
    Y[3, 3] = S.Rational(17, 256)
    Y[7, 7] = S.Rational(227, 512)
    Qs = coeff_matrices()
    pairings = [S.trace(Q * Y) for Q in Qs]
    assert pairings == m
    assert all(Y[i, i] >= 0 for i in range(8))
    # The only nonzero entries are diagonal, so each skew-block annihilator is zero.
    assert Y[:4, 4:] == Y[4:, :4].T

    # Exact connected-triad potential outside either positive profile template.
    # Frequencies: e1, e2, e1+e2, each present, with the primitive relation
    # e1 + e2 - (e1+e2) = 0.
    ex, ey, es = (1, 0), (0, 1), (1, 1)
    f = cos(ex) - sin(ex) + cos(ey) - sin(ey)
    g = cos(ex) + sin(ex) + cos(ey) - sin(ey) + cos(es) + sin(es)
    fx, fy, gx, gy = f.diff(0), f.diff(1), g.diff(0), g.diff(1)
    uu, vv = fx**2 + gx**2, fy**2 + gy**2
    ww, qq = fx*fy + gx*gy, fx*gy - fy*gx
    m_profile = [z.mean() for z in
                 (uu**2, vv**2, uu*vv, ww**2, uu*ww, vv*ww,
                  qq*uu, qq*vv, qq*ww)]
    assert m_profile == [S.Rational(27,2), S.Rational(31,2), S.Rational(19,2),
                         S.Rational(11,2), S.Rational(11,2), S.Rational(11,2),
                         0, -2, -1]
    X = (fx, fy, gx, gy)
    covariance = S.Matrix(4, 4, lambda i, j: (X[i]*X[j]).mean())
    assert covariance == S.Matrix([
        [1, 0, 0, 0],
        [0, 1, 0, 1],
        [0, 0, 2, 1],
        [0, 1, 1, 2],
    ])
    assert covariance.det() == 1
    assert ((uu+vv)**2).mean() == 48

    Dx, Dy = f*gx - g*fx, f*gy - g*fy
    coeffs = {
        "Dx_(1,2)": Dx.coefficient((1,2)),
        "Dy_(1,2)": Dy.coefficient((1,2)),
        "Dx_(0,1)": Dx.coefficient((0,1)),
        "Dy_(0,1)": Dy.coefficient((0,1)),
    }
    assert coeffs == {"Dx_(1,2)": S.I/2, "Dy_(1,2)": 0,
                      "Dx_(0,1)": 1, "Dy_(0,1)": S.Rational(1,2)}
    # If Phi=r V(p x+q y), det(Phi, q Phi_x-p Phi_y)=0.
    # These two Fourier coefficients force q=0 then p=0.
    phi_complex = f + S.I*g
    ky_support = sorted({k[1] for k, z in phi_complex.c.items() if z})
    assert ky_support == [-1, 0, 1]
    at00 = (S.Integer(2), S.Integer(3))
    atpi0 = (S.Integer(0), S.Integer(-1))
    assert at00[0]*atpi0[1] - at00[1]*atpi0[0] == -2

    result = {
        "scope": "Exact symbolic Fourier and rational dual-map checks; no universal theorem is machine-verified.",
        "modulation_example": {
            "profile": "r=1+cos(x)/2; V=(cos(y),sin(y)); B=0",
            "moment_vector": [str(z) for z in m],
            "dual_Y_nonzero_diagonal": {
                "1": str(Y[0,0]), "4": str(Y[3,3]), "8": str(Y[7,7])
            },
            "coefficient_pairings": [str(z) for z in pairings],
        },
        "connected_triad_obstruction": {
            "potential": {
                "phi1": "cos(x)-sin(x)+cos(y)-sin(y)",
                "phi2": "cos(x)+sin(x)+cos(y)-sin(y)+cos(x+y)+sin(x+y)",
            },
            "frequency_classes": [[1,0],[0,1],[1,1]],
            "primitive_relation": "(1,0)+(0,1)-(1,1)=0",
            "left_SO2_moment_vector_at_zero": [str(z) for z in m_profile],
            "covariance": [[str(covariance[i,j]) for j in range(4)] for i in range(4)],
            "covariance_determinant": str(covariance.det()),
            "fourth_gradient_moment": str(((uu+vv)**2).mean()),
            "phase_collinearity_fourier_coefficients": {k: str(v) for k,v in coeffs.items()},
            "complex_y_frequency_support": ky_support,
            "image_values_for_k_zero": [[str(z) for z in at00], [str(z) for z in atpi0]],
        },
    }
    out = Path(__file__).with_name("verification_results.json")
    out.write_text(json.dumps(result, indent=2) + "\n")
    print("PASS exact modulation moment vector and 8x8 PSD completion")
    print("PASS exact connected-triad moments, covariance, and nonmodulation tests")
    print(f"WROTE {out}")


if __name__ == "__main__":
    main()
