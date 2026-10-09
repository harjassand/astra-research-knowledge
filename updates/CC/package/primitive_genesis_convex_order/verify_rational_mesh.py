#!/usr/bin/env python3
"""Exact finite tests of the rational mesh and positive interpolation compiler.
Numerical LPs select candidate supports; rational arithmetic verifies every
returned support, weight, row sum and transformed vector. LP tolerances are
not accepted as mathematical certificates.
"""
from __future__ import annotations
from pathlib import Path
from fractions import Fraction
import itertools
import json
import math
import numpy as np
from scipy.optimize import linprog
import sympy as sp

ROOT=Path(__file__).resolve().parent
checks=[]
def check(name,ok,**extra):
    if not ok:raise RuntimeError(f'{name}: {extra}')
    checks.append({'name':name,'passed':True,**extra})

def mesh(n):
    result=[]
    for a,b in itertools.product(range(-n,n+1),repeat=2):
        nums=(2*a*n,2*b*n,n*n-a*a-b*b)
        den=n*n+a*a+b*b
        if sum(x*x for x in nums)!=den*den:raise RuntimeError('unit sphere identity')
        for sign in [-1,1]:result.append(tuple(sp.Rational(sign*x,den) for x in nums))
    return sorted(set(result))
for T in [0,1,3,10,100]:
    n=math.isqrt(2*(T+1))
    if n*n<2*(T+1):n+=1
    alpha=Fraction(n*n-1,n*n)
    check(f'rational_headroom_T{T}',alpha**(T+1)>=Fraction(1,2),n=n,
          raw_state_bound=2*(2*n+1)**2)
for n in [2,3,5]:
    pts=mesh(n)
    check(f'unit_mesh_n{n}',len(pts)<=2*(2*n+1)**2,distinct_states=len(pts))

# A mesh for the actual delta=1/3 example at horizon T=3.
n=3;T=3
alpha=sp.Rational(n*n-1,n*n)
u=mesh(n)
W=sp.Matrix(u)/alpha
N=W.rows
float_A=np.vstack([np.ones(N),np.asarray(W.T,float)])
c,s=sp.Rational(3,5),sp.Rational(4,5)
Rx=sp.Matrix([[1,0,0],[0,c,-s],[0,s,c]])
Rz=sp.Matrix([[c,-s,0],[s,c,0],[0,0,1]])
gates=[sp.eye(3),Rx,Rx.T,Rz,Rz.T]
indices=np.linspace(0,N-1,6,dtype=int)
certificates=[]
for gi,g in enumerate(gates):
    for i in indices:
        target=alpha*g*W[int(i),:].T
        rhs=sp.Matrix([1,*target])
        sol=linprog(np.arange(N)*1e-9,A_eq=float_A,b_eq=np.asarray(rhs,float).ravel(),
                    bounds=(0,None),method='highs')
        if not sol.success:raise RuntimeError(sol.message)
        supp=np.flatnonzero(sol.x>1e-9).tolist()
        A=sp.Matrix.vstack(sp.ones(1,len(supp)),W[supp,:].T)
        # A full-column-rank support, possibly of size <4, has one exact candidate.
        if A.rank()!=len(supp):raise RuntimeError('LP support unexpectedly dependent')
        exact=(A.T*A).inv()*A.T*rhs
        ok=A*exact==rhs and all(z>=0 for z in exact)
        check(f'rational_kernel_g{gi}_i{i}',ok,support_size=len(supp))
        certificates.append({'gate':gi,'row':int(i),'support':supp,
                             'weights':[str(z) for z in exact]})
check('rational_mesh_actual_delta_headroom',sp.Rational(1,3)*alpha**(-T-1)<=1,
      states=N,horizon=T,delta='1/3',alpha=str(alpha))
receipt={'status':'All rational finite checks passed; not a full enumeration or formal proof.',
         'check_groups':len(checks),'rational_kernel_certificates':len(certificates),
         'results':checks,'certificates':certificates}
(ROOT/'rational_mesh_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({k:v for k,v in receipt.items() if k not in ['results','certificates']},indent=2))
