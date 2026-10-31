"""Exact full-entropy cone arithmetic and finite predictive-flow dual semantics."""
from fractions import Fraction as Q
from pathlib import Path
import json
import math
import sys

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'reversible_currents'))
sys.path.insert(0,str(HERE.parent/'predictive_flow'))
from currents import log_bounds
from flow_grid import geometry,prefix,word_feature


def exponential_bounds(x,terms=60):
    """Positive Taylor series plus a geometric remainder; finite controls."""
    x=Q(x)
    if x<0:
        lo,hi=exponential_bounds(-x,terms)
        return 1/hi,1/lo
    if terms+2<=x:raise ValueError('increase exponential series budget')
    total=term=Q(1)
    for j in range(1,terms+1):
        term*=x/j;total+=term
    remainder=term*x/(terms+1)/(1-x/(terms+2))
    return total,total+remainder


def conjugate_bounds(h,bits=20,method='dyadic_initial_bracket'):
    """Enclose phi*(h), phi(t)=2t atanh(t), using a rational root bracket.

    phi'(t)=log((1+t)/(1-t))+2t/(1-t^2), phi''>=4.
    Every returned bound uses exact Fraction arithmetic and a proved series
    remainder. No floating optimizer contributes validity.
    """
    h=abs(Q(h))
    if h==0:return Q(0),Q(0)
    if bits<1:raise ValueError('positive precision required')
    lo=Q(0)
    if method=='rational_initial_bracket':hi=h/(h+1)
    elif method=='dyadic_initial_bracket':
        hi=Q(1,2)
        while 2*hi/(1-hi*hi)<h:hi=(1+hi)/2
    else:raise ValueError('unknown conjugate root-bracketing method')
    assert 2*hi/(1-hi*hi)>=h
    tolerance=Q(1,2**bits);terms=20+bits
    while hi-lo>tolerance:
        mid=(lo+hi)/2
        llo,lhi=log_bounds((1+mid)/(1-mid),terms)
        dlo,dhi=llo+2*mid/(1-mid*mid),lhi+2*mid/(1-mid*mid)
        if h<=dlo:hi=mid
        elif h>=dhi:lo=mid
        elif dhi-dlo<=tolerance:
            radius=(dhi-dlo)/4
            lo=max(lo,mid-radius);hi=min(hi,mid+radius)
        else:terms+=8
    lower=2*lo*lo/(1-lo*lo)
    upper=min(h*h/8,2*hi*hi/(1-hi*hi))
    assert 0<=lower<=upper
    return lower,upper


def prepare(data,max_states=1000):
    s,L,k=data['alphabet_size'],data['depth'],data['mesh']
    leaves,nodes,descriptors,words=geometry(s,L,k,max_states)
    n,d=len(nodes),len(descriptors)
    a=list(map(Q,data['word_coefficients']))
    y=list(map(Q,data['row_duals']))
    potential=list(map(Q,data['state_potential']))
    if len(a)!=len(words) or len(y)!=n*d or len(potential)!=n or any(v>0 for v in y):
        raise ValueError('invalid full entropy dual shape/signs')
    D=[sum((coef*word_feature(node,w,leaves,L,k) for coef,w in zip(a,words)),Q(0)) for node in nodes]
    cache={}
    for i,node in enumerate(nodes):
        for side,b,w,sign in descriptors:
            cache[i,side,w]=prefix(node,side,w,leaves,k)
            cache[i,side,(b,)+w]=prefix(node,side,(b,)+w,leaves,k)
    active=[[(coef,desc) for coef,desc in zip(y[i*d:(i+1)*d],descriptors) if coef] for i in range(n)]

    def rows(i,j,side):
        value=Q(0)
        for coef,(q,b,w,sign) in active[i]:
            if q==side:
                value+=coef*(sign*((cache[j,q,w] if nodes[j][0]==b else 0)
                                   -cache[i,q,(b,)+w])-Q(1,k))
        return value

    def without_z(i,j):
        return D[i]+potential[i]-potential[j]+rows(i,j,0)+rows(j,i,1)

    B=[Q(0),Q(0)]
    for i in range(n):
        for side in (0,1):
            combined={}
            for coef,(q,b,w,sign) in active[i]:
                if q==side:combined[b,w]=combined.get((b,w),Q(0))+sign*coef
            B[side]=max(B[side],sum(map(abs,combined.values()),Q(0)))
    return {'alphabet':s,'depth':L,'mesh':k,'nodes':nodes,'descriptors':descriptors,
        'words':words,'a':a,'y':y,'potential':potential,'B':B,'without_z':without_z}


def normalization(prepared,bits=20,method='dyadic_initial_bracket'):
    n=len(prepared['nodes']);worst=None;cache={};M=Q(0);minimum=None;count=0
    without_z=prepared['without_z']
    for i in range(n):
        for j in range(i,n):
            hij,hji=without_z(i,j),without_z(j,i)
            hs,ha=(hij+hji)/2,(hij-hji)/2
            key=abs(ha)
            if key not in cache:cache[key]=conjugate_bounds(key,bits,method)[1]
            upper=hs+cache[key]
            worst=upper if worst is None else max(worst,upper)
            minimum=min(hij,hji) if minimum is None else min(minimum,hij,hji)
            M=max(M,abs(ha));count+=1
    return {'z':-worst,'M':M,'H_min':minimum-worst,'columns':count,
        'distinct_conjugate_arguments':len(cache),'conjugate_bits':bits,
        'conjugate_root_method':method}


def verify(data,max_states=1000):
    prepared=prepare(data,max_states)
    found=normalization(prepared,data.get('conjugate_bits',20),data.get('conjugate_root_method','rational_initial_bracket'))
    z=Q(data['normalization_dual'])
    if z>found['z']:raise ValueError('entropy-cone column violated by normalization')
    a=prepared['a'];R=max(a)-min(a);L=prepared['depth']
    root=math.isqrt(L)
    if root*root<L:root+=1
    O=max(prepared['potential'])-min(prepared['potential'])
    C=sum(prepared['B'],Q(0))/2+root*R
    Hmin=found['H_min']+z-found['z']
    return {**prepared,'z':z,'W':[z+x for x in a],'R':R,'O':O,'C':C,
        'M':found['M'],'H_min':Hmin,'columns_checked':found['columns'],
        'distinct_conjugate_arguments':found['distinct_conjugate_arguments'],
        'conjugate_bits':found['conjugate_bits']}


def load(path,max_states=1000):
    return verify(json.loads(Path(path).read_text()),max_states)
