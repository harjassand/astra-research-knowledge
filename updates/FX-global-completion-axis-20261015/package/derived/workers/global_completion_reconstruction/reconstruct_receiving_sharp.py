#!/usr/bin/env python3
"""Independent tensor and pivot reconstruction of the pinned receiving theorem.

Reads W without importing or executing its code and writes only beside this file.
"""
from __future__ import annotations
import hashlib
import json
from itertools import combinations, combinations_with_replacement
from pathlib import Path
import time
import sympy as sp

HERE=Path(__file__).resolve().parent
W=Path('/Users/harjas/Documents/ChatGPT/ultra/work/astra-global-completion-axis-20261015')
SOURCE=W/'updates/FW-moving-heat-observable-20261015/package/derived/workers/sharp_boundary_qc/UNIVERSAL_SHARP_NEGATIVE_CERTIFICATE.json'
data=json.loads(SOURCE.read_text())
r,y=sp.symbols('r y',real=True)
started=time.monotonic()
checks=[]
def check(label,value,**fields):
    if not bool(value): raise AssertionError(label)
    checks.append(dict(label=label,status='EXACT_PASS',**fields))
    print('PASS:',label,flush=True)
def zero(M): return all(sp.cancel(v)==0 for v in M)
def rat(item):
    return sp.cancel(sum(sp.Rational(c)*r**i for i,c in enumerate(item['numerator']))/sum(sp.Rational(c)*r**i for i,c in enumerate(item['denominator'])))
def matrix(name): return sp.Matrix([[rat(v) for v in row] for row in data[name]])
def positive_polynomial(pol):
    cc=sp.Poly(pol,y).all_coeffs()
    if all(c>=0 for c in cc) and any(c>0 for c in cc): return 1
    if all(c<=0 for c in cc) and any(c<0 for c in cc): return -1
    return 0
def positive_on_negative_branch(f):
    num,den=sp.fraction(sp.cancel(f.subs(r,-2-y)))
    return positive_polynomial(num)!=0 and positive_polynomial(num)==positive_polynomial(den)
def no_zero_on_negative_branch(f):
    num,den=sp.fraction(sp.cancel(f.subs(r,-2-y)))
    return positive_polynomial(num)!=0 and positive_polynomial(den)!=0
C,S,V,WW=[matrix(n) for n in ('C','S','congruence_basis_V','W')]
d1,d2=map(rat,data['diffusion'])
check('receiving dimensions and symmetry',C.shape==(24,12) and S.shape==(12,12) and zero(S-S.T) and V.shape==(12,12) and WW.shape==(6,10))
check('receiving fixed identity minor rank',C[12:,:]==sp.eye(12))
check('receiving denominators have no poles for r<-2',all(no_zero_on_negative_branch(sp.denom(v)) for M in (C,S,V,WW) for v in M))
check('receiving natural diffusion positive whole branch',sp.cancel(d1-(2*r+1)/(r-1))==0 and sp.cancel(d2+3/(r-1))==0 and positive_on_negative_branch(d1) and positive_on_negative_branch(d2))
x=sp.Matrix(sp.symbols('a b c d',real=True));a,b,c,d=x
u=a*a+c*c;j=a*d-b*c;H=((a-d)**2+(b+c)**2)**2
F=3*r*H/(8*(r+2))+r*(r-1)*u*u/6+j*j+r*u*j
J1,J2=sp.zeros(4,6),sp.zeros(4,6)
for i,k in enumerate((0,1,3,4)):J1[i,k]=1
for i,k in enumerate((1,2,4,5)):J2[i,k]=1
pairs=list(combinations(range(4),2));mons=list(combinations_with_replacement(range(4),2))
check('receiving exported two-form order',data['two_form_pair_order']==[list(v) for v in pairs] and data['quadratic_monomial_order']==[list(v) for v in mons])
Om=sp.zeros(4)
for (i,k),v in zip(pairs,WW*sp.Matrix([x[i]*x[k] for i,k in mons])):Om[i,k],Om[k,i]=v,-v
eta=Om.T*x/4
check('receiving closedness',all(sp.cancel(sp.diff(Om[k,l],x[i])-sp.diff(Om[i,l],x[k])+sp.diff(Om[i,k],x[l]))==0 for i,k,l in combinations(range(4),3)))
check('receiving global Euler primitive',all(sp.cancel(sp.diff(eta[k],x[i])-sp.diff(eta[i],x[k])-Om[i,k])==0 for i,k in pairs))
target=d1*J1.T*sp.hessian(F,x)*J1+d2*J2.T*sp.hessian(F,x)*J2
null=J1.T*Om*J2;target+=(null+null.T)/2
polys=[[sp.Poly(sp.expand(target[i,k]),*x) for k in range(6)] for i in range(6)]
Q=(C*S*C.T).applyfunc(sp.cancel)
for i,k in mons:
    block=Q[6*i:6*i+6,6*k:6*k+6]
    lhs=block if i==k else block+block.T
    rhs=sp.Matrix(6,6,lambda n,m:polys[n][m].coeff_monomial(x[i]*x[k]))
    check(f'receiving universal tensor identity A-monomial {i},{k}',zero(lhs-rhs))
detV=sp.factor(V.det())
check('receiving invertible congruence whole branch',sp.factor(detV+432*(r+1)/(2*r+1)**3)==0 and no_zero_on_negative_branch(detV),determinant=str(detV))
congruence=(V.T*S*V).applyfunc(sp.cancel)
sizes=[4,4,2,2];offset=0;pivots=[]
reconstruction=sp.zeros(12)
for k,sz in enumerate(sizes):
    block=congruence[offset:offset+sz,offset:offset+sz]
    LL,DD=block.LDLdecomposition(hermitian=False)
    check(f'receiving independently recomputed block {k} LDL',zero(LL*DD*LL.T-block))
    pp=[sp.factor(v) for v in DD.diagonal()]
    check(f'receiving block {k} pivots positive for every r<-2',all(positive_on_negative_branch(v) for v in pp),pivots=[str(v) for v in pp])
    reconstruction[offset:offset+sz,offset:offset+sz]=block
    pivots.extend(pp);offset+=sz
check('receiving zero off-block entries',zero(congruence-reconstruction))
check('receiving total positive pivot count',len(pivots)==12)
receipt=dict(schema='astra-independent-receiving-sharp-reconstruction-v1',status='EXACT_RECONSTRUCTION_PASS',pinned_main='ab5118e70a7e6a0dd39e75dd563d3a3f50b06b25',certificate_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),sympy_version=sp.__version__,checks=checks,elapsed_seconds=time.monotonic()-started,scope='Independent internal reconstruction of exact universal negative-branch certificate. The all-background heat argument is separately audited in AUDIT.md. No external review or priority clearance.')
(HERE/'RECEIVING_SHARP_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('EXACT_RECONSTRUCTION_PASS',flush=True)
