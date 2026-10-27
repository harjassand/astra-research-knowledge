#!/usr/bin/env python3
"""Continuum on-shell response to delta*(n_L-n_R) in the supplied ladder.

Only NumPy and the standard library are required. Uses the complete spectral
measures (bound atom AND continuum) and the odd-sector hard-core resolvent.
The output is a golden-rule coefficient, not an exponential-decay theorem.
"""
import json
import math
from pathlib import Path
import numpy as np
from numpy.polynomial.legendre import leggauss

BASE = Path(__file__).resolve().parent
A = 4 - 2 * math.sqrt(3)
B = 4 / math.sqrt(3) - 2


def surface(energy, centre):
    d = np.asarray(energy, dtype=float) - centre
    outer = abs(d) > 1
    root = np.sqrt(np.maximum(d*d - 1, 0))
    # Boundary value of (z-h_bath)^-1 from the UPPER half plane.
    value = 2*(d - 1j*np.sqrt(np.maximum(1-d*d, 0)))
    outer_den = np.where(outer, d + np.where(d >= 0, root, -root), 1.)
    value = np.where(outer, 2/outer_den, value)
    return value


def green(energy, centre, coupling2):
    return 1/(np.asarray(energy)-3-coupling2*surface(energy, centre))


def bisect(fun, lo, hi, iterations=100):
    a, b = fun(lo), fun(hi)
    if a*b > 0:
        raise ValueError((lo, hi, a, b))
    for _ in range(iterations):
        mid = (lo+hi)/2
        if mid in (lo, hi):
            break
        c = fun(mid)
        if a*c <= 0:
            hi, b = mid, c
        else:
            lo, a = mid, c
    return (lo+hi)/2


def density(energy, centre, coupling2):
    energy = np.asarray(energy)
    rho = 2/np.pi*np.sqrt(np.maximum(1-(energy-centre)**2, 0))
    return coupling2*rho*abs(green(energy, centre, coupling2))**2


def smooth_integral(fun, lo, hi, nq, cuts=()):
    """Split at declared branch points, then cosine-map every subinterval.

    This removes the leading square-root endpoint behavior; it is numerical
    quadrature, not interval certification.
    """
    t,w = leggauss(nq)
    theta = (t+1)*np.pi/2
    result = 0j
    edges = [lo]+sorted(set(p for p in cuts if lo<p<hi))+[hi]
    for a,b in zip(edges[:-1],edges[1:]):
        xx = (a+b)/2-(b-a)*np.cos(theta)/2
        ww = w*np.pi/2*(b-a)*np.sin(theta)/2
        result += np.sum(ww*fun(xx))
    return result


def measure(g, plus, nq):
    centre, coupling2 = (5., 2*g*g) if plus else (1., g*g)
    root = bisect(lambda x: float(np.real(1/green(x, centre, coupling2))),
                  2.0000001, 3.9999999)
    d = root-centre
    deriv = 2*(1-abs(d)/math.sqrt(d*d-1))
    weight = 1/(1-coupling2*deriv)
    t, w = leggauss(nq)
    theta = (t+1)*np.pi/2
    en = centre-np.cos(theta)
    wt = w*np.pi/2*np.sin(theta)*density(en, centre, coupling2)
    return dict(centre=centre, coupling2=coupling2, atom=root, residue=weight,
                energy=np.r_[root, en], weight=np.r_[weight, wt])


def lfun(z, mu, deriv=False):
    den = mu['energy'][:, None]+mu['energy'][None, :]-z
    return np.sum(mu['weight'][:, None]*mu['weight'][None, :]/
                  (den*den if deriv else den))


def compute(g, nq=160, perturbation='memory'):
    plus, minus = measure(g, True, nq), measure(g, False, nq)
    ep, em = plus['atom'], minus['atom']
    lam = bisect(lambda x: float(lfun(x, plus)+lfun(x, minus)),
                 2*ep+1e-11, 2*em-1e-11)
    norm_factor = math.sqrt(2/(lfun(lam, plus, True)+lfun(lam, minus, True)))

    def gp(x): return green(x, 5., 2*g*g)
    def gm(x): return green(x, 1., g*g)
    if perturbation == 'memory':
        hp,hm = gp,gm
        fp = lambda xx: np.ones_like(np.asarray(xx))
        fm = fp
    elif perturbation == 'first_rung':
        hp = lambda xx: ((np.asarray(xx)-3)*gp(xx)-1)/(math.sqrt(2)*g)
        hm = lambda xx: ((np.asarray(xx)-3)*gm(xx)-1)/g
        fp = lambda xx: (np.asarray(xx)-3)/(math.sqrt(2)*g)
        fm = lambda xx: (np.asarray(xx)-3)/g
    else:
        raise ValueError(perturbation)
    x, w = plus['energy'], plus['weight']
    y, v = minus['energy'], minus['weight']
    # K=<q_o,(H_harmonic,odd-lambda-i0)^-1 q_o>.
    intp = lambda fun: smooth_integral(lambda xx: density(xx,5.,2*g*g)*fun(xx),
                    4.,6.,nq,cuts=(lam,lam-2))
    intm = lambda fun: smooth_integral(lambda yy: density(yy,1.,g*g)*fun(yy),
                    0.,2.,nq,cuts=(lam-4,lam-6))
    kval = -plus['residue']*gm(lam-ep)-intp(lambda xx: gm(lam-xx))
    # C=<q_o,(H_harmonic,odd-lambda-i0)^-1 V psi_p>.
    cval = norm_factor*(plus['residue']*hp(lam-ep)*hm(lam-ep)+
                        minus['residue']*hm(lam-em)*hp(lam-em)+
                        intp(lambda xx: hp(lam-xx)*hm(lam-xx))+
                        intm(lambda yy: hm(lam-yy)*hp(lam-yy)))
    alpha = cval/kval

    jp = -hp(lam-x)
    jm = -hm(lam-y)
    eta_grid = norm_factor*(jp[:,None]*fm(y)[None,:]+fp(x)[:,None]*jm[None,:])
    eta_norm2 = float(np.sum(w[:,None]*v[None,:]*abs(eta_grid)**2))
    lp = lfun(lam,plus)
    lm = lfun(lam,minus)
    pair_overlap = float(-2*lp*lm/(lfun(lam,plus,True)+lfun(lam,minus,True)))
    bath_number = float(2-2*pair_overlap-eta_norm2) if perturbation == 'memory' else None

    lo, hi = max(4., lam-2), min(6., lam)
    t, q = leggauss(nq)
    theta = (t+1)*np.pi/2
    xs = (lo+hi)/2-(hi-lo)*np.cos(theta)/2
    ys = lam-xs
    shell_weight = q*np.pi/2*(hi-lo)*np.sin(theta)/2*density(xs, 5., 2*g*g)*density(ys, 1., g*g)
    eta = -norm_factor*(fm(ys)*hp(lam-xs)+fp(xs)*hm(lam-ys))
    s_hc = float(np.sum(shell_weight*abs(eta-alpha)**2))
    s_free = float(np.sum(shell_weight*abs(eta)**2))
    # Exact spectral identity Im K = pi * continuum shell density.
    shell_mass = float(np.sum(shell_weight))
    imk_check = abs(kval.imag-np.pi*shell_mass)
    # C's imaginary part is the eta-weighted shell density.
    imc_check = abs(cval.imag-np.pi*np.sum(shell_weight*eta).real)
    return dict(g=g, quadrature_nodes=nq, perturbation=perturbation, pair_energy=lam,
                onebody_plus=ep, onebody_minus=em,
                connected_shift=lam-ep-em,
                pair_normalizer=norm_factor,
                K_real=float(kval.real), K_imag=float(kval.imag),
                C_real=float(cval.real), C_imag=float(cval.imag),
                alpha_real=float(alpha.real), alpha_imag=float(alpha.imag),
                alpha_over_g2=float(alpha.real/g**2),
                detuning_vector_norm2=eta_norm2,
                detuning_vector_norm2_over_g2=eta_norm2/g**2,
                bare_pair_overlap=pair_overlap,
                pair_bath_population=bath_number,
                bath_population_over_g2=bath_number/g**2 if bath_number is not None else None,
                shell_eta_max=float(np.max(abs(eta))),
                spectral_density_hardcore=s_hc,
                spectral_density_if_constraint_omitted=s_free,
                probability_width_per_delta2=2*np.pi*s_hc,
                width_per_delta2_g8=2*np.pi*s_hc/g**8,
                predicted_small_g_coefficient=64*B*B/(27*np.pi) if perturbation=='memory' else None,
                imK_shell_identity_error=float(imk_check),
                imC_shell_identity_error=float(imc_check),
                measure_mass_errors=[float(abs(sum(p['weight'])-1)) for p in (plus,minus)])


def main():
    result = dict(
        perturbation='delta*(n_L-n_R), memory frequencies 3+delta and 3-delta',
        meaning='Gamma_probability=delta^2*coefficient+o(delta^2), conditional on resonance regularity',
        asymptotic='Gamma_probability ~ 64*(4/sqrt(3)-2)^2/(27*pi)*delta^2*g^8',
        cases=[compute(g) for g in [.4,.3,.2,.15,.1,.075,.05,.035]],
        convergence=[compute(.2, n) for n in [80,160,320]],
        source_revision='c1b8ac1516457a88b383a6350680e3be865fbffd')
    (BASE/'continuum_response_results.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
