"""ASTRA XH2 — mechanically meaningful regeneration: cohesive energy and seam ageing.

Synthetic mathematical models, not measured properties of GlcNAz-bacterial cellulose.
References: Chen et al. Nat Commun 2026 doi:10.1038/s41467-026-69130-8;
Liu et al. Nat Commun 2020 doi:10.1038/s41467-020-14871-3;
Crosslinking of fibrous hydrogels, Nat Commun 2018 doi:10.1038/s41467-018-04508-x.
"""
import numpy as np
from math import pi, log, exp, sqrt
from scipy.optimize import brentq


def single_layer_scission(traction=1e5, force=100e-12, bond_work=4e-19,
                          target_energy=.5):
    """Required load-bearing sites, energy from one severed bond each and amplification."""
    density=traction/force
    return dict(load_paths_per_um2=density/1e12,
                direct_scission_J_m2=density*bond_work,
                target_per_bond_work_J=target_energy/density,
                constant_force_sliding_m=target_energy/traction,
                triangular_delta_critical_m=2*target_energy/traction,
                amplification=target_energy/(density*bond_work))


def fibre_tail(traction=1e5, energy=.5, force=100e-12, radius_nm=5.,
               density_kg_m3=1500.):
    """Assumes parallel constant-force sliding tails, one per useful load path.
    These are necessary ideal geometric/material quantities, not a sufficient
    network design. Individual fibres cannot overlap in the nominal cross section.
    """
    areal_paths=traction/force
    r=radius_nm*1e-9
    length=energy/traction
    pack=areal_paths*pi*r*r
    mass_areal=density_kg_m3*areal_paths*pi*r*r*length
    return dict(areal_paths_per_um2=areal_paths/1e12,
                sliding_length_um=length*1e6,
                packing_fraction=pack,
                mass_ug_per_mm2=mass_areal*1000,
                feasible_by_packing=pack<=1)


def stacked_seams(n, fail_prob_per_exposure):
    exposures=n*(n+1)//2
    return (1-fail_prob_per_exposure)**exposures


def max_seam_hazard(n, target_reliability=.9):
    return 1-target_reliability**(2/(n*(n+1)))


def seam_survival(bonds, alpha=.25):
    """Synthetic hazard per cycle exp(-alpha * each seam's functional bonds).
    Seam index 0 is oldest and exposed to most service cycles.
    """
    b=np.array(bonds,dtype=float)
    assert np.all(b>=0)
    n=len(b)
    exposures=np.arange(n,0,-1)
    h=np.exp(-alpha*b)
    return float(np.exp(np.dot(exposures,np.log1p(-h))))


def optimal_seam_bond_allocation(n, total_bonds, alpha=.25):
    """Exact log-reliability maximizer: h_i = lambda/(alpha*exposure_i+lambda).
    If total_bonds>0 all b_i positive (b_i=0 leads certain first-cycle failure).
    Bond allocations are continuous normalized effective-bond units, not molecules.
    """
    L=np.arange(n,0,-1,dtype=float)
    def b_lambda(lamb):
        return np.log1p(alpha*L/lamb)/alpha
    lam=brentq(lambda x: b_lambda(x).sum()-total_bonds,1e-20,1e20)
    alloc=b_lambda(lam)
    assert abs(alloc.sum()-total_bonds)<1e-6
    return alloc,seam_survival(alloc,alpha)


def numerical_checks():
    x=single_layer_scission()
    assert abs(x['load_paths_per_um2']-1000)<1e-10
    assert abs(x['direct_scission_J_m2']-.0004)<1e-12
    assert abs(x['amplification']-1250)<1e-10
    assert abs(stacked_seams(10,.01)-.99**55)<1e-12
    for n in [3,5,10]:
        for B in [n*10,n*20]:
            b,optimal=optimal_seam_bond_allocation(n,B,.25)
            equal=seam_survival(np.ones(n)*B/n,.25)
            assert optimal>=equal-1e-9
            # derivative constant verifies KKT
            L=np.arange(n,0,-1)
            h=np.exp(-.25*b)
            marg=L*.25*h/(1-h)
            assert max(marg)-min(marg)<1e-7
    print('Closed-form bond-energy, exact seam-exposure, convex optimization and KKT tests passed.')


def report():
    numerical_checks()
    print('Single-junction load/energy bottleneck:',single_layer_scission())
    print('Ideal fibre-tail configurations at 100 kPa, Gamma=0.5 J/m2')
    for force in [50e-12,100e-12,500e-12,1e-9]:
        for r in [5,10,20,40]:
            x=fibre_tail(force=force,radius_nm=r)
            print(f'  f={force*1e12:4.0f} pN, r={r:2} nm, sites={x["areal_paths_per_um2"]:8.2f}/um2, packing={x["packing_fraction"]:.3f}, mass={x["mass_ug_per_mm2"]:.3f} ug/mm2, passes_packing={x["feasible_by_packing"]}')
    print('Seam stack service reliability, per-exposure shared hazard across seams independent:')
    for n in [1,3,5,10,20,30]:
        print(f' n={n:2}, q_per_seam=.99, S={stacked_seams(n,.01):.6f}; required h at 90% lifetime S={max_seam_hazard(n):.8f}')
    print('Exact optimal allocation of synthetic functional bond budget among 10 stacked seams:')
    for B in [120,160,200,220,240,260]:
        uniform=seam_survival([B/10]*10)
        bonds,best=optimal_seam_bond_allocation(10,B)
        print(f' B={B:3}: uniform S={uniform:.4f}, exposure-weighted optimum S={best:.4f}, oldest/newest b={bonds[0]:.2f}/{bonds[-1]:.2f}')

if __name__=='__main__': report()


def segmented_exposures(n, block):
    """Idealized bypass after every `block` repairs; the continuing load
    goes directly to persistent host support and older stacked seams unload.
    Requires a NEW, unacquired physical direct-host connection each reset.
    """
    assert n>=1 and 1<=block<=n
    blocks=[min(block,n-i) for i in range(0,n,block)]
    return sum(s*(s+1)//2 for s in blocks), len(blocks)


def segmented_survival(n,block,h,s):
    """Each reset independently fails with probability s, each loaded seam
    per interval with probability h. No correlation or aging beyond exposures.
    """
    exposures,resets=segmented_exposures(n,block)
    return (1-h)**exposures*(1-s)**resets


def segmented_report():
    print('\nTEST: direct-host load-path reset frequency, 10 repair cycles')
    n=10;h=.01
    for s in [.001,.005,.02,.05,.10]:
        scores=[(segmented_survival(n,k,h,s),k,segmented_exposures(n,k)) for k in range(1,n+1)]
        best=max(scores)
        print(' reset hazard',s,'best',best,'all k=1,2,3,5,10',[(k,round(segmented_survival(n,k,h,s),4),segmented_exposures(n,k)) for k in [1,2,3,5,10]])
    # Analytic approximate block optimum sqrt(2 c/h) using log-failure units
    s=.02;c=-log(1-s); rate=-log(1-h)
    print(' asymptotic optimum block sqrt(2*resetloghazard/seamloghazard)=',sqrt(2*c/rate))
    # Direct stochastic validation
    rng=np.random.default_rng(448)
    reps=180000
    for k in (1,2,5,10):
        blocks=[min(k,n-i) for i in range(0,n,k)]
        good=np.ones(reps,dtype=bool)
        for m in blocks:
            good &= (rng.random(reps)>=s)
            for active_seams in range(1,m+1):
                good &= np.all(rng.random((reps,active_seams))>=h,axis=1)
        exact=segmented_survival(n,k,h,s)
        empirical=good.mean()
        assert abs(empirical-exact)<.005,(k,empirical,exact)
    print(' segmented-exposure stochastic checks passed')

if __name__=='__main__': segmented_report()


def reversible_dissipation_fraction(cycle_damage, recovery_integral):
    """Fast reversible force-bearing sacrificial sites: each mechanical cycle
    disables fraction p of active sites; between cycles inactive sites recover
    with constant hazard r during interval Delta (u=r*Delta).
    Returns pre-cycle and just-post-cycle steady-state active fractions.
    No cell kinetics or real wet-cellulose parameters inferred.
    """
    p=cycle_damage;q=exp(-recovery_integral)
    before=(1-q)/(1-(1-p)*q)
    return before,(1-p)*before


def minimal_recovery_for_post_damage(cycle_damage,post_req):
    p=cycle_damage
    if post_req>=1-p:return float('inf')
    if post_req<=0:return 0.
    ratio=((1-p)-post_req)/((1-p)*(1-post_req))
    return -log(ratio)


def fatigue_recovery_report():
    print('\nFast bond reformation versus cellularly replenished mass')
    for p in [.01,.05,.1,.2]:
        for target in [.7,.8,.9]:
            req=minimal_recovery_for_post_damage(p,target)
            print(' p=',p,'post-cycle minimum=',target,'recovery rate * cycle period >=',req)
            if np.isfinite(req):
                pre,post=reversible_dissipation_fraction(p,req)
                assert abs(post-target)<1e-10
    # independent finite-cycle numerical dynamics validation
    for p,rDt in [(.05,.5),(.1,.7),(.2,2.)]:
        x=1.
        for _ in range(1000):
            x=1-(1-(1-p)*x)*exp(-rDt)
        pre,post=reversible_dissipation_fraction(p,rDt)
        assert abs(x-pre)<1e-12
    print(' bond-recovery recurrence and exact threshold tests passed')

if __name__=='__main__': fatigue_recovery_report()
