import json
import numpy as np
import sympy as s
from scipy.optimize import minimize_scalar
from pathlib import Path
x,u,y=s.symbols('x u y', real=True)
C=s.Matrix([[s.sqrt(3)*x,x**9],[3*x,s.sqrt(3)*x]])/4
T0=s.Matrix([[s.Rational(1,2),-s.sqrt(3)/2],[s.sqrt(3)/2,s.Rational(1,2)]])
T1=s.Matrix([[s.sqrt(3)/2,-s.Rational(1,2)],[s.Rational(1,2),s.sqrt(3)/2]])
M=s.simplify(T0.T*C*T1)
f2=(21*x*x-6*x**10+x**18)/16
r=(9*x-x**9)/8
assert s.simplify(s.trace(C.T*C)+2*C.det()-f2)==0
assert s.simplify(f2-r*r-3*x*x*(1-x**8)**2/64)==0
A=y*y-6*y+21
gap=y**s.Rational(1,8)*(2*s.sqrt(A)+y-9)/16
derivative_certificate=3*(y-1)*(6*y-14+3*s.sqrt(A))/(128*y**s.Rational(7,8)*s.sqrt(A))
assert s.simplify(s.diff(gap,y)-derivative_certificate)==0
y_star=(19-2*s.sqrt(85))/9
assert s.simplify(27*y_star*y_star-114*y_star+7)==0
assert 0<float(y_star)<1
exact_gap=gap.subs(y,y_star)
assert abs(float(exact_gap)-0.0064661038398026)<1e-15
family2=x*x*(1+2*u*(1-y)-u*u*(1-y)*(3+y))
assert s.simplify(family2.subs(u,1/(3+y))-4*x*x/(3+y))==0
assert s.simplify(s.diff(1+u*(1-2*u)*(1-y),u).subs(u,s.Rational(1,4)))==0
L0=np.array([.5,0,np.sqrt(3)/2,0]); L1=np.array([0,np.sqrt(3)/2,0,.5])
E0=np.array([-np.sqrt(3)/2,0,.5,0]); E1=np.array([0,-.5,0,np.sqrt(3)/2])
V=np.array([L0,L1]).T
m=np.array([-1.5,-.5,.5,1.5]); gaps=m[:,None]-m[None,:]
f=lambda v: np.sqrt(21*np.exp(-v)-6*np.exp(-5*v)+np.exp(-9*v))/4
rfun=lambda v:(9*np.exp(-v/2)-np.exp(-9*v/2))/8
rows=[]
for v in [0,.0001,.01,.1,.25,.5,1,2,5,20]:
 t=np.arctan(np.sqrt(3)*(1-np.exp(-4*v))/(9-np.exp(-4*v)))
 K0=np.array([L0,np.cos(t)*L1-np.sin(t)*E1])
 K1=np.array([E0,np.sin(t)*L1+np.cos(t)*E1])
 assert np.max(abs(K0.T@K0+K1.T@K1-np.eye(4)))<1e-14
 deco=np.exp(-v*gaps*gaps/2)
 fe=0
 for i in range(2):
  for j in range(2):
   rho=np.outer(V[:,i],V[:,j])*deco
   rec=K0@rho@K0.T+K1@rho@K1.T
   fe+=rec[i,j]/4
 assert abs(fe-(1+f(v))/2)<1e-14
 rows.append(dict(v=v,coherence_opt=f(v),coherence_ideal=rfun(v),coherence_physical=np.exp(-v/2),angle=t,Fe_opt=fe,Fe_gain_over_ideal=(f(v)-rfun(v))/2,no_noise_Fe_loss=(1-np.cos(t))/2))
maxima={}
for name,g in [('Fe_opt_minus_ideal',lambda v:(f(v)-rfun(v))/2),('Fe_opt_minus_physical',lambda v:(f(v)-np.exp(-v/2))/2),('Fe_ideal_minus_physical',lambda v:(rfun(v)-np.exp(-v/2))/2)]:
 o=minimize_scalar(lambda v:-g(v),bounds=(0,15),method='bounded',options={'xatol':1e-13})
 maxima[name]=dict(v=o.x,gain=g(o.x))
result=dict(symbolic_checks='PASS',exact_gap_maximizer_y=str(y_star),exact_gap_maximum=str(exact_gap),exact_gap_maximum_numeric=float(exact_gap),kraus_and_channel_checks='PASS',cross_syndrome=str(M),maxima_numerical_not_symbolic_certificates=maxima,rows=rows)
Path(__file__).with_name('checks.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
