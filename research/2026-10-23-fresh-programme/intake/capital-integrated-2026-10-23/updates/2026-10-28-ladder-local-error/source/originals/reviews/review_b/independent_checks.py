#!/usr/local/bin/python3
"""Reviewer B's independent diagnostics; imports no endpoint implementation.

Fixed Gaussian quadrature of complete endpoint measures, an exact small
compression check, and pointwise source reconstruction in the original rails.
These numerical diagnostics are not interval enclosures or lifetime evidence.
"""
from pathlib import Path
import json
import math
from functools import lru_cache

import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.linalg import eigh, eigh_tridiagonal
from scipy.optimize import brentq

ROOT = Path(__file__).resolve().parent
G = 1 / 5


@lru_cache(None)
def rule(n):
    u, w = leggauss(n)
    return (u + 1) * math.pi / 4, w * math.pi / 4


class Measure:
    def __init__(self, c, k, n):
        self.c, self.k, self.n = c, k, n
        self.atom = brentq(lambda x: (3-x-k*self.bath(x)).real,
                           *( (2.8, 3.) if c == 5 else (3., 3.1) ),
                           xtol=5e-15)
        self.mass = float((1/(1+k*self.bath_prime(self.atom))).real)

    def bath(self, z):
        t = np.asarray(z, dtype=complex) - self.c
        root = np.sqrt(t-1)*np.sqrt(t+1)
        return -2/(t+root)

    def bath_prime(self, z):
        t = np.asarray(z, dtype=complex) - self.c
        root = np.sqrt(t-1)*np.sqrt(t+1)
        return 2/(root*(t+root))

    def memory(self, z):
        return 1/(3-z-self.k*self.bath(z))

    def memory_prime(self, z):
        return (1+self.k*self.bath_prime(z))*self.memory(z)**2

    def density(self, x):
        t = np.asarray(x)-self.c
        q = np.sqrt(np.maximum(0, 1-t*t))
        return 2*self.k*q/(math.pi*((3-x+2*self.k*t)**2+4*self.k**2*q*q))

    def cont(self, fn, cuts=()):
        edges = sorted(set([self.c-1, self.c+1] +
                           [float(v) for v in cuts if self.c-1 < v < self.c+1]))
        theta, weights = rule(self.n)
        s, c = np.sin(theta), np.cos(theta)
        total = 0j
        for a, b in zip(edges[:-1], edges[1:]):
            x = a+(b-a)*s*s
            total += np.dot(weights, self.density(x)*fn(x)*2*(b-a)*s*c)
        return total

    def integrate(self, fn, cuts=()):
        return self.mass*fn(self.atom)+self.cont(fn, cuts)

    def L(self, E):
        return float(self.integrate(lambda x: self.memory(E-x)).real)


def continuum(n):
    p, m = Measure(5, 2*G*G, n), Measure(1, G*G, n)
    E = brentq(lambda e: p.L(e)+m.L(e), 2*p.atom+1e-9, 2*m.atom-1e-9,
               xtol=5e-15)
    D = float((p.integrate(lambda x: p.memory_prime(E-x))+
               m.integrate(lambda y: m.memory_prime(E-y))).real)
    C = math.sqrt(2/D)
    a, b = lambda x: p.memory(E-x).real, lambda y: m.memory(E-y).real
    K = p.integrate(lambda x: m.memory(E-x), (E-2, E))
    J = p.integrate(lambda x: a(x)*m.memory(E-x), (E-2, E))
    J += m.integrate(lambda y: b(y)*p.memory(E-y), (E-6, E-4))
    alpha = J/K
    theta, weights = rule(n)
    lo, hi = max(4., E-2), min(6., E)
    x = lo+(hi-lo)*np.sin(theta)**2
    shell_weight = p.density(x)*m.density(E-x)*2*(hi-lo)*np.sin(theta)*np.cos(theta)
    U = a(x)+m.memory(x).real
    shell = lambda fn: float(np.dot(weights, shell_weight*fn))
    rho = C*C*shell(abs(U-alpha)**2)
    shell0, shell1, shell2 = shell(np.ones_like(U)), shell(U), shell(U*U)
    Kbb = p.mass*m.mass/(p.atom+m.atom-E)
    Jbb = Kbb*(a(p.atom)+b(m.atom))
    Kbc = p.mass*m.cont(lambda y: 1/(p.atom+y-E))
    Kcb = m.mass*p.cont(lambda x: 1/(x+m.atom-E))
    Jbc = p.mass*m.cont(lambda y: (a(p.atom)+b(y))/(p.atom+y-E))
    Jcb = m.mass*p.cont(lambda x: (a(x)+b(m.atom))/(x+m.atom-E))
    # Independent atom-subtracted evaluation. The unsplit formula separately
    # samples two near odd atom poles and can amplify atom/root roundoff when
    # their large contributions cancel. In this decomposition the common
    # bound-bound denominator is evaluated once in both K and J.
    regm = lambda z: m.memory(z)-m.mass/(m.atom-z)
    regp = lambda z: p.memory(z)-p.mass/(p.atom-z)
    Kcc_stable = p.cont(lambda x: regm(E-x), (E-2, E))
    Jcc_stable = p.cont(lambda x: a(x)*regm(E-x), (E-2, E))
    Jcc_stable += m.cont(lambda y: b(y)*regp(E-y), (E-6, E-4))
    Kstable = Kbb+Kbc+Kcb+Kcc_stable
    Jstable = Jbb+Jbc+Jcb+Jcc_stable
    alpha_stable = Jstable/Kstable
    alpha_no_bb = (J-Jbb)/(K-Kbb)
    alpha_cc = (J-Jbb-Jbc-Jcb)/(K-Kbb-Kbc-Kcb)
    moments = {}
    for name, ch in [('plus', p), ('minus', m)]:
        moments[name] = [float(ch.integrate(lambda x, j=j: x**j).real)
                         for j in range(3)]
    norm = C*C*(p.integrate(lambda x: a(x)**2).real+
                 m.integrate(lambda y: b(y)**2).real+2*p.L(E)*m.L(E))
    return dict(order_per_segment=n, Ep=E, Eplus=p.atom, Eminus=m.atom, D=D,
                C=C, pair_root_residual=p.L(E)+m.L(E),
                source_norm_squared=float(norm), moments=moments,
                K=[float(K.real), float(K.imag)],
                J_unscaled=[float(J.real), float(J.imag)],
                alpha_unscaled=[float(alpha.real), float(alpha.imag)],
                stable_alpha_unscaled=[float(alpha_stable.real), float(alpha_stable.imag)],
                stable_rho=C*C*shell(abs(U-alpha_stable)**2),
                unsplit_minus_stable_rho=rho-C*C*shell(abs(U-alpha_stable)**2),
                unsplit_minus_stable_J=float((J-Jstable).real),
                K_bound_bound=float(Kbb), J_bound_bound=float(Jbb),
                optical_K_residual=float(K.imag-math.pi*shell0),
                optical_J_residual=float(J.imag-math.pi*shell1),
                rho=rho, uncompressed_rho=C*C*shell2,
                weighted_variance=C*C*(shell2-shell1*shell1/shell0),
                rho_omitting_bb_in_correction=C*C*shell(abs(U-alpha_no_bb)**2),
                rho_using_only_cc_in_correction=C*C*shell(abs(U-alpha_cc)**2),
                shell_U_min=float(U.min()), shell_U_max=float(U.max()))


def boson_matrix(h, basis):
    lookup = {q: i for i, q in enumerate(basis)}
    d, N = len(h), len(basis)
    H = np.zeros((N, N))
    for col, state in enumerate(basis):
        occ = np.bincount(state, minlength=d)
        for source in np.flatnonzero(occ):
            after = occ.copy()
            annihilate = math.sqrt(after[source])
            after[source] -= 1
            for dest in np.flatnonzero(h[:, source]):
                new = after.copy()
                amp = annihilate*math.sqrt(new[dest]+1)*h[dest, source]
                new[dest] += 1
                target = tuple(np.repeat(np.arange(d), new))
                if target in lookup:
                    H[lookup[target], col] += amp
    return H


def original_rail_source(n):
    d = 2+2*n
    h = np.diag(np.full(d, 3.))
    t, s = (1+math.sqrt(2))*G/2, (math.sqrt(2)-1)*G/2
    for i, j, v in [(0, 2, t), (1, 2+n, t), (0, 2+n, s), (1, 2, s)]:
        h[i, j] = h[j, i] = v
    for j in range(n):
        h[2+j, 2+n+j] = h[2+n+j, 2+j] = 2.
    for first in (2, 2+n):
        for j in range(n-1):
            h[first+j, first+j+1] = h[first+j+1, first+j] = -.5
    full = [(i, j) for i in range(d) for j in range(i, d)]
    loc = {q: k for k, q in enumerate(full)}
    H0 = boson_matrix(h, full)
    forbidden = [loc[(0, 0)], loc[(1, 1)]]
    allowed = [k for k in range(len(full)) if k not in forbidden]
    H = H0[np.ix_(allowed, allowed)]
    qe = np.zeros(len(full)); qe[forbidden] = 1/math.sqrt(2)
    qo = qe.copy(); qo[forbidden[1]] *= -1
    vdiag = np.array([2*(i == j == 0)-2*(i == j == 1)+
                      (i == 0 and j != 0)-(i == 1 and j != 1)+
                      (j == 0 and i != 0)-(j == 1 and i != 1)
                      for i, j in full], float)
    specs = []
    single_modes = []
    for parity in (1, -1):
        vals, U = eigh_tridiagonal(np.r_[3., np.full(n, 5 if parity == 1 else 1)],
                                  np.r_[math.sqrt(2)*G if parity == 1 else G,
                                        np.full(n-1, -.5)])
        P = np.zeros((d, n+1))
        P[0, 0], P[1, 0] = 1/math.sqrt(2), parity/math.sqrt(2)
        for j in range(n):
            P[2+j, 1+j], P[2+n+j, 1+j] = 1/math.sqrt(2), parity/math.sqrt(2)
        single_modes.append(P@U)
        specs.append((vals, U[0], U[0]**2))
    xp, ap, wp = specs[0]; ym, am, wm = specs[1]
    def L(x, w, E):
        return np.sum(w[:, None]*w[None, :]/(x[:, None]+x[None, :]-E))
    bp, bm = xp[np.argmax(wp)], ym[np.argmax(wm)]
    E = brentq(lambda e: L(xp, wp, e)+L(ym, wm, e), 2*bp+1e-9, 2*bm-1e-9,
               xtol=5e-15)
    D = sum(np.sum(w[:, None]*w[None, :]/(x[:, None]+x[None, :]-E)**2)
            for x, w in [(xp, wp), (ym, wm)])
    C = math.sqrt(2/D)
    psi = C*np.linalg.solve(H0-E*np.eye(len(full)), qe)
    ev, U = eigh(H)
    idx = np.argmin(abs(ev-E))
    direct = U[:, idx]
    if direct@psi[allowed] < 0:
        direct = -direct
    W = np.empty((len(full), len(xp)*len(ym)))
    for i, vp in enumerate(single_modes[0].T):
        for j, vm in enumerate(single_modes[1].T):
            W[:, i*len(ym)+j] = [math.sqrt(2)*vp[a]*vm[a] if a == b else
                                 vp[a]*vm[b]+vm[a]*vp[b] for a, b in full]
    A = np.sum(wp[None, :]/(xp[:, None]+xp[None, :]-E), axis=1)
    B = np.sum(wm[None, :]/(ym[:, None]+ym[None, :]-E), axis=1)
    fmode = (C*ap[:, None]*am[None, :]*(A[:, None]+B[None, :])).ravel()
    qmode = (ap[:, None]*am[None, :]).ravel()
    f = vdiag*psi
    fdir = vdiag[allowed]*direct
    sums = (xp[:, None]+ym[None, :]).ravel()
    rows = []
    for shift, eta in [(0., .037), (.121, .009), (-.08, .2)]:
        z = E+shift+1j*eta
        R = 1/(sums-z)
        reduced = np.dot(fmode*R, fmode)-np.dot(fmode*R, qmode)**2/np.dot(qmode*R, qmode)
        r_direct = fdir@np.linalg.solve(H-z*np.eye(len(H)), fdir)
        positive = np.sum(eta*abs(fmode-(np.dot(fmode*R, qmode)/
                            np.dot(qmode*R, qmode))*qmode)**2/abs(sums-z)**2)
        rows.append(dict(shift=shift, eta=eta, resolvent_difference=float(abs(reduced-r_direct)),
                         positive_identity_difference=float(abs(reduced.imag-positive))))
    return dict(n=n, dimension_physical=len(H), Ep=E,
                H_symmetry_residual=float(np.linalg.norm(H-H.T)),
                pair_norm=float(psi@psi),
                forbidden_norm=float(np.linalg.norm(psi[forbidden])),
                pair_vector_difference=float(np.linalg.norm(psi[allowed]-direct)),
                pair_eigen_residual=float(np.linalg.norm((H-E*np.eye(len(H)))@psi[allowed])),
                source_norm_squared=float(fdir@fdir),
                source_pointwise_difference=float(np.linalg.norm(W@fmode-f)),
                odd_tensor_isometry_residual=float(np.linalg.norm(W.T@W-np.eye(W.shape[1]))),
                forbidden_vector_difference=float(np.linalg.norm(W@qmode-qo)),
                source_forbidden_overlap=float(qmode@fmode), checks=rows)


def exact_small_check():
    import sympy as sp
    r2, I = sp.sqrt(2), sp.I
    hp = sp.Matrix([[3, r2/5], [r2/5, 5]])
    hm = sp.Matrix([[3, sp.Rational(1, 5)], [sp.Rational(1, 5), 1]])
    A = sp.kronecker_product(hp, sp.eye(2))+sp.kronecker_product(sp.eye(2), hm)
    z = sp.Rational(31, 5)+I/17
    R = (A-z*sp.eye(4)).inv()
    correction = R[1:, 1:]-R[1:, 0]*R[0, 1:]/R[0, 0]
    compressed = (A[1:, 1:]-z*sp.eye(3)).inv()
    residual = (correction-compressed).applyfunc(sp.simplify)
    qplus = sp.Matrix([sp.Rational(1, 2), 1/r2, sp.Rational(1, 2)])
    qminus = sp.Matrix([sp.Rational(1, 2), -1/r2, sp.Rational(1, 2)])
    qo = sp.Matrix([1/r2, 0, -1/r2])
    V = sp.diag(2, 0, -2)
    p = (qplus-qminus)/r2
    source_checks = [sp.simplify(V*qplus-r2*qo), sp.simplify(V*qminus-r2*qo),
                     sp.simplify(V*p)]
    assert residual == sp.zeros(3)
    assert all(v == sp.zeros(3, 1) for v in source_checks)
    return dict(compression_exact_zero=True, boson_factor_sqrt2_exact=True,
                bare_pair_V_exact_zero=True,
                complex_test_energy=str(z), odd_free_dimension=4)


if __name__ == '__main__':
    data = dict(exact=exact_small_check(),
                continuum=[continuum(n) for n in (24, 48, 96, 192, 384)],
                original_rail_fock=[])
    # The macOS BLAS build can retain floating flags from eigensolvers. Keep
    # the diagnostic numerical checks explicit, including a full finiteness
    # traversal, instead of treating those flags as proof of bad values.
    with np.errstate(divide='ignore', over='ignore', invalid='ignore'):
        data['original_rail_fock'] = [original_rail_source(n) for n in (3, 5, 7)]
    def finite_tree(value):
        if isinstance(value, dict):
            for item in value.values():
                finite_tree(item)
        elif isinstance(value, list):
            for item in value:
                finite_tree(item)
        elif isinstance(value, float):
            assert math.isfinite(value)
    finite_tree(data)
    for row in data['original_rail_fock']:
        assert abs(row['pair_norm']-1) < 2e-11
        assert max(row['source_pointwise_difference'], row['forbidden_norm'],
                   row['pair_vector_difference'], row['pair_eigen_residual']) < 2e-11
        assert max(x['resolvent_difference'] for x in row['checks']) < 2e-11
    for row in data['continuum']:
        assert row['rho'] > row['weighted_variance'] > 0
        assert max(abs(row['optical_K_residual']), abs(row['optical_J_residual'])) < 2e-11
    (ROOT/'independent_results.json').write_text(json.dumps(data, indent=2)+'\n')
    print(json.dumps(data, indent=2))
