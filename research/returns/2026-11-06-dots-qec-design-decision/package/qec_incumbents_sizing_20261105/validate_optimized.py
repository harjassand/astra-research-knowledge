import numpy as np,json,sys
from pathlib import Path
from optimized_subregion import model,synd,fail,sparse_bernoulli,BASE
m=model(BASE/'qec_fault_tuple_20261105/d21/input_graph.json',BASE/'qec_fault_tuple_20261105/d21/parameters.json');rng=np.random.default_rng(776)
E=(rng.random((100,m['n']))<m['q']*5).astype(np.uint8);S=synd(m,E)
for c in range(100):
 inds=rng.choice(m['n'],size=50,replace=False);n=m['ei'][inds].ravel();n=n[n>=0];np.bitwise_xor.at(S[c],n//8,(1 << (n%8)).astype(np.uint8));E[c,inds]^=1
assert np.array_equal(S,synd(m,E))
p=np.array([.03,.1,.2,.3,.4]);counts=np.zeros(32,int);N=100000
for _ in range(N):
 inds=sparse_bernoulli(rng,p);counts[int(np.sum(1<<inds))]+=1
probs=np.array([np.prod([p[i] if k>>i&1 else 1-p[i] for i in range(5)]) for k in range(32)])
chi=float(np.sum((counts-N*probs)**2/(N*probs)))
assert chi<70
out=dict(incremental_syndromes_verified=100,sparse_bernoulli_samples=N,small_space_chi_squared=chi,df=31,expected=probs.tolist(),observed=counts.tolist(),scope='Component checks, not MCMC mixing proof')
Path(__file__).with_name('optimized_component_checks.json').write_text(json.dumps(out,indent=2));print(json.dumps({k:v for k,v in out.items() if k not in ['expected','observed']}))
