"""Independent coherent-commutator audit. Floating exact-identity checks, not hardware."""
import numpy as np,json
from pathlib import Path
rng=np.random.default_rng(202610290618)
I=np.eye(2); X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1,-1]);P=[np.kron(a,b) for a in [X,Y,Z] for b in [X,Y,Z]]
D=4; out=[]
for mi,mo,nk in [(1,2,2),(2,3,2),(3,2,3),(2,1,4)]:
 for trial in range(4):
  A=rng.normal(size=(nk*D*mo,D*mi))+1j*rng.normal(size=(nk*D*mo,D*mi)); Ks=np.linalg.qr(A)[0].reshape(nk,D*mo,D*mi)
  ref=mi+1
  psi=rng.normal(size=(mi,ref))+1j*rng.normal(size=(mi,ref));psi/=np.linalg.norm(psi)
  sig=psi@psi.conj().T;rho=np.outer(psi.ravel(),psi.ravel().conj())
  ds=np.array([[K@np.kron(p,np.eye(mi))-np.kron(p,np.eye(mo))@K for p in P] for K in Ks])
  H=np.array([[sum(np.trace(np.kron(np.eye(D),sig)@v[j].conj().T@v[k]) for v in ds)/(2*D) for k in range(9)] for j in range(9)])
  # Dense physical circuit on pure mixed-input purification and M:Q.
  inputstate=np.einsum('j,f,su,mv->jfsmuv',np.ones(9)/3,np.ones(2)/np.sqrt(2),np.eye(D)/np.sqrt(D),psi)
  for j,p in enumerate(P):inputstate[j,0]=np.einsum('st,tmuv->smuv',p,inputstate[j,0])
  branches=[]
  for sign in [1,-1]:
   physical=np.zeros((9*mo*ref,9*mo*ref),complex); formula=physical.copy()
   for K in Ks:
    w=np.einsum('smtn,jftnuv->jfsmuv',K.reshape(D,mo,D,mi),inputstate)
    for j,p in enumerate(P):w[j,1]=np.einsum('st,tmuv->smuv',p,w[j,1])
    v=((w[:,0]+sign*w[:,1])/np.sqrt(2)).transpose(0,2,4,1,3).reshape(9*mo*ref,D*D)
    physical+=v@v.conj().T
    terms=[K@np.kron(p,np.eye(mi))+sign*np.kron(p,np.eye(mo))@K for p in P]
    for u in range(D):
     for v in range(D):
      L=np.concatenate([B.reshape(D,mo,D,mi)[u,:,v,:] for B in terms],axis=0)/(6*np.sqrt(D))
      L=np.kron(L,np.eye(ref));formula+=L@rho@L.conj().T
   assert np.linalg.norm(physical-formula)<2e-12
   branches.append(physical)
  minus=branches[1].reshape(9,mo*ref,9,mo*ref)
  C=np.einsum('jaka->jk',minus)
  gramerr=np.linalg.norm(C-H.T/18)
  # Arbitrary complex control and uniform postselection independently contracted from Delta.
  c=rng.normal(size=9)+1j*rng.normal(size=9);c/=np.linalg.norm(c)
  ampout=np.zeros((9,9),complex);postprob=0.
  for v in ds:
   for j in range(9):
    for k in range(9):ampout[j,k]+=c[j]*c[k].conjugate()*np.trace(v[j]@np.kron(np.eye(D)/D,sig)@v[k].conj().T)/4
   B=sum(c[j]*v[j] for j in range(9))/6
   postprob+=np.trace(B@np.kron(np.eye(D)/D,sig)@B.conj().T).real
  schurerr=np.linalg.norm(ampout-np.outer(c,c.conj())*H.T/2)
  posterr=abs(postprob-(c.conj()@H@c).real/18)
  ordinary=np.zeros((mo*ref,mo*ref),complex)
  for K in Ks:
   for u in range(D):
    for v in range(D):
     B=np.kron(K.reshape(D,mo,D,mi)[u,:,v,:]/np.sqrt(D),np.eye(ref));ordinary+=B@rho@B.conj().T
  marginal=np.einsum('jajb->ab',sum(branches).reshape(9,mo*ref,9,mo*ref))
  marginalerr=np.linalg.norm(marginal-ordinary)
  assert max(gramerr,schurerr,posterr,marginalerr)<2e-12
  out.append(dict(memory_in=mi,memory_out=mo,kraus=nk,gram_error=float(gramerr),schur_error=float(schurerr),complex_postselection_error=float(posterr),unconditioned_memory_reference_error=float(marginalerr),trace_error=float(abs(np.trace(sum(branches))-1))))
path=Path(__file__).with_suffix('.json');path.write_text(json.dumps({'scope':'16 rectangular full-memory channels, retained entangled reference; no hardware or interval claim','cases':out},indent=2)+'\n')
print(json.dumps({'cases':len(out),'max_error':max(max(v for k,v in r.items() if 'error' in k) for r in out)},indent=2))
