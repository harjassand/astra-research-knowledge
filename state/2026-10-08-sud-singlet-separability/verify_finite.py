#!/usr/bin/env python3
"""Exact finite-N SU(2) separability decompositions and SU(3) obstruction.
Requires only Python 3.11+ standard library. Finite arithmetic checks;
not an external proof of asymptotic statements or historical priority.
"""
from dataclasses import dataclass
from fractions import Fraction as F
from math import comb, factorial

@dataclass(frozen=True)
class Q3:
    """a+b sqrt(3), a,b exact rationals."""
    a: F = F(0)
    b: F = F(0)
    def __init__(self,a=0,b=0):
        object.__setattr__(self,"a",F(a))
        object.__setattr__(self,"b",F(b))
    def __add__(self,o):
        if not isinstance(o,Q3):o=Q3(o)
        return Q3(self.a+o.a,self.b+o.b)
    __radd__=__add__
    def __neg__(self): return Q3(-self.a,-self.b)
    def __sub__(self,o): return self+(-o if isinstance(o,Q3) else -Q3(o))
    def __mul__(self,o):
        if not isinstance(o,Q3):o=Q3(o)
        return Q3(self.a*o.a+3*self.b*o.b,self.a*o.b+self.b*o.a)
    __rmul__=__mul__

def product_poly(vectors):
    # Formal real polynomial prod_i(u0+r_i.u). Insert factors of i at integration.
    poly={(0,0,0,0):Q3(1)}
    for vector in vectors:
        nxt={}
        for e,c in poly.items():
            for j,v in enumerate((Q3(1),)+tuple(vector)):
                if not v: continue
                ee=list(e);ee[j]+=1;ee=tuple(ee)
                nxt[ee]=nxt.get(ee,Q3(0))+c*v
        poly=nxt
    return poly

def sphere_moment(e):
    # Haar-SU(2) / uniform S^3 moment. Odd monomials vanish.
    if any(x%2 for x in e):return F(0)
    ms=[x//2 for x in e]; val=F(1)
    for m in ms:
        for j in range(m):val*=F(2*j+1,2)
    for j in range(sum(ms)):val/=j+2
    return val

def sector_weights(vectors):
    k=len(vectors);assert k%2==0
    p=product_poly(vectors); ans=[]
    for j in range(k//2,-1,-1):
        n=2*j;q=Q3()
        # U_n(u0)=sum_h(-1)^h binom(n-h,h)(2u0)^(n-2h).
        for h in range(j+1):
            coef=(-1)**h*comb(n-h,h)*2**(n-2*h)
            for e,c in p.items():
                moment=sphere_moment((e[0]+n-2*h,)+e[1:])
                if moment:
                    im=sum(e[1:]);assert im%2==0
                    q+=c*(coef*moment*(-1)**(im//2))
        q*=2*j+1
        assert q.b==0,(j,q)  # all final weights rational
        ans.append(q.a)
    assert sum(ans)==1,(vectors,ans)
    return tuple(ans)

def tableaux_dim(lam):
    d=len(lam);n=sum(lam);num=factorial(n)
    for i in range(d):
        for j in range(i+1,d):
            num*=lam[i]-lam[j]+j-i
    den=1
    for i in range(d):den*=factorial(lam[i]+d-1-i)
    assert num%den==0
    return num//den

def target_weight(d,N,lam):
    assert N%d==0
    r=N//d
    mu=tuple(r-lam[d-1-i] for i in range(d))
    assert min(mu)>=0
    return F(tableaux_dim(lam)*tableaux_dim(mu),tableaux_dim((r,)*d))

def vec(x=0,y=0,z=0): return (x if isinstance(x,Q3) else Q3(x),
                              y if isinstance(y,Q3) else Q3(y),
                              z if isinstance(z,Q3) else Q3(z))
def main():
    rt=Q3(0,F(1,3))
    tetra=[tuple(Q3(0,F(s,3)) for s in signs)
           for signs in ((1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1))]
    zz=[vec(z=1)]*2+[vec(z=-1)]*2
    tetra_w=sector_weights(tetra)
    zz_w=sector_weights(zz)
    goal4=tuple(target_weight(2,10,lam) for lam in ((4,0),(3,1),(2,2)))
    assert tetra_w==(F(1,9),F(2,3),F(2,9))
    assert zz_w==(F(1,6),F(1,2),F(1,3))
    assert tuple((6*a+b)/7 for a,b in zip(tetra_w,zz_w))==goal4
    print("PASS Omega(10,4): 6/7 tetrahedron twirl + 1/7 two-antipodal-pair twirl")
    zd=[vec(z=1)]*3+[vec(z=-1)]*3
    h=[vec(1,0,0),
       vec(F(-1,2),Q3(0,F(1,2)),0),
       vec(F(-1,2),Q3(0,F(-1,2)),0)]*2
    up=[vec(Q3(0,F(1,2)),0,F(1,2)),
        vec(Q3(0,F(-1,4)),F(3,4),F(1,2)),
        vec(Q3(0,F(-1,4)),F(-3,4),F(1,2))]
    p=up+[vec(x,y,-z) for x,y,z in up]
    qd,qh,qp=map(sector_weights,(zd,h,p))
    assert qd==(F(1,20),F(1,4),F(9,20),F(1,4))
    assert qh==(F(11,320),F(15,64),F(189,320),F(9,64))
    assert qp==(F(233,10240),F(539,2048),F(5877,10240),F(287,2048))
    goal6=tuple(target_weight(2,16,lam) for lam in ((6,0),(5,1),(4,2),(3,3)))
    assert tuple((201*a+16*b+3072*c)/3289
                 for a,b,c in zip(qd,qh,qp))==goal6
    print("PASS Omega(16,6): (201D+16H+3072P)/3289 twirl")
    psym=target_weight(3,9,(3,0,0))
    assert psym==F(5,42)
    gap=F(1,6)-psym
    assert gap==F(1,21)
    print("PASS Omega(9,3): symmetric probability 5/42, separable >=1/6, distance >=1/21")
    print("All finite identities exactly verified using rational arithmetic in Q(sqrt 3).")

if __name__=="__main__":
    main()
