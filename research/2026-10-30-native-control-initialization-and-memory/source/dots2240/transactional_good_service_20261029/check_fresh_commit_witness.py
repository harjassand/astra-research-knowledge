"""Clock regression for reset->fresh-commit->terminal certificate; not probability proof."""
from pathlib import Path
from collections import deque
import runpy,io,contextlib,json
with contextlib.redirect_stdout(io.StringIO()):
    a=runpy.run_path('producer-workspace/check_transactional_flags.py')
states=a['states'];trans=a['transitions'];flag=a['flag']
checks=0;entry_checks=0
for ps,ls in states:
    for ss,kind,_ in trans((ps,ls)):
        for h in range(2):
            if ps[h]==ss[0][h]:continue
            if kind in ('terminal_reset','abort_reset'):
                assert ss[0][h]==('Q',0)
                assert not flag(h,ss[0][h],ss[1]);checks+=1
            if kind=='abort_reset':assert flag(h,ps[h],ls)
            p,q=ps[h],ss[0][h]
            old=p[0]=='C' or p[0]=='R' and p[1][0]=='C'
            new=q[0]=='C' or q[0]=='R' and q[1][0]=='C'
            if new and not old:assert kind=='commit_reset';entry_checks+=1
# Multi-source reachability: from any Q0 configuration, no terminal is reachable
# without an actual commitment of the selected owner.
results=[]
for h in range(2):
    seen={(ps,ls) for ps,ls in states if ps[h]==('Q',0)};todo=deque(seen);edges=0
    while todo:
        s=todo.popleft()
        for ss,kind,_ in trans(s):
            changes_h=ss[0][h]!=s[0][h]
            if changes_h and kind=='commit_reset':continue
            assert not (changes_h and kind=='terminal_reset'),(h,s,ss)
            edges+=1
            if ss not in seen:seen.add(ss);todo.append(ss)
    results.append({'owner':h,'reachable_states_without_own_commit':len(seen),'edges_checked':edges})
out={'scope':'Clock eligibility and complete-reset destination checks only; quantum/probability claims use proofs',
'configurations':len(states),'reset_destination_checks':checks,'only_commit_enters_computation_checks':entry_checks,
'no_terminal_from_Q0_without_fresh_commit':results,'passed':True}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
