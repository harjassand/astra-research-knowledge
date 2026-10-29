"""Exact raw-vector-field acquisition of divergence-compensated modules.

Only raw polynomial coefficients, the weight m and a rank budget enter acquire().
The hidden conjugacy is confined to construction and independent validation.
No floating point is used for discovery or closure verification.
"""
from fractions import Fraction as F
import json, time
from pathlib import Path
import sympy as sp
import numpy as np
from scipy.linalg import expm

x, y = sp.symbols('x y')
VARS = (x, y)

def clean(p): return {a: c for a,c in p.items() if c}
def add(p,q,scale=F(1)):
    r=p.copy()
    for a,c in q.items(): r[a]=r.get(a,F(0))+scale*c
    return clean(r)
def mul(p,q):
    r={}
    for a,c in p.items():
        for b,d in q.items():
            ab=tuple(ai+bi for ai,bi in zip(a,b))
            r[ab]=r.get(ab,F(0))+c*d
    return clean(r)
def deriv(p,j):
    r={}
    for a,c in p.items():
        if a[j]:
            b=list(a); b[j]-=1; r[tuple(b)]=c*a[j]
    return r
def fromsym(expr):
    return {a:F(int(c.p),int(c.q)) for a,c in sp.Poly(sp.expand(expr),VARS).terms()}
def tosym(p):
    return sp.Add(*(sp.Rational(c.numerator,c.denominator)*x**a[0]*y**a[1] for a,c in p.items()))
def evaluate(p,point):
    return sum(float(c)*np.prod([point[j]**a[j] for j in range(2)]) for a,c in p.items())
def pivot(p): return max(p,key=lambda a:(sum(a),a))
def degree(p): return max(map(sum,p),default=-1)
def encode(p): return [[list(a),str(c)] for a,c in sorted(p.items())]

def acquire(raw_f,m,rank_budget=20):
    """Returns exact closure or an exact independent-polynomial rank lower bound."""
    if len(raw_f)!=2 or any(len(a)!=2 for f in raw_f for a in f):
        raise ValueError('This exact test implementation supports two variables only.')
    if not isinstance(m,int) or m<0 or rank_budget<0:
        raise ValueError('Weight and rank budget must be nonnegative integers.')
    if rank_budget<3:
        return dict(status='EXACT_RANK_LOWER_BOUND',weight=m,rank_lower_bound=3,seconds=0.,peak_terms=1,peak_degree=1,peak_coefficient_bits=1)
    n=len(raw_f)
    q={}
    for i,f in enumerate(raw_f): q=add(q,deriv(f,i),F(-1,n+1))
    def T(p):
        r=mul(q,p)
        r={a:m*c for a,c in r.items()}
        for j,f in enumerate(raw_f): r=add(r,mul(deriv(p,j),f))
        return r
    basis=[{(0,0):F(1)},{(1,0):F(1)},{(0,1):F(1)}]
    pivots=[pivot(b) for b in basis]
    transitions=[]
    peak_terms=1; peak_degree=1; peak_bits=1
    def inspect(p):
        nonlocal peak_terms,peak_degree,peak_bits
        peak_terms=max(peak_terms,len(p));peak_degree=max(peak_degree,degree(p))
        peak_bits=max(peak_bits,max((max(abs(c.numerator).bit_length(),c.denominator.bit_length()) for c in p.values()),default=0))
    idx=0; start=time.perf_counter()
    while idx<len(basis):
        p=T(basis[idx]);inspect(p); row={}
        for j,(b,a) in enumerate(zip(basis,pivots)):
            c=p.get(a,F(0))
            if c:
                row[j]=c;p=add(p,b,-c);inspect(p)
        if p:
            a=pivot(p);c=p[a]
            b={v:k/c for v,k in p.items()};basis.append(b);pivots.append(a)
            row[len(basis)-1]=c
            if len(basis)>rank_budget:
                return dict(status='EXACT_RANK_LOWER_BOUND',weight=m,rank_lower_bound=len(basis),seconds=time.perf_counter()-start,peak_terms=peak_terms,peak_degree=peak_degree,peak_coefficient_bits=peak_bits)
        transitions.append(row);idx+=1
    r=len(basis)
    A=[[transitions[i].get(j,F(0)) for j in range(r)] for i in range(r)]
    # Independent coefficient-level replay: every output polynomial identity.
    for i,b in enumerate(basis):
        residual=T(b)
        for j,c in enumerate(A[i]): residual=add(residual,basis[j],-c)
        assert not residual
    return dict(status='EXACT_CLOSURE',weight=m,dimension=r,seconds=time.perf_counter()-start,peak_terms=peak_terms,peak_degree=peak_degree,peak_coefficient_bits=peak_bits,q=encode(q),basis=[encode(b) for b in basis],matrix=[[str(c) for c in row] for row in A],_basis=basis,_matrix=A)

def main():
    # Hidden polynomial automorphism, not supplied to acquire():
    # x=u+v^2, y=v+(u+v^2)^2. Degree=4; determinant exactly one.
    u,v=sp.symbols('u v')
    h=sp.Matrix([u+v**2,v+(u+v**2)**2])
    inverse={u:x-(y-x**2)**2,v:y-x**2}
    base=sp.Matrix([u-u*u,7*v-u*v])
    raw=[sp.expand(z.subs(inverse,simultaneous=True)) for z in h.jacobian([u,v])*base]
    raw_poly=list(map(fromsym,raw))
    assert sp.expand(h.jacobian([u,v]).det())==1
    runs=[]
    closed=None
    for m in range(5):
        result=acquire(raw_poly,m,rank_budget=16)
        if result['status']=='EXACT_CLOSURE': closed=result
        runs.append({k:v for k,v in result.items() if not k.startswith('_')})
        print(m,result['status'],result.get('dimension',result.get('rank_lower_bound')),result['seconds'],flush=True)
    assert closed and closed['weight']==4
    assert all(r['status']=='EXACT_RANK_LOWER_BOUND' for r in runs[:4])
    # Independent hidden-flow validation of the acquired raw-state ratio formula.
    A=np.array([[float(c) for c in row] for row in closed['_matrix']])
    tests=[]
    for initial in [(0.2,0.1),(0.6,-0.03),(-0.05,0.05)]:
        u0,v0=initial
        original=np.array([u0+v0*v0,v0+(u0+v0*v0)**2])
        phi0=np.array([evaluate(p,original) for p in closed['_basis']])
        for t in [0.,.03,.11,.2]:
            z=expm(t*A)@phi0
            predicted=z[1:3]/z[0]
            den=1+u0*(np.exp(t)-1)
            ut=u0*np.exp(t)/den; vt=v0*np.exp(7*t)/den
            expected=np.array([ut+vt*vt,vt+(ut+vt*vt)**2])
            err=float(np.max(np.abs(predicted-expected)))
            assert err<1e-9
            tests.append(dict(initial=initial,t=t,max_absolute_error=err,denominator=float(z[0])))
    out=dict(raw_vector_field=[str(z) for z in raw],raw_degrees=[degree(p) for p in raw_poly],raw_term_counts=[len(p) for p in raw_poly],hidden_constructor_for_validation_only=dict(map=[str(z) for z in h],inverse=[str(inverse[u]),str(inverse[v])],base=[str(z) for z in base]),runs=runs,numerical_validation=tests)
    Path(__file__).with_name('results.json').write_text(json.dumps(out,indent=2))
    print('max trajectory error',max(z['max_absolute_error'] for z in tests))

if __name__=='__main__':main()
