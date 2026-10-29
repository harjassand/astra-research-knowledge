import numpy as np
from scipy.linalg import expm
import json

def matrices(n,edges,g,k):
 states=[s for s in range(1<<n) if all(not((s>>a&1) and (s>>b&1)) for a,b in edges)]
 ix={s:i for i,s in enumerate(states)}; d=len(states); bs=[]
 for x in range(n):
  b=np.zeros((d,d),complex)
  for j,s in enumerate(states):
   if s>>x&1:b[ix[s^(1<<x)],j]=1
  bs.append(b)
 H=g*sum((b+b.T.conj() for b in bs),np.zeros((d,d),complex)); I=np.eye(d)
 # column vectorization Heisenberg generator
 L=1j*(np.kron(I,H)-np.kron(H.T,I))
 for b in bs:
  nn=b.T.conj()@b
  L+=k*(np.kron(b.T,b.T.conj())-.5*np.kron(I,nn)-.5*np.kron(nn.T,I))
 return states,bs,H,L

def run(name,n,edges,g,k,t):
 st,bs,H,L=matrices(n,edges,g,k); d=len(st); I=np.eye(d); x=0;b=bs[x];nn=b.T.conj()@b
 kill=L-k*np.kron(b.T,b.T.conj())
 eff=I-(expm(t*kill)@I.reshape(-1,order='F')).reshape((d,d),order='F')
 eig=np.linalg.eigvalsh((eff+eff.T.conj())/2)
 neighbors=[v if u==x else u for u,v in edges if x in (u,v)]
 G=np.diag([float(all(not(s>>y&1) for y in neighbors)) for s in st]); Q=I-nn
 curv=(L@L@nn.reshape(-1,order='F')).reshape((d,d),order='F')
 residual=np.linalg.norm(Q@curv@Q-2*g*g*G@Q)
 return dict(graph=name,dimension=d,g=g,kappa=k,t=t,event_effect_min=float(eig[0]),event_effect_max=float(eig[-1]),compression_residual=float(residual))
if __name__=='__main__':
 graphs=[('isolated',1,[]),('edge',2,[(0,1)]),('triangle',3,[(0,1),(1,2),(2,0)]),('star4',5,[(0,j) for j in range(1,5)]),('path6',6,[(j,j+1) for j in range(5)]),('cycle5',5,[(j,(j+1)%5) for j in range(5)])]
 out=[run(name,n,e,g,1.,t) for name,n,e in graphs for g,t in [(0.1,1.),(1.,0.2),(1.,1.),(10.,1.)]]
 print(json.dumps(out,indent=2))
 assert max(r['compression_residual'] for r in out)<1e-9
 assert min(r['event_effect_min'] for r in out)>-1e-10
