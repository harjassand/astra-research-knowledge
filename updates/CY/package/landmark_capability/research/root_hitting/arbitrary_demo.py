"""Run the arbitrary-product-start numerical construction on one exact comparator."""
import json
import time
from pathlib import Path
from multitarget import arbitrary_survival,exact_small

start=time.time();cases=[]
p=['.4','.6','.7'];rates=['.3','1.1','2.7'];targets=[0,7];r=['1','0','1']
for degree in (12,24):
    t='2'
    row=arbitrary_survival(p,rates,r,targets,t,degree=degree,digits=100,step='.06')
    exact=exact_small(p,rates,targets,t,r)
    row.update({'time':t,'initial_probabilities':r,'comparator':exact,
                'absolute_error':abs(row['survival']-exact['survival'])})
    cases.append(row)
result={'status':'floating_diagnostic_only','elapsed_seconds':time.time()-start,'cases':cases}
Path(__file__).with_name('arbitrary_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
