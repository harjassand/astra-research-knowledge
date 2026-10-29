"""High precision finite qubit-dual proposal for cancellation-limited faces.
Exact certificates, not Newton convergence, remain the acceptance rule.
"""
import mpmath as mp
import certified_projection_v4 as v4
from certified_projection_v4 import *

def positive_coeff(v):
 a=v[0];r=mp.sqrt(sum(x*x for x in v[1:]));J=mp.zeros(4)
 if a-r>=0:return mp.matrix(v),mp.eye(4)
 if a+r<=0:return mp.zeros(4,1),J
 u=mp.matrix(v[1:]);E=mp.matrix([(a+r)/2]+[(1+a/r)*x/2 for x in u]);J[0,0]=mp.mpf('.5')
 for i in range(3):
  J[0,i+1]=J[i+1,0]=u[i]/(2*r)
  for j in range(3):J[i+1,j+1]=(1+a/r)/2*(i==j)-a*u[i]*u[j]/(2*r**3)
 return E,J

def high_propose(Y,mult,dps=100,maxiter=200):
 with mp.workdps(dps):
  ym=[mp.matrix([mp.mpf(x.numerator)/x.denominator for x in y]) for y in Y]
  unit=mp.matrix([1,0,0,0]);ks=list(mult)
  def fg(L,hessian=False):
   Es=[];H=mp.zeros(4);f=2*L[0]
   for y,k in zip(ym,ks):
    E,J=positive_coeff(list(y-L*(mp.mpf(k)/2)));Es.append(E);H+=k*J
    f+=2*sum(x*x for x in E)/k
   g=2*(unit-sum(Es,mp.zeros(4,1)))
   return f,g,Es,H
  # Start from the double proposal, but recompute all effects at high precision.
  _,ld,_=v4.finite_dual_proposal(Y,mult)
  L=mp.matrix([mp.mpf(float(x)) for x in ld])
  for it in range(maxiter):
   f,g,Es,H=fg(L)
   if mp.norm(g)<mp.mpf('1e-60'):break
   try:step=mp.lu_solve(H+mp.mpf('1e-80')*mp.eye(4),-g)
   except ZeroDivisionError:step=-g
   descent=sum(a*b for a,b in zip(g,step))
   if descent>=0:step=-g;descent=-sum(x*x for x in g)
   t=mp.mpf(1)
   for _ in range(200):
    trial=L+t*step
    if fg(trial)[0]<=f+mp.mpf('0.0001')*t*descent:break
    t/=2
   L=trial
  _,g,Es,_=fg(L)
  candidate=np.array([matrix([F(str(x)) for x in E]) for E in Es])
  # Preserve high-precision multiplier; do not first convert through float.
  ld=[F(str(x)) for x in L]
  return candidate,ld,it+1,str(mp.norm(g))

def project_certified(Y,mult,xi=F(1,10**9),bits=96):
 try:return v4.project_certified(Y,mult,xi,bits)
 except RuntimeError as original:
  if max(mult)>2**40:raise original
  cand,L,it,residual=high_propose(Y,mult)
  E=repair(cand,bits)
  # F(str(mp)) has finite decimal denominators and is exactly checked.
  E,c=v4._cert(Y,mult,E,L,xi,bits,'high_precision_finite_dual',it)
  c['high_precision_gradient_residual']=residual
  if not c['certified']:raise RuntimeError('HIGH_PRECISION_UNCERTIFIED gap='+c['gap'])
  return E,c
