from fractions import Fraction as F
from pathlib import Path
import numpy as np, random, json
root=Path('producer-workspace/chiral_hamiltonian_interface_20261102')
z=np.load(root/'cubic_move.npz',allow_pickle=True)
T=[(tuple(map(int,t)),int(s)) for t,s in z['T']]
nv=len(z['phi_a']); rng=random.Random(20261103)
def rnd(x): return (x+F(1,2)).numerator//(x+F(1,2)).denominator
def omega(u,theta,A,V):
 out=F(0)
 for (a,b,c,d),o in T:
  edge=lambda i,j:rnd(u[j]-u[i]+V*(theta[j]-theta[i]))
  dm=edge(c,d)-edge(b,d)+edge(b,c)
  first=theta[a]*(A*edge(a,b)-rnd(A*u[b])+rnd(A*u[a])-A*V*(rnd(theta[b])-rnd(theta[a])))*dm
  second=A*V*(theta[b]-theta[a])*(rnd(theta[c])-rnd(theta[b])-rnd(theta[c]-theta[b]))*(edge(c,d)-rnd(u[d])+rnd(u[c]))
  out+=o*(first+second)
 return out
def selflink(phi):
 out=0
 for (a,b,c,d),o in T:
  edge=lambda i,j:rnd(phi[j]-phi[i])
  out+=o*edge(a,b)*(edge(c,d)-edge(b,d)+edge(b,c))
 return out
nonzero=0
for trial in range(24):
 us=[[F(rng.randrange(-50,51),101) for _ in range(nv)] for _ in range(2)]
 theta=[F(rng.randrange(-51,52),103) for _ in range(nv)]
 beta=F(rng.randrange(-106,107),107)
 total=F(0); shifted=F(0)
 n=[rng.randrange(-2,3) for _ in range(nv)]
 for u,(A,V) in zip(us,[(2,2),(-8,1)]):
  x=omega(u,theta,A,V)
  y=omega(u,[t+beta for t in theta],A,V)
  target=beta*A*selflink([ui+V*th for ui,th in zip(u,theta)])
  assert y-x==target
  nonzero+=bool(target)
  assert omega([ui+ni for ui,ni in zip(u,n)],theta,A,V)==x
  total+=x
  shifted+=omega(u,[t+ni for t,ni in zip(theta,n)],A,V)
 assert (shifted-total).denominator==1
result={'exact_rational_trials':24,'vertices':nv,'tetrahedra':len(T),'nonzero_cocycle_examples':nonzero,'uniform_shift_exact':True,'matter_integer_shift_exact':True,'theta_integer_shift_mod_one_exact':True}
print(json.dumps(result,indent=2));(root/'joint_gap/audit_compact_cochain_exact_results.json').write_text(json.dumps(result,indent=2))
