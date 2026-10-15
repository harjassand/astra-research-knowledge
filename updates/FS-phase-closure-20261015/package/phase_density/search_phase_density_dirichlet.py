"""Competing compatible Dirichlet search with two convex scalar blocks.
All energies here use numerical Gauss quadrature and are exploratory, NOT
negative-witness certificates. Sine coefficients enforce the exact boundary
condition analytically; an l1 density constraint enforces positivity between
quadrature nodes as well. No previous optimizer states are used.
"""
from pathlib import Path
import json,time
import numpy as np
import torch
from scipy.optimize import minimize,LinearConstraint,Bounds
from numpy.polynomial.legendre import leggauss
torch.set_num_threads(1);torch.set_default_dtype(torch.float64)
ROOT=Path(__file__).resolve().parent
K=3;N=28
z,ww=leggauss(N);g=(z+1)/2;wg=ww/2
xx,yy=np.meshgrid(g,g,indexing='ij');x=xx.ravel();y=yy.ravel();weight=np.outer(wg,wg).ravel()
modes=[(i,j) for i in range(1,K+1) for j in range(1,K+1)]
S=[];Sx=[];Sy=[]
for i,j in modes:
 S.append(np.sin(np.pi*i*x)*np.sin(np.pi*j*y))
 Sx.append(np.pi*i*np.cos(np.pi*i*x)*np.sin(np.pi*j*y))
 Sy.append(np.pi*j*np.sin(np.pi*i*x)*np.cos(np.pi*j*y))
S,Sx,Sy=[torch.tensor(np.array(t).T) for t in (S,Sx,Sy)]
w=torch.tensor(weight);n=len(modes)
def G(a,b,c,d):
 u=a*a+c*c;v=b*b+d*d;q=a*d-b*c
 return 3*(u+v-2*q)**2+(35/24)*u*u+q*q-2.5*q*u

def run(B,seed,scale,cycles=12):
 B=np.array(B,dtype=float);shift=np.array([3+2*np.linalg.norm(B),.3])
 ux=shift[0]+B[0,0]*x+B[0,1]*y;uy=shift[1]+B[1,0]*x+B[1,1]*y
 r2=ux*ux+uy*uy;rho0=r2*r2
 rx0=4*r2*(ux*B[0,0]+uy*B[1,0]);ry0=4*r2*(ux*B[0,1]+uy*B[1,1])
 kx0=(ux*B[1,0]-uy*B[0,0])/r2;ky0=(ux*B[1,1]-uy*B[0,1])/r2
 rho0,rx0,ry0,kx0,ky0=[torch.tensor(t) for t in (rho0,rx0,ry0,kx0,ky0)]
 fb=float(G(*B.ravel()));rng=np.random.default_rng(seed)
 ac=np.zeros(n);tc=rng.normal(size=n)*scale/np.array([i*i+j*j for i,j in modes]);ledger=[]
 def energy(a,t,ret=False):
  fac=1+S@a;rho=rho0*fac
  ax=(rx0*fac+rho0*(Sx@a))/(4*rho);ay=(ry0*fac+rho0*(Sy@a))/(4*rho)
  kx=kx0+Sx@t;ky=ky0+Sy@t
  vals=rho*G(ax,ay,kx,ky)
  return torch.dot(w,vals)-fb
 def f_a(z,t):
  zz=torch.tensor(z,requires_grad=True);tt=torch.tensor(t);a=zz[:n]-zz[n:]
  val=energy(a,tt);grad=torch.autograd.grad(val,zz)[0]
  return val.item(),grad.detach().numpy()
 def f_t(t,a):
  tt=torch.tensor(t,requires_grad=True);aa=torch.tensor(a);val=energy(aa,tt)
  grad=torch.autograd.grad(val,tt)[0];return val.item(),grad.detach().numpy()
 start=time.time();init=float(energy(torch.tensor(ac),torch.tensor(tc)))
 for it in range(cycles):
  z0=np.r_[np.maximum(ac,0),np.maximum(-ac,0)]
  ar=minimize(lambda z:f_a(z,tc),z0,jac=True,method='SLSQP',bounds=Bounds(np.zeros(2*n),np.full(2*n,.95)),constraints=LinearConstraint(np.ones((1,2*n)),-np.inf,.95),options={'maxiter':200,'ftol':1e-11})
  az=ar.x[:n]-ar.x[n:]
  # Keep only feasible, non-increasing iterates; failed solves are recorded.
  if np.sum(np.abs(az))<=.95000000001 and f_a(ar.x,tc)[0]<=float(energy(torch.tensor(ac),torch.tensor(tc)))+1e-8:ac=az
  tr=minimize(lambda t:f_t(t,ac),tc,jac=True,method='L-BFGS-B',options={'maxiter':250,'ftol':1e-13,'gtol':1e-8,'maxls':40})
  if tr.fun<=float(energy(torch.tensor(ac),torch.tensor(tc)))+1e-8:tc=tr.x
  en=float(energy(torch.tensor(ac),torch.tensor(tc)))
  ledger.append({'cycle':it,'gap':en,'amplitude_success':bool(ar.success),'phase_success':bool(tr.success),'amplitude_iters':int(ar.nit),'phase_iters':int(tr.nit),'density_l1':float(np.sum(np.abs(ac)))})
  if en< -1e-8 or (it>=4 and abs(ledger[-2]['gap']-en)<1e-11):break
 result={'B':B.tolist(),'target_translation':shift.tolist(),'seed':seed,'initial_phase_scale':scale,'initial_gap':init,'final_gap_quadrature':en,'cycles':ledger,'amplitude_coefficients':ac.tolist(),'phase_coefficients':tc.tolist(),'sine_modes':modes,'quadrature_order':N,'seconds':time.time()-start,'density_relative_lower_bound':1-float(np.sum(np.abs(ac)))}
 print({k:v for k,v in result.items() if k not in ('amplitude_coefficients','phase_coefficients','cycles','sine_modes')},flush=True)
 return result
if __name__=='__main__':
 cases=[([[1,0],[0,1]],11,.15),([[1,0],[0,1]],22,.45),([[1,0],[0,1.5]],31,.25),([[1,.5],[-.3,1]],42,.3),([[0,0],[0,0]],51,.3),([[2,0],[0,.5]],62,.25)]
 out={'scope':'Exploration only; analytic compatibility and density positivity, numerical integration/minimization. Six planned cases; only appended completed cases count.','results':[]}
 for B,seed,scale in cases:
  out['results'].append(run(B,seed,scale));(ROOT/'dirichlet_search.json').write_text(json.dumps(out,indent=2))
