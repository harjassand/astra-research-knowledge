"""Finite checks for the critical-spin construction. These are not proofs.

Only numpy, sympy, and mpmath are required; no network or quantum library.
"""
from __future__ import annotations

import itertools
import json
import math
from fractions import Fraction
from pathlib import Path

import mpmath as mp
import numpy as np
import sympy as sy


def kron_all(mats):
    out = np.array([1.0 + 0.0j])
    for mat in mats:
        out = np.kron(out, mat)
    return out


def spin_operators(N):
    paulis = [np.array([[0, 1], [1, 0]], complex),
              np.array([[0, -1j], [1j, 0]], complex),
              np.diag([1, -1]).astype(complex)]
    eye = np.eye(2)
    Js = []
    for sigma in paulis:
        J = np.zeros((2**N, 2**N), complex)
        for i in range(N):
            factors = [eye] * N
            factors[i] = sigma / 2
            J += kron_all(factors)
        Js.append(J)
    return Js


def exact_permutation_twirl(N, j2, theta, phi):
    """Enumerate tiny-N permutations and compare with the full sector state."""
    chi = np.array([math.cos(theta/2),
                    np.exp(1j*phi)*math.sin(theta/2)])
    singlet = np.array([0, 1, -1, 0], complex) / math.sqrt(2)
    factors = [chi] * j2 + [singlet] * ((N-j2)//2)
    v = kron_all(factors)
    rho = np.zeros((2**N, 2**N), complex)
    tensor = v.reshape((2,) * N)
    for permutation in itertools.permutations(range(N)):
        w = tensor.transpose(permutation).reshape(-1)
        rho += np.outer(w, w.conj())
    rho /= math.factorial(N)
    Js = spin_operators(N)
    Jsq = sum(J@J for J in Js)
    direction = [math.sin(theta)*math.cos(phi),
                 math.sin(theta)*math.sin(phi), math.cos(theta)]
    Ju = sum(t*J for t, J in zip(direction, Js))
    j = j2 / 2
    # The zero-eigenspace is jointly J^2=j(j+1), J_u=j.
    constraint = (Jsq-j*(j+1)*np.eye(2**N)) @ (Jsq-j*(j+1)*np.eye(2**N))
    constraint += (Ju-j*np.eye(2**N)) @ (Ju-j*np.eye(2**N))
    values, vectors = np.linalg.eigh(constraint)
    basis = vectors[:, values < 1e-8]
    expected_mult = (math.comb(N, (N-j2)//2)
                     - (math.comb(N, (N-j2)//2-1)
                        if (N-j2)//2 else 0))
    assert basis.shape[1] == expected_mult
    target = basis @ basis.conj().T / expected_mult
    trace_error = sum(abs(np.linalg.eigvalsh(rho-target))) / 2
    return dict(N=N, j=j, direction=direction,
                multiplicity=expected_mult, trace_error=float(trace_error))


def exact_rotation_coefficients():
    x = sy.Symbol('x')
    def haar_monomial(k):
        if k % 2:
            return Fraction(0)
        q = k//2
        return Fraction(math.comb(2*q, q), (q+1)*4**q)
    answers = []
    for n in range(13):
        normalization = haar_monomial(2*n)
        for ell in range(n+1):
            char = sy.Poly(sy.chebyshevu(2*ell, x), x)
            got = sum(Fraction(int(c))*haar_monomial(int(k)+2*n)
                      for (k,), c in char.terms()) / normalization / (2*ell+1)
            expected = Fraction(math.factorial(n)*math.factorial(n+1),
                                math.factorial(n-ell)*math.factorial(n+ell+1))
            assert got == expected, (n, ell, got, expected)
            answers.append([n, ell, str(got)])
    return dict(exact_cases=len(answers), all_equal=True)


def sector_data(N):
    js = np.arange(N % 2 / 2, N/2+1, dtype=float)
    k = js + .5
    L = N+1
    loga = (2*np.log(2*k)-math.log(L)
            + math.lgamma(L+1)
            - np.array([math.lgamma(L/2-x+1) for x in k])
            - np.array([math.lgamma(L/2+x+1) for x in k])
            + 2*js*(js+1)/N)
    loga -= np.max(loga)
    return js, k/N**.75, np.exp(loga)


def finite_preparation_certificate(N, M=.1, B=.2):
    js, rs, weights = sector_data(N)
    M0 = 2*M  # A safe public traceless-part bound.
    delta = 3*M0*(js+.5)/N**1.5 + B/N**.75
    tilt = M*rs**2+B*rs
    denominator = np.sum(weights*np.exp(-tilt))
    upper = weights*np.exp(tilt+delta)
    F1, F2, F3 = [float(np.sum(upper*js**q)/denominator)
                  for q in (1, 2, 3)]
    coherent = 3*math.pi**2/16 * (
        (4*M0+2*B**2)*F1/N**1.5 + B/N**.75
        + 8*M0**2*(F3+F2)/N**3)
    symbol = float(np.sum(weights*np.exp(tilt)*np.expm1(delta))/denominator)
    return dict(N=N, M=M, B=B, coherent_bound=coherent,
                symbol_bound=symbol, total_bound=min(1.0, coherent+symbol),
                N_3_4_times_bound=(coherent+symbol)*N**.75,
                normalized_moment_1=F1/N**.75,
                normalized_moment_2=F2/N**1.5,
                normalized_moment_3=F3/N**2.25)


def radial_jitter_tv(N):
    js, rs, a = sector_data(N)
    probs = a / np.sum(a)
    delta = N**(-.75)
    lo = rs-delta/2
    hi = rs+delta/2
    lo[0] = 0
    width = hi-lo
    nodes, weights = np.polynomial.legendre.leggauss(48)
    x = (lo[:, None]+hi[:, None])/2 + width[:, None]*nodes[None, :]/2
    Z0 = .25*(.75**.75)*math.gamma(.75)
    p0 = x*x*np.exp(-4*x**4/3)/Z0
    cell_density = probs[:, None] / width[:, None]
    tv_inside = float(np.sum(np.abs(cell_density-p0)*width[:, None]*weights[None, :]/2)/2)
    tail = float(mp.gammainc(mp.mpf('.75'), 4*hi[-1]**4/3, mp.inf) / mp.gamma(mp.mpf('.75')))/2
    return dict(N=N, jitter_TV=tv_inside+tail,
                sqrt_N_times_TV=(tv_inside+tail)*math.sqrt(N))


def leading_radial_constant():
    mp.mp.dps = 40
    Er2 = mp.sqrt(mp.mpf(3)/4)*mp.gamma(mp.mpf(5)/4)/mp.gamma(mp.mpf(3)/4)
    EL = 2*Er2
    roots = sorted(math.sqrt(float(r.real)) for r in
                   np.roots([32/15, 0, -4, float(EL)])
                   if abs(r.imag) < 1e-10 and r.real > 0)
    Z0 = mp.mpf(1)/4*(mp.mpf(3)/4)**(mp.mpf(3)/4)*mp.gamma(mp.mpf(3)/4)
    f = lambda r: r*r*mp.exp(-mp.mpf(4)/3*r**4)/Z0
    correction = lambda r: 4*r*r-mp.mpf(32)/15*r**6
    C0 = mp.quad(lambda r: abs(correction(r)-EL)*f(r), [0, *roots, mp.inf])/2
    return dict(EL=float(EL), positive_roots=roots,
                limiting_sqrt_N_TV=float(C0))


def coherent_channel(j2, tau):
    """Exact-degree coherent quadrature, used only at small spin."""
    n = j2
    if n == 0:
        return tau.copy()
    z, wz = np.polynomial.legendre.leggauss(n+1)
    phi = np.arange(2*n+1)*2*math.pi/(2*n+1)
    zgrid = np.repeat(z, len(phi))
    phigrid = np.tile(phi, len(z))
    c = np.sqrt((1+zgrid)/2)
    s = np.sqrt((1-zgrid)/2)
    V = np.array([math.sqrt(math.comb(n, k))*c**(n-k)*s**k*np.exp(1j*k*phigrid)
                  for k in range(n+1)])
    w = np.repeat(wz/2/len(phi), len(phi))
    q = np.real(np.sum(V.conj()*(tau@V), axis=0))
    return (V*((n+1)*w*q)[None, :]) @ V.conj().T


def noncommuting_small_check(N, j2):
    j = j2/2
    m = np.arange(j, -j-1, -1)
    Jz = np.diag(m)
    plus = np.zeros((j2+1, j2+1), complex)
    for k in range(1, j2+1):
        plus[k-1, k] = math.sqrt((j-m[k])*(j+m[k]+1))
    Jx = (plus+plus.conj().T)/2
    Jy = (plus-plus.conj().T)/2j
    A = np.diag([.2, -.1, .05])
    b = np.array([.3, .1, .2])
    Js = [Jx, Jy, Jz]
    K = sum(A[k,k]*Js[k]@Js[k] for k in range(3))/N**1.5
    K += sum(b[k]*Js[k] for k in range(3))/N**.75
    vals, vecs = np.linalg.eigh(K)
    expvals = np.exp(vals-max(vals))
    tau = (vecs*expvals[None, :])@vecs.conj().T / sum(expvals)
    Btau = coherent_channel(j2, tau)
    error = sum(abs(np.linalg.eigvalsh(tau-Btau)))/2
    M0 = max(abs(np.linalg.eigvalsh(A-np.trace(A)*np.eye(3)/3)))
    field = float(np.linalg.norm(b))
    first = 2*M0*j*(j+1)/N**1.5+field*j/N**.75
    second = 4*M0*j*(j+1)/N**1.5+field*j/N**.75
    bound = 3*math.pi**2/(16*(j+1))*(second+first*first)
    assert abs(np.trace(Btau)-1) < 1e-10
    assert error <= bound+1e-10
    return dict(N=N, j=j, actual_trace_error=float(error), sector_bound=float(bound),
                quadrature_trace=float(np.trace(Btau).real))


def main():
    small = []
    for N in range(2, 7):
        for j2 in range(N % 2, N+1, 2):
            for theta, phi in [(0., 0.), (.9, .4)]:
                small.append(exact_permutation_twirl(N, j2, theta, phi))
    assert max(x['trace_error'] for x in small) < 1e-11
    data = dict(
        scope='Tiny-N identities and floating-point diagnostics; not proof or priority evidence.',
        permutation_twirl=dict(cases=len(small), max_trace_error=max(x['trace_error'] for x in small),
                               details=small),
        rotation_coefficients=exact_rotation_coefficients(),
        public_preparation_certificates=[finite_preparation_certificate(N) for N in
                                         [64, 256, 1024, 4096, 16384]],
        radial_rate=[radial_jitter_tv(N) for N in [64, 256, 1024, 4096, 16384]],
        leading_radial_constant=leading_radial_constant(),
        noncommuting_sectors=[noncommuting_small_check(N, j2) for N,j2 in
                              [(16, 8), (32, 12), (64, 20), (128, 30)]]
    )
    target = Path(__file__).with_name('spin_glass_checks.json')
    target.write_text(json.dumps(data, indent=2))
    print(json.dumps({key: value for key,value in data.items() if key != 'permutation_twirl'}, indent=2))
    print('Permutation twirl:', len(small), 'cases, max T=', max(x['trace_error'] for x in small))
    print('Saved', target)


if __name__ == '__main__':
    main()
