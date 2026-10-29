from exact_threshold import *
from pathlib import Path
import random,json
rng=random.Random(291029)
for _ in range(500):
 x=F(rng.randrange(10**15),rng.randrange(1,10**8));u=upper_root(x);assert u*u>=x and (u==0 or (u-F(1,2**32))**2<x)
base=dict(T=10**18,J=10**18//3,t=10**18//768,services=10**18//3,p='1/3',m=3,score_upper=0,k_loss=20,k_fault=20,verified_code=True,resource_abort=False)
a=evaluate(**base);assert a['accept']
for change in [dict(verified_code=False),dict(resource_abort=True),dict(services=base['services']-1)]:
 assert not evaluate(**(base|change))['accept']
b=evaluate(**(base|dict(score_upper=1)));assert F(b['bad_count_upper'])>=F(a['bad_count_upper'])
for change in [dict(p=0),dict(p=1),dict(m=2),dict(T=0),dict(services=base['J']+1),dict(t=-1)]:
 try:evaluate(**(base|change))
 except ValueError:pass
 else:raise AssertionError(change)
result=dict(root_checks=500,invalid_parameter_tests=6,synthetic_large_horizon=a,scope='Synthetic decision arithmetic only, no acquired trajectory or physical acceptance.')
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
