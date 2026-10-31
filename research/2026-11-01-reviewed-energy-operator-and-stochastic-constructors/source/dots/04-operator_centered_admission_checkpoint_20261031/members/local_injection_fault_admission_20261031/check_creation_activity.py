#!/usr/bin/env python3
"""Exact finite operator checks for coherent-creation jump-count bounds.
Uses exp(u)=2, hence W=exp(2uN) is rational and all checks are exact.
No empirical or hardware claim; a finite check supplements the general proof.
"""
from pathlib import Path
import json
import sympy as s
I=s.eye(2);X=s.Matrix([[0,1],[1,0]]);Y=s.Matrix([[0,-s.I],[s.I,0]]);Z=s.diag(1,-1)
n=s.diag(0,1);lower=s.Matrix([[0,1],[0,0]])
kron=s.kronecker_product
n1=kron(n,I,I);n2=kron(I,n,I);N=n1+n2
K1=kron(X,I,X);K2=kron(I,Y,Y)
H=K1+K2+3*kron(n,I,Z)+1000*kron(n,n,I)+s.Rational(1,3)*kron(I,I,Z)
H+=s.Rational(7,5)*(kron(lower.T,lower,I)+kron(lower,lower.T,I))
W=kron(s.diag(1,4),s.diag(1,4),I)
rows=[]
for losses in [(16,20),(1,2),(100,101)]:
 for injections in [(s.Rational(0),s.Rational(0)),(s.Rational(1,10),s.Rational(1,7))]:
  jumps=[]
  for loc in range(2):
   L=kron(lower,I,I) if loc==0 else kron(I,lower,I)
   jumps.extend([(s.Rational(losses[loc]),L),(injections[loc],L.H)])
  def adj(O,tilt=1):
   A=s.I*(H*O-O*H)
   for rate,L in jumps:
    B=L.H*L;A+=rate*(tilt*L.H*O*L-(B*O+O*B)/2)
   return s.simplify(A)
  ci_term=sum(s.Rational(1,x) for x in losses)
  mean_rhs=-(losses[0]*n1+losses[1]*n2)/2+(sum(injections)+2*ci_term)*s.eye(8)
  # exp(3u)-1=7, 4 sinh(u)^2/(1-exp(-u))=9/2.
  mgf_B=7*sum(injections)+s.Rational(9,2)*ci_term
  for name,A in [('mean',mean_rhs-adj(N)),('mgf',mgf_B*W-adj(W,2))]:
   assert A==A.H
   L,D=A.LDLdecomposition(hermitian=True)
   assert s.simplify(L*D*L.H-A)==s.zeros(8)
   assert all(s.simplify(D[i,i])>0 for i in range(8))
  rows.append(dict(loss=list(losses),injection=[str(x) for x in injections],exact_PSD_mean=True,exact_PSD_MGF=True,MGF_B=str(mgf_B)))
out=dict(scope=__doc__,cases=len(rows),rows=rows)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
