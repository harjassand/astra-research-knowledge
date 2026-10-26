"""Astra Chemistry: rooted-product vacancy frontier, Gaussian reach, and global traceless release.

Status: mathematical/construction tests only. No kinetic rates were fitted to peptide reactions.
Existing PNA-adapter template chemistry (Niu/Hili/Liu 2013), PNA-primer relay
(Joshi/Romanens/Winssinger 2025), CAPTN (Spaltenstein et al. 2025), and
fuel-driven strand displacement (Mitra et al. 2026) are independent precedents;
the integrated operation here is NOT experimentally demonstrated.

Dependencies: numpy, scipy (for independent verification of extrema).
"""
from __future__ import annotations
from functools import lru_cache
from math import exp, log, log1p, pi, sqrt
import numpy as np
from scipy.optimize import minimize_scalar
from scipy.special import erf


def reach_density(step: int, sigma2_peptide: float, sigma2_template:float=0.,
                  rigid_template_step:float=0.) -> float:
    """Gaussian contact *density* between independently rooted strands at step j.

    X_j ~ N(0,j*sigma2_peptide I3), Y_j ~ N(j*r e_z,j*sigma2_template I3).
    The density for their separation to equal zero is exact. A reactive ball
    of small radius R has probability ~ (4pi R^3/3) times this density.
    The ideal-chain approximation is not valid at arbitrary short polymer length.
    """
    assert step > 0 and sigma2_peptide > 0 and sigma2_template >= 0
    v=step*(sigma2_peptide+sigma2_template)
    return (2*pi*v)**(-1.5)*exp(-.5*(rigid_template_step*step)**2/v)


def contact_rate(step:int, a_first:float=1., geometry:str='flexible', gamma:float=0.):
    """Assumed reaction hazard proportional to small-volume Gaussian contact density.

    'flexible': j^-3/2 for two independent Gaussian strands rooted only at origin.
    'stiff': j^-3/2 exp[-gamma*(j-1)] for linearly separating target loci.
    'local': newly attached adjacent-module anchor resets encounter length to 1.
    Not a universal polymer law; denaturants, sequence, confinement, and avidity matter.
    """
    assert step>=1 and a_first>0 and gamma>=0
    if geometry=='flexible': return a_first/step**1.5
    if geometry=='stiff': return a_first/step**1.5*exp(-gamma*(step-1))
    if geometry=='local': return a_first
    raise ValueError(geometry)


def length_fidelity(length, damage_over_first_rate=1e-6, geometry='flexible', gamma=0.):
    """Exact competing exponential clock probability of ALL correct bonds,
    given no chemical errors besides global irreversible damage while waiting.
    Each step has rate a_j, damage rate d; success per step a_j/(a_j+d).
    """
    assert length>=1 and damage_over_first_rate>=0
    return exp(-sum(log1p(damage_over_first_rate/contact_rate(j,1.,geometry,gamma))
                    for j in range(1,length+1)))


def cleanup_success(num_tags, u=1., h=0., d=0., t=0.):
    """All independently cleavable tags removed correctly by t; no whole-product damage.

    Every tag: cleavage u vs competing irreversible wrong cleavage/damage h.
    Whole product: damage d per time, independent of tag count.
    q_tag(t)=u/(u+h)*(1-exp[-(u+h)t]).
    """
    assert num_tags>=1 and u>0 and h>=0 and d>=0 and t>=0
    k=u+h
    q=u/k*(-np.expm1(-k*t))
    if q==0: return 0.
    return exp(-d*t+num_tags*log(q))


def optimal_cleanup(num_tags, u=1., h=0., d=0.):
    """Exact optimum over shared simultaneous tag-cleavage interval (d>0).

    t*=log(1+num_tags*(u+h)/d)/(u+h). If d=0 the supremum is obtained
    asymptotically; return inf and [u/(u+h)]^num_tags.
    """
    assert num_tags>=1 and u>0 and h>=0 and d>=0
    k=u+h
    if d==0: return float('inf'),(u/k)**num_tags
    t=log1p(num_tags*k/d)/k
    return t,cleanup_success(num_tags,u,h,d,t)


def leakage_exposure(L,alpha,r0=1.,nearest_step=1):
    """Sum over every downstream pair of potential nonfrontier access.

    As L grows, sum_{r>=nearest_step}^{L-1}(L-r)*r0/r^alpha.
    r0 is a dimensionless integrated hazard ratio for an off-target site.
    alpha=0 quadratic; alpha=1 LlogL; alpha>1 linear (not zero).
    """
    assert L>=1 and nearest_step>=1 and alpha>=0 and r0>=0
    return sum((L-r)*r0/r**alpha for r in range(nearest_step,L))


def exact_future_leak_fidelity(L,alpha,r0=1e-5):
    """Constant intended hazard 1 each stage and additively leaking future sites.
    Exact independent irreversible competing clocks with no other hazards.
    """
    acc=0.
    for current in range(L):
        bad=sum(r0/r**alpha for r in range(1,L-current))
        acc+=log1p(bad)
    return exp(-acc)


@lru_cache(None)
def safe_histories(L,cycles):
    """Formal induction test of ideal rooted-prefix gate across all paths.
    Tags 1..j are rooted and occupy the matching addresses; the available
    next site is j+1. A successful amide adds exactly one tagged module;
    miss or resolved S-acyl leaves the rooted prefix unchanged.\n
    Physical assumptions deliberately strong: verified address rebinding,
    stable product covalent tether, terminal protection against double coupling,
    and complete donor/temporary S-acyl clearance before fuel.
    """
    states={0}
    for _ in range(cycles):
        nxt=set()
        for n in states:
            occupied=set(range(1,n+1))
            open_sites={n+1} if n<L else set()
            assert occupied.isdisjoint(open_sites)
            assert not open_sites or min(open_sites)==n+1
            # fail or chemically resolved reversible intermediate: unchanged
            nxt.add(n)
            # correct amide: product-retained handle occupies former vacancy
            if n<L:nxt.add(n+1)
        states=nxt
    return frozenset(states)


def strict_rebinding_survival(L, theta):
    """Probability all historically accumulated tags are simultaneously docked
    after EVERY refresh, assuming independent tag occupancy theta per refresh.
    This strong and often unnecessary requirement incurs quadratic burden.
    """
    assert L>=1 and 0<=theta<=1
    return theta**(L*(L+1)//2)


def gate_counterexample_failures():
    """Two necessary physical requirements; neither is proved by state machine.
    A bound labile thioester carries the same covalent product-connected handle
    as a correct amide. A retained free donor after the chase similarly can
    carry the next-address opening trigger. Those yield false advancement.
    """
    # product root R, temporary sulfur ester S, donor tag D: graph connectivity
    labile_intermediate_edges={('R','S'),('S','D')}
    stable_ever_edges={('R','amide'),('amide','D')}
    assert any('D' in edge for edge in labile_intermediate_edges)
    assert any('D' in edge for edge in stable_ever_edges)
    # local address-opening signal based on *retained tag* alone is identical
    # without thioester-specific chase and complete removal of free donors.
    return 'Thioester cleanup and physically removing free donor are both necessary.'


def checks():
    from numpy.random import default_rng
    rng=default_rng(20261027)
    # Contact-density algebra: with two flexible independent strands,
    # ratio between step j and step 1 is j^-3/2, even if their Kuhn variances differ.
    for _ in range(400):
        j=int(rng.integers(1,400))
        vp=10**rng.uniform(-2,1);vt=10**rng.uniform(-2,1)
        x=reach_density(j,vp,vt)/reach_density(1,vp,vt)
        assert abs(x-j**(-1.5))<1e-12
        dr=float(rng.uniform(0,3))
        rigid=reach_density(j,vp,0,dr)/reach_density(1,vp,0,dr)
        expect=j**(-1.5)*exp(-.5*(j-1)*dr**2/vp)
        assert abs(rigid-expect)<1e-12
    # Independent numerical bounded optimization of cleanup time.
    maxres=0.
    for _ in range(220):
        L=int(rng.integers(1,200))
        u=10**rng.uniform(-2,1)
        h=u*10**rng.uniform(-7,-1)
        d=u*10**rng.uniform(-5,-1)
        t,value=optimal_cleanup(L,u,h,d)
        out=minimize_scalar(lambda x:-cleanup_success(L,u,h,d,x),
                            bounds=(0,max(3*t,1)),method='bounded',
                            options={'xatol':1e-10})
        maxres=max(maxres,abs(value+out.fun))
        assert abs(value+out.fun)<1e-9,(L,u,h,d,value,out.fun)
    # Independent Monte Carlo for joint all-tags-cleaved and product-survives.
    L=32;u=1;h=.0001;d=.002;t=9.3;total=0;succ=0
    for _ in range(120):
        n=2000
        t_first=rng.exponential(1/(u+h),size=(n,L))
        correct_choice=(rng.random((n,L))<u/(u+h))
        whole_life=rng.exponential(1/d,size=n)
        accepted=(t_first<=t).all(axis=1)&correct_choice.all(axis=1)&(whole_life>t)
        succ+=accepted.sum();total+=n
    expected=cleanup_success(L,u,h,d,t)
    observed=succ/total
    assert abs(observed-expected)<.006,(observed,expected)
    for L in (3,4,5,10):
        for n in (0,1,2,3,L+2):
            assert safe_histories(L,n)==frozenset(range(min(n,L)+1))
    assert gate_counterexample_failures()
    assert abs(strict_rebinding_survival(3,.8)-.8**6)<1e-12
    assert all(exact_future_leak_fidelity(64,alpha,1e-5)<1 for alpha in [0,1,1.5,2])
    print('Gaussian contact: 400 independent special-case checks')
    print('Global cleavage: 220 numerical optimizers, max difference',maxres)
    print('Joint-cleavage Monte Carlo:',observed,'exact',expected,'samples',total)
    print('Prefix-state exhaustive outcome sets: passed')


def main():
    checks()
    for L in (16,64,1024):
        print('L=',L,'d/a_1=1e-6: unanchored',length_fidelity(L,1e-6,'flexible'),
              'rung anchored',length_fidelity(L,1e-6,'local'))
        for d_over_u in (1e-4,1e-3,1e-2):
            t,f=optimal_cleanup(L,1,0,d_over_u)
            print(' global cleavage d/u=',d_over_u,'time in 1/u units',t,
                  'whole-chain success',f)
        print(' future unblocked site exposure epsilon=1e-5:',
              [(a,leakage_exposure(L,a,1e-5),exact_future_leak_fidelity(L,a,1e-5))
               for a in (0,1,1.5,2)])
    print('CONCLUSION: prefix correctness requires complete chase, donor exit, occupied-site fidelity, and gate discrimination;\n'
          'these are UNMEASURED for the proposed relay. No synthetic capability established.')

if __name__=='__main__':main()
