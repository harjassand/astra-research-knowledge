"""High-precision lower-tail diagnostic against a separate dense CTMC expm."""
import json
import time
from pathlib import Path
import mpmath as mp
from multitarget import arbitrary_survival

start=time.time();p=['.4','.6','.7'];rates=['.3','1.1','2.7'];r=['0']*3;t='.00001'
row=arbitrary_survival(p,rates,r,[7],t,degree=64,digits=170,step='.035',scaled_pole=True)
with mp.workdps(100):
    generator=mp.matrix(7,7)
    for x in range(7):
        for i,(p0,rate0) in enumerate(zip(p,rates)):
            rate=mp.mpf(rate0)*(1-mp.mpf(p0) if x>>i&1 else mp.mpf(p0))
            generator[x,x]-=rate;y=x^(1<<i)
            if y<7:generator[x,y]+=rate
    transition=mp.expm(generator*mp.mpf(t));exact=1-sum(transition[0,j] for j in range(7))
    got=mp.mpf(row['cdf_decimal']);error=abs(got-exact)
    row.update({'reference_cdf':mp.nstr(exact,80),'absolute_error':mp.nstr(error,30),
                'relative_error':mp.nstr(error/exact,30),'time':t,
                'reference':'100 decimal digit dense exponential of the 7-state killed generator',
                'status':'floating diagnostic, not interval certification'})
row['elapsed_seconds']=time.time()-start
Path(__file__).with_name('rare_lower_tail_results.json').write_text(json.dumps(row,indent=2)+'\n')
print(json.dumps(row,indent=2))
