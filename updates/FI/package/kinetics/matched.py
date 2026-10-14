"""Same acquisition inputs, same 5% interval-ratio goal. Single-run timings."""
import json,time,numpy as np
from pathlib import Path
from fractions import Fraction as F
from model import fixture,add_context_clock,discover_partition,Compiler
from kinetic_tomography import acquire_unknown_support
from solve import pcg_tensor
from certify import certify
from full_reference import run_reference
ROOT=Path(__file__).parent

def main():
    results={}
    for method in ['tensor','full']:
        start=time.perf_counter()
        model,tr=acquire_unknown_support(add_context_clock(fixture(B=3,m=6,rarity=3),F(1,100)))
        groups,search=discover_partition(model);c=Compiler(model,groups);acq=time.perf_counter()-start
        if method=='tensor':
            v,log=pcg_tensor(c,rank=12,iterations=16,target_ratio=1.025)
            ans=certify(c,v);ans.update(coefficients=sum(a.size for a in v),iterations=len(log),log=log)
            np.savez_compressed(ROOT/'matched_tensor.npz',**{str(i):a for i,a in enumerate(v)})
        else:ans=run_reference(c,target_ratio=1.05)
        ans.update(end_to_end_seconds=time.perf_counter()-start,acquisition_compilation_seconds=acq,energy_queries=tr['energy_queries'],clock_queries=tr['balanced_clock_queries'],accuracy_goal_upper_lower=1.05)
        assert ans['ratio_float']<=1.05
        results[method]=ans
        json.dump(ans,open(ROOT/f'matched_{method}.json','w'),indent=2)
        json.dump(tr,open(ROOT/f'matched_{method}_transcript.json','w'),indent=2)
        print(method,{k:ans[k] for k in ['lower_float','upper_float','ratio_float','end_to_end_seconds','iterations','energy_queries','clock_queries']},flush=True)
    json.dump(results,open(ROOT/'matched_comparison.json','w'),indent=2)
if __name__=='__main__':main()
