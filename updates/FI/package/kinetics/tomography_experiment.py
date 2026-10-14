import time,json
from pathlib import Path
from fractions import Fraction as F
import numpy as np
from model import fixture,add_context_clock,discover_partition,Compiler
from kinetic_tomography import acquire_unknown_support
from solve import pcg_tensor
from certify import certify
ROOT=Path(__file__).parent

def run(name,cross_kinetic=False):
    start=time.perf_counter();truth=add_context_clock(fixture(B=3,m=6,rarity=3),F(1,100))
    # An additional authored falsification variant: kinetic dependence outside
    # the energy neighbourhood, invisible to all-zero-context clock readings.
    if cross_kinetic:
        energy_nei=set(truth['clock_contexts'][0])
        a=min(energy_nei);j=next(j for j in range(1,truth['n']) if j not in energy_nei)
        truth['clock_contexts'][0]=sorted([a,j]);truth['clock_tables'][0]=[truth['nu'][0],truth['nu'][0]/2,truth['nu'][0]/2,truth['nu'][0]]
    model,tr=acquire_unknown_support(truth);groups,search=discover_partition(model);c=Compiler(model,groups)
    acquisition=time.perf_counter()-start
    v,log=pcg_tensor(c,rank=12,iterations=12)
    ans=certify(c,v);ans.update(total_seconds=time.perf_counter()-start,acquisition_compilation_seconds=acquisition,energy_queries=tr['energy_queries'],clock_queries=tr['balanced_clock_queries'],R_mass=str(c.R_mass),R_clock=str(c.R_clock),R=str(c.R),partition=search,metadata=truth['metadata'],unknown_clock_support=True,rank=12,coefficients=sum(x.size for x in v),raw_operator_terms=len(c.rawterms),kinetic_dependencies_beyond_energy=[(i,j) for i,ss in model['clock_contexts'].items() for j in ss if tuple(sorted((i,j))) not in model['edges']],clock_context_table_entries=sum(map(len,model['clock_tables'].values())),log=log)
    json.dump(ans,open(ROOT/(name+'.json'),'w'),indent=2);json.dump(tr,open(ROOT/(name+'_transcript.json'),'w'),indent=2);np.savez_compressed(ROOT/(name+'.npz'),**{str(i):a for i,a in enumerate(v)})
    print(name,{k:ans[k] for k in ['lower_float','upper_float','ratio_float','total_seconds','energy_queries','clock_queries','R','coefficients','raw_operator_terms','kinetic_dependencies_beyond_energy']},flush=True)
    return ans
if __name__=='__main__':
    run('unknown_support_rare')
    run('unknown_support_cross',True)
