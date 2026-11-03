import numpy as np,itertools,json
from collections import defaultdict
D='producer-workspace/chiral_hamiltonian_interface_20261102'
z=np.load(D+'cubic_move.npz',allow_pickle=True)
T=[(tuple(t),int(s)) for t,s in z['T']]; nv=len(z['phi_a'])
faces=defaultdict(int)
for t,s in T:
 for j in range(4): faces[t[:j]+t[j+1:]]+=s*(-1)**j
assert all(x==0 for x in faces.values())
rnd=lambda x: np.floor(x+.5)
def selflink(phi):
 m=lambda i,j:rnd(phi[j]-phi[i])
 return sum(s*m(a,b)*(m(c,d)-m(b,d)+m(b,c)) for (a,b,c,d),s in T)
def omega(u,th,A,V):
 v=u+V*th
 m=lambda i,j:rnd(v[j]-v[i])
 ans=0.
 for (a,b,c,d),s in T:
  n=m(c,d)-m(b,d)+m(b,c)
  t1=th[a]*(A*m(a,b)-(rnd(A*u[b])-rnd(A*u[a]))-A*V*(rnd(th[b])-rnd(th[a])))*n
  t2=A*V*(th[b]-th[a])*((rnd(th[c])-rnd(th[b]))-rnd(th[c]-th[b]))*(m(c,d)-(rnd(u[d])-rnd(u[c])))
  ans+=s*(t1+t2)
 return ans
rng=np.random.default_rng(71)
err=perr=0.; examples=[]
for k in range(100):
 u=[rng.uniform(-.5,.5,nv) for _ in range(2)];th=rng.uniform(-.5,.5,nv);b=rng.uniform(-1,1)
 for j,(A,V) in enumerate([(2,2),(-8,1)]):
  d=omega(u[j],th+b,A,V)-omega(u[j],th,A,V)
  target=b*A*selflink(u[j]+V*th)
  err=max(err,abs(d-target))
  if len(examples)<4 and abs(target)>.01:examples.append({'phase_difference':d,'plus_target':target,'minus_residual':d+target})
 original=sum(omega(u[j],th,A,V) for j,(A,V) in enumerate([(2,2),(-8,1)]))
 th2=th.copy();th2[rng.integers(nv)]+=rng.choice([-2,-1,1,2])
 updated=sum(omega(u[j],th2,A,V) for j,(A,V) in enumerate([(2,2),(-8,1)]))
 perr=max(perr,abs((updated-original)-rnd(updated-original)))
out={'vertices':nv,'tetrahedra':len(T),'trials':100,'max_plus_cocycle_error':err,'max_compact_theta_phase_error':perr,'nonzero_examples':examples}
print(json.dumps(out,indent=2));json.dump(out,open(D+'joint_gap/actual_shared_disentangler_checks.json','w'),indent=2)
assert err<1e-9 and perr<1e-9
