"""Exhaustive weak-first-edge OFF + unconditional acquisition-abort repair audit.
Workspace is a clean/dirty basis bit; DATA is arbitrary and absent from this flag test.
"""
from pathlib import Path
from itertools import product
import json, hashlib
P=Path(__file__).parent
source=(P/'transactional_source_snapshot.py').read_text();ns={}
exec(source.split('states=list(')[0],ns)
oldtrans=ns['transitions'];supports=ns['supports'];lengths=ns['lengths'];change=ns['change'];flag=ns['flag'];violates=ns['violates']
def transitions(s):
    clock,ws=s
    for t,kind,coh in oldtrans(clock):
        hs=[h for h in range(2) if clock[0][h]!=t[0][h]]
        if kind=='acquire' and any(clock[0][h]==('A',0) for h in hs):continue
        if kind=='unacquire' and any(t[0][h]==('A',0) for h in hs):continue
        w=list(ws)
        if kind in {'commit_reset','terminal_reset','abort_reset','ready_reset'}:
            assert len(hs)==1;w[hs[0]]=0
        yield (t,tuple(w)),kind,coh
    for h,p in enumerate(clock[0]):
        if p[0]=='A' and p[1]>=1:
            w=list(ws);w[h]=0
            yield (change(clock,h,('Q',0)),tuple(w)),'acquisition_abort_reset',False
        if p[0] in {'A','Q'}:
            w=list(ws);w[h]=0
            yield (clock,tuple(w)),'workspace_refresh',False

def busy(s,h):
    (ps,ls),ws=s
    return ps[h]!=('A',0) or ws[h]!=0 or any(ls[r] in {f'o{h}',f'z{h}'} for r in supports[h])

def clear_path(s,h):
    seq=[]
    def take(t,kind):
        nonlocal s
        assert any(x==t and k==kind for x,k,_ in transitions(s)),(s,t,kind)
        seq.append(kind);s=t
    def update(p=None,r=None,l=None,reset=False,kind=None):
        w=list(s[1]);w[h]=0 if reset else w[h]
        take((change(s[0],h if p is not None else None,p,r,l),tuple(w)),kind)
    p=s[0][0][h]
    if p[0]=='A' and p[1]>=1:update(('Q',0),reset=True,kind='acquisition_abort_reset')
    elif p[0]=='R':update(('Q',0),reset=True,kind='abort_reset')
    elif flag(h,p,s[0][1]):
        j=next(j for j,r in enumerate(supports[h]) if violates(h,p,j,s[0][1][r]))
        update(('R',p,j),kind='abort_drive');update(('Q',0),reset=True,kind='abort_reset')
    p=s[0][0][h]
    if p[0]=='C':
        while s[0][0][h][1]<lengths[h]:update(('C',s[0][0][h][1]+1),kind='gate')
        update(('Q',0),reset=True,kind='terminal_reset')
    p=s[0][0][h]
    if p[0]=='Q':
        for r in supports[h]:
            if s[0][1][r]==f'o{h}':update(r=r,l=f'z{h}',kind='cleanup_drive')
            if s[0][1][r]==f'z{h}':update(r=r,l='f',kind='cleanup_reset')
        while s[0][0][h][1]<len(supports[h]):update(('Q',s[0][0][h][1]+1),kind='verify')
        update(('A',0),reset=True,kind='ready_reset')
    elif p==('A',0) and s[1][h]:update(reset=True,kind='workspace_refresh')
    assert not busy(s,h),(s,h,seq)
    assert all(k not in {'acquire','unacquire'} for k in seq)
    return len(seq)

states=trans=paths=maximum=0
for ps,ls,ws in product(product(*ns['phases']),product(*ns['lockoptions']),product([0,1],repeat=2)):
    s=((ps,ls),ws);states+=1
    before=tuple(busy(s,h) for h in range(2))
    for ss,kind,coh in transitions(s):
        after=tuple(busy(ss,h) for h in range(2))
        assert before==after if coh else all(a<=b for a,b in zip(after,before)),(s,ss,kind,before,after)
        trans+=1
    for h in range(2):
        steps=clear_path(s,h);paths+=1;maximum=max(maximum,steps)
        assert steps<=max(lengths)+3*len(supports[h])+4
out={'status':'pass','states_including_clean_dirty_workspace_bits':states,'directed_transition_checks':trans,'owner_clearing_paths':paths,'maximum_path_steps':maximum,'conservative_path_bound':13,'fast_H_preserves_every_busy_flag':True,'resolved_fast_resets_only_decrease_busy_flags':True,'no_path_uses_any_acquisition_edge':True,'scope':'Full clock/lock/workspace-basis eligibility and Boolean flags; operator block argument and finite-rate probability supplied separately','source_snapshot_sha256':hashlib.sha256(source.encode()).hexdigest()}
print(json.dumps(out,indent=2))
