from pathlib import Path
from itertools import product
from collections import deque
import json
P=Path(__file__).parent
ns={};exec((P/'check_transactional_flags.py').read_text().split('states=list(')[0],ns)
states=list(product(product(*ns['phases']),product(*ns['lockoptions'])))
ix={s:i for i,s in enumerate(states)}
rev=[[] for s in states];events=[set(),set()];n=0; R_cleanup_forbidden_checks=0;commit_checks=0
for i,s in enumerate(states):
 for t,kind,coherent in ns['transitions'](s):
  rev[ix[t]].append(i);n+=1
  changed=[h for h in range(2) if s[0][h]!=t[0][h]]
  if kind in {'terminal_reset','abort_reset'}:
   assert not coherent and len(changed)==1
   h=changed[0];assert t[0][h]==('Q',0)
   events[h].add(i)
  if kind=='commit_reset':
   assert not coherent and len(changed)==1
   h=changed[0];assert s[0][h]==('A',len(ns['supports'][h])) and t[0][h]==('C',0)
   commit_checks+=1
  for h in range(2):
   if s[0][h][0]=='R':
    for r in ns['supports'][h]:
     if s[1][r]==f'o{h}':
      assert t[1][r]==f'o{h}'
      R_cleanup_forbidden_checks+=1
maxdist=[]
for h in range(2):
 dist={i:1 for i in events[h]};q=deque(dist)
 while q:
  i=q.popleft()
  for j in rev[i]:
   if j not in dist:dist[j]=dist[i]+1;q.append(j)
 assert len(dist)==len(states)
 maxdist.append(max(dist.values()))
# A direct counterexample to claiming all R belongs to an invariant C/R_C sector.
s=((('R',('A',0),0),('A',0)),('o0','f','f'))
assert any(t[0][0]==('A',0) and kind=='unabort_drive' for t,kind,c in ns['transitions'](s))
out=dict(status='pass',states=len(states),transitions=n,all_states_reach_each_owners_actual_event=True,max_shortest_event_steps=maxdist,commit_edges_non_event_and_irreversible=commit_checks,R_owned_tag_preservation_checks=R_cleanup_forbidden_checks,all_R_short_iteration_counterexample_confirmed=True,scope='Independent finite graph reachability/event typing only; no quantum probability certification')
(P/'independent_graph_checks.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
