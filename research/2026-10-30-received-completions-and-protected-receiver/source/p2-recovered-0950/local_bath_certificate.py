#!/usr/bin/env python3
"""Exact local commutator checks and a finite derivative-majorant example.

Finite chains only. The general size-independent estimate is proved in
LOCAL_REGULARITY.md; these checks neither audit that proof independently nor
qualify arbitrary unbounded all-Fock sources.
"""
from pathlib import Path
from fractions import Fraction as F
from math import factorial
import sys,json
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'p2_algebraic_bus_20261030'))
from exact_sector_check import multiply,add
from check_bus import I,X,Y,Z,kron

def scale(poly,c):return {key:c*x for key,x in poly.items() if c*x}

def delta(h,a):
    out=multiply(h,a)
    for key,x in multiply(a,h).items():add(out,key,-x)
    result={}
    for (w,p),x in out.items():add(result,(w,1-p),x if p==0 else -x)
    return result

def word(n,letters):
    a=['I']*n
    for site,p in letters.items():a[site]=p
    return ''.join(a)

def chain(n):
    h={}
    for site in range(n):
        h[(word(n,{site:'X'}),0)]=F(17,100)
        h[(word(n,{site:'Z'}),0)]=F(11,100)
    for site in range(n-1):
        h[(word(n,{site:'Z',site+1:'X'}),0)]=F(1,5)
        h[(word(n,{site:'Y',site+1:'Y'}),0)]=F(13,100)
    return h

def canonical(poly):return {(w.rstrip('I'),p):v for (w,p),v in poly.items()}

def matrix(poly,n):
    ps={'I':I,'X':X,'Y':Y,'Z':Z};out=np.zeros((2**n,2**n),complex)
    for (w,p),c in poly.items():out+=float(c)*1j**p*kron(*(ps[a] for a in w))
    return out

def exp_series_coefficients(g,n):
    # If A(z)=exp(G(z)), n A_n = sum_{q=1}^n q G_q A_{n-q}.
    a=[F(1)]+[F(0)]*n
    for m in range(1,n+1):a[m]=sum(F(q)*g[q]*a[m-q] for q in range(1,m+1))/m
    return a

def main():
    root=Path(__file__).parent;B0=F(6,5);J=F(2,5);rows=[];jets={}
    for n in [2,4,6,8]:
        h=chain(n);a={(word(n,{0:p}),0):x for p,x in zip('XYZ',[F(9,10),F(1,5),F(-1,10)])}
        jet=[];detail=[]
        for r in range(6):
            l1=sum(abs(x) for x in a.values());bound=B0*(4*J)**r*factorial(r)
            assert l1<=bound,(n,r,l1,bound)
            # Orbit derivatives of a Hermitian operator remain Hermitian.
            assert all(p==0 for (_,p) in a)
            detail.append({'r':r,'exact_Pauli_l1_upper_bound':str(l1),
                           'dimension_independent_bound':str(bound),'Pauli_terms':len(a)})
            jet.append(canonical(a));a=delta(h,a)
        jets[n]=jet
        hm=matrix(h,n);norm=float(np.max(np.abs(np.linalg.eigvalsh(hm))))
        rows.append({'memory_spins':n,'total_Hamiltonian_norm_numerical':norm,'derivatives':detail})
    assert jets[6]==jets[8], 'Up to five commutators the additional remote sites must be irrelevant.'
    for r in range(2):assert jets[2][r]==jets[8][r]
    for r in range(4):assert jets[4][r]==jets[8][r]
    # The previous 96-word family has clean coefficient c T^3 / 13824,
    # where T is total cycle duration. Hadamard gives c <= B0^3.
    k=3;T0=F(1,10);eta0=B0**3/F(13824)
    h=[B0*(4*J)**r*factorial(r) for r in range(k+3)]
    gs={}
    for q in range(1,k+3):
        phi=eta0*F(factorial(k),factorial(k-q))*T0**(k-q) if q<=k else F(0)
        gs[q]=(q*h[q-1]+T0*h[q]+phi)/factorial(q)
    coeff=exp_series_coefficients(gs,k+2);a5=coeff[k+2]
    examples=[]
    for t in [F(1,100),F(1,50),F(1,20)]:
        rb=2*a5*t**5
        examples.append({'cycle_duration':str(t),'exact_residual_bound':str(rb),
                         'residual_bound_float':float(rb),
                         'joint_product_bound':float(rb)+float(rb)**2/(1+np.sqrt(1-float(rb)**2)) if rb<1 else None})
    out={'scope':'Root exact rational finite-chain nested-commutator checks plus a proved derivative-majorant evaluation. No independent review, device, all-Fock qualification, or efficient completed-gate claim.',
         'source_terms':'onsite .17 X + .11 Z; bond .20 Z X + .13 Y Y',
         'coupling_checked':'.9 X0 + .2 Y0 - .1 Z0',
         'J':str(J),'B0':str(B0),'chain_checks':rows,
         'six_and_eight_spin_jets_agree_exactly_through_order':5,
         'base96_majorant':{'k':k,'T0':str(T0),'eta_bound':str(eta0),
                            'a5_exact':str(a5),'examples':examples},
         'scope_limit':'Bounds are per cycle. Completing a finite angle still needs the actual repeated native word and charges its full duration, control errors, and data holding.'}
    (root/'local_bath_certificate.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'chain_norms':[{'spins':r['memory_spins'],'norm':r['total_Hamiltonian_norm_numerical']} for r in rows],
                      'exact_local_jet_agreement':True,'base96_majorant':out['base96_majorant']},indent=2))

if __name__=='__main__':main()
