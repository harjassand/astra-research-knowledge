#!/usr/local/bin/python3
"""Fresh tensor/Fock and Gauss continuum checks; imports no candidate code.

Numerical results are diagnostics, not interval enclosures.  All source formulas
are reconstructed from the local ladder and the spectral theorem.
"""
import json
import math
from pathlib import Path

import numpy as np
import sympy as sy
from scipy.linalg import eigh
from scipy.optimize import brentq
from scipy.special import roots_legendre

OUT = Path(__file__).resolve().parent
G = 1 / 5


def symbolic_checks():
    rt = sy.sqrt(2)
    pp = sy.Matrix([sy.Rational(1, 2), 1 / rt, sy.Rational(1, 2)])
    mm = sy.Matrix([sy.Rational(1, 2), -1 / rt, sy.Rational(1, 2)])
    pm = sy.Matrix([1 / rt, 0, -1 / rt])
    v = sy.diag(2, 0, -2)
    assert sy.simplify(v * pp - rt * pm) == sy.zeros(3, 1)
    assert sy.simplify(v * mm - rt * pm) == sy.zeros(3, 1)
    assert sy.simplify((pp - mm) / rt) == sy.Matrix([0, 1, 0])
    assert v * sy.Matrix([0, 1, 0]) == sy.zeros(3, 1)
    x, E, kp, km = sy.symbols("x E kp km")
    # Three exact endpoint moments: 1, 3, 9+k.
    sp = 1 / x + (E - 3) / x**2 + ((E - 3)**2 + kp) / x**3
    sm = -1 / x - 3 / x**2 - (9 + km) / x**3
    expansion = sy.expand(sp + sm)
    assert sy.expand(expansion - (E - 6) / x**2 - (E**2 - 6 * E + kp - km) / x**3) == 0
    d = sy.symbols("d", positive=True)
    derivative = sy.simplify(sy.diff(d / sy.sqrt((2 + d)**2 - 1), d))
    assert sy.simplify(derivative - (2 * d + 3) / ((2 + d)**2 - 1)**sy.Rational(3, 2)) == 0
    ap = (215 + 4 * sy.sqrt(83)) / 85
    am = (335 - 2 * sy.sqrt(79)) / 105
    # Eliminate the radical in the bath Schur equation before checking atoms.
    def schur_polynomial(a, c, k):
        # r_c(a)=(3-a)/k, and r=1/(c-a-r/4).
        r = (3 - a) / k
        return sy.simplify(r * (c - a - r / 4) - 1)
    assert schur_polynomial(ap, 5, sy.Rational(2, 25)) == 0
    assert schur_polynomial(am, 1, sy.Rational(1, 25)) == 0
    p, t, b, K0, J0, Q0 = sy.symbols("p t b K0 J0 Q0")
    coincident = p*b*b/t + Q0 - (p*b/t + J0)**2/(p/t+K0)
    cancelled = Q0-2*b*J0+b*b*K0-(J0-b*K0)**2/(p/t+K0)
    assert sy.factor(coincident-cancelled) == 0
    return {
        "memory_source_factor": "V|++>=sqrt(2)|+->, V|-->=sqrt(2)|+->",
        "bare_pair_detuning_zero": True,
        "shell_source_moment_expansion": str(expansion),
        "pole_weight_monotonicity_derivative": str(derivative),
        "exact_atom_Schur_polynomial_checks": True,
        "coincident_atom_cancellation_identity": True,
    }


def local_onebody(n, g):
    dim = 2 + 2 * n
    h = 3 * np.eye(dim)
    direct = (1 + math.sqrt(2)) * g / 2
    crossed = (math.sqrt(2) - 1) * g / 2
    h[0, 2] = h[2, 0] = h[1, 2 + n] = h[2 + n, 1] = direct
    h[0, 2 + n] = h[2 + n, 0] = h[1, 2] = h[2, 1] = crossed
    for j in range(n):
        h[2 + j, 2 + n + j] = h[2 + n + j, 2 + j] = 2
    for j in range(n - 1):
        for offset in [2, 2 + n]:
            h[offset + j, offset + j + 1] = h[offset + j + 1, offset + j] = -.5
    return h


def tensor_fock_check(n, g=G):
    # Symmetric first-quantized tensor isometry; no occupation-loop builder.
    h = local_onebody(n, g)
    d = len(h)
    pairs = [(i, j) for i in range(d) for j in range(i, d)]
    isometry = np.zeros((d * d, len(pairs)))
    for col, (i, j) in enumerate(pairs):
        if i == j:
            isometry[d * i + j, col] = 1
        else:
            isometry[d * i + j, col] = isometry[d * j + i, col] = 1 / math.sqrt(2)
    Hharm = isometry.T @ (np.kron(h, np.eye(d)) + np.kron(np.eye(d), h)) @ isometry
    keep = [a for a, ij in enumerate(pairs) if ij not in [(0, 0), (1, 1)]]
    physical = [pairs[a] for a in keep]
    H = Hharm[np.ix_(keep, keep)]
    perm = np.r_[1, 0, np.arange(2 + n, 2 + 2 * n), np.arange(2, 2 + n)]
    lookup = {ij: a for a, ij in enumerate(physical)}
    S = np.zeros_like(H)
    for a, (i, j) in enumerate(physical):
        S[lookup[tuple(sorted((int(perm[i]), int(perm[j]))))], a] = 1
    s, W = eigh(S)
    Te, To = W[:, s > .5], W[:, s < -.5]
    evenvals, evenvectors = eigh(Te.T @ H @ Te)
    bare = np.zeros(len(H)); bare[lookup[(0, 1)]] = 1
    overlap = bare @ Te @ evenvectors
    idx = np.argmax(overlap**2)
    E = evenvals[idx]
    psi = Te @ evenvectors[:, idx]
    if bare @ psi < 0:
        psi = -psi
    Vdiag = np.array([int(i == 0) + int(j == 0) - int(i == 1) - int(j == 1) for i, j in physical])
    source = Vdiag * psi
    # Direct harmonic resolvent applied to the even forbidden vector.
    qe = np.zeros(len(pairs)); qe[pairs.index((0, 0))] = qe[pairs.index((1, 1))] = 1 / math.sqrt(2)
    dressed = np.linalg.solve(Hharm - E * np.eye(len(Hharm)), qe)
    dressed /= np.linalg.norm(dressed)
    if bare @ dressed[keep] < 0:
        dressed = -dressed
    pair_error = np.linalg.norm(dressed[keep] - psi)
    forbidden_error = max(abs(dressed[pairs.index((0, 0))]), abs(dressed[pairs.index((1, 1))]))
    # Independent spectral representation: use full h and its parity basis.
    Wone = np.zeros((d, d))
    Wone[0, 0] = Wone[1, 0] = 1 / math.sqrt(2)
    Wone[0, n + 1] = 1 / math.sqrt(2); Wone[1, n + 1] = -1 / math.sqrt(2)
    for j in range(n):
        Wone[2 + j, 1 + j] = Wone[2 + n + j, 1 + j] = 1 / math.sqrt(2)
        Wone[2 + j, n + 2 + j] = 1 / math.sqrt(2)
        Wone[2 + n + j, n + 2 + j] = -1 / math.sqrt(2)
    hparity = Wone.T @ h @ Wone
    xp, Up = eigh(hparity[:n + 1, :n + 1])
    ym, Um = eigh(hparity[n + 1:, n + 1:])
    wp, wm = Up[0]**2, Um[0]**2
    sumsp = xp[:, None] + xp[None, :]
    sumsm = ym[:, None] + ym[None, :]
    N = np.sum(np.outer(wp, wp) / (sumsp - E)**2) + np.sum(np.outer(wm, wm) / (sumsm - E)**2)
    C = math.sqrt(2 / N)
    Ap = np.sum(wp[None, :] / (sumsp - E), axis=1)
    Am = np.sum(wm[None, :] / (sumsm - E), axis=1)
    f = C * (Ap[:, None] + Am[None, :])
    mass = np.outer(wp, wm)
    energies = xp[:, None] + ym[None, :]
    oddH = To.T @ H @ To
    oddf = To.T @ source
    checks = []
    for epsilon in [.17, .023, .0017]:
        z = E + 1j * epsilon
        direct = oddf @ np.linalg.solve(oddH - z * np.eye(len(oddH)), oddf)
        D = np.sum(mass / (energies - z))
        B = np.sum(mass * f / (energies - z))
        A = np.sum(mass * f**2 / (energies - z))
        reduced = A - B**2 / D
        positive = np.sum(mass * epsilon * abs(f - B / D)**2 / ((energies - E)**2 + epsilon**2))
        checks.append({"epsilon": epsilon, "direct": [direct.real, direct.imag],
                       "resolvent_error": abs(direct - reduced),
                       "positive_identity_error": abs(direct.imag - positive)})
    return {"n": n, "g": g, "physical_dimension": len(H), "Ep": E,
            "parity_commutator": float(np.linalg.norm(H @ S - S @ H)),
            "pair_vector_reconstruction_error": float(pair_error),
            "harmonic_forbidden_overlap": float(forbidden_error),
            "source_norm": float(source @ source),
            "spectral_source_norm_error": float(abs(source @ source - np.sum(mass * f**2))),
            "spectral_source_forbidden_overlap": float(np.sum(mass * f)), "checks": checks}


def bath_physics(z, center):
    t = np.asarray(z, dtype=complex) - center
    root = np.sqrt(t - 1) * np.sqrt(t + 1)
    return 2 / (t + root)


def endpoint(z, center, k):
    return 1 / (3 - np.asarray(z) + k * bath_physics(z, center))


def quadrature_channel(center, k, n):
    # Gauss-Legendre in theta; this is continuum quadrature, not a Jacobi truncation.
    atom = brentq(lambda b: float(endpoint(b, center, k).real**-1),
                  2.8 if center == 5 else 3.00000001,
                  2.99999999 if center == 5 else 3.1, xtol=5e-15)
    t = atom - center
    bath_derivative = -abs(bath_physics(atom, center)) / math.sqrt(t*t - 1)
    atom_weight = float(1 / (1 - k * bath_derivative))
    z, w = roots_legendre(n)
    theta, dt = (z + 1) * math.pi / 2, w * math.pi / 2
    u, v = np.cos(theta), np.sin(theta)
    x = center + u
    mass = dt * 2 * k * v*v / (math.pi * ((3 - x + 2*k*u)**2 + 4*k*k*v*v))
    return np.r_[atom, x], np.r_[atom_weight, mass]


def split_integral(center, k, atom, weight, function, n, cuts=()):
    # Every atom is retained; split continuum thresholds before fixed-node quadrature.
    z, w = roots_legendre(n)
    intervals = [0., math.pi]
    intervals += [math.acos(x-center) for x in cuts if center-1 < x < center+1]
    intervals = sorted(set(intervals))
    result = weight * function(atom)
    for low, high in zip(intervals[:-1], intervals[1:]):
        th = low + (z + 1) * (high-low) / 2
        u, v = np.cos(th), np.sin(th)
        x = center + u
        mass = w * (high-low) / 2 * 2*k*v*v / (math.pi*((3-x+2*k*u)**2+4*k*k*v*v))
        result += np.sum(mass * function(x))
    return complex(result)


def continuum_check(n, g=G):
    kp, km = 2*g*g, g*g
    xp, wp = quadrature_channel(5, kp, n)
    ym, wm = quadrature_channel(1, km, n)
    sp, sm = xp[:, None] + xp[None, :], ym[:, None] + ym[None, :]
    Wp, Wm = np.outer(wp, wp), np.outer(wm, wm)
    def Ltotal(E):
        return np.sum(Wp/(sp-E)) + np.sum(Wm/(sm-E))
    E = brentq(Ltotal, 2*xp[0]+1e-8, 2*ym[0]-1e-8, xtol=5e-15)
    D = np.sum(Wp/(sp-E)**2) + np.sum(Wm/(sm-E)**2)
    C = math.sqrt(2/D)
    integ_p = lambda fn: split_integral(5,kp,xp[0],wp[0],fn,n,(E-2,E))
    integ_m = lambda fn: split_integral(1,km,ym[0],wm[0],fn,n,(E-6,E-4))
    M = integ_p(lambda x:endpoint(E-x,1,km))
    J = C*(integ_p(lambda x:endpoint(E-x,5,kp).real*endpoint(E-x,1,km))
           +integ_m(lambda y:endpoint(E-y,1,km).real*endpoint(E-y,5,kp)))
    alpha = J/M
    low, high = max(4.,E-2), min(6.,E)
    z, w = roots_legendre(n)
    theta, dt = (z+1)*math.pi/4, w*math.pi/4
    x = low+(high-low)*np.sin(theta)**2
    y = E-x
    def density(x,c,k):
        u=x-c
        rad=np.sqrt(np.maximum(0.,1-u*u))
        return 2*k*rad/(math.pi*((3-x+2*k*u)**2+4*k*k*rad*rad))
    weight=dt*2*(high-low)*np.sin(theta)*np.cos(theta)*density(x,5,kp)*density(y,1,km)
    shell_source=C*(endpoint(E-x,5,kp).real+endpoint(x,1,km).real)
    rho=float(np.sum(weight*abs(shell_source-alpha)**2))
    shellmass=float(np.sum(weight))
    mean=np.sum(weight*shell_source)/shellmass
    variance=float(np.sum(weight*(shell_source-mean)**2))
    # Direct continuum quadrature source norm includes all four measure pieces.
    Ap = np.sum(Wp/(sp-E),axis=1)/wp
    Am = np.sum(Wm/(sm-E),axis=1)/wm
    source=C*(Ap[:,None]+Am[None,:])
    oddmass=np.outer(wp,wm)
    return {"Gauss_nodes_per_piece":n,"g":g,"Ep":float(E),"D":float(D),"C":C,
            "complete_measure_masses":[float(wp.sum()),float(wm.sum())],
            "endpoint_second_moments":[float(np.dot(wp,xp*xp)),float(np.dot(wm,ym*ym))],
            "source_norm":float(np.sum(oddmass*source*source)),
            "source_forbidden_overlap":float(np.sum(oddmass*source)),
            "M":[M.real,M.imag],"J":[J.real,J.imag],"alpha":[alpha.real,alpha.imag],
            "rho":rho,"uncorrected_shell_density":float(np.sum(weight*shell_source**2)),
            "weighted_variance":variance,
            "optical_M_error":float(M.imag-math.pi*shellmass),
            "optical_J_error":float(J.imag-math.pi*np.sum(weight*shell_source)),
            "shell_source_range":[float(shell_source.min()),float(shell_source.max())]}


if __name__ == "__main__":
    result = {"symbolic":symbolic_checks(),
              "tensor_fock":[tensor_fock_check(n) for n in [3,5,7]],
              "continuum":[continuum_check(n) for n in [64,128,256,512,1024]]}
    (OUT/"independent_checks.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))
