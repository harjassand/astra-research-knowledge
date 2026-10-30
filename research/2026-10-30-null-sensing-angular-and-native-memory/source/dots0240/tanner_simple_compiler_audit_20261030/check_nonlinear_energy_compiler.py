"""Nonlinear raw-syndrome/unary-energy bridge fixture, not a Tanner density test.
3-bit repetition cosets; two duplicate distance views; three single-bit hubs.
All 8*5^3=1000 data/controller basis sectors are checked, including illegal ones.
"""
import itertools,json,numpy as np
states=[(e,a) for e in range(8) for a in itertools.product(range(5),repeat=3)]
index={x:i for i,x in enumerate(states)}
def bit(e,j):return (e>>j)&1
def raw(e):return (bit(e,0)^bit(e,2))|((bit(e,1)^bit(e,2))<<1)
def energy(e):return min(e.bit_count(),3-e.bit_count())
def move_for_raw(h,y):
 # The two views give U=2*distance; zero is the unique minimum raw sector.
 delta=[1,2,3][h]
 return (1<<h) if y==delta else 0
def phi(h,e):return e^move_for_raw(h,raw(e))
def gauge(x):
 e,a=x;aa=list(a)
 occupied=[h for h in range(3) if a[h]]
 if len(occupied)==1:
  h=occupied[0];label=(a[h]-1)^raw(e)
  e^=move_for_raw(h,label);aa[h]=label+1
 return e,tuple(aa)
perm=[index[gauge(x)] for x in states]
assert len(set(perm))==len(states)
inv={states[perm[i]]:states[i] for i in range(len(states))}
def flags_g(x):
 e,a=x;n=sum(v!=0 for v in a)
 return tuple(int(a[h]!=0 and (n>1 or a[h]!=1)) for h in range(3))
def flags_p(x):
 e,a=x;n=sum(v!=0 for v in a)
 return tuple(int(a[h]!=0 and (n>1 or raw(e^move_for_raw(h,a[h]-1))!=a[h]-1)) for h in range(3))
checks={'unitary_permutation':True,'gauged_flag_identity':True,'reset_no_flag_creation':True,
        'reset_clears_own_flag':True,'good_reset_exact_phi':True,'strict_bad_unary_surplus':True}
R=3;max_energy_change=0;min_surplus=100;reset_count=0
for x in states:
 assert flags_p(gauge(x))==flags_g(x)
 e,a=x;c=flags_g(x);xp=gauge(x)
 for h in range(3):
  if not a[h]:continue
  # Exactly one resolved physical label is nonzero on this source.
  ap=list(xp[1]);ap[h]=0
  target=inv[(xp[0],tuple(ap))];et,at=target;ct=flags_g(target)
  reset_count+=1
  assert all(ct[j]<=c[j] for j in range(3));assert ct[h]==0
  energy_token_flips=2*abs(energy(et)-energy(e))
  max_energy_change=max(max_energy_change,energy_token_flips)
  if not c[h]:assert et==phi(h,e)
  else:
   removed=sum(R*(c[j]-ct[j]) for j in range(3))+2*(energy(e)-energy(et))
   min_surplus=min(min_surplus,removed);assert removed>=R-2>0
# Exact full CPTP superoperator idempotence for each h (including coherence).
errs=[]
for h in range(3):
 Ks=[]
 for y in range(4):
  K=np.zeros((8,8))
  for e in range(8):
   if raw(e)==y:K[phi(h,e),e]=1
  Ks.append(K)
 S=sum(np.kron(K,K) for K in Ks)
 errs.append(float(np.max(np.abs(S@S-S))))
 assert errs[-1]==0
# Nonlinear-token distinction and bounded-overlap ratios at every flag mask.
theta=.01;u=.05
def V(e,mask):
 occ=[energy(e)]*2+[mask[h] for h in range(3) for _ in range(R)]
 return np.prod([1+theta**(u-x) for x in occ])-1
max_ratio=0.;equal_energy_raw_diff=[]
for mask in itertools.product([0,1],repeat=3):
 vals=np.array([V(e,mask) for e in range(8)])
 ds=[np.array([vals[e]-vals[phi(h,e)] for e in range(8)]) for h in range(3)]
 for h in range(3):
  assert min(ds[h])>=0
  for j in range(3):
   for e in range(8):
    numer=abs(ds[h][phi(j,e)]-ds[h][e]);den=ds[j][e]
    if den==0:assert numer==0
    else:max_ratio=max(max_ratio,float(numer/den))
assert energy(1)==energy(2) and phi(0,1)!=1 and phi(0,2)==2
out={'dimension':len(states),'actual_resolved_reset_sources_checked':reset_count,
 'checks':checks,'full_CPTP_idempotence_max_errors':errs,
 'max_actual_energy_token_change':max_energy_change,'R':R,
 'minimum_actual_bad_removed_minus_added':min_surplus,
 'bounded_patch_ratio_max_in_fixture':max_ratio,
 'equal_energy_records_need_raw_decisions':{'errors':[1,2],'energies':[energy(1),energy(2)],
   'raw_records':[raw(1),raw(2)],'hub0_outputs':[phi(0,1),phi(0,2)]},
 'scope':'Nonlinear-token/full-space compiler algebra only; no claim of Tanner expansion, density, or lifetime from this toy.'}
print(json.dumps(out,indent=2))
