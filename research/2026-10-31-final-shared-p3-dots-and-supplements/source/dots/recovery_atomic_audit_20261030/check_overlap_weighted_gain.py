"""Independent two-adapter/shared-PARK certificate and complete-gain check.
No source test imports. Basis monomial resets retain all remote labels.
"""
from itertools import product
from collections import defaultdict
import numpy as np,json
from pathlib import Path
phases=('I','S0','S1','E0','E1','V0','V1','H','R0','R1','F0','F1')
states=list(product(phases,phases,(0,1),(0,1),(0,1,2))) # owner: active, PARK dirty, PARK W0
index={s:i for i,s in enumerate(states)}
def bad(c,p,w):
 if c in ('I','S0','R0','R1','F0','F1'):return 0
 if c in ('S1','E0','E1','V0'):return int(not p)
 if c in ('V1','H'):return int(not (p and w==2))
 raise ValueError(c)
def flags(s):return (bad(s[0],s[2],s[4]),bad(s[1],s[3],s[4]))
bits=np.array([flags(s) for s in states]);m=bits.sum(axis=1);theta=.71;f=np.exp(theta*m)
jumps=defaultdict(list);edges=[]
def add(s,t,name,coherent=False):
 if coherent:edges.append((index[s],index[tuple(t)]))
 else:jumps[name].append((index[s],index[tuple(t)]))
for s in states:
 for x in range(2):
  c,p=s[x],s[2+x]
  def go(cc,pp=p,name='',coh=False):
   t=list(s);t[x]=cc;t[x+2]=pp;add(s,t,(x,name),coh)
  if c!='I':go('S0',name='seal_'+c)
  if c=='I':go('S0',name='command')
  if c=='S0':go('E'+str(p),1,coh=True)
  if c.startswith('E'):
   b=int(c[1]);
   if p==1:go('S0',b,coh=True)
   go('S1',name='commit_'+c)
  if c=='S1':go('V0',name='begin_verify')
  if c=='V0' and s[4]==2:go('V1',coh=True)
  if c=='V1':
   if s[4]==2:go('V0',coh=True)
   go('H',name='hold')
  if c=='H':go('S0',name='erase');go('R0',name='release')
  if c=='R0':go('F'+str(p),0,coh=True)
  if c.startswith('F'):
   b=int(c[1]);
   if p==0:go('R0',b,coh=True)
   go('R1',name='clear_commit_'+c)
  if c=='R1':go('I',name='idle')
 # Actual PARK creation/reset/unpark abstractions, resolved source label.
 if s[4]==0 and (s[2] or s[3]):
  t=list(s);t[4]=2;add(s,t,('native','ready_to_PARK'))
 if s[4]==1:
  t=list(s);t[4]=2;add(s,t,('native','quiescent_dirty'))
 if s[4]==2:add(s,s,('native','quiescent_zero'))
 if s[4] in (1,2) and not(s[2] or s[3]):
  t=list(s);t[4]=0;add(s,t,('native','unpark_'+str(s[4])))
assert all(np.array_equal(bits[a],bits[b]) for a,b in edges)
worst=0.;seal_drift=np.zeros(len(states));nonseal_drift=np.zeros(len(states));max_healed=0
for label,pairs in jumps.items():
 # Each separately source-resolved physical reset has an injective mapping
 # of retained outside labels; its J^*FJ is exactly diagonal, not assumed.
 assert len(set(a for a,b in pairs))==len(pairs)
 assert len(set(b for a,b in pairs))==len(pairs),label
 for a,b in pairs:
  delta=f[b]-f[a];worst=max(worst,delta)
  assert np.all(bits[b]<=bits[a]),(label,states[a],states[b])
  max_healed=max(max_healed,int(m[a]-m[b]))
  if isinstance(label[0],int) and label[1].startswith('seal_'):seal_drift[a]+=delta
  else:nonseal_drift[a]+=delta
rhs=-(1-np.exp(-theta))*m*f
assert np.max(np.abs(seal_drift-rhs))<1e-12
assert np.max(nonseal_drift)<1e-12
out={'states':len(states),'coherent_edges':len(edges),'source_resolved_jump_bundles':len(jumps),'maximum_weighted_gain_minus_loss':worst,'max_certificates_healed_by_one_native_jump':max_healed,'seal_exact_drift_max_error':float(np.max(np.abs(seal_drift-rhs))),'scope':'two overlapping adapters with shared native PARK/W0; exact diagonal weighted gains from source-resolved injective retained-label reset maps. Analytic proof needed for general fixed degree.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
