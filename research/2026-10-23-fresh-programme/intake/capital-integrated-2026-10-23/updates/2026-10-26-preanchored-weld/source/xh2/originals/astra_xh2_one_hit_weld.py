"""Astra XH2 scientific continuation: pre-associated xyloglucan single-graft
versus independent multiarm double-graft at a shared stochastic shutdown.

All parameters uncalibrated toy parameters. References:
- Whitney et al, Am J Bot 2006, doi:10.3732/ajb.93.10.1402:
  high MW xyloglucan incorporable during bacterial cellulose synthesis;
  composites may weaken under uniaxial tension.
- Hemicellulose adhesion BC AFM, PMID 30658836: 4.3x adhesion energy
  with xyloglucan (not macroscopic strength).
- Herburger et al, Plant J 2021, PMCID PMC8611796: HTG grafts
  cellulose onto high MW xyloglucan, at lower activity than short XGO.
- Frankova & Fry, Carbohydrate Polymers 2026, PMID 41274712:
  multivalent XXXGol acceptors accepted by HTG but two-sided actual weld
  and mechanical performance not demonstrated.
- Frankova et al, 2020, PMID 32918959: HTG on bacterial cellulose Ialpha;
  cannot transfer cotton I vs II relative activities to bacterial cellulose.

A tile has Poisson(N) candidate links. A shared exposure window T~Exp(d)
truncates catalytic action for all links together. Conditional on T,
links react independently. One-hit candidate is physically pre-anchored to
new cellulose with probability a and retained on old substrate cleavage
with probability eta; HTG grafts it to old cellulose once (hazard k).
Two-hit candidate has valence 4 and needs useful retained grafts on both
sides, consistent with the earlier hypothetical XH2 model.

Theoretical limits:
- one-hit tile no-link failure, k=d: (1-exp(-N*a*eta))/(N*a*eta)
- large-N with k/d=r, no-link failure ~1/(r*N*a*eta).
- two-hit, v=4, symmetric old/new, small-t p(t) ~3*(eta*k*t)^2,
  so no-link shared-window failure ~ sqrt(pi)/(2*eta*k/d*sqrt(3N)).
- for m links required, one-hit k=d failure ~ m/(N*a*eta) (large N).
- Adding guaranteed maturation time t0 makes success conditional at T=0
  strictly positive, restoring exponential (rather than polynomial) decay
  with link abundance.
- Prior contact formation Tcontact~Exp(g) vs closure~Exp(d) gives
  multiplicative independent p_contact=g/(g+d). Without physical contact,
  biochemistry alone cannot create a load path.
"""
from dataclasses import dataclass
from math import exp, pi, sqrt
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.stats import poisson

@dataclass(frozen=True)
class Params:
    rate_ratio:float=1.0 # catalytic graft hazard k / regional shutdown hazard d
    ret:float=0.8      # donor fragment remains mechanically attached to old network
    anchor:float=0.5   # XyG associated with the NEW network and mechanically useful
    target_old:float=1.0 # fraction of catalytic encounters targeting OLD, not NEW cellulose
    valence:int=4      # synthetic alternative
    maturation:float=0.0 # minimum reaction time after closure, in units 1/d
    tiles:int=20
    target:float=0.9

def p_one(u,p:Params):
    """u=e^(-d*T) ~ Unif(0,1); retained pre-anchored XyG one-hit."""
    q=1.-exp(-p.rate_ratio*p.maturation)*u**p.rate_ratio
    return p.anchor*p.ret*p.target_old*q

def p_two(u,p:Params):
    q=1.-exp(-p.rate_ratio*p.maturation)*u**p.rate_ratio
    v=p.valence
    x=p.ret*q
    return max(0.,1.-2.*(1.-.5*x)**v+(1.-x)**v)

def tile_failure(N,p:Params, mechanism='one', min_paths=1):
    assert N>=0 and min_paths>=1
    f=p_one if mechanism=='one' else p_two
    def integrand(u):
        return float(poisson.cdf(min_paths-1,N*f(u,p)))
    return quad(integrand,0.,1.,epsabs=3e-12,epsrel=3e-11,limit=250)[0]

def min_N(p:Params, mechanism='one', min_paths=1, contact_ratio=float('inf')):
    contact=1. if contact_ratio==float('inf') else contact_ratio/(1.+contact_ratio)
    needed=p.target**(1./p.tiles)
    if contact<=needed: return float('inf')
    acceptable=1.-needed/contact
    def f(logN):return tile_failure(exp(logN),p,mechanism,min_paths)-acceptable
    from math import log
    lo,hi=log(1.e-6),log(1.e15)
    if f(hi)>0:return float('inf')
    return exp(brentq(f,lo,hi,xtol=2e-9))

def effective_net_gain(preanchor, retained, bond_gain, donor_harm_probability, harm_magnitude):
    """Toy expected utility PER HTG turnover for one-hit mechanism.
    One old-side catalytic event creates a load-bearing new link with
    probability preanchor*retained. It can harm a prior old fibre with
    joint probability donor_harm_probability. Normalized force coefficients
    are explicitly illustrative, not experimental values.
    """
    return preanchor*retained*bond_gain - donor_harm_probability*harm_magnitude

def checks():
    p=Params()
    for N in (1,5,30,100,500,1500):
        x=N*p.anchor*p.ret*p.target_old
        exact=-np.expm1(-x)/x
        got=tile_failure(N,p,'one',1)
        assert abs(got-exact)<5e-10,(N,got,exact)
    # Q: one-hit slope at small T is first order; 2-hit is second order.
    for t in (1e-4,5e-5):
        u=exp(-t)
        o=p_one(u,p)
        d=p_two(u,p)
        assert abs(o/t -p.anchor*p.ret*p.target_old)<2e-4
        assert abs(d/t**2 -3*p.ret**2)<1.5e-3
    assert min_N(p,'one',1) < min_N(p,'two',1)
    # Increasing guaranteed maturation cannot worsen performance.
    for mechanism in ('one','two'):
        assert tile_failure(50,Params(maturation=.2),mechanism) < tile_failure(50,p,mechanism)
    print('PASS exact 1-hit formula, 1st/2nd order limits, quadrature and monotonicity')

if __name__=='__main__':
    checks()
    p=Params()
    print('per-tile failure threshold:',1-p.target**(1/p.tiles))
    print('\nBASELINE k/d=1, eta=.8, one-hit anchor=.5, old two-hit valence4')
    for m in (1,3,5):
        one=min_N(p,'one',m);two=min_N(p,'two',m)
        print(f'paths={m}: single-graft N={one:.2f} two-graft linker N={two:.2f} two-graft arms={4*two:.2f} arm-equivalent ratio={4*two/one:.1f}x')
    print('\nONE-HIT sensitivity to pre-anchor and high-MW acceptor catalytic slowdown')
    for r in (1.,.3,.1,.03,.01):
        for a in (.25,.5,.8):
            q=Params(rate_ratio=r,anchor=a)
            print('k/d',r,'anchor',a,'Nmin m1',round(min_N(q),1),'Nmin m5',round(min_N(q,min_paths=5),1))
    print('\nOPPOSITE-FACE TARGETING: reaction to OLD rather than NEW cellulose (k/d=1)')
    for theta in (1.,.75,.5,.25,.1,.05,.01):
        q=Params(target_old=theta)
        print('theta_old',theta,'N 1-link',round(min_N(q,'one',1),1),'N 5-link',round(min_N(q,'one',5),1))
    print('\nCROSSOVER WHEN PREASSOCIATED ONE-HIT HAS SLOWER EFFECTIVE REACTION RATE')
    from scipy.optimize import brentq
    old=min_N(p,'two',1)
    for scale in (1.,4.):
        threshold=brentq(lambda r:min_N(Params(rate_ratio=r),'one',1)-old*scale,.001,1.)
        print('one-hit k/d threshold for same',('molecules' if scale==1 else 'reactive-arm equivalents'),':',round(threshold,6))
    print('\nGUARANTEED EXTRACELLULAR MATURATION, same k/d=1, 20 tiles target 90%')
    for t0 in (0.,.05,.1,.2,.5):
        q=Params(maturation=t0)
        print('t0',t0,'one m1',round(min_N(q,'one',1)),'one m5',round(min_N(q,'one',5)),'two m1',round(min_N(q,'two',1)))
    print('\nCONTACT-before-shutdown constraint: 20 tiles, >=1 link, k/d=1, anchor .5')
    for gr in (100.,190.,200.,300.,500.,1000.,float('inf')):
        print('g/d',gr,'one_min N',f'{min_N(p,"one",1,gr):.1f}','two_min N',f'{min_N(p,"two",1,gr):.1f}')
    print('\nADVERSARIAL DAMAGE criterion (toy units): expected net gain per cleavage')
    for a in (.2,.5,.8):
        for harm in (.1,.3,.5):
            print('anchor',a,'harm probability',harm,'gain',round(effective_net_gain(a,.8,1.,harm,1.),3))

# Further derivations: target-old targeting, persistence of the xyloglucan
# association in a hydrated loaded interface, and composite-strength tradeoff.
from scipy.special import gammainc

def one_hit_window_failure_closed(X:int|float,min_paths:int=1):
    """For k=d, q(T)=1-exp(-dT) is uniform on [0,1]. Conditional number
    of surviving mechanical links ~Pois(X*q), where X=N*a*eta*theta*S.
    Integrating P(Pois(Xq)<m) gives sum gammainc(j+1,X)/X.
    S is the hypothetical probability a preassociated attachment survives
    a later mechanical service interval; NOT given by AFM adhesion energy.
    """
    if X<=0:return 1.
    return float(sum(gammainc(j+1,X) for j in range(min_paths))/X)

def required_effective_exposure(tiles=20,target=.90,min_paths=1):
    allowance=1-target**(1/tiles)
    return brentq(lambda X:one_hit_window_failure_closed(X,min_paths)-allowance,
                  .01,1e9,xtol=1e-10)

def required_candidates_one_hit(anchor=.5,retention=.8,target_old=.5,
                                service_survival=1.,min_paths=1):
    X=required_effective_exposure(min_paths=min_paths)
    return X/(anchor*retention*target_old*service_survival)

def critical_strength_fraction(span_cost,interface_cost,interface_improvement):
    """Original minimum mass proportional A+B: A=h/sigma_f, B=r/tau.
    Composite with fibre strength multiplier s and interface shear multiplier c
    improves mass if A/s+B/c<A+B.
    c must denote *shear transfer strength* NOT the experimentally reported
    4.3x increase in AFM adhesion energy (different observable).
    """
    if interface_improvement<=1:return 1.
    return 1/(1+(interface_cost/span_cost)*(1-1/interface_improvement))

def continuation_checks():
    for m in (1,3,5):
        X=required_effective_exposure(min_paths=m)
        p=Params(target_old=.5)
        N=X/(p.anchor*p.ret*p.target_old)
        integral=tile_failure(N,p,'one',min_paths=m)
        exact=one_hit_window_failure_closed(X,m)
        assert abs(integral-exact)<3e-10,(m,integral,exact)
    # Exact target dependency when all reaction and holding rates are constant.
    assert abs(required_candidates_one_hit(target_old=.5)/
              required_candidates_one_hit(target_old=1.)-2)<1e-12
    print('PASS: incomplete-Gamma closed form vs independent Poisson integral, targeting and lifetime scaling')

if __name__ == '__main__':
    continuation_checks()
    print('\nPHYSICALLY RELEVANT competing-reaction direction and service survival; 90% of 20 tiles')
    for paths in (1,5):
        for theta in (1.,.5,.1):
            for service in (1.,.5,.1):
                print('paths',paths,'theta_old',theta,'mechanical_retention',service,
                      'Nmin',round(required_candidates_one_hit(target_old=theta,
                                               service_survival=service,min_paths=paths),1))
    print('\nFIBRE-STRENGTH COST versus interface-strength benefit; shear multiplier is illustrative')
    for ratio in (.5,1.,5.):
        for c in (1.5,2.,4.3):
            print('interface/span cost ratio',ratio,'strength multiplier',c,
                  'minimum fibre-strength retention',round(critical_strength_fraction(1.,ratio,c),4))

def one_hit_failure_buffer_closed(X,extra_time,min_paths=1):
    """Closed-form conditional Poisson CDF mixture under T~Exp(1) and an
    additional deterministic active time t0=extra_time. k=d=1 and link
    probability a*eta*theta*(1-exp(-(T+t0))). X=N*a*eta*theta*S.
    """
    if extra_time==0:return one_hit_window_failure_closed(X,min_paths)
    if X<=0:return 1.
    from scipy.special import gammainc
    c=exp(-extra_time)
    q0=1-c
    ans=sum(gammainc(j+1,X)-gammainc(j+1,X*q0) for j in range(min_paths))/(X*c)
    return float(max(0.,min(1.,ans)))

def required_buffered_candidates(contact_ratio=float('inf'),extra_time=0.,
                                 min_paths=1,anchor=.5,eta=.8,theta=.5,
                                 service_survival=1.,tiles=20,target=.90):
    contact=1. if contact_ratio==float('inf') else contact_ratio/(1+contact_ratio)
    per_tile_target=target**(1/tiles)
    if contact<=per_tile_target:return float('inf')
    cap=1-per_tile_target/contact
    X=brentq(lambda x:one_hit_failure_buffer_closed(x,extra_time,min_paths)-cap,
             1e-9,1e7,xtol=1e-8)
    return X/(anchor*eta*theta*service_survival)

def final_checks():
    for m in (1,3,5):
        for t in (0,.05,.2,.5):
            X=40
            precise=one_hit_failure_buffer_closed(X,t,m)
            from dataclasses import replace
            q=Params(maturation=t)
            numerical=tile_failure(X/(q.anchor*q.ret),q,'one',min_paths=m)
            assert abs(precise-numerical)<2e-12,(m,t,precise,numerical)
    print('PASS exact buffered closed form versus full stochastic-window quadrature')

if __name__=='__main__':
    final_checks()
    print('\nCONTACT + MATURATION full-cycle mechanical one-hit threshold')
    for gr in (200.,500.,float('inf')):
        for t0 in (0,.05,.2,.5):
            print('g/d',gr,'extra catalytic time',t0,
                  'Nmin_1',round(required_buffered_candidates(gr,t0,1)),
                  'Nmin_5',round(required_buffered_candidates(gr,t0,5)))

# Stoichiometric upper-bound for a single reactive xyloglucan chain terminus.
# An unbranched XyG molecule (whatever number of substituted backbone positions)
# has one nonreducing terminal acceptor that can be ligated to an OLD-cellulose
# donor by the one-hit HTG design. At equal total XyG *mass* B and identical
# catalytic opportunities per accessible end, available candidate ends scale
# as (B / MW) * capture_probability * old_side_access * survival.
# Long XyG can adsorb more reliably than short XyG, but at fixed mass its
# molar count and accessible terminal density decline.
def mass_normalized_effective_ends(mw_kda,preanchor,end_exposure=1.,
                                   theta_old=1.,service_survival=1.):
    return (preanchor*end_exposure*theta_old*service_survival)/mw_kda

def long_xg_advantage_condition(mw_short=200.,mw_long=880.,a_short=.2,a_long=.95):
    ratio=mass_normalized_effective_ends(mw_long,a_long)/mass_normalized_effective_ends(mw_short,a_short)
    return ratio,ratio>1

def xyloglucan_checks():
    assert abs(long_xg_advantage_condition(a_short=.2,a_long=.95)[0]-.95/.2/4.4)<1e-12
    assert not long_xg_advantage_condition(a_short=.5,a_long=1.)[1]
    print('PASS: finite nonreducing-end density per xyloglucan mass')

if __name__=='__main__':
    xyloglucan_checks()
    print('XyG length tradeoff at equal mass, 200 vs 880 kDa; long preanchor .95:')
    for a_short in (.05,.1,.2,.3,.5):
        ratio,better=long_xg_advantage_condition(a_short=a_short,a_long=.95)
        print('short preanchor',a_short,'long/short effective termini per mass',ratio,
              'long preferable:',better)
