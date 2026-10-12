"""Sparse, exact Hermitian Pauli algebra used for the transport certificates.
Keys (x,z) encode P=i**popcount(x&z) X**x Z**z. Coefficients are real.
No Hilbert-space matrices are required by the certificate operations.
"""
from fractions import Fraction as Q
from itertools import combinations
from collections import defaultdict
import sympy as sp


def clean(a):
    return {k:v for k,v in a.items() if v != 0}

def add(*args):
    out=defaultdict(lambda:0)
    for a in args:
        for k,v in a.items(): out[k]+=v
    return clean(out)

def scale(a,c): return clean({k:c*v for k,v in a.items()})
def inner(a,b): return sum((v*b.get(k,0) for k,v in a.items()),Q(0))
def norm2(a): return inner(a,a)

def phase(p,q):
    x,z=p; u,v=q
    return ((x&z).bit_count()+(u&v).bit_count()-((x^u)&(z^v)).bit_count()+2*(z&u).bit_count())%4

def A(H,O):
    """Return -i[H,O] exactly for real Hermitian Pauli coefficients."""
    out=defaultdict(lambda:0)
    for p,h in H.items():
        for q,o in O.items():
            ph=phase(p,q)
            if ph in (1,3):
                out[(p[0]^q[0],p[1]^q[1])] += (2 if ph==1 else -2)*h*o
    return clean(out)

def S(O,gamma): return clean({p:2*gamma*p[0].bit_count()*v for p,v in O.items()})
def Sinv(O,gamma): return clean({p:v/(2*gamma*p[0].bit_count()) for p,v in O.items() if p[0]})
def P(O): return {p:v for p,v in O.items() if not p[0]}
def off(O): return {p:v for p,v in O.items() if p[0]}

def string(items):
    x=z=0
    for i,s in items:
        if s in ('X','Y'): x|=1<<i
        if s in ('Y','Z'): z|=1<<i
    return (x,z)

def model(n,t=Q(1),U=Q(4),V=Q(1),fields=None,edge_weights=None):
    if n<5: raise ValueError('Use n>=5 so periodic distances are unambiguous.')
    H={}; J={}; Hhop={}
    edges=[]
    for i in range(n):
        j=(i+1)%n
        te=t if edge_weights is None else edge_weights[i]
        edges.append((i,j,te))
        for s in ('X','Y'):
            Hhop=add(Hhop,{string([(i,s),(j,s)]):-te/2})
        J=add(J,{string([(i,'X'),(j,'Y')]):te/2,
                   string([(i,'Y'),(j,'X')]): -te/2})
        H=add(H,{string([(i,'Z'),(j,'Z')]):U/4},
                {string([(i,'Z'),((i+2)%n,'Z')]):V/4})
    H=add(H,Hhop)
    if fields:
        H=add(H,{(0,1<<i):-h/2 for i,h in enumerate(fields) if h})
    return H,J,Hhop,edges

def swap_mask(mask,i,j):
    return mask^((1<<i)|(1<<j)) if ((mask>>i)^(mask>>j))&1 else mask

def M_diagonal(phi,edges,gamma):
    out=defaultdict(lambda:0)
    d=4*gamma
    for (x,mask),v in phi.items():
        assert x==0
        for i,j,t in edges:
            dst=swap_mask(mask,i,j)
            if dst!=mask:
                out[(0,mask)]+=2*t*t/d*v
                out[(0,dst)]-=2*t*t/d*v
    return clean(out)

def pressure_exact(b,n,edges,gamma):
    """Solve M phi=-b degree by degree with a pinned gauge, using rationals.
    Assumes connected hopping graph and exact source orthogonality per degree.
    """
    phi={}; reports=[]
    degrees=sorted({z.bit_count() for x,z in b})
    for k in degrees:
        masks=[sum(1<<i for i in c) for c in combinations(range(n),k)]
        idx={mask:i for i,mask in enumerate(masks)}
        assert sum((b.get((0,m),0) for m in masks),Q(0))==0
        if len(masks)==1: continue
        mat=sp.zeros(len(masks)-1)
        rhs=sp.Matrix([-sp.Rational(b.get((0,m),0)) for m in masks[:-1]])
        for m in masks[:-1]:
            j=idx[m]
            for (x,dst),v in M_diagonal({(0,m):Q(1)},edges,gamma).items():
                i=idx[dst]
                if i<len(masks)-1: mat[i,j]+=sp.Rational(v)
        sol=mat.inv()*rhs if len(masks)<4 else mat.inv(method='DM')*rhs
        for m,v in zip(masks[:-1],sol):
            if v: phi[(0,m)]=Q(int(sp.numer(v)),int(sp.denom(v)))
        reports.append({'degree':k,'dimension':len(masks),'gauge':'last Walsh coefficient zero'})
    assert not add(M_diagonal(phi,edges,gamma),b)
    return phi,reports

def compile_pair(H,J,g0,n,edges,gamma):
    b=P(A(H,Sinv(add(J,scale(A(H,g0),-1)),gamma)))
    phi,report=pressure_exact(b,n,edges,gamma)
    g=add(g0,phi)
    f=Sinv(add(J,scale(A(H,g),-1)),gamma)
    assert not P(A(H,f)), 'Exact population balance failed'
    return f,g,phi,report

def certificate(H,J,f,g,n,gamma):
    af=A(H,f); ag=A(H,g)
    assert not P(af)
    low=(2*inner(J,f)-inner(f,S(f,gamma))-inner(af,Sinv(af,gamma)))/n
    y=add(J,scale(ag,-1))
    up=(inner(y,Sinv(y,gamma))+inner(g,S(g,gamma)))/n
    # Avoid square roots: residuals in inverse-S norm.
    r1=add(S(f,gamma),scale(y,-1))
    r2=add(S(g,gamma),af)
    gap=(inner(r1,Sinv(r1,gamma))+inner(r2,Sinv(r2,gamma)))/n
    assert up-low==gap
    assert gap>=0
    return low,up,gap

# Optional symmetry reduction. This changes only the exact finite Poisson solve.
pressure_full=pressure_exact

def rotate(mask,n,k=1):
    k%=n
    return ((mask<<k)|(mask>>(n-k)))&((1<<n)-1) if k else mask

def pressure_exact(b,n,edges,gamma):
    cycle={(min(i,j),max(i,j)) for i,j,t in edges}=={(min(i,(i+1)%n),max(i,(i+1)%n)) for i in range(n)}
    uniform=len({t for i,j,t in edges})==1
    invariant=all(b.get((0,rotate(z,n)),0)==v for (x,z),v in b.items())
    if not (cycle and uniform and invariant):
        return pressure_full(b,n,edges,gamma)
    phi={}; reports=[]
    for k in sorted({z.bit_count() for x,z in b}):
        masks=[sum(1<<i for i in c) for c in combinations(range(n),k)]
        reps=sorted({min(rotate(m,n,r) for r in range(n)) for m in masks})
        orbits={m:sorted({rotate(m,n,r) for r in range(n)}) for m in reps}
        assert sum((len(orbits[m])*b.get((0,m),0) for m in reps),Q(0))==0
        if len(reps)==1: continue
        idx={m:i for i,m in enumerate(reps)}
        mat=sp.zeros(len(reps)-1)
        rhs=sp.Matrix([-sp.Rational(b.get((0,m),0)) for m in reps[:-1]])
        for col,m in enumerate(reps[:-1]):
            image=M_diagonal({(0,z):Q(1) for z in orbits[m]},edges,gamma)
            for row,r in enumerate(reps[:-1]):
                mat[row,col]=sp.Rational(image.get((0,r),0))
        sol=mat.inv(method='DM')*rhs
        for m,v in zip(reps[:-1],sol):
            if v:
                for z in orbits[m]: phi[(0,z)]=Q(int(sp.numer(v)),int(sp.denom(v)))
        reports.append({'degree':k,'full_dimension':len(masks),'translation_orbits':len(reps),'gauge':'last orbit coefficient zero'})
    assert not add(M_diagonal(phi,edges,gamma),b)
    return phi,reports
