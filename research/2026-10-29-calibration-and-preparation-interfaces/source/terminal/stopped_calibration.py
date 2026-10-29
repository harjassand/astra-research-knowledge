"""Exact tools for the stopped-program calibration theorem.

Python >=3.10, standard library only.  Run `python stopped_calibration.py`.
This is a new, self-contained construction; it does not import earlier P3 code.

All mathematical checks use fractions/integers.  The seeded calibration draw
uses Python's PRNG and is an implementation demonstration, not evidence that
physical observations are IID or that a confidence theorem has been audited.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as F
from itertools import product
from math import ceil, log, tanh
from pathlib import Path
from random import Random
from time import perf_counter
import json


def solve(A, B):
    """Exact Gauss-Jordan, with several right-hand sides."""
    n = len(A)
    k = len(B[0])
    M = [[F(x) for x in A[i]] + [F(x) for x in B[i]] for i in range(n)]
    for j in range(n):
        pivot = next((i for i in range(j,n) if M[i][j]), None)
        if pivot is None:
            raise ValueError('Singular system: supply the transient subgraph.')
        M[j], M[pivot] = M[pivot], M[j]
        z = M[j][j]
        M[j] = [x/z for x in M[j]]
        for i in range(n):
            if i == j or not M[i][j]:
                continue
            z = M[i][j]
            M[i] = [x-z*y for x,y in zip(M[i],M[j])]
    return [row[n:n+k] for row in M]


def absorption(P, transient):
    """Absorbing endpoints follow the transient states, which come first."""
    n = transient
    A = [[F(i==j)-P[i][j] for j in range(n)] for i in range(n)]
    return solve(A, [row[n:] for row in P[:n]])


def conditional(p, event):
    total = sum(p[i] for i in event)
    if not total:
        raise ValueError('Zero-probability evidence.')
    return tuple(p[i]/total for i in event)


def tv(p,q):
    return sum(abs(x-y) for x,y in zip(p,q))/2


def rooted_forests(P, transient):
    """Independent exhaustive oracle, used only for small exact checks."""
    n = transient
    options = [[j for j,x in enumerate(P[i]) if x and j != i] for i in range(n)]
    for destinations in product(*options):
        roots = []
        valid = True
        for start in range(n):
            visited = set()
            at = start
            while at < n:
                if at in visited:
                    valid = False
                    break
                visited.add(at)
                at = destinations[at]
            if not valid:
                break
            roots.append(at-n)
        if valid:
            weight = F(1)
            for i,j in enumerate(destinations):
                weight *= P[i][j]
            yield tuple(destinations), tuple(roots), weight


@dataclass(frozen=True)
class Edge:
    src: int
    dst: int
    cost: int
    key: int
    parent: Edge | None = None


def minimum_rooted_arborescence(vertices, root, edges):
    """Exact integer Chu-Liu/Edmonds, oriented toward the root.

    Contract one directed cycle per recursion. Parallel arcs are retained.
    The output contains edges in the input graph, not contracted arcs.
    """
    vertices = set(vertices)
    selected = {}
    for v in vertices - {root}:
        choices = [e for e in edges if e.src == v and e.dst != v]
        if not choices:
            raise ValueError('No rooted arborescence exists.')
        selected[v] = min(choices, key=lambda e:(e.cost,e.key))
    cycle = None
    finished = {root}
    for start in vertices:
        seen = {}
        at = start
        while at not in finished and at not in seen:
            seen[at] = len(seen)
            at = selected[at].dst
        if at in seen:
            ordered = list(seen)
            cycle = set(ordered[seen[at]:])
            break
        finished.update(seen)
    if cycle is None:
        return list(selected.values())
    new = max(vertices)+1
    contracted = []
    for e in edges:
        a = new if e.src in cycle else e.src
        b = new if e.dst in cycle else e.dst
        if a == b:
            continue
        cost = e.cost - selected[e.src].cost if e.src in cycle else e.cost
        contracted.append(Edge(a,b,cost,e.key,e))
    chosen = minimum_rooted_arborescence((vertices-cycle)|{new},root,contracted)
    leaving = next(e for e in chosen if e.src == new)
    break_at = leaving.parent.src
    lifted = [e.parent for e in chosen]
    lifted += [selected[v] for v in cycle if v != break_at]
    return lifted


def forest_extreme(P, transient, costs, maximize=False):
    """Optimize a sum of integer edge costs over all absorption forests."""
    N = len(P)
    root = N
    edges = []
    key = 0
    for i in range(transient):
        for j,x in enumerate(P[i]):
            if x and i != j:
                c = costs[i,j]
                edges.append(Edge(i,j,-c if maximize else c,key))
                key += 1
    for j in range(transient,N):
        edges.append(Edge(j,root,0,key))
        key += 1
    chosen = minimum_rooted_arborescence(range(N+1),root,edges)
    original = [(e.src,e.dst) for e in chosen if e.src < transient]
    value = sum(costs[e] for e in original)
    return value, original


def _log_unit_interval(x, terms):
    assert F(1) <= x <= F(2)
    z = (x-1)/(x+1)
    square = z*z
    power = z
    total = F(0)
    for j in range(terms):
        total += power/F(2*j+1)
        power *= square
    low = 2*total
    remainder = 2*power/(F(2*terms+1)*(1-square))
    return low, low+remainder


def log_interval(x, bits=40):
    """Rigorous rational interval for log(x), width <=2^-bits."""
    x = F(x)
    if x <= 0:
        raise ValueError('Logarithm requires a positive rational.')
    if x == 1:
        return F(0),F(0)
    y = x
    power = 0
    while y >= 2:
        y /= 2
        power += 1
    while y < 1:
        y *= 2
        power -= 1
    terms = max(4,bits//3)
    target = F(1,1<<bits)
    while True:
        lo,hi = _log_unit_interval(y,terms)
        l2,h2 = _log_unit_interval(F(2),terms)
        if power >= 0:
            lo,hi = lo+power*l2, hi+power*h2
        else:
            lo,hi = lo+power*h2, hi+power*l2
        if hi-lo <= target:
            return lo,hi
        terms += 4


def floor_fraction(x):
    return x.numerator // x.denominator


def ceil_fraction(x):
    return -((-x.numerator)//x.denominator)


def forest_spread_certificate(P,Q,transient,bits=32):
    """Rigorous upper/lower bound on forest log-likelihood spread.

    The row gauge is removed exactly before taking logarithms. Integer
    arborescences give global extrema; no floating optimization is used.
    tanh(spread/4) is the sharp general tilt bound. We also return the
    entirely rational safe bound min(1,spread_upper/4).
    """
    if len(P) != len(Q):
        raise ValueError('Dimension mismatch.')
    S = 1<<bits
    lower,upper = {},{}
    for i in range(transient):
        options = [j for j in range(len(P)) if j != i and P[i][j]]
        if any(bool(P[i][j]) != bool(Q[i][j]) for j in range(len(P)) if j != i):
            raise ValueError('Off-diagonal supports differ.')
        if not options:
            raise ValueError('Nontransient row in transient subgraph.')
        reference = Q[i][options[0]]/P[i][options[0]]
        for j in options:
            ratio = (Q[i][j]/P[i][j])/reference
            lo,hi = log_interval(ratio,bits+4)
            lower[i,j] = floor_fraction(S*lo)
            upper[i,j] = ceil_fraction(S*hi)
    max_upper, max_edges = forest_extreme(P,transient,upper,True)
    min_lower, min_edges = forest_extreme(P,transient,lower,False)
    max_lower,_ = forest_extreme(P,transient,lower,True)
    min_upper,_ = forest_extreme(P,transient,upper,False)
    lo = max(F(0),F(max_lower-min_upper,S))
    hi = F(max_upper-min_lower,S)
    return {
        'spread_lower':lo, 'spread_upper':hi,
        'tv_upper_rational':min(F(1),hi/4),
        'max_upper_forest':max_edges, 'min_lower_forest':min_edges,
        'bits':bits,
    }


def random_absorbing_chain(rng,n,outcomes=3):
    N=n+outcomes
    P=[]
    for i in range(n):
        weights=[rng.randrange(0,7) for _ in range(N)]
        # Every transient row has a direct route to every absorbing outcome.
        for j in range(n,N):
            weights[j]=rng.randrange(1,7)
        total=sum(weights)
        P.append([F(x,total) for x in weights])
    for i in range(n,N):
        P.append([F(i==j) for j in range(N)])
    return P


def perturb_chain(P,n,rng):
    Q=[row[:] for row in P]
    for i in range(n):
        weights=[x*F(rng.randrange(85,116),100) for x in P[i]]
        total=sum(weights)
        Q[i]=[x/total for x in weights]
    return Q


def forest_checks():
    rng=Random(410129)
    chain_count=0
    posterior_checks=0
    forest_count=0
    arborescence_checks=0
    spread_checks=0
    for n in range(1,5):
        for trial in range(12):
            P=random_absorbing_chain(rng,n)
            Q=perturb_chain(P,n,rng)
            fp=list(rooted_forests(P,n))
            fq=list(rooted_forests(Q,n))
            assert [x[:2] for x in fp]==[x[:2] for x in fq]
            ratios=[b[2]/a[2] for a,b in zip(fp,fq)]
            spread_ratio=max(ratios)/min(ratios)
            forest_count+=len(fp)
            hp,hq=absorption(P,n),absorption(Q,n)
            for model,forests,h in ((P,fp,hp),(Q,fq,hq)):
                total=sum(x[2] for x in forests)
                for start in range(n):
                    recovered=[sum(w for _,r,w in forests if r[start]==out)/total for out in range(3)]
                    assert recovered==h[start]
            for start in range(n):
                for mask in range(1,8):
                    event=[j for j in range(3) if mask>>j&1]
                    distance=tv(conditional(hp[start],event),conditional(hq[start],event))
                    assert distance < 1
                    assert ((1+distance)/(1-distance))**2 <= spread_ratio
                    posterior_checks+=1
            costs={(i,j):rng.randrange(-30,31) for i in range(n) for j,p in enumerate(P[i]) if p and j!=i}
            expected=[sum(costs[i,j] for i,j in enumerate(dest)) for dest,_,_ in fp]
            assert forest_extreme(P,n,costs)[0]==min(expected)
            assert forest_extreme(P,n,costs,True)[0]==max(expected)
            arborescence_checks+=2
            if trial<3:
                certificate=forest_spread_certificate(P,Q,n,bits=20)
                l,h=log_interval(spread_ratio,32)
                assert certificate['spread_lower'] <= h
                assert certificate['spread_upper'] >= l
                # Each rounded edge interval has width at most two grid units.
                assert certificate['spread_upper']-certificate['spread_lower'] <= F(4*n,1<<20)
                spread_checks+=1
            # Change holding times by very large row factors; keep jump odds.
            W=[row[:] for row in P]
            for i in range(n):
                factor=F(1,2**(i+9))
                for j in range(len(P)):
                    if i!=j:
                        W[i][j]=P[i][j]*factor
                W[i][i]=1-sum(W[i][j] for j in range(len(P)) if j!=i)
            assert absorption(W,n)==hp
            assert forest_spread_certificate(P,W,n,bits=12)['spread_upper']==0
            chain_count+=1
    return dict(chains=chain_count,forests=forest_count,posterior_inequalities=posterior_checks,
                integer_arborescence_extrema=arborescence_checks,certified_spreads=spread_checks,
                row_speed_invariance=chain_count,status='PASS_EXACT_RATIONAL')


def gambler_chain(p,L):
    # Transient states correspond to positions 1,...,2L-1. Two terminals.
    n=2*L-1
    P=[[F(0) for _ in range(n+2)] for _ in range(n+2)]
    for i in range(n):
        minus=n if i==0 else i-1
        plus=n+1 if i==n-1 else i+1
        P[i][minus]=1-p
        P[i][plus]=p
    P[n][n]=P[n+1][n+1]=F(1)
    return P,n,L-1


def lower_bound_checks():
    cases=[]
    for L in (1,2,3,5,8,12):
        for p in (F(1,2),F(51,100),F(3,5)):
            P,n,start=gambler_chain(p,L)
            h=absorption(P,n)[start][1]
            formula=1/(1+((1-p)/p)**L)
            assert h==formula
            cases.append({'L':L,'p':str(p),'plus_probability':str(h)})
    return {'status':'PASS_EXACT_RATIONAL','cases':cases}


def deadline_failure():
    rows=[]
    for H in (4,16,64,256,1024):
        eta=F(1,H)
        a=(1+eta)**H
        b=(1-eta)**H
        posterior=a/(a+b)
        gap=posterior-F(1,2)
        # Three physical states: two live branches, one absorbing failure.
        # This is externally read at H, not an autonomous 3-state stop rule.
        assert gap>F(3,8)
        rows.append({'H':H,'local_relative_error':str(eta),'posterior_A':float(posterior),
                     'posterior_tv_from_half':float(gap),'evidence_base_log2':-H})
    return {'status':'PASS_EXACT_RATIONAL','rows':rows,
            'scope':'counterexample to omitting an external deadline from stopped-program state accounting'}


def composed_controller(p,gate_length=40,run_length=40,L=8):
    """Rare initial gate, recurrent waiting for a run, then gambler output."""
    g,r=gate_length,run_length
    n=g+r+(2*L-1)
    fail,minus,plus=n,n+1,n+2
    P=[[F(0) for _ in range(n+3)] for _ in range(n+3)]
    for i in range(g):
        P[i][i+1]=p
        P[i][fail]=1-p
    for j in range(r):
        i=g+j
        onward=i+1 if j+1<r else g+r+(L-1)
        P[i][onward]+=p
        P[i][g]+=1-p
    for j in range(2*L-1):
        i=g+r+j
        P[i][minus if j==0 else i-1]=1-p
        P[i][plus if j==2*L-2 else i+1]=p
    for i in (fail,minus,plus):
        P[i][i]=1
    return P,n


def acquisition_demo():
    gate,run,L=40,40,8
    K=gate+run+2*L-1
    epsilon,delta,beta=F(1,10),F(1,20),F(1,4)
    alpha=epsilon/K
    _,universal_log_upper=log_interval((1+alpha)/(1-alpha),40)
    universal_rational=min(F(1),K*universal_log_upper/4)
    # Exact conservative ln(2M/delta) enclosure; M=2 positive source cells.
    _,ln_upper=log_interval(F(4)/delta,40)
    samples=ceil_fraction(F(3)/(beta*alpha**2)*ln_upper)
    rng=Random(620261029)
    begun=perf_counter()
    heads=rng.getrandbits(samples).bit_count()
    draw_seconds=perf_counter()-begun
    p_hat=F(heads,samples)
    true_p=F(1,2)
    assert abs(p_hat-true_p)<=alpha*true_p
    true_matrix,n=composed_controller(true_p,gate,run,L)
    estimated_matrix,_=composed_controller(p_hat,gate,run,L)
    begun=perf_counter()
    h_true=absorption(true_matrix,n)[0]
    exact_true_seconds=perf_counter()-begun
    begun=perf_counter()
    h_hat=absorption(estimated_matrix,n)[0]
    exact_estimated_seconds=perf_counter()-begun
    assert h_true[1]+h_true[2]==true_p**gate
    assert h_hat[1]+h_hat[2]==p_hat**gate
    assert conditional(h_true,[1,2])==(F(1,2),F(1,2))
    expected_plus=1/(1+((1-p_hat)/p_hat)**L)
    assert conditional(h_hat,[1,2])[1]==expected_plus
    distance=tv(conditional(h_true,[1,2]),conditional(h_hat,[1,2]))
    # The conventional comparator is exactly this same absorbing linear solve.
    # No advantage over an equally informed solver is claimed.
    certificate=forest_spread_certificate(true_matrix,estimated_matrix,n,bits=24)
    assert distance<=certificate['tv_upper_rational']
    # This interval uses only the calibration event, empirical count, and
    # known controller formula. Unlike the pair certificate above, it does
    # not inspect the true source probability.
    p_low=max(p_hat/(1+alpha),1-(1-p_hat)/(1-alpha))
    p_high=min(p_hat/(1-alpha),1-(1-p_hat)/(1+alpha))
    posterior_low=1/(1+((1-p_low)/p_low)**L)
    posterior_high=1/(1+((1-p_high)/p_high)**L)
    data_only_error=max(expected_plus-posterior_low,posterior_high-expected_plus)
    assert posterior_low <= F(1,2) <= posterior_high
    assert distance <= data_only_error <= universal_rational <= epsilon
    expected_wait=(1-true_p**run)/((1-true_p)*true_p**run)
    return {
        'states_transient':K,'source_states':1,'source_outputs':2,
        'raw_coin_samples':samples,'heads':heads,'p_hat':str(p_hat),
        'relative_tolerance_alpha':str(alpha),'confidence_failure_delta':str(delta),
        'source_probability_floor_beta':str(beta),'target_epsilon':str(epsilon),
        'universal_posterior_tv_bound_display':tanh(K/4*log(float((1+alpha)/(1-alpha)))),
        'universal_safe_rational_bound':str(universal_rational),
        'universal_safe_rational_bound_display':float(universal_rational),
        'evidence_probability_true':str(true_p**gate),
        'expected_wait_after_gate_true':str(expected_wait),
        'posterior_plus_hat':str(expected_plus),'actual_posterior_tv':str(distance),
        'actual_posterior_tv_display':float(distance),
        'retrospective_pair_forest_spread_upper':str(certificate['spread_upper']),
        'retrospective_pair_tv_upper_rational':str(certificate['tv_upper_rational']),
        'retrospective_pair_tv_upper_display':float(certificate['tv_upper_rational']),
        'pair_certificate_access':'uses both true and estimated matrices; not a data-only certificate',
        'data_only_posterior_interval':[str(posterior_low),str(posterior_high)],
        'data_only_posterior_interval_display':[float(posterior_low),float(posterior_high)],
        'data_only_posterior_error_bound':str(data_only_error),
        'data_only_posterior_error_bound_display':float(data_only_error),
        'calibration_draw_seconds':draw_seconds,'conventional_solve_true_seconds':exact_true_seconds,
        'conventional_solve_estimated_seconds':exact_estimated_seconds,
        'comparator':'same-data exact absorbing-chain solve; identical predictions, no exclusive speedup',
        'randomness_status':'seeded PRNG implementation demonstration; IID validity is a theorem assumption',
        'scope':'terminal posterior only; neither a full stopped history nor a timed observation is emitted',
    }


def serialize(x):
    if isinstance(x,F):
        return str(x)
    raise TypeError(type(x).__name__)


def main():
    begun=perf_counter()
    checks=forest_checks()
    print('EXACT_FOREST_CHECKS',json.dumps(checks),flush=True)
    lower=lower_bound_checks()
    failure=deadline_failure()
    print('LOWER_BOUND_AND_DEADLINE_CHECKS_PASS',flush=True)
    demo=acquisition_demo()
    compact={k:v for k,v in demo.items() if k in (
        'states_transient','raw_coin_samples','heads','evidence_probability_true',
        'expected_wait_after_gate_true','actual_posterior_tv_display',
        'universal_safe_rational_bound_display','retrospective_pair_tv_upper_display',
        'data_only_posterior_interval_display','data_only_posterior_error_bound_display',
        'conventional_solve_true_seconds','conventional_solve_estimated_seconds')}
    print('ACQUISITION_DEMO',json.dumps(compact),flush=True)
    result={'status':'COMPLETED_LOCAL_CHECKS_NO_EXTERNAL_REVIEW','exact_checks':checks,
            'lower_bound_family':lower,'deadline_failure':failure,'acquisition_demo':demo,
            'wall_seconds':perf_counter()-begun}
    Path(__file__).with_name('stopped_calibration_results.json').write_text(json.dumps(result,indent=2,default=serialize))


if __name__=='__main__':
    main()
