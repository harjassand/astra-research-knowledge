"""Exact-rational certificate around floating weighted Dykstra proposal.
A qubit Hermitian matrix is represented by (a,x,y,z), H=aI+xX+yY+zZ.
"""
from fractions import Fraction as F
from math import isqrt
import numpy as np
from scipy.optimize import minimize, root
I=np.eye(2,dtype=complex)
PA=np.array([I,[[0,1],[1,0]],[[0,-1j],[1j,0]],[[1,0],[0,-1]]],complex)
def coeff(a):return np.einsum('kij,ji->k',PA,a).real/2
def matrix(v):return np.einsum('k,kij->ij',[float(x) for x in v],PA)
def dot(a,b):return sum((x*y for x,y in zip(a,b)),F(0))
def add(a,b):return [x+y for x,y in zip(a,b)]
def sub(a,b):return [x-y for x,y in zip(a,b)]
def scale(c,a):return [c*x for x in a]
def sqrt_interval(x,bits=160):
 assert x>=0
 D=1<<bits;n=isqrt((x.numerator*D*D)//x.denominator)
 lo=F(n,D);hi=lo if lo*lo==x else F(n+1,D)
 assert lo*lo<=x<=hi*hi
 return lo,hi
def psd_exact(v):return v[0]>=0 and v[0]*v[0]>=dot(v[1:],v[1:])
def dyadic(x,bits=96):return F(round(float(x)*(1<<bits)),1<<bits)
def repair(candidate,bits=96):
 # Round, add individual spectral upper-bound shifts, scale below I,
 # then place the exact positive residual in the final aggregate.
 H=[]
 for a in candidate:
  v=[dyadic(z,bits) for z in coeff(a)]
  _,u=sqrt_interval(dot(v[1:],v[1:]),bits+32)
  v[0]+=max(F(0),u-v[0]);assert psd_exact(v);H.append(v)
 S=[sum((h[j] for h in H),F(0)) for j in range(4)]
 _,u=sqrt_interval(dot(S[1:],S[1:]),bits+32)
 c=max(F(1),S[0]+u)
 E=[scale(1/c,h) for h in H]
 rem=sub([F(1),F(0),F(0),F(0)],scale(1/c,S));assert psd_exact(rem)
 E[-1]=add(E[-1],rem)
 assert all(psd_exact(e) for e in E)
 assert [sum(e[j] for e in E) for j in range(4)]==[1,0,0,0]
 return E

def objective(E,Y,w):return sum((2*wi*dot(sub(e,y),sub(e,y)) for e,y,wi in zip(E,Y,w)),F(0))
def dual_lower(L,Y,w,bits=192):
 value=-2*L[0]+sum((2*wi*dot(y,y) for wi,y in zip(w,Y)),F(0))
 for wi,y in zip(w,Y):
  v=sub(scale(2*wi,y),L)
  lo,hi=sqrt_interval(dot(v[1:],v[1:]),bits)
  eig_upper=[v[0]+hi,v[0]-lo]
  pos_sq=sum((max(F(0),z)**2 for z in eig_upper),F(0))
  value-=pos_sq/(4*wi)
 return value

def propose(Y,mult,tol=2e-14,maxiter=30000):
 # Per-label coordinates; metric mult_i ||x_i-y_i||^2.
 y=np.array([matrix(scale(F(1,int(k)),v)) for v,k in zip(Y,mult)])
 x=y.copy();p=np.zeros_like(x);q=p.copy();A=sum(mult)
 for it in range(maxiter):
  v=x+p;ev,U=np.linalg.eigh(v);z=(U*np.maximum(ev,0)[...,None,:])@U.conj().swapaxes(-1,-2);p=v-z
  u=z+q;v=u+(I-np.einsum('i,ijk->jk',np.array(mult,float),u))/float(A);q=u-v
  change=float(np.max(abs(v-x)));x=v
  if change<tol:break
 return np.array([float(k)*a for k,a in zip(mult,x)]),2*coeff(q[0]),it+1

def propose_large(Y,mult):
 # The unseen objective is negligible but NOT omitted from certificate.
 # Optimize the limiting seen-only dual over Lambda>=0; this is merely
 # a candidate factory, never the proof of acceptance.
 assert mult[-1]>1 and all(k==1 for k in mult[:-1])
 seen=np.array([matrix(y) for y in Y[:-1]])
 def fg(v):
  L=matrix(v);ev,U=np.linalg.eigh(seen-L/2)
  E=(U*np.maximum(ev,0)[...,None,:])@U.conj().swapaxes(-1,-2)
  val=2*v[0]+np.sum(np.maximum(ev,0)**2)
  grad=2*(np.array([1,0,0,0])-coeff(E.sum(0)))
  return val,grad
 opt=minimize(lambda v:fg(v),[.1,0,0,0],jac=True,method='SLSQP',constraints=[{'type':'ineq','fun':lambda v:v[0]-np.linalg.norm(v[1:])}],options={'ftol':1e-14,'maxiter':2000})
 # On an interior dual face, solve the stationarity equation directly;
 # no root status is trusted without the exact certificate downstream.
 polish=root(lambda v:fg(v)[1],opt.x,tol=1e-11)
 if polish.x[0]>=np.linalg.norm(polish.x[1:]) and np.linalg.norm(fg(polish.x)[1])<np.linalg.norm(fg(opt.x)[1]):
  opt.x=polish.x
 L=matrix(opt.x);ev,U=np.linalg.eigh(seen-L/2)
 E=(U*np.maximum(ev,0)[...,None,:])@U.conj().swapaxes(-1,-2)
 return np.concatenate([E,(I-E.sum(0))[None,:,:]]),opt.x,opt.nit


def project_certified(Y,mult,xi=F(1,10**9),bits=96):
 w=[F(1,int(k)) for k in mult]
 if len(Y)==1:
  # A one-effect POVM has a unique feasible point, for any multiplicity.
  E=[[F(1),F(0),F(0),F(0)]]
  L=scale(2*w[0],sub(Y[0],E[0]))
  primal=objective(E,Y,w);dual=dual_lower(L,Y,w,max(192,max(mult).bit_length()+128))
  gap=primal-dual
  rec={'iterations':0,'primal':str(primal),'dual_lower':str(dual),'gap':str(gap),'gap_float':float(gap),'xi':str(xi),'certified':gap<=xi,'interval_bits':max(192,max(mult).bit_length()+128),'round_bits':bits,'proposal':'unique_single_effect','input_Y':[[str(x) for x in y] for y in Y],'multiplicities':[str(k) for k in mult],'output_E':[[str(x) for x in e] for e in E],'dual_L':[str(x) for x in L]}
  assert 0<=gap<=xi
  return E,rec
 route='weighted_dykstra' if max(mult)<=10**12 else 'limiting_seen_dual'
 cand,ld,it=propose(Y,mult) if route=='weighted_dykstra' else propose_large(Y,mult)
 E=repair(cand,bits)
 L=[dyadic(x,bits) for x in ld]
 # For enormous unseen multiplicity, forbid tiny negative dual eigenspaces
 # that could be amplified by 1/w. This is only a proposal modification;
 # the resulting loss is fully included in the exact certified dual gap.
 if max(mult)>10**12:
  _,u=sqrt_interval(dot(L[1:],L[1:]),bits+32);L[0]+=max(F(0),u-L[0])
 prec=max(192,max(mult).bit_length()+128)
 primal=objective(E,Y,w);dual=dual_lower(L,Y,w,prec);gap=primal-dual
 assert gap>=0
 rec={'proposal':route,'iterations':it,'primal':str(primal),'dual_lower':str(dual),'gap':str(gap),'gap_float':float(gap),'xi':str(xi),'certified':gap<=xi,'interval_bits':prec,'round_bits':bits,
      'input_Y':[[str(x) for x in y] for y in Y],'multiplicities':[str(k) for k in mult], 'output_E':[[str(x) for x in e] for e in E], 'dual_L':[str(x) for x in L]}
 if gap>xi:raise RuntimeError('UNCERTIFIED projection gap='+str(float(gap))+' > '+str(float(xi)))
 return E,rec
