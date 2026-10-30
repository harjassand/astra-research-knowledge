import sys
sys.dont_write_bytecode=True
import sympy as s
import itertools
from collections import defaultdict
from pathlib import Path
x,y,u,v=s.symbols('x y u v',real=True);V=s.Matrix([x,y,u,v]);r=x*x+y*y;t=u*u+v*v
F=t*t+2*r*t;C1=x*(u*u-v*v);C2=2*x*u*v;HF=s.hessian(F,V);DF=s.Matrix([s.diff(F,j) for j in V]);dCs=[s.Matrix([s.diff(C,j) for j in V]) for C in [C1,C2]]
R=[s.Matrix([1,0,1,0]),s.Matrix([1,0,-1,0]),s.Matrix([2,0,0,2]),s.Matrix([s.Rational(5,4),0,s.Rational(3,4),1])]
k=[(1,0),(0,1),(1,1),(2,1)];phase=[(0,0),(0,0),(-1,0),(-1,-1)]
cs=s.symbols('c0:4');G=sum((R[i]*cs[i] for i in range(4)),s.zeros(4,1));subs=dict(zip(V,G))
def moment(poly):
 out=defaultdict(lambda:s.S.Zero)
 for powers,coeff in s.Poly(s.expand(poly.subs(subs,simultaneous=True)),*cs).terms():
  inds=[j for j in range(4) for z in range(powers[j])];degree=len(inds)
  for signs in itertools.product([-1,1],repeat=degree):
   freq=[sum(signs[h]*k[j][z] for h,j in enumerate(inds)) for z in range(2)]
   if freq!=[0,0]:continue
   ph=tuple(sum(signs[h]*phase[j][z] for h,j in enumerate(inds)) for z in range(2))
   out[ph]+=coeff/s.Integer(2)**degree
 return {key:s.factor(value) for key,value in out.items() if value}
H=sum((HF.subs(dict(zip(V,Ri)))/2 for Ri in R),s.zeros(4));W=s.zeros(4,2);T=s.zeros(2)
for Ri in R:
 Hi=HF.subs(dict(zip(V,Ri)));gi=s.Matrix.hstack(*[g.subs(dict(zip(V,Ri))) for g in dCs]);W+=gi/2;T+=gi.T*Hi.pinv()*gi/2
K=H.row_join(W).col_join(W.T.row_join(T));inv=K.inv()
features=list(DF)+[C1,C2]
targets=[]
for ph in [(1,0),(0,1)]:targets.append(s.Matrix([2*moment(poly).get(ph,0) for poly in features]))
M=s.Matrix.hstack(*targets);cost=(M.T*inv*M/2).applyfunc(s.factor)
f=moment(F);rad=moment(((V.dot(V))/2)**2)
print('targets',M);print('cost',cost);print('F phases',f);print('norm4 phases',rad)
f0=f.get((0,0),0);a=2*f.get((1,1),0);b=2*f.get((1,-1),0)
rad0=rad.get((0,0),0);rada=2*rad.get((1,1),0);radb=2*rad.get((1,-1),0)
low=s.factor(f0-abs(a)-abs(b)-cost[0,0]-cost[1,1]-2*abs(cost[0,1]));upper=rad0+abs(rada)+abs(radb)
print('uniform budget lower',low,'norm4 upper',upper,'ratio',s.factor(low/upper))
# Actual backgrounds for the two moment targets; all y components vanish.
Ai=[]
for Ri in R:
 Hi=HF.subs(dict(zip(V,Ri)));gi=s.Matrix.hstack(*[g.subs(dict(zip(V,Ri))) for g in dCs]);Ai.append((inv[:4,:]*M+Hi.pinv()*gi*inv[4:,:]*M).applyfunc(s.factor))
# Verify every one of the eight cubics, for both phase targets.
basis=list(DF)+[C1,C2,y*(u*u-v*v),2*y*u*v]
for C in basis:
 grad=s.Matrix([s.diff(C,j) for j in V]);mm=moment(C)
 for j,ph in enumerate([(1,0),(0,1)]):
  lhs=sum(grad.subs(dict(zip(V,Ri))).dot(Aij[:,j])/2 for Ri,Aij in zip(R,Ai))
  assert s.factor(lhs-2*mm.get(ph,0))==0
assert low>0
assert s.factor(low-s.Rational(3,2)*upper)>0
reconstructed=sum((Ai[j].T*HF.subs(dict(zip(V,R[j])))*Ai[j]/4 for j in range(4)),s.zeros(2))
assert s.simplify(reconstructed-cost)==s.zeros(2)
Path(__file__).with_name('overlap_exact.txt').write_text('\n'.join(['K='+str(K),'targets='+str(M),'cost='+str(cost),'F='+str(f),'norm4='+str(rad),'budget_lower='+str(low),'norm4_upper='+str(upper),'ratio='+str(s.factor(low/upper))]+['A'+str(i)+'='+str(Aij) for i,Aij in enumerate(Ai)])+'\n')
print('PASS: both overlapping targets match all eight cubics, uniform positive budget')
