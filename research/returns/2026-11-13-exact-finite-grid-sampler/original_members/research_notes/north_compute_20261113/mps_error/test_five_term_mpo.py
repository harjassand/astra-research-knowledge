import sys,json,itertools
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path('research_notes/quantum_connected_bridge_20261113/frame_mps').resolve()))
from mps_sampler import MPS,Q,zz
from five_term_mpo import dressed_terms,direct_qd_terms,apply_sum_products
from sampler import bitphase,qgate
rng=np.random.default_rng(582);results=[]
for n in [4,6,8]:
 worst=0;total=0
 for trial in range(20):
  m=MPS(n,tol=1e-14);v=np.zeros(1<<n,complex);v[0]=1
  # Entangled input; all sites conservatively unknown for full-operator test.
  for _ in range(4):
   u,w=sorted(rng.choice(n,2,replace=False));m.pair(u,w,Q);v=qgate(v,(1<<u)|(1<<w))
  pair=tuple(sorted(rng.choice(n,2,replace=False)));counts={(i,j):int(rng.integers(1,8)) for i in range(n) for j in range(i+1,n) if rng.random()<.4}
  W=np.ones(1<<n,complex)
  for e,c in counts.items():W*=bitphase(n,e,c*np.arctan2(4,3))
  expected=W.conj()*qgate(W*v,sum(1<<i for i in pair))
  apply_sum_products(m,dressed_terms(*pair,counts))
  error=float(np.max(abs(m.vector()-expected)));worst=max(worst,error);total+=1
  assert error<1e-11
 # Known basis input term elimination tests.
 for bits in itertools.product([0,1],repeat=min(n,3)):
  known=[0]*n
  for i,b in enumerate(bits):known[i]=b
  m=MPS(n,tol=1e-14);x=sum(b<<i for i,b in enumerate(known));v=np.zeros(1<<n,complex);v[x]=1
  for i,b in enumerate(known):
   if b:m.one(i,np.array([[0,1],[1,0]]))
  pair=(0,n-1);counts={(i,i+1):i+1 for i in range(n-1)};W=np.ones(1<<n,complex)
  for e,c in counts.items():W*=bitphase(n,e,c*np.arctan2(4,3))
  expected=W.conj()*qgate(W*v,(1<<pair[0])|(1<<pair[1]));terms=dressed_terms(*pair,counts,known)
  assert len(terms)==2
  apply_sum_products(m,terms);error=float(np.max(abs(m.vector()-expected)));assert error<1e-11;worst=max(worst,error);total+=1
 results.append(dict(n=n,checks=total,max_amplitude_error=worst))
# Direct combinedQD formula, full operator reconstruction.
terms=direct_qd_terms(0,1);full=sum((c*np.kron(f.get(0,np.eye(2)),f.get(1,np.eye(2))) for c,f in terms),np.zeros((4,4),complex));assert np.max(abs(full-Q@zz(np.arctan2(4,3))))<1e-14
Path(__file__).with_suffix('.json').write_text(json.dumps(results,indent=2));print(json.dumps(results,indent=2))
