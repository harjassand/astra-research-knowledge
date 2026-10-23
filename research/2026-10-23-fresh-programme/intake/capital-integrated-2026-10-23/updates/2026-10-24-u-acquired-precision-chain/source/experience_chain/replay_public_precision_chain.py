"""Replay the learner from paid observation archives only.

No imports from the simulator, no private truth file, and no RNG seed manifest.
The rank/noise/model constants and alpha schedules are declared class priors.
"""
from pathlib import Path
import hashlib
import json
import math
import numpy as np


HERE=Path(__file__).resolve().parent
DATA=HERE/'luna_batched_mean'
R, K0, MAX_CHECKS = 3, 32, 12
ALPHA_SOURCE=ALPHA_TARGET=.02


def fit(y, j, delta, sigma, m_source):
    K, n=y.shape; d=n-1
    z=2*y[:,1:]/delta
    tau=2*sigma/(delta*math.sqrt(m_source))
    alpha=6*ALPHA_SOURCE/(math.pi**2*(j+1)**2)
    t=math.sqrt(2*math.log(3/alpha))
    aG=2*tau*(math.sqrt(R)+math.sqrt(d)+t)/math.sqrt(K)
    aW=(math.sqrt(d)+t)/math.sqrt(K)
    bW=tau*tau*(2*aW+aW*aW)
    C=z.T@z/K-tau*tau*np.eye(d)
    lam,U=np.linalg.eigh(C)
    h=max(0.,float(lam[-1])); lr=float(lam[-R])
    eobs=min(aG+bW,bW+aG*aG/2+aG*math.sqrt(h+bW+aG*aG/4))
    s=eobs/lr if lr>eobs else math.inf
    return U[:,-R:],s,{'K':K,'s':s,'radius':eobs,'lambda_r':lr,'alpha':alpha}


def main():
    # These are the only two data-file reads performed by the learner replay.
    with np.load(DATA/'public_source_observations.npz') as z:
        ys=z['y'].copy(); ms=z['m'].copy()
        delta=float(z['delta']); sigma=float(z['sigma']); b=z['b'].copy()
    with np.load(DATA/'public_target_observations.npz') as z:
        yt=z['y'].copy(); mt=z['m'].copy(); eps=z['epsilon'].copy(); idx=z['target_index'].copy()
        assert delta==float(z['delta']) and sigma==float(z['sigma'])
        assert np.array_equal(b,z['b'])
    n=len(b); beta=delta/(1+delta)
    assert np.array_equal(b,np.eye(n)[0])
    assert np.all(ms==ms[0]) and np.array_equal(idx,np.arange(1,len(yt)+1))
    j=-1; K=0; s=math.inf; U=None
    checks=[]; selections=[]; outputs=[]; bounds=[]
    previous_epsilon=None
    for t,(y,m,epsilon) in enumerate(zip(yt,mt,eps),1):
        while s>epsilon/beta:
            j+=1
            if j>=MAX_CHECKS:
                raise RuntimeError('declared source check budget exhausted')
            K=K0*2**j
            if K>len(ys):
                raise RuntimeError('paid archive has insufficient source observations')
            U,s,row=fit(ys[:K],j,delta,sigma,int(ms[0]))
            checks.append(row)
        if epsilon!=previous_epsilon:
            selections.append({'first_target':t,'epsilon':float(epsilon),'source_K':K,'s':s})
            previous_epsilon=epsilon
        alpha=6*ALPHA_TARGET/(math.pi**2*t*t)
        logalpha=math.log(1/alpha)
        Q=R+2*math.sqrt(R*logalpha)+2*logalpha
        budget=epsilon*epsilon-beta*beta*s*s/4
        if budget<=0:
            raise RuntimeError('source certificate gives nonpositive target budget')
        required=max(1,math.ceil(sigma*sigma*Q/((1+delta)**2*budget)))
        def sq_bound(exposure):
            return beta*beta*s*s/4+sigma*sigma*Q/((1+delta)**2*exposure)
        while sq_bound(required)>epsilon*epsilon:
            required+=1
        while required>1 and sq_bound(required-1)<=epsilon*epsilon:
            required-=1
        assert required==int(m)
        vhat=U@(U.T@(2*y[1:]/delta))
        x=np.r_[1-beta/2,-beta*vhat/2]
        outputs.append(x); bounds.append(math.sqrt(sq_bound(m)))
    x=np.asarray(outputs)
    source_possible=sum(6*ALPHA_SOURCE/(math.pi**2*(j+1)**2) for j in range(MAX_CHECKS))
    target_possible=sum(6*ALPHA_TARGET/(math.pi**2*t*t) for t in range(1,len(yt)+1))
    result={
        'status':'PASS','learner_data_files_read':[
            'luna_batched_mean/public_source_observations.npz',
            'luna_batched_mean/public_target_observations.npz'],
        'private_seed_or_truth_reads':0,'targets':len(yt),'source_queries':K,
        'source_exposure':int(np.sum(ms[:K])),'target_exposure':int(np.sum(mt)),
        'total_exposure':int(np.sum(ms[:K])+np.sum(mt)),
        'checks':checks,'selected_source_levels':selections,
        'all_recorded_target_exposures_equal_replay':True,
        'all_computed_bounds_within_requested_tolerance':bool(np.all(np.array(bounds)<=eps)),
        'max_float_bound_minus_tolerance':float(np.max(np.array(bounds)-eps)),
        'potential_schedule_failure_bound':source_possible+target_possible,
        'simpler_all_prefix_failure_bound':ALPHA_SOURCE+ALPHA_TARGET,
        'output_sha256':hashlib.sha256(np.ascontiguousarray(x).view(np.uint8)).hexdigest(),
        'scope':'Observation-only float64 replay; not an interval-certified rounding proof or model validation.'}
    (HERE/'public_precision_replay.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
