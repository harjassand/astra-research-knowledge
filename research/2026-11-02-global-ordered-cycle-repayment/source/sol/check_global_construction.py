#!/usr/bin/env python3
"""Exact checks of actual branch laws, repayment identities and emitted data.

Finite checks are diagnostics and arithmetic certificates at their stated scope;
the universal theorem is the ordinary proof. This is the same author's checking,
not an independent audit.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict
from math import prod
import json
from ordered_cycle_certificate import acquire,raw_cycle,complexes,ceilq

P=Path(__file__).resolve().parent

def ff(a,b):return 0 if a<b else prod(range(a-b+1,a+1))
def rate(x,y,c):return c*prod(ff(a,b) for a,b in zip(x,y))
def next_state(x,e):
    y,z,c=e;assert rate(x,y,c)>0
    return tuple(a-b+d for a,b,d in zip(x,y,z))
def in_section(x):return x[0]==0 or x[1]==x[2]==0
def max_source(x,raw):return max(i for i,(y,z,c) in enumerate(raw) if rate(x,y,c)>0)

def maximal_normalize(x,raw,cap=1000):
    path=[x];indices=[]
    while not in_section(x):
        i=max_source(x,raw);x=next_state(x,raw[i]);indices.append(i);path.append(x)
        assert len(indices)<cap
    return x,indices,path

def deletion_checks(k,raw):
    B=[0,1,1]+list(range(3,k+1));C=[0,0,1]+list(range(3,k+1));A=[0,1]+[2]*(2*k-3)+[k,k]
    rows=[]
    for index,word in [(0,A),(1,B),(2,C)]:
        start=tuple(1 if j==index else 0 for j in range(3));x=start;peak=sum(x)
        for i in word:x=next_state(x,raw[i]);peak=max(peak,sum(x))
        assert x==(0,0,0) and len(word)<=2*k+1 and peak-sum(start)<=6*k-5
        rows.append({'coordinate':index,'word':word,'length':len(word),'count_overshoot':peak-sum(start)})
    return rows

def axis_single_error_identities(k,raw):
    a=20*k*k;C=complexes(k);rows=[]
    for j in range(1,k+1):
        start=tuple(v+w for v,w in zip((a,0,0),C[j]));x=next_state(start,raw[j-1])
        end,word,path=maximal_normalize(x,raw)
        expected=(a-1,0,0) if j==k else (a,0,0)
        assert end==expected and j+1+len(word)<=3*k+3
        rows.append({'first_error_phase':j,'source':j-1,'actual_repayment_word':word,
                     'endpoint_delta_A':end[0]-a,'subsequent_jumps':len(word)})
    return rows

def normalizer_mgf(raw,x,t,k):
    active={x:F(1)};out=[]
    for step in range(1,k+1):
        nxt=defaultdict(F)
        for state,p in active.items():
            rates=[rate(state,y,c) for y,z,c in raw];q=sum(rates)
            for i,(e,r) in enumerate(zip(raw,rates)):
                if not r:continue
                dst=next_state(state,e);pp=p*r/q
                if i==k or step==k:out.append((pp,dst))
                else:nxt[dst]+=pp
        active=nxt
    assert sum(p for p,dst in out)==1 and not active
    return sum(p*t**(sum(dst)-sum(x)) for p,dst in out),len(out)

def profile(b,params):
    B=int(params['section_B_cutoff']);G=F(params['profile_G']);r=F(params['profile_ratio_kappa1_over_kappa0'])
    return F(0) if b>=B else G*((B-b)+r*F((B-b)*(B+b+1),2))

def plane_prefix(raw,b,c,kind,t,params):
    k=len(raw)-1;N=b+c;front={(0,b,c):F(1)};out=[]
    for phase in range(k+1):
        nxt=defaultdict(F)
        for x,p in front.items():
            assert x[0]==phase
            allowed=({0} if phase==0 else {0,1} if phase==1 else {phase}) if kind=='low_B' else (
                     {0} if phase==0 else {1} if phase==1 else {1,2} if phase==2 else {phase})
            rr=[rate(x,y,cc) for y,z,cc in raw];q=sum(rr)
            for i,(e,r) in enumerate(zip(raw,rr)):
                if not r:continue
                dst=next_state(x,e);pp=p*r/q
                if i not in allowed:
                    assert not in_section(dst)
                    value=t**(sum(dst)-N) # Earned global V_off/W upper bound.
                    out.append((pp,value,'abort'))
                elif phase==k:
                    assert dst[0]==0
                    value=t**(sum(dst)-N)*(1+profile(dst[1],params)/F(sum(dst)+1))
                    out.append((pp,value,'return'))
                else:nxt[dst]+=pp
        front=nxt
    assert not front and sum(p for p,v,kind in out)==1
    start=1+profile(b,params)/F(N+1)
    return sum(p*v for p,v,kind in out)-start,len(out)

def axis_laurent_first_order(raw,t):
    """Exact constant and 1/a coefficient, retaining the actual raw-source policy."""
    k=len(raw)-1;J=3*k+3;C=complexes(k)
    # State is the bounded offset (A-a,B,C), mismatch count. Prob=(p0,p1).
    active={((0,0,0),0):(F(1),F(0))};out0=F(0);out1=F(0);leaves=0
    for step in range(J+1):
        nxt={}
        for (offset,errors),(p0,p1) in active.items():
            if step and offset[1]==offset[2]==0:
                val=t**sum(offset);out0+=p0*val;out1+=p1*val;leaves+=1;continue
            if step==J:
                val=t**sum(offset);out0+=p0*val;out1+=p1*val;leaves+=1;continue
            enabled=[i for i,y in enumerate(C) if offset[1]>=y[1] and offset[2]>=y[2]]
            j=max(enabled)
            lead={i:raw[i][2]*ff(offset[1],C[i][1])*ff(offset[2],C[i][2]) for i in enabled}
            beta=lead.get(j-1,F(0))/lead[j] if j else F(0)
            candidates=[(j,F(1),-beta)]
            if j:candidates.append((j-1,F(0),beta))
            for i,r0,r1 in candidates:
                pp0=p0*r0;pp1=p1*r0+p0*r1
                if not pp0 and not pp1:continue
                y,z,kap=raw[i];dst=tuple(a-b+c for a,b,c in zip(offset,y,z))
                if i<j and errors:
                    val=t**sum(dst);out0+=pp0*val;out1+=pp1*val;leaves+=1
                else:
                    key=(dst,errors+(i<j))
                    old=nxt.get(key,(F(0),F(0)));nxt[key]=(old[0]+pp0,old[1]+pp1)
        active=nxt
    assert not active and out0==1
    expected=raw[k-1][2]/raw[k][2]*(1/t-1)
    assert out1==expected and out1<0
    return {'constant_MGF':str(out0),'one_over_A_drift_coefficient':str(out1),
            'predicted_coefficient':str(expected),'nonzero_formal_terminal_branches':leaves,
            'scope':'Exact formal leading coefficient for the whole acquired finite axis rule; O(A^-2) remainder is paid by the analytic proof.'}

if __name__=='__main__':
    rows=[]
    for k in [3,4,5,8]:
        rates=[F(j+1,2*j+1) for j in range(k+1)];raw=raw_cycle(k,rates)
        rows.append({'k':k,'deletion_words':deletion_checks(k,raw),
                     'axis_single_error':axis_single_error_identities(k,raw),
                     'axis_formal_envelope':axis_laurent_first_order(raw,F(11,10))})
    raw=raw_cycle(4,[1,1,1,1,2]);cert=acquire(raw);p=cert['parameters_exact'];t=F(p['t']);rho=F(p['rho'])
    a,b,c=map(lambda key:int(p[key]),['A_hi','B_hi','C_hi']);tests=[(a,0,1),(a,1,0),(1,b,0),(2,b,1),(1,0,c),(1,1,c),(2,1,c),(a,1,1)]
    checks=[]
    for x in tests:
        mgf,branches=normalizer_mgf(raw,x,t,4);assert mgf<=rho
        checks.append({'state':x,'actual_expected_W_ratio_exact':str(mgf),'rho_exact':str(rho),'terminal_branches':branches})
    B=int(p['section_B_cutoff']);L=int(p['head_radius_M']);plane=[]
    for bb,cc,kind in [(0,L+B,'low_B'),(B-1,L+B,'low_B'),(L+B,0,'low_C'),(L+B,B-1,'low_C')]:
        drift,branches=plane_prefix(raw,bb,cc,kind,t,p)
        bound=-F(1,cc) if kind=='low_B' else -(1-1/t)*F(p['negative_low_C_d'])/2
        assert drift<=bound
        plane.append({'chart':kind,'B':str(bb),'C':str(cc),'upper_drift_exact':str(drift),
                      'theorem_bound_exact':str(bound),'branches':branches})
    for bb in [0,1,B//2,B-1]:
        assert profile(bb,p)-profile(bb+1,p)==F(p['profile_G'])*(1+F(p['profile_ratio_kappa1_over_kappa0'])*(bb+1))
    out={'scope':'Same-principal exact finite arithmetic and actual-branch checks, not an independent audit or a substitute for the all-state proof.',
         'structural_identity_checks':rows,'global_normalizer_checks':checks,'plane_feedback_checks':plane}
    (P/'results/construction_checks.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'structural_k_values':[r['k'] for r in rows],
                      'exact_global_normalizer_instances':len(checks),'exact_plane_feedback_instances':len(plane),
                      'all_axis_leading_coefficients':'matched exact negative formula','all_checks':'PASS'},indent=2))
