import numpy as np,json
from pathlib import Path
rng=np.random.default_rng(202610291120)
I=np.eye(2);X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1,-1]);pauli=[X,Y,Z];P=[np.kron(a,b) for a in pauli for b in pauli]
sing=np.array([0,1,-1,0],complex)/np.sqrt(2);trip=[np.array([1,0,0,0],complex),np.array([0,1,1,0],complex)/np.sqrt(2),np.array([0,0,0,1],complex)]
K0=[np.outer(sing,sing.conj())]+[np.outer(a,b.conj())/np.sqrt(3) for a in trip for b in trip]
depol=[np.outer(a,b)/2 for a in np.eye(4) for b in np.eye(4)]
rows=[]
for trial in range(10):
 q=rng.normal(size=4);q/=np.linalg.norm(q);u=q[0]*I-1j*sum(q[i+1]*pauli[i] for i in range(3));W=np.kron(u,I);K=[W@k@W.conj().T for k in K0]
 S=np.eye(4)-2*np.outer(sing,sing.conj());twisted=W@S@W.conj().T
 c=np.array([np.trace(p@twisted).real/2 for p in P])/np.sqrt(3);assert abs(c@c-1)<1e-12
 for eta in [0,.001,.01,.1,1]:
  ks=[np.sqrt(1-eta)*k for k in K]+[np.sqrt(eta)*k for k in depol]
  H=sum(np.array([[np.trace((k@p-p@k).conj().T@(k@t-t@k))/8 for t in P] for p in P]) for k in ks)
  target=np.eye(9)-(1-eta)*np.outer(c,c)
  err=np.linalg.norm(H-target);assert err<1e-12
  vecs=[k.reshape(-1) for k in ks];choi=sum(np.outer(v,v.conj()) for v in vecs)
  low=np.linalg.eigvalsh(choi).min();assert low>=eta/4-1e-12
  rows.append(dict(trial=trial,eta=eta,H_residual=float(err),minus_probability=float(np.trace(H).real/18),dark_label_probability=eta/(8+eta),choi_min_eigenvalue=float(low)))
Path(__file__).with_suffix('.json').write_text(json.dumps(dict(scope='Dense numeric Kraus diagnostic of proved collective-twirl/depolarizing source-to-label reduction; ideal IID source, not measured hardware',max_residual=max(r['H_residual'] for r in rows),rows=rows),indent=2)+'\n')
print('passed',len(rows),'fixtures; max residual',max(r['H_residual'] for r in rows))
