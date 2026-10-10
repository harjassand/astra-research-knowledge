#!/usr/bin/env python3
"""Exact rational checks of s43's algebra; finite examples are not a proof."""
from fractions import Fraction as F
from itertools import product
import json


class P:
    def __init__(self, n, terms=None):
        self.n = n
        self.t = {k:F(v) for k,v in (terms or {}).items() if v}
    @classmethod
    def c(cls,n,v): return cls(n,{(0,)*n:F(v)})
    @classmethod
    def x(cls,n,i):
        e=[0]*n; e[i]=1
        return cls(n,{tuple(e):1})
    def coerce(self,v): return v if isinstance(v,P) else P.c(self.n,v)
    def __add__(self,b):
        b=self.coerce(b); t=dict(self.t)
        for e,c in b.t.items(): t[e]=t.get(e,F(0))+c
        return P(self.n,t)
    __radd__=__add__
    def __neg__(self): return P(self.n,{e:-c for e,c in self.t.items()})
    def __sub__(self,b): return self+-self.coerce(b)
    def __rsub__(self,b): return self.coerce(b)+-self
    def __mul__(self,b):
        b=self.coerce(b); t={}
        for e,c in self.t.items():
            for d,a in b.t.items():
                z=tuple(x+y for x,y in zip(e,d))
                t[z]=t.get(z,F(0))+c*a
        return P(self.n,t)
    __rmul__=__mul__
    def __truediv__(self,b): return self* (F(1)/F(b))
    def __pow__(self,k):
        z=P.c(self.n,1)
        for _ in range(k): z=z*self
        return z
    def diff(self,i):
        t={}
        for e,c in self.t.items():
            if e[i]:
                d=list(e); d[i]-=1; t[tuple(d)]=c*e[i]
        return P(self.n,t)
    def at0(self): return self.t.get((0,)*self.n,F(0))
    def __eq__(self,b): return self.t==self.coerce(b).t


def L(v,z): return sum((v[i]*z.diff(i) for i in range(len(v))),P.c(len(v),0))
def br(u,v): return [L(u,x)-L(v,y) for x,y in zip(v,u)]
def vs(v,s): return [s*x for x in v]
def va(v,w): return [a+b for a,b in zip(v,w)]
def const(v): return [P.c(len(v),a) for a in v]
def linear(v): return sum((a*P.x(len(v),i) for i,a in enumerate(v)),P.c(len(v),0))
def vec0(v): return [p.at0() for p in v]
def mm(a,b): return [[sum((x*y for x,y in zip(row,col)),F(0)) for col in zip(*b)] for row in a]
def tr(a): return [list(x) for x in zip(*a)]


def solve(a,b):
    a=[[F(x) for x in row]+[F(y)] for row,y in zip(a,b)]; n=len(a)
    for j in range(n):
        k=next((k for k in range(j,n) if a[k][j]),None)
        if k is None: raise ValueError('singular')
        a[j],a[k]=a[k],a[j]
        s=a[j][j]; a[j]=[x/s for x in a[j]]
        for k in range(n):
            if k!=j:
                s=a[k][j]; a[k]=[x-s*y for x,y in zip(a[k],a[j])]
    return [row[-1] for row in a]


def inv(a):
    n=len(a)
    return tr([solve(a,[int(i==j) for i in range(n)]) for j in range(n)])


def rank(a):
    a=[[F(x) for x in row] for row in a]
    if not a: return 0
    r=0
    for j in range(len(a[0])):
        k=next((k for k in range(r,len(a)) if a[k][j]),None)
        if k is None: continue
        a[r],a[k]=a[k],a[r]
        s=a[r][j]; a[r]=[x/s for x in a[r]]
        for k in range(r+1,len(a)):
            s=a[k][j]; a[k]=[x-s*y for x,y in zip(a[k],a[r])]
        r+=1
        if r==len(a): break
    return r


def make(K,alpha):
    n=len(K); x=[P.x(n,i) for i in range(n)]
    f=[-linear(K[i])-F(alpha[i])*x[i]**3 for i in range(n)]
    return n,x,f


def moment_pairs(f,v,z,count):
    fields=[v]; scalars=[z]
    for m in range(count-1):
        fields.append(vs(br(v,br(v,br(fields[-1],f))),F(-1,6)))
        scalars.append(-L(v,L(v,L(f,scalars[-1])))/6)
    moments=[L(v,z).at0() for z in scalars]
    return fields,scalars,moments


def support_euler(f,v,z):
    n=len(v)
    fields,scalars,p=moment_pairs(f,v,z,2*n)
    r=rank([[p[i+j] for j in range(n)] for i in range(n)])
    assert r
    H=[[p[i+j] for j in range(r)] for i in range(r)]
    c=solve(H,[-p[i+r] for i in range(r)])+[F(1)]
    assert c[0]
    E=const([0]*n)
    for j in range(1,r+1):
        Dj=vs(br(v,br(fields[j-1],f)),F(-1,6))
        E=va(E,vs(Dj,-c[j]/c[0]))
    return E,r,c,p


def test_K_action(K,alpha,vraw,label):
    n,x,f=make(K,alpha); v=const(vraw); z=linear(vraw)
    E,r,c,p=support_euler(f,v,z)
    expectE=[x[i] if vraw[i] else P.c(n,0) for i in range(n)]
    assert E==expectE,(label,'E')
    R=vs(br(v,f),-1); W=va(R,vs(br(E,R),-1))
    Kv=va(W,vs(br(W,E),F(-1,2)))
    expected=mm(K,[[F(q)] for q in vraw]); expected=[row[0] for row in expected]
    assert Kv==const(expected),(label,'Kv')
    Rz=-L(f,z)
    zKv=Rz+L(E,Rz)/6-L(E,L(E,Rz))/6
    assert zKv==linear(expected),(label,'zKv')
    beta={F(a)*F(vv)**2 for a,vv in zip(alpha,vraw) if vv}
    assert r==len(beta)
    for b in beta: assert sum((c[j]*b**j for j in range(len(c))),F(0))==0
    return {'case':label,'support_size':sum(bool(v) for v in vraw),'distinct_beta':r,'K_action':'PASS'}


def test_dense(K,alpha,label):
    n,x,f=make(K,alpha); g=const([1]+[0]*(n-1)); h=x[0]
    alpha1=-L(g,L(g,L(g,L(f,h)))).at0()/6
    assert alpha1==alpha[0]
    k=[F(row[0]) for row in K]
    kfield=va(vs(br(g,f),-1),vs(g,-3*alpha1*h**2))
    assert kfield==const(k)
    z0=-L(f,h)-alpha1*h**3
    assert z0==linear(k)
    v,z,p=moment_pairs(f,kfield,z0,2*n)
    beta=[F(a)*q*q for a,q in zip(alpha,k)]
    assert all(k) and len(set(beta))==n
    for m in range(2*n):
        qm=[k[i]*beta[i]**m for i in range(n)]
        assert v[m]==const(qm)
        assert z[m]==linear(qm)
        assert p[m]==sum((k[i]**2*beta[i]**m for i in range(n)),F(0))
    H=[[p[i+j] for j in range(n)] for i in range(n)]
    c=solve(H,[-p[i+n] for i in range(n)])+[F(1)]
    for b in beta: assert sum((c[j]*b**j for j in range(n+1)),F(0))==0
    weights=solve([[b**m for b in beta] for m in range(n)],p[:n])
    assert weights==[q*q for q in k]
    Q=[[k[i]*beta[i]**m for i in range(n)] for m in range(n)]
    B=[[-L(v[j],L(f,z[i])).at0() for j in range(n)] for i in range(n)]
    assert B==mm(mm(Q,K),tr(Q))
    Ki=mm(mm(inv(Q),B),tr(inv(Q)))
    assert Ki==[[F(a) for a in row] for row in K]
    return {'case':label,'n':n,'heterogeneous':len(set(alpha))>1,'dense_recovery':'PASS'}


def W_basis(K,alpha):
    n=len(K); basis=[[F(1)]+[F(0)]*(n-1)]
    while True:
        old=len(basis)
        candidates=[]
        for v in basis: candidates.append([r[0] for r in mm(K,[[q] for q in v])])
        for u,v,w in product(basis,repeat=3):
            candidates.append([F(alpha[i])*u[i]*v[i]*w[i] for i in range(n)])
        for v in candidates:
            if rank(basis+[v])>len(basis):
                basis.append(v); break
        if len(basis)==old or len(basis)==n: return basis


def test_polarization(K,alpha,r=4):
    n,x,f=make(K,alpha); g=const([1]+[0]*(n-1)); h=x[0]
    def opword(fields):
        z=h
        for v in reversed(fields): z=L(v,z)
        return z.at0()
    for letters in product([0,1],repeat=r):
        target=opword([g if v else f for v in letters])
        gsites=[i for i,v in enumerate(letters) if v]
        total=F(0)
        for bits in product([0,1],repeat=len(gsites)):
            a=[0]*r
            for i,b in zip(gsites,bits): a[i]=b
            sign=(-1)**(len(gsites)-sum(bits))
            total+=sign*opword([va(f,vs(g,aa)) for aa in a])
        assert total==target
    return {'case':'pulse_boolean_polarization','word_depth':r,'words':2**r,'status':'PASS'}


def test_canonical_reduction():
    # A rational, signed synchronized block with heterogeneous coefficients,
    # plus a completely inactive physical coordinate.
    V=[[F(1),F(0)],[F(0),F(3,5)],[F(0),F(-4,5)],[F(0),F(0)]]
    orth=[F(0),F(4,5),F(3,5),F(0)]
    Kbar=[[F(4),F(1)],[F(1),F(5)]]
    K=mm(mm(V,Kbar),tr(V))
    K=[[K[i][j]+7*orth[i]*orth[j]+8*int(i==3 and j==3) for j in range(4)] for i in range(4)]
    alpha=[F(2),F(25,9),F(25,16),F(3)]
    assert mm(tr(V),V)==[[F(1),F(0)],[F(0),F(1)]]
    assert mm(K,V)==mm(V,Kbar)
    for j,ab in enumerate([F(2),F(1)]):
        assert [alpha[i]*V[i][j]**3 for i in range(4)]==[ab*V[i][j] for i in range(4)]
    assert len(W_basis(K,alpha))==2
    n,x,f=make(K,alpha)
    q=[V[i][0]+2*V[i][1] for i in range(4)]
    fields,scalars,p=moment_pairs(f,const(q),linear(q),5)
    assert p==[F(2)**m+4*F(4)**m for m in range(5)]
    H2=[[p[i+j] for j in range(2)] for i in range(2)]
    H3=[[p[i+j] for j in range(3)] for i in range(3)]
    assert rank(H2)==2 and rank(H3)==2
    c=solve(H2,[-p[2],-p[3]])+[F(1)]
    assert c==[F(8),F(-6),F(1)]
    weights=solve([[F(2)**m,F(4)**m] for m in range(2)],p[:2])
    assert weights==[F(1),F(4)]
    assert [F(2)/weights[0],F(4)/weights[1]]==[F(2),F(1)]
    Q=[[F(1),F(2)],[F(2),F(8)]]
    B=[[-L(fields[j],L(f,scalars[i])).at0() for j in range(2)] for i in range(2)]
    assert mm(mm(inv(Q),B),tr(inv(Q)))==Kbar
    return {'case':'canonical_weighted_signed_reduction','physical_n':4,'minimal_r':2,'flatness':'PASS','minimal_recovery':'PASS'}


def test_node_census_and_signed_failure():
    K3=[[F(4),F(-1),F(-1)],[F(-1),F(3),F(-1)],[F(-1),F(-1),F(3)]]
    K4=[[F(4),F(-1),F(-1),F(0)],
        [F(-1),F(7,2),F(-3,2),F(1)],
        [F(-1),F(-3,2),F(7,2),F(-1)],
        [F(0),F(1),F(-1),F(6)]]
    for K,q in [(K3,[1,2,2]),(K4,[1,2,2,0])]:
        n,x,f=make(K,[1]*len(K))
        fields,scalars,p=moment_pairs(f,const(q),linear(q),5)
        assert p==[F(1)+8*F(4)**m for m in range(5)]
        H=[[p[i+j] for j in range(2)] for i in range(2)]
        c=solve(H,[-p[2],-p[3]])+[F(1)]
        assert c==[F(4),F(-5),F(1)]
        weights=solve([[F(1)**m,F(4)**m] for m in range(2)],p[:2])
        alpha_bar=[F(1)/weights[0],F(4)/weights[1]]
        assert alpha_bar==[F(1),F(1,2)]
        census=sum(F(1)/a for a in alpha_bar)
        assert census==3
    W3=[[F(1),F(0),F(0)],[F(0),F(1),F(1)]]
    W4=[[F(1),F(0),F(0),F(0)],[F(0),F(1),F(1),F(0)]]
    assert mm(W3,tr(W3))==mm(W4,tr(W4))
    assert mm(mm(W3,K3),tr(W3))==mm(mm(W4,K4),tr(W4))
    assert len(W_basis(K3,[1]*3))==len(W_basis(K4,[1]*4))==2
    return {'case':'M_matrix_census_and_signed_connected_failure','M_matrix_n':3,
            'recovered_census':3,'signed_connected_n':4,'same_canonical_model':'PASS'}


def main():
    out=[]
    K4=[[9,1,2,3],[1,10,1,1],[2,1,11,2],[3,1,2,12]]
    out.append(test_dense(K4,[1,2,3,4],'dense_heterogeneous'))
    out.append(test_dense(K4,[1]*4,'dense_homogeneous'))
    out.append(test_K_action(K4,[1,2,3,4],[1,0,2,0],'sparse_support'))
    out.append(test_K_action(K4,[1,1,2,2],[1,1,0,0],'repeated_beta'))
    out.append(test_K_action(K4,[4,1,2,2],[1,2,0,0],'heterogeneous_beta_collision'))
    out.append(test_polarization([[4,1],[1,3]],[1,2]))
    chain=[[4,1,0,0],[1,5,2,0],[0,2,6,3],[0,0,3,7]]
    W=W_basis(chain,[1,2,3,4]); assert len(W)==4
    out.append({'case':'sparse_chain','closure_dimension':len(W),'n':4,'status':'PASS'})
    u=[1,2,3,4]
    Klow=[[4*int(i==j)+u[i]*u[j] for j in range(4)] for i in range(4)]
    W=W_basis(Klow,[1]*4); assert len(W)==4
    krylov=[[F(1),F(0),F(0),F(0)]]
    for _ in range(3): krylov.append([r[0] for r in mm(Klow,[[q] for q in krylov[-1]])])
    assert rank(krylov)==2
    out.append({'case':'noncyclic_but_nonlinearly_full','linear_cyclic_dimension':2,'closure_dimension':4,'status':'PASS'})
    twin=[[4,1,1],[1,3,1],[1,1,3]]
    twin2=[[4,1,1],[1,F(7,2),F(1,2)],[1,F(1,2),F(7,2)]]
    W=W_basis(twin,[1]*3); assert len(W)==2
    assert mm(twin,tr(W))==mm(twin2,tr(W))
    out.append({'case':'connected_synchrony_counterexample','closure_dimension':2,'n':3,'identical_restricted_dynamics':'PASS'})
    out.append(test_canonical_reduction())
    out.append(test_node_census_and_signed_failure())
    print(json.dumps(out,indent=2))


if __name__=='__main__': main()
