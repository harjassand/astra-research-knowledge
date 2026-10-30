"""Independent finite overlapping-view test, including globally invalid baselines.
Four DATA bits on a ring. Each two-bit view has code {00,11}, hence one
full-row-rank local parity check; global parity syndromes obey one relation.
"""
import json
from functools import lru_cache
n=4;w=2;views=[(i,(i+1)%n) for i in range(n)]
weight=int.bit_count
def parity(e,view):return sum((e>>j)&1 for j in view)%2
def synd(e):return sum(parity(e,v)<<i for i,v in enumerate(views))
def energy(e,eta):return weight(synd(e)^eta)
def masks(view):return [sum(((b>>i)&1)<<j for i,j in enumerate(view)) for b in range(4)]
choices=[masks(v) for v in views]
def actual(e,eta,h):
 vals=[(energy(e^f,eta),f) for f in choices[h]]
 best=min(x for x,f in vals)
 return 0 if energy(e,eta)==best else min(f for x,f in vals if x==best)
def active(e,eta):return sum(actual(e,eta,h)!=0 for h in range(n))
checks=0;invalid_checks=0;idempotence=0;maxmoves=0
for eta in range(1<<n):
 @lru_cache(None)
 def longest(e):
  nxt=[e^actual(e,eta,h) for h in range(n) if actual(e,eta,h)]
  return 0 if not nxt else 1+max(longest(z) for z in nxt)
 for e in range(1<<n):
  ue=energy(e,eta);u=energy(e,0);b=weight(eta)
  assert abs(ue-u)<=w*b and ue<=2*weight(e)+w*b
  assert active(e,eta)>=active(e,0)-3*b
  for f in range(1<<n):
   assert abs(energy(e^f,eta)-ue)<=2*weight(f);checks+=1
  for h in range(n):
   f=actual(e,eta,h)
   assert not f or energy(e^f,eta)<ue
   assert actual(e^f,eta,h)==0;idempotence+=1
  ell=longest(e);assert ell<=ue;maxmoves=max(maxmoves,ell)
  if weight(eta)%2:invalid_checks+=1
# The one-bit inconsistent-copy obstruction: two different fixed targets cycle.
e=0;trajectory=[e]
for target in [1,0,1,0,1,0]:
 if e!=target:e^=1
 trajectory.append(e)
assert trajectory==[0,1,0,1,0,1,0]
print(json.dumps({'bit_count':n,'energy_views':views,'each_bit_incidence':2,'Lipschitz_checks':checks,'orbit_minimizer_idempotence_checks':idempotence,'globally_invalid_baseline_source_states':invalid_checks,'max_accepted_moves':maxmoves,'all_finite_work_bounds_pass':True,'inconsistent_copy_cycle':trajectory,'scope':'Exact biased-energy algebra on a small model, not Tanner expansion or native-memory simulation'},indent=2))
