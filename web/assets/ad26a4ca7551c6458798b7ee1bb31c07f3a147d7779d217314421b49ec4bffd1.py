"""Exact symbolic identities underlying the all-d O(d) proof; requires SymPy.
The accompanying proof, not a finite dimension sweep, supplies quantifiers.
"""
from pathlib import Path
import json, hashlib
import sympy as s
D,A,B=s.symbols('d a b',real=True)
x=s.Symbol('x')
H=s.ones(3)+(D-1)*s.eye(3)
K=s.Matrix([[D-1,1,0],[1,D-1,0],[-1,-1,0]])
assert H*K==K.T*H
assert s.expand(K.charpoly(x).as_expr()-x*(x-D)*(x-D+2))==0
assert s.factor(H.det())==(D-1)**2*(D+2)
N0=2+(D-1)*(D*A+(D+2)*B)
NS=2-D*A+(D-2)*B
NA=2+D*A-(D+2)*B
assert s.expand(N0+(D-1)*NA)==s.expand(2*D*(1+(D-1)*A))
assert s.expand(N0+(D-1)*NS)==s.expand(2*D*(1+(D-1)*B))
na=D*(D-1)/2;ns=(D-1)*(D+2)/2
assert s.expand(2*(na*A+ns*B)-(D-1)*(D*A+(D+2)*B))==0
u=(2-D*(2*A-1))/(D+2)
assert s.cancel(u-(2*B-1)-2*(D+2-D*A-(D+2)*B)/(D+2))==0
t=s.symbols('t',real=True)
ca=(1-t)/(D-1);cb=(D-2+D*t)/((D-1)*(D+2))
assert s.factor(1+na*ca+ns*cb)==D
lam=(D+2)/(2*(D+1));V=D**2-1;k=D-1
assert s.factor((V-k)/(V-lam*V))==2
# Literal contraction identity in two fixed dimensions; analytic all-d proof separate.
checks=[]
for d in [3,4]:
 def ev(a,b,c):
  v=s.zeros(d**3,1);v[d*d*a+d*b+c]=1;return v
 swapAB=s.zeros(d**3);swapAC=s.zeros(d**3)
 for a in range(d):
  for b in range(d):
   for c in range(d):
    col=d*d*a+d*b+c
    swapAB[d*d*b+d*a+c,col]=1
    swapAC[d*d*c+d*b+a,col]=1
 C=[]
 for v in range(d):
  C.extend([sum((ev(i,i,v) for i in range(d)),s.zeros(d**3,1)),sum((ev(i,v,i) for i in range(d)),s.zeros(d**3,1)),sum((ev(v,i,i) for i in range(d)),s.zeros(d**3,1))])
 eAB=sum((C[3*v]*C[3*v].T for v in range(d)),s.zeros(d**3))
 eAC=sum((C[3*v+1]*C[3*v+1].T for v in range(d)),s.zeros(d**3))
 star=eAB+eAC-swapAB-swapAC
 U=s.Matrix.hstack(*C)
 assert U.T*U==s.diag(*([H.subs(D,d)]*d))
 assert star*U==U*s.diag(*([K.subs(D,d)]*d))
 # General two-sector Choi formula, exact symbolic a,b eigenprojectors.
 F=s.zeros(d*d);e=s.zeros(d*d)
 for i in range(d):
  for j in range(d):F[d*j+i,d*i+j]=1;e[d*i+i,d*j+j]=1
 Po=e/d;Ps=(s.eye(d*d)+F)/2-Po;Pa=(s.eye(d*d)-F)/2
 J=(A+B)*Po/2+(B-A)*F/(2*d)+(1-B)*s.eye(d*d)/d**2
 expected=N0.subs(D,d)*Po/(2*d*d)+NS.subs(D,d)*Ps/(2*d*d)+NA.subs(D,d)*Pa/(2*d*d)
 assert all(s.expand(v)==0 for v in J-expected)
 checks.append({'d':d,'Gram_and_contraction_matrix':True,'Choi_projector_identity':True})
out={'status':'PASS','general_symbolic_identities':['Gram self-adjointness and exact characteristic polynomial','CP lower-bound combinations','full-frame normalization','comparator slack identity','pure-orbit trace profiles','all-d sharpness ratio'],'fixed_dimension_identity_checks':checks,'scope':'General theorem is analytic in PROOF.txt; these exact identities are internal arithmetic evidence, not a formal kernel replay.'}
path=Path(__file__).parent
out['proof_sha256']=hashlib.sha256((path/'PROOF.txt').read_bytes()).hexdigest()
(path/'replay.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
