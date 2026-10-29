"""Actual known PGM measurement on product Choi resources; finite dense diagnostic."""
import numpy as np,itertools,json,math
from pathlib import Path
P=Path(__file__).parent

def processor(d,N):
 D=d**(N+1);Ps=[]
 for port in range(N):
  p=np.zeros((D,D))
  for other in itertools.product(range(d),repeat=N-1):
   v=np.zeros(D)
   for a in range(d):
    digits=[a];it=iter(other)
    digits += [a if j==port else next(it) for j in range(N)]
    idx=sum(x*d**(N-k) for k,x in enumerate(digits));v[idx]=1/np.sqrt(d)
   p+=np.outer(v,v)
  Ps.append(p)
 S=sum(Ps);lam,V=np.linalg.eigh(S);positive=lam>1e-10;Sinv=(V[:,positive]/np.sqrt(lam[positive]))@V[:,positive].T;supp=V[:,positive]@V[:,positive].T
 Es=[Sinv@p@Sinv+(np.eye(D)-supp)/N for p in Ps];roots=[]
 for E in Es:
  vals,U=np.linalg.eigh(E);assert vals.min()>-1e-12;roots.append((U*np.sqrt(np.maximum(vals,0)))@U.T)
 assert np.linalg.norm(sum(Es)-np.eye(D))<1e-11
 psi=np.zeros((d,D,d**N),complex)
 for r in range(d):
  for bs in itertools.product(range(d),repeat=N):
   ib=sum(x*d**(N-1-k) for k,x in enumerate(bs));ia=r*d**N+ib;psi[r,ia,ib]=d**(-(N+1)/2)
 def run(kraus):
  J=np.zeros((d*d,d*d),complex)
  for ks in itertools.product(kraus,repeat=N):
   state=psi.reshape([d,D]+[d]*N)
   for i,K in enumerate(ks):state=np.moveaxis(np.tensordot(K,state,axes=(1,2+i)),0,2+i)
   state=state.reshape(d,D,d**N)
   for i,root in enumerate(roots):
    out=np.einsum('ij,rjb->rib',root,state).reshape([d,D]+[d]*N);order=[0,2+i,1]+[2+j for j in range(N) if j!=i];out=out.transpose(order).reshape(d*d,-1);J+=out@out.conj().T
  return J
 Fe=sum(np.trace(e@p) for e,p in zip(Es,Ps))/(d**2*d**(N-1))
 return run,float(Fe)
rows=[];rng=np.random.default_rng(111922)
for d,N in [(2,n) for n in range(1,6)]+[(3,1),(3,2)]:
 run,F=processor(d,N);J=run([np.eye(d)]);phi=np.eye(d).ravel()/np.sqrt(d);Phi=np.outer(phi,phi);assert abs(phi@J@phi-F)<1e-11
 lam=(d*d*F-1)/(d*d-1);expected=lam*Phi+(1-lam)*np.eye(d*d)/(d*d);cov=np.linalg.norm(J-expected);assert cov<1e-11
 Q,_=np.linalg.qr(rng.normal(size=(d,d))+1j*rng.normal(size=(d,d)));JU=run([Q]);T=np.kron(np.eye(d),Q);ures=np.linalg.norm(JU-T@J@T.conj().T);assert ures<1e-11
 lower=N/(N+d*d-1);assert F>=lower-1e-12
 trnorm=np.linalg.eigvalsh(J-Phi);halfchoi=np.sum(abs(trnorm))/2;assert abs(halfchoi-(1-F))<1e-11
 rows.append({'d':d,'ports':N,'entanglement_fidelity':F,'proved_lower':lower,'half_diamond_by_covariance':1-F,'proved_half_diamond_upper':(d*d-1)/(N+d*d-1),'depolarizing_Choi_residual':float(cov),'unknown_unitary_program_commutation_residual':float(ures)})
# Product noisy Choi states of a CPTP amplitude-damping channel, not pure resources.
d=2;N=3;run,F=processor(d,N);J=run([np.eye(d)]);g=.23;ks=[np.diag([1,np.sqrt(1-g)]),np.array([[0,np.sqrt(g)],[0,0]])];noisy=run(ks);expected=sum(np.kron(np.eye(d),K)@J@np.kron(np.eye(d),K).conj().T for K in ks);noise_res=np.linalg.norm(noisy-expected);assert noise_res<1e-11
out={'scope':'Finite dense operations and floating checks, not scalable native compiler; exact proof in GOVERNING.md','rows':rows,'noisy_product_CPTP_Choi_simulation_residual':float(noise_res)};(P/'CHECKS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
