from fractions import Fraction as F
import random,json,numpy as np
from pathlib import Path
rng=random.Random(405119);checks=0;maxmoment=0
for rootN in [2,4,8,16,32,64]:
 gamma=F(1,rootN);eta=F(1,4*rootN);e=F(3,4)
 for trial in range(200):
  w=[F(rng.randrange(1,1000),1000),None];w[1]=1-w[0]
  p=[(1-gamma)*x+gamma/2 for x in w];loss=[F(rng.randrange(1001),1000) for i in range(2)]
  # Sum all actual evaluate-arm-success/failure records; shadow and success contribute zero.
  moment=F(0);means=[F(0),F(0)]
  for i in range(2):
   prob=e*p[i]*loss[i];est=1/(e*p[i]);means[i]+=prob*est;moment+=prob*w[i]*est**2
   assert eta*est<=F(2,3)
  assert means==loss and moment<=F(16,3)
  assert sum((p[i]-w[i])*loss[i] for i in range(2))<=gamma
  maxmoment=max(maxmoment,float(moment));checks+=1
# General coherent Bell/flag coefficients and a noncommuting POVM, positive observed mismatch identity.
rngn=np.random.default_rng(155761);I=np.eye(2);X=np.array([[0,1],[1,0]]);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1,-1]);P=[I,X,Y,Z];phi=np.array([1,0,0,1])/np.sqrt(2);bells=[np.kron(I,p)@phi for p in P];maxerr=0
for trial in range(80):
 z=rngn.normal(size=(8,9))+1j*rngn.normal(size=(8,9));rho=z@z.conj().T;rho/=np.trace(rho)
 v=rngn.normal(size=3);v/=np.linalg.norm(v);E=(I+.73*sum(v[i]*P[i+1] for i in range(3)))/2
 Ms=[E,np.zeros((2,2)),I-E,np.zeros((2,2))]
 sig=[]
 for b in bells:
  V=np.kron(b[:,None],I);sig.append(V.conj().T@rho@V)
 loss=1-sum(np.trace(M@s).real for M,s in zip(Ms,sig));observed=0
 for x,b in enumerate(bells):
  for label,M in enumerate(Ms):
   if x!=label:observed+=np.trace(np.kron(np.outer(b,b.conj()),M)@rho).real
 maxerr=max(maxerr,abs(loss-observed))
assert maxerr<1e-13
out={'exact_meta_record_moment_fixtures':checks,'maximum_observed_second_moment':maxmoment,'theorem_second_moment_upper_bound':16/3,'coherent_positive_loss_fixtures':80,'maximum_positive_loss_identity_error':maxerr,'scope':'Independent finite moment and instrument checks, not a full selector run, source experiment, or finite arithmetic implementation.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
