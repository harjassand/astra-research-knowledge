#!/usr/bin/env python3
"""Independent exact compatible Fourier checks for the G tangent contact.

All fields are generated as gradients from two-phase Laurent modes.  The
anisotropic map (x,y) -> (x, N y) is a periodic covering, so constant-term
integration on the two phase torus is exact for every integer N.
"""
from __future__ import annotations

import json
from pathlib import Path
import sympy as sp

Laurent = dict[tuple[int, int], sp.Expr]


def plus(*items: Laurent) -> Laurent:
    out: Laurent = {}
    for item in items:
        for key, val in item.items():
            out[key] = sp.expand(out.get(key, 0) + val)
    return {k: sp.expand(v) for k, v in out.items() if v != 0}


def times(p: Laurent, q: Laurent) -> Laurent:
    out: Laurent = {}
    for (i, j), a in p.items():
        for (k, ell), b in q.items():
            key = (i + k, j + ell)
            out[key] = sp.expand(out.get(key, 0) + a * b)
    return {k: sp.expand(v) for k, v in out.items() if v != 0}


def scale(p: Laurent, c: sp.Expr) -> Laurent:
    return {k: sp.expand(c * v) for k, v in p.items() if c * v != 0}


def trig(mode: tuple[int, int], amplitude: sp.Expr, sine: bool = False) -> Laurent:
    amplitude = sp.sympify(amplitude)
    k = mode
    if sine:
        return {k: sp.cancel(amplitude / (2 * sp.I)),
                (-k[0], -k[1]): sp.cancel(-amplitude / (2 * sp.I))}
    return {k: amplitude / 2, (-k[0], -k[1]): amplitude / 2}


def average(p: Laurent) -> sp.Expr:
    return sp.factor(sp.cancel(p.get((0, 0), 0)))


def evaluate(expr: sp.Expr, entries: list[Laurent], variables: tuple[sp.Symbol, ...]) -> Laurent:
    out: Laurent = {}
    for powers, coeff in sp.Poly(sp.expand(expr), *variables).terms():
        term: Laurent = {(0, 0): coeff}
        for field, power in zip(entries, powers):
            for _ in range(power):
                term = times(term, field)
        out = plus(out, term)
    return out


a, b, c, d = sp.symbols("a b c d", real=True)
u, v, q = a*a + c*c, b*b + d*d, a*d - b*c
G = 3*(u + v - 2*q)**2 + sp.Rational(35, 24)*u**2 + q**2 - sp.Rational(5, 2)*q*u
variables = (a, b, c, d)
gradG = [sp.diff(G, x) for x in variables]
hessG = sp.hessian(G, variables)


def field(N: int, modes: list[tuple[tuple[int, int], sp.Expr, sp.Expr, sp.Expr, sp.Expr]]) -> list[Laurent]:
    """Mode rows: ((p,q), s_cos,s_sin,rho_cos,rho_sin).

    Physical frequency is (p,N*q), s is the e12 coefficient, and
    d-(3/2)a=N^-2*rho.  The associated output vector is chosen so each
    mode is exactly rank one and hence the sum is an actual periodic gradient.
    """
    eps = sp.cancel(1 / sp.sympify(N))
    A: Laurent = {}
    B: Laurent = {}
    C: Laurent = {}
    D: Laurent = {}
    for (p, qmode), sco, ssi, rco, rsi in modes:
        if qmode <= 0:
            raise ValueError("this parameterization requires positive slow y frequency")
        ratio = sp.Rational(p, qmode)
        smode = plus(trig((p, qmode), sco), trig((p, qmode), ssi, True))
        rmode = scale(plus(trig((p, qmode), rco), trig((p, qmode), rsi, True)), eps**2)
        amode = scale(smode, eps*ratio)
        dmode = plus(scale(amode, sp.Rational(3, 2)), rmode)
        cmode = scale(dmode, eps*ratio)
        A = plus(A, amode)
        B = plus(B, smode)
        C = plus(C, cmode)
        D = plus(D, dmode)
    return [A, B, C, D]


def run(N: int, p1: int, p2: int, amplitudes: tuple[sp.Expr, sp.Expr, sp.Expr],
        rho: tuple[sp.Expr, sp.Expr, sp.Expr] = (0, 0, 0)) -> dict:
    p3 = p1 + p2
    rows = [
        ((p1, 1), amplitudes[0], 0, rho[0], 0),
        ((p2, 1), amplitudes[1], 0, rho[1], 0),
        ((p3, 2), amplitudes[2], 0, rho[2], 0),
    ]
    entries = field(N, rows)
    bvec = sp.Matrix([average(evaluate(g, entries, variables)) for g in gradG])
    H = sp.Matrix([[average(evaluate(hessG[i, j], entries, variables))
                    for j in range(4)] for i in range(4)])
    cval = average(evaluate(G, entries, variables))
    cov = sp.Matrix([[average(times(entries[i], entries[j])) for j in range(4)]
                     for i in range(4)])
    sfield = entries[1]
    moments = []
    for j in (2, 3, 4):
        sj: Laurent = {(0, 0): sp.Integer(1)}
        for _ in range(j):
            sj = times(sj, sfield)
        moments.append(average(sj))
    A = sp.Matrix([1, 0, 0, 1])
    W = [sp.Matrix([1, 0, 0, -1]), sp.Matrix([0, 1, 0, 0]), sp.Matrix([0, 0, 1, 0])]
    Q = sp.Matrix.hstack(A, *W)
    Hb = Q.T * H * Q
    eb = Q.T * bvec
    # Pure-line affine regression ell=b-u H R.
    R = sp.Matrix([0, 1, 0, 0])
    ureg = sp.factor(moments[1] / (3*moments[0]))
    ell = bvec - ureg*H*R
    elb = Q.T * ell
    Dblock = Hb[1:, 1:]
    k = Hb[1:, 0]
    h = Hb[0, 0]
    hstar = sp.factor(h - (k.T * Dblock.inv() * k)[0])
    rstar = sp.factor(elb[0] - (k.T * Dblock.inv() * elb[1:, 0])[0])
    gap = sp.factor(cval - (bvec.T * H.inv() * bvec)[0] / 2)
    # Relative transverse norms for the fixed contact R=e12.
    Y2 = average(plus(times(entries[0], entries[0]), times(entries[2], entries[2]), times(entries[3], entries[3])))
    Y4_poly: Laurent = {}
    norm2: Laurent = {}
    for entry in entries:
        norm2 = plus(norm2, times(entry, entry))
    norm4 = times(norm2, norm2)
    Ynorm2 = plus(times(entries[0], entries[0]), times(entries[2], entries[2]), times(entries[3], entries[3]))
    Ynorm4 = times(Ynorm2, Ynorm2)
    Y4 = average(Ynorm4)
    delta2 = sp.sqrt(Y2/moments[0])
    delta4 = (Y4/moments[2])**sp.Rational(1, 4)
    ratio2 = sp.factor(rstar**2 / (hstar*moments[2]*delta2**2))
    ratio4 = sp.factor(rstar**2 / (hstar*moments[2]*delta4**2))
    return {
        "N": N, "m2": sp.factor(moments[0]), "m3": sp.factor(moments[1]), "m4": sp.factor(moments[2]),
        "covariance": [[sp.factor(cov[i,j]) for j in range(4)] for i in range(4)],
        "H": [[sp.factor(H[i,j]) for j in range(4)] for i in range(4)],
        "b": [sp.factor(x) for x in bvec], "c": sp.factor(cval),
        "ell": [sp.factor(x) for x in ell],
        "h": sp.factor(h), "hstar": hstar, "rstar": rstar, "gap": gap,
        "Y2": sp.factor(Y2), "Y4": sp.factor(Y4), "delta2_sq": sp.factor(delta2**2),
        "delta4_4": sp.factor(delta4**4), "ratio_using_delta2": ratio2,
        "ratio_using_delta4": ratio4,
    }


def main() -> None:
    profiles = {
        # Source-like three-mode tangent resonance.
        "source_positive_slopes": (1, 2, (sp.Integer(1), sp.Integer(1), sp.Rational(3, 2))),
        # Zero first-order covariance tilt, with a genuine all-a cubic resonance.
        "balanced_moving_frame": (1, -3, (sp.Integer(2), sp.Integer(1), sp.Integer(1))),
        # Another balanced profile with mixed signs and integer resonance.
        "balanced_high_slope": (2, -3, (sp.Rational(3, 2), sp.Integer(1), sp.Integer(1))),
    }
    output: dict[str, dict] = {}
    for name, (p1, p2, amp) in profiles.items():
        vals = {}
        for N in (4, 8, 16):
            result = run(N, p1, p2, amp)
            vals[str(N)] = {k: str(v) for k, v in result.items()}
        output[name] = vals
    path = Path(__file__).with_name("exact_tangent_triad.json")
    path.write_text(json.dumps(output, indent=2) + "\n")
    print(path)


if __name__ == "__main__":
    main()
