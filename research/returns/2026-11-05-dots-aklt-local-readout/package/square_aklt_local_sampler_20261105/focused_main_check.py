from pathlib import Path
from fractions import Fraction
from collections import Counter
import json,time,hashlib
from scipy.stats import binomtest
from local_perfect_sampler import LocalPerfectLoopSampler
HERE=Path(__file__).resolve().parent
reg=json.loads((HERE/'focused_main_preregistration.json').read_text())
n=reg['samples'];target=tuple(map(tuple,reg['target_route']));p=Fraction(reg['probability_exact'])
s=LocalPerfectLoopSampler(reg['query'],box=tuple(reg['box']),seed=reg['seed'])
count=0;work=Counter();start=time.monotonic()
for k in range(n):
 routes,stats=s.sample();count+=(len(routes)==1 and routes[0]==target);work.update(stats)
 if (k+1)%250000==0:print(json.dumps({'completed':k+1,'fixed_total':n,'elapsed_seconds':time.monotonic()-start}),flush=True)
(HERE/'focused_main_raw_count.json').write_text(json.dumps({'samples':n,'seed':reg['seed'],'observed':int(count),'elapsed_seconds':time.monotonic()-start},indent=2)+'\n')
test=binomtest(count,n,float(p));ci=test.proportion_ci(confidence_level=.99,method='exact')
out={'preregistration':reg,'observed':count,'expected':n*float(p),'binomial_p_value_two_sided':float(test.pvalue),'reject_at_preregistered_alpha':bool(test.pvalue<.01),'target_probability_99pct_clopper_pearson':[float(ci.low),float(ci.high)],'elapsed_seconds':time.monotonic()-start,'mean_work':{k:v/n for k,v in work.items()},'code_sha256':hashlib.sha256((HERE/'local_perfect_sampler.py').read_bytes()).hexdigest(),'interpretation':'Fresh pre-specified main-engine diagnostic. Nonrejection does not establish exactness, and earlier deficits remain part of the record. Mathematical correctness requires the audited invariant and implementation.'}
(HERE/'focused_main_check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
