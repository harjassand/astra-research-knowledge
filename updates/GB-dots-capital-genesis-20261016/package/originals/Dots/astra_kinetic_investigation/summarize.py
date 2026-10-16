from pathlib import Path
import json,sys,os,platform,hashlib
import numpy as np, scipy, sympy, numba
from scipy.stats import t,beta
root=Path(__file__).resolve().parent
rs=[json.loads((root/f'split_rep_{j:02}.json').read_text()) for j in range(12)]
p=np.array([r['estimate'] for r in rs]);mean=float(p.mean());sd=float(p.std(ddof=1));se=sd/len(p)**.5
summary={'replicates':12,'particles_per_stage':256,'levels':rs[0]['levels'],'estimate_mean':mean,'replicate_sd':sd,'empirical_se':se,'relative_empirical_se':se/mean,
 'descriptive_t95_interval':[mean-t.ppf(.975,11)*se,mean+t.ppf(.975,11)*se],
 'range':[float(p.min()),float(p.max())],
 'total_events':sum(r['total_events'] for r in rs),'total_wall_seconds':sum(r['wall_seconds'] for r in rs),
 'per_rep_wall_range':[min(r['wall_seconds'] for r in rs),max(r['wall_seconds'] for r in rs)],
 'max_observed_count':max(s['max_count'] for r in rs for s in r['stages']),
 'caveat':'12 independent splitting estimates; empirical SE and t interval are descriptive, not rigorous coverage or a rare-event certificate. Pilot excluded. Floating SSA not certified.',
 'estimates':p.tolist()}
(root/'experiment_summary.json').write_text(json.dumps(summary,indent=2))
val=json.loads((root/'sampler_validation.json').read_text());h=val['ssa']['hits'];n=val['ssa']['particles']
val['ssa']['binomial_95_interval']=[float(beta.ppf(.025,h,n-h+1)),float(beta.ppf(.975,h+1,n-h))]
(root/'sampler_validation.json').write_text(json.dumps(val,indent=2))
env={'python':sys.version,'numpy':np.__version__,'scipy':scipy.__version__,'sympy':sympy.__version__,'numba':numba.__version__,
 'platform':platform.platform(),'os_cpu_count':os.cpu_count(),'affinity_cpus':len(os.sched_getaffinity(0)),
 'cpu_model':next((line.split(':',1)[1].strip() for line in Path('/proc/cpuinfo').read_text().splitlines() if line.startswith('model name')),None),
 'threading':'single Numba worker; OPENBLAS_NUM_THREADS=1 for recorded experiments',
 'peak_RSS':'not recorded for each benchmark process; no peak-memory superiority claim',
 'timing_scope':'tool invocation/framework startup, all failed attempts, source acquisition and reasoning are not in the per-replicate wall sums',
 'known_failed_attempts':['Direct git clone unavailable due DNS; sources read through GitHub connector.','fsp_reference.py 100 1 timed out at 40 seconds; replaced by two-site T=0.2 diagnostic.','algebra_explore.py first invocation used wrong working directory; immediate exit, then rerun successfully.']}
(root/'environment.json').write_text(json.dumps(env,indent=2))
print(json.dumps(summary,indent=2)); print(val['ssa'])
