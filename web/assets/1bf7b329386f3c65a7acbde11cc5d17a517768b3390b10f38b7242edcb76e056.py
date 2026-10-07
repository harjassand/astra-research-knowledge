#!/usr/bin/env python3
"""Gaussian-integer exact fixture for the complex rank-one moment formula."""
from fractions import Fraction
from itertools import combinations, permutations
import json
from pathlib import Path

class G:
    __slots__ = ("re", "im")
    def __init__(self, re=0, im=0): self.re, self.im = Fraction(re), Fraction(im)
    def __add__(self, other):
        other = as_g(other); return G(self.re+other.re, self.im+other.im)
    __radd__ = __add__
    def __neg__(self): return G(-self.re, -self.im)
    def __sub__(self, other): return self + (-as_g(other))
    def __rsub__(self, other): return as_g(other) - self
    def __mul__(self, other):
        other = as_g(other); return G(self.re*other.re-self.im*other.im, self.re*other.im+self.im*other.re)
    __rmul__ = __mul__
    def conj(self): return G(self.re, -self.im)
    def norm2(self): return self.re*self.re+self.im*self.im
    def __eq__(self, other):
        other = as_g(other); return self.re == other.re and self.im == other.im
    def __repr__(self): return f"G({self.re},{self.im})"

def as_g(x): return x if isinstance(x, G) else G(x)
def conj(x): return x.conj() if isinstance(x, G) else x
def norm2(x): return x.norm2() if isinstance(x, G) else Fraction(x*x)

def det(A):
    n = len(A)
    if n == 0: return G(1)
    total = G(0)
    for p in permutations(range(n)):
        inv = sum(p[i] > p[j] for i in range(n) for j in range(i+1,n))
        term = G(-1 if inv%2 else 1)
        for i,j in enumerate(p): term = term * A[i][j]
        total = total + term
    return total

def mat(A,I,J): return [[A[i][j] for j in J] for i in I]
def addpoly(a,b,cap):
    z=[0]*(cap+1)
    for i,x in enumerate(a[:cap+1]): z[i]=z[i]+x
    for i,x in enumerate(b[:cap+1]): z[i]=z[i]+x
    return z
def mulpoly(a,b,cap):
    z=[0]*(cap+1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):
            if i+j<=cap: z[i+j]=z[i+j]+x*y
    return z

def local(A,u,v):
    n=len(A); out={name:[] for name in ("A","B","C","U","V")}
    for ell in range(n//2+1):
        aa=bb=cc=0
        for I in combinations(range(n),ell):
            si=set(I)
            for J in combinations([j for j in range(n) if j not in si],ell):
                M=mat(A,I,J); d=det(M); delta=G(0)
                for p in range(ell):
                    for q in range(ell):
                        minor=[row[:q]+row[q+1:] for r,row in enumerate(M) if r!=p]
                        cof=(-1 if (p+q)%2 else 1)*det(minor)
                        delta=delta+v[J[q]]*cof*u[I[p]]
                aa+=norm2(d); bb=bb+d*conj(delta); cc+=norm2(delta)
        out["A"].append(aa); out["B"].append(bb); out["C"].append(cc)
    for ell in range((n-1)//2+1):
        uu=vv=0
        for I in combinations(range(n),ell+1):
            si=set(I)
            for J in combinations([j for j in range(n) if j not in si],ell):
                M=mat(A,I,J); eta=G(0)
                for p in range(ell+1):
                    minor=[row[:] for r,row in enumerate(M) if r!=p]
                    eta=eta+(-1 if p%2 else 1)*u[I[p]]*det(minor)
                uu+=norm2(eta)
        for I in combinations(range(n),ell):
            si=set(I)
            for J in combinations([j for j in range(n) if j not in si],ell+1):
                M=mat(A,I,J); theta=G(0)
                for q in range(ell+1):
                    minor=[row[:q]+row[q+1:] for row in M]
                    theta=theta+(-1 if q%2 else 1)*v[J[q]]*det(minor)
                vv+=norm2(theta)
        out["U"].append(uu); out["V"].append(vv)
    return out

def block_diag(blocks):
    n=sum(len(B) for B in blocks); A=[[G(0) for _ in range(n)] for _ in range(n)]; off=0
    for B in blocks:
        for i in range(len(B)):
            for j in range(len(B)): A[off+i][off+j]=B[i][j]
        off+=len(B)
    return A

def formula(blocks,u,v,k):
    stats=[]; off=0
    for B in blocks:
        stats.append(local(B,u[off:off+len(B)],v[off:off+len(B)])); off+=len(B)
    cap=k; p0=[1]; p1=[G(0)]; p2=[0]
    for s in stats:
        a,b,c=s["A"],s["B"],s["C"]
        p0n=mulpoly(p0,a,cap)
        p1n=addpoly(mulpoly(p1,a,cap),mulpoly(p0,b,cap),cap)
        p2n=addpoly(addpoly(mulpoly(p2,a,cap),mulpoly(p0,c,cap),cap),
                    addpoly(mulpoly([conj(x) for x in p1],b,cap),mulpoly(p1,[conj(x) for x in b],cap),cap),cap)
        p0,p1,p2=p0n,p1n,p2n
    balanced=p0[k]+p1[k]+conj(p1[k])+p2[k]
    mismatch=0
    for a in range(len(stats)):
        for b in range(len(stats)):
            if a==b or k==0: continue
            prod=[1]
            for t,s in enumerate(stats):
                localpoly=s["U"] if t==a else s["V"] if t==b else s["A"]
                prod=mulpoly(prod,localpoly,k-1)
            if k-1<len(prod): mismatch+=prod[k-1]
    return balanced+mismatch,balanced,mismatch

def brute(F,k):
    n=len(F); total=Fraction(0)
    for I in combinations(range(n),k):
        si=set(I)
        for J in combinations([j for j in range(n) if j not in si],k): total+=norm2(det(mat(F,I,J)))
    return total

def main():
    raw_blocks=[
      [[[(0,1),(1,0)],[(1,0),(0,-1)]], [[(1,1),(0,1)],[(1,0),(1,-1)]]],
      [[[(1,0),(0,1)],[(1,-1),(0,0)]], [[(0,1),(1,0)],[(1,1),(0,-1)]]],
    ]
    raw_uv=[
      ([(1,1),(0,-1),(2,0),(1,-1)],[(0,1),(1,0),(-1,1),(2,0)]),
      ([(0,1),(1,0),(1,1),(-1,0)],[(2,0),(-1,1),(0,1),(1,-1)]),
    ]
    results=[]
    for blocks_raw,(u_raw,v_raw) in zip(raw_blocks,raw_uv):
        blocks=[[[G(*z) for z in row] for row in B] for B in blocks_raw]
        A=block_diag(blocks); u=[G(*z) for z in u_raw]; v=[G(*z) for z in v_raw]
        F=[[A[i][j]+u[i]*v[j] for j in range(len(A))] for i in range(len(A))]
        for k in range(len(A)//2+1):
            got,bal,mis=formula(blocks,u,v,k); want=brute(F,k)
            assert got==want,(k,got,want,bal,mis)
            results.append({"case":len(results)//3,"n":len(A),"k":k,"coefficient":str(got),"balanced":str(bal),"defect_pairs":str(mis)})
    result={"status":"PASS exact Gaussian-integer fixtures","results":results,
            "scope":"Finite exact checks for complex cross terms; not proof or external validation."}
    Path(__file__).with_name("rank_one_block_complex_check.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))
if __name__=="__main__": main()
