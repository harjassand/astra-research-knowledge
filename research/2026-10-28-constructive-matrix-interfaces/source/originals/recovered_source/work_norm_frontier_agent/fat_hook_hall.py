#!/usr/bin/env python3
"""Manufactured super-Hall--Littlewood coordinates, without all partitions.
phi(p_j)=sum x_i^j+sum y_i^j/(1-Q^j). All states are m^O(r+s).
"""
from functools import lru_cache
from fractions import Fraction
from collections import Counter

def transpose(lam):return tuple(sum(x>=j for x in lam) for j in range(1,max(lam,default=0)+1))
def contained(mu,lam):return len(mu)<=len(lam) and all(a<=b for a,b in zip(mu,lam))
def n_stat(lam):return sum(i*x for i,x in enumerate(lam))

def smallest_fat_hook(lam):
    """Manufacture alphabet sizes minimizing r+s for this actual shape."""
    candidates=[(r,lam[r] if r<len(lam) else 0) for r in range(len(lam)+1)]
    return min(candidates,key=lambda pair:(sum(pair),abs(pair[0]-pair[1]),pair))

@lru_cache(None)
def fat_shapes(m,r,s):
    result=[]
    def tail(total,cap,previous,cols,top):
        if len(cols)==cap:
            if not total:result.append(tuple(x for x in top if x)+transpose(tuple(cols)))
            return
        for h in range(min(previous,total),-1,-1):tail(total-h,cap,h,cols+[h],top)
    def head(left,previous,top):
        if len(top)==r:
            tail(left,min(s,top[-1]) if top else s,left,[],top);return
        for a in range(min(previous,left),-1,-1):head(left-a,a,top+[a])
    head(m,m,[])
    if len(result)!=len(set(result)):raise AssertionError('duplicate shape')
    return tuple(sorted(result,reverse=True))

@lru_cache(None)
def interlaces(lam):
    out=[]
    def visit(i,nu):
        if i==len(lam):out.append(tuple(x for x in nu if x));return
        low=lam[i+1] if i+1<len(lam) else 0
        for value in range(lam[i],low-1,-1):visit(i+1,nu+[value])
    visit(0,[]);return tuple(out)

@lru_cache(None)
def hl_strip(lam,nu,Q):
    lc=transpose(lam);nc=transpose(nu);counts=Counter(nu);v=Fraction(1,Q);weight=Fraction(1)
    for j in range(len(lc)):
        d0=lc[j]-(nc[j] if j<len(nc) else 0)
        d1=(lc[j+1] if j+1<len(lc) else 0)-(nc[j+1] if j+1<len(nc) else 0)
        if d0==0 and d1==1:weight*=1-v**counts[j+1]
    return weight

@lru_cache(None)
def skew_hl(lam,mu,variables,Q):
    if not contained(mu,lam):return ()
    if not variables:return (((),Fraction(1)),) if lam==mu else ()
    lc=transpose(lam);mc=transpose(mu)
    if any(c-(mc[i] if i<len(mc) else 0)>variables for i,c in enumerate(lc)):return ()
    out={}
    for nu in interlaces(lam):
        if not contained(mu,nu):continue
        coefficient=hl_strip(lam,nu,Q);degree=sum(lam)-sum(nu)
        for powers,value in skew_hl(nu,mu,variables-1,Q):
            key=powers+(degree,);out[key]=out.get(key,0)+coefficient*value
    return tuple((key,value) for key,value in out.items() if value)

@lru_cache(None)
def gaussian(n,k,v):
    if not 0<=k<=n:return 0
    if not k or k==n:return 1
    return gaussian(n-1,k-1,v)+v**k*gaussian(n-1,k,v)

@lru_cache(None)
def whittaker(lam,variables,Q):
    if len(lam)>variables:return ()
    if not variables:return (((),Fraction(1)),) if not lam else ()
    out={};v=Fraction(1,Q)
    for nu in interlaces(lam):
        padded=nu+(0,)*(len(lam)-len(nu));tail=lam[1:]+(0,);coefficient=Fraction(1)
        for a,b,c in zip(lam,tail,padded):coefficient*=gaussian(a-b,a-c,v)
        degree=sum(lam)-sum(nu)
        for powers,value in whittaker(nu,variables-1,Q):
            key=powers+(degree,);out[key]=out.get(key,0)+coefficient*value
    return tuple((key,value) for key,value in out.items() if value)

def narrow_subshapes(lam,s):
    bounds=transpose(lam);bounds=bounds[:s]+(0,)*max(0,s-len(bounds));out=[]
    def visit(j,previous,cols):
        if j==s:out.append(transpose(tuple(cols)));return
        for height in range(min(previous,bounds[j]),-1,-1):visit(j+1,height,cols+[height])
    visit(0,len(lam),[]);return out

def b_factor(lam,Q):
    v=Fraction(1,Q);out=Fraction(1)
    for multiplicity in Counter(lam).values():
        for j in range(1,multiplicity+1):out*=1-v**j
    return out

@lru_cache(None)
def super_hl(lam,r,s,Q):
    out={}
    for mu in narrow_subshapes(lam,s):
        coefficient=Fraction(-1,Q)**sum(mu)/b_factor(mu,Q)
        left=skew_hl(lam,mu,r,Q)
        if not left:continue
        right=whittaker(transpose(mu),s,Q)
        for x,a in left:
            for y,b in right:
                key=x+y;out[key]=out.get(key,0)+coefficient*a*b
    return tuple((key,value) for key,value in out.items() if value)

def leading_term(lam,r,s,Q):
    top=lam[:r]+(0,)*max(0,r-len(lam));tail=lam[r:];columns=transpose(tail)
    if len(columns)>s:return None
    powers=top+columns+(0,)*(s-len(columns))
    return powers,Fraction(-1,Q)**sum(tail)/b_factor(tail,Q)

def multiply(left,right):
    out={}
    for a,c in left.items():
        for b,d in right.items():
            key=tuple(x+y for x,y in zip(a,b));out[key]=out.get(key,0)+c*d
    return {key:value for key,value in out.items() if value}

def compositions(total,length):
    if not length:
        if not total:yield ()
        return
    for first in range(total+1):
        for tail in compositions(total-first,length-1):yield (first,)+tail

def evaluate(poly,point):
    result=Fraction(0)
    for powers,coefficient in poly.items():
        for x,exponent in zip(point,powers):coefficient*=x**exponent
        result+=coefficient
    return result

class FatHookBasis:
    def __init__(self,m,r,s,Q):
        self.m=m;self.r=r;self.s=s;self.Q=Q;self.entries=[]
        for lam in fat_shapes(m,r,s):
            poly=dict(super_hl(lam,r,s,Q));lead,coefficient=leading_term(lam,r,s,Q)
            if not poly or max(poly)!=lead or poly[lead]!=coefficient:
                raise AssertionError('manufactured super-HL leading term mismatch')
            self.entries.append((lead,lam,coefficient,poly))
        self.entries.sort(reverse=True)
    def decode(self,poly):
        residual=dict(poly);out={}
        for lead,lam,diagonal,basis_poly in self.entries:
            value=residual.get(lead,0)/diagonal
            if not value:continue
            out[lam]=value
            for key,c in basis_poly.items():residual[key]=residual.get(key,0)-value*c
        if any(residual.values()):raise ValueError('polynomial outside manufactured super-HL image')
        return out
    def hall_product(self,alpha,beta):
        product=multiply(dict(super_hl(alpha,self.r,self.s,self.Q)),dict(super_hl(beta,self.r,self.s,self.Q)))
        result={}
        for lam,value in self.decode(product).items():
            value*=Fraction(self.Q)**(n_stat(lam)-n_stat(alpha)-n_stat(beta))
            if value.denominator!=1 or value<0:raise AssertionError('nonintegral or negative Hall coefficient')
            if value:result[lam]=value.numerator
        return result
    def evaluation_plan(self,candidates=None):
        """Manufacture independent integer-point evaluations; no kernel calls."""
        n=len(self.entries);pivots={};rows=[];points=[];indices=[];tested=0
        if candidates is None:candidates=compositions(self.m,self.r+self.s)
        for index,point in enumerate(candidates):
            tested+=1;row=[evaluate(poly,point) for lead,lam,c,poly in self.entries]
            reduced=row[:]
            for p,old in sorted(pivots.items()):
                if reduced[p]:
                    coefficient=reduced[p]
                    reduced=[x-coefficient*y for x,y in zip(reduced,old)]
            p=next((i for i,x in enumerate(reduced) if x),None)
            if p is None:continue
            diagonal=reduced[p];pivots[p]=[x/diagonal for x in reduced]
            rows.append(row);points.append(point);indices.append(index)
            if len(rows)==n:break
        if len(rows)!=n:raise AssertionError('integer simplex did not separate the basis')
        return dict(points=points,matrix=rows,indices=indices,candidates_tested=tested)

    def decode_evaluations(self,values,plan):
        n=len(self.entries)
        if len(values)!=n:raise ValueError('one exact value per manufactured point required')
        M=[row[:]+[Fraction(value)] for row,value in zip(plan['matrix'],values)]
        for j in range(n):
            pivot=next((i for i in range(j,n) if M[i][j]),None)
            if pivot is None:raise AssertionError('evaluation matrix is singular')
            M[j],M[pivot]=M[pivot],M[j];diagonal=M[j][j]
            M[j]=[x/diagonal for x in M[j]]
            for i in range(n):
                if i!=j and M[i][j]:
                    coefficient=M[i][j];M[i]=[x-coefficient*y for x,y in zip(M[i],M[j])]
        return {entry[1]:M[i][-1] for i,entry in enumerate(self.entries) if M[i][-1]}
