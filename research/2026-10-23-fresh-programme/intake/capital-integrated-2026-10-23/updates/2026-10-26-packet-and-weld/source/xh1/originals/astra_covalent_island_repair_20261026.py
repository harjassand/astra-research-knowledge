"""Astra chemical assembly: rigorous topology/renewal/clearance calculations.

Conceptual conditional model, NOT a lab demonstration. Experimental comparators:
Niu, Hili, Liu (2013) Nature Chemistry doi:10.1038/nchem.1577
Argueta-Gonzalez et al. (2022) RSC Chem Biology doi:10.1039/D2CB00020B
Frommer et al. (2024) Angew Chem doi:10.1002/anie.202317482
Nian et al. (2025) Nature Comm doi:10.1038/s41467-025-60143-3

All numerical p, rate, gate error, and off-target numbers below are hypothetical.
"""
import math
import numpy as np
from scipy.stats import nbinom
from scipy.optimize import brentq
from functools import lru_cache
from math import comb


def all_partner_correct(n, beta_over_k):
    """Exact all-correct probability in sequential independent exponential
    matching race among n initially present cognate azide-alkyne pairs.
    Each cognate pair has k and every ordered off-pair has beta; any wrong
    covalent bond is absorbing failure. Correct edge consumes both handles.
    """
    return math.exp(-sum(math.log1p(j*beta_over_k) for j in range(n)))


def beta_threshold(n, fidelity):
    return brentq(lambda x: all_partner_correct(n,x)-fidelity,0,1,xtol=1e-18)


def exact_spatial_matching(n, beta_over_k, decay_length):
    """Exact DP over subsets of still-unreacted cognate pairs. Rate for
    noncognate A_i+B_j: beta*exp(-(abs(i-j)-1)/decay_length) if i!=j.
    All-correct dynamic on correct-events-only pathways. n<=17 for speed.
    No site rearrangement after reaction and fixed DNA positional rates.
    """
    assert 1<=n<=17
    b = np.array([[0 if i==j else beta_over_k*math.exp(-(abs(i-j)-1)/decay_length)
                   for j in range(n)] for i in range(n)])
    dp=np.zeros(1<<n)
    dp[0]=1
    for mask in range(1,1<<n):
        sites=[i for i in range(n) if (mask>>i)&1]
        nleft=len(sites)
        wrong=sum(b[i,j] for i in sites for j in sites if i!=j)
        dp[mask]=sum(dp[mask &~(1<<i)] for i in sites)/(nleft+wrong)
    return float(dp[-1])


def max_run_chance(n,p,run):
    """Exact probability Bernoulli(p) sequence has >=run consecutive successes."""
    vec=np.zeros(run); vec[0]=1
    for _ in range(n):
        new=np.zeros(run)
        new[0]=(1-p)*vec.sum()
        new[1:]=p*vec[:-1]
        vec=new
    return 1-float(vec.sum())


def multivalent_stripping_time(m,u,a):
    """Exact mean time to 0 bound arms in birth-death chain: n->n-1 at n*u,
    n->n+1 at (m-n)*a, starting n=m, 0 an absorbing wash sink.
    Arms exchange and rebind independently; real PNA may be cooperative.
    """
    assert m>=1 and u>0 and a>=0
    r=a/u
    ans=0.
    for n in range(1,m+1):
        term=sum((comb(m,k)/comb(m,n))*r**(k-n) for k in range(n,m+1))
        ans+=term/(n*u)
    return ans


def stripping_lower_bound(m,u,a):
    """First summand of exact mean; exponential in m for a>0."""
    if a==0:return 1/u
    return (math.pow(1+a/u,m)-1)/(m*a)


def prefix_ratchet(L,p,quantile=.99):
    """Each round tries every remaining edge independently; only rooted
    contiguous prefix is retained after denaturing clearance; detached
    islands discarded; next round refills downstream. Thus rounds to finish
    are 1+NegBin(L,p) number of failures before L successes.
    """
    expected=1+L*(1-p)/p
    variance=L*(1-p)/p**2
    quant=int(nbinom.ppf(quantile,L,p))+1
    return expected,math.sqrt(variance),quant


def all_edges_held_rounds(L,p,F=.99):
    return math.ceil(math.log(-math.expm1(math.log(F)/L))/math.log1p(-p))


def packet_prefix_quantile(L,b,p,F=.99):
    """N=L/b parallel independently rooted packets, each self-cleared.
    This *excludes* final packet joining and connector damage!
    """
    assert L % b==0
    N=L//b
    x=1
    while nbinom.cdf(x-1,b,p)**N<F:
        x+=1
    return x


def packet_all_correct(L,b,beta_over_k,gate_failure):
    """Fidelity bound for isolated packets of b junctions: all-to-all
    wrong partner CuAAC inside each packet, while packet joins each have
    independent failed gate with probability gate_failure. Finite L %b=0.
    No overlap or incomplete packet handling; comparator only.
    """
    assert L % b==0
    N=L//b
    f=all_partner_correct(b,beta_over_k)
    return f**N*(1-gate_failure)**(N-1)


def graph_path_alternations(n):
    """With 2m individually distinct AA/BB vertices, fixed first A and
    last B, alternating Hamiltonian paths that satisfy valency/endpoints.
    Neither mass, total edge count, fixed ends nor parity identifies order.
    """
    assert n%2==0
    m=n//2
    return math.factorial(m-1)**2


def check_dp_against_all_to_all():
    # separate exact DP for distance-decay -> uniform at long decay length
    for n in [3,6,9]:
        r=.003
        x=exact_spatial_matching(n,r,decay_length=1e10)
        y=all_partner_correct(n,r)
        assert abs(x-y)<1e-9,(n,x,y)


def check_mfpt_linear_algebra():
    for m in [1,2,5,8]:
        for a in [0,.03,.3,.9]:
            u=.3
            Q=np.zeros((m,m))
            for n in range(1,m+1):
                Q[n-1,n-1] = -n*u-(m-n)*a
                if n>1:Q[n-1,n-2]=n*u
                if n<m:Q[n-1,n]=(m-n)*a
            t=np.linalg.solve(-Q,np.ones(m))[-1]
            closed=multivalent_stripping_time(m,u,a)
            assert math.isclose(t,closed,rel_tol=1e-10,abs_tol=1e-10),(m,a,t,closed)
            assert closed>=stripping_lower_bound(m,u,a)-1e-10


def mc_prefix_check():
    rng=np.random.default_rng(2601)
    L=30;p=.6;trials=100000
    rounds=1+rng.negative_binomial(L,p,size=trials)
    expect,sd,_=prefix_ratchet(L,p)
    se=sd/math.sqrt(trials)
    assert abs(rounds.mean()-expect)<5*se
    print('MC prefix renewal',rounds.mean(),'expected',expect,'sampleSE',se)


def main():
    check_dp_against_all_to_all()
    check_mfpt_linear_algebra()
    mc_prefix_check()
    print('\nALL-PARTNER MATCHING COVALENT FIDELITY')
    for n in [16,100,1000]:
        b=beta_threshold(n,.99)
        print('n=',n,'beta/k maximal for >=99%',b,
              'at beta/k=1e-7, P=',all_partner_correct(n,1e-7))
    print('\nSPATIAL MATCHING DP (n=14; beta/k=0.001)')
    for xi in [.25,.5,1,2,1e10]:
        print('decay range',xi,'Pcorrect=',exact_spatial_matching(14,.001,xi))
    print('\nFALSE TOPOLOGY DEGENERACY')
    for n in [6,10,20]:
        print('distinct alternating 2-ended full-length paths n=',n,
              'count',graph_path_alternations(n))
    print('\nLONGEST DISCONNECTED ISLAND: probability >=r consecutive joined edges (n=1000,p=.6)')
    for r in [8,10,12,14,16,20]:
        print('r=',r,'probability',max_run_chance(1000,.6,r))
    print('\nMULTIARM STRIPPING (u=.3 /s); mean seconds')
    for m in [1,2,5,10,14,20]:
        print('arms=',m,'a=0:',multivalent_stripping_time(m,.3,0),
              'a=.03:',multivalent_stripping_time(m,.3,.03),
              'a=.3:',multivalent_stripping_time(m,.3,.3))
    print('\nROUNDS FOR CORRECT CONTIGUOUS ROOTED PRODUCT: L=1000')
    for p in [.6,.9,.99]:
        e,sd,q=prefix_ratchet(1000,p)
        held=all_edges_held_rounds(1000,p)
        print('p=',p,'prefix mean',e,'sd',sd,'99th pct',q,
              'unstripped-edges rounds for >=99% complete',held)
    print('\nINDIVIDUALLY ROOTED PACKETS WITHOUT FUSION: L=1000 p=.6')
    for b in [5,10,20,50,100,200,1000]:
        print('b=',b,'99pct all packet prefixes complete by round=',packet_prefix_quantile(1000,b,.6))
    print('\nISOLATED PACKET CONNECTOR QUALITY (L=1000, beta/k=1e-7, connector failure=1e-4)')
    cand=[]
    for b in [1,2,4,5,8,10,20,25,40,50,100,125,200,250,500,1000]:
        f=packet_all_correct(1000,b,1e-7,1e-4)
        cand.append((f,b))
        print('packet b=',b,'model fidelity=',f)
    print('best among sampled',max(cand))
    assert packet_all_correct(1000,40,1e-7,1e-4)>.99
    assert all_partner_correct(1000,1e-7)<.99
    print('\nAll verified assertions passed (hypothetical rates, no physical system claimed).')

if __name__=='__main__':main()

# Additional independent consequences from the same controlled model.

def chemically_identical_pulses(k,w,total_exposure):
    """If all hazards are proportional to catalyst activity c(t), only
    E=integral c(t)dt enters the outcome. Holding vs N equal pulses tie.
    The edge is assumed irreversibly joined right or wrong, otherwise intact.
    """
    assert k>=0 and w>=0 and total_exposure>=0
    return 0 if k+w==0 else k/(k+w)*(-math.expm1(-(k+w)*total_exposure))


def cut_clearance_probability(anchors,cleavage_per_anchor):
    """Strong stringent-cut model: EVERY remnant tether keeps an island
    attached to carrier. Assumes independent cutting and no spontaneous
    release of tethered fragments. Only a conditional counterexample.
    """
    return cleavage_per_anchor**anchors


def required_cut_fidelity(anchors,target):
    return target**(1/anchors)


def required_photodamage_rate(rounds,target=.99):
    """per-reset irreversible damage probability, independent."""
    return 1-target**(1/rounds)


def packet_beta_limit(L,b,gate_failure,target=.99):
    return brentq(lambda r:packet_all_correct(L,b,r,gate_failure)-target,0,0.01,xtol=1e-18)


def check_pulse_invariance():
    k=.6;w=.01
    E=4.8
    once=chemically_identical_pulses(k,w,E)
    # discrete survival propagation repeated pulses including irreversibly
    # correct/wrong absorption. An experiment fixing E cannot distinguish.
    a=0.;b=0.;q=1.
    for interval in [.8]*6:
        alpha=-math.expm1(-(k+w)*interval)
        a+=q*alpha*k/(k+w)
        b+=q*alpha*w/(k+w)
        q*=1-alpha
    assert math.isclose(a,once,rel_tol=1e-12)
    assert math.isclose(a+b+q,1,rel_tol=1e-12)
    return a,b,q


def next_results():
    print('\n=== PULSING ONLY CHANGES CLOCK, NOT FIDELITY, IF ALL HAZARDS SCALE TOGETHER ===')
    print('6 pulses vs one continuous equal catalytic exposure, k=.6,w=.01,E=4.8', check_pulse_invariance())
    print('\n=== CUT-REQUIRED SCALING TO GET 99% CLEARANCE ===')
    for N in [10,100,500,1000]:
        c=required_cut_fidelity(N,.99)
        print('tethers',N,'single-cut reliability needed',c,'if c=.999 probability',cut_clearance_probability(N,.999))
    print('\n=== DAMAGE CEILING FOR REPEATED RESET ===')
    for n in [13,35,112,668]:
        print('reset rounds',n,'max independent irreversible damage per reset',required_photodamage_rate(n))
    print('\n=== SIZING FIDELITY WINDOW FOR 1000 EDGES ===')
    for b in [10,20,40,50,100,200,1000]:
        limit=packet_beta_limit(1000,b,1e-4,.99)
        print('packet junctions',b,'beta/k threshold for 99% all-correct',limit)
    print('A single right-vs-wrong reactivity multipler without spatial restriction needs >', 1e-6/beta_threshold(1000,.99),'when initial beta/k=1e-6')

if __name__ == '__main__':next_results()

# Covenantly rooted prefix ratchet: all downstream links are attempted each
# round, then every unrooted island is physically discarded and replenished.
# This is distinct from persistent parallel click where all islands are kept.

def wasted_successful_downstream_links(L,p):
    """Exact expectation of chemically successful click events sacrificed
    because an earlier edge was missing during that round. Assumes every
    yet-unretained downstream junction is attempted once per round,
    each with independent probability p, and all unrooted islands disappear.
    Formula from sum over earlier-edge failures (negative-binomial renewal).
    """
    return (1-p)*L*(L-1)/2


def packet_waste(L,b,p):
    assert L % b == 0
    return (L//b)*wasted_successful_downstream_links(b,p)


def mc_wasted_successes(L,p,trials=15000,seed=3341):
    rng=np.random.default_rng(seed)
    rounds=np.empty(trials,dtype=int)
    wastes=np.empty(trials,dtype=int)
    for t in range(trials):
        prefix=0;r=0;waste=0
        while prefix<L:
            r+=1
            outcome=rng.random(L-prefix)<p
            first_fail=np.flatnonzero(~outcome)
            j=first_fail[0] if len(first_fail)>0 else len(outcome)
            if j<len(outcome):
                waste+=int(outcome[j+1:].sum())
            prefix+=j
        rounds[t]=r;wastes[t]=waste
    return rounds,wastes


def new_prefix_results():
    print('\n=== COVALENT-ISLAND WASTE THEOREM ===')
    for L,p in [(20,.6),(30,.9),(1000,.6),(1000,.9),(1000,.99)]:
        expectation=wasted_successful_downstream_links(L,p)
        print('L=',L,'p=',p,'expected wasted formed bonds',expectation,
              'retained correct bonds',L,'waste per retained',expectation/L)
    r,w=mc_wasted_successes(25,.6)
    theory_w=wasted_successful_downstream_links(25,.6)
    theory_r=prefix_ratchet(25,.6)[0]
    se_w=w.std(ddof=1)/math.sqrt(len(w))
    se_r=r.std(ddof=1)/math.sqrt(len(r))
    print('MC success-waste L25 p.6:',w.mean(),'theory',theory_w,'SE',se_w,
          'rounds MC',r.mean(),'theory',theory_r)
    assert abs(w.mean()-theory_w)<5*se_w
    assert abs(r.mean()-theory_r)<5*se_r
    print('\n=== PACKETS CURE QUADRATIC WASTE ONLY IF ROOTED AND JOINABLE ===')
    L=1000;p=.6
    for b in [5,10,20,40,50,100,200,1000]:
        if L%b==0:
            print('L',L,'p',p,'packet size',b,
                  'total expected wasted bonds',packet_waste(L,b,p),
                  'global expected lost fraction',packet_waste(L,b,p)/wasted_successful_downstream_links(L,p))

if __name__=='__main__':new_prefix_results()
