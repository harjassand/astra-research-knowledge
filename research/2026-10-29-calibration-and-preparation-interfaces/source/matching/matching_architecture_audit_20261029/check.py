import numpy as np,json
from pathlib import Path
rng=np.random.default_rng(20261029)
def matchings(xs):
 if not xs: yield [];return
 a=xs[0]
 for j in range(1,len(xs)):
  b=xs[j]
  for z in matchings(xs[1:j]+xs[j+1:]):yield [(a,b)]+z
def state(n,M):
 v=np.zeros(2**n)
 for x in range(2**n):
  z=1
  for a,b in M:
   ba=(x>>a)&1;bb=(x>>b)&1
   if ba==bb:z=0;break
   z*=(-1)**ba/np.sqrt(2)
  v[x]=z
 return v
def iso(rows,cols):return np.linalg.qr(rng.normal(size=(rows,cols))+1j*rng.normal(size=(rows,cols)))[0]
rows=[]
for n in [4,6]:
 D=2**n;S=np.array([state(n,M) for M in matchings(list(range(n)))]).T
 U,s,_=np.linalg.svd(S,full_matrices=False);d=sum(s>1e-9);V=U[:,:d];P=V@V.conj().T
 coeff=(n+2)/(n-1);lam=3/(n+2)
 for it in range(20):
  # unrestricted nonunital/leaking map, including nearly identity to test low-loss regime
  r=3;W=iso(r*D,D);A=list(W.reshape(r,D,D))
  if it%2:A=[np.sqrt(.999)*np.eye(D)]+[np.sqrt(.001)*a for a in A]
  q=1-sum(np.mean(abs(np.sum(S.conj()*(a@S),axis=0))**2) for a in A)
  fp=sum(abs(np.trace(V.conj().T@a@V))**2/d**2 for a in A)
  leak=sum(np.linalg.norm((np.eye(D)-P)@a@V,'fro')**2/d for a in A)
  K=2**int(np.floor(np.log2(d)));Q=V@iso(d,K)
  fq=sum(abs(np.trace(Q.conj().T@a@Q))**2/K**2 for a in A)
  # reset on leakage yields nonnegative extra Bell overlap; raw is conservative
  assert 1-fq <=d/K*(1-fp)+1e-10
  assert q >=(1-lam)*(1-fp)+lam*leak-1e-10
  rows.append(dict(n=n,d=int(d),K=K,trial=it,q=float(q),full_loss=float(1-fp),sub_loss=float(1-fq),leak=float(leak),bound=float(d/K*coeff*q)))
# n=4 revealed matching reflection has test success one and full-code Bell fidelity zero
n=4;S=np.array([state(n,M) for M in matchings(list(range(n)))]).T
U,s,_=np.linalg.svd(S,full_matrices=False);V=U[:,:2];P=V@V.T
counter=[]
for v in S.T:
 A=np.eye(16)-2*P+2*np.outer(v,v)
 counter.append(dict(test_success=float(abs(v@A@v)**2),bell_fidelity=float(abs(np.trace(V.T@A@V))**2/4)))
out={'scope':'Numerical CPTP fixtures only; spectral theorem assumed, not established by tests','trials':rows,'leaked_matching_reflections':counter}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print('passed',len(rows),'CPTP fixtures; leaked-setting counterexamples',counter)
