"""Portable no-RNA verification of packaged bytes and reported point arithmetic.
Does not reproduce RNA preprocessing/model fitting or completed inference.
"""
from pathlib import Path
import hashlib,json,math,sys,time,csv,subprocess
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def close(a,b,tol=2e-12):
 if not math.isclose(a,b,rel_tol=tol,abs_tol=tol):raise AssertionError((a,b))
def main():
 t=time.perf_counter();checked=0
 manifest=ROOT/'MANIFEST.json'
 if manifest.exists():
  m=json.loads(manifest.read_text())
  for q,r in m['files'].items():
   p=ROOT/q
   assert p.is_file() and p.stat().st_size==r['bytes'] and sha(p)==r['sha256'],q;checked+=1
 f=json.loads((ROOT/'FREEZE.json').read_text())
 assert sha(ROOT/'FROZEN_CONTRACT.txt')==f['contract_sha256']
 assert sha(ROOT/'src/run_guide_experiment.py')==f['analysis_source_sha256']
 assert sha(ROOT/'results/DESIGN_MAP.json')==f['design_map_sha256']
 p=json.loads((ROOT/'results/POINT_RESULT.json').read_text());r=json.loads((ROOT/'results/RESULT.json').read_text());d=json.loads((ROOT/'results/DESIGN_MAP.json').read_text());resource=json.loads((ROOT/'results/RESOURCE_RECEIPT.json').read_text())
 assert len(d['eligible_pairs'])==105 and len(d['excluded_pairs'])==53 and d['matching_control_n']==7
 assert r['bootstrap_completed']==resource['completed']==7 and resource['requested']==399
 assert resource['peak_rss_bytes']>3*2**30
 assert r['leave_one_control_out_status'].startswith('NOT_PERFORMED') and r['inference_status'].startswith('NOT_COMPUTED')
 assert r['status']=='STOP_RESOURCE_CAP_NO_ROBUST_GUIDE_SIGNAL_ESTABLISHED'
 assert 'simulated_p' not in json.dumps(r) and 'basic_interval' not in json.dumps(r)
 for s in r['point_summary']:
  z=int(s['direction'][0])-1;v=p['point'][s['representation']][z]
  assert len(v['gain'])==105
  for i in range(105):close(v['ordinary_mse'][i]-v['transfer_mse'][i],v['gain'][i])
  for k in ('gain','ordinary_mse','transfer_mse','additive_mse'):close(math.fsum(v[k])/105,s[k])
  assert s['positive_family_gains']==sum(x>0 for x in v['gain'])
  assert s['source_selected_lambda']==[.01,.1,1,10,100][v['lambda_index']]
  close(s['ordinary_error_reduction_vs_raw_additive'],1-s['ordinary_mse']/s['additive_mse'])
 assert all(s['gain']<0 for s in r['point_summary'] if s['representation']=='log')
 assert all(s['gain']>0 for s in r['point_summary'] if s['representation']=='rate')
 assert len(list(csv.DictReader((ROOT/'results/ALL_FAMILY_SCORES.csv').open())))==420
 print(json.dumps({'status':'PASS','manifest_files_verified':checked,'checks':'freeze/source/design hashes;stored MSE/gain arithmetic;all420family rows;partial execution status;no asserted inference','RNA_or_model_replay':False,'wall_s':time.perf_counter()-t}))
if __name__=='__main__':main()
