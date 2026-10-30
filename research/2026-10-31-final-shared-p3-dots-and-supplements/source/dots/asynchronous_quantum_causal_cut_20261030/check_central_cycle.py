import numpy as np, json
from collections import deque
# Explicit complete tick channel on counter c=0,1,2 and stage j=0,...,n.
n=4; d=3*(n+1); lam=0.7
ks=[]
for c in range(3):
 for j in range(n+1):
  f=j+1 if c==2 and j<n else j
  k=np.zeros((d,d),complex); k[c*(n+1)+f,c*(n+1)+j]=1; ks.append(k)
I=np.eye(d); source=sum(k.conj().T@k for k in ks)
comp=float(np.linalg.norm(source-I))
# Arbitrary Hamiltonian does not change the tilted identity calculation.
rng=np.random.default_rng(19); A=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d)); H=(A+A.conj().T)/2
mgf={}
for th in [-0.7,0.4]:
 adj=1j*(H@I-I@H)+lam*(np.exp(th)*sum(k.conj().T@I@k for k in ks)-I)
 mgf[str(th)]=float(np.linalg.norm(adj-lam*(np.exp(th)-1)*I))
# Disable c=0: leaves keep basis states fixed but really dephase superpositions.
v=np.zeros(d,complex);v[0]=v[1]=1/np.sqrt(2); rho=np.outer(v,v.conj()); out=sum(k@rho@k.conj().T for k in ks)
disabled_dephase=float(np.linalg.norm(out-rho))
# Conservative finite-state latch model. Each commit may leave ONE stale attempt.
# State c,stage,possible_stale,snapshot_fresh_since_commit,has_committed.
initial=[(c,j,1,False,False) for c in range(3) for j in range(n+1)]
seen=set(initial); q=deque(initial); failures=[]
while q:
 c,j,stale,fresh,prev=q.popleft(); nxt=[]
 # Tick advances active state only.
 nxt.append((c,min(n,j+1) if c==2 else j,stale,fresh,prev))
 # First SUCCESS may be stale; subsequent ones are fresh. Saturated counter does not rewrite S.
 for is_stale in ([True,False] if stale else [False]):
  nf=fresh if c==2 else (not is_stale)
  nc=min(2,c+1); nj=0 if c==1 else j
  nxt.append((nc,nj,0,nf,prev))
 # FREE opportunity commits only if timer complete. Any other opportunity is a no-op.
 if c==2 and j==n:
  if prev and not fresh: failures.append((c,j,stale,fresh,prev))
  nxt.append((0,0,1,False,True))
 for z in nxt:
  if z not in seen: seen.add(z); q.append(z)
res={"tick_kraus_completeness_residual":comp,"tilted_identity_residuals":mgf,"disabled_mode_dephasing_is_nonzero":disabled_dephase,"latch_states_checked":len(seen),"second_commit_stale_counterexamples":failures,"short_interval_max_fraction_n":17*21/400,"long_interval_min_fraction_n":23*19/400}
assert comp<1e-12 and all(x<1e-12 for x in mgf.values()) and disabled_dephase>0
assert not failures
print(json.dumps(res,indent=2))
