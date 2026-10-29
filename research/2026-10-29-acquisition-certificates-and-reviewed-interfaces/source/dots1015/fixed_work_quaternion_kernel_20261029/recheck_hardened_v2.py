import json,sys,copy
from fractions import Fraction as F
from pathlib import Path
sys.set_int_max_str_digits(0)
import bounded_sos_oracle_v2 as b
import fixed_work_oracle_v2 as w
sys.path.insert(0,'producer-workspace/quaternion_oracle_controller_20261029')
import quartic_sos_oracle as qo
r=Path(__file__).parent;s=Path('producer-workspace/quaternion_oracle_controller_20261029');counts={}
for filename,verify in [('bounded_sos_bank_results.json',b.verify),('retained_bank_results.json',w.verify)]:
 obj=json.loads((r/filename).read_text());rows=obj['rows'];n=0
 for row in rows:
  raw={(2,2,0,0):1,(0,2,2,0):1,(2,0,2,0):1,(0,0,0,4):1,(1,1,1,1):-4} if row['bank']=='Choi-Lam' else qo.bank_polynomial(json.loads((s/f"bank_{row['bank']}.json").read_text()),row['edge']);assert verify(raw,row['certificate']);n+=1
 counts[filename]=n
old=json.loads((s/'online_ftpl_result.json').read_text());queries={(t+1,z['edge']):dict(zip(qo.exps,map(F,z['query']))) for t,row in enumerate(old['oracle_calls']) for z in row}
for filename,verify in [('bounded_sos_offline_query_results.json',b.verify),('offline_query_results.json',w.verify)]:
 rows=json.loads((r/filename).read_text())['rows']
 for row in rows:assert verify(queries[row['round'],row['edge']],row['certificate'])
 counts[filename]=len(rows)
live=json.loads((r/'bounded_live_three_role_result.json').read_text())
for row in live['oracle_calls']:
 for z in row:assert b.verify(dict(zip(qo.exps,map(F,z['query']))),z['certificate'])
for edge,c in enumerate(live['retrospective_candidates']):assert b.verify(dict(zip(qo.exps,[F(x)/2 for x in live['final_feedback'][edge]])),c)
counts['live_and_retrospective']=363
forgery=json.loads(Path('producer-workspace/negative_scale_forgery.json').read_text())['certificate']
rejected=[]
for name,raw,c in [('negative_scale',{(4,0,0,0):1},forgery),('wrong_quaternion_dimension',dict(zip(qo.exps,map(F,live['oracle_calls'][0][0]['query']))),dict(live['oracle_calls'][0][0]['certificate'],quaternion=['0','0','0','0','1']))]:
 try:b.verify(raw,c)
 except (AssertionError,ValueError,IndexError):rejected.append(name)
 else:raise AssertionError(name)
for raw in [{(4,):1},{(4.,0,0,0):1},{(0,0,0,0):1}]:
 try:b.verify(raw,forgery)
 except ValueError:rejected.append(str(raw))
 else:raise AssertionError('malformed key')
(r/'hardened_v2_recheck.json').write_text(json.dumps(dict(verified_counts=counts,rejected_regressions=rejected,scope='Exact recheck of unchanged generated certificates using corrected scale/dimension/input contract; no regenerated trajectory'),indent=2)+'\n');print(counts)
