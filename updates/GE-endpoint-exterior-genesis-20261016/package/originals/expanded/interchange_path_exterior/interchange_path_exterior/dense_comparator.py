"""One bounded comparison, importing the delivered dense implementation unchanged."""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
import sys,time,resource,json,math
from pathlib import Path
sys.path.insert(0,os.environ.get('PAIR_CERTIFICATE_BASE',str(Path(__file__).resolve().parent/'original_dependencies')))
from rigorous_pair_certificate import certify
n=20;rates=[10**i for i in range(n-1)];boost=[1,10]+[10**n]*(n-3)
begin=time.perf_counter();r=certify(n,[(i,i+1) for i in range(n-1)],rates,boost,2)
r['wall_seconds']=time.perf_counter()-begin;r['peak_RSS_KiB']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
r['stored_power_entries']=sum((p['clock_power_m']+1)*r['pair_states']**2 for p in r['precision'])
Path(__file__).with_name('dense_receipt.json').write_text(json.dumps(r,indent=2))
print('DONE',r['wall_seconds'],r['peak_RSS_KiB'],flush=True)
