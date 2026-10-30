"""Exhaustive arbitrary-clock-state audit, not merely clean reachable states.
No epochs; counter/owner checks and abort labels are explicit local predicates.
"""
from itertools import product
from collections import Counter
from pathlib import Path
import json,hashlib
supports=[(0,1),(1,2)];lengths=[3,2];gate_targets=[(0,1,0),(1,2)]
base=[];phases=[]
for h in range(2):
    k=len(supports[h]);b=[('A',i) for i in range(k+1)]+[('G',i) for i in range(1,lengths[h]+1)]+[('Q',i) for i in range(k+1)]
    base.append(b)
    rs=[]
    for p in b:
        for j in range(k):
            if p[0]!='Q' or j<p[1]:rs.append(('R',p,j))
    phases.append(b+rs)
lockoptions=[('f','o0','z0'),('f','o0','z0','o1','z1'),('f','o1','z1')]
def violates(h,p,j,l):
    own={f'o{h}',f'z{h}'};typ,i=p[:2]
    if typ=='A':return l!=f'o{h}' if j<i else l in own
    if typ=='G':return l!=f'o{h}'
    if typ=='Q':return j<i and l in own
    raise ValueError('R is not a tested normal phase')
def flag(h,p,ls):
    return p[0]=='R' or any(violates(h,p,j,ls[q]) for j,q in enumerate(supports[h]))
def claims(h,p,j):
    return p[0]=='G' or p[0]=='A' and j<p[1]
def change(s,h=None,p=None,q=None,l=None):
    ps=list(s[0]);ls=list(s[1])
    if h is not None:ps[h]=p
    if q is not None:ls[q]=l
    return tuple(ps),tuple(ls)
def transitions(s):
    ps,ls=s
    for h,p in enumerate(ps):
        k=len(supports[h]);typ,i=p[:2]
        if typ=='A':
            if i<k and ls[supports[h][i]]=='f':yield change(s,h,('A',i+1),supports[h][i],f'o{h}'),'acquire',True
            if i>0 and ls[supports[h][i-1]]==f'o{h}':yield change(s,h,('A',i-1),supports[h][i-1],'f'),'unacquire',True
        t=0 if p==('A',k) else i if typ=='G' else None
        if t is not None:
            if t<lengths[h] and ls[gate_targets[h][t]]==f'o{h}':yield change(s,h,('G',t+1)),'gate',True
            if t>0 and ls[gate_targets[h][t-1]]==f'o{h}':yield change(s,h,('A',k) if t==1 else ('G',t-1)),'ungate',True
            if t==lengths[h]:yield change(s,h,('Q',0)),'terminal_reset',False
        if typ=='Q':
            if i<k and ls[supports[h][i]] not in {f'o{h}',f'z{h}'}:yield change(s,h,('Q',i+1)),'verify',True
            if i>0 and ls[supports[h][i-1]] not in {f'o{h}',f'z{h}'}:yield change(s,h,('Q',i-1)),'unverify',True
            if i==k:yield change(s,h,('A',0)),'ready_reset',False
        if typ!='R':
            for j,q in enumerate(supports[h]):
                if violates(h,p,j,ls[q]):yield change(s,h,('R',p,j)),'abort_drive',True
        else:
            old,j=p[1:];q=supports[h][j]
            if violates(h,old,j,ls[q]):yield change(s,h,old),'unabort_drive',True
            yield change(s,h,('Q',0)),'abort_reset',False
    for q,l in enumerate(ls):
        if l=='f':continue
        h=int(l[1]);j=supports[h].index(q)
        enabled=not claims(h,ps[h],j)
        if l[0]=='o' and enabled:yield change(s,q=q,l=f'z{h}'),'cleanup_drive',True
        if l[0]=='z':
            if enabled:yield change(s,q=q,l=f'o{h}'),'uncleanup_drive',True
            yield change(s,q=q,l='f'),'cleanup_reset',False
states=list(product(product(*phases),product(*lockoptions)))
counts=Counter();badcounts=Counter();n=0
for ps,ls in states:
    s=(ps,ls);before=tuple(flag(h,ps[h],ls) for h in range(2));badcounts[before]+=1
    for ss,kind,coherent in transitions(s):
        after=tuple(flag(h,ss[0][h],ss[1]) for h in range(2))
        if coherent:assert before==after,(s,ss,kind,before,after)
        else:assert all(a<=b for a,b in zip(after,before)),(s,ss,kind,before,after)
        counts[kind]+=1;n+=1
# Regression: A0 with own first lock is bad and has explicit repair paths.
trap=((('A',0),('A',0)),('o0','f','f'))
assert flag(0,trap[0][0],trap[1])
assert any(k=='abort_drive' for _,k,_ in transitions(trap))
assert any(k=='cleanup_drive' for _,k,_ in transitions(trap))
out={'scope':'All clock basis states, including arbitrary corrupted phases/locks; quantum-history defects not included',
'phases_per_hub':[len(x) for x in phases],'clock_states':len(states),'directed_transition_checks':n,
'all_H_edges_preserve_every_owner_flag':True,'all_resets_only_decrease_flags':True,
'counter_reset_self_orphan_has_repair':True,'transition_counts':dict(counts),
'flag_pattern_counts':{str(k):v for k,v in badcounts.items()},'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
