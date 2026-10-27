"""Check actual filtered flag, polar code and ancilla-rank estimate for nonflat sigma."""
import numpy as np
rng=np.random.default_rng(261026133)
counts={'small_h':0,'filtered':0};maxrank=0
for k in [1,2,4,7]:
 for rep in range(12):
  sig=rng.dirichlet(np.full(k,.3));p=[.1,.6,.99][rep%3];q=1-p;theta=[.2,.9,1.][rep%3]
  n=3*k+1;V=np.eye(n)[:,:3*k]
  G=rng.normal(size=(3,k))+1j*rng.normal(size=(3,k));G*=np.sqrt(theta)/np.linalg.norm(G)
  f=np.r_[G.reshape(-1),np.sqrt(1-theta)]
  weights=p*sig/(q+p*sig);h=np.r_[(G*(1-weights)).reshape(-1),np.sqrt(1-theta)]
  e=np.linalg.norm(f-h);hn=np.linalg.norm(h)
  assert abs(e*e-np.sum(abs(G)**2*weights**2))<1e-12
  if hn<.5:
   assert e>.5-1e-12 and 2*q<=4*q*e+1e-12;counts['small_h']+=1;continue
  hf=h/hn;inside=V.conj().T@hf;th=np.vdot(inside,inside).real
  if th<1e-14:W=V.copy()
  else:
   u=inside/np.sqrt(th);g=V@u
   if th>1-1e-12:
    outside=np.eye(n)[:,-1];new=-outside
   else:
    outside=(hf-np.sqrt(th)*g)/np.sqrt(1-th)
    new=np.sqrt(1-th)*g-np.sqrt(th)*outside
   W=V+np.outer(new-g,u.conj())
  assert np.linalg.norm(W.conj().T@W-np.eye(3*k))<1e-10
  assert np.linalg.norm(W.conj().T@hf)<1e-10
  D=V-W
  psi=rng.normal(size=9)+1j*rng.normal(size=9);psi/=np.linalg.norm(psi)
  X=np.kron(np.outer(psi,psi.conj()),np.diag(sig))
  DX=np.kron(np.eye(3),D)@X
  sv=np.linalg.svd(DX,compute_uv=False);rank=np.count_nonzero(sv>1e-10);maxrank=max(maxrank,rank);assert rank<=3
  assert sv.sum()<=np.sqrt(6)*q*e/(p*hn)+1e-10
  reset=2*q*np.sqrt(max(1-abs(np.vdot(f,hf))**2,0))
  assert reset<=2*q*e+1e-10
  assert 2*p*sv.sum()+reset<=(2+4*np.sqrt(6))*q*e+1e-10
  counts['filtered']+=1
print({'status':'PASS','cases':counts,'maximum_changed_operator_rank_with_ancilla':maxrank})
