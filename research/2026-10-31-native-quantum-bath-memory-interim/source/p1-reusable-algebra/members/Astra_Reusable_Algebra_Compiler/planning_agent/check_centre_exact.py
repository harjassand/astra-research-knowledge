"""Exact centre-only extraction on the N=8 hidden rational demonstration.

The general proof permits algebraic-number roots. This small example has
rational central roots, so Python Fraction suffices for a transparent check.
"""
from fractions import Fraction as F
from math import isqrt
import random
import json
from check_cyclic_exact import eye,transpose,mm,add,scale,cols,rank,solve_columns,acquire,rational_task


def linear_combination(coeffs,matrices):
    R=scale(F(0),matrices[0])
    for c,A in zip(coeffs,matrices): R=add(R,scale(c,A))
    return R


def nullspace(M):
    M=[row[:] for row in M]
    rows=len(M)
    n=len(M[0])
    pivot_rows=[]
    i=0
    for j in range(n):
        p=next((p for p in range(i,rows) if M[p][j]),None)
        if p is None: continue
        M[p],M[i]=M[i],M[p]
        z=M[i][j]
        M[i]=[v/z for v in M[i]]
        for p in range(rows):
            if p!=i and M[p][j]:
                z=M[p][j]
                M[p]=[a-z*b for a,b in zip(M[p],M[i])]
        pivot_rows.append((j,i))
        i+=1
        if i==rows: break
    pivots={j for j,i in pivot_rows}
    ans=[]
    for f in range(n):
        if f in pivots: continue
        x=[F(0)]*n
        x[f]=F(1)
        for j,i in pivot_rows: x[j]=-M[i][f]
        ans.append(x)
    return ans


def algebra_basis(generators):
    d=len(generators[0])
    E=[eye(d)]
    idx=0
    while idx<len(E):
        for B in generators:
            Y=mm(B,E[idx])
            if solve_columns([sum(X,[]) for X in E],sum(Y,[])) is None:
                E.append(Y)
        idx+=1
    return E


def centre_basis(E,generators):
    commutator_columns=[]
    for X in E:
        commutator_columns.append(sum([sum(add(mm(X,B),scale(F(-1),mm(B,X))),[])
                                       for B in generators],[]))
    coeffs=nullspace(cols(commutator_columns))
    return [linear_combination(c,E) for c in coeffs]


def minimal_polynomial(Z):
    powers=[]
    P=eye(len(Z))
    while True:
        c=solve_columns(powers,sum(P,[]))
        if c is not None: return [-x for x in c]+[F(1)]
        powers.append(sum(P,[]))
        P=mm(P,Z)


def rational_sqrt(x):
    a,b=isqrt(x.numerator),isqrt(x.denominator)
    assert a*a==x.numerator and b*b==x.denominator
    return F(a,b)


def trace(A):
    return sum(A[i][i] for i in range(len(A)))


if __name__=='__main__':
    n=8
    A1=eye(n)
    for i in range(3,6): A1[i][i]=F(-1)
    A1[6][6]=A1[7][7]=F(2)
    A2=[[F(0)]*n for _ in range(n)]
    for i in range(3): A2[i][i+3]=A2[i+3][i]=F(1)
    A2[6][6]=A2[7][7]=F(3)
    v=[F(i+1) for i in range(n)]
    H=add(eye(n),scale(-F(2)/sum(x*x for x in v),mm(cols([v]),[v])))
    hidden=[mm(mm(H,A),H) for A in (A1,A2)]
    rng=random.Random(1909)
    g=[F(rng.randint(-19,19)) for _ in range(n)]
    V,B,queries,depth=acquire(n,2,lambda j,x:[r[0] for r in mm(hidden[j],cols([x]))],g)
    G=mm(transpose(V),V)
    E=algebra_basis(B)
    C=centre_basis(E,B)
    assert len(E)==5 and len(C)==2
    for Z in C:
        assert mm(G,Z)==mm(transpose(Z),G)
    for t in range(1,5):
        Z=add(C[0],scale(F(t),C[1]))
        f=minimal_polynomial(Z)
        if len(f)-1==len(C): break
    assert len(f)==3
    disc=rational_sqrt(f[1]*f[1]-4*f[0])
    roots=[(-f[1]-disc)/2,(-f[1]+disc)/2]
    d=len(B[0])
    projectors=[scale(1/(a-b),add(Z,scale(-b,eye(d))))
                for a,b in (roots,roots[::-1])]
    assert add(*projectors)==eye(d)
    R=rational_task(*B)
    results=[]
    for P in projectors:
        assert mm(P,P)==P
        assert mm(G,P)==mm(transpose(P),G)
        da=rank([sum(mm(P,X),[]) for X in E])
        Ra=rank(transpose(P))
        ra=isqrt(da)
        assert ra*ra==da and Ra%ra==0
        sa=Ra//ra
        results.append({"simple_algebra_dimension":da,"central_projector_rank":Ra,
                        "irrep_dimension":ra,"compressed_multiplicity":sa,
                        "one_copy_rational_task_trace":str(trace(mm(P,R))/sa),
                        "seed_projected_energy":str(mm(G,P)[0][0])})
    assert sorted((r['irrep_dimension'],r['compressed_multiplicity']) for r in results)==[(1,1),(2,2)]
    assert sum(mm(G,P)[0][0] for P in projectors)==sum(x*x for x in g)
    print(json.dumps({"status":"exact_centre_projector_and_dimension_checks_passed",
        "ambient_dimension":n,"cyclic_dimension":d,"algebra_dimension":len(E),
        "centre_dimension":len(C),"central_minimal_polynomial_coefficients":[str(x) for x in f],
        "central_roots":[str(x) for x in roots],"generator_matvecs":queries,
        "blocks":results},indent=2))
