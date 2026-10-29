import numpy as np,json
from pathlib import Path
I=np.eye(2);X=np.array([[0,1],[1,0]]);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1,-1]);P=[I,X,Y,Z]
rng=np.random.default_rng(320)
errs=[]
for _ in range(30):
 v=rng.normal(size=3);v/=np.linalg.norm(v);O=sum(x*s for x,s in zip(v,[X,Y,Z]))
 a=np.array([np.trace(O.T@p.conj().T@O@p).real/2 for p in P])
 formula=np.array([1-2*v[1]**2,1-2*v[2]**2,-1,1-2*v[0]**2])
 errs.extend([max(abs(a-formula)),abs(sum(a*a)/4-sum(v**4))])
for n in [1,2,3]:
 v=np.ones(3)/np.sqrt(3);o=sum(x*s for x,s in zip(v,[X,Y,Z]));O=np.array([[1.]])
 for _ in range(n):O=np.kron(O,o)
 D=2**n;rho=(np.eye(D)+O)/D;phi=np.eye(D).reshape(-1)/np.sqrt(D)
 import itertools
 probs=[]
 for labels in itertools.product(range(4),repeat=n):
  p=np.array([[1.]])
  for a in labels:p=np.kron(p,P[a])
  bell=np.kron(np.eye(D),p)@phi
  actual=np.vdot(bell,np.kron(rho,rho)@bell).real
  expected=(1+np.prod([1/3 if a!=2 else -1 for a in labels]))/4**n
  errs.append(abs(actual-expected));probs.append(actual)
 chi=sum((q-4**(-n))**2/4**(-n) for q in probs)
 errs.append(abs(chi-3**(-n)))
assert max(errs)<1e-12
out={'max_residual':float(max(errs)),'checks':len(errs),'scope':'dense identical-copy Bell probabilities, n<=3; no general learner'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
