"""Executable regression, distinct from infinite-state certificate proofs."""
import copy,json,random
from fractions import Fraction
from pathlib import Path
from acquire_integrated_phase_face import acquire
base=json.loads(Path(__file__).with_name('integrated_raw_inputs.json').read_text())['multi_step']
rng=random.Random(20261030);out=[]
for trial in range(4):
 net=copy.deepcopy(base)
 for r in net['reactions']:
  if r['name'].startswith('face_'):r['rate']=str(Fraction(rng.randint(1,5),rng.randint(1,5)))
 old=net['species'][:];fresh=[f'R{trial}_{i}' for i in range(len(old))];rng.shuffle(fresh);ren=dict(zip(old,fresh))
 net['species']=[ren[s] for s in old];rng.shuffle(net['species'])
 for r in net['reactions']:
  for key in ['source','target']:r[key]={ren[k]:v for k,v in r[key].items()}
 rng.shuffle(net['reactions']);a=acquire(net)
 assert a['status']=='PHASE_FACE_TRANSFER_CANDIDATE_FOUND',a
 face=a['face_potential_certificate']['acquired']
 assert face['catalyst']==ren['C'] and face['absorber']==ren['D']
 assert set(face['transient_types'])=={ren['E'],ren['F']}
 out.append(dict(trial=trial,status=a['status'],means=face['mean_vector'],trace=a['trace_certificate']['trace_total']))
for name,remove in [('missing_baseline','F_to_A'),('not_weakly_reversible','A_to_F')]:
 net=copy.deepcopy(base);net['reactions']=[r for r in net['reactions'] if r['name']!=remove]
 a=acquire(net);assert a['status']=='NO_CERTIFICATE_IN_THIS_CLASS',a
 out.append(dict(test=name,status=a['status'],attempts=a.get('attempts')))
print(json.dumps(out,indent=2));Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
