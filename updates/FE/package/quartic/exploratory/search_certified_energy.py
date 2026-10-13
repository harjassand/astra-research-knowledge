"""Floating Fourier stress test of an EXACTLY rank-one-convex rational quartic.
Finite searches do not certify quasiconvexity. Grid has no degree-four aliasing.
"""
import numpy as np, torch, json
from pathlib import Path
torch.set_num_threads(1); torch.set_default_dtype(torch.float64)
OUT=Path(__file__).parent

def energy(X):
 a,b,c,d=X.unbind(-1);u=a*a+c*c;v=b*b+d*d;w=a*b+c*d;q=a*d-b*c
 return u*u+v*v+4*w*w+3.5*q*q-2.9*q*(u+v)

def design(cutoff,N=32):
 k=np.array([(i,j) for i in range(cutoff+1) for j in range(-cutoff,cutoff+1) if (i>0 or j>0)],float)
 pts=np.indices((N,N)).reshape(2,-1).T*2*np.pi/N
 waves=np.concatenate([np.cos(pts@k.T),np.sin(pts@k.T)],axis=1)
 kh=np.tile(k/np.linalg.norm(k,axis=1)[:,None],(2,1))
 D=[]
 for i in range(2):
  for j in range(len(kh)):
   X=np.zeros((N*N,4));X[:,2*i:2*i+2]=waves[:,j,None]*kh[j];D.append(X)
 return torch.tensor(np.stack(D).reshape(len(D),-1)),k

records=[];best=None
for cutoff in [3,5]:
 D,k=design(cutoff,32); torch.manual_seed(100+cutoff)
 B=12; coeff=torch.nn.Parameter(torch.randn(B,D.shape[0])*.2)
 bg=torch.nn.Parameter(torch.randn(B,4)*.5)
 opt=torch.optim.Adam([coeff,bg],lr=.04)
 for it in range(1000):
  X=(coeff@D).reshape(B,-1,4);sc=X.square().sum(-1).square().mean(-1).pow(.25)
  X=X/sc[:,None,None]
  gap=energy(X+bg[:,None,:]).mean(-1)-energy(bg)
  loss=gap.sum();opt.zero_grad();loss.backward();opt.step()
  with torch.no_grad():
   bn=bg.norm(dim=1);bg*=torch.clamp(3/bn,max=1)[:,None]
 if True:
  vals=gap.detach().numpy(); rec={'cutoff':cutoff,'grid':32,'restarts':B,'steps':1000,'min_gap':float(vals.min()),'max_gap':float(vals.max()),'gaps':vals.tolist()}
  records.append(rec);print(json.dumps(rec),flush=True)
  ix=int(vals.argmin())
  if best is None or vals[ix]<best:
   best=vals[ix];np.savez(OUT/'fourier_search_best.npz',coeff=coeff[ix].detach().numpy(),background=bg[ix].detach().numpy(),k=k,cutoff=cutoff,gap=vals[ix])
(OUT/'fourier_search_log.json').write_text(json.dumps(records,indent=2))
