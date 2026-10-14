from pathlib import Path
import numpy as np
import sympy as s
import torch, json, time
from itertools import product
torch.set_num_threads(1);torch.set_default_dtype(torch.float64)
a,b,c,d=s.symbols('a b c d');vs=(a,b,c,d);u=a*a+c*c;v=b*b+d*d;q=a*d-b*c
F=s.expand(3*(u+v-2*q)**2+s.Rational(35,24)*u**2+q*q-s.Rational(5,2)*q*u)
TT=np.empty((4,)*4)
for ids in product(range(4),repeat=4):
 g=F
 for ix in ids:g=s.diff(g,vs[ix])
 TT[ids]=float(g/24)
T=torch.tensor(TT)
K=3;N=13
ks=np.array([(i,j) for i in range(K+1) for j in range(-K,K+1) if i>0 or j>0],float)
xx=np.array(list(product(np.arange(N)*2*np.pi/N,repeat=2)))
phase=xx@ks.T
wave=torch.tensor(np.stack([-np.sin(phase),np.cos(phase)],axis=-1))
kn=torch.tensor(ks/np.linalg.norm(ks,axis=1,keepdims=True))
logs=[]
for seed in range(6):
 torch.manual_seed(seed)
 amps=torch.nn.Parameter(torch.randn(2,len(ks),2)*.1)
 opt=torch.optim.Adam([amps],lr=.035)
 best=None
 def moments():
  g=torch.einsum('pmf,omf,mj->poj',wave,amps,kn).reshape(-1,4)
  norm=torch.mean(torch.sum(g*g,1)**2)**.25;g=g/norm
  C=g.T@g/len(g)
  H=12*torch.einsum('ijkl,kl->ij',T,C)
  bvec=4*torch.einsum('ijkl,pj,pk,pl->i',T,g,g,g)/len(g)
  en=torch.einsum('ijkl,pi,pj,pk,pl->',T,g,g,g,g)/len(g)
  A=-torch.linalg.solve(H+1e-9*torch.eye(4),bvec)
  loss=en+torch.dot(bvec,A)+.5*torch.dot(A,H@A)
  return loss,en,H,bvec,A,g
 for it in range(800):
  opt.zero_grad();loss,*rest=moments()
  if not torch.isfinite(loss): break
  if best is None or loss.item()<best[0]:best=(loss.item(),amps.detach().numpy().copy(),it)
  loss.backward();torch.nn.utils.clip_grad_norm_([amps],20);opt.step()
 with torch.no_grad():
  amps.copy_(torch.tensor(best[1]));loss,en,H,bvec,A,g=moments()
  out={'seed':seed,'iteration':best[2],'gap':loss.item(),'c':en.item(),'H':H.tolist(),'b':bvec.tolist(),'background':A.tolist(),'eigenvalues':torch.linalg.eigvalsh(H).tolist(),'amplitudes':amps.tolist()}
  logs.append(out)
  print(seed,loss.item(),torch.linalg.eigvalsh(H).tolist(),flush=True)
Path(__file__).with_name('tangent_search.json').write_text(json.dumps({'cutoff':K,'grid':N,'steps':800,'wavevectors':ks.tolist(),'runs':logs},indent=2))
