#!/usr/bin/env python3
"""Fresh dense and exact audit of the supplied double-factorial spin family.
No imports from the prior candidate's computational code.
"""
from __future__ import annotations
import json, math
from pathlib import Path
from fractions import Fraction
import numpy as np
import sympy as sp

ROOT=Path(__file__).resolve().parents[1]
PAULI=[np.array([[0,1],[1,0]],complex),np.array([[0,-1j],[1j,0]]),np.diag([1.,-1.])]

def op_site(a,i,n):
    r=np.ones((1,1),complex)
    for q in range(n): r=np.kron(r,a if q==i else np.eye(2))
    return r

def pt(a,n,subset):
    axes=list(range(2*n))
    for i in subset: axes[i],axes[n+i]=axes[n+i],axes[i]
    return a.reshape([2]*(2*n)).transpose(axes).reshape(2**n,2**n)

def dfac(m): return math.prod(range(1,m+1,2))

def dense(n):
    js=[sum((op_site(a,i,n)/2 for i in range(n)),start=np.zeros((2**n,2**n),complex)) for a in PAULI]
    cas=sum((j@j for j in js),start=np.zeros((2**n,2**n),complex))
    vals,vecs=np.linalg.eigh(cas)
    weights=np.array([1/dfac(2*int(round((math.sqrt(1+4*max(0,v))-1)/2))+1) for v in vals])
    rho=(vecs*weights)@vecs.conj().T; rho/=np.trace(rho)
    cuts=[]
    for k in range(1,n//2+1):
        e=np.linalg.eigvalsh(pt(rho,n,range(k)))
        cuts.append({'cut_size':k,'pt_min_eigenvalue':float(e[0])})
    return {'N':n,'casimir':float(np.trace(rho@cas).real),'cuts':cuts},rho,cas

def exact_four():
    sx=sp.Matrix([[0,1],[1,0]]); sy=sp.Matrix([[0,-sp.I],[sp.I,0]]); sz=sp.diag(1,-1)
    eye=sp.eye(16); js=[]
    for s in [sx,sy,sz]:
        j=sp.zeros(16)
        for i in range(4):
            j+=sp.kronecker_product(*(s if q==i else sp.eye(2) for q in range(4)))/2
        js.append(j)
    c=sum((j*j for j in js),sp.zeros(16))
    # Spectral projectors from exact Lagrange polynomials in the Casimir.
    p0=(c-2*eye)*(c-6*eye)/12
    p1=-c*(c-6*eye)/8
    p2=c*(c-2*eye)/24
    r=p0+p1/3+p2/15; r/=sp.trace(r)
    pt2=sp.zeros(16)
    for i in range(4):
        for a in range(4):
            for j in range(4):
                for b in range(4): pt2[4*i+a,4*j+b]=r[4*i+b,4*j+a]
    vals=pt2.eigenvals()
    assert sp.Rational(-1,48) in vals
    vectors=(pt2+sp.eye(16)/48).nullspace()
    # A Schmidt-rank-two vector inside the negative eigenspace proves
    # one-copy distillability across the two-laboratory 2:2 cut.
    witnesses=[]
    for v in vectors:
        x=sp.Matrix(4,4,list(v))
        if x.rank()<=2:
            num=sp.simplify((v.conjugate().T*pt2*v)[0]); den=sp.simplify((v.conjugate().T*v)[0])
            witnesses.append({'vector':[str(z) for z in v],'schmidt_rank':x.rank(),
              'normalized_pt_expectation':str(sp.simplify(num/den))})
    assert witnesses
    return {'rho_eigenvalues':{str(k):v for k,v in r.eigenvals().items()},
      'pt_two_two_eigenvalues':{str(k):v for k,v in vals.items()},
      'rank_two_negative_vectors':witnesses,'casimir':str(sp.trace(r*c))}

def exact_spin_one_block():
    root2=sp.sqrt(2)
    sp1=sp.Matrix([[0,root2,0],[0,0,root2],[0,0,0]])
    sm1=sp1.T
    ss=[(sp1+sm1)/2,(sp1-sm1)/(2*sp.I),sp.diag(1,0,-1)]
    jj=[sp.kronecker_product(a,sp.eye(3))+sp.kronecker_product(sp.eye(3),a) for a in ss]
    c=sum((a*a for a in jj),sp.zeros(9)); eye=sp.eye(9)
    p0=(c-2*eye)*(c-6*eye)/12
    p1=-c*(c-6*eye)/8
    p2=c*(c-2*eye)/24
    rho=(p0+p1/3+p2/15)*sp.Rational(3,7)
    tr=sp.zeros(9)
    for i in range(3):
        for a in range(3):
            for j in range(3):
                for b in range(3): tr[3*i+a,3*j+b]=rho[3*i+b,3*j+a]
    v=sp.zeros(9,1);v[1]=v[5]=1/root2
    ev=(v.conjugate().T*tr*v)[0]
    assert ev==-sp.Rational(1,21)
    assert sp.Matrix(3,3,list(v)).rank()==2
    return {'normalized_block':'(3/7)P_0+(1/7)P_1+(1/35)P_2',
        'PT_eigenvalues':{str(k):v for k,v in tr.eigenvals().items()},
        'rank_two_vector':'(|+1,0>+|0,-1>)/sqrt(2)',
        'PT_expectation':str(ev),
        'all_even_N_scope':'Every even N>=4 contains this conditional spin-1 versus spin-1 block after operations local to the 2:(N-2) grouped cut.'}

def main():
    rows=[]
    for n in [2,4,6,8]:
        row,_,_=dense(n); rows.append(row)
        assert row['cuts'][0]['pt_min_eigenvalue'] > -1e-12
        if n>=4: assert row['cuts'][1]['pt_min_eigenvalue'] < -1e-4
    exact=exact_four()
    # Cross-copy product of local Bell pairs is separable across the N labs.
    # For singlet projectors, <Phi_{2^N}|P0 tensor P0|Phi_{2^N}>
    # =rank(P0)/2^N, which can exceed the square of the single-copy SEP max.
    cross=[]
    for n in range(2,13):
        N=2*n
        mult=math.comb(N,n)-math.comb(N,n-1)
        value=Fraction(mult,2**N)
        single=Fraction(1,n+1)
        cross.append({'N':N,'local_bell_two_copy_value':str(value),
          'squared_single_copy_bound':str(single**2),'strict_violation':value>single**2})
    assert cross[0]['strict_violation']
    result={'status':'Fresh internal audit, not external verification',
      'dense_reconstructions':rows,'exact_four_qubit_certificate':exact,'exact_spin_one_block':exact_spin_one_block(),
      'failure_of_single_copy_bound_multiplicativity':cross,
      'scope':'Larger-cut NPT does not contradict singleton separability. It blocks a fully-PPT reinterpretation. A rank-two PT-negative vector certifies distillation only when each side may jointly operate its two qubits.'}
    path=ROOT/'results'/'prior_family_audit.json'; path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__': main()
