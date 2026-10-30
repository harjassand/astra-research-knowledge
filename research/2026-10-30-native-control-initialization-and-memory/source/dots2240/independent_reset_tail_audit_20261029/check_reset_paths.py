from pathlib import Path
from itertools import product
import json,hashlib
P=Path(__file__).parent
source=(P/'transactional_flags_source_snapshot.py').read_text()
ns={};exec(source.split('states=list(')[0],ns)
transitions=ns['transitions'];supports=ns['supports'];lengths=ns['lengths'];flag=ns['flag'];violates=ns['violates'];change=ns['change']
counts={'paths':0,'max_path':0,'max_clear':0,'C_R_paths':0,'max_C_R_path':0}
def path(s,h,short=False):
    seq=[]
    def take(ss,kind):
        nonlocal s
        assert any(t==ss and k==kind for t,k,_ in transitions(s)),(s,ss,kind)
        seq.append((h,kind));s=ss
    def reset(j,kind):take(change(s,j,('Q',0)),kind)
    def clear(j):
        start=len(seq);p=s[0][j];k=len(supports[j])
        if p[0]=='R': reset(j,'abort_reset')
        elif flag(j,p,s[1]):
            ix=next(i for i,r in enumerate(supports[j]) if violates(j,p,i,s[1][r]))
            take(change(s,j,('R',p,ix)),'abort_drive');reset(j,'abort_reset')
        p=s[0][j]
        if p[0]=='C':
            while s[0][j][1]<lengths[j]:take(change(s,j,('C',s[0][j][1]+1)),'gate')
            reset(j,'terminal_reset')
        p=s[0][j]
        if p[0]=='Q':
            for r in supports[j]:
                if s[1][r]==f'o{j}':take(change(s,q=r,l=f'z{j}'),'cleanup_drive')
                if s[1][r]==f'z{j}':take(change(s,q=r,l='f'),'cleanup_reset')
            while s[0][j][1]<k:take(change(s,j,('Q',s[0][j][1]+1)),'verify')
            take(change(s,j,('A',0)),'ready_reset')
        elif p[0]=='A':
            while s[0][j][1]>0:
                i=s[0][j][1];take(change(s,j,('A',i-1),supports[j][i-1],'f'),'unacquire')
        assert s[0][j]==('A',0) and all(s[1][r] not in {f'o{j}',f'z{j}'} for r in supports[j])
        counts['max_clear']=max(counts['max_clear'],len(seq)-start)
    if short:
        p=s[0][h]
        if p[0]=='R':reset(h,'abort_reset')
        elif flag(h,p,s[1]):
            j=next(j for j,r in enumerate(supports[h]) if violates(h,p,j,s[1][r]))
            take(change(s,h,('R',p,j)),'abort_drive');reset(h,'abort_reset')
        else:
            while s[0][h][1]<lengths[h]:take(change(s,h,('C',s[0][h][1]+1)),'gate')
            reset(h,'terminal_reset')
        return len(seq)
    clear(h)
    for j in range(len(supports)):
        if j!=h and set(supports[j])&set(supports[h]):clear(j)
    assert all(s[1][r]=='f' for r in supports[h])
    for i,r in enumerate(supports[h]):take(change(s,h,('A',i+1),r,f'o{h}'),'acquire')
    take(change(s,h,('C',0)),'commit_reset')
    for t in range(lengths[h]):take(change(s,h,('C',t+1)),'gate')
    reset(h,'terminal_reset')
    return len(seq)
for ps,ls in product(product(*ns['phases']),product(*ns['lockoptions'])):
    s=(ps,ls)
    for h,p in enumerate(ps):
        m=path(s,h);counts['paths']+=1;counts['max_path']=max(counts['max_path'],m)
        if p[0] in {'C','R'}:
            q=path(s,h,True);counts['C_R_paths']+=1;counts['max_C_R_path']=max(counts['max_C_R_path'],q)
            assert q<=max(2,lengths[h]+1)
        k=len(supports[h]);L=max(lengths);d=2
        bound=(1+k*(d-1))*(L+3*k+4)+k+L+2
        assert m<=bound
out={'status':'pass','scope':'Exhaustive actual clock-edge path eligibility, not a quantum probability or data-channel test',**counts,'snapshot_sha256':hashlib.sha256(source.encode()).hexdigest(),'full_alphabet_path_bound':46,'short_path_bound':4}
(P/'check_reset_paths.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
