"""Full quantum-program/bath-memory effect checks for a guarded logical port.
Random joint CPTP maps are actual finite instruments; they do not implement the expensive learner.
"""
import numpy as np,json
from pathlib import Path
rng=np.random.default_rng(202610291315);I=np.eye(2);X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1,-1]);P=[I,X,Y,Z];m=4
states=[np.array([1,0],complex),np.array([0,1],complex),np.array([1,1],complex)/np.sqrt(2),np.array([1,-1],complex)/np.sqrt(2),np.array([1,1j],complex)/np.sqrt(2),np.array([1,-1j],complex)/np.sqrt(2)]
def adj(Ks,E):return sum((K.conj().T@E@K for K in Ks),np.zeros((m,m),complex))
rows=[]
for trial in range(10):
 raw=rng.normal(size=(24,8))+1j*rng.normal(size=(24,8));isom=np.linalg.qr(raw)[0];Ks=list(isom.reshape(3,8,8));B=[]
 for p in P:
  B.append([np.einsum('ab,biaj->ij',p.conj().T,K.reshape(2,m,2,m))/2 for K in Ks])
 good=B[0];bad=[b for bs in B[1:] for b in bs];Ebad=adj(bad,np.eye(m));Q=np.zeros((m,m),complex);passing=[]
 for psi in states:
  perp=np.array([-psi[1].conjugate(),psi[0].conjugate()])
  for K in Ks:
   A=K.reshape(2,m,2,m);f=np.einsum('a,aibj,b->ij',perp.conj(),A,psi)/np.sqrt(6);p=np.einsum('a,aibj,b->ij',psi.conj(),A,psi)/np.sqrt(6);Q+=f.conj().T@f;passing.append(p)
 relation=np.linalg.norm(Ebad-1.5*Q);assert relation<1e-12
 s=.1;a=1-s;R=1.5*s/a;bound=(R/(1+R))**2;J=5;L=80
 F={(j,f):np.zeros((m,m),complex) for j in range(J+1) for f in range(3)}
 for l in range(1,L+1):
  G={}
  for f in range(3):G[J,f]=np.eye(m) if f==2 else np.zeros((m,m),complex)
  for j in range(J):
   for f in range(3):
    # Successful service now, or a test-pass retry. Cap does not ensure completion.
    terminal=lambda jj,ff: (np.eye(m) if ff==2 else np.zeros((m,m),complex)) if jj==J else F[jj,ff]
    G[j,f]=s*adj(good,terminal(j+1,f))+s*adj(bad,terminal(j+1,min(2,f+1)))+a*adj(passing,F[j,f])
  F=G
 maximum=float(np.linalg.eigvalsh(F[0,0]).max());assert maximum<=bound+1e-12
 # Verify full retired-key twirl on a correlated logical-memory-reference input.
 v=rng.normal(size=32)+1j*rng.normal(size=32);v/=np.linalg.norm(v);rho=np.outer(v,v.conj());actual=np.zeros((32,32),complex);ideal=actual.copy()
 for p in P:
  pM=np.kron(p,np.eye(m))
  for K in Ks:
   A=np.kron(pM@K@pM,np.eye(4));actual+=A@rho@A.conj().T/4
 for p,bs in zip(P,B):
  for b in bs:
   A=np.kron(np.kron(p,b),np.eye(4));ideal+=A@rho@A.conj().T
 residual=np.linalg.norm(actual-ideal);assert residual<1e-12
 rows.append(dict(trial=trial,positive_test_effect_residual=float(relation),retired_key_joint_instrument_residual=float(residual),bad_accepted_effect_norm=maximum,negative_binomial_bound=bound,cap=L,services=J,corrected_faults=1))
Path(__file__).with_suffix('.json').write_text(json.dumps({'scope':'Finite joint CPTP quantum-program/source-memory diagnostics; model-free guard transfer, not actual compiler/hardware or yield evidence','rows':rows},indent=2)+'\n');print('passed',len(rows),'max effect',max(r['bad_accepted_effect_norm'] for r in rows),'NB',bound)
