"""A small dependency-light, exact-rational prototype of cyclic acquisition.

Acquisition uses only the supplied matvec closure, not the hidden blocks.
Fraction Gaussian elimination here prioritizes inspectability, not optimal speed.
NumPy is used only after exact checks for an additional numerical spectrum check.
"""
from fractions import Fraction as F
import random
import json
import numpy as np


def eye(n):
    return [[F(i==j) for j in range(n)] for i in range(n)]


def transpose(A):
    return [list(x) for x in zip(*A)]


def mm(A,B):
    return [[sum(a*b for a,b in zip(row,col)) for col in zip(*B)] for row in A]


def add(A,B):
    return [[a+b for a,b in zip(ra,rb)] for ra,rb in zip(A,B)]


def scale(t,A):
    return [[t*a for a in row] for row in A]


def cols(vs):
    return transpose(vs)


def solve_columns(vs,y):
    """Return the unique coefficients if independent columns vs span y; else None."""
    d=len(vs)
    if not d:
        return [] if not any(y) else None
    M=[list(row)+[b] for row,b in zip(cols(vs),y)]
    pivot=0
    for j in range(d):
        i=next((i for i in range(pivot,len(M)) if M[i][j]),None)
        assert i is not None, "basis columns must remain independent"
        M[pivot],M[i]=M[i],M[pivot]
        z=M[pivot][j]
        M[pivot]=[v/z for v in M[pivot]]
        for i in range(len(M)):
            if i!=pivot and M[i][j]:
                z=M[i][j]
                M[i]=[a-z*b for a,b in zip(M[i],M[pivot])]
        pivot+=1
    if any(any(row[:d]) is False and row[d] for row in M[d:]):
        return None
    return [M[j][d] for j in range(d)]


def inverse(A):
    vectors=transpose(A)
    return cols([solve_columns(vectors,e) for e in transpose(eye(len(A)))])


def rank(vs):
    basis=[]
    for v in vs:
        if solve_columns(basis,v) is None:
            basis.append(v)
    return len(basis)


def acquire(n,k,matvec,g):
    basis=[g]
    products={}
    word_lengths=[0]
    idx=0
    queries=0
    while idx<len(basis):
        for j in range(k):
            y=matvec(j,basis[idx])
            queries+=1
            c=solve_columns(basis,y)
            if c is None:
                basis.append(y)
                word_lengths.append(word_lengths[idx]+1)
                c=[F(0)]*(len(basis)-1)+[F(1)]
            products[j,idx]=c
        idx+=1
    d=len(basis)
    compressed=[cols([products[j,i]+[F(0)]*(d-len(products[j,i]))
                      for i in range(d)]) for j in range(k)]
    return cols(basis),compressed,queries,max(word_lengths)


def rational_task(A1,A2):
    n=len(A1)
    D=add(scale(F(2),eye(n)),mm(A1,A1))
    X=add(add(mm(mm(A1,A2),A1),scale(F(2),A2)),scale(F(3),A1))
    Di=inverse(D)
    return mm(mm(Di,X),Di)


def distinct(xs,tol=1e-7):
    out=[]
    for x in sorted(xs):
        if not out or abs(x-out[-1])>tol:
            out.append(float(x))
    return out


if __name__ == '__main__':
    # Hidden decomposition M_2 tensor I_3 plus C tensor I_2: N=8, a=5, D=5.
    n=8
    A1=eye(n)
    for i in range(3,6): A1[i][i]=F(-1)
    A1[6][6]=A1[7][7]=F(2)
    A2=[[F(0)]*n for _ in range(n)]
    for i in range(3): A2[i][i+3]=A2[i+3][i]=F(1)
    A2[6][6]=A2[7][7]=F(3)
    v=[F(i+1) for i in range(n)]
    H=add(eye(n),scale(-F(2)/sum(x*x for x in v),mm(cols([v]),[v])))
    assert mm(H,H)==eye(n)
    hidden=[mm(mm(H,A),H) for A in (A1,A2)]
    rng=random.Random(1909)
    g=[F(rng.randint(1,19)) for _ in range(n)]
    def oracle(j,x):
        return [row[0] for row in mm(hidden[j],cols([x]))]
    V,B,queries,depth=acquire(n,2,oracle,g)
    d=len(B[0])
    assert d==5 and queries==2*d
    G=mm(transpose(V),V)
    for A,C in zip(hidden,B):
        assert mm(A,V)==mm(V,C)
        assert mm(G,C)==mm(transpose(C),G)
    full_basis=[eye(n),hidden[0],hidden[1],mm(hidden[0],hidden[1]),mm(hidden[0],hidden[0])]
    reduced_basis=[eye(d),B[0],B[1],mm(B[0],B[1]),mm(B[0],B[0])]
    assert rank([sum(A,[]) for A in full_basis])==5
    assert rank([sum(A,[]) for A in reduced_basis])==5
    Rfull=rational_task(*hidden)
    Rsmall=rational_task(*B)
    assert mm(Rfull,V)==mm(V,Rsmall)
    assert mm(G,Rsmall)==mm(transpose(Rsmall),G)
    # Orthonormalize only for the numerical, independent spectrum check.
    Gf=np.array(G,dtype=float)
    L=np.linalg.cholesky(Gf)
    S=L.T@np.array(Rsmall,dtype=float)@np.linalg.inv(L.T)
    ev_full=distinct(np.linalg.eigvalsh(np.array(Rfull,dtype=float)))
    ev_small=distinct(np.linalg.eigvalsh((S+S.T)/2))
    assert np.allclose(ev_full,ev_small,atol=1e-8)
    print(json.dumps({"status":"exact_acquisition_and_rational_intertwining_passed",
        "ambient_dimension":n,"algebra_dimension":5,"cyclic_dimension":d,
        "generator_matvecs":queries,"max_acquired_word_depth":depth,
        "exact_faithfulness_rank":5,"distinct_full_spectrum":ev_full,
        "distinct_compressed_spectrum":ev_small},indent=2))
