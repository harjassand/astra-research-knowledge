#!/usr/bin/env python3
"""An exact raw-list discriminator for the pinned actual-time receiver.

Six controller phases, nonequilibrium cycle affinities, two A/B conversion
orders. All calculations are mathematical; no physical chemistry is operated.
"""
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
import json, math
import sympy as sp

P=Path(__file__).resolve().parent
levels=[0,1,2,0,1,2];nph=len(levels);marked={0};nv=2+nph
T=F(11,10);U=F(137,125);lam=F(1);mu=F(1)
n0=10
raw=[]

def complex_(a=0,b=0,phase=None):
    v=[a,b]+[0]*nph
    if phase is not None:v[2+phase]=1
    return tuple(v)

def pair(y,z,k,l,label):
    raw.append((y,z,F(k),label+' forward'))
    raw.append((z,y,F(l),label+' reverse'))

# Binding ladders plus within-level switches give a genuine driven cycle.
for s,r,k,l in [(0,1,2,3),(1,2,4,5),(3,4,5,7),(4,5,6,11)]:
    pair(complex_(b=1,phase=s),complex_(phase=r),k,l,'binding')
for s,r,k,l in [(0,3,11,13),(1,4,17,19),(2,5,23,29)]:
    pair(complex_(phase=s),complex_(phase=r),k,l,'isomerization')
pair(complex_(a=1,phase=0),complex_(b=1,phase=0),F(3,2),F(5,4),'exchange k0')
pair(complex_(a=1,b=2,phase=0),complex_(b=3,phase=0),F(2,3),F(7,6),'exchange k2')
pair(complex_(),complex_(a=1),lam,mu,'reservoir')

def falling(a,k):
    if a<k:return 0
    v=1
    for i in range(k):v*=a-i
    return v

def rate(x,y,k):
    q=k
    for a,j in zip(x,y):q*=falling(a,j)
    return q

def state(a,n,s):
    assert a>=0 and n>=levels[s]
    return complex_(a,n-levels[s],s)

def read_state(x):
    assert sum(x[2:])==1
    s=next(i for i,a in enumerate(x[2:]) if a)
    return x[0],x[1]+levels[s],s

def neighbors(x):
    for y,z,k,label in raw:
        q=rate(x,y,k)
        if q:
            target=tuple(a-u+v for a,u,v in zip(x,y,z))
            assert min(target)>=0
            yield target,q,label

N=sp.Symbol('n',integer=True,positive=True)
Q=sp.zeros(nph)
for y,z,k,label in raw:
    if label.startswith(('binding','isomerization')):
        s=next(i for i,v in enumerate(y[2:]) if v)
        r=next(i for i,v in enumerate(z[2:]) if v)
        b=N-levels[s];q=sp.Rational(k.numerator,k.denominator)
        for j in range(y[1]):q*=b-j
        Q[s,r]+=q;Q[s,s]-=q
tail=[s for s in range(nph) if s not in marked]
v=sp.zeros(nph,1)
sol=(-Q.extract(tail,tail)).inv()*sp.ones(len(tail),1)
for s,val in zip(tail,sol):v[s]=sp.factor(val)
qv=Q*v
assert all(sp.simplify(qv[s]+1)==0 for s in tail)
J=sp.factor(1+sum(qv[s] for s in marked))
cfr=max(F(3,2)/F(5,4),F(2,3)/F(7,6))
rmin=min(F(5,4),F(7,6));ct=rmin*(1-1/T)/16
eps=sp.factor(sp.Rational(ct.numerator,ct.denominator)*N/J)
h=[sp.factor(1+eps*val) for val in v]
assert all(h[s]==1 for s in marked)

def frac(val):
    p,q=sp.fraction(val);return F(int(p),int(q))

@lru_cache(None)
def hvalues(n):
    if n<n0:return tuple(F(1) for s in range(nph))
    return tuple(frac(x.subs(N,n)) for x in h)

@lru_cache(None)
def powers(base,expo):return base**expo

def normalized_value(x,nbase):
    a,n,s=read_state(x)
    return powers(T,n-nbase)*hvalues(n)[s]+powers(U,a+n)/powers(T,nbase)

def actual_generator_normalized(a,n,s):
    x=state(a,n,s);value=normalized_value(x,n)
    return sum(q*(normalized_value(z,n)-value) for z,q,label in neighbors(x))

def magnitude(x):
    if not x:return {'sign':0,'log10_abs':None}
    return {'sign':1 if x>0 else -1,
            'log10_abs':math.log10(abs(x.numerator))-math.log10(x.denominator)}

if __name__=='__main__':
    # Verify the raw conservation vector and each actual phase/marker guard.
    weights=[1,1]+[1+j for j in levels]
    for y,z,k,label in raw:
        if not label.startswith('reservoir'):
            assert sum(w*(b-a) for w,a,b in zip(weights,y,z))==0
        if label.startswith(('binding','isomerization')):
            assert y[0]==z[0]==0
        if label.startswith('exchange'):
            assert y[2:]==z[2:] and y[2]==1
    # Exact nonequilibrium affinity of one physical binding/switch square.
    affinity=F(2,3)*F(17,19)*F(7,5)*F(13,11)
    assert affinity!=1
    eta=1/(16*cfr*T)
    # Strict rational proof of U^(1+eta)>T by integer powering.
    assert U**(eta.denominator+eta.numerator)>T**eta.denominator
    rows=[];neg_tail=0;head_positive=0
    for n in [10,30,100,1000,10000]:
        e=frac(eps.subs(N,n));hv=hvalues(n)
        qn=Q.subs(N,n);qhv=qn*sp.Matrix([sp.Rational(a.numerator,a.denominator) for a in hv])
        assert all(frac(qhv[s])==-e for s in tail)
        assert all(0<=frac(qhv[s])<=ct*n for s in marked)
        # Counts include the actual seam a=floor(eta*n), high-A dominance,
        # low-A waiting states, and nonequilibrium controller phases.
        alist=sorted({0,1,2,3,max(0,int(eta*n)),int(eta*n)+1,n//2,n,2*n})
        vals=[]
        for a in alist:
            for s in range(nph):
                gen=actual_generator_normalized(a,n,s)
                vals.append(gen)
                if n==10000:
                    assert gen<0,(a,n,s,float(gen));neg_tail+=1
                elif gen>0:head_positive+=1
        rows.append({'n':n,'epsilon':str(e),'max_h':float(max(hv)),
                     'tested_a':alist,'min_LV_over_tn':magnitude(min(vals)),
                     'max_LV_over_tn':magnitude(max(vals))})
    # Verify the true finite head too; it is allowed to have positive drift.
    head_checks=0
    for n in range(n0):
        for s,j in enumerate(levels):
            if n>=j:
                for a in [0,1,4,30]:
                    actual_generator_normalized(a,n,s);head_checks+=1
    out={'scope':'Exact symbolic finite phase acquisition and actual raw-generator diagnostics. The all-state theorem is the separate analytical proof, not these finite samples.',
         'phases':nph,'directed_raw_reactions':len(raw),'sole_reservoir':'0 <-> A',
         'conservative_weights':weights,'marked_phases':sorted(marked),
         't':str(T),'u':str(U),'eta':str(eta),'strict_exponential_join':'verified by exact rational integer powers',
         'one_nonequilibrium_cycle_affinity':str(affinity),
         'ordinary_product_poisson_baseline':'the binding/switch square violates the required phase-weight ratios; no common product-Poisson phase weights satisfy this square',
         'v':list(map(str,v)),'J':str(J),'epsilon':str(eps),
         'actual_tail_negative_states':neg_tail,'smaller_test_positive_drifts_retained':head_positive,
         'actual_finite_head_evaluations':head_checks,'rows':rows,
         'uniform_gap':'NOT_ASSUMED','neighboring_profile_ratios':'NOT_USED; every inventory-changing endpoint is marked with h=1',
         'global_recurrence_for_arbitrary_core':'NOT_ACHIEVED'}
    (P/'results/pinned_phase_checks.json').write_text(json.dumps(out,indent=2)+'\n')
    (P/'results/pinned_phase_raw.json').write_text(json.dumps({'species':['A','B']+['E'+str(i) for i in range(nph)],'phase_inventory':levels,'reactions':[{'source':y,'target':z,'rate':str(k),'label':label} for y,z,k,label in raw]},indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ['v','J','epsilon']},indent=2))
