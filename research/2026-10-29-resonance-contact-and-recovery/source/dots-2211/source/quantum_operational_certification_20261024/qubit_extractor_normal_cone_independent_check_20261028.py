"""Independent exact curvature, kernel and dual-order checks; no source calls."""
from pathlib import Path
import sympy as s,json
I=s.eye(2);P=[s.Matrix([[0,1],[1,0]]),s.Matrix([[0,-s.I],[s.I,0]]),s.diag(1,-1)];k=s.kronecker_product;d=4
B=[k(p,I) for p in P];C=[b/8 for b in B];C[2]+=k(I,P[2])/16
H=sum((k(p.T,c) for p,c in zip(P,C)),s.zeros(8));KB=(s.eye(8)+sum((k(p.T,b) for p,b in zip(P,B)),s.zeros(8)))/2;PB=KB/2
Y=sum((c*b for c,b in zip(C,B)),s.zeros(4));Q=k(I,Y)-H;mu=s.Rational(3,8)
assert PB*PB==PB and Q*PB==s.zeros(8)
assert all(x>=0 for x in (Q-mu*(s.eye(8)-PB)).eigenvals())
rows=[]
for m in [2,3,5,10]:
 c=s.Rational(m*m-1,m*m+1);r=s.Rational(2*m,m*m+1);U=s.eye(4);U[0,0]=U[3,3]=c;U[0,3]=r;U[3,0]=-r
 for p in [s.Rational(0),s.Rational(2,3),s.Rational(1)]:
  A=[p*U*b*U.H for b in B]
  # Convex combination of an exact embedding and completely depolarizing unital map.
  KA=(s.eye(8)+sum((k(t.T,a) for t,a in zip(P,A)),s.zeros(8)))/2
  assert all(x>=0 for x in KA.eigenvals())
  leak=s.trace((s.eye(8)-PB)*KA);cross=sum(s.trace(a*b) for a,b in zip(A,B));D2=sum(s.trace((a-b)**2) for a,b in zip(A,B));gap=sum(s.trace(c*(b-a)) for c,b,a in zip(C,B,A))
  assert leak==(3*d-cross)/4 and D2<=8*leak and gap>=mu*leak>=mu*D2/8
  if p==1:assert D2==8*leak
  rows.append({'m':m,'CP_mixture':str(p),'objective_gap':str(gap),'curvature_bound':str(mu*D2/8)})
out={'status':'PASS_EXACT_NORMAL_CONE_CURVATURE','source_outcomes':0,'cases':rows,'scope':'Exact 12 physical CP-image fixtures plus kernel and strict gap; proof review establishes generality.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(out['status'])
