import numpy as np,json
from scipy.linalg import expm,logm
rng=np.random.default_rng(4001030)
rows=[]
for d in [2,3,4,6]:
 for trial in range(25):
  E=np.diag(np.sort(rng.uniform(0,3,d))); s=.7; V=expm(s*E); Vh=expm(s*E/2); Vi=expm(-s*E/2)
  Y=np.eye(d,dtype=complex); g=0
  for _ in range(3):
   A=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d)); X=A.conj().T@A; X/=np.linalg.norm(X,2); delta=.06
   Y=expm(delta*X)@Y
   g+=2*delta*np.exp(s*(E[-1,-1]-E[0,0])/2)*np.linalg.norm(X,2)
  S=Y@Vh; W=S.conj().T@S
  rhs=(W@logm(W)-g*W)/s
  gap=S.conj().T@E@S-rhs; gap=(gap+gap.conj().T)/2
  ident=S.conj().T@logm(S@S.conj().T)@S-W@logm(W)
  rows.append({'dimension':d,'gap_min':float(np.linalg.eigvalsh(gap)[0]),'polar_identity_error':float(np.linalg.norm(ident,2)),'energy_Y_commutator':float(np.linalg.norm(E@Y-Y@E,2))})
assert min(x['gap_min'] for x in rows)>-1e-10
assert max(x['polar_identity_error'] for x in rows)<1e-10
print(json.dumps({'cases':len(rows),'min_gap':min(x['gap_min'] for x in rows),'max_polar_error':max(x['polar_identity_error'] for x in rows),'max_noncommutation':max(x['energy_Y_commutator'] for x in rows),'scope':'Finite algebra diagnostics, not native apparatus simulation.'},indent=2))
