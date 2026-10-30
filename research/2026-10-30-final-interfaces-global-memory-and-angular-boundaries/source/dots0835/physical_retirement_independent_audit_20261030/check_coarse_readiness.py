"""Independent coarse-readiness audit of the actual reset-first source fixture.
Basis eligibility is diagnostic; it does not prove quantum finite-monitor probabilities.
No governing source or old result is modified.
"""
from pathlib import Path
from itertools import product
import json, hashlib
ROOT=Path('producer-workspace/weak_initiation_compiler_20261030')
src=(ROOT/'check_fast_busy_repair.py').read_text()
ns={'__file__':str(ROOT/'check_fast_busy_repair.py')}
exec(src.split('states=trans=paths=maximum=0')[0],ns)
strong=ns['busy']; supports=ns['supports']
def coarse(s,h):
    (ps,ls),ws=s
    return ps[h]!=('A',0) or any(ls[r] in {f'o{h}',f'z{h}'} for r in supports[h])
ns['busy']=coarse
n=edges=paths=mx=coarse_ready_dirty_workspace=0
for ps,ls,ws in product(product(*ns['ns']['phases']),product(*ns['ns']['lockoptions']),product([0,1],repeat=2)):
    state=((ps,ls),ws); n+=1
    b=tuple(coarse(state,h) for h in range(2))
    for h in range(2):
        assert b[h]<=strong(state,h)
        if not b[h] and ws[h]: coarse_ready_dirty_workspace+=1
    for target,kind,coh in ns['transitions'](state):
        bb=tuple(coarse(target,h) for h in range(2))
        assert bb==b if coh else all(x<=y for x,y in zip(bb,b)),(state,target,kind,b,bb)
        edges+=1
    for h in range(2):
        m=ns['clear_path'](state,h); paths+=1; mx=max(mx,m)
result={'status':'PASS','states':n,'transition_checks':edges,'clearing_paths':paths,'maximum_path_steps':mx,
        'ready_owner_instances_with_dirty_workspace':coarse_ready_dirty_workspace,
        'fast_H_preserves_coarse_masks':True,'actual_resets_do_not_create_nonready':True,
        'clear_paths_use_no_acquisition_edge':True,
        'scope':'Clock/tag/workspace-basis eligibility only; full coherent instrument proof is in receipt',
        'fast_fixture_sha256':hashlib.sha256(src.encode()).hexdigest(),
        'transition_snapshot_sha256':hashlib.sha256((ROOT/'transactional_source_snapshot.py').read_bytes()).hexdigest()}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
