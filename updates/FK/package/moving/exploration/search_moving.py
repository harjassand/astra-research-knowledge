#!/usr/bin/env python3
"""Exploratory compatible Fourier search, not a proof.
The physical periodic cell is allowed to deform by a constant invertible input map.
All reported gaps are directly reevaluated at the saved affine background.
"""
import json, math, time
from pathlib import Path
import numpy as np
import sympy as sp
import torch

torch.set_num_threads(1)
torch.set_default_dtype(torch.float64)
root=Path(__file__).resolve().parent
xx=sp.symbols('a b c d',real=True);a,b,c,d=xx
u=a*a+c*c;v=b*b+d*d;q=a*d-b*c
F=3*(u+v-2*q)**2+sp.Rational(35,24)*u*u+q*q-sp.Rational(5,2)*q*u
T=np.zeros((4,4,4,4))
for idx in np.ndindex(T.shape):
 T[idx]=float(sp.diff(F,*[xx[j] for j in idx])/24)
T=torch.tensor(T)
K=3;n=4*K+1
ks=np.array([(p,r) for p in range(-K,K+1) for r in range(-K,K+1) if (p>0 or (p==0 and r>0))],float)
grid=np.array([(x,y) for x in range(n) for y in range(n)],float)*2*math.pi/n
phase=grid@ks.T
basis=np.empty((n*n,2*len(ks),2))
basis[:,0::2,:]=-np.sin(phase)[:,:,None]*ks[None,:,:]
basis[:,1::2,:]=np.cos(phase)[:,:,None]*ks[None,:,:]
basis=torch.tensor(basis)

def calc(coef,geom):
 X0=torch.einsum('mo,nmi->noi',coef,basis)
 al=4*torch.tanh(geom[0]/4); sh=3*torch.tanh(geom[1]/3)
 S=torch.stack([torch.stack([torch.exp(al),sh]),torch.stack([al*0,torch.exp(-al)])])
 X=X0@S
 vv=X.reshape(-1,4)
 m4=torch.mean(torch.sum(vv*vv,dim=1)**2)
 vv=vv/m4.pow(.25)
 aa,bb,cc,dd=vv.unbind(1)
 uu=aa*aa+cc*cc;ww=bb*bb+dd*dd;qq=aa*dd-bb*cc
 cval=(3*(uu+ww-2*qq)**2+(35/24)*uu*uu+qq*qq-2.5*qq*uu).mean()
 C2=vv.T@vv/len(vv)
 C3=torch.einsum('ni,nj,nk->ijk',vv,vv,vv)/len(vv)
 H=12*torch.einsum('ijkl,kl->ij',T,C2)
 bvec=4*torch.einsum('ijkl,jkl->i',T,C3)
 B=-torch.linalg.solve(H+1e-9*torch.eye(4),bvec)
 gap=cval+torch.dot(bvec,B)+.5*torch.dot(B,H@B)
 return gap, H, B, S, m4

records=[];bestall=None
for seed in [17,29,43,71,103,137]:
 torch.manual_seed(seed)
 coef=torch.nn.Parameter(.2*torch.randn(len(ks)*2,2))
 initial_a=0.0 if seed in [17,29] else (-2.5 if seed in [43,71] else 2.5)
 geom=torch.nn.Parameter(torch.tensor([initial_a,0.0]))
 opt=torch.optim.Adam([coef,geom],lr=.025)
 best=float('inf'); snap=None
 for step in range(600):
  opt.zero_grad();gap,H,B,S,m4=calc(coef,geom)
  if not torch.isfinite(gap):break
  vgap=float(gap.detach())
  if vgap<best:
   best=vgap
   snap={'seed':seed,'step':step,'gap':best,'coefficients':coef.detach().numpy().tolist(),'geometry_parameters':geom.detach().numpy().tolist(),'input_transform':S.detach().numpy().tolist(),'affine_background':B.detach().numpy().tolist(),'hessian_eigenvalues':torch.linalg.eigvalsh(H.detach()).numpy().tolist(),'unnormalized_fourth_moment':float(m4.detach())}
  gap.backward();torch.nn.utils.clip_grad_norm_([coef,geom],100);opt.step()
 with torch.no_grad():
  savedcoef=torch.tensor(snap['coefficients']);savedgeom=torch.tensor(snap['geometry_parameters'])
  reevaluated,*_=calc(savedcoef,savedgeom)
  snap['reevaluated_gap']=float(reevaluated)
 records.append({key:snap[key] for key in ['seed','step','gap','reevaluated_gap','hessian_eigenvalues','input_transform']})
 print(json.dumps(records[-1]),flush=True)
 if bestall is None or best<bestall['gap']:bestall=snap
(root/'moving_search.json').write_text(json.dumps({'cutoff':K,'grid':n,'steps_per_start':600,'starts':records,'best':bestall,'frequencies':ks.tolist(),'status':'FLOATING LOCAL SEARCH ONLY; NOT A LOWER BOUND OR QUASICONVEXITY CERTIFICATE'},indent=2)+'\n')
