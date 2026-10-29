import numpy as np,itertools,json
from pathlib import Path
rng=np.random.default_rng(202610291225);I=np.eye(2);P=[I,np.array([[0,1],[1,0]]),np.array([[0,-1j],[1j,0]]),np.diag([1,-1])]
def kron(xs):
 a=np.ones((1,1),complex)
 for x in xs:a=np.kron(a,x)
 return a
def S(r):
 v=np.linalg.eigvalsh((r+r.conj().T)/2);v=v[v>1e-14];return float(-np.dot(v,np.log(v)))
def channel(r,pr,lifts):return sum(w*u@r@u.conj().T for w,u in zip(pr,lifts))
rows=[];maxratio=0;worst_submod=0;min_margin=1.;residual=0
for trial in range(100):
 n=3;dR=2;d=2**n*dR;params=[];lifts=[];zs=[]
 for i in range(n):
  # actual self-compatible channel: twirl symmetric isometry with input/output Pauli conjugations.
  B=np.array([[1,0,0],[0,1/np.sqrt(2),0],[0,1/np.sqrt(2),0],[0,0,1]])
  A=rng.normal(size=(3,2))+1j*rng.normal(size=(3,2))
  if trial<50:A=np.array([[1,0],[0,0],[0,1]])+10**rng.uniform(-3,0)*A
  Q,_=np.linalg.qr(A);V=B@Q
  def marg(x):return np.trace(x.reshape(2,2,2,2),axis1=1,axis2=3)
  lam=np.array([np.trace(P[j]@marg(V@P[j]@V.conj().T)).real/2 for j in range(1,4)]);a=int(np.argmax(abs(lam)))+1
  pr=np.array([1+sum(lam),1+lam[0]-lam[1]-lam[2],1-lam[0]+lam[1]-lam[2],1-lam[0]-lam[1]+lam[2]])/4
  other=[j for j in [1,2,3] if j!=a];pairs=[(0,a),tuple(other)];weights=[2*min(pr[j],pr[k]) for j,k in pairs];alpha=sum(weights)
  assert alpha>=1-1/np.sqrt(2)-1e-12
  # Explicit probability-vector reconstruction from paired pinching branches and residual unitary branches.
  rebuilt=np.zeros(4);rest=pr.copy()
  for (j,k),w in zip(pairs,weights):rebuilt[j]+=w/2;rebuilt[k]+=w/2;rest[j]-=w/2;rest[k]-=w/2
  rebuilt+=rest;residual=max(residual,np.max(abs(rebuilt-pr)));assert min(rest)>-1e-12
  params.append((pr,alpha));ls=[kron([pp if z==i else I for z in range(n)]+[np.eye(dR)]) for pp in P];lifts.append(ls);zs.append(ls[a])
 rank=int(rng.integers(1,d+1));X=rng.normal(size=(d,rank))+1j*rng.normal(size=(d,rank));rho=X@X.conj().T;rho/=np.trace(rho)
 base=S(rho);f={};states={}
 for mask in range(2**n):
  rr=rho.copy()
  for i in range(n):
   if mask>>i&1:rr=(rr+zs[i]@rr@zs[i])/2
  states[mask]=rr;f[mask]=S(rr)-base
 for mask in range(2**n):
  for i in range(n):
   for j in range(i+1,n):
    if not (mask>>i&1 or mask>>j&1):
     deficit=f[mask|1<<i|1<<j]-f[mask|1<<j]-f[mask|1<<i]+f[mask]
     worst_submod=max(worst_submod,deficit);assert deficit<1e-11
 phi=rho.copy()
 for (pr,alpha),ls in zip(params,lifts):phi=channel(phi,pr,ls)
 gain=S(phi)-base;alpha=min(x[1] for x in params);full=f[2**n-1]
 expected=sum(np.prod([params[i][1] if mask>>i&1 else 1-params[i][1] for i in range(n)])*f[mask] for mask in f)
 assert gain+1e-11>=expected and expected+1e-11>=alpha*full
 min_margin=min(min_margin,gain-alpha*full);ratio=full/gain if gain>1e-13 else 0;maxratio=max(maxratio,ratio)
 rows.append(dict(alpha=alpha,entropy_gain=gain,dephasing_gain=full,expected_subset_gain=expected,ratio=ratio))
out=dict(trials=100,system_qubits=3,reference_dimension=2,max_ratio=maxratio,worst_submodularity_defect=worst_submod,min_proved_margin=min_margin,probability_decomposition_residual=float(residual),rows=rows,scope='Floating full correlated-state/reference diagnostics; exact argument governs. No hardware.')
Path(__file__).with_name('TENSOR_CHECKS.json').write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in out.items() if k!='rows'})
