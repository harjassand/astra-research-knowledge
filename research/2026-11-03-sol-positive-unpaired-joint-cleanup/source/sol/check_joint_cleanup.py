#!/usr/bin/env python3
"""Discriminating checks of the joint cleanup, not an all-state proof.

1. Adversarial noncore reachability, including EVERY pure-core terminal
   landing in a finite family, checks the claimed finite work bound.
2. Actual finite birth/death service solves retain the real clock and
   competing growth hazards, testing the uniform population scaling.
3. A raw stranded-inventory word refutes a tempting shorter decomposition.
"""
from collections import deque
from fractions import Fraction as F
from pathlib import Path
import json

P=Path(__file__).resolve().parent

def service(a,d,c,f):
    if a and d:return max(a,d)>=3 and c//2+f//2>=1
    return (a>=3 and c>=2) or (d>=3 and f>=2)

def allocations(a,d,c,f):
    if not(a and d):return [(c,f)]
    oi,oj=c%2,f%2;J=c//2+f//2
    return [(2*j+oi,2*(J-j)+oj) for j in range(J+1)]

def cleanup_count_check(root):
    H=max(root[:2]);bound=100*(H+1)
    todo=deque([root]);seen={root};max_g=max_t=max_nc=0;exits=0
    g0=F(root[0]+root[1])-F(3,2)*(root[2]+root[3])
    while todo:
        a,d,c,f=todo.popleft()
        g=F(a+d)-F(3,2)*(c+f)
        ng=2*(g0-g)
        assert ng.denominator==1 and ng>=0
        ng=int(ng)
        nt=F(root[0]+root[1]+ng-a-d,3)
        assert nt.denominator==1 and nt>=0
        nt=int(nt);max_g=max(max_g,ng);max_t=max(max_t,nt);max_nc=max(max_nc,ng+nt)
        assert max(ng+nt,a,d)<=bound,(root,(a,d,c,f),ng,nt,bound)
        if a==d==0:exits+=1;continue
        out=[]
        if service(a,d,c,f):
            for cc,ff in allocations(a,d,c,f):
                if a>=3 and cc>=2:out.append((a-3,d,cc-2,ff))
                if d>=3 and ff>=2:out.append((a,d-3,cc,ff-2))
            assert out,(root,(a,d,c,f))
        else:
            for cc,ff in allocations(a,d,c,f):
                if a:
                    out.append((a+1,d,cc+1,ff)) # source1 always enabled for hot B
                    if a>=2 and cc:out.append((a+1,d,cc+1,ff)) # source2 same minor-state output
                if d:
                    out.append((a,d+1,cc,ff+1))
                    if d>=2 and ff:out.append((a,d+1,cc,ff+1))
        for nxt in out:
            if nxt not in seen:seen.add(nxt);todo.append(nxt)
    return {'root':root,'states':len(seen),'exits':exits,'max_growths':max_g,
            'max_terminals':max_t,'max_noncore':max_nc,'proved_bound':bound}

def tridiagonal(lower,diag,upper,rhs):
    n=len(diag);dd=list(diag);rr=list(rhs)
    for j in range(1,n):
        p=lower[j]/dd[j-1];dd[j]-=p*upper[j-1];rr[j]-=p*rr[j-1]
    ans=[0.]*n;ans[-1]=rr[-1]/dd[-1]
    for j in range(n-2,-1,-1):ans[j]=(rr[j]-upper[j]*ans[j+1])/dd[j]
    return ans

def fall2(v):return v*(v-1)
def fall3(v):return v*(v-1)*(v-2) if v>=3 else 0

def service_probe(n,J,a,d,r1,r2,oi=0,oj=0):
    # Nonbalanced generic fixture, also distinct ordered-block rates.
    alpha=(2.,5.,3.,7.);beta=(1.,2.,3.,4.);kf,kb=2.,1.
    size=J+1;lower=[0.]*size;diag=[0.]*size;upper=[0.]*size;grow=[0.]*size
    for j in range(size):
        c=2*j+oi;f=2*(J-j)+oj;b=r1+c;e=r2+f
        u1=fall2(b)*fall2(c);u2=fall2(e)*fall2(f)
        left=kf*a*d*u1;right=kb*a*d*u2
        kill=alpha[3]*fall3(a)*u1+beta[3]*fall3(d)*u2
        lower[j]=-left;upper[j]=-right;diag[j]=left+right+kill
        grow[j]=(alpha[0]+alpha[1]*a*b+alpha[2]*fall2(a)*b*c
                 +beta[0]+beta[1]*d*e+beta[2]*fall2(d)*e*f)
    time=tridiagonal(lower,diag,upper,[1.]*size)
    occupation_growth=tridiagonal(lower,diag,upper,grow)
    actual_interrupt=tridiagonal(lower,[diag[j]+grow[j] for j in range(size)],upper,grow)
    assert min(time)>0 and min(occupation_growth)>0
    assert all(-1e-10<=p<=1+1e-10 for p in actual_interrupt)
    assert all(p<=v+1e-8 for p,v in zip(actual_interrupt,occupation_growth))
    return {'n':n,'J':J,'anchors':[a,d],'r':[r1,r2],
            'max_physical_time':max(time),'scaled_clock':max(time)*(n+J)**2*J,
            'max_actual_growth_interrupt':max(actual_interrupt),
            'scaled_interrupt':n*max(actual_interrupt),
            'max_growth_compensator':max(occupation_growth)}

Y=((0,0,0),(1,1,0),(2,1,1),(3,2,2))
def raw_word(n=20):
    state=[0,n,1,0,n,0]
    word=('I0','I1','II0','II1','II2','COREf','II3','I1','I2','I3','I1','I2','I3')
    rows=[];counts=[0]*4
    for label in word:
        before=tuple(state)
        a,b,c,d,e,f=state
        srv=service(a,d,c,f)
        if label=='COREf':
            assert a*d and b>=2 and c>=2
            state[1]-=2;state[2]-=2;state[4]+=2;state[5]+=2
        else:
            port=1 if label.startswith('II') else 0;s=int(label[-1]);o=3*port
            assert all(state[o+k]>=Y[s][k] for k in range(3))
            if srv:assert s==3,(label,before)
            for k in range(3):state[o+k]+=Y[(s+1)%4][k]-Y[s][k]
            counts[s]+=1
        rows.append({'label':label,'before':before,'service':srv,'after':tuple(state)})
    assert tuple(state)==(0,n-3,0,0,n+2,2)
    assert sum(state)==2*n+1 and counts==[2,4,3,3]
    return {'initial':[0,n,1,0,n,0],'word':rows,'counts_by_source':counts,
            'final':state,'minority_sum_increment':1,'mass_increment':0,
            'consequence':'Priority does not make every activation independently neutral/deleting; joint cleanup is charged its full bounded cost.'}

def main():
    counts=[]
    for H in (1,2,3,5):
        for a,d in ((H,H),(H,1),(H,0),(1,H)):
            for c,f in ((0,0),(1,0),(2,1),(5,7),(20,0),(0,20)):
                counts.append(cleanup_count_check((a,d,c,f)))
    probes=[]
    for n in (20,1000,10**6):
        for J in (1,3,20,100):
            for a,d in ((3,1),(3,2),(3,3),(8,2)):
                for r1,r2 in ((n,n),(n,3*n),(3*n,n)):
                    probes.append(service_probe(n,J,a,d,r1,r2))
    output={'scope':'Finite adversarial work and actual finite service checks. The all-population proof is in POSITIVE_UNPAIRED_JOINT_CLEANUP.md.',
            'work_checks':counts,'service_checks':probes,'stranded_word':raw_word()}
    (P/'results/joint_cleanup_checks.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({'work_cases':len(counts),'adversarial_states':sum(v['states'] for v in counts),
                      'max_noncore':max(v['max_noncore'] for v in counts),
                      'service_cases':len(probes),'worst_scaled_clock':max(v['scaled_clock'] for v in probes),
                      'worst_n_times_interrupt':max(v['scaled_interrupt'] for v in probes),
                      'stranded_word_final':output['stranded_word']['final']},indent=2))

if __name__=='__main__':main()
