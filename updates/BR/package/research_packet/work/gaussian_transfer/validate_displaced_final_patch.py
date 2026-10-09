from fractions import Fraction as F
from pathlib import Path
import hashlib,json,random,time
import displaced_evaluator as ev
from displaced_sampler import DisplacedHeraldGaussian
ROOT=Path(__file__).resolve().parent
original=ev._log_H_once
calls=0
def injected(*args,**kwargs):
 global calls
 calls+=1
 if calls==1:raise ev._NeedPrecision('injected narrow retry test')
 return original(*args,**kwargs)
ev._log_H_once=injected
value,meta=ev.log_H(1000001,F(1,3),F(1,10**40),30)
ev._log_H_once=original
assert calls==2 and meta['precision_attempts']==2
base=[[F(1,8),F(1,7)],[F(1,7),F(1,9)]]
g=[F(1,5),F(1,6)]
model=DisplacedHeraldGaussian.from_pure(base,g,0,10**6)
start=time.perf_counter();out=model.sample(random.Random(4),F(1,10**6));elapsed=time.perf_counter()-start
assert not model.last_ticket_fallback
record={'source_sha256':{f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in ['displaced_evaluator.py','displaced_sampler.py']},'injected_retry_attempts':calls,'injected_retry_log_radius':meta['absolute_log_radius'],'h':1000000,'epsilon':'1e-6','seed':4,'sample':list(map(str,out)),'seconds':elapsed,'ticket_fallback':model.last_ticket_fallback,'ticket_count':model.last_ticket_count,'random_bits':model.last_random_bits,'scope':'Narrow retry-path and final endpoint regression; full unchanged-math distribution matrix retained with previous coefficient hash.'}
(ROOT/'displaced_final_patch_results.json').write_text(json.dumps(record,indent=2))
print(record)
