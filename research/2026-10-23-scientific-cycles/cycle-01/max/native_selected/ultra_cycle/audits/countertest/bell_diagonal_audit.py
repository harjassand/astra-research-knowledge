"""Independent tiny nonuniform Bell-diagonal audit; no tensor theorem inference."""
import json,math,resource,sys,time
from pathlib import Path
import numpy as np

start=time.perf_counter(); cpu=time.process_time()
bell=np.array([[1,0,0,1],[0,1,1,0],[0,1,-1,0],[1,0,0,-1]],float)/math.sqrt(2)
cases=[]
for lam in [np.array([.61,.23,.11,.05]),np.array([0,.2,.3,.5]),
            np.ones(4)/4,np.array([1.,0,0,0])]:
    X=(bell*np.sqrt(lam))@bell.T
    ps=[]
    for a in [0,1]:
        T=np.trace(X.reshape(2,2,2,2),axis1=a,axis2=a+2)
        ps.append(float(np.vdot(T,T).real)/2)
    formula=float(np.sqrt(lam).sum()**2/4)
    classical=[float(np.square(np.sqrt(lam).reshape(2,2).sum(axis=a)).sum())/2 for a in [0,1]]
    ent=-sum(float(p)*math.log(float(p)) for p in lam if p>0)
    assert max(abs(z-formula) for z in ps)<1e-13
    assert all(c+1e-13>=p for c,p in zip(classical,ps))
    cases.append(dict(spectrum=lam.tolist(),actual_scores=ps,
        formula_score=formula,coordinate_averaging_scores=classical,
        entropy=ent,delta=math.log(2)*sum(ps)-ent))
rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
out=dict(cases=cases,status='PASS',wall_seconds=time.perf_counter()-start,
    cpu_seconds=time.process_time()-cpu,peak_rss_bytes=int(rss if sys.platform=='darwin' else rss*1024))
Path(__file__).with_name('BELL_DIAGONAL_CHECK.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
