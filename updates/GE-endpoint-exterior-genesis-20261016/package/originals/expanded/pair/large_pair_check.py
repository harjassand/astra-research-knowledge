from rigorous_pair_certificate import certify
import resource,time,json
from pathlib import Path
n=12;edges=[(i,i+1) for i in range(n-1)];rates=[10**i for i in range(n-1)];boost=[1,10]+[10**12]*(n-3)
t=time.perf_counter();r=certify(n,edges,rates,boost,2)
r['wall_seconds']=time.perf_counter()-t;r['process_peak_RSS_KiB']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss;r['full_permutation_states']=479001600;r['original_intensity']=sum(rates);r['averaged_boundary_intensity']=11
Path(__file__).with_name('large_pair_results.json').write_text(json.dumps(r,indent=2))
print('LARGE',r['certified'],r['total_upper_float'],r['wall_seconds'],r['process_peak_RSS_KiB'],flush=True)
