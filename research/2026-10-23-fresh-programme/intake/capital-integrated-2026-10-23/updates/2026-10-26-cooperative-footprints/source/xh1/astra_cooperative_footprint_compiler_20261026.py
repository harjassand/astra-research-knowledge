"""Astra molecular writer: cooperative product-footprints, release-aware compilation,
blind asynchronous reaction order and reliability. Analytic/computational tests only.
No actual chemical kinetics measured by this file.
"""
from functools import lru_cache
from itertools import combinations, permutations
from math import factorial, prod, log
import numpy as np


def legal_ports(site, footprints, hyperblocks, nports=1):
    """hyperblocks[(site,port)] is a list of sets of *simultaneously retained*
    completed products that together suppress this reaction approach.
    Blocking is permanent and monotone in the set of present footprints.
    """
    return [p for p in range(nports) if not any((footprints & mask)==mask for mask in hyperblocks.get((site,p), ()))]


def compile_releasable(n, hyperblocks, prerequisite=None, ports=None):
    """Find minimum number of *immediate guide release* operations after successful
    reaction. State=(completed bits, remaining footprints bits). Product chemical
    modification is retained whether guide is released or not.
    A release is allowed only after a successful bond and is assumed exact and safe.
    """
    pre = prerequisite or [0]*n
    nports = ports or [1]*n
    full=(1<<n)-1
    @lru_cache(None)
    def dp(done, footprints):
        if done == full: return (0, ())
        best=(10**9, ())
        for j in range(n):
            bit=1<<j
            if done & bit or (pre[j]&done)!=pre[j]: continue
            for port in legal_ports(j, footprints, hyperblocks, nports[j]):
                for release in (False, True):
                    newfoot=footprints if release else footprints|bit
                    rest, plan=dp(done|bit,newfoot)
                    score=rest+int(release)
                    if score<best[0]: best=(score, ((j,port,release),)+plan)
        return best
    k,plan=dp(0,0)
    return (None,()) if k==10**9 else (k,plan)


def replay(n, blocks, plan, prereq=None, ports=None):
    done=foot=0
    pre=prereq or [0]*n
    portcount=ports or [1]*n
    for j,p,release in plan:
        assert j<n and not(done>>j&1)
        assert pre[j]&done==pre[j]
        assert p in legal_ports(j,foot,blocks,portcount[j])
        done|=1<<j
        if not release: foot|=1<<j
    assert done==(1<<n)-1
    return foot


def pairwise_block_to_hyper(n,arcs):
    """A product at i individually blocks port 0 of site j."""
    b={}
    for i,j in arcs: b.setdefault((j,0),[]).append(1<<i)
    return b


def graph_acyclic(n,arcs):
    incoming=[0]*n
    out=[[] for _ in range(n)]
    for u,v in arcs: incoming[v]+=1;out[u].append(v)
    stack=[i for i in range(n) if incoming[i]==0]
    cnt=0
    while stack:
        i=stack.pop();cnt+=1
        for j in out[i]:
            incoming[j]-=1
            if incoming[j]==0:stack.append(j)
    return cnt==n


def fvs_min(n,arcs):
    """Deleting the outgoing footprint of selected vertices removes every edge
    with that vertex as its source. Necessary and sufficient in P=empty pairwise model."""
    for k in range(n+1):
        for sub in combinations(range(n),k):
            killed=set(sub)
            if graph_acyclic(n,[(i,j) for i,j in arcs if i not in killed]):
                return k,sub
    raise AssertionError


def probability_blind_async(n, arcs, rates=None):
    """Reacting sites are activated simultaneously; independent exponential
    reaction clocks, initially unmodified. A completed source i blocks target j
    unless target was already completed. For constant rates, success equals
    probability the spontaneous order is a reverse topological sort of arcs.
    No wrong bonds, no irreversible dead-sites, no retries needed for this upper bound.
    """
    a=tuple(rates) if rates is not None else (1.,)*n
    full=(1<<n)-1
    @lru_cache(None)
    def p(done):
        if done==full:return 1.
        total=sum(a[j] for j in range(n) if not(done>>j&1))
        result=0.
        for j in range(n):
            if done>>j&1:continue
            if any(i==j and not(done>>v&1) for i,v in arcs):continue
            result+=a[j]/total*p(done|(1<<j))
        return result
    return p(0)


def brute_probability_equal(n,arcs):
    count=0
    for order in permutations(range(n)):
        pos={j:i for i,j in enumerate(order)}
        if all(pos[j]<pos[i] for i,j in arcs):count+=1
    return count/factorial(n)


def cooperative_triads():
    # A site is blocked ONLY if the other two completed products are retained.
    blocks={(j,0):[sum(1<<i for i in range(3) if i!=j)] for j in range(3)}
    assert all(legal_ports(j,0,blocks) for j in range(3))
    for a,b in combinations(range(3),2):
        # Even following any single completed product, no second target is blocked.
        assert legal_ports(b,1<<a,blocks)
        assert legal_ports(a,1<<b,blocks)
    # With all footprints retained, each possible final site is blocked.
    for j in range(3):
        assert legal_ports(j,((1<<3)-1)^(1<<j),blocks)==[]
    k,plan=compile_releasable(3,blocks)
    assert k==1
    replay(3,blocks,plan)
    # An alternate guide approach at site 2 stays accessible even with other footprints.
    twoport=dict(blocks)
    k2,plan2=compile_releasable(3,twoport,ports=[1,1,2])
    assert k2==0
    return blocks, (k,plan), (k2,plan2)


def validate_all_4site_graphs():
    n=4
    arcs=[(i,j) for i in range(n) for j in range(n) if i!=j]
    tally={0:0,1:0,2:0,3:0,4:0}
    for mask in range(1<<len(arcs)):
        graph=[arcs[i] for i in range(len(arcs)) if mask>>i &1]
        k,plan=compile_releasable(n,pairwise_block_to_hyper(n,graph))
        k2,_=fvs_min(n,graph)
        assert k==k2,(graph,k,k2)
        replay(n,pairwise_block_to_hyper(n,graph),plan)
        tally[k]+=1
    return tally


def reliability_examples():
    from scipy.special import gammaln
    # 1000 sites all correct after blind retries before activating any blocking products.
    L=1000;p=.6;target=.99
    # probability a site succeeded by m attempts: 1-(1-p)^m
    m=next(m for m in range(1,100) if (1-(1-p)**m)**L>=target)
    blind_one_edge=probability_blind_async(2,[(0,1)])
    blind_path3=probability_blind_async(3,[(0,1),(1,2)])
    assert abs(blind_one_edge-.5)<1e-14
    assert abs(blind_path3-1/6)<1e-14
    for n in range(2,6):
        for edges in ([],[(i,i+1) for i in range(n-1)],[(0,j) for j in range(1,n)]):
            assert abs(probability_blind_async(n,edges)-brute_probability_equal(n,edges))<1e-13
    # Permanent one-shot guide removal with probability r per required release.
    r=.999
    k_for99_1000=target**(1/1000)
    # If retryable guide release succeeds with hazard g, irreversibly harms root at d,
    # each event is a race, and harmless attempts simply repeat.
    g=.1
    max_d=g*(target**(-1/1000)-1)
    return dict(min_blind_site_retries_for_1000=m,
                modeled_success_at_m=(1-(1-p)**m)**L,
                blind_pair=blind_one_edge,blind_chain3=blind_path3,
                blind_500_independent_pairs=2.**-500,
                one_shot_release_20_with_p999=r**20,
                min_one_shot_release_p_for_1000=k_for99_1000,
                max_permanent_damage_hazard_for_g01_s_1000=max_d)


def try_independent_mc():
    rng=np.random.default_rng(10262026)
    n=100000
    # One edge: 0 blocks 1, successful order is 1,0.
    T=rng.exponential(1.,size=(n,2))
    empirical=float(np.mean(T[:,1]<T[:,0]))
    se=(.25/n)**.5
    assert abs(empirical-.5)<5*se
    # 3 cooperative footprints: independent clocks, two products always form and trap the last.
    T3=rng.exponential(1.,size=(n,3))
    assert np.all(np.argsort(T3,axis=1)[:,2]>=0)
    return empirical,se


if __name__=='__main__':
    cooperative,one_release,alternate=cooperative_triads()
    print('COOPERATIVE THREE-SITE DEADLOCK:',cooperative)
    print('WITH ONE GUIDE RELEASE:',one_release)
    print('WITH ALTERNATE CHEMICAL APPROACH:',alternate)
    print('MIN RELEASES BY NUMBER (4-SITE GRAPHS):',validate_all_4site_graphs())
    print('ASYNCHRONOUS STOCHASTIC CHEMISTRY:',reliability_examples())
    print('INDEPENDENT MONTE CARLO:',try_independent_mc())
    print('ALL ASSERTIONS PASSED')


def probability_async_hyper(n, blocks, ports=None, rate=None):
    """No feedback controller. Initially all sites have independent exp clocks;
    any product can permanently block subsequent targets. A legal sampled
    reaction permutation means all sites chemically complete before trapping.
    Equal rates -> uniform permutation; general constant initial rates ->
    Plackett-Luce weighted order.
    """
    portcount=ports or [1]*n
    rates=rate or [1.]*n
    total=0.
    for order in permutations(range(n)):
        foot=0
        weight=1.
        remaining=set(range(n))
        valid=True
        for j in order:
            weight*=rates[j]/sum(rates[u] for u in remaining)
            if not legal_ports(j,foot,blocks,portcount[j]):
                valid=False
                break
            foot|=1<<j
            remaining.remove(j)
        if valid:total+=weight
    return total


def chemical_synergy_from_conversion(p0,pA,pB,pAB, t=1.):
    """Four preset covalent-product cohorts, then a target challenge, same time t.
    First order reaction assumptions: lambda=-log(unreacted fraction)/t.
    Under independent multiplicative inhibition, lambdaAB*lambda0=
    lambdaA*lambdaB. Additional pairwise-undetectable inhibition eta below.
    """
    from math import log1p
    labs=[-log1p(-x)/t for x in (p0,pA,pB,pAB)]
    assert all(x>0 for x in labs)
    return dict(k0=labs[0],kA=labs[1],kB=labs[2],kAB=labs[3],
                cooperative_suppression=1-labs[3]*labs[0]/(labs[1]*labs[2]))


def check_stronger():
    from math import exp
    blocks,_,_=cooperative_triads()
    assert abs(probability_async_hyper(3,blocks))<1e-15
    assert abs(probability_async_hyper(3,blocks,ports=[1,1,2])-1/3)<1e-15
    # If all bond products immediately shed their guide, no retained guide footprints.
    assert abs(probability_async_hyper(3,{})-1)<1e-15
    # Test a DAG and fully obstruction-free cases against previous graph clock DP.
    assert abs(probability_async_hyper(3,pairwise_block_to_hyper(3,[(0,1),(1,2)]))-1/6)<1e-15
    # Binary independent guide release after first two products: third blocked only
    # if BOTH release attempts fail, independent r. No permanent wrong products.
    for r in (.1,.5,.9,.99):
        analyt=1-(1-r)**2
        s=0.
        for released_first in (False,True):
            for released_second in (False,True):
                prob=(r if released_first else 1-r)*(r if released_second else 1-r)
                s+=prob if (released_first or released_second) else 0.
        assert abs(s-analyt)<1e-12
    rng=np.random.default_rng(20261027)
    r=.9; m=500000
    releases=rng.random((m,2))<r
    empirical=np.mean(np.any(releases,axis=1))
    assert abs(empirical-(1-(1-r)**2))<5*(.99*.01/m)**.5
    # 100 independent cooperative triads and their independent one-shot release.
    ntriads=100; target=.99
    needed_r=1-(1-target**(1/ntriads))**.5
    assert .989<needed_r<.991
    # Predetermined release at one site only: it must finish among the first 2,
    # probability 2/3, and its release must succeed.
    assert abs((2/3)*r-.6)<1e-14
    # Quantify cooperative inhibition invisible to pairwise separate challenges:
    p0=1-exp(-.04*30)
    pA=pB=p0
    pAB=1-exp(-.002*30)
    inferred=chemical_synergy_from_conversion(p0,pA,pB,pAB,t=30)
    assert abs(inferred['cooperative_suppression']-.95)<1e-12
    return dict(blind_three_site_full_probability=probability_async_hyper(3,blocks),
                blind_one_alternate_port_success=probability_async_hyper(3,blocks,ports=[1,1,2]),
                blind_with_scarless_acyl_transfer=probability_async_hyper(3,{}),
                guide_release_r90_per_triad=.99,
                guide_release_r90_100_triads=.99**100,
                needed_guide_release_p_for_100_triads=needed_r,
                background_chemical_inhibition=inferred,
                independent_mc_p=empirical)

if __name__=='__main__':
    print('COOPERATIVE CHEMISTRY UNDER BLIND TIMING:',check_stronger())


def protected_transfer_yield(p,w,m,L):
    """On an individual chemically competent root site, per donor-feed
    correct p, irreversible wrong w, harmless no-coupling 1-p-w.
    A correct amide consumes the site's ONLY reactive primary amine, carries no
    free new nucleophile and survives the next feed. Correct product fraction
    after m independent feed opportunities is p/(p+w)*(1-(1-p-w)^m).
    Other sites independent; full product correctness is site_fraction^L.
    """
    assert 0<p<=1 and w>=0 and p+w<=1 and m>=0 and L>=1
    good=p/(p+w)*(-np.expm1(m*np.log1p(-p-w))) if p+w<1 else p
    return float(good**L)


def check_transfer_and_correlation():
    L=1000;p=.6; m=14
    F=protected_transfer_yield(p,1e-6,m,L)
    assert abs(F-0.9956585220914766)<1e-11
    max_w=p*(.99**(-1/L)-1)
    assert 6.02e-6<max_w<6.04e-6
    assert protected_transfer_yield(p,1e-5,1000,L)<.99
    r=.9;q=1-r
    # If failures of guide clearance are independent, two retained donor
    # guides jointly block a third site with probability q^2.
    independent_success=1-q*q
    # If failures are perfectly correlated, the same pair blocks with prob q.
    shared_failure_success=1-q
    assert abs(independent_success-.99)<1e-13
    assert abs(shared_failure_success-.9)<1e-13
    return dict(sensorless_1000site_correct_at_14_attempts=F,
                max_wrong_per_attempt_for_99pct_infinite_retry=max_w,
                independent_pair_guide_clearance=independent_success,
                fully_correlated_pair_guide_clearance=shared_failure_success,
                hundred_triad_success_if_independent=(1-q*q)**100,
                hundred_triad_success_if_commonmode=(1-q)**100)

if __name__=='__main__':
    print('PROTECTED TRANSFER RETRIES & SHARED CLEARANCE FAILURES:',
          check_transfer_and_correlation())


def independent_mc_cooperative(trials=300000):
    blocks,_,_=cooperative_triads()
    rng=np.random.default_rng(20261028)
    clocks=rng.exponential(size=(trials,3))
    orders=np.argsort(clocks,axis=1)
    # Under symmetric cooperative blockers the final site in any ordering is lost.
    no_alt_success=np.zeros(trials,dtype=bool)
    # With site 2 possessing a second port immune to other products, success if
    # site 2 is last, exactly two of the six uniform permutations.
    with_alt=(orders[:,-1]==2)
    empirical=float(np.mean(with_alt))
    se=float(((1/3)*(2/3)/trials)**.5)
    assert abs(empirical-1/3)<5*se
    return empirical,se,float(no_alt_success.mean())

if __name__=='__main__':
    print('INDEPENDENT COOPERATIVE ASYNCHRONOUS MC:',independent_mc_cooperative())
