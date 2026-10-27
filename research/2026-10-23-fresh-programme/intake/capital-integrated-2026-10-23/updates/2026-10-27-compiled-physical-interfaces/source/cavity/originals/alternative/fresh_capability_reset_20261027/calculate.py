#!/usr/bin/env python3
"""Passive planar-cavity chemical sensitivity. No molecular rate simulation.
Run with Python 3 + numpy. Model assumptions and proof are in RESULT.md.
"""
from __future__ import annotations
import json, math, time
from pathlib import Path
import numpy as np
from numpy.polynomial.legendre import leggauss

ROOT = Path(__file__).resolve().parent
KB_EV = 8.617333262145e-5
HBARC = 1.973269804593025e-7  # eV m
HBAR = 6.582119569509067e-16  # eV s
ZETA3 = 1.2020569031595942854
C0 = 3 / (32 * math.pi**2) + math.pi**2 / 480

def a_sum(tau):
    """Sum_{j>=1} A(j tau) using exchanged positive exponential sums.
    A(t)=1.5(t+1)e^-t + integral_t^infinity x^2/(exp(x)-1) dx.
    The m*tau>65 numerical tail is omitted. No interval arithmetic claimed.
    """
    m = np.arange(1, max(2, int(math.ceil(65/tau)))+1, dtype=float)
    z, d = np.exp(-m*tau), -np.expm1(-m*tau)
    pieces = (tau**2/m*z*(1+z)/d**3
              + 2*tau/m**2*z/d**2 + 2/m**3*z/d)
    z1, d1 = math.exp(-tau), -math.expm1(-tau)
    return float(1.5*(tau*z1/d1**2 + z1/d1) + np.sum(pieces))

def bound(L, T=300):
    tau = 4*math.pi*L*KB_EV*T/HBARC
    B = a_sum(tau)/(8*math.pi)
    return dict(L_m=L, T_K=T, tau=tau, metal_B=B,
                general_B=B+(1.5+2*ZETA3)/(16*math.pi),
                meaning='abs(delta_mu)/(kBT) <= C*B/(n*L^3)',
                required_C_over_n_m3_for_factor10=math.log(10)*L**3/B)

def fsum_bound(L, T=300):
    """Density-free corollary for independent additive A/B polarizabilities.
    Requires mpmath. The bound is per effective charge count of A+B.
    No actual molecule or measured polarizability is asserted.
    """
    from mpmath import mp
    with mp.workdps(35):
        kb=mp.mpf('1.380649e-23'); hb=mp.mpf('1.054571817e-34')
        c=mp.mpf('299792458'); e=mp.mpf('1.602176634e-19')
        me=mp.mpf('9.1093837139e-31'); ep=mp.mpf('8.8541878188e-12')
        xi1=2*mp.pi*kb*T/hb
        volume=e**2/(ep*me*xi1**2)
        tau=2*mp.mpf(str(L))*xi1/c
        total=mp.mpf(0)
        for j in range(1,int(mp.ceil(65/tau))+1):
            t=j*tau; z=mp.exp(-t)
            A=(mp.mpf('1.5')*(t+1)*z-t*t*mp.log(1-z)
               +2*t*mp.polylog(2,z)+2*mp.polylog(3,z))
            total+=A/(j*j)
        per_z=volume*total/(8*mp.pi*mp.mpf(str(L))**3)
        return dict(L_m=L,T_K=T,weighted_A_sum=float(total),
                    volume_per_effective_charge_m3=float(volume),
                    beta_abs_delta_mu_bound_per_effective_charge=float(per_z),
                    effective_charge_count_required_for_factor10=float(mp.log(10)/per_z),
                    meaning='Z_eff=(m_e/e^2)*sum_{charges in A+B} q^2/m; beta abs(delta_mu) <= Z_eff * value')

def medium(E, s, E0, water, static=False):
    """Source Lorentz form, target damping=0. d epsilon/df=target chi.
    f denotes infinitesimal conversion with delta alpha=alpha_R. This is
    a declared response direction, not an acquired chemical reaction.
    E=hbar*xi in eV. Water parameters: Kotov et al SI V.
    """
    chi = np.full_like(E, s) if static else s*E0**2/(E0**2+E**2)
    if water:
        bg = 1+(77.46-1)/(1+E*11800e-15/HBAR)
        bg += 0.843*18.4**2/(18.4**2+E**2+13.5*E)
    else:
        bg = np.ones_like(E)
    return bg+chi, chi

def response(L, s, E0, T=300, water=True, static=False,
             order=180, cutoff=44, composition_f=0):
    """Full Fresnel derivative for identical Au Drude halfspaces.
    n=0 derivative is analytically zero for fixed Drude halfspaces and finite
    static gap permittivity. p=2Lq, tau*j=2L*xi_j/c. Returned B gives
    delta_mu/(kBT)=B/(n L^3). No source-figure reproduction claimed.
    """
    tau = 4*math.pi*L*KB_EV*T/HBARC
    jmax = int(math.ceil(cutoff/tau))
    nodes, weights = leggauss(order)
    p = ((nodes+1)*cutoff/2)[None,:]
    wp = (weights*cutoff/2)[None,:]
    prop, refl, free, max_eta = 0., 0., 0., 0.
    for start in range(1,jmax+1,128):
        j = np.arange(start,min(start+128,jmax+1),dtype=float)[:,None]
        t, E = tau*j, 2*math.pi*KB_EV*T*j
        eps, deps = medium(E,s,E0,water,static)
        eps = eps+composition_f*deps
        max_eta = max(max_eta,float(np.max(deps/eps)))
        epsm = 1+8.9**2/(E*(E+0.0357))
        z, zm = np.sqrt(p**2+eps*t**2), np.sqrt(p**2+epsm*t**2)
        dz = deps*t**2/(2*z)
        rs = (z-zm)/(z+zm)
        drs = 2*zm*dz/(z+zm)**2
        aa, bb = epsm*z, eps*zm
        rp = (aa-bb)/(aa+bb)
        drp = 2*(bb*epsm*dz-aa*deps*zm)/(aa+bb)**2
        u = np.exp(-z)
        pterm, rterm, fterm = np.zeros_like(z),np.zeros_like(z),np.zeros_like(z)
        for r,dr in ((rs,drs),(rp,drp)):
            den = 1-r**2*u
            pterm += r**2*dz*u/den
            rterm += -2*r*dr*u/den
            fterm += np.log1p(-r**2*u)
        prop += float(np.sum(wp*p*pterm))
        refl += float(np.sum(wp*p*rterm))
        free += float(np.sum(wp*p*fterm))
    norm = 8*math.pi
    return dict(L_m=L,s_static_susceptibility=s,E0_eV=E0,T_K=T,
                water_background=water,static_target_approx=static,
                quadrature_order=order,dimensionless_cutoff=cutoff,
                positive_Matsubara_terms=jmax,
                B_response=(prop+refl)/norm,
                B_propagation_only=prop/norm,B_Fresnel_response=refl/norm,
                positive_frequency_free_energy_times_L2_over_kBT=free/norm,
                sampled_max_eta=max_eta,
                meaning='delta_mu/(kBT)=B_response/(n L^3); delta_alpha=alpha_R')

def pointwise_check(samples=20000):
    """Finite diagnostic of the proved inequality, distinct mirrors included."""
    rng=np.random.default_rng(144271)
    eps=10**rng.uniform(0,10,samples)
    mirrors=10**rng.uniform(0,12,(2,samples))
    t,p=10**rng.uniform(-6,2,(2,samples))
    z=np.sqrt(p**2+eps*t**2)
    v=eps*t**2/(2*z**2)
    u=np.exp(-z)
    full=np.zeros(samples)
    for mode in ('s','p'):
        rs,drs=[],[]
        for em in mirrors:
            zm=np.sqrt(p**2+em*t**2)
            r=(z-zm)/(z+zm) if mode=='s' else (em*z-eps*zm)/(em*z+eps*zm)
            dr=(1-r**2)*(v if mode=='s' else v-1)/2
            rs.append(r); drs.append(dr)
        R=rs[0]*rs[1]
        dR=drs[0]*rs[1]+rs[0]*drs[1]
        full+=u*(R*z*v-dR)/(1-R*u)
    with np.errstate(over='ignore'):
        envelope=1.5*u+z/np.expm1(z)
    live=envelope>1e-270
    ratio=np.abs(full[live])/envelope[live]
    assert float(np.max(ratio))<=1+2e-9
    return dict(seed=144271,samples=samples,live_samples=int(np.sum(live)),
                max_abs_derivative_over_envelope=float(np.max(ratio)),
                status='PASS finite diagnostic; algebraic proof is separate')

def main():
    started=time.monotonic()
    bounds=[bound(L*1e-9) for L in (1,2,3,10,30,100,300,1000,5000,10000)]
    models=[]
    for resonance_gap in (100e-9,5000e-9):
        E0=math.pi*HBARC/resonance_gap
        for s in (0.04,1.,4.):
            for L in (10e-9,100e-9,5000e-9):
                models.append(response(L,s,E0))
    checks=dict(pointwise_envelope=pointwise_check())
    selected=dict(L=100e-9,s=1.,E0=math.pi*HBARC/100e-9)
    base=response(**selected)
    refined=response(**selected,order=300,cutoff=56)
    checks['quadrature_refinement']=dict(base_B=base['B_response'],
        refined_B=refined['B_response'],
        relative_difference=abs(base['B_response']/refined['B_response']-1))
    assert checks['quadrature_refinement']['relative_difference']<1e-7
    for row in models:
        assert abs(row['B_response'])<=bound(row['L_m'])['metal_B']*(1+1e-8)
    checks['model_cases_within_global_C1_bound']=len(models)
    h=1e-3
    plus=response(**selected,composition_f=h)
    minus=response(**selected,composition_f=-h)
    fd=(plus['positive_frequency_free_energy_times_L2_over_kBT']
        -minus['positive_frequency_free_energy_times_L2_over_kBT'])/(2*h)
    checks['central_difference']=dict(analytic_B=base['B_response'],finite_difference_B=fd,
        relative_difference=abs(fd/base['B_response']-1))
    assert checks['central_difference']['relative_difference']<1e-5
    ordinary=[]
    for L in (100e-9,1000e-9,5000e-9):
        args=dict(L=L,s=1.,E0=math.pi*HBARC/100e-9)
        exact,stat=response(**args),response(**args,static=True)
        ordinary.append(dict(L_m=L,exact_B=exact['B_response'],SSA_B=stat['B_response'],
            SSA_over_exact=stat['B_response']/exact['B_response']))
    results=dict(
        contract='homogeneous scalar passive gap; fixed mirror response; composition derivative of bulk-subtracted planar interplate free energy',
        source_parameters=dict(
            source='Kotov et al PRL 135,263601 (2025), Eq1,4; arXiv:2509.05156v2 SI Eq11,18 and following paragraph',
            Au_Drude_eV=dict(omega_p=8.9,gamma_D=0.0357),
            water=dict(epsilon_D=77.46,tau_fs=11800,f=0.843,omega0_eV=18.4,gamma0_eV=13.5),
            declared_variations='Au halfspaces; added oscillator damping=0; s=4(g/omega0)^2; bare resonant gaps100nm and5000nm. Model scans, not measured reactants or source-figure reproductions.',
            actual_reaction_spectrum_number_density_and_contrast='NOT_ACQUIRED'),
        bound_T0_constant=C0,bounds=bounds,model_cases=models,
        independent_molecule_fsum_bound=[fsum_bound(L) for L in (100e-9,1000e-9,5000e-9,10000e-9)],
        ordinary_static_screening_comparator=ordinary,checks=checks,
        elapsed_seconds=time.monotonic()-started,
        physical_operation='NOT_ACHIEVED',novelty='UNKNOWN; no priority claim')
    (ROOT/'results.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps(dict(bounds=bounds,checks=checks,ordinary=ordinary,
                         elapsed_seconds=results['elapsed_seconds']),indent=2))

if __name__=='__main__':
    main()
