#!/usr/bin/env python3
"""Standalone rational checker for the low-sector prefix identities.

No peer module is imported.  Pfaffians, minors, sign averages, and the small
dyadic self-reduction law are computed directly with Fraction arithmetic.
"""
from fractions import Fraction as Q
from itertools import combinations, product
from functools import lru_cache
from pathlib import Path
from math import comb
import json

Z=(Q(0),Q(0)); ONE=(Q(1),Q(0))
def ca(x,y): return (x[0]+y[0],x[1]+y[1])
def cn(x): return (-x[0],-x[1])
def cs(x,y): return ca(x,cn(y))
def cm(x,y): return (x[0]*y[0]-x[1]*y[1],x[0]*y[1]+x[1]*y[0])
def c2(x): return x[0]*x[0]+x[1]*x[1]
def cdiv_int(x,d): return (x[0]/d,x[1]/d)

def det(A):
    if not A: return ONE
    out=Z
    for j,x in enumerate(A[0]):
        minor=[row[:j]+row[j+1:] for row in A[1:]]
        term=cm(x,det(minor))
        out=ca(out,term if j%2==0 else cn(term))
    return out

def direct_prefix(F,k,U=(),D=(),H=()):
    n=len(F); U,D,H=set(U),set(D),set(H); total=Q(0)
    for I0 in combinations(range(n),k):
        I=set(I0)
        if not U<=I or I&D or I&H: continue
        for J0 in combinations(range(n),k):
            J=set(J0)
            if I&J or not D<=J or J&H or (I|J)&H: continue
            minor=[[F[i][j] for j in sorted(J)] for i in sorted(I)]
            total += c2(det(minor))
    return total

def pa(p,q):
    out=[Z]*max(len(p),len(q))
    for i,x in enumerate(p): out[i]=ca(out[i],x)
    for i,x in enumerate(q): out[i]=ca(out[i],x)
    while len(out)>1 and out[-1]==Z: out.pop()
    return out
def pn(p): return [cn(x) for x in p]
def pm(p,q):
    out=[Z]*max(1,len(p)+len(q)-1)
    for i,x in enumerate(p):
        for j,y in enumerate(q): out[i+j]=ca(out[i+j],cm(x,y))
    while len(out)>1 and out[-1]==Z: out.pop()
    return out

def prefix_Y(F,k,signs,U=(),D=(),H=()):
    """Directly compute sum_R |[z^|U|]Pf(A(z)[R])|^2."""
    n=len(F); U,D,H=set(U),set(D),set(H); a=len(U)
    tau=[]
    for i in range(n):
        if i in U: tau.append([Z,ONE])
        elif i in D or i in H: tau.append([Z])
        else: tau.append([(Q(signs[i]),Q(0))])
    A=[[pa(pm(tau[i],[F[i][j]]),pn(pm(tau[j],[F[j][i]])))
        for j in range(n)] for i in range(n)]
    total=Q(0)
    for R0 in combinations(range(n),2*k):
        R=tuple(R0)
        if not D<=set(R) or set(R)&H: continue
        @lru_cache(None)
        def pf(S):
            if not S: return [ONE]
            out=[Z]
            for j in range(1,len(S)):
                term=pm(A[S[0]][S[j]],pf(S[1:j]+S[j+1:]))
                out=pa(out,term if j%2 else pn(term))
            return out
        coeff=pf(R)[a] if len(pf(R))>a else Z
        total += c2(coeff)
    return total

def make_fixture():
    F=[]
    for i in range(4):
        row=[]
        for j in range(4):
            re=Q((2*i+3*j+1)%7-3,3)
            im=Q((i-2*j+4)%5-2,4)
            row.append((re,im))
        F.append(row)
    Fzero=[[((Q(0) if i==j else Q(1)),Q(0)) for j in range(4)] for i in range(4)]
    return F,Fzero

def prefix_assignments(n):
    for labels in product(range(4),repeat=n):
        yield ({i for i,x in enumerate(labels) if x==1},
               {i for i,x in enumerate(labels) if x==2},
               {i for i,x in enumerate(labels) if x==3})

def target_law(F,k):
    out={}
    for I0 in combinations(range(len(F)),k):
        I=set(I0)
        for J0 in combinations(range(len(F)),k):
            J=set(J0)
            if I&J: continue
            w=c2(det([[F[i][j] for j in sorted(J)] for i in sorted(I)]))
            if w: out[(tuple(sorted(I)),tuple(sorted(J)))]=w
    z=sum(out.values())
    assert z>0
    return {s:w/z for s,w in out.items()}

def dyadic_law(F,k,epsilon):
    n=len(F); B=1
    while (1<<B) < Q(8*n,1)/epsilon: B+=1
    q=1<<B
    states={(frozenset(),frozenset(),frozenset()):Q(1)}
    for site in range(n):
        nxt={}
        for (U,D,H),pstate in states.items():
            weights=[direct_prefix(F,k,U|{site},D,H),
                     direct_prefix(F,k,U,D|{site},H),
                     direct_prefix(F,k,U,D,H|{site})]
            assert sum(weights)==direct_prefix(F,k,U,D,H)
            z=sum(weights)
            assert z>0
            c1=(q*weights[0]/z).numerator//(q*weights[0]/z).denominator
            x=q*(weights[0]+weights[1])/z
            c2floor=x.numerator//x.denominator
            counts=[c1,c2floor-c1,q-c2floor]
            assert all(c>=0 for c in counts)
            for label,count in enumerate(counts):
                if not count: continue
                u,d,h=set(U),set(D),set(H)
                (u if label==0 else d if label==1 else h).add(site)
                key=(frozenset(u),frozenset(d),frozenset(h))
                nxt[key]=nxt.get(key,Q(0))+pstate*Q(count,q)
        states=nxt
    law={(tuple(sorted(U)),tuple(sorted(D))):p
         for (U,D,H),p in states.items()}
    return law,B,q

def legal_completion(n,k,U,D,H,site):
    u,d,h=set(U),set(D),set(H)
    suffix=list(range(site,n))
    nu,nd=k-len(u),k-len(d)
    if nu<0 or nd<0 or nu+nd>len(suffix):
        raise ValueError('prefix has no combinatorial completion')
    u.update(suffix[:nu]); d.update(suffix[nu:nu+nd])
    h.update(suffix[nu+nd:])
    assert len(u)==len(d)==k and not (u&d or u&h or d&h)
    return tuple(sorted(u)),tuple(sorted(d)),tuple(sorted(h))

def main():
    F,Fzero=make_fixture(); exact_checks=zero_checks=0; max_words=0
    for matrix in (F,Fzero):
        for k in (1,2):
            for U,D,H in prefix_assignments(4):
                free=sorted(set(range(4))-U-D-H)
                values=[]
                for ss in product((-1,1),repeat=len(free)):
                    signs=[1]*4
                    for i,s in zip(free,ss): signs[i]=s
                    y=prefix_Y(matrix,k,signs,U,D,H)
                    values.append(y)
                mass=direct_prefix(matrix,k,U,D,H)
                assert sum(values)/len(values)==mass,(k,U,D,H,mass,values)
                a,b=len(U),len(D)
                C=comb(2*k-a-b,k-a) if a<=k and b<=k and a+b<=2*k else 0
                assert all(y>=0 for y in values)
                assert all(y<=C*mass for y in values),(k,U,D,H,C,mass,max(values))
                if mass==0:
                    assert all(y==0 for y in values)
                    zero_checks+=1
                exact_checks+=1; max_words=max(max_words,len(values))
    eps=Q(1,2); approx,B,q=dyadic_law(F,2,eps); truth=target_law(F,2)
    tv=sum(abs(approx.get(s,Q(0))-truth.get(s,Q(0)))
           for s in set(approx)|set(truth))/2
    assert tv<=Q(2*4,q)<=eps
    assert all(p==0 or s in truth for s,p in approx.items())
    fallback=legal_completion(4,1,{0},set(),set(),1)
    out={'status':'PASS','method':'standalone direct Pfaffian/minor computations; no peer module imported',
         'exact_prefix_mean_checks':exact_checks,'zero_prefix_checks':zero_checks,
         'maximum_sign_words_per_prefix':max_words,
         'dyadic_sampler_fixture':{'n':4,'k':2,'epsilon':'1/2','bits_per_site':B,
           'output_count':q,'exact_TV':str(tv),'proved_TV_ceiling':str(Q(8,q)),
           'target_support_size':len(truth),'approx_support_inside_target':True},
         'prefix_consistent_fallback':{'I':fallback[0],'J':fallback[1],'empty':fallback[2]}}
    dest=Path(__file__).with_name('low_sector_outputs')/'phase2_low_sector_independent_check.json'
    dest.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__': main()
