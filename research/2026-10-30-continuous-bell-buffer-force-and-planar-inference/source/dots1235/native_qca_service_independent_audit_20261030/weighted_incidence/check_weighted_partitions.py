import itertools,json,numpy as np
from functools import lru_cache
rng=np.random.default_rng(141)
records=[]
for n,K,Q in [(5,2,.2),(8,3,.35),(10,4,.8),(8,3,1.)]:
 labels=range(n);nu={}
 for k in range(1,K+1):
  for A in itertools.combinations(labels,k):nu[frozenset(A)]=float(rng.uniform(.1,1))
 row=max(sum(v for A,v in nu.items() if i in A) for i in labels)
 nu={A:v*Q/row for A,v in nu.items()}
 @lru_cache(None)
 def W(R):
  if not R:return 1.
  i=min(R)
  return sum(v*W(R-A) for A,v in nu.items() if i in A and A<=R)
 ratio=0.
 for k in range(1,n+1):
  for R in itertools.combinations(labels,k):
   R=frozenset(R);ratio=max(ratio,W(R)/Q**(len(R)/K))
 assert ratio<=1+1e-12
 records.append(dict(n=n,K=K,Q=Q,maximum_ratio=ratio,hyperedges=len(nu)))
# Q>1 cannot be substituted in the proposed induction: singleton weights=2,
# K=2 and two labels give W=4 > Q^(2/K)=2.
out={'scope':'Dense finite weighted partition algebra only, not a physical/QCA simulation','checks':records,'Q_above_one_counterexample':{'K':2,'Q':2,'W_two_labels':4,'claimed_bound_if_misused':2}}
print(json.dumps(out,indent=2))
