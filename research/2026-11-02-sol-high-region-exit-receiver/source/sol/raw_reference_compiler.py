#!/usr/bin/env python3
"""Acquire a raw complex-balanced subgenerator and a genuine rejection word.

The output is a finite certificate and explicit occupation-envelope bound,
not the original chain's stationary law, a full exit-kernel solve, or recurrence.
"""
from fractions import Fraction as F
from collections import deque,Counter,defaultdict
from itertools import product
from pathlib import Path
from math import factorial,comb
import json,sys
import mpmath as mp

P=Path(__file__).resolve().parent
sys.path.insert(0,str(P.parent/'astra-sol-subgeometric-synthesis-20261102'))
from conservative_fiber_kernel import raw_network,falling

def monomial(c,s):
    out=F(1)
    for a,b in zip(c,s):out*=F(a)**b
    return out

def path(raw,start,target):
    if start==target:return []
    q=deque([start]);back={start:None}
    while q:
        v=q.popleft()
        for e,(s,u,k) in enumerate(raw):
            if s!=v or u in back:continue
            back[u]=(v,e)
            if u==target:
                out=[];cur=u
                while back[cur] is not None:
                    pre,j=back[cur];out.append(j);cur=pre
                return out[::-1]
            q.append(u)
    raise ValueError(('NOT_WEAKLY_REVERSIBLE_OR_UNREACHABLE',start,target))

def poly_value(poly,c):return sum((a*monomial(c,s) for s,a in poly.items()),F(0))

def touchard(n,mean):
    S=[[0]*(n+1) for _ in range(n+1)];S[0][0]=1
    for j in range(1,n+1):
        for k in range(1,j+1):S[j][k]=S[j-1][k-1]+k*S[j-1][k]
    return sum((F(S[n][k])*F(mean)**k for k in range(n+1)),F(0))

def shifted_poisson_moment(power,mean,shift):
    return sum((F(comb(power,j))*F(shift)**(power-j)*touchard(j,mean)
                for j in range(power+1)),F(0))

def acquire(raw,x):
    raw=[(tuple(s),tuple(u),F(k)) for s,u,k in raw];x=tuple(x);d=len(x)
    assert min(x)>=0 and all(k>0 and len(s)==d and len(u)==d for s,u,k in raw)
    active=next((e for e,(s,u,k) in enumerate(raw) if s!=u and falling(x,s)>0),None)
    raw_payload=[{'source':s,'product':u,'kappa_exact':str(k)} for s,u,k in raw]
    if active is None:return {'status':'PHYSICAL_SINGLETON_NO_NONTRIVIAL_ENABLED_REACTION','input':list(map(str,x)),'raw_reactions':raw_payload}
    complexes=sorted({v for s,u,k in raw for v in (s,u)});D=max(map(sum,complexes));M=len(complexes)
    cycles=[];multiplicity=Counter()
    for e,(s,u,k) in enumerate(raw):
        cycle=[e]+path(raw,u,s);cycles.append(cycle);multiplicity.update(cycle)
    assert all(multiplicity[e]>0 for e in range(len(raw)))
    start=raw[active][0]
    linkage={start};todo=[start]
    while todo:
        v=todo.pop()
        for s,u,k in raw:
            if s==v and u not in linkage:linkage.add(u);todo.append(u)
    chosen=None
    for y in sorted(linkage):
        if not any(s==y and u!=y for s,u,k in raw):continue
        poly=defaultdict(F)
        for s,u,k in raw:
            if u==y:poly[s]+=k
            if s==y:poly[y]-=k
        poly={s:a for s,a in poly.items() if a}
        if poly:chosen=(y,poly);break
    assert chosen is not None
    y,poly=chosen;h=max(map(sum,poly));top={s:a for s,a in poly.items() if sum(s)==h}
    direction=None
    for candidate in product(range(1,D+2),repeat=d):
        value=poly_value(top,candidate)
        if value:direction=candidate;leading=value;break
    assert direction is not None
    delta=F(factorial(h))*abs(leading)/2**h;target=min(delta,F(1))
    candidates=[]
    for t in range(h+1):
        c=tuple(a+1+t*v for a,v in zip(x,direction));value=poly_value(poly,c)
        candidates.append((c,value))
    difference=sum((F((-1)**(h-t)*comb(h,t))*v for t,(_,v) in enumerate(candidates)),F(0))
    assert difference==factorial(h)*leading
    c,defect=next((c,v) for c,v in candidates if abs(v)>=target)
    flux=[k*monomial(c,s) for s,u,k in raw]
    epsilon=min(flux[e]/multiplicity[e] for e in range(len(raw)))
    normal=[epsilon*multiplicity[e]/monomial(c,s) for e,(s,u,k) in enumerate(raw)]
    rejected=[k-b for (_,_,k),b in zip(raw,normal)]
    assert min(normal)>0 and min(rejected)>=0
    balanced=defaultdict(F)
    for e,(s,u,k) in enumerate(raw):
        z=normal[e]*monomial(c,s);balanced[s]-=z;balanced[u]+=z
    assert all(v==0 for v in balanced.values())
    eligible=[e for e,(s,u,k) in enumerate(raw) if s in linkage]
    bad=max(eligible,key=lambda e:rejected[e]*monomial(c,raw[e][0]))
    assert rejected[bad]>0
    residual_total=sum((rejected[e]*monomial(c,raw[e][0]) for e in eligible),F(0))
    assert residual_total>=abs(defect)
    assert rejected[bad]*monomial(c,raw[bad][0])>=abs(defect)/len(eligible)
    accepted_word=path(raw,start,raw[bad][0]);state=x;prob=F(1);witness=[]
    seen={x}
    for e in accepted_word:
        s,u,k=raw[e];factor=falling(state,s);assert factor>0
        total=sum((kk*falling(state,ss) for ss,uu,kk in raw),F(0))
        p=normal[e]*factor/total;assert p>0;prob*=p
        witness.append({'physical_input':list(map(str,state)),'accepted_channel':e,'conditional_probability_exact':str(p)})
        state=tuple(a-b+cc for a,b,cc in zip(state,s,u));assert state not in seen
        seen.add(state)
    s,u,k=raw[bad];factor=falling(state,s);assert factor>0
    total=sum((kk*falling(state,ss) for ss,uu,kk in raw),F(0))
    p=rejected[bad]*factor/total;assert p>0;prob*=p
    witness.append({'physical_input':list(map(str,state)),'rejected_channel':bad,'conditional_probability_exact':str(p)})
    qnormal=sum((b*falling(x,s) for (s,u,k),b in zip(raw,normal)),F(0));assert qnormal>0
    # Exact local master balance checks for the acquired reference.
    check_states=[x,tuple(a+2 for a in x)]+[tuple(a+b for a,b in zip(x,v)) for v in complexes[:4]]
    for z in check_states:
        incoming=sum((b*monomial(c,tuple(a-bb for a,bb in zip(s,u)))*falling(z,u)
                       for (s,u,k),b in zip(raw,normal)),F(0))
        outgoing=sum((b*falling(z,s) for (s,u,k),b in zip(raw,normal)),F(0))
        assert incoming==outgoing
    mp.mp.dps=max(100,max(len(str(v)) for v in x)+100)
    def ml(v):return mp.log(mp.mpf(v.numerator))-mp.log(mp.mpf(v.denominator))
    logpole=-sum(map(mp.mpf,c))+sum(mp.mpf(a)*mp.log(b)-mp.loggamma(a+1) for a,b in zip(x,c))
    logL=-logpole-ml(qnormal)-ml(prob)
    rate_moment=sum(flux,F(0));mean=sum(c);moments=[]
    for power in (0,1,2):
        expectation=shifted_poisson_moment(power,mean,1)
        expectation+=sum((k*monomial(c,s)*shifted_poisson_moment(power,mean,1+sum(s))
                           for s,u,k in raw),F(0))
        moments.append({'power':power,'reference_reward_mean_exact':str(expectation),
                        'log_proved_actual_occupation_upper_bound':mp.nstr(logL+ml(expectation),40)})
    return {'status':'RAW_REFERENCE_AND_ACTUAL_REJECTION_BOUND_ACQUIRED','input':list(map(str,x)),
            'raw_reactions':raw_payload,
            'raw_dimensions':{'species':d,'complexes':M,'reactions':len(raw),'degree':D},
            'cycle_cover':cycles,'edge_cycle_multiplicities':[multiplicity[e] for e in range(len(raw))],
            'chosen_active_complex':start,'defect_complex':y,'defect_direction':direction,
            'defect_degree':h,'leading_coefficient_exact':str(leading),
            'defect_target_exact':str(target),'actual_complex_defect_exact':str(defect),
            'reference_mean':list(map(str,c)),'circulation_scale_exact':str(epsilon),
            'normal_coefficients_exact':list(map(str,normal)),
            'rejected_coefficients_exact':list(map(str,rejected)),
            'accepted_raw_word':accepted_word,'specified_final_rejected_channel':bad,
            'actual_full_race_word_certificate':witness,'success_probability_lower_bound_exact':str(prob),
            'reference_rate_at_input_exact':str(qnormal),
            'log_product_poisson_mass_at_actual_input':mp.nstr(logpole,40),
            'log_Kac_killed_occupation_prefactor':mp.nstr(logL,40),
            'raw_poisson_activity_mean_exact':str(rate_moment),'occupation_rewards':moments,
            'sufficient_global_polynomial_exponent':(d+1)//2+2*D*(M+1),
            'master_balance_checks':len(check_states),
            'scope':'Finite exact raw certificate and explicit actual killed-reward/envelope bounds. No full original kernel, recurrence, numerical advantage or practical efficiency claimed.'}

def additional_network():
    C=((0,0,0),(2,1,0),(1,0,3),(0,3,2),(2,2,2))
    return [(C[j],C[(j+1)%len(C)],F(2 if j==3 else 1)) for j in range(len(C))]

if __name__=='__main__':
    (P/'results').mkdir(exist_ok=True);rows=[]
    cases=[('six_species',raw_network(),x) for x in
        ((0,0,0,0,0,0),(1000,0,0,1000,0,0),(3,1,1002,0,0,0),
         (0,0,1000,0,1000,0),(10**100,0,0,10**25,0,0))]
    cases.extend((('other_weakly_reversible',additional_network(),(100,0,0)),
                  ('conservative_pair',[((1,0),(0,1),F(2)),((0,1),(1,0),F(1))],(1000,0)),
                  ('absorbing',[((1,),(2,),F(1)),((2,),(1,),F(1))],(0,))))
    for label,raw,x in cases:
        row=acquire(raw,x);row['case']=label;rows.append(row)
        print(json.dumps({'case':label,'input':row['input'],'status':row['status'],
                          'accepted_word':row.get('accepted_raw_word'),
                          'reference_mean':row.get('reference_mean'),
                          'log_L':row.get('log_Kac_killed_occupation_prefactor')}),flush=True)
        (P/'results/raw_reference_certificates.json').write_text(json.dumps(rows,indent=2)+'\n')
