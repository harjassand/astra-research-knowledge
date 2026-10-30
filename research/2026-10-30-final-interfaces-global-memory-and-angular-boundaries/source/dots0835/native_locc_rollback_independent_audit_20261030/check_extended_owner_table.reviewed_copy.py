"""Exhaustive all-basis-label check of the new I/A/C/B/Q/R machine.
Checks classical predicate identities underpinning operator no-creation;
not a substitute for quantum instruments/probability estimates.
"""
from itertools import product
from collections import Counter, deque
from pathlib import Path
import json
supports=[(0,1),(1,2)]; lengths=[2,1]; gate_targets=[(0,1),(1,)]
base=[]; phases=[]
for h,k in enumerate(map(len,supports)):
    b=[('I',0)]+[('A',i) for i in range(k+1)]+[('C',i) for i in range(lengths[h]+1)]+[('B',j,l) for j in range(lengths[h]+1) for l in range(j+1)]+[('Q',i) for i in range(k+1)]
    base.append(b)
    rr=[('R',p,j) for p in b for j in range(k) if p[0]!='Q' or j<p[1]]
    phases.append(b+rr)
lockoptions=[('f','o0','z0'),('f','o0','z0','o1','z1'),('f','o1','z1')]
def violates(h,p,j,l):
    own={f'o{h}',f'z{h}'}; typ=p[0]
    if typ=='I':return l in own
    if typ=='A':return l!=f'o{h}' if j<p[1] else l in own
    if typ in {'C','B'}:return l!=f'o{h}'
    if typ=='Q':return j<p[1] and l in own
    raise ValueError(p)
def flag(h,p,ls):
    return p[0]=='R' or any(violates(h,p,j,ls[q]) for j,q in enumerate(supports[h]))
def claims(h,p,j):
    return p[0] in {'C','B','R'} or p[0]=='A' and j<p[1]
def compute(p):return p[0] in {'C','B'} or p[0]=='R' and p[1][0] in {'C','B'}
def ch(s,h=None,p=None,q=None,l=None):
    ps=list(s[0]);ls=list(s[1])
    if h is not None:ps[h]=p
    if q is not None:ls[q]=l
    return tuple(ps),tuple(ls)
def trans(s, launches=True):
    ps,ls=s
    for h,p in enumerate(ps):
        k=len(supports[h]); typ=p[0]
        if typ=='I' and launches:yield ch(s,h,('A',0)),'load_reset',False
        if typ=='A':
            i=p[1]
            if i<k and ls[supports[h][i]]=='f':yield ch(s,h,('A',i+1),supports[h][i],f'o{h}'),'acquire',True
            if i>0 and ls[supports[h][i-1]]==f'o{h}':yield ch(s,h,('A',i-1),supports[h][i-1],'f'),'unacquire',True
            if i==k:yield ch(s,h,('C',0)),'commit_reset',False
        if typ=='C':
            t=p[1]
            if t<lengths[h] and ls[gate_targets[h][t]]==f'o{h}':yield ch(s,h,('C',t+1)),'gate',True
            if t>0 and ls[gate_targets[h][t-1]]==f'o{h}':yield ch(s,h,('C',t-1)),'ungate',True
            if t==lengths[h]:yield ch(s,h,('Q',0)),'terminal_reset',False
            yield ch(s,h,('B',t,t)),'watchdog_to_rollback',False
        if typ=='B':
            j,l=p[1:]
            if l>0 and ls[gate_targets[h][l-1]]==f'o{h}':yield ch(s,h,('B',j,l-1)),'rollback_inverse',True
            if l<j and ls[gate_targets[h][l]]==f'o{h}':yield ch(s,h,('B',j,l+1)),'rollback_forward',True
            if l==0:yield ch(s,h,('Q',0)),'rollback_reset',False
        if typ=='Q':
            i=p[1]
            if i<k and ls[supports[h][i]] not in {f'o{h}',f'z{h}'}:yield ch(s,h,('Q',i+1)),'verify',True
            if i>0 and ls[supports[h][i-1]] not in {f'o{h}',f'z{h}'}:yield ch(s,h,('Q',i-1)),'unverify',True
            if i==k:yield ch(s,h,('I',0)),'ready_reset',False
        if typ in {'I','A','Q','R'}:yield ch(s,h,('Q',0)),'watchdog_complete_reset',False
        if typ!='R':
            for j,q in enumerate(supports[h]):
                if violates(h,p,j,ls[q]):yield ch(s,h,('R',p,j)),'abort_drive',True
        else:
            old,j=p[1:];q=supports[h][j]
            if violates(h,old,j,ls[q]):yield ch(s,h,old),'unabort_drive',True
            yield ch(s,h,('Q',0)),'abort_reset',False
    for q,l in enumerate(ls):
        if l=='f':continue
        h=int(l[1]);j=supports[h].index(q);enabled=not claims(h,ps[h],j)
        if l[0]=='o' and enabled:yield ch(s,q=q,l=f'z{h}'),'cleanup_drive',True
        if l[0]=='z':
            if enabled:yield ch(s,q=q,l=f'o{h}'),'uncleanup_drive',True
            yield ch(s,q=q,l='f'),'cleanup_reset',False
states=list(product(product(*phases),product(*lockoptions)))
counts=Counter();hold=0;watch=0
for s in states:
    ps,ls=s;before=tuple(flag(h,ps[h],ls) for h in range(2))
    for ss,kind,coherent in trans(s):
        after=tuple(flag(h,ss[0][h],ss[1]) for h in range(2))
        assert before==after if coherent else all(a<=b for a,b in zip(after,before)),(s,ss,kind,before,after)
        for h,p in enumerate(ps):
            if compute(p) and compute(ss[0][h]):
                assert all((ls[r]==f'o{h}')==(ss[1][r]==f'o{h}') for r in supports[h]),(s,ss,kind,h)
                hold+=1
            if compute(p) and not compute(ss[0][h]):
                assert kind in {'terminal_reset','rollback_reset','abort_reset','watchdog_complete_reset'} and ss[0][h]==('Q',0)
        if kind=='watchdog_to_rollback':watch+=1
        counts[kind]+=1
# Complete graph backwards reachability proves an actual finite path to global ready
# from EVERY malformed state after launch is disabled; complete watchdog is disabled
# at truly ready I so that target is absorbing for this stop-mode check.
ready=((('I',0),('I',0)),('f','f','f'))
reverse={s:[] for s in states}
for s in states:
    for ss,kind,coh in trans(s,False):
        # Nominal park rule suppresses I watchdog; I inconsistency repairs remain.
        if kind=='watchdog_complete_reset' and any(s[0][h][0]=='I' and ss[0][h]!=s[0][h] for h in range(2)):continue
        reverse[ss].append(s)
dist={ready:0};queue=deque([ready])
while queue:
    s=queue.popleft()
    for prev in reverse[s]:
        if prev not in dist:dist[prev]=dist[s]+1;queue.append(prev)
assert len(dist)==len(states),(len(dist),len(states))
# Regression demonstrating why a blocked rollback needs dirty consistency abort.
blocked=((('B',1,1),('I',0)),('f','f','f'))
assert any(k=='abort_drive' for _,k,_ in trans(blocked))
assert not any(k=='rollback_inverse' for _,k,_ in trans(blocked))
out={'states':len(states),'phases_per_owner':[len(p) for p in phases], 'directed_transitions':sum(counts.values()),'transition_counts':dict(counts),'no_creation_all_labels':True,'compute_ownership_conservation_checks':hold,'watchdog_equal_prefix_transitions':watch,'park_all_states_reach_ready':True,'maximum_shortest_park_path':max(dist.values()),'blocked_rollback_explicit_dirty_exit':True,'scope':'All basis labels. Operator history/no-creation and probability arguments are separately proved in manuscript.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
