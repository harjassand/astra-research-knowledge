from itertools import product
from collections import defaultdict
from pathlib import Path
import json
# Independent exhaustive finite record check, NOT a CP/probability test.
actions=[('kick',(0,)),('kick',(1,)),('kick',(0,1)),('reset',0),('reset',1)]
count=emissions=repeatcell=0
for n in range(8):
 for word in product(actions,repeat=n):
  last=[None,None];desc=defaultdict(list);byowner=defaultdict(list);cells=defaultdict(int)
  for i,(kind,arg) in enumerate(word):
   t=i+0.25
   if kind=='kick':
    for h in arg:last[h]=(i,t,arg)
   else:
    h=arg
    if last[h] is not None:
     k,tau,H=last[h];desc[k].append(h);byowner[h].append((tau,t));cells[(h,int(t//3))]+=1;emissions+=1
    last[h]=None
  for ds in desc.values():assert len(ds)==len(set(ds)) and len(ds)<=2
  for h,ivals in byowner.items():
   for (tau,u),(tau2,u2) in zip(ivals,ivals[1:]):assert tau2>u
   shortened=[(tau,3*int(u//3)) for tau,u in ivals if tau<3*int(u//3)]
   for (a,b),(c,d) in zip(shortened,shortened[1:]):assert b<=c
   percell=defaultdict(int)
   for tau,u in ivals:
    if tau<3*int(u//3):percell[int(u//3)]+=1
   assert all(x<=1 for x in percell.values())
  repeatcell+=sum(x>1 for x in cells.values());count+=1
out=dict(status='pass',records=count,marked_emissions_checked=emissions,repeated_owner_cell_instances=repeatcell,maximum_record_length=7,ancestor_owner_uniqueness=True,same_owner_full_intervals_disjoint=True,repeated_cell_at_most_one_prestart_ancestor=True,scope='Finite classical record algebra only; no quantum moment or tail certification')
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
