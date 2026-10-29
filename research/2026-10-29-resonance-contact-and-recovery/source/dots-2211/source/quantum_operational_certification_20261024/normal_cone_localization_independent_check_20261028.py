"""Exact common-bank coefficient expectations, local scores, gap transfer and intertwiner."""
import sympy as s,json
from pathlib import Path
I=s.eye(2);P=[s.Matrix([[0,1],[1,0]]),s.Matrix([[0,-s.I],[s.I,0]]),s.diag(1,-1)];k=s.kronecker_product;B=[k(p,I) for p in P]
def trG(M):return s.Matrix(2,2,lambda a,b:sum(M[2*a+g,2*b+g] for g in range(2)))
def trL(M):return s.Matrix(2,2,lambda a,b:sum(M[2*l+a,2*l+b] for l in range(2)))
banks=[]
for la,ep in [(s.Rational(1,2),s.Rational(1,4)),(s.Rational(3,5),s.Rational(1,5))]:
 C=[la*b/4 for b in B];C[2]+=ep*k(I,P[2])/4
 # Shared uniformly private input j/sign and product-Pauli readout.
 # Integrating physical outcomes gives signed readout mean Tr(P rho).
 checks=0
 for site in range(2):
  for j0 in range(3):
   for ell in range(3):
    observable=k(P[ell],I) if site==0 else k(I,P[ell])
    total=0
    for j in range(3):
     for sign in [-1,1]:
      rho=s.eye(4)/4+sign*C[j]
      for axis0 in range(3):
       for axis1 in range(3):
        if j==j0 and [axis0,axis1][site]==ell:
         total+=s.Rational(1,54)*9*sign*s.trace(observable*rho)
    assert s.simplify(total-s.trace(observable*C[j0]))==0;checks+=1
 local=[trG(c) for c in C];gauge=[trL(c) for c in C]
 assert local==[la*p/2 for p in P] and gauge==[s.zeros(2),s.zeros(2),ep*P[2]/2]
 Y=sum((a*b for a,b in zip(C,B)),s.zeros(4));Q=k(I,Y)-sum((k(p.T,a) for p,a in zip(P,C)),s.zeros(8))
 Qlocal=s.Matrix(4,4,lambda a,b:sum(Q[2*a+g,2*b+g] for g in range(2)))
 Ylocal=sum((a*p for a,p in zip(local,P)),s.zeros(2));assert Qlocal==k(I,Ylocal)-sum((k(p.T,a) for p,a in zip(P,local)),s.zeros(4))
 vL=(1+3*la)/4;vG=(1+ep)/4
 assert vL>vG
 banks.append({'lambda':str(la),'epsilon':str(ep),'exact_common_bank_coefficients':checks,'logical_oracle':str(vL),'gauge_oracle':str(vG)})
# Intertwining formula holds without mutual coefficient commutativity.
intertwines=0
for m in [5,10,20]:
 c=s.Rational(m*m-1,m*m+1);r=s.Rational(2*m,m*m+1);U=s.eye(4);U[0,0]=U[3,3]=c;U[0,3]=r;U[3,0]=-r
 A=[U*b*U.H for b in B];L=(s.eye(4)+sum((a*b for a,b in zip(A,B)),s.zeros(4)))/4
 assert L.det()!=0
 for a,b in zip(A,B):assert a*L==L*b and L.H*L*b==b*L.H*L
 intertwines+=1
out={'status':'PASS_EXACT_COMMON_BANK_AND_INTERTWINER','source_outcomes':0,'banks':banks,'common_average_valid_by_linearity':True,'exact_intertwiner_cases':intertwines,'scope':'Analytic integration of actual private-setting records; not sampled acquisition or confidence acceptance.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(out['status'])
