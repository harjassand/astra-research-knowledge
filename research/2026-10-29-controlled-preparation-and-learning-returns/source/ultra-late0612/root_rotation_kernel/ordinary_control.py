"""Same-input ordinary Wild full-law alternative; one fixed acquisition."""
from pathlib import Path
import json,time
import numpy as np
from consumer import c,Kernel

def wild(t,model,kernel,chol,rng):
    stack=[('node',t)];values=[];leaves=0
    while stack:
        kind,left=stack.pop()
        if kind=='combine':
            a,b=values.pop(),values.pop();r=kernel.draw(rng)
            values.append((a+b+r@(a-b))/2)
        else:
            wait=rng.exponential()
            if wait>=left:
                j=int(rng.choice(len(chol),p=model.probabilities));values.append(chol[j]@rng.normal(size=3));leaves+=1
            else:stack.extend([('combine',0),('node',left-wait),('node',left-wait)])
    assert len(values)==1
    return values[0],leaves

def main():
    start=time.perf_counter();model=c.model(b=1.1);kernel=Kernel();chol=np.linalg.cholesky(model.matrices)
    preparation=time.perf_counter()-start;rng=np.random.default_rng(2026102963);out=[]
    for t in (0.,3.):
        tick=time.perf_counter();draws=[wild(t,model,kernel,chol,rng) for _ in range(500)]
        seconds=time.perf_counter()-tick;vs=np.array([x[0] for x in draws]);cov=kernel.covariance(t,model.mean)
        out.append(dict(t=t,n=500,seconds=seconds,leaves=sum(x[1] for x in draws),
                        expected_leaves=500*np.exp(t),covariance_diagonal=np.diag(cov).tolist(),
                        empirical_second_moments=(vs*vs).mean(axis=0).tolist()))
    result=dict(scope='same supplied matrices/kernel/500-output ideal-law task; floating diagnostics; not all-solver advantage',
                seed=2026102963,preprocessing_seconds=preparation,rows=out,
                excluded='equilibrium approximations and moment-only tasks have separate accuracy/output contracts')
    Path(__file__).with_name('ORDINARY_CONTROL.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
