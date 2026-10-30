"""Receive an eight-mode actual Hessian heat counterexample over Q.

psi=-cos x+eps sin(x)^6 cos y. Ordinary heat increases the
polyconvex det(Hess psi)^2 energy for an explicit rational eps.
"""
from pathlib import Path
from fractions import Fraction as R
from collections import defaultdict
import json,time
root=Path(__file__).resolve().parent;start=time.perf_counter()
def add(*ps):
 out=defaultdict(R)
 for P in ps:
  for k,v in P.items():out[k]+=v
 return {k:v for k,v in out.items() if v}
def mul(P,Q):
 out=defaultdict(R)
 for (i,j,n),v in P.items():
  for (a,b,m),w in Q.items():out[i+a,j+b,n+m]+=v*w
 return {k:v for k,v in out.items() if v}
def sc(P,a):return {k:v*a for k,v in P.items() if v*a}
def mean(P):return {n:v for (i,j,n),v in P.items() if i==j==0}
def heat(P):return {k:-R(k[0]**2+k[1]**2)*v for k,v in P.items() if k[0] or k[1]}
psi={}
def cos(k,co,ep=0):return {(k[0],k[1],ep):co/2,(-k[0],-k[1],ep):co/2}
psi=add(cos((1,0),R(-1)),cos((0,1),R(10,32),1),*(cos((a,b),co/2,1) for a,co in ((2,R(-15,32)),(4,R(6,32)),(6,R(-1,32))) for b in (-1,1)))
# Mixed derivative is -kx*ky on every Fourier coefficient.
A=[{k:-R(k[0]**2)*v for k,v in psi.items() if k[0]},{k:-R(k[0]*k[1])*v for k,v in psi.items() if k[0]*k[1]},{k:-R(k[1]**2)*v for k,v in psi.items() if k[1]}];At=list(map(heat,A));det=add(mul(A[0],A[2]),sc(mul(A[1],A[1]),-1));dt=add(mul(At[0],A[2]),mul(A[0],At[2]),sc(mul(A[1],At[1]),-2));E=mean(mul(det,det));dE=mean(sc(mul(det,dt),2));assert set(dE)=={2,4} and dE[2]==R(3,1024)
eps=R(1,1000);value=sum(v*eps**k for k,v in dE.items());assert value>0
out={'actual_potential':'-cos(x)+epsilon*sin(x)^6*cos(y)','nonzero_real_Fourier_modes':8,'epsilon':str(eps),'determinant_energy_polynomial':{str(k):str(v) for k,v in sorted(E.items())},'ordinary_heat_energy_derivative_polynomial':{str(k):str(v) for k,v in sorted(dE.items())},'strict_positive_heat_energy_derivative':str(value),'polyconvex_energy':'det(A)^2','quasiconvexity_failure':False,'seconds':time.perf_counter()-start,'scope':'Exact actual smooth periodic scalar Hessian. Rules out ordinary-heat monotonicity even for this known polyconvex density; it does not obstruct QC or attainable capacity.'};(root/'heat_failure.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
