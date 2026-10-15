#!/usr/bin/env python3
"""Portable exact checker for this worker's positive-branch completed example.

Reads only POSITIVE_R1_COMPLETION.json. The analytic QC implication and
ordinary non-PC support proof are separate written arguments.
"""
import hashlib,json
from itertools import combinations,combinations_with_replacement
from pathlib import Path
import sympy as s

HERE=Path(__file__).resolve().parent
path=HERE/'POSITIVE_R1_COMPLETION.json'
data=json.loads(path.read_text())
matrix=lambda name:s.Matrix([[s.Rational(v) for v in row] for row in data[name]])
C,S,W=map(matrix,['C','S','omega'])
x=s.Matrix(s.symbols('a b c d',real=True));a,b,c,d=x
u=a*a+c*c;j=a*d-b*c;H=((a-d)**2+(b+c)**2)**2
alpha=s.Rational(data['alpha'])
assert data['r']=='1' and data['subtracted_H']=='1' and alpha==62385
F=(alpha-1)*H+j*j+u*j
J1,J2=s.zeros(4,6),s.zeros(4,6)
for i,k in enumerate([0,1,3,4]):J1[i,k]=1
for i,k in enumerate([1,2,4,5]):J2[i,k]=1
Om=s.zeros(4)
pairs=list(combinations(range(4),2));mons=list(combinations_with_replacement(range(4),2))
assert data['omega_pairs']==[list(v) for v in pairs]
assert data['omega_monomials']==[list(v) for v in mons]
for (i,k),p in zip(pairs,W*s.Matrix([x[i]*x[k] for i,k in mons])):Om[i,k],Om[k,i]=p,-p
eta=Om.T*x/4
assert all(s.expand(s.diff(Om[k,l],x[i])-s.diff(Om[i,l],x[k])+s.diff(Om[i,k],x[l]))==0 for i,k,l in combinations(range(4),3))
assert all(s.expand(s.diff(eta[k],x[i])-s.diff(eta[i],x[k])-Om[i,k])==0 for i,k in pairs)
target=J1.T*s.hessian(F,x)*J1+J2.T*s.hessian(F,x)*J2
correction=J1.T*Om*J2
target+=(correction+correction.T)/2
polys=[[s.Poly(s.expand(target[i,k]),*x) for k in range(6)] for i in range(6)]
Q=C*S*C.T
for i,k in mons:
 block=Q[6*i:6*i+6,6*k:6*k+6]
 lhs=block if i==k else block+block.T
 rhs=s.Matrix(6,6,lambda n,m:polys[n][m].coeff_monomial(x[i]*x[k]))
 assert lhs==rhs,(i,k)
L,D=S.LDLdecomposition(hermitian=False)
assert L*D*L.T==S and all(v>0 for v in D.diagonal())
assert list(D.diagonal())==list(map(s.Rational,data['positive_ldl_pivots']))
assert C.rank()==18
receipt=dict(schema='astra-positive-r1-portable-export-check-v1',status='EXACT_PASS',certificate_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),integrand='62385 H+j^2+u j',subtracted_H='1',gram_rank=18,positive_ldl_pivots=18,full_ten_monomial_six_by_six_jet_matrix_identity=True,closedness=True,global_primitive=True,analytic_consequence='All-background QC with affine Jensen margin at least 4/1875, using AUDIT.md. Ordinary non-PC using EXACT_NONPOLYCONVEX_COMPLETION.md.',external_review=False,formal_proof_verification=False,priority='UNKNOWN')
(HERE/'POSITIVE_R1_EXPORT_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('EXACT_PASS: 62385H+j²+uj minus H; exact identity, primitive, rank18 and 18 positive LDL pivots.')
