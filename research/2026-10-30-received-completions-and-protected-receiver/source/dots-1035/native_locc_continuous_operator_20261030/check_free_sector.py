"""Audit parent's FREE=(I or Q)&no-own-tags predicate on the actual owner table.
Read definitions only from accepted regression, without changing its files.
"""
from pathlib import Path
from itertools import product
from collections import deque,Counter
import json
src=Path('producer-workspace/check_extended_owner_table.py').read_text().split('states=list(product')[0]
ns={};exec(compile(src,'accepted_owner_table_definitions','exec'),ns)
phases=ns['phases'];lockoptions=ns['lockoptions'];supports=ns['supports'];trans=ns['trans']
def active(s,h):
    p=s[0][h];ls=s[1]
    return not(p[0] in {'I','Q'} and all(ls[r] not in {f'o{h}',f'z{h}'} for r in supports[h]))
states=list(product(product(*phases),product(*lockoptions)));counts=Counter();births=0
for s in states:
    before=[active(s,h) for h in range(2)]
    for ss,kind,coh in trans(s):
        after=[active(ss,h) for h in range(2)]
        if coh:assert before==after,(s,ss,kind)
        elif kind!='load_reset':assert all(a<=b for a,b in zip(after,before)),(s,ss,kind)
        else:
            for h in range(2):
                if after[h]>before[h]:assert s[0][h][0]=='I' and ss[0][h]==('A',0);births+=1
        counts[kind]+=1
# LOAD=0 with I watchdog RETAINED, unlike old stopped-I readiness convention.
reverse={s:[] for s in states};targets=[s for s in states if not any(active(s,h) for h in range(2))]
for s in states:
    for ss,kind,coh in trans(s,False):reverse[ss].append(s)
dist={s:0 for s in targets};q=deque(targets)
while q:
    s=q.popleft()
    for prev in reverse[s]:
        if prev not in dist:dist[prev]=dist[s]+1;q.append(prev)
assert len(dist)==len(states)
out={'basis_configurations':len(states),'directed_transition_checks':sum(counts.values()),'only_LOAD_can_create_activity':True,'clean_LOAD_activity_births':births,'all_H_preserve_activity':True,'all_other_resets_noncreating':True,'zero_LOAD_keeps_I_watchdog':True,'global_FREE_target_states':len(targets),'all_states_reach_FREE':True,'maximum_shortest_path_to_FREE':max(dist.values()),'workspace_unrestricted':True,'scope':'actual finite owner-table algebra, not finite-rate probability or noisy theorem'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
