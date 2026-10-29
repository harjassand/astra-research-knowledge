"""Predeclared replay of the TWO recorded >3.5SE cases.

N=100000 each, seed2026102943; single run, no stop-on-pass or producer edits.
Results remain diagnostic whatever their signs. Primary code was whole-read.
"""
from pathlib import Path
import importlib.util,json,sys,time
import numpy as np

sys.dont_write_bytecode=True
base=Path(__file__).resolve().parents[1]/'t_collision_operation'
def load(name,file):
    spec=importlib.util.spec_from_file_location(name,base/file)
    module=importlib.util.module_from_spec(spec);sys.modules[name]=module
    spec.loader.exec_module(module);return module

def run():
    a=load('root_dual_replay','angular_dual.py');r=load('root_ref_replay','moment_reference.py')
    rng=np.random.default_rng(2026102943);n=100000;out={}
    start=time.perf_counter();counts=a.Counts()
    values=np.array([a.linear_factory(lambda:rng.random()<.05,.9,rng,counts) for _ in range(n)])
    def summary(x,target):
        se=float(x.std(ddof=1)/np.sqrt(len(x)))
        return dict(n=len(x),mean=float(x.mean()),target=target,stderr=se,z=(float(x.mean())-target)/se)
    out['factory']=dict(summary(values,.1),counts=counts.json(),seconds=time.perf_counter()-start)
    start=time.perf_counter();model=a.declared_model();counts=a.Counts()
    values=np.array([a.moment_sample(2,np.array([1.,0,0]),30.,model.draw_e,rng,counts) for _ in range(n)])
    m2,m4=r.moments(30.,[1,0,0]);target=(m4/3-2*model.c*m2+model.c**2)/model.h**2
    out['rotating_q2_t30']=dict(summary(values,target),counts=counts.json(),seconds=time.perf_counter()-start)
    out['scope']='one predeclared independent floating replay; original anomalies retained; no exact-law proof from MC'
    out['seed']=2026102943
    return out

if __name__=='__main__':
    result=run();Path(__file__).with_name('REPLAY.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
