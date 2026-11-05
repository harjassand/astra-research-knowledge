"""Small exact-rational checks of the Fourier cover and adaptive-clock claims.
The general arguments are in sampler_obstruction.md and reusable_register_audit.md.
"""
from fractions import Fraction as F

m=4
spaces={frozenset([0])};queue=list(spaces)
for R in queue:
 for v in range(1,1<<m):
  if v in R:continue
  U=R|frozenset(s^v for s in R)
  if U not in spaces:spaces.add(U);queue.append(U)
assert len(spaces)==67
cases=0
for xs in [(F(1,2),F(1,3),F(2,3),F(1,5)),(F(1),)*4]:
 w=[]
 for s in range(1<<m):
  z=F(1)
  for j in range(m):
   if s>>j&1:z*=xs[j]
  w.append(z)
 for R in spaces:
  zr=sum(w[s] for s in R)
  for L in spaces:
   if not L<=R:continue
   zl=sum(w[s] for s in L)
   assert zl/zr>=F(len(L),len(R))
   for a in R:assert zl>=sum(w[s^a] for s in L)
   cases+=1
print('Verified regular-cover acceptance inequality on',cases,'exact subspace/weight cases.')

P=[[F(99,100),F(1,100)],[F(1,10),F(9,10)]]
pi=[F(10,11),F(1,11)];b=[F(0),F(1,2)];horizon=4
assert [sum(pi[s]*P[s][t] for s in range(2)) for t in range(2)]==pi
bound=horizon*sum(pi[s]*b[s] for s in range(2));maximum=F(0)
for policy in range(1<<(2*horizon)):
 future=[F(0),F(0)]
 for t in range(horizon-1,-1,-1):
  future=[b[s]+(1-b[s])*sum(P[s][u]*future[u] for u in range(2)) if policy>>(2*t+s)&1 else F(0) for s in range(2)]
 fail=sum(pi[s]*future[s] for s in range(2))
 assert fail<=bound
 maximum=max(maximum,fail)
print('Verified',1<<(2*horizon),'state-dependent stopping policies; max failure =',maximum,'<=',bound)
print('Rare-record example: unconditional one-step failure',pi[1]*b[1],'; conditioned on dangerous report',b[1])
