"""Reproducible final experiment with explicit public/hidden input separation."""
from pathlib import Path
ROOT = Path(__file__).resolve().parent
import time,json,sys,warnings,platform
import numpy as np
from scipy.sparse.linalg import spsolve
from probe import soft_east,matrix,run
from certify import certify_run,certify_field,outward
from rule_probe import learn_parent_rule,predicted_fac

class RateOracle:
    """Obtain one microscopic facilitation factor at an arbitrary selected edge.
    The simulation fixture computes it on demand from the hidden physical model.
    This is stronger than access to atomistic energies/forces; no molecular-rate
    estimation capability is asserted.
    """
    def __init__(self,public,chain):
        self.public=public
        self._parents={int(chain[0]):None}
        for i in range(1,len(chain)):self._parents[int(chain[i])]=int(chain[i-1])
        self.calls=0;self.seconds=0.;self.cache={}
    def query(self,e):
        st=time.perf_counter();self.calls+=1
        p=self._parents[int(self.public['dims'][e])]
        x=int(self.public['a'][e])
        val=1. if p is None or (x>>p)&1 else self.public['softness']
        self.cache[int(e)]=val;self.seconds+=time.perf_counter()-st
        return val


def experiment(q,eps,seed=81426,policies=('relative','optimistic','random')):
    st=time.perf_counter();fixture=soft_east(10,q,eps,seed)
    public={k:v for k,v in fixture.items() if k not in ('fac','order')}
    preparation_seconds=time.perf_counter()-st
    N=len(public['m']);E=len(public['a'])
    # Strongest generic small-state comparator: acquire all rates and solve once.
    ref_oracle=RateOracle(public,fixture['order']);st=time.perf_counter()
    allfac=np.array([ref_oracle.query(e) for e in range(E)])
    v=spsolve(matrix(public,public['base']*allfac),public['m'])
    low,up,delta,_=certify_field(public,allfac,v)
    refseconds=time.perf_counter()-st
    record={'q':q,'softness':eps,'L':10,'seed':seed,'states':N,'edges':E,
            'model_assembly_seconds':preparation_seconds,
            'reference':{'queries':ref_oracle.calls,'certified_lower':outward(low,True),'certified_upper':outward(up,False),
                         'residual_delta':outward(delta,False),'seconds_including_queries_and_validation':refseconds},'runs':[]}
    # Strong structure-aware comparator receives the extra single-parent premise.
    ro=RateOracle(public,fixture['order']);st=time.perf_counter()
    parents,inds,ans=learn_parent_rule(public,ro.query)
    inferred=predicted_fac(public,parents)
    assert np.array_equal(inferred,allfac)
    v=spsolve(matrix(public,public['base']*inferred),public['m'])
    ll,uu,dd,_=certify_field(public,inferred,v)
    record['structure_aware']={'queries':ro.calls,'seconds_including_learning_assembly_solve_validation':time.perf_counter()-st,
                              'conditional_lower':outward(ll,True),'conditional_upper':outward(uu,False),
                              'premise':'Every flip is constantly facilitated or depends monotonically on one unknown non-target spin.'}
    for policy in policies:
        oracle=RateOracle(public,fixture['order']);start=time.perf_counter()
        result=run(public,policy,refresh=32,oracle=oracle.query)
        assert result['queries']==oracle.calls==len(oracle.cache)
        cert=certify_run(public,result)
        # Certificate has no access to private facilitation factors or chain labels.
        record['runs'].append({'run':result,'certificate':cert,'oracle_calls':oracle.calls,
                              'oracle_seconds':oracle.seconds,'total_seconds':time.perf_counter()-start})
        print(q,eps,seed,policy,'calls',oracle.calls,'cert',cert['certified_lower'],cert['certified_upper'],
              'ratio',cert['certified_upper_lower_ratio'],'total',record['runs'][-1]['total_seconds'],flush=True)
    return record

if __name__=='__main__':
    data={'environment':{'python':platform.python_version(),'numpy':np.__version__,'threads':'OPENBLAS_NUM_THREADS=1'},
          'results':[],'status':'No WE/AIMMD/TAMMBER implementation was run. No atomistic benchmark was run.'}
    for q,eps in [(.05,1e-6),(.02,1e-8),(.01,1e-10),(.005,1e-12)]:
        data['results'].append(experiment(q,eps))
        json.dump(data,open(str(ROOT / 'final_results.json'),'w'),indent=2)
    for seed in [1,23,45]:
        data['results'].append(experiment(.005,1e-12,seed,policies=('relative',)))
        json.dump(data,open(str(ROOT / 'final_results.json'),'w'),indent=2)
