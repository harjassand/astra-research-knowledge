"""Independent full replay and targeted receiving regressions, no author writes."""
from pathlib import Path
import copy,gzip,json,hashlib,sys,time
sys.path.insert(0,str(Path(__file__).resolve().parent))
import check_retained_large_acquisition as c
R=c.R

def run():
 root=Path(__file__).resolve().parent
 o=json.loads((root/'retained_large_4096_result.json').read_text())
 raw=(root/'retained_large_4096_observations.json.gz').read_bytes()
 assert hashlib.sha256(raw).hexdigest()==o['transcript_gzip_sha256']
 records=json.loads(gzip.decompress(raw))['records']
 kw=dict(expected_b=o['task_b'],expected_ell_num=o['task_ell_numer'],expected_ell_den=o['task_ell_denominator'],expected_length=24,expected_tolerance=R(1,50),expected_confidence=R(1,1000),expected_generators=2)
 # Exact norm calculations are memoized only AFTER the same actual calculation;
 # mutation tests never alter their inputs. This avoids redoing the 79m products.
 original=c.upper_norm;cache={}
 def memo(*args,**kwargs):
  key=repr((args,kwargs))
  if key not in cache:cache[key]=original(*args,**kwargs)
  return copy.deepcopy(cache[key])
 c.upper_norm=memo
 t=time.perf_counter();positive=c.replay(o,records,**kw);negative=0
 def reject(out=o,rec=records,**changes):
  nonlocal negative
  k=kw.copy();k.update(changes)
  try:c.replay(out,rec,**k)
  except (AssertionError,ValueError,KeyError,TypeError,IndexError):negative+=1
  else:raise AssertionError('mutated receiving admitted')
 for key,value in [('expected_confidence',R(1,100)),('expected_confidence',.001),('expected_confidence',True),('expected_generators',1),('expected_generators',True),('expected_length',23),('expected_tolerance',R(1,25))]:reject(**{key:value})
 for key,value in [('delta','1/100'),('m',1),('norm_certificates',o['norm_certificates'][:-1]),('norm_certificates',o['norm_certificates']+[o['norm_certificates'][0]])]:
  bad=o.copy();bad[key]=value;reject(out=bad)
 # All actual rows have Ni-1 counts, so the old helper's equal-total test alone
 # would pass. Current receiver must bind the actual total to scheduled Ni.
 bad=records[:];idx=next(i for i,x in enumerate(bad) if x['kind']=='incoming_pair');entry=copy.deepcopy(bad[idx])
 for half in entry['counts']:
  for row in half:
   j=next(j for j,x in enumerate(row) if x);row[j]-=1
 bad[idx]=entry;reject(rec=bad)
 # Ordinary corruption after receiving is also rejected.
 bad=copy.deepcopy(o);bad['compiled']['initial_grid_state'][0]+=1;reject(out=bad)
 bad=o.copy();bad['logical_forward_calls']-=1;reject(out=bad)
 bad=records[:];idx=next(i for i,x in enumerate(bad) if x['kind']=='outgoing');entry=copy.deepcopy(bad[idx]);j=next(j for j,x in enumerate(entry['counts']) if x);entry['counts'][j]-=1;bad[idx]=entry;reject(rec=bad)
 extra=c.extra_checks(o)
 c.upper_norm=original
 return {'status':'PASS','full_exact_replay_checks':positive,'targeted_rejection_checks':negative,'posthoc_checks':extra,'elapsed_seconds':time.perf_counter()-t,'norm_recomputation_scope':'Full positive replay computes exact norm checks; subsequent mutations share unchanged memoized norm inputs. No mutated norm input is silently trusted.','scope':'Conditional typed scientific-record replay; does not authenticate iid/randomness/protocol provenance. Not a hardened arbitrary-JSON service.'}
if __name__=='__main__':
 out=run();Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
