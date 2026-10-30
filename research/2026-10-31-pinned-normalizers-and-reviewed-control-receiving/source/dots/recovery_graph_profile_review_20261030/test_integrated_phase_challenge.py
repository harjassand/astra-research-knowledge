from pathlib import Path
import sys,json,copy
p=Path(__file__).parent/'integrated_phase_sources';sys.path.insert(0,str(p))
import acquire_integrated_phase_face as m
raw=json.loads((p/'integrated_raw_inputs.json').read_text());out={}
for k in ('old_coupled','multi_step','hidden_mass','closed_face_rejected'):out[k]=m.acquire(raw[k])
# Remove internal reverse: directed face remains transient and the full cycle remains reversible by paths.
v=copy.deepcopy(raw['multi_step']);v['reactions']=[r for r in v['reactions'] if r['name']!='face_F_to_E'];out['directed_two_stage']=m.acquire(v)
# A third transient stage, rational rates, full physical cycle connectivity retained.
v=copy.deepcopy(raw['multi_step']);v['species'].insert(-1,'W');v['reactions']=[r for r in v['reactions'] if not r['name'].startswith('face_')]
def add(y,z,name,rate):
 for w in (y,z):w['A']=w.get('A',0)+2;w['B']=5
 v['reactions'].append(dict(name=name,source=y,target=z,rate=rate))
add(dict(C=1,E=1),dict(C=1,F=1),'phase1','2/3')
add(dict(C=1,F=1),dict(C=1,E=1),'phaseback','1/5')
add(dict(C=1,F=1),dict(C=1,W=1),'phase2','3/2')
add(dict(C=1,W=1),dict(C=1,D=1),'phaserestore','7/4')
add(dict(W=1,D=1),dict(A=1,D=1),'W_to_A','1')
add(dict(A=1,D=1),dict(W=1,D=1),'A_to_W','1')
out['rational_three_stage']=m.acquire(v)
# Arbitrary labels and order should not supply hidden catalyst/pool knowledge.
v=copy.deepcopy(raw['multi_step']);ren={s:'r'+str(i) for i,s in enumerate(reversed(v['species']))};v['species']=[ren[s] for s in reversed(v['species'])]
for r in v['reactions']:
 for key in ('source','target'):r[key]={ren[s]:n for s,n in r[key].items()}
v['reactions'].reverse();out['renamed_reordered']=m.acquire(v)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
for k,r in out.items():
 f=r.get('face_potential_certificate') or {};print(k,r['status'],f.get('acquired',{}).get('mean_vector'),r.get('trace_certificate',{}).get('trace_total'))
