import numpy as np,json
from pathlib import Path
rng=np.random.default_rng(49132);I=np.eye(2);X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1.,-1.]);ps=[X,Y,Z];rows=[]
for m in [2,3,5]:
 for case in range(20):
  z=rng.normal(size=(m,m))+1j*rng.normal(size=(m,m));W=z@z.conj().T;W/=np.trace(W)
  v,u=np.linalg.eigh(W);sw=u@np.diag(np.sqrt(v))@u.conj().T
  z=rng.normal(size=(m,m))+1j*rng.normal(size=(m,m));C=(z+z.conj().T)/2;C/=max(1,np.linalg.norm(C,2));a=1.4;b=.8;J=b*sw@C@sw
  ds=[np.kron(X,a*W),np.kron(Y,b*W),np.kron(Z,J)]
  L=sum(np.kron(p.T,d) for p,d in zip(ps,ds));Y0=np.kron(I,(a+b)*W+J);slack=np.kron(I,Y0)-L
  assert np.linalg.eigvalsh(slack).min()>-1e-10
  phi=np.array([1.,0,0,1])/np.sqrt(2);zero=np.kron(phi[:,None],np.eye(m));assert np.linalg.norm(slack@zero)<1e-10
  # Scale responses to an actual CPTP channel with a fullrank fixed background.
  scale=1/(8*m);ds=[scale*d for d in ds];D=2*m;tau=np.eye(D)/D
  choi=np.kron(I/2,tau)+sum(np.kron(p.T,d) for p,d in zip(ps,ds))/4
  assert np.linalg.eigvalsh(choi).min()>0
  fe=.25+scale*((a+b)*np.trace(W)+np.trace(J)).real/4
  score=.25+sum(np.trace(p@np.einsum('aibi->ab',d.reshape(2,m,2,m))).real for p,d in zip(ps,ds))/8
  assert abs(fe-score)<1e-12
  rows.append(dict(m=m,case=case,Fopt=float(fe),junk_commutator=float(np.linalg.norm(W@J-J@W)),minimum_dual_slack=float(np.linalg.eigvalsh(slack).min())))
Path(__file__).with_suffix('.json').write_text(json.dumps({'scope':'60 valid channels and analytic PSD dual, no learned decoder execution','cases':rows},indent=2)+'\n');print('PASS',len(rows))
