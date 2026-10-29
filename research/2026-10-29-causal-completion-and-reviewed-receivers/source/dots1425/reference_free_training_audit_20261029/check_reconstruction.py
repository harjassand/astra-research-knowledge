import sympy as s,itertools,json,math
from fractions import Fraction as F
from pathlib import Path
rows=[];signchecks=0;corners=0
for k,d in [(2,3),(3,2),(3,4),(4,3)]:
 # Exact channel from weighted computational measure/prepare, plus complex
 # matrix-unit transfer checked abstractly so no accidentally real-only fixture.
 inputs=[]
 for i in range(k):
  v=s.eye(k)[:,i];inputs.append(v*v.H)
 for i in range(k):
  for j in range(i+1,k):
   ei=s.eye(k)[:,i];ej=s.eye(k)[:,j]
   states=[]
   for phase in [1,-1,s.I,-s.I]:
    v=ei+phase*ej;states.append(v*v.H/2)
   inputs+=states
   R=states[0]-states[1];Y=states[2]-states[3]
   expected=ei*ej.H
   assert (R+s.I*Y)/2==expected
   assert (R-s.I*Y)/2==expected.H;signchecks+=1
 assert len(inputs)==2*k*k-k
 # Output observables recover generic complex Hermitian entries exactly.
 H=s.Matrix(d,d,lambda a,b: s.Rational(a+1,d*d) if a==b else (s.Rational(a+b+1,17)+s.I*s.Rational(b-a,19)))
 assert H==H.H
 for a in range(d):
  P=s.eye(d)[:,a]*s.eye(d)[:,a].H;assert s.trace(P*H)==H[a,a]
  for b in range(a+1,d):
   E=s.eye(d)[:,a]*s.eye(d)[:,b].H;XR=(E+E.H)/2;XI=s.I*(E-E.H)/2
   assert s.simplify(s.trace(XR*H)-s.re(H[a,b]))==0;assert s.simplify(s.trace(XI*H)-s.im(H[a,b]))==0
   assert max(XR.eigenvals())-min(XR.eigenvals())==1
   assert max(XI.eigenvals())-min(XI.eigenvals())==1
 # Worst component-error corners from FOUR individually estimated output entries.
 for erp,erm,eip,eim in itertools.product([-1,1],repeat=4):
  assert abs(F(erp-erm+eip-eim,2*k))<=F(2,k);corners+=1
 rows.append(dict(k=k,d=d,input_settings=len(inputs),total_measurement_settings=len(inputs)*d*d))
# Exact integer confidence schedule implies the exponential Hoeffding budget:
# e^-L <=2^-L for L>=0, proved analytically, and 2^-L<=beta/(2M) checked exactly.
counts=0
for M in [1,12,54,784]:
 for beta in [F(1,2),F(1,1000)]:
  for e0 in [F(1,4),F(1,30)]:
   L=0
   while 2**L<F(2*M)/beta:L+=1
   m=math.ceil(F(L,2)/e0**2)
   assert 2*m*e0**2>=L and F(1,2**L)<=beta/(2*M);counts+=1
out=dict(rows=rows,exact_preparation_sign_identities=signchecks,error_corner_checks=corners,exact_integer_confidence_cases=counts,scope='Exact operator identities, observable signs/ranges, error and integer budgets; no opaque-source training run or full decoder execution')
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
