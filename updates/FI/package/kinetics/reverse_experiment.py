import time,json,numpy as np
from pathlib import Path
from fractions import Fraction as F
from model import fixture,add_context_clock,Compiler,discover_partition
from reverse_tomography import acquire_reverse
from solve import pcg_tensor
from certify import certify
from full_reference import run_reference
ROOT=Path(__file__).parent

def run(name,context=True,method='tensor',target=None):
    start=time.perf_counter();truth=fixture(B=3,m=6,rarity=3)
    if context:truth=add_context_clock(truth,F(1,100))
    model,tr=acquire_reverse(truth);groups,search=discover_partition(model);c=Compiler(model,groups);acq=time.perf_counter()-start
    if method=='tensor':
        v,log=pcg_tensor(c,rank=12 if context else 8,iterations=12 if context else 8,target_ratio=target)
        ans=certify(c,v);ans.update(log=log,coefficients=sum(a.size for a in v),iterations=len(log))
        np.savez_compressed(ROOT/(name+'.npz'),**{str(i):a for i,a in enumerate(v)})
    else:ans=run_reference(c,target_ratio=1.05)
    ans.update(end_to_end_seconds=time.perf_counter()-start,acquisition_compilation_seconds=acq,energy_queries=tr['energy_queries'],reverse_clock_queries=tr['reverse_clock_queries'],method=method,physical_experiment=False,scope='original-law reverse-relaxation computational queries; no intervention-invariance under bias assumed',partition=search)
    json.dump(ans,open(ROOT/(name+'.json'),'w'),indent=2);json.dump(tr,open(ROOT/(name+'_transcript.json'),'w'),indent=2)
    print(name,{k:ans[k] for k in ['lower_float','upper_float','ratio_float','end_to_end_seconds','iterations','reverse_clock_queries']},flush=True)
    return ans
if __name__=='__main__':
    run('reverse_A',context=False)
    run('reverse_B')
    run('reverse_matched_tensor',target=1.025)
    run('reverse_matched_full',method='full')
