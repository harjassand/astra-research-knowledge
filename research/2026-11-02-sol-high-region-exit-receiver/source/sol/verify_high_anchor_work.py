#!/usr/bin/env python3
"""Exact local workload certificates; finite checks do not prove recurrence."""
from fractions import Fraction as F
from math import ceil
from itertools import product
from pathlib import Path
import json,random

P=Path(__file__).resolve().parent
Y=((0,0,0),(1,1,0),(2,1,1),(3,2,2))

def ff(x,s):
    ans=1
    for z,n in zip(x,s):
        if z<n:return 0
        for j in range(n):ans*=z-j
    return ans

def constants(rates):
    B=sum(v[0] for v in rates);b=min(v[0] for v in rates)
    f=min(min(v[1],2*v[2],8*v[3]) for v in rates)
    D=max(max(v[0]/v[1],2*(v[0]+v[1])/v[2],3*(v[0]+v[1]+v[2])/v[3]) for v in rates)
    a=ceil(4+8*B/b);L=ceil(max(3,2*a*D,12*B/f))
    return {'B0':B,'b0':b,'f0':f,'D':D,'a':a,'L':L}

def parts(x):
    plus=minus=O=J=0
    for q in range(0,len(x),3):
        A,B,C=x[q:q+3];r=B-C;t=min(B,C)
        plus+=max(r,0);minus+=max(-r,0);O+=t%2;J+=t//2
    return 3*plus+2*O+J,minus

def psi(x,a):
    V,Q=parts(x);return V+a*Q

def proper_constants(rates,c,core_edges,weights):
    H=max(weights);h=min(weights);tot=[F(0)]*len(rates)
    for i,j,kappa in core_edges:tot[i]+=kappa/rates[i][3]
    core=54*H*(2*H/h+1)*max(tot,default=F(0));block=3*H*c['D']
    return {'weights':weights,'c0':8*(c['a']+1)**2,'C_core':core,'C_block':block,
            'C':8*(core+block+1/c['B0'])}

def proper(x,c,pc):
    Q=F(0)
    for i,eta in enumerate(pc['weights']):
        A,B,C=x[3*i:3*i+3];t=min(B,C)
        h=abs(B-C)+F(3,2)*t+F(t%2,2)
        Q+=eta*max(A-h,0)**2
    return Q+pc['C']*(psi(x,c['a'])+pc['c0'])**2

def classify(A,B,C):
    t=min(B,C)
    if t>=2:return 3,'fast'
    if t==1:return 2,'fast'
    if B>C:return 1,'fast'
    if B<C:return 0,'slow'
    return 0,'empty'

def check(x,rates,c,core_edges,pc):
    assert min(x)>=0 and all(x[j]>=c['L'] for j in range(0,len(x),3))
    a,L=c['a'],c['L'];v=psi(x,a)
    hazards={k:F(0) for k in ('fast','slow','empty','other')};drift=F(0)
    U=proper(x,c,pc);proper_drift=F(0)
    for port,alpha in enumerate(rates):
        q=3*port;A,B,C=x[q:q+3];normal,kind=classify(A,B,C)
        for j in range(4):
            rate=alpha[j]*ff((A,B,C),Y[j])
            if not rate:continue
            z=list(x)
            for t in range(3):z[q+t]+=Y[(j+1)%4][t]-Y[j][t]
            d=psi(z,a)-v
            assert abs(d)<=a+1
            if j==normal:
                assert d=={'fast':-1,'slow':2-a,'empty':3}[kind]
                hazards[kind]+=rate
            else:
                assert d<=a
                hazards['other']+=rate
            drift+=rate*d
            proper_drift+=rate*(proper(z,c,pc)-U)
    for i,j,kappa in core_edges:
        s=[0]*len(x);s[3*i]=s[3*j]=1;s[3*i+1]=s[3*i+2]=2
        rate=kappa*ff(x,s)
        if rate:
            z=list(x);z[3*i+1]-=2;z[3*i+2]-=2;z[3*j+1]+=2;z[3*j+2]+=2
            assert min(z)>=0 and psi(z,a)==v
            proper_drift+=rate*(proper(z,c,pc)-U)
    assert hazards['other']<=c['D']/L*hazards['fast']
    q=sum(hazards.values())
    assert q>=c['B0']
    if v:
        assert drift<=-q/8,(x,drift,q,hazards)
        assert proper_drift<=-1,(x,proper_drift)
    return {'state':list(map(str,x)),'psi':v,'q_noncore':str(q),'actual_drift':str(drift),
            'drift_plus_q_over_8':str(drift+q/8),'proper_receiver_drift':str(proper_drift),
            'hazards':{k:str(v) for k,v in hazards.items()}}

def pump():
    x=(1,2,1000000,1,2,2);cur=x;states=[x]
    for label in ('I1','I2','forward','I2','I3','backward'):
        z=list(cur)
        if label.startswith('I'):
            j=int(label[1]);assert ff(cur[:3],Y[j])>0
            assert max(k for k in range(4) if ff(cur[:3],Y[k])>0)==j
            for t in range(3):z[t]+=Y[(j+1)%4][t]-Y[j][t]
        else:
            i,j=(0,1) if label=='forward' else (1,0)
            assert cur[3*i]>=1 and cur[3*j]>=1 and min(cur[3*i+1:3*i+3])>=2
            for t in (1,2):z[3*i+t]-=2;z[3*j+t]+=2
        cur=tuple(z);states.append(cur)
    assert cur==tuple(v+int(j==2) for j,v in enumerate(x))
    return {'channels':['I1','I2','core_forward','I2','I3','core_backward'],'states':states,
            'scope':'Actual positive-rate pumping word for maximal-source policy; not a transience claim.'}

def main():
    rows=[];count=0;random.seed(61102)
    cases=[((1,1,1,1),(1,1,1,1)),((1,2,3,5),(2,1,4,3)),
           ((F(1,7),23,F(3,5),11),(13,F(2,3),17,F(1,11))),
           ((1,1,1,1),)*3]
    for case_index,raw in enumerate(cases):
        rates=tuple(tuple(map(F,v)) for v in raw);c=constants(rates);m=len(rates)
        core=([(0,1,F(2)),(1,0,F(1))] if case_index==0 else
              [(i,j,F(10)**(13*i-11*j)) for i in range(m) for j in range(m) if i!=j])
        weights=tuple(F(2+i,2) for i in range(m));pc=proper_constants(rates,c,core,weights)
        local=0;sample=[]
        if m==2:
            for hidden in product(range(6),repeat=4):
                for anchors in ((c['L'],c['L']),(c['L']+2,10**30)):
                    x=(anchors[0],hidden[0],hidden[1],anchors[1],hidden[2],hidden[3])
                    r=check(x,rates,c,core,pc);local+=1
                    if len(sample)<2 and r['psi']:sample.append(r)
        else:
            for _ in range(2500):
                x=tuple(z for i in range(m) for z in (c['L']+random.randrange(3),random.randrange(10),random.randrange(10)))
                check(x,rates,c,core,pc);local+=1
        for _ in range(1000):
            x=tuple(z for i in range(m) for z in (c['L']+random.choice((0,1,10**25)),
                    random.choice((0,1,2,3,10**10,10**50)),random.choice((0,1,2,3,10**10,10**50))))
            r=check(x,rates,c,core,pc);local+=1
            if len(sample)<5 and r['psi']:sample.append(r)
        count+=local;rows.append({'rates':[[str(v) for v in a] for a in rates],
            'constants':{k:str(v) for k,v in c.items()},
            'proper_receiver_constants':{k:str(v) for k,v in pc.items()},
            'checked_actual_states':local,'examples':sample})
    out={'exact_actual_generator_checks':count,'cases':rows,'low_anchor_policy_failure':pump(),
         'scope':'Exact rational local identity checks and actual pumping-word replay; the quantified proof is HIGH_ANCHOR_ACTUAL_NORMALIZATION.md. No full recurrence or independent audit.'}
    (P/'results/high_anchor_work_checks.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'exact_actual_generator_checks':count,'constant_cases':[{k:v for k,v in r.items() if k!='examples'} for r in rows],
                      'actual_low_anchor_pump_replayed':True},indent=2))

if __name__=='__main__':main()
