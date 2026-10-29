import sympy as s,json
from fractions import Fraction as F
from math import ceil
from pathlib import Path
I=s.eye(2);X=s.Matrix([[0,1],[1,0]]);Y=s.Matrix([[0,-s.I],[s.I,0]]);Z=s.diag(1,-1)
states=[(I+sign*P)/2 for P in [X,Y,Z] for sign in [-1,1]]
rows=[]
for a,b in [(s.Rational(4,5),s.Rational(3,5)),(s.Rational(3,5),s.Rational(4,5)),(s.Rational(12,13),s.Rational(5,13)),(s.Integer(1),s.Integer(0)),(s.Integer(0),s.Integer(1))]:
 Ks=[s.diag(1,a),s.Matrix([[0,b],[0,0]])]
 Fe=sum(s.trace(K)*s.conjugate(s.trace(K)) for K in Ks)/4
 avg=sum(s.trace(r*sum((K*r*K.H for K in Ks),s.zeros(2))) for r in states)/6
 assert s.simplify(avg-(2*Fe+1)/3)==0
 rows.append({'a':str(a),'Fe':str(Fe),'Favg':str(avg)})
seed=[]
for k in [2,4,16,256]:
 for eps in [F(1,2),F(1,10)]:
  for b in [2,10]:
   h=k*eps/(k+1);m=ceil(32*b/h);B=0
   while F(1,2**B)>F(1,256*m):B+=1
   assert m*F(1,2**B)<=F(1,256)
   assert (3*h*m/4).__floor__()==24*b
   seed.append([k,str(eps),b,m,B])
assert F(1,4)+F(3,4)*F(1,128)<F(1,2)
Path(__file__).with_suffix('.json').write_text(json.dumps({'exact_six_state_channels':rows,'finite_sampler_schedules':seed,'scope':'standard identity and integer schedules, not full decoder execution'},indent=2)+'\n')
print('PASS',len(rows),'exact channel identities',len(seed),'schedules')
