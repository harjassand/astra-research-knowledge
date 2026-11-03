import numpy as np,json
from pathlib import Path
rng=np.random.default_rng(119)
parent=np.array([-1,0,0,1,1,2,2]);n=len(parent)
maxerr=0; intermediate_excursions_returning=0
for _ in range(1000):
 q=rng.integers(-3,4,n); dq=rng.integers(-2,3,n);dq[0]=-sum(dq[1:]);qp=q+dq
 E=rng.integers(-4,5,n-1)
 def subtree(a):
  a=a.copy()
  for v in range(n-1,0,-1):a[parent[v]]+=a[v]
  return a
 tmp=E+subtree(q)[1:]; Ef=tmp-subtree(qp)[1:]
 def div(e):
  d=np.zeros(n,int)
  for v in range(1,n):d[parent[v]]+=e[v-1];d[v]-=e[v-1]
  return d
 maxerr=max(maxerr,int(np.max(abs((qp-div(Ef))-(q-div(E))))))
 if np.any(abs(tmp)>4) and np.all(abs(Ef)<=4):intermediate_excursions_returning+=1
r={'random_trials':1000,'max_Gauss_change':maxerr,'valid_final_states_that_intermediate_rejection_would_wrongly_remove':intermediate_excursions_returning}
Path(__file__).with_name('tree_gauss_compiler_results.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
