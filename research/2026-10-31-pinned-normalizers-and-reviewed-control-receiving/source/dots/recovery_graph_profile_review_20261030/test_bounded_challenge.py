import sys,importlib.util,json,copy,random
from pathlib import Path
from fractions import Fraction as F
p=Path(__file__).parent;sys.path.insert(0,str(p/'integrated_phase_sources'))
def load(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
new=load('bounded_review',p/'bounded_sources/acquire_bounded_rank_face.py');old=load('rank_review',p/'rank_sources/acquire_rank_face.py')
raw=json.loads((p/'bounded_sources/raw_inputs.json').read_text());out={};checks=0
for name,net in raw.items():
 result=new.acquire(net);out[name]={'new':result,'old_status':old.acquire(net)['status']}
 pc=result['pool_certificate'];D=result['residual_species'].index(result['pivot']);k=len(result['residual_species']);pp=pc['pools'];dr=pc['protected_pool']
 for rec in pc['bounded_extras']:
  i=rec['source_pool'];co=list(map(F,rec['shifted_variable_coefficients']));c=F(rec['shifted_constant']);b=F(rec['per_label_bound'])
  for _ in range(100):
   vv=[random.Random(checks+j).randint(0,20) for j in range(k)];Y=sum(vv[j] for j in pp[i])
   if Y:assert c+sum(q*v for q,v in zip(co,vv))<=b*Y;checks+=1
 expected=max([F(0)]+[sum(F(e['rate']) for e in pc['baseline_edges'] if e['source']==i)+sum(F(e['per_label_bound']) for e in pc['bounded_extras'] if e['source_pool']==i) for i in range(len(pp))])
 assert expected==F(pc['rank_certificate']['residual_clock_bound'])
 assert all(e['target_pool']==0 for e in pc['unbounded_rank_nonincreasing_extras'])
# Scale the formerly blocked uphill term to a large fixed rational rate, not an unbounded control.
v=copy.deepcopy(raw['blocked_rank'])
for r in v['reactions']:
 if r['name']=='extra_E_to_C':r['rate']='1000/3'
out['large_fixed_uphill']=dict(new=new.acquire(v),old_status=old.acquire(v)['status'])
# Retained non-A D-consuming boundary must still reject.
v=copy.deepcopy(raw['blocked_rank']);v['reactions'].append(dict(name='unbounded_C_birth',source=dict(A=2,C=1,D=1,B=5),target=dict(A=2,C=2,B=5),rate='1'))
out['bad_cross_boundary']=dict(new=new.acquire(v),old_status=old.acquire(v)['status'])
Path(__file__).with_suffix('.json').write_text(json.dumps(dict(rate_bound_checks=checks,comparisons=out),indent=2)+'\n')
for name,z in out.items():print(name,z['new']['status'],z['old_status'],z['new'].get('pool_certificate',{}).get('rank_certificate'))
print('rate_bound_checks',checks)
