"""Finite weighted four-variable dual proposal; exact gap governs acceptance.
Not a uniform convergence or running-time theorem. Versions1--3 untouched.
"""
from certified_projection_v3 import *
from certified_projection_v3 import project_certified as _v3

def _cert(Y,mult,E,L,xi,bits,route,it=0):
 w=[F(1,k) for k in mult];prec=max(192,max(mult).bit_length()+128)
 assert all(psd_exact(e) for e in E) and [sum(e[j] for e in E) for j in range(4)]==[1,0,0,0]
 primal=objective(E,Y,w);dual=dual_lower(L,Y,w,prec);gap=primal-dual;assert gap>=0
 return E,{'proposal':route,'iterations':it,'primal':str(primal),'dual_lower':str(dual),'gap':str(gap),'gap_float':float(gap),'xi':str(xi),'certified':gap<=xi,'interval_bits':prec,'round_bits':bits,'input_Y':[[str(x) for x in y] for y in Y],'multiplicities':[str(k) for k in mult],'output_E':[[str(x) for x in e] for e in E],'dual_L':[str(x) for x in L]}

def finite_dual_proposal(Y,mult,maxiter=200):
 # f(L)=Tr L + sum k ||(Y_i-k L/2)_+||_F^2/k,
 # gradient = I-sum E_i in matrix inner product.
 ym=np.array([matrix(y) for y in Y]);ks=np.array(mult,float)
 def evaluate(v,hessian=False):
  a=ym-ks[:,None,None]*matrix(v)/2
  eig,U=np.linalg.eigh(a);pos=np.maximum(eig,0)
  E=(U*pos[...,None,:])@U.conj().swapaxes(-1,-2)
  f=2*v[0]+sum(np.sum(pos**2,axis=1)/ks)
  g=2*(np.array([1.,0,0,0])-coeff(E.sum(0)))
  if not hessian:return f,g,E
  H=np.zeros((4,4))
  for k,ev,u in zip(ks,eig,U):
   divided=np.empty((2,2))
   for i in range(2):
    for j in range(2):
     divided[i,j]=((max(ev[i],0)-max(ev[j],0))/(ev[i]-ev[j]) if abs(ev[i]-ev[j])>1e-14 else (1. if ev[i]>0 else 0.))
   for j,P in enumerate(PA):
    de=u@(divided*(u.conj().T@P@u))@u.conj().T
    H[:,j]+=k*coeff(de)
  return f,g,E,H
 v=np.zeros(4)
 for it in range(maxiter):
  f,g,E,H=evaluate(v,True)
  if np.linalg.norm(g)<1e-12:break
  step=np.linalg.lstsq(H+1e-12*np.eye(4),-g,rcond=None)[0]
  if g@step>=0:step=-g/max(1,np.linalg.norm(g))
  t=1.
  for _ in range(70):
   trial=v+t*step;fnew,_,_=evaluate(trial)
   if fnew<=f+1e-4*t*(g@step):break
   t/=2
  v=trial
 return evaluate(v)[2],v,it+1

def project_certified(Y,mult,xi=F(1,10**9),bits=96):
 assert len(Y)==len(mult)>0 and all(isinstance(k,int) and k>0 for k in mult)
 # Solve the unconstrained equality projection exactly; if every block is
 # positive this is already the cone-constrained optimum, for any size K.
 residual=sub([sum(y[j] for y in Y) for j in range(4)],[F(1),F(0),F(0),F(0)])
 L=scale(F(2,sum(mult)),residual)
 E=[sub(y,scale(F(k,2),L)) for y,k in zip(Y,mult)]
 if all(psd_exact(e) for e in E):
  out,c=_cert(Y,mult,E,L,xi,bits,'exact_all_positive_affine')
  if c['certified']:return out,c
 # Limiting seen-only candidate is allowed even at moderate K. Its actual
 # finite weighted objective/dual is always checked, never omitted.
 if len(Y)>1 and mult[-1]>1024 and all(k==1 for k in mult[:-1]):
  cand,ld,it=propose_large(Y,mult);E=repair(cand,bits);L=[dyadic(x,bits) for x in ld]
  _,u=sqrt_interval(dot(L[1:],L[1:]),bits+32);L[0]+=max(F(0),u-L[0])
  out,c=_cert(Y,mult,E,L,xi,bits,'seen_limit_finite_gap_checked',it)
  if c['certified']:return out,c
 if max(mult)<=2**40:
  cand,ld,it=finite_dual_proposal(Y,mult);E=repair(cand,bits);L=[dyadic(x,bits) for x in ld]
  out,c=_cert(Y,mult,E,L,xi,bits,'finite_weighted_semismooth_dual',it)
  if c['certified']:return out,c
 return _v3(Y,mult,xi,bits)
