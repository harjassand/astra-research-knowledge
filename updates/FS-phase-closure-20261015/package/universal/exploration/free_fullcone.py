"""Alternating compatible free-time cycles and an acoustic-SDP cone solve.
All outputs are exploratory. No numerical matrix is asserted an exact certificate.
"""
import json,math,numpy as np,torch
import free_time_cycles as fc
from fullcone_poisson import mon
from acoustic_barrier import solve,matrix,tr

def run(N=3,K=5,seed=0,rounds=4,steps=800):
 torch.manual_seed(seed);obj=fc.Cycle(N,K)
 par=torch.randn(K,2*N+1,2,requires_grad=True)
 B=(.05*torch.randn(4)).requires_grad_(True)
 coeff=np.array([107/24,3,19,-13,0,0,-14.5,-12,0.]);xx=np.r_[coeff,[11,91/6,0,0,11,41/3]];xx/=tr@xx
 hist=[];ncoef=np.array([1,1,2,0,0,0,0,0,0.]);eps=.0002
 for rd in range(rounds):
  pc=torch.tensor(xx[:9]);fc.F=lambda v,w: (mon(v,w)*pc).sum(-1)
  opt=torch.optim.Adam([par,B],lr=.025)
  best=None
  for it in range(steps):
   opt.zero_grad();loss,dat=obj.value(par,B)
   if not torch.isfinite(loss) or (dat['tau']<=0).any():break
   loss.backward();torch.nn.utils.clip_grad_norm_([par,B],20);opt.step()
  loss,dat=obj.value(par,B);du,q,c=obj.field(par);tau=dat['tau'].detach()
  with torch.no_grad():
   vv=du[:,None,:]/tau[:,None,None];bc1=torch.complex(B[0],B[2]);bc2=torch.complex(B[1],B[3])
   moms=(mon(bc1+vv,bc2+q)-mon(bc1,bc2)).mean(-2)
   d=((moms*obj.w[None,:,None]).sum(1)*tau[:,None]).sum(0)/dat['n4'].sum()
  newx,minval,eig=solve(d.numpy())
  # strict convex positive padding has explicit acoustic certificate
  nx=np.array([1,1,2,0,0,0,0,0,0,1,0,0,0,0,0.])
  xx=(1-48*eps)*newx+eps*nx
  val=float(d.numpy()@xx[:9])
  h=dict(round=rd,N=N,K=K,seed=seed,ratio_before=float(loss),ratio_after_cone=val,min_eig=float(np.linalg.eigvalsh(matrix(xx))[0]),coefficients=xx.tolist(),nodes=torch.view_as_real(c).detach().tolist(),raw_nodes=par.detach().tolist(),B=B.detach().tolist(),tau=tau.tolist(),n4=float(dat['n4'].sum()))
  hist.append(h);print(seed,rd,h['ratio_before'],val,h['min_eig'],flush=True)
  json.dump(hist,open(f'/mnt/data/ASTRA_Universal_Compensation/exploration/fullcone_cycles_N{N}_K{K}_s{seed}.json','w'),indent=2)
 return hist
if __name__=='__main__':
 import argparse
 a=argparse.ArgumentParser();a.add_argument('--N',type=int,default=3);a.add_argument('--K',type=int,default=5);a.add_argument('--seed',type=int,default=0);a.add_argument('--rounds',type=int,default=4);a.add_argument('--steps',type=int,default=800);a=a.parse_args()
 run(a.N,a.K,a.seed,a.rounds,a.steps)
