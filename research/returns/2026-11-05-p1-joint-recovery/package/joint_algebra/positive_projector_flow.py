from pathlib import Path
ROOT = str(Path(__file__).resolve().parent) + "/"
import numpy as np, itertools, math, sys, json
from scipy.linalg import eigh
from singlet_singular import basis
from yangian_weak import local

def run(n,steps,seed):
 d=2**n; sites=[[local(n,i,a) for a in range(1,4)] for i in range(n)]
 Q=[]
 for a,b,c in [(0,1,2),(1,2,0),(2,0,1)]:
  Q.append(sum(sites[i][b]@sites[j][c]-sites[i][c]@sites[j][b] for i in range(n) for j in range(i+1,n)))
 Q=np.array(Q); Q2=sum(q@q for q in Q)
 k=3 if n>=6 else n//2; Ps=[];ranks=[]
 for bits in itertools.product([0,1],repeat=k):
  P=np.eye(d)
  for j,b in enumerate(bits):
   sing=(np.eye(d)-sum(sites[2*j][a]@sites[2*j+1][a] for a in range(3)))/4
   P=P@(sing if b==0 else np.eye(d)-sing)
  Ps.append(P);ranks.append(round(np.trace(P).real))
 Ps=np.array(Ps,dtype=complex)
 if seed==-1:
  dat=np.load(f'{ROOT}balanced_cut_n{n}.npz');Ps=dat['projectors'];ranks=[d//2,d//2]
 if seed>0:
  rng=np.random.default_rng(seed);B=basis(n);z=rng.normal(size=len(B))+1j*rng.normal(size=len(B));G=np.einsum('i,ijk->jk',z,B);G=(G+G.conj().T)/2
  lam,V=eigh(G);U=(V*np.exp(1j*lam))@V.conj().T;Ps=U@Ps@U.conj().T
 def energy_and_H(A):
  H=(Q2@A+A@Q2-2*sum(q@A@q for q in Q))/16
  e=np.einsum('xij,xij->',A.conj(),H).real/d
  return float(e),H
 e,H=energy_and_H(Ps);step=1.;init=e
 for it in range(steps):
  G=2j*sum(P@HH-HH@P for P,HH in zip(Ps,H))/d;G=(G+G.conj().T)/2
  gg=np.linalg.norm(G)**2
  if gg<1e-18:break
  lam,V=eigh(G)
  for trial in range(20):
   U=(V*np.exp(-1j*step*lam))@V.conj().T;new=U@Ps@U.conj().T;ee,HH=energy_and_H(new)
   if ee<=e-1e-4*step*gg:break
   step*=.5
  if ee>=e:break
  Ps,e,H=new,ee,HH;step=min(step*1.15,100)
  if it%100==0:print(json.dumps(dict(n=n,seed=seed,it=it,energy=e,step=step,grad=gg)),flush=True)
 print(json.dumps(dict(n=n,seed=seed,final_iteration=it,initial=init,energy=e,ranks=ranks,grad=gg)),flush=True)
 np.savez(f'{ROOT}positive_flow_n{n}_s{seed}.npz',projectors=Ps,energy=e,ranks=ranks)
if __name__=='__main__':run(int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]))
