from pathlib import Path
import sys,json,gzip,copy,tempfile,hashlib
p=Path('producer-workspace/feedback_extension');sys.path.insert(0,str(p))
import replay_polynomial_feedback as x
base=(p.parent/'history_sensitive_4096_result.json').read_bytes();model=json.loads(base)
records=json.loads(gzip.decompress((p.parent/'history_sensitive_4096_observations.json.gz').read_bytes()))['records'];local=json.loads((p/'block_comparison_results.json').read_text())
args=dict(expected_b=model['task_b'],expected_ell_num=model['task_ell_numer'],expected_ell_den=model['task_ell_denominator'],expected_length=24,expected_tolerance=x.R(1,50),expected_confidence=x.R(1,1000),expected_generators=2,expected_base_sha=x.BASE_SHA,base_bytes=base)
# ONLY negative receiving tests: full real base and all 32 norms were independently replayed first.
# Cache exact frozen inputs, never accept a changed operator/probe as an existing result.
coarse=[z for z in records if z['kind']=='coarse'];parts=model['partition'];n=model['n'];which=[0]*n;within=[0]*n
for g,pp in enumerate(parts):
 for j,i in enumerate(pp):which[i]=g;within[i]=j
cache={}
def key(rows,N,parts,delta,probe):return hashlib.sha256(repr((rows,N,parts,str(delta),probe)).encode()).hexdigest()
for z in local['local_certificates']:
 a,g,h=z['a'],z['source_block'],z['target_block'];src=parts[g];k=len(src);d=k+len(parts[h]);rows=[[] for _ in range(d)]
 for ii,i in enumerate(src):rows[ii]=[(k+within[j],v) for j,v in coarse[a]['counts'][i] if which[j]==h]
 N=sum(v for row in rows for _,v in row)
 if N:cache[key(rows,N,[list(range(k)),list(range(k,d))],x.R(1,1000)/(8*2*4*4),z['certificate']['probe'])]=copy.deepcopy(z['certificate'])
def cached(rows,N,parts,delta,forced_probe):return copy.deepcopy(cache[key(rows,N,parts,delta,forced_probe)])
def cached_base(mm,rr,**kw):
 assert mm==model and rr==records
 return 0
x.upper_norm=cached;x.replay_base=cached_base
ok=x.replay(model,records,local,**args);assert ok['status']=='PASS_POLYNOMIAL_OFFLINE_FEEDBACK'
checks=1
mut=[]
def add(f):
 z=copy.deepcopy(local);f(z);mut.append(z)
add(lambda z:z.update(model_bound='0'));add(lambda z:z.update(alpha='0'));add(lambda z:z.update(additional_integer_products=0));add(lambda z:z.update(status='INCONCLUSIVE_THIS_CERTIFICATE'))
add(lambda z:z['comparison_matrix'][0].__setitem__(0,'0'))
add(lambda z:z['local_certificates'][0].update(observed_count_total=z['local_certificates'][0]['observed_count_total']+1))
add(lambda z:z['local_certificates'][0].update(scaled_block_norm_upper='0'))
add(lambda z:z['local_certificates'][0]['certificate'].update(upper='0'))
add(lambda z:z['local_certificates'][0]['certificate']['probe'].__setitem__(0,z['local_certificates'][0]['certificate']['probe'][0]^1))
for z in mut:
 try:x.replay(model,records,z,**args)
 except (AssertionError,KeyError):checks+=1
 else:raise AssertionError('accepted forged local certificate')
q=Path(tempfile.mkdtemp(prefix='feedback_bad_packed_'))
for name in ['block_map.bin','policy_by_remaining_steps.bin','initial_support.bin','terminal_indicator.bin']:(q/name).write_bytes((p/name).read_bytes())
for name in ['block_map.bin','policy_by_remaining_steps.bin','initial_support.bin','terminal_indicator.bin']:
 good=(q/name).read_bytes();bad=bytes([good[0]^1])+good[1:];(q/name).write_bytes(bad)
 try:x.replay(model,records,local,packed_directory=q,**args)
 except AssertionError:checks+=1
 else:raise AssertionError('accepted corrupt '+name)
 (q/name).write_bytes(good)
print('Cached-negative receiver checks',checks,'PASS; full genuine replays run separately')
