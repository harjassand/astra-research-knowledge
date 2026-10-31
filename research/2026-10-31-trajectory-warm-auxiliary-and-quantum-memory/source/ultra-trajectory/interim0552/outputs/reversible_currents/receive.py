#!/usr/bin/env python3
"""Exact finite controls for the two analytic proofs in this directory.

This receiver supplies finite algebra/implementation evidence, not an
independent proof audit or a physical data set. All simulation is labelled.
"""
from collections import defaultdict
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import importlib.util
import json
import math
import random
import time

from currents import (binomial_power, critical_score, evaluate as current_eval,
                      log_bounds, lower_rate_interval, q_bound)
from dual_trace import evaluate as dual_eval, load_certificate

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def old_receiver():
    spec = importlib.util.spec_from_file_location(
        "earlier_predictive_receiver", HERE.parent/'predictive_flow/receive.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def reversible_kernel(weights):
    n = len(weights)
    rows = [sum(row) for row in weights]
    total = sum(rows)
    pi = [Q(r, total) for r in rows]
    P = [[Q(v, rows[i]) for v in weights[i]] for i in range(n)]
    assert all(pi[i]*P[i][j] == pi[j]*P[j][i] for i,j in product(range(n),repeat=2))
    return P, pi


def current_laws(P, pi, g, horizon, alternate=False):
    states = {(i, 0): p for i,p in enumerate(pi)}
    out = []
    for t in range(horizon):
        next_states = defaultdict(Q)
        for (i, score), p in states.items():
            for j, transition in enumerate(P[i]):
                if transition:
                    inc = g[i][j] * (-1 if alternate and t%2 else 1)
                    next_states[j, score+inc] += p*transition
        states = next_states
        law = defaultdict(Q)
        for (i, score), p in states.items():
            law[score] += p
        assert sum(law.values()) == 1
        out.append(dict(law))
    return out


def null_current_controls(rng):
    checked = mgfs = tails = 0
    for trial in range(24):
        n = 2+trial%4
        weights = [[0]*n for _ in range(n)]
        g = [[0]*n for _ in range(n)]
        for i in range(n):
            for j in range(i,n):
                weights[i][j] = weights[j][i] = rng.randrange(1,10)
                if i != j:
                    g[i][j] = rng.choice((-1,1))
                    g[j][i] = -g[i][j]
        P, pi = reversible_kernel(weights)
        for t,law in enumerate(current_laws(P,pi,g,8),1):
            for r in (Q(3,2),Q(2),Q(3)):
                mgf = sum((p*r**s for s,p in law.items()),Q(0))
                assert mgf <= ((r+1/r)/2)**t
                mgfs += 1
            for threshold in range(t%2,t+1,2):
                tail = sum((p for s,p in law.items() if abs(s)>=threshold),Q(0))
                assert tail <= q_bound(t,threshold)
                tails += 1
        checked += 1
    # A genuine reversible chain attaining the mgf bound exactly.
    P = [[Q(i!=j,2) for j in range(3)] for i in range(3)]
    g = [[0 if i==j else 1 if (j-i)%3==1 else -1 for j in range(3)] for i in range(3)]
    for n,law in enumerate(current_laws(P,[Q(1,3)]*3,g,12),1):
        expected = {2*k-n:Q(math.comb(n,k),2**n) for k in range(n+1)}
        assert law == expected
    return {'rational_reversible_chains': checked,
        'exact_mgf_inequalities': mgfs, 'exact_tail_inequalities': tails,
        'sharp_three_cycle_binomial_mgf_received_through_n': 12}


def cover_controls(P,pi,labels):
    states=list(product(range(len(P)),(-1,1)))
    flow={}
    for i,h in states:
        for j,trans in enumerate(P[i]):
            if trans:
                flow[(i,h),(j,-h)]=pi[i]*trans/2
    for i,h in states:
        outgoing=sum((v for (x,y),v in flow.items() if x==(i,h)),Q(0))
        incoming=sum((v for (x,y),v in flow.items() if y==(i,h)),Q(0))
        assert outgoing==incoming==pi[i]/2
    for (x,y),mass in flow.items():
        i,h=x; j,hh=y
        assert hh==-h
        reverse=flow.get((y,x),Q(0))
        assert reverse>0
        assert mass/reverse == (pi[i]*P[i][j])/(pi[j]*P[j][i])
        g=h*(1 if labels[i]==labels[j] else -1)
        rg=hh*(1 if labels[i]==labels[j] else -1)
        assert g==-rg
    return {'stationary_lift_edges':len(flow),'edge_entropy_ratios_preserved':True}


def source_controls(old):
    b=Q(1,2)
    states,labels,P,pi=old.source(b)
    for i,(s,t) in enumerate(states):
        q=s*t
        positive=Q(0)
        for j,(ss,tt) in enumerate(states):
            if P[i][j]:
                assert ss*tt==-q
                eta=q*s*ss
                if eta==1: positive+=P[i][j]
        assert positive==Q(3,4)
    g=[[1 if labels[i]==labels[j] else -1 for j in range(4)] for i in range(4)]
    for n,law in enumerate(current_laws(P,pi,g,12,True),1):
        absolute=defaultdict(Q)
        for s,p in law.items(): absolute[abs(s)]+=p
        expected=defaultdict(Q)
        for k in range(n+1): expected[abs(2*k-n)]+=Q(math.comb(n,k)*3**k,4**n)
        assert dict(absolute)==dict(expected)
    alpha=Q(1,40)
    n=88; critical=critical_score(n,alpha)
    assert critical==28
    power=binomial_power(n,critical)
    assert power>=1-alpha
    assert all(binomial_power(t,critical_score(t,alpha))<1-alpha for t in range(1,n))
    hold=Q(1,100000)
    lazy=[[hold*(i==j)+(1-hold)*P[i][j] for j in range(4)] for i in range(4)]
    assert all(lazy[i][i]>0 for i in range(4))
    lazy_power=(1-hold)**n*power
    assert lazy_power>=1-alpha
    cover=cover_controls(P,pi,labels)
    return states,labels,P,pi,{
        'source_driving_sign_probability_exact':'3/4',
        'exact_binomial_absolute_score_law_checked_through_n':12,
        'first_current_horizon':n,'critical_score':critical,
        'exact_power':str(power),'power_preview':float(power),
        'aperiodic_hold_probability':str(hold),
        'aperiodic_power_lower':str(lazy_power),
        'aperiodic_power_lower_preview':float(lazy_power), 'cover':cover}


def dormant_control(P,pi,labels):
    n=len(P); w=Q(1,10); eps=Q(1,10000); delta=eps*(1-w)/w
    new=[[Q(0)]*(2*n) for _ in range(2*n)]
    for i in range(n):
        for j in range(n): new[i][j]=(1-delta)*P[i][j]
        new[i][n+i]=delta
        new[n+i][i]=eps
        new[n+i][n+i]=1-eps
    pnew=[w*p for p in pi]+[(1-w)*p for p in pi]
    assert all(sum(row)==1 for row in new)
    assert all(sum(pnew[i]*new[i][j] for i in range(2*n))==pnew[j] for j in range(2*n))
    factor=w*(1-delta)
    for i,j in product(range(n),repeat=2):
        assert pnew[i]*new[i][j]==factor*pi[i]*P[i][j]
    for i in range(n): assert pnew[i]*new[i][n+i]==pnew[n+i]*new[n+i][i]
    for a in set(labels):
        assert sum((pnew[i] for i in range(2*n) if labels[i%n]==a),Q(0)) == sum((pi[i] for i in range(n) if labels[i]==a),Q(0))
    # Test the exact active/no-bridge submeasure on every path of 4 steps.
    checked=0
    for path in product(range(n),repeat=5):
        base=pi[path[0]]; extended=pnew[path[0]]
        for i,j in zip(path,path[1:]): base*=P[i][j]; extended*=new[i][j]
        assert extended==w*(1-delta)**4*base
        checked+=1
    return {'states':2*n,'active_weight':str(w),'bridge_epsilon':str(eps),
        'active_exit_probability':str(delta),'exact_entropy_scale':str(factor),
        'visible_one_time_marginal_exactly_preserved':True,
        'no_bridge_submeasure_paths_checked':checked}


def bridge_controls(cert,P,pi,labels):
    assert cert['depth']==1 and cert['alphabet']==2
    k=cert['mesh']; d=len(cert['descriptors'])
    index={node:i for i,node in enumerate(cert['nodes'])}
    u=[[sum((P[i][j] for j,a in enumerate(labels) if a==b),Q(0)) for b in (0,1)] for i in range(len(P))]
    fs=[]; hs=[]
    hlookup=dict(zip(cert['words'],cert['H']))
    for i,a in enumerate(labels):
        x=k*u[i][0]; lo=x.numerator//x.denominator; rem=x-lo
        rounded=[(lo,Q(1))] if rem==0 else [(lo,1-rem),(lo+1,rem)]
        f=[Q(0),Q(0)]
        for (c0,p0),(c1,p1) in product(rounded,repeat=2):
            ii=index[a,(c0,k-c0),(c1,k-c1)]
            for y,(_,b,w,sign) in zip(cert['y'][ii*d:(ii+1)*d],cert['descriptors']):
                assert w==()
                f[b]+=p0*p1*sign*y
        fs.append(f)
        hs.append(sum((u[i][left]*u[i][right]*hlookup[left,a,right]
                      for left,right in product((0,1),repeat=2)),Q(0)))
        assert sum(map(abs,f))<=cert['B']
    M=[[sum((fs[i][b]*((labels[j]==b)-u[i][b]) for b in (0,1)),Q(0)) for j in range(len(P))] for i in range(len(P))]
    margin=min(hs[i]+hs[j]-M[i][j]-M[j][i] for i,j in product(range(len(P)),repeat=2))
    assert margin>=0
    for i in range(len(P)):
        assert sum((P[i][j]*M[i][j] for j in range(len(P))),Q(0))==0
        assert max(M[i])-min(M[i])<=cert['B']
    rev=all(pi[i]*P[i][j]==pi[j]*P[j][i] for i,j in product(range(len(P)),repeat=2))
    backwards=[[pi[j]*P[j][i]/pi[i] for j in range(len(P))] for i in range(len(P))]
    back_means=[sum((backwards[j][i]*M[j][i] for i in range(len(P))),Q(0)) for j in range(len(P))]
    # M(X_{t+1},X_t) conditioned on X_{t+1}=j has expectation of M(j,i).
    if rev: assert all(v==0 for v in back_means)
    # Check the observed-word innovation equations, including hidden memory.
    failures=[]
    for x in range(len(P)):
        for past in (0,1):
            mixed=sum((u[x][b]*hlookup[past,labels[x],b] for b in (0,1)),Q(0))
            forward=sum((P[x][j]*(hlookup[past,labels[x],labels[j]]-mixed) for j in range(len(P))),Q(0))
            assert forward==0
        backnoise=sum((backwards[x][j]*(sum((u[x][b]*hlookup[labels[j],labels[x],b] for b in (0,1)),Q(0))-hs[x]) for j in range(len(P))),Q(0))
        if rev: assert backnoise==0
        elif backnoise: failures.append(str(backnoise))
    return {'hidden_states':len(P),'reversible':rev,
        'pointwise_D5_minimum_margin':str(margin),
        'backward_martingale_means':list(map(str,back_means)),
        'nonreversible_backward_observation_noise':failures}


def negative_controls():
    n=8; alpha=Q(1,40)
    # A forbidden but stationary mod-three observer on a constant record.
    assert (1+1)%3 != (1-1)%3
    assert q_bound(n,n)<alpha
    # Actual reversible microscopic birth-death chain, WRONG initial law.
    m=8
    P=[[Q(0)]*(m+1) for _ in range(m+1)]
    for i in range(m+1):
        P[i][min(i+1,m)]+=Q(3,4)
        P[i][max(i-1,0)]+=Q(1,4)
    Z=sum(3**i for i in range(m+1)); pi=[Q(3**i,Z) for i in range(m+1)]
    assert all(pi[i]*P[i][j]==pi[j]*P[j][i] for i,j in product(range(m+1),repeat=2))
    wrong_start_all_right=Q(3,4)**n
    assert wrong_start_all_right>alpha>q_bound(n,n)
    labels=[(i//2)%2 for i in range(m+1)]
    assert current_eval(labels,alpha)['reject_reversible']
    # Shared rounding of identical probability 1/4: E[r^2]=1/4 != 1/16.
    assert Q(1,4)!=Q(1,4)**2
    return {'forbidden_stationary_mod3_observer_false_rejection':True,
        'nonstationary_reversible_binary_source_false_rejection_subevent':str(wrong_start_all_right),
        'stationarity_required':True,'independent_predictive_group_rounding_required':True}


def log_and_rate_controls():
    # Check enclosure nesting under a longer series. The analytic remainder
    # formula supplies rigor; these are concrete implementation controls.
    for x in (Q(1,1000),Q(1,2),Q(1),Q(2),Q(3),Q(1234567,19)):
        lo,hi=log_bounds(x,20); lo2,hi2=log_bounds(x,40)
        assert lo<=lo2<=hi2<=hi
    ratios=[]
    for b in (Q(1,2),Q(1,10),Q(1,100)):
        llo,lhi=log_bounds((1+b)/(1-b))
        elo,ehi=b*llo,b*lhi
        plo,phi=log_bounds(1+b); mlo,mhi=log_bounds(1-b)
        Ilo=((1+b)*plo+(1-b)*mlo)/2
        Ihi=((1+b)*phi+(1-b)*mhi)/2
        assert elo>=4*Ihi
        alpha=Q(1,40)
        ratios.append({'b':str(b),'entropy_rate_preview':float(elo),
            'asymptotic_certificate_fraction_lower':float(4*alpha*Ilo/ehi),
            'asymptotic_certificate_fraction_upper':float(4*alpha*Ihi/elo)})
    # Actual coverage calculation under a weakly driven source, not a null.
    coverage=[]
    b=Q(1,100); p=(1+b)/2
    elo,ehi=log_bounds((1+b)/(1-b)); elo*=b; ehi*=b
    for n in (8,20,50,100):
        mass=Q(0)
        for k in range(n+1):
            lo,hi=lower_rate_interval(n,abs(2*k-n))
            if lo>ehi:
                mass+=Q(math.comb(n,k)*p.numerator**k*(p.denominator-p.numerator)**(n-k),p.denominator**n)
            else: assert hi<=elo or lo==hi==0
        assert mass<=Q(1,40)
        coverage.append({'n':n,'exact_overcoverage_failure_probability':str(mass)})
    return {'log_enclosures_nested':True,'rate_scale_controls':ratios,
        'weak_drive_source_exact_coverage_controls':coverage}


def draw_record(P,pi,labels,transitions,rng):
    def draw(probabilities):
        den=math.lcm(*(p.denominator for p in probabilities))
        pick=rng.randrange(den); cumulative=0
        for i,p in enumerate(probabilities):
            cumulative+=p.numerator*(den//p.denominator)
            if pick<cumulative: return i
        raise AssertionError('invalid categorical distribution')
    x=draw(pi); record=[labels[x]]
    for _ in range(transitions):
        x=draw(P[x]); record.append(labels[x])
    return record


def main():
    start=time.perf_counter(); rng=random.Random(20261031)
    old=old_receiver()
    states,labels,P,pi,source=source_controls(old)
    cert=load_certificate(HERE/'symmetric_dual.json')
    raw=load_certificate(HERE.parent/'predictive_flow/generic_triple_certificate.json')
    assert cert['B']==Q(33,296) and cert['R']==Q(151,592) and cert['C']==Q(23,74)
    assert raw['B']==Q(33,148) and raw['R']==Q(10,37) and raw['C']==Q(113,296)
    nullP=[[Q(1,2),Q(1,4),Q(1,4)],[Q(1,4),Q(3,4),Q(0)],[Q(1,4),Q(0),Q(3,4)]]
    nullpi=[Q(1,3)]*3; nulllabels=[0,0,1]
    bridges=[bridge_controls(cert,nullP,nullpi,nulllabels)]
    for trial in range(20):
        n=2+trial%4; weights=[[0]*n for _ in range(n)]
        for i in range(n):
            for j in range(i,n): weights[i][j]=weights[j][i]=rng.randrange(1,20)
        K,p=reversible_kernel(weights)
        bridges.append(bridge_controls(cert,K,p,[rng.randrange(2) for _ in range(n)]))
    nonrev=bridge_controls(cert,P,pi,labels)
    assert nonrev['nonreversible_backward_observation_noise']
    acquisitions=[]
    for name,K,p,lab in [('source',P,pi,labels),('reversible_hidden_memory_null',nullP,nullpi,nulllabels)]:
        record=draw_record(K,p,lab,6000,rng)
        (HERE/(name+'_record.json')).write_text(json.dumps(record)+'\n')
        result={'kind':'synthetic single stationary trajectory',
            'stationary_preparations':1,'transitions_generated':6000,
            'observed_bits':6001,'duals_frozen_before_record':True,
            'current_prefix_88':current_eval(record[:89]),
            'predictive_dual_full_trace':dual_eval(cert,record)}
        # Per-method fixed-horizon guarantees; this is not an uncharged
        # combined decision rule choosing the best p-value on these records.
        acquisitions.append({'name':name,**result})
    output={'scope':__doc__,'exact_certificate_columns_checked':{
        'raw':raw['columns_checked'],'symmetry_averaged':cert['columns_checked']},
        'coefficient_bounds':{'B':str(cert['B']),'R':str(cert['R']),'C':str(cert['C'])},
        'null_current_controls':null_current_controls(rng),
        'source':source,'dormant_copy':dormant_control(P,pi,labels),
        'pointwise_dual_bridge_controls':bridges,
        'nonreversible_backward_identity_negative_control':nonrev,
        'negative_controls':negative_controls(),
        'log_and_rate_controls':log_and_rate_controls(),
        'synthetic_acquisitions':acquisitions,'seconds':time.perf_counter()-start,
        'status':'ALL_EXACT_FINITE_CONTROLS_PASSED'}
    (HERE/'receipt.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({'status':output['status'],'seconds':output['seconds'],
        'certificate_columns':output['exact_certificate_columns_checked'],
        'null_controls':output['null_current_controls'],
        'synthetic_decisions':[{'name':x['name'],
            'current_88_reject':x['current_prefix_88']['reject_reversible'],
            'dual_6000_reject':x['predictive_dual_full_trace']['reject_reversible'],
            'dual_rate_lower':x['predictive_dual_full_trace']['rate_preview']}
            for x in acquisitions]},indent=2))


if __name__=='__main__':
    main()
