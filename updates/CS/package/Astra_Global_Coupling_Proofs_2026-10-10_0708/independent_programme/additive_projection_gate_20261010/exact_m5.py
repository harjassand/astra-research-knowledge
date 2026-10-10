"""Exhaustive m=5,w<=4 search after rigorous GL(5,2) and hyperplane reductions.
Hyperplanes reduce to the separately replayed m=4,w<=3 case.
For each maximum kernel dimension d, GL(5,2) sends a largest kernel
onto span(e1,...,ed); fix this kernel, then enumerate all other choices.
"""
from itertools import combinations
from pathlib import Path
import json,time
from verify_gate import all_subspaces

def full_check(m,w):
    ss=all_subspaces(m);ps=[s for s in ss if len(s)==4];full=(1<<len(ps))-1
    masks=[sum(1<<i for i,p in enumerate(ps)if len(p&s)==2)for s in ss]
    points=[sum(1<<x for x in s)for s in ss];ambient=(1<<(1<<m))-1;checks=0
    for inds in combinations(range(len(ss)),w):
        mask=0;joint=ambient
        for i in inds:mask|=masks[i];joint&=points[i]
        checks+=1
        if joint==1 and mask==full:return {'counterexample':[sorted(ss[i])for i in inds],'checks':checks}
    return {'counterexample':None,'checks':checks}

def reduced_check():
    m=5;ss=all_subspaces(m);ps=[s for s in ss if len(s)==4];full=(1<<len(ps))-1
    masks={s:sum(1<<i for i,p in enumerate(ps)if len(p&s)==2)for s in ss}
    points={s:sum(1<<x for x in s)for s in ss};stats=[]
    for d in range(4):
        fixed=frozenset(range(1<<d));candidates=[s for s in ss if len(s)<=1<<d and s!=fixed]
        cms=[masks[s]for s in candidates];cps=[points[s]for s in candidates];fm=masks[fixed];fp=points[fixed];checks=0;covering=0
        for t in range(4):
            for inds in combinations(range(len(candidates)),t):
                mask=fm
                for i in inds:mask|=cms[i]
                checks+=1
                if mask!=full:continue
                covering+=1;joint=fp
                for i in inds:joint&=cps[i]
                if joint==1:return {'counterexample':[sorted(fixed)]+[sorted(candidates[i])for i in inds]}
        stats.append({'maximum_kernel_dimension':d,'candidates':len(candidates),'representative_families_checked':checks,'plane_covering_representatives':covering})
    return {'counterexample':None,'orbits_scope':'Not one representative per orbit; fixing one largest kernel includes at least one representative of every GL(5,2) orbit. Some orbits checked repeatedly. Hyperplanes handled separately by restriction. Full-space kernels are redundant. Distinct families of size<=4 included.','statistics':stats}
if __name__=='__main__':
    t=time.time();ans={'m4_replay':full_check(4,3),'m5_reduced_exhaustion':reduced_check(),'seconds':time.time()-t}
    Path(__file__).with_name('exact_m5_results.json').write_text(json.dumps(ans,indent=2));print(json.dumps(ans,indent=2))
