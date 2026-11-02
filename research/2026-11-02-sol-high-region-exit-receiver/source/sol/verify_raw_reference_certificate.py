#!/usr/bin/env python3
"""Replay finite raw reference certificates without calling the constructor.

Exact arithmetic checks only; the Kac/transport theorem is a separate proof.
This is same-principal verification, not an independent scientific audit.
"""
from fractions import Fraction as F
from collections import defaultdict,Counter
from pathlib import Path
from math import prod,factorial,comb
import copy,json

P=Path(__file__).resolve().parent
def ff(x,s):
    out=1
    for a,b in zip(x,s):
        if a<b:return 0
        out*=prod(range(a-b+1,a+1))
    return out
def mon(c,s):return prod(F(a)**b for a,b in zip(c,s))

def verify(v):
    raw=[(tuple(r['source']),tuple(r['product']),F(r['kappa_exact'])) for r in v['raw_reactions']]
    x=tuple(map(int,v['input']));assert min(x)>=0 and all(k>0 for s,u,k in raw)
    if v['status'].startswith('PHYSICAL_SINGLETON'):
        assert not any(s!=u and ff(x,s)>0 for s,u,k in raw);return
    c=tuple(map(int,v['reference_mean']));normal=list(map(F,v['normal_coefficients_exact']));rej=list(map(F,v['rejected_coefficients_exact']))
    assert all(0<b<=k and r==k-b for (s,u,k),b,r in zip(raw,normal,rej))
    count=Counter()
    for cycle in v['cycle_cover']:
        assert cycle
        start=raw[cycle[0]][0];cur=start
        for e in cycle:
            assert raw[e][0]==cur;cur=raw[e][1];count[e]+=1
        assert cur==start
    assert all(count[e]>=1 and count[e]==v['edge_cycle_multiplicities'][e] for e in range(len(raw)))
    epsilon=F(v['circulation_scale_exact']);assert epsilon==min(k*mon(c,s)/count[e] for e,(s,u,k) in enumerate(raw))
    balance=defaultdict(F)
    for e,(s,u,k) in enumerate(raw):
        f=normal[e]*mon(c,s);assert f==epsilon*count[e]
        balance[s]-=f;balance[u]+=f
    assert all(a==0 for a in balance.values())
    y=tuple(v['defect_complex']);poly=defaultdict(F)
    for s,u,k in raw:
        if u==y:poly[s]+=k
        if s==y:poly[y]-=k
    poly={s:a for s,a in poly.items() if a};h=max(map(sum,poly));assert h==v['defect_degree']
    direction=v['defect_direction'];D=v['raw_dimensions']['degree']
    assert all(1<=a<=D+1 for a in direction)
    lead=sum((a*mon(direction,s) for s,a in poly.items() if sum(s)==h),F(0))
    assert lead==F(v['leading_coefficient_exact'])!=0
    values=[]
    for t in range(h+1):
        candidate=tuple(a+1+t*b for a,b in zip(x,direction))
        values.append((candidate,sum((a*mon(candidate,s) for s,a in poly.items()),F(0))))
    assert sum(((-1)**(h-t)*comb(h,t)*a for t,(_,a) in enumerate(values)),F(0))==factorial(h)*lead
    target=min(F(factorial(h))*abs(lead)/2**h,F(1));assert target==F(v['defect_target_exact'])>0
    assert (c,F(v['actual_complex_defect_exact'])) in values
    assert abs(F(v['actual_complex_defect_exact']))>=target
    start=tuple(v['chosen_active_complex']);assert x>=tuple(0 for _ in x) and ff(x,start)>0
    state=x;prob=F(1);seen={state}
    steps=v['actual_full_race_word_certificate'];assert len(steps)==len(v['accepted_raw_word'])+1
    for j,e in enumerate(v['accepted_raw_word']):
        step=steps[j];assert step['accepted_channel']==e and tuple(map(int,step['physical_input']))==state
        s,u,k=raw[e];assert ff(state,s)>0
        q=sum((kk*ff(state,ss) for ss,uu,kk in raw),F(0));p=normal[e]*ff(state,s)/q
        assert p==F(step['conditional_probability_exact'])>0;prob*=p
        state=tuple(a-b+d for a,b,d in zip(state,s,u));assert state not in seen;seen.add(state)
    e=v['specified_final_rejected_channel'];last=steps[-1]
    assert last['rejected_channel']==e and tuple(map(int,last['physical_input']))==state
    s,u,k=raw[e];assert ff(state,s)>0
    q=sum((kk*ff(state,ss) for ss,uu,kk in raw),F(0));p=rej[e]*ff(state,s)/q
    assert p==F(last['conditional_probability_exact'])>0;prob*=p
    assert prob==F(v['success_probability_lower_bound_exact'])
    assert sum((b*ff(x,s) for (s,u,k),b in zip(raw,normal)),F(0))==F(v['reference_rate_at_input_exact'])>0
    assert sum((k*mon(c,s) for s,u,k in raw),F(0))==F(v['raw_poisson_activity_mean_exact'])

def main():
    rows=json.loads((P/'results/raw_reference_certificates.json').read_text())
    for v in rows:verify(v)
    base=next(v for v in rows if v['status'].startswith('RAW_REFERENCE'))
    mutations=[]
    b=copy.deepcopy(base);b['normal_coefficients_exact'][0]=str(F(b['raw_reactions'][0]['kappa_exact'])+1);mutations.append(b)
    b=copy.deepcopy(base);b['cycle_cover'][0]=b['cycle_cover'][0][:-1];mutations.append(b)
    b=copy.deepcopy(base);b['success_probability_lower_bound_exact']='0';mutations.append(b)
    b=copy.deepcopy(base);b['reference_mean'][0]=str(int(b['reference_mean'][0])+1);mutations.append(b)
    rejected=0
    for b in mutations:
        try:verify(b)
        except (AssertionError,KeyError,ValueError):rejected+=1
        else:raise AssertionError('tamper accepted')
    out={'exact_raw_certificates_replayed':len(rows),'tampered_certificates_rejected':rejected,
         'scope':'Same-principal finite data verification only, not an audit or recurrence proof.'}
    (P/'results/raw_reference_verification.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))

if __name__=='__main__':main()
