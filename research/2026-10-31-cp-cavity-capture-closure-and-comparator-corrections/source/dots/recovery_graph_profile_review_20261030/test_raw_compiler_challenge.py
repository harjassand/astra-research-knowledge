import importlib.util, json, copy, random
from pathlib import Path
p=Path(__file__).parent/'raw_compiler_sources/acquire.py'
s=importlib.util.spec_from_file_location('review_acquire',p);mod=importlib.util.module_from_spec(s);s.loader.exec_module(mod)
raw=json.loads((p.parent/'raw_inputs.json').read_text());out={}
for name,net in raw.items():out[name]=mod.acquire(net)
# Independent raw mutation: a baseline departure can exhaust D into a mixed hold.
v=copy.deepcopy(raw['coupled']);v['reactions'].append(dict(name='extra_departure_via_mixed',source=dict(A=3,D=1,B=5),target=dict(A=2,C=1,E=1,B=5),rate='1'))
out['baseline_step_through_mixed']=mod.acquire(v)
# Two-D ingress and a two-copy restoring source, not CE support-only logic.
v=copy.deepcopy(raw['original']);v['species'].remove('C');v['reactions']=[r for r in v['reactions'] if 'C' not in r['source'] and 'C' not in r['target']]
v['reactions'] += [dict(name='A_to_E',source=dict(A=3,D=1,B=5),target=dict(A=2,E=1,D=1,B=5),rate='1'),dict(name='two_D_to_two_E',source=dict(A=2,D=2,B=5),target=dict(A=2,E=2,B=5),rate='1'),dict(name='two_E_restore',source=dict(A=2,E=2,B=5),target=dict(A=2,D=2,B=5),rate='1')]
out['two_D_ingress_two_E_restore']=mod.acquire(v)
# Non-A D-consuming birth without a matching restoration must fail.
v=copy.deepcopy(raw['original']);v['reactions'].append(dict(name='C_birth',source=dict(A=2,C=1,D=1,B=5),target=dict(A=2,C=2,B=5),rate='1'))
out['non_A_birth']=mod.acquire(v)
# Name/order independence of raw inferred decomposition.
v=copy.deepcopy(raw['coupled']);rename={x:'s'+str(i) for i,x in enumerate(reversed(v['species']))}
v['species']=[rename[x] for x in reversed(v['species'])]
for r in v['reactions']:
 r['source']={rename[x]:n for x,n in r['source'].items()};r['target']={rename[x]:n for x,n in r['target'].items()}
v['reactions'].reverse();out['renamed_reordered']=mod.acquire(v)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:{'status':v['status'],'L':v.get('pool_certificate',{}).get('L'),'trace':v.get('trace_certificate',{}).get('trace_total'),'attempts':v.get('attempts')} for k,v in out.items()},indent=2))
