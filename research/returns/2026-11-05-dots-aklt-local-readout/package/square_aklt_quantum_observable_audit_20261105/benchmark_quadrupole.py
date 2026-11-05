from pathlib import Path
import sys,time,json,statistics
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'square_aklt_boundary_operation_20261105'))
from perfect_loop_sampler import PerfectLoopSampler
from torus_loop_birth_sampler import TorusLoopBirthSampler
from quadrupole_estimator import averaged_horizontal_estimators
side=int(sys.argv[1]) if len(sys.argv)>1 else 32
n=int(sys.argv[2]) if len(sys.argv)>2 else 100
s=PerfectLoopSampler(side,side,seed=194835,birth_factory=TorusLoopBirthSampler)
seps=[r for r in [1,2,4,8] if r<side];values={r:[] for r in seps};st=time.monotonic();obsseconds=0
for k in range(n):
 routes,stats=s.sample();t=time.monotonic();z=averaged_horizontal_estimators(routes,side,seps);obsseconds+=time.monotonic()-t
 for r in seps:values[r].append(z[r])
elapsed=time.monotonic()-st
result={'side':side,'iid_samples':n,'total_seconds':elapsed,'seconds_per_sample':elapsed/n,'observable_seconds_total':obsseconds,'values':{r:{'mean':statistics.mean(v),'sample_variance':statistics.variance(v),'estimated_standard_error':statistics.stdev(v)/n**.5} for r,v in values.items()},'scope':'Sample means and estimated standard errors, not rigorous confidence intervals. Open-box virtual-identity boundary state; averages over all valid horizontal pairs.'}
Path(__file__).with_name(f'quadrupole_benchmark_{side}.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
