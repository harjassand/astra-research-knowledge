"""Astra XH2, 2026-10-26 — a chemically specified *test* for cellulose welds.

This is purely analytical/computational research, NOT experimental validation or
an assertion that HTG gives load-bearing cellulose welding. Previous XH2
fibre parameters are inherited for a matched comparison.

Primary mechanistic evidence:
- Herburger et al 2020, Molecular Plant 13:1047-1062, PMCID PMC7339142:
  Equisetum HTG transfers cellulose to xyloglucan; in-situ plant-cell-wall
  evidence, bacterial expansin boosts cellulose transglycosylation.
- Frankova & Fry, Carbohydr Polym 372:124525, January 2026:
  XXXGol_(1-4)-diaminoethane synthetic multimeric HTG acceptors; no
  demonstrated two-sided mechanical cellulose-to-cellulose junction.
- Herburger et al 2021, Plant J, PMCID PMC8611796:
  on tested cotton/filter-paper cellulose-I CXE was ~9% cellulose-II rate;
  not measured on living bacterial-cellulose repair patches.

Mechanism tested:
  a short multivalent acceptor must react to ONE cellulose donor on each of
  two overlapping structural fibre families (old/new). It cannot span a
  macroscopic crack without independent fibre growth. Each donor-derived
  fragment must remain mechanically connected to its original network;
  this probability is a free parameter 'retained'. Cleavage alone is NOT a
  good load-bearing attachment.

Definitions/derivations:
  v identical reactive arms. Each arm independently yields a mechanically
  retained cellulose graft with probability u=q*eta. Conditional on graft,
  chooses old or new network with probabilities theta, 1-theta. Productive
  bivalent or multivalent bridge probability by inclusion-exclusion:
     Pcross = 1 - (1-u*theta)**v - (1-u*(1-theta))**v + (1-u)**v.
  In particular Pcross(v=2, theta=.5)=u^2/2. Same-side reaction or single
  graft does not produce an inter-network mechanical weld.

  Along a NEW fibre embedded Le on each side, available linker precursors
  follow Poisson point process intensity n0 (per um), and independently
  fraction c are true nm-scale old-to-new overlap (UNMEASURED). Successful
  junction number each side ~Poisson(Le*n0*c*Pcross).

  Independent count N_old,N_new; axial force is bounded by
    min(Af*sigma_f, 2*pi*r*tau0*Le + f_s*min(N_old,N_new))
  where tau0 is a free non-covalent background and f_s is sustained allowable
  force per complete covalent junction (not a rupture-force measurement).
  The 'min' is a conservative equal-force series bottleneck model, BUT the
  addition of background and bond loads is optimistic (no creep/correlation).
  E[min(N1,N2) capped] = sum_{k=1}^floor(cap) P(Pois(mu)>=k)^2
       + remaining_fraction*P(Pois(mu)>=floor(cap)+1)^2.
  This exact identity checks Monte Carlo; it is not a prediction for real BC.

  Matched earlier XH2 illustrative scenario:
  gap h=100um, patch area=1mm2, 100kPa target, r=50nm,
  effective wet fibre tensile strength=100MPa, cellulose density=1500kg/m3.
  Every parameter except dimensions is HYPOTHETICAL, including native wet
  physical shear tau0 and HTG conversion/force/availability.
"""

import math
from dataclasses import dataclass
import numpy as np
from scipy.optimize import minimize_scalar, brentq
from scipy.stats import poisson
from scipy.special import ive

@dataclass(frozen=True)
class Model:
    gap_um: float = 100.
    fibre_radius_m: float = 50e-9
    fibre_strength_pa: float = 100e6
    cellulose_density: float = 1500.
    traction_target_pa: float = 100e3
    area_m2: float = 1e-6
    background_shear_pa: float = 10e3
    candidates_per_um: float = 200.
    contact_fraction: float = 0.20
    individual_bond_force_nN: float = 1.0
    arm_grafting_prob: float = .7
    donor_fragment_retained: float = .8
    theta: float = .5
    valence: int = 4


def p_two_sided(v, q, retained, theta=.5):
    u=q*retained
    if v < 2: return 0.0
    return max(0., 1.-(1.-u*theta)**v-(1.-u*(1.-theta))**v+(1.-u)**v)


def mean_min_poisson(mu):
    # E[min(N1,N2)] via Skellam absolute-value formula, n1,n2 iid Pois(mu)
    if mu <= 0: return 0.
    return mu*(1.-ive(0,2*mu)-ive(1,2*mu))


def capped_min_poisson(mu, cap):
    """E[min(min(Pois1,Pois2),cap)] exact; cap may be noninteger."""
    if cap <= 0 or mu <= 0: return 0.
    n=int(math.floor(cap))
    # use vectorization; no approximations apart from underlying floating point
    k=np.arange(1,n+1, dtype=int)
    p=poisson.sf(k-1, mu)
    v=float(np.dot(p,p))
    frac=cap-n
    if frac:
        tail=poisson.sf(n,mu)
        v+=frac*tail*tail
    return v


def input_rate_per_um(m: Model):
    return (m.candidates_per_um*m.contact_fraction*
            p_two_sided(m.valence,m.arm_grafting_prob,
                        m.donor_fragment_retained,m.theta))


def expected_axial_capacity(L_um, m:Model):
    """Exact expected force in Newtons for one aligned two-sided fibre."""
    h=m.gap_um
    if L_um <= h: return 0.
    le_um=(L_um-h)/2.
    r=m.fibre_radius_m
    maxforce=math.pi*r*r*m.fibre_strength_pa
    background=2.*math.pi*r*m.background_shear_pa*le_um*1e-6
    if background>=maxforce: return maxforce
    f=1e-9*m.individual_bond_force_nN
    mu=input_rate_per_um(m)*le_um
    return background + f*capped_min_poisson(mu,(maxforce-background)/f)


def optimise_fibre(m:Model, max_um=20000):
    h=m.gap_um
    def efficiency(logL):
        L=math.exp(logL)
        mass=m.cellulose_density*math.pi*m.fibre_radius_m**2*(L*1e-6)
        return expected_axial_capacity(L,m)/mass
    sol=minimize_scalar(lambda x:-efficiency(x),bounds=(math.log(h*(1.+1e-9)),math.log(max_um)),method='bounded',options={'xatol':1e-9})
    possibilities=[sol.x,math.log(h*(1.+1e-9)),math.log(max_um)]
    best=max(possibilities,key=efficiency)
    E=efficiency(best)
    # Required cellulose mass per repair area in ug per mm2: kg/m2 * 1e3
    return {'L_um':math.exp(best), 'mass_ug_mm2':m.traction_target_pa/E*1e3,
            'bond_density_per_um':input_rate_per_um(m),
            'p_cross':p_two_sided(m.valence,m.arm_grafting_prob,
                                m.donor_fragment_retained,m.theta),
            'mu_bonds_per_face':input_rate_per_um(m)*(math.exp(best)-h)/2.,
            'effective_force_N':expected_axial_capacity(math.exp(best),m)}


def coupled_crosslink_loss(v=4,q=.7,eta=.8,theta=.5,bridge_force=1.,loss_force=1.):
    """Toy risk criterion; each graft that fails to retain donor contributes
    expected possible load damage. Crucial unknown is real proportion of
    'cleavages' that destroy load-bearing donor fibres. Independent-arm risk
    model, not measured damage rate. Result is a net load proxy, not actual Gc.
    """
    pos=p_two_sided(v,q,eta,theta)*bridge_force
    harm=v*q*(1.-eta)*loss_force
    return {'good_events':pos,'harm_events':harm,'net':pos-harm,
            'benefit_to_harm_ratio':pos/harm if harm else math.inf}


def simulate_junctions(mu,cap,seed=100,reps=100000):
    rng=np.random.default_rng(seed)
    old=rng.poisson(mu,reps)
    new=rng.poisson(mu,reps)
    z=np.minimum(np.minimum(old,new),cap)
    return float(z.mean()),float(z.std(ddof=1)/math.sqrt(reps))


def calibration_scale(q_ref=.7,relative_activity=.09):
    """Only for a *hypothetical fixed-time simple hazard comparison*;
    experimentally measured cellulose I/II activity ratios do NOT imply
    such a proportional graft probability in a living BC interface.
    """
    dose=-math.log(1-q_ref)
    return 1.-math.exp(-relative_activity*dose)


def tests():
    assert p_two_sided(1,.7,.8)==0
    assert abs(p_two_sided(2,.7,.8,.5)-.5*(.7*.8)**2)<1e-13
    assert 0<=p_two_sided(4,.7,.8,.5)<=1
    for mu in (.1,.3,1,5,20,100):
        z=capped_min_poisson(mu,2000)
        assert abs(z-mean_min_poisson(mu))<2e-8,(mu,z,mean_min_poisson(mu))
    mc,se=simulate_junctions(15,9.8,seed=13,reps=200000)
    ana=capped_min_poisson(15,9.8)
    assert abs(mc-ana)<5*se,(mc,se,ana)
    m=Model()
    assert optimise_fibre(m)['mass_ug_mm2']>0
    print('PASS: bridge combinatorics, exact Poisson series vs Bessel, Monte Carlo, tensile optimization')

if __name__=='__main__':
    tests()
    print('\nCROSSLINK FATE (independent arms, q=.7, retained=.8, symmetric side access)')
    for v in (1,2,3,4,5,6,8,10):
        p=p_two_sided(v,.7,.8)
        print(f'valence={v:2d} P(true old-new bridge)={p:.6f} per reactive arm={p/v:.6f}')
    print('\nACTIVITY PROXY FROM CELLULOSE-I VS CELLULOSE-II OBSERVATION (NOT a living cell prediction)')
    q_I=calibration_scale(.7,.09)
    print('q_I=',q_I,'p4_I=',p_two_sided(4,q_I,.8),'p4_ref=',p_two_sided(4,.7,.8))
    print('\nALIGNED REPAIR; r=50nm, wet effective sigma=100MPa, gap100um, traction100kPa, tau0=10kPa')
    print('contact | valence | Pcross | bonds per um embedded | optimal length um | dry mass ug/mm2')
    for c in (.01,.03,.1,.2,.4,.7,1.):
        for v in (2,4):
            out=optimise_fibre(Model(contact_fraction=c,valence=v))
            print(f'{c:7.2f} {v:8d} {out["p_cross"]:8.4f} {out["bond_density_per_um"]:22.4f} {out["L_um"]:18.1f} {out["mass_ug_mm2"]:20.4f}')
    print('\nCANDIDATE INACCESSIBILITY AND LONG TERM BOND-FORCE SENSITIVITY')
    for q in (.7,calibration_scale(.7,.09)):
        for f in (1.,.1):
            for c in (.1,.4,1.):
                out=optimise_fibre(Model(arm_grafting_prob=q,individual_bond_force_nN=f,contact_fraction=c,valence=4))
                print('q',round(q,4),'force_nN',f,'contact',c,'mreq',round(out['mass_ug_mm2'],4),'L_um',round(out['L_um'],1))
    print('\nNECESSARY CHEMICAL NET-BENEFIT CHECK (not a fracture-energy model)')
    for eta in (.5,.7,.8,.95):
        for v in (2,4):
            print('retention',eta,'valence',v,coupled_crosslink_loss(v=v,eta=eta))
    print('\nPATCH MASS vs culture-equivalent (NOT a local culture rate)')
    print('1 ug in 0.1 uL =',1e-6 / 1e-7,'g/L; 9.1 g/L 14 day bulk yield is an incompatible time/volume comparator')

# A second attack: can simply performing the old-side and new-side chemistry
# in two stages outperform a well-mixed linker at an IDENTICAL total per-arm
# probability? NO under the independent, identical-arm model.
def sequential_cross_fixed_budget(valence, p_old, total_arm_success):
    """First stage can attach old (prob p_old), second attaches new using
    otherwise unreacted arms, with p_new=total_arm_success-p_old.
    Across the two stages the overall probability an arm reacts is held fixed.
    Inclusion-exclusion gives the same expression as the mixed model with
    theta=p_old/total_arm_success. This ignores conditional allosteric changes.
    """
    if not (0<=p_old<=total_arm_success<=1): raise ValueError('invalid probabilities')
    p_new=total_arm_success-p_old
    p_none=1-total_arm_success
    return max(0, 1-(1-p_old)**valence-(1-p_new)**valence+p_none**valence)


def minimum_contact_for_budget(m:Model, max_um=200.,budget_ug=1.):
    """Root search over nm-scale interfacial contact fraction. Returns None
    if even complete contact is insufficient under the model."""
    from dataclasses import replace
    f=lambda c:optimise_fibre(replace(m,contact_fraction=c),max_um=max_um)['mass_ug_mm2']-budget_ug
    if f(1.)>0:return None
    if f(0.)<0:return 0.
    return brentq(f,0.,1.,xtol=1e-11)


def net_retention_threshold(valence=4,q=.7):
    """Threshold *only* if every productive bridge counts as one unit and
    every grafted fragment lost from the original network costs one unit.
    Not a model of true viscoelastic fracture-energy gain; deliberately
    adversarial cleavage-risk check."""
    g=lambda eta:coupled_crosslink_loss(v=valence,q=q,eta=eta)['net']
    return brentq(g,1e-8,1.-1e-8)


def next_checks():
    q=.56
    for v in (2,3,4,5,8):
        arg=np.linspace(0,q,101)
        values=np.array([sequential_cross_fixed_budget(v,a,q) for a in arg])
        assert int(np.argmax(values))==50
        assert abs(values[50]-p_two_sided(v,1.,q,.5))<2e-13
    for arm in (.7,calibration_scale(.7,.09)):
        for force in (1.,.1):
            m=Model(arm_grafting_prob=arm,individual_bond_force_nN=force)
            threshold=minimum_contact_for_budget(m,200)
            if threshold is not None:
                from dataclasses import replace
                assert abs(optimise_fibre(replace(m,contact_fraction=threshold),max_um=200)['mass_ug_mm2']-1)<1e-8
    print('PASS: sequential exposure no-go under equal chemistry budget, contact budget roots')

if __name__=='__main__':
    next_checks()
    print('\nCOMPETENT ALTERNATIVE: staged exposure with SAME per-arm reaction budget')
    for v in (2,4,6):
        u=.56
        for fraction_old in (.1,.5,.9):
            print('v',v,'old fraction of fixed budget',fraction_old,'productive',round(sequential_cross_fixed_budget(v,u*fraction_old,u),6))
        print('maximum symmetric',p_two_sided(v,1,u,.5))
    print('\nMINIMUM NANOSCALE CONTACT FRACTION FOR 1ug/mm2 DRY CELLULOSE, max fibre reach L=200um')
    for q in (.7,calibration_scale(.7,.09)):
        for fs in (1.,.1):
            m=Model(arm_grafting_prob=q,individual_bond_force_nN=fs)
            print('q=',round(q,4),'f_s_nN=',fs,'c_min=',minimum_contact_for_budget(m,200))
    print('\nCONSERVATIVE DONOR-CLEAVAGE RISK: eta needed for positive one-to-one net event count')
    for q in (.7,calibration_scale(.7,.09)):
        for v in (2,4):
            print('q=',round(q,4),'v=',v,'eta_critical=',round(net_retention_threshold(v,q),6))

# Further attack: crack closure or reagent depletion can stop all linkers in
# the SAME local patch simultaneously. Shared random exposure produces many
# all-failure patches even if average graft counts appear adequate.
from scipy.special import roots_laguerre
from scipy.integrate import quad

# Gauss-Laguerre approximates E[g(Y)] for Y~Exp(1); use 160-point quadrature.
LAG_X,LAG_W=roots_laguerre(160)

def shared_window_stats(v=4,retained=.8,relative_rate=1.,linker_candidates=20):
    """A repair tile remains catalytically accessible for a single random
    shutdown time T~Exp(d). Individual reactive-arm reaction hazard k;
    ratio=k/d, no actual measured rate. All candidate linkers in the tile
    SHARE T, but react independently conditional on it.

    Conditional q=1-exp(-kT). Candidate linkers Poisson mean N, so a tile
    has zero complete old/new welds with probability exp(-N P_v(q)).
    Independent-window 'null' matches E[P_v] but gives failure exp(-N E[P_v]).

    Jensen guarantees E[exp(-N P)] >= exp(-N E[P]), i.e. common shutdown
    ALWAYS reduces tile reliability compared with independently averaged
    windows with same mean. Endogenous crack closure is potentially worse.
    """
    def p_of_y(y):
        q=-math.expm1(-relative_rate*y)
        return p_two_sided(v,q,retained)
    mean_p=shared_window_exact_mean(v,retained,relative_rate)
    failure_correlated=quad(lambda y:math.exp(-y-linker_candidates*p_of_y(y)),
                            0, math.inf,epsabs=1e-12,epsrel=1e-12,limit=200)[0]
    failure_independent=math.exp(-linker_candidates*mean_p)
    assert failure_correlated >= failure_independent-1e-12
    return {'mean_p':mean_p,'P_no_cross_shared':failure_correlated,
            'P_no_cross_independent':failure_independent,
            'P_at_least_one_shared':1.-failure_correlated,
            'P_at_least_one_independent':1.-failure_independent}


def shared_window_exact_mean(v=4,retained=.8,relative_rate=1.):
    """Independent analytic moment check for Gauss-Laguerre quadrature.
    E[(1-e^{-kT})^j]=sum_{a=0}^j (-1)^a C(j,a)/(1+a*k/d).
    """
    a=relative_rate
    val=0.
    for j in range(2,v+1):
        moment=sum(((-1)**z)*math.comb(j,z)/(1+z*a) for z in range(j+1))
        val+=(-1)**j * math.comb(v,j) * retained**j * (1.-2.**(1.-j)) * moment
    return val


def tail_checks():
    for valence in (2,3,4,6):
        for rel in (.09,.3,1,3,10):
            ans=shared_window_stats(v=valence,relative_rate=rel,linker_candidates=10)
            exact=shared_window_exact_mean(v=valence,relative_rate=rel)
            assert abs(ans['mean_p']-exact)<1e-9,(valence,rel,ans,exact)
    print('PASS: random shared reaction-window quadrature vs closed moments; Jensen failure inequality')

if __name__=='__main__':
    tail_checks()
    print('\nCORRELATED WINDOW (entire tile loses access together) VERSUS INDEPENDENT GRAFT WINDOWS')
    print('k/d | candidate linkers | mean pCross | tile failure shared | failure independent | 20-tile successful closure shared vs independent')
    for kd in (.09,.3,1,3,10):
        for N in (10,30):
            d=shared_window_stats(relative_rate=kd,linker_candidates=N)
            s=(1-d['P_no_cross_shared'])**20
            i=(1-d['P_no_cross_independent'])**20
            print(f'{kd:4.2f} {N:17d} {d["mean_p"]:11.4f} {d["P_no_cross_shared"]:19.4f} {d["P_no_cross_independent"]:19.4f} {s:18.6f} {i:17.6f}')

# Mechanism repair: preload/localize enzyme + bivalent or multivalent acceptor
# into the *overlap*, so extracellular covalent maturation persists for a
# deterministic minimum time t0 after live nutrient inflow ceases. The two-hit
# common-shutdown power law is replaced by a positive minimum reaction hazard.
def retained_maturation_failure(v=4,retained=.8,k_over_d=1.,N=30,t0_over_mean_shutdown=0.):
    def p(y):
        q=-math.expm1(-k_over_d*(y+t0_over_mean_shutdown))
        return p_two_sided(v,q,retained)
    return quad(lambda y:math.exp(-y-N*p(y)),0,math.inf,
                epsabs=1e-12,epsrel=1e-11,limit=200)[0]


def min_linkers_for_tiles(target=.90,tiles=20,t0=0.,k_over_d=1.,v=4,retained=.8):
    allowable=1-target**(1/tiles)
    func=lambda N:retained_maturation_failure(v,retained,k_over_d,N,t0)-allowable
    if func(1)<0:return 1.
    return brentq(func,1.,1e10,xtol=1e-7)


def maturation_checks():
    for kd in (.3,1.,3.):
        for N in (3.,30.,100.):
            x=retained_maturation_failure(k_over_d=kd,N=N,t0_over_mean_shutdown=0)
            y=shared_window_stats(relative_rate=kd,linker_candidates=N)['P_no_cross_shared']
            assert abs(x-y)<1e-10
        vals=[retained_maturation_failure(k_over_d=kd,N=30,t0_over_mean_shutdown=t) for t in (0,.1,.3,1,3)]
        assert all(a>=b for a,b in zip(vals,vals[1:]))
    print('PASS: retained extracellular maturation controls shared-shutdown failure monotonically')

if __name__=='__main__':
    maturation_checks()
    print('\nEXTRACELLULAR MATURATION REMEDY, exact N needed for 90% of 20 regions with >=1 complete weld')
    for t0 in (0,.02,.05,.1,.2,.3,.5,1.,2.):
        N=min_linkers_for_tiles(t0=t0,k_over_d=1.)
        print('post-shutdown guaranteed maturation duration in mean shutdown-time units=',t0,
              'Nmin=',math.ceil(N),'time-integrated q_floor=',round(1-math.exp(-t0),4))
    print('\nCHECK T0>0 restores exponential tail in N (failure numbers)')
    for N in (30,100,300,1000):
        print('N',N,'no_tail',retained_maturation_failure(N=N),
              't0=0.25',retained_maturation_failure(N=N,t0_over_mean_shutdown=.25))

# Final obstruction: all welding chemistry is worthless for a tile in which
# biosynthesis never first makes old/new cellulose contact before shared
# closure/inflow-loss. If physical-contact establishment time is Exp(g) and
# closure time Exp(d), probability of establishing contact first is g/(g+d).
# Conditional on contact, memoryless residual clock Exp(d). An extracellular
# post-closure enzyme reserve is useful only where contact was established.
def two_clock_tile_success(g_over_d,k_over_d=1.,N=30,t0=0.,v=4,retained=.8):
    p_contact=g_over_d/(1.+g_over_d)
    chemical_success=1.-retained_maturation_failure(v,retained,k_over_d,N,t0)
    return p_contact*chemical_success


def min_contact_rate_ratio_for_cycles(tiles=20,target=.9):
    pt=target**(1/tiles)
    return pt/(1-pt)


def contact_gate_checks():
    for g in (.1,1.,10.,200.):
        p=two_clock_tile_success(g,N=100000,t0=1.)
        assert p<=g/(g+1.)+1e-12
    target=min_contact_rate_ratio_for_cycles()
    assert abs((target/(1+target))**20-.9)<1e-12
    print('PASS: physical-contact-before-shutdown ceiling, no enzymatic rescue without contact')

if __name__=='__main__':
    contact_gate_checks()
    print('\nPHYSICAL CONTACT-CREATION GATE: even perfect subsequent chemistry cannot exceed')
    for g in (1,5,10,30,100,200):
        pc=g/(1+g)
        print('contact/closure rate',g,'per tile limit',pc,'20-tile ceiling',pc**20)
    print('contact:closure required for >=90% in 20 tiles even perfect weld:',min_contact_rate_ratio_for_cycles())
    print('\nBOTH GATES, full example chemistry post-shutdown t0=.3 in mean closure-time units')
    for g in (5,30,100,200,500):
        for N in (30,100):
            p=two_clock_tile_success(g,N=N,t0=.3)
            print('g/d',g,'N',N,'tile',round(p,6),'20 tiles',round(p**20,6))
