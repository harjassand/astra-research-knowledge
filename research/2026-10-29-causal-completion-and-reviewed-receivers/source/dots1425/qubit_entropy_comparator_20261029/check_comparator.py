import numpy as np,json
from pathlib import Path
rng=np.random.default_rng(20261029);I=np.eye(2);P=[I,np.array([[0,1],[1,0]]),np.array([[0,-1j],[1j,0]]),np.diag([1,-1])]
S=np.array([[1,0,0],[0,1/np.sqrt(2),0],[0,1/np.sqrt(2),0],[0,0,1]])
def entropy(rho):
 v=np.linalg.eigvalsh((rho+rho.conj().T)/2);v=v[v>1e-15];return float(-np.dot(v,np.log(v)))
def marginal(r):return np.trace(r.reshape(2,2,2,2),axis1=1,axis2=3)
def params(V):
 lam=np.array([np.trace(P[j]@marginal(V@P[j]@V.conj().T)).real/2 for j in range(1,4)])
 probs=np.array([1+sum(lam),1+lam[0]-lam[1]-lam[2],1-lam[0]+lam[1]-lam[2],1-lam[0]-lam[1]+lam[2]])/4
 assert min(probs)>-1e-12;assert sum(sorted(lam*lam)[-2:])<=1+1e-12
 return lam,probs
chs=[]
for i in range(100):
 A=rng.normal(size=(3,2))+1j*rng.normal(size=(3,2))
 if i<40:
  A=np.array([[1,0],[0,0],[0,1]],complex)+10**rng.uniform(-4,-.2)*A
 Q,_=np.linalg.qr(A);chs.append(params(S@Q))
maxlocal=0;maxcomplete=0;best=None;trials=0
for lam,pr in chs:
 axis=int(np.argmax(abs(lam)))+1
 for dimR in [1,2,4]:
  lifts=[np.kron(p,np.eye(dimR)) for p in P];Z=lifts[axis]
  for z in range(80):
   rank=int(rng.integers(1,2*dimR+1));A=rng.normal(size=(2*dimR,rank))+1j*rng.normal(size=(2*dimR,rank));rho=A@A.conj().T;rho/=np.trace(rho)
   if z%3==0:
    rho=(rho+Z@rho@Z)/2 + 10**rng.uniform(-5,-.2)*(rho-(rho+Z@rho@Z)/2)
   phi=sum(w*pp@rho@pp for w,pp in zip(pr,lifts));deph=(rho+Z@rho@Z)/2;s=entropy(rho);loss=entropy(phi)-s;dloss=entropy(deph)-s
   if loss>1e-13:
    ratio=dloss/loss
    if dimR==1:maxlocal=max(maxlocal,ratio)
    elif ratio>maxcomplete:maxcomplete=ratio;best=dict(lambdas=lam.tolist(),dim_reference=dimR,ratio=ratio,loss=loss,dephasing_loss=dloss,rho_real=rho.real.tolist(),rho_imag=rho.imag.tolist())
   if dimR==1:assert dloss<=2*loss+1e-11
   trials+=1
out=dict(trials=trials,channels=100,max_local_ratio=maxlocal,max_complete_ratio=maxcomplete,complete_candidate=best,scope='Floating random diagnostics; local theorem proved separately. Complete extension remains conjectural unless proof/counterexample supplied.')
Path(__file__).with_name('CHECKS.json').write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in out.items() if k!='complete_candidate'})
