"""Actual inherited finite owner table + PARK, fixed pause masks.
Uses no collapsed retirement primitive. Basis-predicate diagnostic only;
finite quantum path effects and clean adapter provenance need separate proof.
"""
from pathlib import Path
import json
p=Path('producer-workspace/check_extended_owner_table.py')
ns={}; exec(p.read_text().split('states=list(product(')[0],ns)
product,Counter,deque=ns['product'],ns['Counter'],ns['deque']
oldv=ns['violates']; oldtrans=ns['trans']
ns['violates']=lambda h,p,j,l: False if p[0]=='PARK' else oldv(h,p,j,l)
phases=[ps+[('PARK',0)] for ps in ns['phases']]
states=list(product(product(*phases),product(*ns['lockoptions'])))
def trans(s,pauses):
 for ss,kind,coh in oldtrans(s):
  h=next((h for h in range(2) if s[0][h]!=ss[0][h]),None)
  if kind=='load_reset' and pauses[h]:continue
  if kind=='ready_reset' and pauses[h]:ss=ns['ch'](ss,h,('PARK',0))
  yield ss,kind,coh
 for h,p in enumerate(s[0]):
  if p[0]=='PARK':
   if pauses[h]:yield s,'quiescent_W_reset',False
   else:yield ns['ch'](s,h,('Q',0)),'unpark_via_Q_W_reset',False
nedge=0;badstrict=0;reach={}
for pauses in product((0,1),repeat=2):
 reverse={s:[] for s in states}
 targets=[]
 for s in states:
  flags=tuple(ns['flag'](h,s[0][h],s[1]) for h in range(2))
  if all(s[0][h][0]==('PARK' if pauses[h] else 'I') and all(s[1][r] not in {f'o{h}',f'z{h}'} for r in ns['supports'][h]) for h in range(2)):targets.append(s)
  for ss,kind,coh in trans(s,pauses):
   nedge+=1; reverse[ss].append(s)
   after=tuple(ns['flag'](h,ss[0][h],ss[1]) for h in range(2))
   assert (after==flags) if coh else all(a<=b for a,b in zip(after,flags)),(s,ss,kind)
   for h in range(2):
    if s[0][h][0]=='PARK' and pauses[h]:assert ss[0][h][0]=='PARK',(s,ss,kind)
   if kind=='quiescent_W_reset':
    # If PARK consistency required no-own, this gain would NOT heal it.
    badstrict+=any(s[0][h][0]=='PARK' and pauses[h] and any(s[1][r] in {f'o{h}',f'z{h}'} for r in ns['supports'][h]) for h in range(2))
 dist={s:0 for s in targets};q=deque(targets)
 while q:
  s=q.popleft()
  for prev in reverse[s]:
   if prev not in dist:dist[prev]=dist[s]+1;q.append(prev)
 assert len(dist)==len(states),(pauses,len(dist),len(states))
 reach[str(pauses)]={'reachable_states':len(dist),'maximum_shortest_path':max(dist.values())}
out={'states_per_fixed_pause_mask':len(states),'directed_edges_all_masks':nedge,'full_table_structural_no_creation':True,'held_PARK_absorbing_in_phase':True,'all_states_reach_no_own_target':reach,'strict_no_own_PARK_not_healed_by_milestone_cases':badstrict,'PARK_good_convention':'W=0 with arbitrary tags; NOT-CLAIM and identity frame','scope':'actual inherited label table; workspace reset/range proof and finite monitored probability are separate; malformed adapter erase phases not included'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
