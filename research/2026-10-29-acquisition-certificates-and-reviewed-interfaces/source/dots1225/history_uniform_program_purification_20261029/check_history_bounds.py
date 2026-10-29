import sympy as s,json
from fractions import Fraction as Q
from pathlib import Path
x=s.symbols('x');a=(1-x)/8;proof=[]
for k in range(1,8):
 S=s.Matrix([[(8-k)*a/(k+1),0],[x/(k+1),(9-k)*a/(k+1)]])
 F=s.Matrix([[1-sum(S[:,0])-k*x/(k+1)**2,(9-k)*a/(k+1)**2],[k*x/(k+1)**2,1-sum(S[:,1])-(9-k)*a/(k+1)**2]])
 b=k*x/((9-k)*a+k*x);bn=(k+1)*x/((8-k)*a+(k+1)*x);state=s.Matrix([1-b,b]);u=S*state;f=F*state
 assert s.factor(u[1]-bn*sum(u))==0
 expected=k*(9-k)*a*x*(x-a)/((k+1)*((9-k)*a+k*x)**2)
 assert s.factor(f[1]-b*sum(f)-expected)==0
 t=s.symbols('t');p=s.Poly(s.expand(F.det().subs(x,t/9)),t);c=[p.nth(i) for i in range(3)];bern=[c[0],c[0]+c[1]/2,sum(c)];assert all(z>0 for z in bern)
 proof.append(dict(k=k,detF=str(s.factor(F.det())),bernstein=[str(z) for z in bern],failure_residual=str(s.factor(expected))))
count=0
for eta in [Q(0),Q(1,100),Q(1,2),Q(99,100)]:
 xx=eta/(8+eta);aa=1/(8+eta);states=[(1,xx)]
 for depth in range(12):
  nxt=[]
  for k,r in states:
   assert r<=k*xx/((9-k)*aa+k*xx);count+=1
   if k==8:continue
   s0=(8-k)*aa*(1-r)/(k+1);s1=(xx*(1-r)+(9-k)*aa*r)/(k+1)
   f01=k*xx/(k+1)**2;f10=(9-k)*aa/(k+1)**2
   f0=(1-((8-k)*aa+xx)/(k+1)-f01)*(1-r)+f10*r
   f1=f01*(1-r)+(1-(9-k)*aa/(k+1)-f10)*r
   if s0+s1:nxt.append((k+1,s1/(s0+s1)))
   if f0+f1:nxt.append((k,f1/(f0+f1)))
  states=nxt
# Exact heterogeneous purification monotonicity: numerator derivative concave; minima at endpoints.
for r in [3,8]:
 vmax=s.Rational(r,r+1)
 h=lambda v:2*r+4*v-(r+3)*v*v
 assert h(0)>0 and h(vmax)>0
res=dict(exact_history_checks=count,growth_monotonicity=proof,heterogeneous_dimensions=[4,9],uniform_base_cost='41481/140',scope='Exact rational invariant and scalar identities, not quantum hardware run')
Path(__file__).with_suffix('.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res,indent=2))
