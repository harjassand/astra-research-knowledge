import numpy as np
import torch
from scipy.optimize import minimize, LinearConstraint
import json, time
from pathlib import Path
torch.set_num_threads(1)
torch.set_default_dtype(torch.float64)
ROOT=Path(__file__).resolve().parent
# rho=1+sum cos,sin Fourier modes; all objective evaluations are exploration only.
K=4; N=64
modes=[(i,j) for i in range(0,K+1) for j in range(-K,K+1) if (i>0 or j>0)]
grid=np.arange(N)*2*np.pi/N
xx,yy=np.meshgrid(grid,grid,indexing='ij'); x=xx.ravel(); y=yy.ravel()
bs=[]; bx=[]; by=[]
for i,j in modes:
 z=i*x+j*y
 bs += [np.cos(z),np.sin(z)]
 bx += [-i*np.sin(z),i*np.cos(z)]
 by += [-j*np.sin(z),j*np.cos(z)]
Bs=torch.tensor(np.array(bs).T); Bx=torch.tensor(np.array(bx).T); By=torch.tensor(np.array(by).T)

def GF(a,b,c,d):
 u=a*a+c*c; v=b*b+d*d; q=a*d-b*c
 return 3*(u+v-2*q)**2 + (35/24)*u*u+q*q-2.5*q*u

def run(phase):
 kx=np.zeros_like(x); ky=np.ones_like(y)
 for i,j,A,B in phase:
  z=i*x+j*y
  w=-A*np.sin(z)+B*np.cos(z)
  kx+=i*w; ky+=j*w
 tx=torch.tensor(kx); ty=torch.tensor(ky)
 def fn(z):
  zz=torch.tensor(z,requires_grad=True)
  rho=1+Bs@zz
  a=(Bx@zz)/(4*rho); b=(By@zz)/(4*rho)
  f=(rho*GF(a,b,tx,ty)).mean()
  grad=torch.autograd.grad(f,zz)[0]
  return f.item(),grad.detach().numpy()
 cons=LinearConstraint(Bs.numpy(),-0.97,np.inf)
 t=time.time(); res=minimize(fn,np.zeros(len(bs)),jac=True,method='SLSQP',constraints=cons,
  options={'maxiter':350,'ftol':1e-11,'disp':False})
 return {'phase':phase,'modes':modes,'rho_coefficients':res.x.tolist(),'energy_quadrature':float(res.fun),
 'success':bool(res.success),'message':res.message,'iterations':int(res.nit),'seconds':time.time()-t,
 'min_grid_density':float(np.min(1+Bs.numpy()@res.x)), 'max_grid_density':float(np.max(1+Bs.numpy()@res.x)),
 'coefficient_l1':float(np.sum(np.abs(res.x))),'gradient_norm':float(np.linalg.norm(fn(res.x)[1]))}

phases=[[(1,0,0,0.12),(0,1,0,0.10),(1,1,0,0.08)],
 [(1,0,0,0.30),(0,1,0,0.25),(1,1,0,0.20)],
 [(1,0,0,0.5),(0,1,0,0.35),(1,1,0,0.25),(2,-1,0,0.10)]]
results=[]
for phase in phases[:1]:
 r=run(phase); results.append(r);print({k:v for k,v in r.items() if k not in ('rho_coefficients','modes')},flush=True)
 (ROOT/'density_refined.json').write_text(json.dumps({'scope':'Numerical exploration; no continuum bound follows from collocation.','results':results},indent=2))
