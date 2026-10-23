"""Targeted receipt controls. No H5AD read, bootstrap draws, or producer full analysis."""
import argparse,hashlib,json,sys,types,time,resource,platform
from pathlib import Path
import numpy as np
p=argparse.ArgumentParser();p.add_argument('--producer',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
t=time.perf_counter();cpu=time.process_time();root=a.producer.resolve();sys.path.insert(0,str(root/'src'))
from run_guide_experiment import fit_direction,Data
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
f=json.loads((root/'FREEZE.json').read_text());r=json.loads((root/'results/RESULT.json').read_text());body=json.loads((root/'results/RESOURCE_RECEIPT.json').read_text());outer=json.loads((root/'results/OUTER_RESOURCE_RECEIPT.json').read_text());design=json.loads((root/'results/DESIGN_MAP.json').read_text())
assert sha(root/'src/run_guide_experiment.py')==f['analysis_source_sha256']==body['source_sha256']
assert sha(root/'FROZEN_CONTRACT.txt')==f['contract_sha256']==body['freeze_contract_sha256']
assert sha(root/'results/DESIGN_MAP.json')==f['design_map_sha256']
assert f['analysis_code_locked_utc']<outer['start_utc']<outer['end_utc']
assert r['resource_body']==body and r['resource_entire_command']==outer
with np.load(root/'results/BOOTSTRAP_DRAWS.npz') as z:
 shapes={k:list(z[k].shape) for k in z.files}
 assert shapes['gains']==[7,2,2,105] and shapes['null_gain']==[7,2,2]
 assert all(s[0]==7 for s in shapes.values())
 assert np.all(z['control_weights'].sum(1)==7)
assert r['bootstrap_completed']==body['completed']==7 and body['requested']==399
assert outer['returncode']==1 and body['peak_rss_bytes']>3*2**30
assert r['leave_one_control_out_status'].startswith('NOT_PERFORMED')
assert r['inference_status'].startswith('NOT_COMPUTED')
# Test actual code dependency with finite synthetic values and actual arm mapping.
arrays=sorted(design['delivered_counts']);ai={s:i for i,s in enumerate(arrays)};fam=[q for q in design['families'] if q['eligible']];targets=sorted({s for q in fam for s in (q['a'],q['b'])})
d=types.SimpleNamespace(N=len(fam),ng=17,idx=np.array([[ai[s] for s in q['arms']] for q in fam]),c=ai[design['matching_control']],inc=np.zeros((len(fam),len(targets))))
for i,q in enumerate(fam):
 for s in (q['a'],q['b']):d.inc[i,targets.index(s)]=1
d.noise={k:np.full(len(arrays),.003) for k in ('log','rate')};d.hats=[Data.ridge_hats(d,np.array([design['delivered_counts'][arrays[j]] for j in d.idx[:,direction]])) for direction in (0,1)]
rng=np.random.default_rng(50021);m=rng.uniform(.05,2,(len(arrays),d.ng));controls=[]
for kind in ('log','rate'):
 for direction in (0,1):
  target=d.idx[:,1-direction];source=d.idx[:,direction];x=fit_direction(d,m,kind,direction,True);mut=m.copy();mut[target]=rng.uniform(100,1000,(d.N,d.ng));y=fit_direction(d,mut,kind,direction,True)
  for key in ('beta','cv','rank','single_gram_eigenvalues'):assert np.array_equal(x[key],y[key]),key
  assert x['lambda_index']==y['lambda_index']
  assert np.array_equal(x['null_means'][source],y['null_means'][source])
  assert np.array_equal(x['null_means'][target],y['null_means'][target])
  assert not np.array_equal(x['gain'],y['gain'])
  controls.append({'scale':kind,'direction':direction,'heldout_mutation':'calibration and predictions invariant; scores changed'})
# Independent exact small shared-control identity and counterexample to naive cross-product.
from fractions import Fraction as F
c=[F(1),F(2),F(4),F(8),F(16),F(32),F(64)];n=len(c);mean=sum(c)/n;variance=sum((x-mean)**2 for x in c)/(n-1)
u=sum(c[i]*c[j] for i in range(n) for j in range(n) if i!=j)/(n*(n-1));assert mean*mean-variance/n==u
# Algebraic observational equivalence for array vs family shifts, exact binary construction.
A=np.eye(len(arrays),dtype=int);T=np.zeros((len(arrays),len(fam)),dtype=int)
for j,q in enumerate(fam):
 for arr in q['arms'][:2]:T[ai[arr],j]=1
J=T.copy();assert np.array_equal(A@T,J)
# Do not execute full runner: direct unit analysis of its frozen resource comparison.
threshold=3*2**30;linux_rss_kib=4*2**20
assert linux_rss_kib < threshold and linux_rss_kib*1024 > threshold
out={'status':'PASS_WITH_PORTABILITY_LIMIT','producer_source_sha256':sha(root/'src/run_guide_experiment.py'),'freeze_binding':'matching source/design/contract; recorded chronology internally consistent, not independently timestamp-attested','partial_draw_shapes':shapes,'partial_inference_status_consistent':True,'target_response_controls':controls,'exact_shared_control_identity':{'left':str(mean*mean-variance/n),'right':str(u),'control_bias_term':str(variance/n)},'implementation_ambiguity':'exact J=A*T construction; conditional unrestricted array effects, not causation claim','rss_portability':{'producer_platform':'macOS per actual command/Python receipt','reported_peak_bytes':body['peak_rss_bytes'],'linux_counterexample_4GiB_raw_KiB_would_not_trigger':True,'full_runner_executed':False},'execution_scope':'synthetic actual-source targeted controls plus saved-array/receipt reads; no RNA values, no new draws, no LOCO','wall_seconds':time.perf_counter()-t,'cpu_seconds':time.process_time()-cpu,'receiver_platform':platform.system(),'receiver_peak_rss_native':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'receiver_peak_rss_units':'KiB' if sys.platform.startswith('linux') else 'bytes'}
a.output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
