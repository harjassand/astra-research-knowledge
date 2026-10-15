"""Continuous profile geometry with exact convex free-time minimization per edge.
Numerical discovery only. Background unrestricted. y integration and Gauss time
integration are dealiased at representation level; floating errors remain.
"""
import os,math,json
os.environ['OMP_NUM_THREADS']='1'
import numpy as np,torch
from numpy.polynomial.legendre import leggauss
torch.set_default_dtype(torch.float64);torch.set_num_threads(1)
def F(v,w):
 u=v.abs()**2;z=w.abs()**2;q=(v.conj()*w).imag
 return 3*(u+z-2*q)**2+35/24*u*u+q*q-2.5*q*u
class Cycle:
 def __init__(self,N,K):
  self.N=N;self.K=K;self.ns=torch.arange(-N,N+1)
  yy=torch.arange(4*N+1)*2*math.pi/(4*N+1)
  self.basis=torch.exp(1j*self.ns[:,None]*yy)
  t,w=leggauss(3);self.t=torch.tensor((t+1)/2);self.w=torch.tensor(w/2)
  self.s=torch.tensor([-2.,-1.,0.,1.,2.]);self.Vinv=torch.linalg.inv(torch.stack([self.s**i for i in range(5)],1))
 def field(self,par):
  c=torch.view_as_complex(par.contiguous())
  c=c-c.mean(0,keepdim=True)*(self.ns==0)
  # set shape scale independently of background and timings
  scale=torch.sqrt(((1+self.ns.abs())**2*c.abs()**2).mean()+1e-20)
  c=c/scale
  u=c@self.basis;uy=(c*(1j*self.ns))@self.basis
  du=u.roll(-1,0)-u
  q=uy[:,None,:]*(1-self.t[None,:,None])+uy.roll(-1,0)[:,None,:]*self.t[None,:,None]
  return du,q,c
 def coeffs(self,du,q,B):
  a=torch.complex(B[0],B[2]);b=torch.complex(B[1],B[3])
  vals=(F(a+self.s[:,None,None,None]*du[None,:,None,:],b+q[None,:,:,:])-F(a,b)).mean(-1)
  vals=(vals*self.w[None,None,:]).sum(-1)
  return self.Vinv@vals
 def timings(self,coef):
  a0,a1,a2,a3,a4=coef
  with torch.no_grad():
   A=a0.clamp_min(1e-16);E=a4.clamp_min(1e-16)
   center=(3*E/A)**.25
   lo=center*1e-8;hi=center*1e8
   for _ in range(80):
    mid=torch.sqrt(lo*hi);g=A-a2/mid**2-2*a3/mid**3-3*E/mid**4
    lo=torch.where(g<0,mid,lo);hi=torch.where(g>=0,mid,hi)
   tau=(lo+hi)/2
  # implicit derivative through unique duration minimizer; forward Newton residual tiny
  gp=2*a2/tau**3+6*a3/tau**4+12*a4/tau**5
  g=a0-a2/tau**2-2*a3/tau**3-3*a4/tau**4
  return tau-g/gp.clamp_min(1e-16)
 def value(self,par,B):
  du,q,c=self.field(par);co=self.coeffs(du,q,B);tau=self.timings(co)
  act=co[0]*tau+co[1]+co[2]/tau+co[3]/tau**2+co[4]/tau**3
  v=du[:,None,:]/tau[:,None,None]
  n4=(((v.abs()**2+q.abs()**2)**2).mean(-1)*self.w[None,:]).sum(-1)*tau
  return act.sum()/n4.sum(),dict(tau=tau,action=act,n4=n4,coeffs=co,c=c)

def run(N,K,seed,steps=1000):
 torch.manual_seed(seed);obj=Cycle(N,K)
 par=torch.randn(K,2*N+1,2,requires_grad=True)
 if seed==0 and K>=3:
  with torch.no_grad():
   par*=.1
   # start from a closed cycle traversing the known negative opposite-carrier edge
   for j,(r,s) in enumerate([(1.25,2),(2,1.25),(1.25,1.25)]):
    par[j,N+1,0]=r;par[j,N-1,0]=s
 B=torch.randn(4,requires_grad=True)*.03;B=B.detach().requires_grad_(True)
 opt=torch.optim.Adam([par,B],lr=.02)
 best=None;bad=0
 for it in range(steps):
  opt.zero_grad();loss,d=obj.value(par,B)
  if not torch.isfinite(loss) or torch.any(d['tau']<=0):bad+=1;break
  val=loss.item()
  if best is None or val<best['ratio']:
   best=dict(N=N,K=K,seed=seed,iteration=it,ratio=val,raw_nodes=par.detach().tolist(),B=B.detach().tolist(),nodes=torch.view_as_real(d['c']).detach().tolist(),tau=d['tau'].detach().tolist(),actions=d['action'].detach().tolist(),n4=d['n4'].detach().tolist(),a0=d['coeffs'][0].detach().tolist(),a4=d['coeffs'][4].detach().tolist())
  loss.backward();torch.nn.utils.clip_grad_norm_([par,B],20);opt.step()
 # retained values match pre-update nodes exactly
 best['bad_steps']=bad
 return best
if __name__=='__main__':
 import argparse
 ap=argparse.ArgumentParser();ap.add_argument('--N',type=int,default=3);ap.add_argument('--K',type=int,default=5);ap.add_argument('--steps',type=int,default=1000);ap.add_argument('--seeds',type=int,default=3);a=ap.parse_args()
 out=[];path=f'/mnt/data/ASTRA_Universal_Compensation/exploration/free_cycles_N{a.N}_K{a.K}.json'
 for seed in range(a.seeds):
  r=run(a.N,a.K,seed,a.steps);out.append(r);json.dump(out,open(path,'w'),indent=2)
  print(a.N,a.K,seed,r['ratio'],r['tau'],r['bad_steps'],flush=True)
