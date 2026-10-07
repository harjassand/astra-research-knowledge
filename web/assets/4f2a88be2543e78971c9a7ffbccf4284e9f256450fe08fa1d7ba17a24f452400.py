"""Exact rational cube rounding: no supplied signing oracle.

Moment-based balanced signings + common-uniform dyadic initialization +
Caratheodory reduction after every coarsening. Research fixture implementation;
uses Fraction elimination, not an optimized numerical backend.
"""
from fractions import Fraction as F
from math import comb, gcd, lcm
from itertools import product
import json, time


def balanced_sign(A, S, counter):
    """Return balanced signs via conditional expectations of even row moments."""
    m=len(A); s=len(S)
    if not s: return []
    r=(2*m-1).bit_length(); degree=2*r
    padded=list(S)+([-1] if s%2 else [])
    pairs=list(zip(padded[::2],padded[1::2]))
    ds=[[ (row[i] if i>=0 else F(0))-(row[j] if j>=0 else F(0))
          for i,j in pairs] for row in A]
    suffix=[]
    for d in ds:
        moments=[[F(0)]*(degree+1) for _ in range(len(pairs)+1)]
        moments[-1][0]=F(1)
        for t in range(len(pairs)-1,-1,-1):
            for ell in range(0,degree+1,2):
                moments[t][ell]=sum(F(comb(ell,v))*d[t]**v*moments[t+1][ell-v]
                                        for v in range(0,ell+1,2))
        suffix.append(moments)
    prefix=[F(0)]*m; choices=[]
    for t in range(len(pairs)):
        costs=[]
        for sign in (-1,1):
            cost=F(0)
            for i in range(m):
                u=prefix[i]+sign*ds[i][t]
                cost+=sum(F(comb(degree,ell))*u**(degree-ell)*suffix[i][t+1][ell]
                           for ell in range(0,degree+1,2))
            costs.append(cost)
        sign=-1 if costs[0]<=costs[1] else 1
        choices.append(sign)
        for i in range(m):prefix[i]+=sign*ds[i][t]
    signs={}
    for (i,j),sign in zip(pairs,choices):
        if i>=0:signs[i]=sign
        if j>=0:signs[j]=-sign
    xi=[signs[j] for j in S]
    assert abs(sum(xi))<=1
    # Independent direct row check certifies the actual generated signing.
    assert all(sum(A[i][j]*signs[j] for j in S)**2 < 8*r*s for i in range(m))
    counter['signing_calls']+=1
    counter['max_signing_size']=max(counter['max_signing_size'],s)
    return xi


def dependence(atoms):
    """An integer affine dependence, or None if columns are independent."""
    if not atoms:return None
    n=len(atoms[0]); count=len(atoms)
    M=[[F(1)]*count]+[[atoms[j][i] for j in range(count)] for i in range(n)]
    pivot_cols=[]; row=0
    for col in range(count):
        pivot=next((i for i in range(row,n+1) if M[i][col]),None)
        if pivot is None:continue
        M[row],M[pivot]=M[pivot],M[row]
        scale=M[row][col]; M[row]=[v/scale for v in M[row]]
        for i in range(n+1):
            if i!=row and M[i][col]:
                scale=M[i][col];M[i]=[u-scale*v for u,v in zip(M[i],M[row])]
        pivot_cols.append(col);row+=1
        if row==n+1:break
    free=next((i for i in range(count) if i not in pivot_cols),None)
    if free is None:return None
    z=[F(0)]*count;z[free]=F(1)
    for i,col in enumerate(pivot_cols):z[col]=-M[i][free]
    denominator=lcm(*(v.denominator for v in z))
    z=[int(v*denominator) for v in z]
    common=gcd(*z);return [v//common for v in z]


def compress(law,counter):
    merged={}
    for atom,weight in law:
        if weight:merged[atom]=merged.get(atom,F(0))+weight
    law=list(merged.items())
    counter['max_precompression_support']=max(counter['max_precompression_support'],len(law))
    while True:
        z=dependence([a for a,w in law])
        if z is None:return law
        theta=min(w/v for (a,w),v in zip(law,z) if v>0)
        law=[(a,w-theta*v) for (a,w),v in zip(law,z) if w-theta*v]
        assert all(w>0 for a,w in law)
        counter['compression_deletions']+=1


def round_law(A,p):
    A=[[F(x) for x in row] for row in A];p=[F(x) for x in p]
    m=len(A);n=len(p)
    assert m and n and all(len(row)==n and all(abs(x)<=1 for x in row) for row in A)
    assert all(0<=x<=1 for x in p)
    counter={'signing_calls':0,'max_signing_size':0,'compression_deletions':0,'max_precompression_support':0}
    baseline=[int(x>F(1,2)) for x in p];qtarget=[min(x,1-x) for x in p]
    signs=[1-2*x for x in baseline]
    Acenter=[[x*d for x,d in zip(row,signs)] for row in A]
    mu=sum(qtarget);J=(n-1).bit_length();grid=F(1,2**J)
    if mu<=1:
        law=[(tuple(F(0) for _ in p),1-mu)] if mu<1 else []
        for i,v in enumerate(qtarget):
            if v:
                a=[F(0)]*n;a[i]=F(1);law.append((tuple(a),v))
    else:
        lower=[F((x/grid).numerator//(x/grid).denominator)*grid for x in qtarget]
        thresholds=[(x-low)/grid for x,low in zip(qtarget,lower)]
        cutpoints=sorted(set([F(0),F(1)]+thresholds))
        law=[]
        for left,right in zip(cutpoints,cutpoints[1:]):
            u=(left+right)/2
            law.append((tuple(low+grid*int(u<t) for low,t in zip(lower,thresholds)),right-left))
        law=compress(law,counter)
        for h in range(J,0,-1):
            step=F(1,2**h); branches=[]
            for atom,weight in law:
                S=[j for j,x in enumerate(atom) if int(x*2**h)%2]
                xi=balanced_sign(Acenter,S,counter) if S else []
                if not S:branches.append((atom,weight));continue
                for orient in (-1,1):
                    new=list(atom)
                    for j,d in zip(S,xi):new[j]+=orient*step*d
                    assert all(0<=x<=1 for x in new)
                    branches.append((tuple(new),weight/2))
            law=compress(branches,counter)
            # These checks are independent of the signing's moment certificate.
            assert sum(w for a,w in law)==1
            assert all(sum(w*a[j] for a,w in law)==qtarget[j] for j in range(n))
            assert all(sum(a)<=mu+2 for a,w in law)
    output=[(tuple(F(b+d*x) for b,d,x in zip(baseline,signs,atom)),weight) for atom,weight in law]
    assert len(output)<=n+1
    return output,counter


def check(A,p,law):
    p=[F(v) for v in p];n=len(p);mu=sum(min(v,1-v) for v in p)
    assert sum(w for a,w in law)==1
    assert all(w>0 and all(x in (0,1) for x in a) for a,w in law)
    assert all(sum(w*a[j] for a,w in law)==p[j] for j in range(n))
    assert all(all(a[j]==p[j] for j in range(n) if p[j] in (0,1)) for a,w in law)
    maxerr=max(abs(sum(F(x)*(z-v) for x,z,v in zip(row,a,p))) for row in A for a,w in law)
    r=(2*len(A)-1).bit_length()
    if mu<=1:assert maxerr<=1+mu
    else:assert (max(F(0),maxerr-1))**2<=144*r*mu
    return str(maxerr)


def fixtures():
    start=time.monotonic();summary=[]
    # Non-dyadic means, forced face coordinates, centered near-one coordinates.
    cases=[(4, [F(1,3),F(1,7),F(2,5),F(0)]),
           (6, [F(1,2)]*6),
           (6,[F(3,7),F(2,5),F(4,9),F(1),F(0),F(3,8)]),
           (8,[F(1,3),F(2,5),F(3,7),F(4,9)]*2),
           (12,[F(1,2)]*12)]
    for n,p in cases:
        A=[]
        for i in range(n):
            A.append([F(1 if ((i*j+j*j+i)%3) else -1) for j in range(n)])
        A.extend([[F(1)]*n,[F((-1)**j) for j in range(n)]])
        law,counter=round_law(A,p);err=check(A,p,law)
        summary.append({'n':n,'rows':len(A),'support':len(law),'error':err,**counter})
    # Vary all means over a 4-coordinate rational grid (independent mean audit).
    grid=[F(0),F(1,3),F(1,2),F(2,3),F(1)]
    A=[[F((-1)**((i+1)*j+j*j)) for j in range(4)] for i in range(4)]
    count=0
    for p in product(grid,repeat=4):
        law,counter=round_law(A,p);check(A,p,law);count+=1
    return {'status':'exact_fixture_checks_passed','rational_grid_laws':count,'fixtures':summary,'elapsed_seconds':time.monotonic()-start,
            'scope':'Exact finite compiler tests. General proof uses the moment inequality and affine dependence argument; these tests are not asymptotic validation.'}

if __name__=='__main__':
    report=fixtures();print(json.dumps(report,indent=2))
    with open('work/scouts/rounding_sparse_compiler_checks.json','w') as f:json.dump(report,f,indent=2)
